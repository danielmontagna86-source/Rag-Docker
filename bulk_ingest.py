import os
import requests
import time

# Configurações
BASE_URL = "http://localhost:3333/ingest"

# Defina a variável de ambiente SOURCE_DIR ou edite o caminho abaixo
# Exemplo Windows: C:\Users\SeuUsuario\Documentos\protheus-sistema
# Exemplo Linux:   /home/usuario/protheus-sistema
SOURCE_DIR = os.getenv("SOURCE_DIR", r"C:\caminho\para\seus\fontes\protheus")

EXTENSIONS = (".prw", ".tlpp", ".ch", ".prx")

def bulk_upload():
    print(f"--- Iniciando Ingestão em Massa: {SOURCE_DIR} ---")

    files_to_process = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(EXTENSIONS):
                files_to_process.append(os.path.join(root, file))

    total = len(files_to_process)
    print(f"Total de arquivos encontrados: {total}")

    for idx, file_path in enumerate(files_to_process, 1):
        file_name = os.path.basename(file_path)
        print(f"[{idx}/{total}] Processando: {file_name}...", end="\r")

        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f)}
                response = requests.post(BASE_URL, files=files)

            if response.status_code != 200:
                print(f"\nErro no arquivo {file_name}: {response.text}")
        except Exception as e:
            print(f"\nFalha crítica no arquivo {file_name}: {e}")

        # Pequeno delay para não sobrecarregar o container
        time.sleep(0.05)

    print(f"\n--- Ingestão concluída! {total} fontes processados. ---")

if __name__ == "__main__":
    bulk_upload()
