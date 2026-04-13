import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Protheus_RAG")

@mcp.tool()
async def consultar_base_interna(pergunta: str) -> str:
    """
    Consulta a base de dados interna (RAG) com os fontes AdvPL do Protheus.
    Use sempre que o usuário perguntar sobre funções, tabelas ou lógica de negócio.
    """
    url = "http://localhost:3333/chat"
    
    # O httpx.AsyncClient permite que o Claude continue processando em segundo plano sem travar a interface
    async with httpx.AsyncClient(timeout=310.0) as client:
        try:
            res = await client.post(url, json={"prompt": pergunta})
            
            if res.status_code != 200:
                return f"A API do RAG falhou (Erro HTTP {res.status_code}). Detalhes: {res.text}"
                
            return res.json().get("response", "Resposta válida, mas vazia do RAG.")
            
        except httpx.TimeoutException:
            return "Erro: O modelo local demorou mais de 5 minutos para responder e estourou o tempo limite."
        except Exception as e:
            return f"Erro fatal ao conectar com o RAG local: {str(e)}"

if __name__ == "__main__":
    mcp.run()