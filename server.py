import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from router import route
from rag.ingest import ingest_pdf, ingest_advpl

app = FastAPI()

class Req(BaseModel):
    prompt: str

@app.post("/chat")
def chat(req: Req):
    return {"response": route(req.prompt)}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    ext = file.filename.split('.')[-1].lower()

    if ext == "pdf":
        ingest_pdf(file_location)
    elif ext in ["prw", "tlpp", "ch", "prx"]:
        ingest_advpl(file_location)

    os.remove(file_location)
    return {"status": "sucesso", "mensagem": f"Arquivo {file.filename} processado."}
