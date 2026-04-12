# ADVPL & RAG — Regras de Ouro

## 1. Encoding Crítico (ADVPL)
- Arquivos `.prw, .tlpp, .ch, .prx, .aph` são **CP1252**.
- **Ação Obrigatória**: Use sempre `mcp file-tools` com a flag `encoding=cp1252`.
- **Proibido**: Salvar arquivos em UTF-8 ou usar ferramentas de edição que não suportem CP1252.

## 2. Consulta ao RAG (MCP)
- Este projeto possui o servidor MCP `rag-docker`.
- **Regra**: Antes de sugerir qualquer lógica de negócio ou função de sistema, utilize a ferramenta `consultar_base_interna` para verificar o que já existe nos fontes indexados.
- **Contexto**: O banco de dados contém todo o ecossistema Protheus da empresa.

## 3. Comandos de Manutenção
- **Subir Docker**: `docker compose up -d`
- **Rebuild**: `docker compose up --build -d`
- **Logs**: `docker logs -f rag_app`
- **Ingestão em Massa**: `python bulk_ingest.py`

## 4. Estrutura do RAG
- `/rag`: Lógica de Embedding e Busca (ChromaDB).
- `/models`: Comunicação com Ollama (Llama 3 local).
- `/cache`: Persistência via Redis.
- `mcp_server.py`: Gateway de comunicação com o Claude.
