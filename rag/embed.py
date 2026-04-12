from sentence_transformers import SentenceTransformer

# Modelo otimizado para busca semântica e código-fonte
# 'all-MiniLM-L6-v2' é rápido e muito eficiente para grandes volumes de arquivos
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed(text):
    """
    Gera embeddings localmente sem depender de API externa.
    """
    embedding = model.encode(text)
    return embedding.tolist()
