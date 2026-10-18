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

## Como usar na prática

Siga estes passos para configurar seu ambiente do zero e validar que está funcionando:

**1. Instale e autentique o Claude Code**
```bash
npm install -g @anthropic-ai/claude-code
claude login
claude --version   # deve exibir a versão instalada
```

**2. Configure as permissões do projeto**
- Abra `01-configuracao/settings.example.json`
- Copie para `.claude/settings.json` na raiz do seu projeto
- Ajuste os blocos `allow` e `deny` conforme suas ferramentas

**3. Crie seu CLAUDE.md**
- Abra `02-context-engineering/` e escolha um dos exemplos de CLAUDE.md
- Copie o conteúdo para `CLAUDE.md` na raiz do seu projeto
- Substitua os comentários `[PREENCHA]` com as regras do seu projeto

**4. Instale uma skill para testar**
- Abra `03-skills/` e copie a skill `code-review` para `.claude/skills/code-review/SKILL.md` no seu projeto
- No Claude Code, digite `/code-review` — se responder, a skill está ativa

**5. Adicione uma rule de linguagem**
- Abra `04-rules/` e copie `python.md` ou outra rule para `.claude/rules/` no seu projeto
- A rule passa a valer automaticamente nas próximas sessões

**6. Critério de sucesso**
Você concluiu o módulo quando:
- [ ] `claude --version` retorna sem erro
- [ ] `.claude/settings.json` existe no seu projeto com ao menos uma permissão configurada
- [ ] `CLAUDE.md` existe na raiz com regras do seu projeto
- [ ] `/code-review` (ou outra skill) responde no Claude Code
- [ ] Uma rule está ativa em `.claude/rules/`

---

> **Dica:** Cada subpasta tem seu próprio `README.md` com exemplos que você pode
> copiar, adaptar e testar imediatamente.
