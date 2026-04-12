from rag.search import search
from models.ollama import call_llm
from cache.redis_cache import get_cache, set_cache

def route(prompt):
    cached = get_cache(prompt)
    if cached:
        return cached

    docs = search(prompt)
    context = "\n".join(docs)

    enriched = f"""
    Contexto:
    {context}

    Pergunta:
    {prompt}
    """

    response = call_llm(enriched)
    set_cache(prompt, response)

    return response
