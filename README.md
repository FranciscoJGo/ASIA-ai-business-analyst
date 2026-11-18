# AI Business Analyst — Proyecto Final
**Universidad de Guadalajara | Licenciatura en Inteligencia Artificial y Ciencia de Datos**  
**Materia:** Arquitectura de Sistemas de Inteligencia Artificial
**Equipo 3** 
### 1. Francisco de Jesus Gonzalez Lopez
### 2.
### 3.
### 4.
### 5.


### Paso 1: Descargar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO_EN_GITHUB>
cd ai-business-analyst

---

## 1. Contexto Académico y Objetivo del Sistema

Este proyecto corresponde al **Equipo 3 – AI Business Analyst** de la materia *Arquitectura de Sistemas de Inteligencia Artificial*. El objetivo no es hacer un simple chatbot, sino diseñar, implementar y defender una **arquitectura moderna de IA completa, observable, evaluable y segura** bajo el principio: `Problema → Requerimientos → Arquitectura → Tecnologías → Implementación`.

### ¿Qué hace nuestro sistema?
Es un **Analista Empresarial Inteligente** para una cadena ficticia de tiendas comerciales en México (**"TechStore México S.A."**). Responde preguntas de negocio combinando información estructurada y no estructurada mediante un **Agente Orquestador** que decide qué herramienta invocar:

1. **Herramienta SQL (`sql_tool.py`):** Consulta la base de datos relacional `data/empresa.db` (SQLite) mediante sentencias `SELECT` seguras para obtener ventas, inventario, productos y desempeño por sucursal.
2. **Herramienta de Análisis y Cálculos (`calc_tool.py`):** Ejecuta cálculos matemáticos y estadísticos exactos con `Pandas` sobre `data/ventas_q3.csv` (evitando errores aritméticos del LLM).
3. **Herramienta RAG (`rag_tool.py`):** Realiza búsqueda semántica en documentos internos PDF (políticas, reportes trimestrales, manuales) almacenados en `chroma_db/` usando embeddings locales de Hugging Face.
4. **Model Router (`router.py`):** Permite alternar dinámicamente entre:
   * **Modo Local (`local`):** Modelo *open-weight* de **Hugging Face** (`Qwen2.5-7B-Instruct-GGUF`) ejecutado localmente mediante **Ollama**. Garantiza **privacidad de datos (PII) y costo $0 por consulta**.
   * **Modo Nube (`cloud`):** Modelo frontera vía API (`gemini-2.5-flash` / OpenAI compatible) para consultas que requieren razonamiento complejo o síntesis extensa.

### Decisiones Arquitectónicas Clave (Lo que NO usamos y por qué)
* **Sin Fine-Tuning:** Los datos de negocio (ventas, políticas) cambian constantemente; actualizar SQL o re-indexar un PDF en RAG es inmediato y barato, mientras que reentrenar pesos es lento y costoso. Los modelos actuales de Hugging Face ya soportan *Tool Calling* de forma nativa.
* **Sin Multi-Agent ni MCP:** Un solo agente orquestador con 3 herramientas bien definidas en Python reduce latencia, costos de tokens y complejidad innecesaria.
* **SQLite y ChromaDB embebidos:** Se guardan como archivos dentro del repositorio para que los 5 integrantes puedan clonar y ejecutar el proyecto en sus computadoras sin configurar servidores externos de bases de datos.

---

## 2. Arquitectura y Flujo de Datos

```text
[Usuario (Streamlit UI)]
         │  POST /ask {pregunta, modo_modelo}
         ▼
[Backend API (FastAPI + Pydantic Validation)]
         │
         ▼
[Model Router] ──► Ruta Local: Hugging Face (Qwen2.5 vía Ollama) [Privacidad / Costo $0]
         │     ──► Ruta Nube:  API Externa (Gemini / OpenAI)       [Alta Complejidad]
         ▼
[AI Orchestrator (LangGraph Agent + Tool Calling)]
    ├──► Tool 1: ejecutar_consulta_sql()     ──► SQLite (data/empresa.db) + Guardrail Read-Only
    ├──► Tool 2: calcular_estadisticas_csv() ──► Pandas (data/ventas_q3.csv)
    └──► Tool 3: buscar_documentos_empresa() ──► ChromaDB + HF Embeddings (data/pdfs/)
         │
         ▼
[Structured Output (Pydantic: RespuestaAnalista)] ──► Trazas a Langfuse (Observabilidad)
         │
         ▼
[Dashboard / Reporte en Streamlit (Texto + Tablas + Herramientas usadas + Fuentes)]


ai-business-analyst/
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Ignora .env, venv y caché
├── Dockerfile                # Empaquetado del backend
├── requirements.txt          # Dependencias compartidas
├── README.md                 # Este documento
├── docs/
│   └── ARQUITECTURA.md       # Documento técnico final (Integrante 5)
├── data/
│   ├── crear_datos.py        # Script que genera empresa.db y ventas_q3.csv (Integrante 2)
│   ├── empresa.db            # Base de datos SQLite (Integrante 2)
│   ├── ventas_q3.csv         # Datos tabulares CSV (Integrante 2)
│   └── pdfs/                 # Documentos internos PDF (Integrante 3)
├── chroma_db/                # Base vectorial generada con ChromaDB (Integrante 3)
├── src/
│   ├── __init__.py
│   ├── schemas.py            # Modelos Pydantic de entrada/salida (Integrante 1)
│   ├── router.py             # Model Router Local vs Nube (Integrante 1)
│   ├── agent.py              # Agente LangGraph + Tool Calling (Integrante 1)
│   ├── main.py               # Servidor FastAPI (Integrante 1)
│   └── tools/
│       ├── __init__.py
│       ├── sql_tool.py       # Herramienta SQL + Guardrails (Integrante 2)
│       ├── calc_tool.py      # Herramienta Cálculos Pandas (Integrante 2)
│       └── rag_tool.py       # Herramienta RAG ChromaDB (Integrante 3)
├── frontend/
│   └── app.py                # Interfaz Streamlit (Integrante 4)
└── eval/
    └── run_eval.py           # Evaluación automática de 12 preguntas (Integrante 5)