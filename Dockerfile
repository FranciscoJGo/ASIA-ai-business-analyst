# Imagen base ligera de Python 3.11
FROM python:3.11-slim

# Evita archivos .pyc y fuerza logs en tiempo real en consola
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes (ej. ChromaDB / SQLite)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias primero (aprovecha caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente y carpeta de datos
COPY src/ ./src/
COPY data/ ./data/

# Exponer puerto estándar de FastAPI
EXPOSE 8000

# Healthcheck nativo para monitoreo del contenedor
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Ejecutar servidor Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]