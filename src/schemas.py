from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PreguntaRequest(BaseModel):
    pregunta: str = Field(..., min_length=3, max_length=1000)
    modo_modelo: str = Field(default="cloud", pattern="^(local|cloud)$")


class RespuestaAnalista(BaseModel):
    respuesta: str
    herramientas_usadas: List[str] = Field(default_factory=list)
    modelo_utilizado: str
    datos_tabla: Optional[List[Dict[str, Any]]] = Field(default=None)
    fuentes_documentos: Optional[List[str]] = Field(default=None)