from fastapi import FastAPI, Request
from models.ollama import call_llm
import sys

app = FastAPI(title="Protheus RAG Gateway")

@app.get("/")
async def root():
    return {"status": "online"}

@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    # Contexto "Turbinado" enquanto o ChromaDB não entra em cena
    contexto = (
        "Você é um especialista em Protheus e AdvPL. "
        "A tabela SE1 armazena Contas a Receber. "
        "DbSelectArea seleciona a tabela de trabalho. "
        "RecLock inicia o travamento de registro para gravação (Inclusão/Alteração). "
        "Sempre finalize as operações com MsUnlock()."
    )
    
    prompt_enriquecido = f"Instrução: Use o contexto abaixo para responder.\nContexto: {contexto}\n\nPergunta: {prompt}"
    
    response = call_llm(prompt_enriquecido)
    
    tamanho = len(response)
    print(f"📦 [API] Retornando {tamanho} caracteres.", file=sys.stderr)
    return {"response": response}