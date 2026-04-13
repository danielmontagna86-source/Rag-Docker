import os
import requests
import time

# --- CONFIGURAÇÕES ---
BASE_URL = "http://localhost:3333"
SOURCE_DIR = r"C:\Users\danie\OneDrive\Documentos\protheus-sistema - Copia\protheus-sistema"
EXTENSIONS = (".prw", ".tlpp", ".ch", ".prx")

def wait_for_api():
    """Verifica se a API está online antes de começar."""
    print("⏳ Aguardando API ficar online...")
    for _ in range(30):
        try:
            r = requests.get(BASE_URL, timeout=5)
            if r.status_code == 200:
                print("✅ API Online e pronta!")
                return True
        except:
            pass
        time.sleep(2)
    return False

def run_ingest():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Pasta não encontrada: {SOURCE_DIR}")
        return

    if not wait_for_api():
        print("❌ API não respondeu a tempo. Abortando.")
        return

    files = [os.path.join(root, f) for root, _, fs in os.walk(SOURCE_DIR) for f in fs if f.lower().endswith(EXTENSIONS)]
    total = len(files)
    
    print(f"🚀 Iniciando carga de {total} arquivos...")

    for i, path in enumerate(files, 1):
        name = os.path.basename(path)
        try:
            with open(path, 'rb') as f:
                # Aumentamos o timeout para 120s para o caso do banco estar ocupado
                r = requests.post(f"{BASE_URL}/ingest", files={'file': (name, f)}, timeout=120)
            
            if r.status_code == 200:
                print(f"✅ [{i}/{total}] {name}")
            else:
                print(f"⚠️ [{i}/{total}] Falha em {name}: {r.status_code}")
                
        except Exception as e:
            print(f"❌ Erro em {name}: {e}")
        
        # Delay mínimo para o Docker respirar
        time.sleep(0.01)

    print("\n🏆 Ingestão concluída com sucesso!")

if __name__ == "__main__":
    run_ingest()