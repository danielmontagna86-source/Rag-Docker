import chromadb
from rag.embed import embed

client = chromadb.Client()
collection = client.get_or_create_collection("docs")

def add_doc(text):
    collection.add(
        documents=[text],
        embeddings=[embed(text)],
        ids=[str(hash(text))]
    )

def search(query):
    res = collection.query(
        query_embeddings=[embed(query)],
        n_results=3
    )
    # Evita erros se a coleção estiver vazia
    if not res["documents"] or not res["documents"][0]:
        return ["Nenhum contexto encontrado."]
    return res["documents"][0]
