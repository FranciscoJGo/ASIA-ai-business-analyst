import os
from functools import lru_cache
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


def get_llm(modo: str = "cloud") -> BaseChatModel:
    """
    Model Router de TechStore México S.A.
    Enruta dinámicamente entre el modelo local (Ollama / OpenAI-compatible)
    y el modelo en la nube (Google Gemini nativo).
    """
    return _crear_llm_cacheado(modo.strip().lower())


@lru_cache(maxsize=2)
def _crear_llm_cacheado(modo_normalizado: str) -> BaseChatModel:
    if modo_normalizado == "local":
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        ollama_model = os.getenv("OLLAMA_MODEL", "hf.co/Qwen/Qwen2.5-7B-Instruct-GGUF")

        return ChatOpenAI(
            model=ollama_model,
            base_url=ollama_base_url,
            api_key="ollama",
            temperature=0.0,
            max_retries=2,
            timeout=60.0
        )

    elif modo_normalizado == "cloud":
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError(
                "Falta la variable de entorno GEMINI_API_KEY. "
                "Configúrala en tu archivo .env para usar modo='cloud'."
            )

        gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

        # Los modelos '-lite' usan valores de muestreo fijos; evitar pasar temperature elimina el UserWarning
        kwargs_modelo = {
            "model": gemini_model,
            "google_api_key": gemini_api_key,
            "max_retries": 2,
            "timeout": 90.0,
        }
        if "lite" not in gemini_model.lower():
            kwargs_modelo["temperature"] = 0.0

        return ChatGoogleGenerativeAI(**kwargs_modelo)

    else:
        raise ValueError(
            f"Modo de modelo no válido: '{modo_normalizado}'. Opciones permitidas: 'local' o 'cloud'."
        )