# Módulo 1 — Claude Code e Cursor

## O que você vai aprender

Este módulo é a **fundação** de todo o workflow. Sem ele, os demais módulos não
fazem sentido. Você vai configurar seu ambiente de desenvolvimento assistido por IA
do zero, entendendo cada peça e por que ela existe.

## Subseções

| Pasta | Tema |
|-------|------|
| `01-configuracao/` | Instalação, settings e keybindings |
| `02-context-engineering/` | CLAUDE.md global e por projeto |
| `03-skills/` | Criando habilidades reutilizáveis |
| `04-rules/` | Regras que guiam o comportamento da IA |
| `05-mcp-servers/` | Model Context Protocol: conectando ferramentas externas |
| `06-subagents/` | Delegando tarefas para agentes especializados |

## Visão Geral da Arquitetura

```
Você (Developer)
      │
      ▼
┌─────────────────────────────────────────────┐
│              Claude Code CLI                │
│                                             │
│  ┌──────────────┐   ┌─────────────────────┐ │
│  │  CLAUDE.md   │   │   .claude/          │ │
│  │  (contexto)  │   │   settings.json     │ │
│  └──────────────┘   │   skills/           │ │
│                     │   hooks/            │ │
│                     └─────────────────────┘ │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │           MCP Servers                │   │
│  │  GitHub │ Filesystem │ Terraform │…  │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
      │
      ▼
  Subagents (tarefas paralelas e especializadas)
```

## Pré-requisitos

```bash
# 1. Instalar o Claude Code
npm install -g @anthropic-ai/claude-code

# 2. Autenticar
claude login

# 3. Verificar instalação
claude --version
```

## Ordem de Estudo Recomendada

1. `01-configuracao/` — configure seu ambiente
2. `02-context-engineering/` — aprenda a "falar" com a IA de forma eficaz
3. `03-skills/` — automatize tarefas repetitivas
4. `04-rules/` — defina padrões do seu projeto
5. `05-mcp-servers/` — conecte ferramentas externas
6. `06-subagents/` — delegar e paralelizar tarefas

---

> **Dica:** Cada subpasta tem seu próprio `README.md` com exemplos que você pode
> copiar, adaptar e testar imediatamente.
