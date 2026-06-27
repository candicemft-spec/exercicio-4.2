import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _parse(result):
    """Extrai o payload JSON de um resultado de call_tool, de forma robusta
    a diferentes versoes do SDK.

    Tenta, em ordem:
      1) structuredContent (quando o SDK ja entrega o objeto/lista pronto);
      2) concatenar todos os blocos de texto e dar json.loads no conjunto;
      3) json.loads do primeiro bloco de texto.
    """
    # 1) structuredContent: alguns SDKs expoem o retorno tipado aqui
    structured = getattr(result, "structuredContent", None)
    if structured is not None:
        # FastMCP embrulha retorno de lista em {"result": [...]}
        if isinstance(structured, dict) and "result" in structured:
            return structured["result"]
        return structured

    # 2) junta todos os blocos de texto
    textos = [
        c.text for c in result.content
        if getattr(c, "type", None) == "text" and getattr(c, "text", None) is not None
    ]
    if len(textos) == 1:
        return json.loads(textos[0])
    # varios blocos: cada um e um item -> monta a lista
    return [json.loads(t) for t in textos]


async def main() -> dict:
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            criar_resultado = _parse(criar)
            listar_resultado = _parse(listar)

            # garante que listar_resultado seja sempre uma lista
            if isinstance(listar_resultado, dict):
                listar_resultado = [listar_resultado]

            return {
                "tools": nomes,
                "criar_resultado": criar_resultado,
                "listar_resultado": listar_resultado,
            }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(main())))
