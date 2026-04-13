from fastapi import FastAPI, Request
from models.ollama import call_llm
import sys

app = FastAPI(title="Protheus RAG Gateway")

@app.get("/")
async def root():
    return {"status": "online", "message": "API RAG Operacional"}

@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    contexto = "[CONTEXTO DOS FONTES ADVPL]"
    prompt_enriquecido = f"Contexto: {contexto}\n\nPergunta: {prompt}"
    
    # Chama o Ollama
    response = call_llm(prompt_enriquecido)
    
    # RAIO-X SRE: Imprime as primeiras 200 letras no log do Docker para provar que há texto!
    tamanho = len(response)
    print(f"📦 [API] Retornando {tamanho} caracteres para o cliente.", file=sys.stderr)
    if tamanho > 0:
        print(f"📝 [API] Previa do Texto: {response[:200]}...", file=sys.stderr)
    else:
        print("⚠️ [API] ALERTA: A resposta do Ollama veio VAZIA!", file=sys.stderr)
        
    return {"response": response}