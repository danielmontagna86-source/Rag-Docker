import requests
from mcp.server.fastmcp import FastMCP

# Cria o servidor MCP
mcp = FastMCP("RAG_Empresa")

@mcp.tool()
def consultar_base_interna(pergunta: str) -> str:
    """
    Consulta a base de dados interna (RAG) para ler PDFs e documentos da empresa.
    Use esta ferramenta sempre que o usuário pedir informações sobre contexto interno, regras de negócio ou documentos.
    """
    try:
        # Como o MCP vai rodar dentro do container, ele bate no localhost do próprio container
        res = requests.post("http://localhost:3333/chat", json={"prompt": pergunta})
        return res.json().get("response", "Não foi possível obter uma resposta do RAG.")
    except Exception as e:
        return f"Erro de conexão com o RAG local: {str(e)}"

if __name__ == "__main__":
    mcp.run()
