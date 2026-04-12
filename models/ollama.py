import requests

def call_llm(prompt):
    res = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]
