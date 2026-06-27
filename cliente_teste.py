import asyncio
import json
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Caminho absoluto do servidor, ancorado na pasta deste arquivo —
# funciona independente do diretorio de onde o cliente for executado.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_SERVIDOR = os.path.join(_AQUI, "servidor_mcp.py")


def _parse(result):
    structured = getattr(result, "structuredContent", None)
    if structured is not None:
        if isinstance(structured, dict) and "result" in structured:
            return structured["result"]
        return structured
    textos = [
        c.text for c in result.content
        if getattr(c, "type", None) == "text" and getattr(c, "text", None) is not None
    ]
    if len(textos) == 1:
        return json.loads(textos[0])
    return [json.loads(t) for t in textos]


async def main() -> dict:
    # usa o mesmo interpretador python que esta rodando este cliente,
    # e o caminho absoluto do servidor
    params = StdioServerParameters(command=sys.executable, args=[_SERVIDOR])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            criar_resultado = _parse(criar)
            listar_resultado = _parse(listar)
            if isinstance(listar_resultado, dict):
                listar_resultado = [listar_resultado]

            return {
                "tools": nomes,
                "criar_resultado": criar_resultado,
                "listar_resultado": listar_resultado,
            }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(main())))
