# 🛠️ Guía Operativa del Equipo

**Proyecto:** AI Business Analyst — Equipo 3
**Empresa ficticia del caso:** TechStore México S.A.

**Para qué sirve este archivo:** que cada integrante pueda (1) instalar el proyecto en su computadora, (2) probarlo localmente, (3) saber exactamente qué archivos y funciones le tocan, y (4) subir su avance a GitHub sin romper el código de los demás.



---

## 0. Reglas de oro 

1. **NUNCA hagas `git push` directo a `main`.** Siempre trabaja en tu rama asignada y entrega con Pull Request.
2. **Edita SOLO los archivos de tu rol** (tabla de la sección 1). Si necesitas un cambio en un archivo ajeno, pídelo en el grupo.
3. **Respeta al pie de la letra los nombres** de archivos, funciones, parámetros, tipos de retorno y campos JSON de la sección 6. El proyecto funciona solo si las 5 piezas encajan.
4. **NUNCA subas el archivo `.env`** ni pegues API Keys en el código, en commits o en capturas de pantalla.
5. **NUNCA subas la carpeta `venv/`.**
6. **Antes de abrir tu Pull Request**, corre tu parte localmente y completa el checklist de la sección 9.
7. **Si cambias una firma o un nombre del contrato, avisa a TODO el grupo.** Un cambio silencioso rompe a otros 4 compañeros.
8. **Si algo falla, lee el error completo** y revisa la sección 10 (Problemas comunes) antes de pedir ayuda. Al pedir ayuda, manda el error completo (copiado, no resumido).

---

## 1. Tabla rápida: ramas y archivos por integrante

Busca tu número, usa **exactamente** el nombre de tu rama y edita **únicamente** los archivos de tu fila.

| Integrante | Rol | Rama de Git | Archivos que te corresponden |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | Backend, Router y Agente | `feat/backend-orquestador` | `src/schemas.py`, `src/router.py`, `src/agent.py`, `src/main.py`, `Dockerfile` |
| **Integrante 2** | Datos, SQL y Cálculos | `feat/datos-sql` | `data/crear_datos.py`, `data/empresa.db`, `data/ventas_q3.csv`, `src/tools/sql_tool.py`, `src/tools/calc_tool.py` |
| **Integrante 3** | RAG y Documentos PDF | `feat/rag-documentos` | `data/pdfs/`, `chroma_db/`, `src/tools/rag_tool.py` (+ el script de ingesta) |
| **Integrante 4** | Frontend Web (Streamlit) | `feat/frontend-ui` | `frontend/app.py` |
| **Integrante 5** | Evaluación y Docs | `feat/eval-docs` | `eval/run_eval.py`, `docs/ARQUITECTURA.md`, `docs/diagrama_arquitectura.png` |

> Archivos compartidos que **nadie edita a su gusto**: `README.md` (entrega del profesor), `requirements.txt` (ver sección 10), `.gitignore`, `.env.example`.

---

## 2. Estructura esperada del repositorio

```text
ai-business-analyst/
├── README.md                 # Entrega para el profesor (no tocar)
├── GUIA_EQUIPO.md            # Este archivo
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile                # Integrante 1
├── src/
│   ├── __init__.py
│   ├── schemas.py            # Integrante 1
│   ├── router.py             # Integrante 1
│   ├── agent.py              # Integrante 1
│   ├── main.py               # Integrante 1
│   └── tools/
│       ├── __init__.py
│       ├── sql_tool.py       # Integrante 2
│       ├── calc_tool.py      # Integrante 2
│       └── rag_tool.py       # Integrante 3
├── data/
│   ├── crear_datos.py        # Integrante 2
│   ├── empresa.db            # Integrante 2
│   ├── ventas_q3.csv         # Integrante 2
│   └── pdfs/                 # Integrante 3 (4 PDFs)
├── chroma_db/                # Integrante 3
├── frontend/
│   └── app.py                # Integrante 4
├── eval/
│   └── run_eval.py           # Integrante 5
└── docs/
    ├── ARQUITECTURA.md       # Integrante 5
    └── diagrama_arquitectura.png
```

> Si algún archivo `__init__.py` falta en `src/` o `src/tools/`, avisa al Integrante 1 para que lo agregue. Sin ellos, los imports `from src.tools.sql_tool import ...` pueden fallar.

---

## 3. Parte 1: Instalación en tu computadora (solo se hace una vez)

Sigue estos 6 pasos **en estricto orden** desde tu terminal.

### 3.1 Descargar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO_EN_GITHUB>
cd ai-business-analyst
```

### 3.2 Verificar que tienes Python 3.10 o 3.11

```bash
python --version
```

En Mac/Linux usa `python3 --version`.

> ⚠️ **Debe ser 3.10 o 3.11.** El código usa tipos como `list[dict] | None`, que no funcionan en Python 3.9 o anterior. Si tienes otra versión (por ejemplo 3.12 o 3.13), algunas librerías pesadas (PyTorch, ChromaDB) pueden fallar al instalarse. Instala 3.11 desde https://www.python.org/downloads/ antes de continuar.

### 3.3 Crear y activar el entorno virtual (venv)

Esto aísla las librerías del proyecto para que no choquen con otras cosas de tu computadora.

**En Windows (PowerShell o CMD):**

```bash
python -m venv venv
venv\Scripts\activate
```

> **Si Windows da error de permisos en PowerShell:** ejecuta
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
> y vuelve a correr `venv\Scripts\activate`.

**En Mac / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

✅ Sabrás que funcionó porque aparecerá `(venv)` al principio de la línea de tu terminal.

### 3.4 Instalar las dependencias del proyecto

Con el `(venv)` activo:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Tardará varios minutos porque descarga PyTorch/Sentence-Transformers y ChromaDB. **No cierres la terminal** mientras instala.

### 3.5 Configurar tus llaves secretas (`.env`)

1. En la carpeta raíz del proyecto, **duplica** el archivo `.env.example` y cámbiale el nombre a `.env`.
2. Ábrelo con VS Code o Bloc de Notas y pega las API Keys que compartimos en el grupo de WhatsApp:
   - `CLOUD_API_KEY`
   - `LANGFUSE_PUBLIC_KEY`
   - `LANGFUSE_SECRET_KEY`
3. Si `.env.example` trae más variables además de esas, **cópialas también** y pregunta en el grupo qué valor poner.

> ⚠️ **MUY IMPORTANTE:** nunca subas el archivo `.env` a GitHub. El `.gitignore` ya está configurado para ignorarlo, pero verifica con `git status` antes de cada commit que `.env` **no** aparezca en la lista.

### 3.6 Instalar Ollama y el modelo de Hugging Face (para el Modo Local)

Esto permite ejecutar el modelo open-weight sin internet y sin gastar créditos de API.

1. Descarga e instala Ollama desde https://ollama.com.
2. Abre una terminal **nueva** y ejecuta:

   ```bash
   ollama run hf.co/Qwen/Qwen2.5-7B-Instruct-GGUF
   ```

3. Espera a que termine de descargar (~4.7 GB). Cuando aparezca `>>> Send a message`, escribe `/bye` y presiona Enter.
4. Asegúrate de que el ícono de Ollama esté corriendo en la barra de tareas (Windows) o en la barra superior (Mac) cuando pruebes el modo local.

> 📌 **Nombre exacto del modelo para todo el equipo:** `hf.co/Qwen/Qwen2.5-7B-Instruct-GGUF`. El Integrante 1 debe usar **ese mismo texto** como nombre del modelo en `src/router.py`; si no coincide, Ollama responderá "model not found".
>
> Requisitos aproximados para el modo local: unos **8 GB de RAM libres** y **~5 GB de disco**. Si tu computadora no lo soporta, avísalo en el grupo: puedes seguir trabajando tu parte usando solo el modo `cloud`.

---

## 4. Parte 2: Cómo probar que todo funciona en tu máquina

Cada vez que vayas a programar o probar, abre **dos terminales** en la carpeta `ai-business-analyst`, **ambas con `(venv)` activado**.

**Terminal 1: levantar el Backend (FastAPI)**

```bash
uvicorn src.main:app --reload --port 8000
```

Abre http://localhost:8000/docs en tu navegador. Si ves la interfaz Swagger con los endpoints `/health` y `/ask`, el backend funciona.

**Terminal 2: levantar el Frontend (Streamlit)**

```bash
streamlit run frontend/app.py
```

Se abrirá una pestaña en http://localhost:8501.

> Si el puerto 8000 o 8501 está ocupado, cierra la terminal anterior que lo esté usando. **No cambies los puertos**: el frontend y el script de evaluación apuntan a `localhost:8000`.

---

## 5. Parte 3: Flujo de trabajo en GitHub (ramas, push y Pull Requests)

> **REGLA DE ORO: NUNCA hagas `git push` directo a `main`. Siempre trabaja en tu rama asignada.**

### A. Crear tu rama antes de empezar a programar

Ejecuta esto **una sola vez** para crear tu rama a partir de `main`:

```bash
git checkout main
git pull origin main
git checkout -b tu-rama-asignada
```

Ejemplo para el Integrante 2: `git checkout -b feat/datos-sql`

Para confirmar en qué rama estás parado, en cualquier momento:

```bash
git branch
```

La rama activa aparece con un asterisco `*` (y en verde en la mayoría de terminales).

### B. Subir tus avances a GitHub (Add → Commit → Push)

Cada vez que termines una función o avances en tu parte:

**1. Verifica qué archivos modificaste** (asegúrate de no haber tocado archivos de otro compañero):

```bash
git status
```

**2. Prepara tus archivos.** Lo más seguro es agregar **solo tus archivos**:

```bash
git add src/tools/sql_tool.py
git add data/
```

(Cambia las rutas por las de tu rol.) Si prefieres usar `git add .`, hazlo **solo después de revisar `git status`** y confirmar que no aparecen `.env`, `venv/` ni archivos de otros integrantes.

**3. Guarda una versión (commit)** con un mensaje descriptivo:

```bash
git commit -m "feat: descripcion clara de lo que agregaste"
```

**4. Sube tus cambios a tu rama en GitHub:**

La **primera vez** que subes la rama:

```bash
git push -u origin tu-rama-asignada
```

Las **siguientes veces** en esa misma rama:

```bash
git push
```

### C. Unir tu trabajo al proyecto principal (Pull Request)

Cuando tu módulo esté probado y funcionando:

1. Entra al repositorio en GitHub desde tu navegador.
2. Verás un aviso amarillo/verde arriba con el nombre de tu rama y un botón **"Compare & pull request"**. Haz clic ahí.
3. Escribe brevemente **qué probaste** y haz clic en **"Create pull request"**.
4. Avisa en el grupo de WhatsApp para que el **Integrante 1** revise que no haya conflictos y presione **"Merge pull request"** hacia `main`.

### D. Actualizar tu computadora con los avances de tus compañeros

Cuando otro integrante ya haya subido su parte a `main` y tú necesites su código:

```bash
git checkout main
git pull origin main
git checkout tu-rama-asignada
git merge main
```

> Antes de hacer `git checkout main` asegúrate de haber hecho commit de tus cambios, o Git te lo impedirá.

### E. Si Git te marca "conflicto" al hacer `merge`

1. **No entres en pánico y no borres nada.**
2. Ejecuta `git status`: verás los archivos en conflicto.
3. Si el conflicto es en un archivo **tuyo**, ábrelo en VS Code, elige qué versión conservar (aparecen las marcas `<<<<<<<`, `=======`, `>>>>>>>`), guarda, y luego:

   ```bash
   git add archivo_resuelto
   git commit
   ```

4. Si el conflicto es en un archivo **de otra persona**, no lo resuelvas tú: **avisa en el grupo**. Probablemente alguien editó un archivo que no le correspondía.
5. Si te perdiste, puedes cancelar el merge con `git merge --abort` y pedir ayuda.

---

## 6. Contratos de código (lo que NO se puede cambiar)

Para que el código de los 5 embone sin errores, se respetan **estrictamente** los nombres de archivos, funciones, parámetros y tipos de retorno que aparecen aquí.

### 6.1 Valores permitidos de `modo_modelo`

| Valor | Significado |
| :--- | :--- |
| `"local"` | Modo Privado Local (Hugging Face vía Ollama, `http://localhost:11434/v1`) |
| `"cloud"` | Modo Avanzado Nube (API externa) |

Siempre en minúsculas, sin espacios. Los usan el frontend, el router y el script de evaluación.

### 6.2 Nombres exactos de las 3 herramientas

Estos nombres son los que el agente invoca y los que aparecen en `herramientas_usadas` (y que el script de evaluación compara):

| Tipo de pregunta | Nombre de la herramienta | Archivo |
| :--- | :--- | :--- |
| SQL | `ejecutar_consulta_sql` | `src/tools/sql_tool.py` |
| Cálculo | `calcular_estadisticas_csv` | `src/tools/calc_tool.py` |
| RAG / documentos | `buscar_documentos_empresa` | `src/tools/rag_tool.py` |

Una pregunta **mixta** debe usar **dos o más** de estas herramientas.

### 6.3 Esquemas Pydantic (`src/schemas.py`)

```python
from pydantic import BaseModel

class PreguntaRequest(BaseModel):
    pregunta: str
    modo_modelo: str

class RespuestaAnalista(BaseModel):
    respuesta: str
    herramientas_usadas: list[str]
    modelo_utilizado: str
    datos_tabla: list[dict] | None = None
    fuentes_documentos: list[str] | None = None
```

### 6.4 Endpoints del backend (`src/main.py`)

| Método | Ruta | Entrada | Salida |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | nada | HTTP 200 con JSON (ej. `{"status": "ok"}`). El frontend lo considera "sano" si responde 200. |
| `POST` | `/ask` | JSON `{"pregunta": "...", "modo_modelo": "local" \| "cloud"}` | JSON con la forma de `RespuestaAnalista` |

Ejemplo de respuesta de `/ask`:

```json
{
  "respuesta": "Las ventas de Guadalajara en Q3 fueron ...",
  "herramientas_usadas": ["ejecutar_consulta_sql"],
  "modelo_utilizado": "hf.co/Qwen/Qwen2.5-7B-Instruct-GGUF",
  "datos_tabla": [{"sucursal": "Guadalajara", "total": 123456.78}],
  "fuentes_documentos": null
}
```

### 6.5 Firma de `ejecutar_consulta_sql` (`src/tools/sql_tool.py`)

```python
def ejecutar_consulta_sql(query_sql: str) -> str:
    """
    Ejecuta una consulta SELECT en data/empresa.db y devuelve los resultados en formato JSON/texto.

    GUARDRAIL DE SEGURIDAD: Debe bloquear y rechazar cualquier query que contenga
    DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE o ATTACH.

    Incluir en el docstring de la función el esquema exacto de las tablas y columnas
    para que el LLM sepa qué consultar.
    """
```

### 6.6 Firma de `calcular_estadisticas_csv` (`src/tools/calc_tool.py`)

```python
def calcular_estadisticas_csv(operacion: str, columna: str, filtro_columna: str = "", filtro_valor: str = "") -> str:
    """
    Realiza cálculos exactos (suma, promedio, maximo, minimo, conteo) usando Pandas
    sobre data/ventas_q3.csv, aplicando un filtro opcional
    (ej. filtro_columna='sucursal', filtro_valor='Guadalajara').
    """
```

Valores válidos de `operacion`: `suma`, `promedio`, `maximo`, `minimo`, `conteo` (en minúsculas y sin acentos, tal cual).

### 6.7 Firma de `buscar_documentos_empresa` (`src/tools/rag_tool.py`)

```python
def buscar_documentos_empresa(consulta: str) -> str:
    """
    Busca en chroma_db los 3 fragmentos más relevantes para la consulta del usuario.
    Devuelve el texto de cada fragmento indicando explícitamente el archivo PDF
    de origen y número de página.
    """
```

### 6.8 Función del router (`src/router.py`)

```python
def get_llm(modo: str):
    """Devuelve el LLM según modo: 'local' (Ollama) o 'cloud' (API externa)."""
```

### 6.9 Tablas y columnas de datos

Las tablas son `sucursales`, `productos` y `ventas` (en `data/empresa.db`), y la misma información de ventas va en `data/ventas_q3.csv`.

> 🔴 **Punto crítico:** los **nombres exactos de las columnas** los define el **Integrante 2**. Debe publicarlos en el grupo **lo antes posible** (y dejarlos en el docstring de `ejecutar_consulta_sql`), porque de ahí dependen el agente (Integrante 1), las preguntas de prueba (Integrante 5) y las preguntas rápidas del frontend (Integrante 4). Una vez publicados **no se cambian**.

---

## 7. Responsabilidades detalladas por integrante

### 🧩 Integrante 1: Arquitecto Backend, Model Router y Orquestador

**Rama:** `feat/backend-orquestador`
**Archivos:** `src/schemas.py`, `src/router.py`, `src/agent.py`, `src/main.py`, `Dockerfile`

**Responsabilidades:**

- Implementar `get_llm(modo: str)` en `src/router.py` para alternar entre **Ollama** (`http://localhost:11434/v1`) y la **API externa**.
- Definir los esquemas Pydantic de la sección 6.3 en `src/schemas.py`.
- Implementar el agente en `src/agent.py` (LangGraph / LangChain Tool Calling) conectando las 3 herramientas (`ejecutar_consulta_sql`, `calcular_estadisticas_csv`, `buscar_documentos_empresa`) y **forzando salida estructurada** (`RespuestaAnalista`).
- Exponer `POST /ask` y `GET /health` en `src/main.py` con **trazabilidad en Langfuse**.
- Crear el `Dockerfile`.
- Como revisor de Pull Requests: validar que no haya conflictos antes de hacer merge a `main`.

> 💡 Mientras las herramientas de los Integrantes 2 y 3 no estén listas, puedes crear funciones "de mentira" (stubs) **en tu rama** que respeten las firmas exactas de la sección 6, y reemplazarlas por las reales al hacer merge. **No subas esos stubs a `src/tools/`**, para no chocar con los archivos reales.

### 🗄️ Integrante 2: Ingeniero de Datos Estructurados, SQL y Cálculos

**Rama:** `feat/datos-sql`
**Archivos:** `data/crear_datos.py`, `data/empresa.db`, `data/ventas_q3.csv`, `src/tools/sql_tool.py`, `src/tools/calc_tool.py`

**Responsabilidades:**

- Crear `data/crear_datos.py` y **ejecutarlo** para generar `data/empresa.db` (SQLite) y `data/ventas_q3.csv` con datos realistas de **TechStore México S.A.**
  - Tablas: `sucursales`, `productos`, `ventas`.
  - **Al menos 200 registros** en **5 ciudades**: Guadalajara, CDMX, Monterrey, Puebla, Querétaro.
  - **Subir tanto el script como los archivos `.db` y `.csv` generados.**
- Programar `src/tools/sql_tool.py` con la firma exacta de la sección 6.5, incluyendo:
  - El **guardrail**: rechazar cualquier query que contenga `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE` o `ATTACH`.
  - El **esquema exacto** de tablas y columnas dentro del docstring.
- Programar `src/tools/calc_tool.py` con la firma exacta de la sección 6.6, usando **Pandas** sobre `data/ventas_q3.csv`.
- **Publicar el esquema de columnas en el grupo cuanto antes** (ver 6.9).

### 📄 Integrante 3: Ingeniero de RAG y Embeddings (Hugging Face)

**Rama:** `feat/rag-documentos`
**Archivos:** `data/pdfs/`, `chroma_db/`, `src/tools/rag_tool.py`

**Responsabilidades:**

- Crear **4 documentos PDF** de TechStore México S.A. dentro de `data/pdfs/`:
  1. `politica_descuentos_2026.pdf`: reglas de descuentos por volumen, aprobación gerencial, márgenes mínimos.
  2. `reporte_financiero_q3.pdf`: resumen ejecutivo, metas trimestrales, retos logísticos.
  3. `manual_operaciones_sucursales.pdf`: horarios, protocolos de inventario, KPIs por tienda.
  4. `plan_expansion_2027.pdf`: nuevas aperturas, presupuesto asignado, criterios de ubicación.
- Crear un **script de ingesta** que:
  - lea los PDFs con `pypdf`,
  - los divida en chunks de **~500 caracteres con overlap de 50**,
  - genere embeddings **localmente** con `HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")`,
  - guarde la base persistente en `chroma_db/`.
- **Subir `data/pdfs/` y `chroma_db/` a GitHub.**
- Programar `src/tools/rag_tool.py` con la firma exacta de la sección 6.7. Cada fragmento devuelto debe indicar **explícitamente el archivo PDF de origen y el número de página**.

> ⚠️ `chroma_db/` contiene archivos binarios: **solo el Integrante 3 la modifica**. Si alguien más la toca, habrá conflictos imposibles de resolver a mano. Si regeneras la base, hazlo completo y sube todo en un solo commit.

### 🖥️ Integrante 4: Desarrollador Frontend (Interfaz Web)

**Rama:** `feat/frontend-ui`
**Archivos:** `frontend/app.py`

**Responsabilidades:**

- Desarrollar la app web en **Streamlit** (`frontend/app.py`).
- **Barra lateral (`st.sidebar`):**
  - Selector de modo de inferencia: **"Modo Privado Local (Hugging Face)"** (valor `"local"`) vs **"Modo Avanzado Nube (API)"** (valor `"cloud"`).
  - Indicador visual de salud del backend consultando `GET http://localhost:8000/health`.
  - Botones de preguntas rápidas de demostración: **1 de SQL, 1 de Cálculo, 1 de RAG, 1 Híbrida**.
- **Área principal:**
  - Historial de chat con `st.chat_message`.
  - Al enviar una pregunta, hace `POST http://localhost:8000/ask` con JSON `{"pregunta": ..., "modo_modelo": ...}`.
  - Muestra: la respuesta ejecutiva, **insignias** (`st.badge` o `st.info`) con el modelo usado y las herramientas invocadas, una **tabla** (`st.dataframe`) si `datos_tabla` no está vacío, y las **fuentes PDF** si `fuentes_documentos` no está vacío.

> 💡 Puedes desarrollar todo contra respuestas simuladas (un diccionario con la forma de la sección 6.4) mientras el backend no esté listo. Maneja también el caso de **error de conexión** (backend apagado) con un mensaje claro en pantalla, no con un traceback.

### 📊 Integrante 5: Ingeniero de Evaluación, Observabilidad y Documentación Final

**Rama:** `feat/eval-docs`
**Archivos:** `eval/run_eval.py`, `docs/ARQUITECTURA.md` (y `docs/diagrama_arquitectura.png`)

**Responsabilidades:**

- **Observabilidad:** verificar junto con el Integrante 1 que las llamadas a FastAPI y al agente queden registradas en **Langfuse** (trazas, tokens, latencia, costos) y **guardar capturas de pantalla** para la presentación.
- **Evaluación automatizada (`eval/run_eval.py`):** un script que envíe **12 preguntas de prueba** a `POST http://localhost:8000/ask` (**3 de SQL, 3 de Cálculos, 3 de RAG, 3 Mixtas**) y calcule e imprima en consola/JSON:
  - **Tool-use Success (%):** porcentaje de preguntas donde el agente eligió la herramienta esperada.
  - **Latencia promedio (s):** comparativa entre `modo_modelo="local"` y `modo_modelo="cloud"`.
  - **Tasa de éxito de esquema (%):** respuestas que cumplieron con `RespuestaAnalista`.
- **Documentación arquitectónica (`docs/ARQUITECTURA.md`):** redactar el entregable teórico completo siguiendo la rúbrica de la materia:
  - **Diagrama arquitectónico completo** (exportado a `docs/diagrama_arquitectura.png`).
  - **Justificación de los 23 componentes arquitectónicos:** qué usamos, por qué, qué alternativas había y qué componentes omitimos por simplicidad.
  - **Análisis de seguridad:** Prompt Injection, guardrails SQL, privacidad de datos PII con inferencia local.

> 💡 Las preguntas de prueba dependen de las columnas definidas por el Integrante 2 y de los PDFs del Integrante 3. Redáctalas en cuanto tengan publicados esos datos.

---

## 8. Orden sugerido de trabajo y dependencias

Quién necesita a quién:

| Quien depende | De quién | Qué necesita |
| :--- | :--- | :--- |
| Integrante 1 (agente) | Integrantes 2 y 3 | Las 3 herramientas funcionando |
| Integrante 4 (frontend) | Integrante 1 | `/health` y `/ask` respondiendo |
| Integrante 5 (eval) | Integrantes 1, 2 y 3 | Backend + datos + PDFs para armar preguntas |

**Orden sugerido de merges a `main`** (recomendación para minimizar conflictos):

1. **Integrante 2** y **Integrante 3** (datos y herramientas, no dependen de nadie).
2. **Integrante 1** (backend y agente, ya con las herramientas reales).
3. **Integrante 4** (frontend contra el backend real).
4. **Integrante 5** (evaluación y documentación final contra todo el sistema).

Mientras esperas a otros, trabaja contra el **contrato** (sección 6): ese es el propósito de que las firmas sean exactas.

---

## 9. ✅ Checklist antes de abrir tu Pull Request

Marca mentalmente cada punto:

- [ ] Estoy en **mi rama asignada** (`git branch` muestra `*` en ella), no en `main`.
- [ ] `git status` muestra **solo archivos de mi rol**.
- [ ] **No** aparecen `.env`, `venv/` ni archivos de otros integrantes.
- [ ] Mis funciones tienen **exactamente** los nombres, parámetros y tipos de la sección 6.
- [ ] Probé mi parte localmente y **no marca errores**.
- [ ] Hice `git pull origin main` y `git merge main` en mi rama, y no hay conflictos.
- [ ] Si instalé una librería nueva, la agregué a `requirements.txt` (sección 10) y **avisé en el grupo**.
- [ ] Escribí en la descripción del Pull Request **qué probé**.

---

## 10. 🆘 Solución rápida a problemas comunes

**`ModuleNotFoundError: No module named 'src'`**
Ejecuta los comandos desde la carpeta **raíz** (`ai-business-analyst/`), no desde dentro de `src/` ni `frontend/`. Verifica también que `src/__init__.py` exista.

**`ModuleNotFoundError` de cualquier otra librería (por ejemplo `fastapi`, `streamlit`)**
Casi siempre significa que el `(venv)` **no está activado** en esa terminal. Actívalo (sección 3.3) o vuelve a correr `pip install -r requirements.txt`.

**Error de conexión con el modo local**
Verifica que Ollama esté abierto en segundo plano, o ejecuta `ollama serve` en una terminal aparte. Confirma también que descargaste el modelo (sección 3.6) con `ollama list`.

**`model not found` en modo local**
El nombre del modelo en `src/router.py` no coincide con el descargado. Debe ser `hf.co/Qwen/Qwen2.5-7B-Instruct-GGUF` (revisa con `ollama list`).

**`Address already in use` / puerto ocupado**
Ya hay otra terminal usando el puerto 8000 u 8501. Ciérrala (Ctrl + C) y vuelve a lanzar.

**El frontend dice que el backend no está disponible**
Asegúrate de que la Terminal 1 (`uvicorn`) esté corriendo y de que http://localhost:8000/docs abra en el navegador.

**Instalaste una librería nueva con `pip install ...`**
Agrega **solo esa línea** (con su versión, por ejemplo `nombre-libreria==1.2.3`; la obtienes con `pip show nombre-libreria`) al final de `requirements.txt`, haz commit y **avisa en el grupo** para que todos corran `pip install -r requirements.txt`.

> ⚠️ **Evita `pip freeze > requirements.txt`.** Ese comando reescribe el archivo completo con todas las librerías de tu computadora, y si dos personas lo hacen, el archivo se vuelve un conflicto enorme en Git. Añadir una sola línea evita ese problema.

**Subí algo por error (por ejemplo `.env` con llaves)**
**No lo borres y ya**: las llaves quedan en el historial de GitHub. Avisa **de inmediato** en el grupo para **regenerar las API Keys** y limpiar el historial.

**Hice commit en `main` por error**
No hagas push. Avisa en el grupo; se puede mover ese commit a tu rama sin perder nada.

---

## 11. 🚫 Lo que NO hay que hacer

- ❌ `git push` directo a `main`.
- ❌ Editar archivos de otro integrante "para arreglar algo rápido".
- ❌ Cambiar nombres de funciones, parámetros, campos JSON o valores de `modo_modelo`.
- ❌ Subir `.env`, `venv/` o API Keys.
- ❌ Hacer `pip freeze > requirements.txt`.
- ❌ Cambiar los puertos (`8000` backend, `8501` frontend).
- ❌ Resolver en silencio un conflicto en un archivo que no es tuyo.
- ❌ Esperar al último momento para probar tu parte con las demás.

---

**Cualquier duda sobre esta guía → pregunta en el grupo de WhatsApp antes de programar.** 🚀