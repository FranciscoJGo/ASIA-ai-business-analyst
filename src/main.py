import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.schemas import PreguntaRequest, RespuestaAnalista
from src.agent import ejecutar_agente

# Cargar variables de entorno (.env)
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TechStore-API")

# Importación segura y retrocompatible de Langfuse
try:
    from langfuse.langchain import CallbackHandler
    LANGFUSE_DISPONIBLE = True
except ImportError:
    try:
        from langfuse.callback import CallbackHandler
        LANGFUSE_DISPONIBLE = True
    except ImportError:
        LANGFUSE_DISPONIBLE = False
        logger.warning("Langfuse no está instalado. La trazabilidad estará deshabilitada.")


def obtener_langfuse_handler():
    """Inicializa el handler de Langfuse si existen credenciales en el entorno."""
    if not LANGFUSE_DISPONIBLE:
        return None
    if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
        try:
            # Langfuse v3+ lee las credenciales automáticamente desde .env
            return CallbackHandler()
        except TypeError:
            # Fallback para Langfuse v2
            return CallbackHandler(
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            )
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando API AI Business Analyst - TechStore México S.A.")
    yield
    logger.info("Apagando API AI Business Analyst...")


app = FastAPI(
    title="TechStore México S.A. - AI Business Analyst API",
    description="Orquestador Multi-Agente con Model Router (Cloud/Local), LangGraph y Langfuse.",
    version="1.0.0",
    lifespan=lifespan
)

# Habilitar CORS por si el equipo conecta un frontend (Streamlit/React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Monitoreo"])
async def health_check():
    """Verifica que el servicio esté activo y reporta estado de observabilidad."""
    return {
        "status": "ok",
        "empresa": "TechStore México S.A.",
        "langfuse_configurado": bool(os.getenv("LANGFUSE_PUBLIC_KEY"))
    }


@app.post("/ask", response_model=RespuestaAnalista, tags=["Analista IA"])
async def preguntar_analista(request: PreguntaRequest):
    """
    Endpoint principal: recibe una consulta de negocio, enruta al modelo seleccionado
    ('cloud' o 'local'), ejecuta herramientas necesarias y devuelve JSON estructurado.
    """
    logger.info(f"Nueva consulta recibida | Modo: {request.modo_modelo} | Pregunta: '{request.pregunta}'")
    
    callbacks = []
    langfuse_handler = obtener_langfuse_handler()
    if langfuse_handler:
        callbacks.append(langfuse_handler)

    try:
        respuesta = ejecutar_agente(
            pregunta=request.pregunta,
            modo_modelo=request.modo_modelo,
            callbacks=callbacks
        )
        return respuesta

    except ConnectionError as ce:
        logger.error(f"Error de conexión con proveedor LLM ({request.modo_modelo}): {ce}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No se pudo conectar con el servidor del modelo en modo '{request.modo_modelo}'. "
                   f"Verifica que Ollama esté corriendo si usas modo local."
        )
    except Exception as e:
        logger.exception("Error inesperado durante la orquestación del agente.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno en el orquestador: {str(e)}"
        )
    finally:
        # Asegura que las trazas asíncronas se envíen a Langfuse antes de cerrar el ciclo
        if langfuse_handler:
            try:
                langfuse_handler.flush()
            except Exception as flush_err:
                logger.warning(f"No se pudo hacer flush en Langfuse: {flush_err}")