import os

# Carrega a chave da variável de ambiente (definida no .env ou no sistema)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi definida. Crie um arquivo .env com base no .env.example.")
