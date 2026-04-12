# 🧠 RAG-Docker MCP: Cérebro de IA Local para TOTVS Protheus (AdvPL)


## 🎯 O Desafio
Como fazer uma IA avançada como o Claude (Anthropic) entender mais de 4.000 arquivos de código-fonte de um ERP (TOTVS Protheus / AdvPL), com regras de negócio altamente customizadas, **sem expor o código da empresa na internet** e **sem pagar rios de dinheiro em chamadas de API**?

## 🚀 A Solução
Este projeto implementa uma arquitetura **RAG (Retrieval-Augmented Generation)** 100% local e conteinerizada via Docker, utilizando o protocolo **MCP (Model Context Protocol)**. Ele vetoriza seus fontes localmente e atua como uma ponte segura entre o seu código e o Claude (seja no Desktop ou em editores como Windsurf e VSCode).

### 🛠️ Tech Stack
* **Infraestrutura:** Docker & Docker Compose
* **Backend:** Python 3.11, FastAPI, Uvicorn
* **Banco Vetorial:** ChromaDB (Otimizado para buscas semânticas em código)
* **Embeddings Locais:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`) via PyTorch. **Zero dependência de APIs externas (como OpenAI ou Gemini).**
* **Integração:** Protocolo MCP oficial da Anthropic.

### 📈 Ganhos e Melhorias da Arquitetura
1.  **Privacidade Total:** Os fontes do seu ERP nunca saem da sua máquina durante a indexação.
2.  **Custo Zero de Ingestão:** Ao utilizar embeddings locais com PyTorch, você pode reindexar 5.000 arquivos quantas vezes quiser sem pagar 1 centavo de API.
3.  **Resiliência:** Sem erros de `404`, `Rate Limit` ou quedas de internet. O cérebro roda na sua máquina.
4.  **Respeito ao Legado:** Configurado especificamente para respeitar o encoding **CP1252**, evitando a corrupção de caracteres em arquivos `.prw`, `.tlpp` e `.ch`.

---

## 💻 Como utilizar no seu ambiente

### 1. Subindo a infraestrutura
Clone este repositório e inicie os containers:
```bash
docker compose up --build -d
