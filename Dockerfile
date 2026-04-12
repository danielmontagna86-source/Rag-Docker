FROM python:3.11-slim

# Dependências de sistema para o modelo local
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/dist/

WORKDIR /app

COPY . .

# Instalamos sentence-transformers para rodar o embedding local
RUN pip install --no-cache-dir fastapi uvicorn requests chromadb pypdf redis numpy python-multipart mcp sentence-transformers torch

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3333"]
