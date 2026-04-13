import requests
import time
import os

def call_llm(prompt_text):
    """
    Motor Qwen 2.5 Coder 1.5B: Especialista em código e veloz em CPU.
    """
    base_url = os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434")
    url = f"{base_url}/api/generate"
    
    payload = {
        "model": "qwen2.5-coder:1.5b",
        "prompt": prompt_text,
        "stream": False,
        "options": {
            "num_predict": 500,  # Limita a resposta para garantir < 60s
            "temperature": 0.3   # Mais foco técnico, menos conversa
        }
    }
    
    print(f"\n🚀 [TELEMETRIA] Conectando ao Qwen Coder em: {url}")
    
    inicio = time.time()
    try:
        res = requests.post(url, json=payload, timeout=300)
        res.raise_for_status()
        
        tempo_total = time.time() - inicio
        print(f"✅ [TELEMETRIA] Resposta recebida em {tempo_total:.2f}s.")
        
        return res.json().get("response", "")
        
    except Exception as e:
        return f"❌ [ERRO] Falha no motor Qwen: {str(e)}"