import requests
import json
import time
import os

def call_llm(prompt_text):
    """
    Chama o modelo LLM local. Adaptável para rede interna Docker ou Host Windows.
    """
    base_url = os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434")
    url = f"{base_url}/api/generate"
    
    payload = {
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False
    }
    
    print(f"\n🚀 [TELEMETRIA] Conectando ao Ollama em: {url}")
    
    inicio = time.time()
    try:
        # TIMEOUT AUMENTADO PARA 300s (5 Minutos) PARA SUPORTAR A CPU
        res = requests.post(url, json=payload, timeout=300)
        res.raise_for_status()
        
        tempo_total = time.time() - inicio
        print(f"✅ [TELEMETRIA] Resposta recebida em {tempo_total:.2f}s.")
        
        return res.json().get("response", "")
        
    except Exception as e:
        erro_msg = f"❌ [ERRO] Falha na integração Ollama ({url}): {str(e)}"
        print(erro_msg)
        return erro_msg