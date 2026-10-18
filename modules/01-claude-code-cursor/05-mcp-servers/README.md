# 05 — MCP Servers

## O que é o Model Context Protocol (MCP)

MCP é um protocolo aberto que permite conectar a IA a **ferramentas externas**.
Pense nele como uma "tomada universal": você conecta ferramentas (GitHub, banco
de dados, Slack, Terraform…) e a IA passa a poder interagir com elas diretamente.

Sem MCP:
```
Você → IA → "veja o PR #42 e me diz o que mudou"
          ← IA: "não tenho acesso ao GitHub"
```

Com MCP:
```
Você → IA → MCP GitHub Server → GitHub API → PR #42
          ← IA: "o PR #42 adiciona validação de CEP, tem 3 arquivos modificados..."
```

## Como Funciona Tecnicamente

```
Claude Code
    │
    ├── MCP Client (embutido)
    │       │
    │       ├── stdio: roda o servidor como processo local
    │       └── sse:   conecta via HTTP a servidor remoto
    │
    ▼
MCP Server (processo separado)
    │
    └── API externa (GitHub, Slack, DB, etc.)
```

## Configurando MCP Servers

A configuração fica no `settings.json` do Claude Code (global ou por projeto):

```json
{
  "mcpServers": {
    "nome-do-server": {
      "command": "npx",
      "args": ["-y", "@nome-do-pacote/mcp-server"],
      "env": {
        "API_KEY": "${VARIAVEL_DE_AMBIENTE}"
      }
    }
  }
}
```

### Onde salvar a configuração

| Escopo | Caminho |
|--------|---------|
| Global (todos os projetos) | `~/.claude/settings.json` |
| Projeto | `/projeto/.claude/settings.json` |
| Local (não commitar) | `/projeto/.claude/settings.local.json` |

> **Tokens e API keys** sempre em `settings.local.json` ou variáveis de ambiente — nunca commitar!

## MCP Servers Populares

### GitHub MCP
Permite: ler PRs, issues, commits, criar comentários, aprovar reviews.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Como testar:**
```bash
# Abrir o Claude Code
claude

# Pedir algo que usa o GitHub
> liste os últimos 5 PRs abertos deste repositório
> qual o status do PR #23?
> crie um comentário no PR #23 dizendo "revisado"
```

### Filesystem MCP
Permite: ler e escrever arquivos fora do diretório do projeto.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/seu-usuario/Documents",
        "/tmp"
      ]
    }
  }
}
```

### Postgres MCP
Permite: executar queries, ver schema, explorar dados.

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
```

**Como testar:**
```bash
> qual a estrutura da tabela pedidos?
> quantos pedidos foram criados hoje?
> mostre os 10 usuários com mais pedidos
```

### Slack MCP
Permite: ler mensagens, enviar notificações, buscar em canais.

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

## Verificando MCP Servers Ativos

```bash
# Dentro do Claude Code
/mcp

# Lista os servers configurados e seus status
# Server ativo:   ✅ github (12 tools)
# Server offline: ❌ postgres (connection refused)
```

## Criando seu Próprio MCP Server

É possível criar um MCP Server customizado para APIs internas da empresa.
Veja o exemplo em `exemplos/mcp-server-customizado/`.

### Estrutura mínima (Node.js)

```javascript
// meu-mcp-server.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "meu-server", version: "1.0.0" });

// Registrar uma ferramenta
server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "buscar_produto",
    description: "Busca um produto pelo ID no catálogo interno",
    inputSchema: {
      type: "object",
      properties: {
        produto_id: { type: "string", description: "ID do produto" }
      },
      required: ["produto_id"]
    }
  }]
}));

// Implementar a ferramenta
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "buscar_produto") {
    const { produto_id } = request.params.arguments;
    // lógica de busca aqui
    return { content: [{ type: "text", text: JSON.stringify(produto) }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Boas Práticas

1. **Tokens em variáveis de ambiente** — nunca hardcoded no settings.json
2. **settings.local.json no .gitignore** — protege credenciais do time
3. **Escopo mínimo** — configure só os MCP servers que o projeto realmente usa
4. **Verifique com `/mcp`** — antes de pedir algo que depende de um server externo

## Arquivos de Exemplo

- `exemplos/settings-com-github.json` — configuração com GitHub MCP
- `exemplos/settings-com-postgres.json` — configuração com Postgres MCP
- `exemplos/settings-completo.json` — todos os servers comuns configurados
