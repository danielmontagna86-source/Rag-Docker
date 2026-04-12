# 🧠 RAG-Docker MCP: Cérebro de IA Local para TOTVS Protheus (AdvPL)

> **Faça o Claude entender os 4.000+ fontes do seu ERP — sem expor seu código, sem pagar por APIs de embedding e sem depender da internet.**

---

## 🎯 O Problema que Todo Analista Protheus Conhece

Você abre o Claude, o Windsurf ou o VSCode com IA e pede ajuda com uma rotina do seu ERP.
A IA devolve um código bonito, genérico, que **não conhece nenhuma das suas customizações**,
seus parâmetros de `SX6`, suas funções utilitárias internas, suas regras de negócio específicas.

Você passa os próximos 20 minutos explicando o contexto que a IA deveria saber.

**E se a IA já soubesse tudo isso antes de você perguntar?**

---

## 🚀 A Solução: RAG Local + MCP

Este projeto implementa uma arquitetura **RAG (Retrieval-Augmented Generation)** 100% local
e conteinerizada via Docker. Ele vetoriza seus fontes AdvPL diretamente na sua máquina e os
disponibiliza para o Claude via **protocolo MCP (Model Context Protocol)** — a ponte oficial
da Anthropic entre ferramentas externas e o modelo.

Na prática: antes de responder qualquer pergunta sua, o Claude consulta silenciosamente os
seus próprios fontes e responde com contexto real do seu ambiente.

---

## 🛠️ Tech Stack

| Camada | Tecnologia |
|---|---|
| Infraestrutura | Docker & Docker Compose |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Banco Vetorial | ChromaDB |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace + PyTorch) |
| LLM Local | Ollama + Llama 3 |
| Cache | Redis |
| Integração Claude | Protocolo MCP oficial (Anthropic) |

> ⚡ **Zero dependência de APIs externas para indexação.** Reindexe 5.000 arquivos quantas vezes quiser sem gastar um centavo.

---

## ✅ Por que usar este projeto?

- 🔒 **Privacidade total** — seus fontes nunca saem da sua máquina durante a indexação
- 💸 **Custo zero de embedding** — modelo local, sem OpenAI, sem Gemini, sem surpresas na fatura
- ⚙️ **Resiliente** — sem rate limit, sem queda de internet, sem erro 404
- 🇧🇷 **Feito para o legado AdvPL** — encoding CP1252 respeitado nativamente, sem corromper acentos


---

## 📁 Estrutura do Projeto

```
rag-docker/
│
├── 📄 server.py           # API FastAPI — endpoints /chat e /ingest
├── 📄 mcp_server.py       # Servidor MCP — ponte com o Claude
├── 📄 router.py           # Orquestrador: cache → RAG → LLM
├── 📄 bulk_ingest.py      # Ingestão em massa dos seus fontes
├── 📄 config.py           # Variáveis de ambiente
├── 📄 Dockerfile
├── 📄 docker-compose.yml
│
├── 📁 rag/
│   ├── chunk.py           # Chunking com overlap (não quebra funções ao meio)
│   ├── embed.py           # Geração de embeddings 100% local
│   ├── ingest.py          # Leitura de PDF e AdvPL (CP1252 obrigatório)
│   └── search.py          # Busca semântica no ChromaDB
│
├── 📁 models/
│   └── ollama.py          # Integração com Llama 3 via Ollama
│
└── 📁 cache/
    └── redis_cache.py     # Cache de respostas via Redis
```

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac/Linux)
- [Python 3.11+](https://www.python.org/downloads/)
- Git

---

## ⚙️ Instalação Passo a Passo

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/rag-docker.git
cd rag-docker
```

### 2. Configure as variáveis de ambiente

Copie o arquivo de exemplo e edite com seus dados:

```bash
# Linux / Mac
cp .env.example .env

# Windows (PowerShell)
copy .env.example .env
```


Abra o `.env` e preencha:

```env
# Chave da API Google Gemini (opcional — só se usar Gemini como LLM)
# Obtenha gratuitamente em: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=sua_chave_aqui

# Caminho completo para a pasta raiz dos seus fontes Protheus
# Exemplo Windows:
SOURCE_DIR=C:\projetos\protheus-sistema
# Exemplo Linux/Mac:
# SOURCE_DIR=/home/usuario/protheus-sistema
```

### 3. Suba os containers

**Primeira execução** (faz o build completo — pode levar alguns minutos):

```bash
docker compose up --build -d
```

**Execuções seguintes:**

```bash
docker compose up -d
```

Verifique se tudo está rodando:

```bash
docker ps
```

Você deverá ver 3 containers ativos: `rag_app`, `rag_redis` e `rag_ollama`.

### 4. Baixe o modelo LLM local (Llama 3)

Com o container do Ollama rodando, baixe o modelo:

```bash
docker exec -it rag_ollama ollama pull llama3
```

> ⏳ O download é feito uma única vez (~4GB). Após isso, o modelo fica disponível localmente para sempre.

### 5. Indexe seus fontes AdvPL

Com os containers ativos, rode a ingestão em massa:

```bash
python bulk_ingest.py
```

O script vai:
1. Percorrer recursivamente o `SOURCE_DIR` definido no `.env`
2. Encontrar todos os arquivos `.prw`, `.tlpp`, `.ch` e `.prx`
3. Ler cada um com encoding **CP1252** (sem corrupção de acentos)
4. Vetorizar e indexar no ChromaDB local

> Para 4.000 arquivos, o processo leva em média 15–30 minutos na primeira vez.


### 6. Configure o MCP no Claude

Adicione o servidor MCP ao seu `claude_desktop_config.json` (ou `mcp_settings.json` no Windsurf/VSCode):

```json
{
  "mcpServers": {
    "rag-protheus": {
      "command": "python",
      "args": ["C:\\caminho\\para\\rag-docker\\mcp_server.py"]
    }
  }
}
```

Reinicie o Claude Desktop (ou seu editor). A ferramenta `consultar_base_interna` estará disponível automaticamente.

---

## 🔁 Fluxo de Funcionamento

```
Você pergunta algo ao Claude
        ↓
Claude chama `consultar_base_interna`
        ↓
mcp_server.py → POST /chat (FastAPI local)
        ↓
router.py verifica o cache Redis
        ↓
rag/search.py busca os chunks mais relevantes no ChromaDB
        ↓
Llama 3 (Ollama) gera a resposta com contexto real dos seus fontes
        ↓
Claude responde com conhecimento do seu ERP
```

---

## 🌐 Endpoints da API

A API REST está disponível em `http://localhost:3333`:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/chat` | Consulta ao RAG + LLM. Body: `{"prompt": "sua pergunta"}` |
| `POST` | `/ingest` | Upload individual de um arquivo para indexação |

**Exemplo de uso direto:**

```bash
curl -X POST http://localhost:3333/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Como funciona o cálculo de comissão no nosso sistema?"}'
```

---

## 🔧 Comandos Úteis

```bash
# Ver logs em tempo real
docker logs -f rag_app

# Reiniciar apenas a aplicação (após mudanças no código)
docker compose restart app

# Rebuild completo
docker compose up --build -d

# Parar tudo
docker compose down

# Reindexar os fontes do zero
python bulk_ingest.py
```


---

## ⚠️ Observações Importantes

### Encoding CP1252
Arquivos AdvPL **sempre** usam CP1252. O `rag/ingest.py` já está configurado corretamente.
Não altere o encoding — caracteres como `ã`, `ç`, `é` serão corrompidos com UTF-8.

### Primeira indexação
A primeira execução do `bulk_ingest.py` demora mais porque o modelo de embedding
(`all-MiniLM-L6-v2`) é baixado do HuggingFace automaticamente (~90MB).
As reindexações seguintes são muito mais rápidas.

### Recursos de hardware recomendados
- RAM mínima: **8GB** (16GB para bases grandes com +4.000 fontes)
- GPU: opcional, mas melhora a latência do Llama 3 significativamente
- Disco: ~5GB livres (modelo Llama 3 + dados do ChromaDB)

---

## 🤝 Contribuições

PRs são bem-vindos! Se você trabalha com Protheus e tem ideias para melhorar
a indexação, chunking ou integração com outros editores, abra uma issue ou mande um PR.

---

## 📄 Licença

MIT License — use, modifique e distribua à vontade.
