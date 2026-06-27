# Exercício 4.2 — MCP server local que consome a API 4.1

Servidor MCP (FastMCP, stdio) que expõe duas tools — `criar_tarefa` e `listar_tarefas` — implementadas chamando a API REST de TODO list do 4.1 (localhost:8000).

## Reflexão (Aula 6)

O que o MCP escondeu: o agente não precisa mais saber que a fonte das tarefas é uma API HTTP em localhost:8000, nem conhecer rotas, verbos, formato de corpo ou status codes. Ele só precisa saber que existe uma tool `criar_tarefa(titulo)`. O MCP tornou o protocolo de transporte (HTTP REST) irrelevante para quem chama — trocar a API por um banco ou outro serviço não mudaria nada para o agente.
