from fastapi import FastAPI, Request, UploadFile, File
from models.ollama import call_llm
import chromadb
import sys
import os

app = FastAPI(title="Protheus RAG Gateway")

# Configuração do Banco Vetorial persistente dentro do container
CHROMA_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="advpl_sources")

@app.get("/")
async def root():
    return {"status": "online", "fontes_indexados": collection.count()}

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    """Recebe um arquivo .prw/.tlpp e indexa no banco."""
    try:
        content = await file.read()
        text = content.decode('utf-8', errors='ignore')
        
        collection.add(
            documents=[text],
            metadatas=[{"filename": file.filename}],
            ids=[file.filename]
        )
        return {"status": "success", "file": file.filename}
    except Exception as e:
        print(f"❌ Erro na ingestão: {e}", file=sys.stderr)
        return {"status": "error", "detail": str(e)}

@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    
    # 🔍 Busca Semântica: Procura os 3 trechos mais relevantes no seu código
    print(f"🔎 [BUSCA] Localizando contexto para: {prompt}", file=sys.stderr)
    results = collection.query(query_texts=[prompt], n_results=3)
    documentos = results.get("documents", [[]])[0]
    
    if documentos:
        contexto = "\n----- NOVO TRECHO DE CÓDIGO -----\n".join(documentos)
        instrucao = "Baseie sua resposta EXCLUSIVAMENTE nos fontes AdvPL fornecidos abaixo."
    else:
        contexto = "Nenhum fonte encontrado no banco de dados."
        instrucao = "Responda com seu conhecimento geral de Protheus, avisando que não achou fontes específicos."

    prompt_enriquecido = (
        f"Role: Especialista Senior AdvPL/Protheus.\n"
        f"Instrução: {instrucao}\n\n"
        f"CONTEXTO DOS SEUS FONTES:\n{contexto}\n\n"
        f"PERGUNTA: {prompt}"
    )
    
    response = call_llm(prompt_enriquecido)
    return {"response": response}