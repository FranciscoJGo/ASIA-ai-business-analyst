import os
import re
import json
from typing import Annotated, TypedDict, List, Dict, Any, Optional

from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from src.router import get_llm
from src.schemas import RespuestaAnalista

# =====================================================================
# 1. IMPORTACIÓN DEFENSIVA DE HERRAMIENTAS (Con Fallbacks / Mocks)
# =====================================================================
try:
    from src.tools.sql_tool import ejecutar_consulta_sql as _sql_fn
except ImportError:
    def _sql_fn(query_sql: str) -> str:
        """Ejecuta una consulta SELECT en data/empresa.db y devuelve los resultados."""
        return json.dumps([
            {"sucursal": "Guadalajara Centro", "ventas_totales": 450000, "estatus": "MOCK_DATA"},
            {"sucursal": "Zapopan Andares", "ventas_totales": 620000, "estatus": "MOCK_DATA"}
        ])

try:
    from src.tools.calc_tool import calcular_estadisticas_csv as _calc_fn
except ImportError:
    def _calc_fn(operacion: str, columna: str, filtro_columna: str = "", filtro_valor: str = "") -> str:
        """Realiza cálculos exactos usando Pandas sobre data/ventas_q3.csv."""
        return (
            f"[MOCK CALC] Operación '{operacion}' sobre columna '{columna}' "
            f"(Filtro: {filtro_columna}={filtro_valor}) -> Resultado: 128540.50 MXN"
        )

try:
    from src.tools.rag_tool import buscar_documentos_empresa as _rag_fn
except ImportError:
    def _rag_fn(consulta: str) -> str:
        """Busca en chroma_db los 3 fragmentos más relevantes en los PDFs internos."""
        return (
            "[MOCK RAG - Politica_Garantias_TechStore_2026.pdf]: Todas las laptops empresariales "
            "cuentan con 24 meses de garantía directa en sucursales de Guadalajara y CDMX."
        )


# Registramos las herramientas con sus nombres canónicos explícitos (independiente del mock)
@tool("ejecutar_consulta_sql")
def sql_tool(query_sql: str) -> str:
    """Ejecuta una consulta SELECT en data/empresa.db y devuelve los resultados en formato JSON."""
    return _sql_fn(query_sql)


@tool("calcular_estadisticas_csv")
def calc_tool(operacion: str, columna: str, filtro_columna: str = "", filtro_valor: str = "") -> str:
    """Realiza cálculos exactos usando Pandas sobre data/ventas_q3.csv (suma, promedio, max, min, conteo)."""
    return _calc_fn(operacion, columna, filtro_columna, filtro_valor)


@tool("buscar_documentos_empresa")
def rag_tool(consulta: str) -> str:
    """Busca en chroma_db los fragmentos más relevantes en los PDFs internos de políticas y manuales."""
    return _rag_fn(consulta)


HERRAMIENTAS = [sql_tool, calc_tool, rag_tool]


# =====================================================================
# 2. DEFINICIÓN DEL ESTADO Y NODOS DE LANGGRAPH
# =====================================================================
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    modo_modelo: str


SYSTEM_PROMPT_ANALISTA = """Eres el AI Business Analyst oficial de TechStore México S.A.
Tu trabajo es responder preguntas de negocio con precisión, rigor analítico y tono ejecutivo.

Reglas de uso de herramientas:
1. Usa `ejecutar_consulta_sql` para consultar datos relacionales en la base de datos SQLite (clientes, sucursales, inventario actual, empleados).
2. Usa `calcular_estadisticas_csv` para hacer cálculos matemáticos o estadísticos exactos sobre las ventas del Q3 (`ventas_q3.csv`). Nunca calcules promedios o sumas grandes mentalmente.
3. Usa `buscar_documentos_empresa` para consultar políticas internas, manuales, contratos o PDFs de la empresa.
4. Si la pregunta es un saludo o conocimiento general que no requiere datos internos, responde directamente sin invocar herramientas.
5. Basa tus conclusiones estrictamente en los datos devueltos por las herramientas."""


def nodo_agente(state: AgentState) -> Dict[str, Any]:
    """Nodo razonador: decide si llamar a una o más herramientas o generar respuesta."""
    llm = get_llm(state["modo_modelo"])
    llm_con_herramientas = llm.bind_tools(HERRAMIENTAS)

    mensajes = [SystemMessage(content=SYSTEM_PROMPT_ANALISTA)] + state["messages"]
    respuesta = llm_con_herramientas.invoke(mensajes)
    return {"messages": [respuesta]}


def construir_grafo():
    """Construye y compila el grafo ReAct de LangGraph."""
    workflow = StateGraph(AgentState)

    workflow.add_node("agente", nodo_agente)
    workflow.add_node("herramientas", ToolNode(HERRAMIENTAS))

    workflow.add_edge(START, "agente")
    workflow.add_conditional_edges(
        "agente",
        tools_condition,
        {
            "tools": "herramientas",
            END: END,
        }
    )
    workflow.add_edge("herramientas", "agente")

    return workflow.compile()


# Instancia compilada reutilizable
grafo_analista = construir_grafo()


# =====================================================================
# 3. UTILIDADES DE PARSEO Y FUNCIÓN PRINCIPAL DE EJECUCIÓN
# =====================================================================
def _extraer_texto_limpio(contenido: Any) -> str:
    """
    Normaliza la salida de texto tanto de modelos OpenAI/Ollama (str)
    como de Gemini 3+ (lista de bloques [{'type': 'text', 'text': '...'}]).
    """
    if isinstance(contenido, str):
        return contenido.strip()
    if isinstance(contenido, list):
        partes = [
            bloque.get("text", "")
            for bloque in contenido
            if isinstance(bloque, dict) and bloque.get("type") == "text"
        ]
        return "\n".join(partes).strip()
    return str(contenido).strip()


def _extraer_metadatos_herramientas(
    mensajes_historial: List[BaseMessage]
) -> tuple[List[str], Optional[List[Dict[str, Any]]], Optional[List[str]]]:
    """
    Audita deterministamente las herramientas ejecutadas y extrae tablas SQL
    y nombres de documentos PDF citados sin consumir llamadas extra al LLM.
    """
    herramientas_usadas: List[str] = []
    datos_tabla: Optional[List[Dict[str, Any]]] = None
    fuentes_set: set[str] = set()

    for msg in mensajes_historial:
        if isinstance(msg, ToolMessage):
            if msg.name and msg.name not in herramientas_usadas:
                herramientas_usadas.append(msg.name)

            contenido_tool = _extraer_texto_limpio(msg.content)

            # Si es salida SQL en JSON, intentar estructurarla como datos_tabla
            if msg.name == "ejecutar_consulta_sql":
                try:
                    parsed = json.loads(contenido_tool)
                    if isinstance(parsed, list) and all(isinstance(r, dict) for r in parsed):
                        datos_tabla = parsed
                except (json.JSONDecodeError, TypeError):
                    pass

            # Detectar nombres de documentos (.pdf, .docx, .csv) mencionados en RAG
            if msg.name == "buscar_documentos_empresa":
                pdfs = re.findall(r"[\w\-]+\.(?:pdf|docx|txt)", contenido_tool, flags=re.IGNORECASE)
                fuentes_set.update(pdfs)

    fuentes_documentos = sorted(list(fuentes_set)) if fuentes_set else None
    return herramientas_usadas, datos_tabla, fuentes_documentos


def ejecutar_agente(
    pregunta: str,
    modo_modelo: str = "cloud",
    callbacks: Optional[List[Any]] = None
) -> RespuestaAnalista:
    """
    Orquesta la ejecución del grafo y estructura la salida final en RespuestaAnalista.
    """
    config = {"callbacks": callbacks} if callbacks else {}

    estado_inicial: AgentState = {
        "messages": [HumanMessage(content=pregunta)],
        "modo_modelo": modo_modelo
    }

    # 1. Ejecutar el ciclo ReAct (Razonamiento + Tool Calling)
    estado_final = grafo_analista.invoke(estado_inicial, config=config)
    mensajes_historial = estado_final["messages"]

    # 2. Auditar herramientas, tablas y fuentes de forma 100% determinista (0 llamadas extra al LLM)
    herramientas_usadas, datos_tabla, fuentes_documentos = _extraer_metadatos_herramientas(
        mensajes_historial
    )

    # 3. Limpiar el texto final generado por el agente
    respuesta_limpia = _extraer_texto_limpio(mensajes_historial[-1].content)

    # 4. Obtener nombre real del modelo instanciado
    llm = get_llm(modo_modelo)
    nombre_modelo = getattr(llm, "model_name", None) or getattr(llm, "model", f"router-{modo_modelo}")

    return RespuestaAnalista(
        respuesta=respuesta_limpia,
        herramientas_usadas=herramientas_usadas,
        modelo_utilizado=str(nombre_modelo),
        datos_tabla=datos_tabla,
        fuentes_documentos=fuentes_documentos
    )