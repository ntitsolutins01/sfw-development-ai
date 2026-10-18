# sfw-development-ai — Workflow de Desenvolvimento Assistido por IA

Repositório de referência do Workflow de Desenvolvimento Assistido por IA.
Contém 15 módulos práticos que cobrem todo o ciclo de desenvolvimento moderno
assistido por inteligência artificial.

## Estrutura do Projeto

```
sfw-development-ai/
├── CLAUDE.md                          ← você está aqui
├── .claude/
│   └── settings.json                  ← permissões e configurações do projeto
├── modules/
│   ├── 01-claude-code-cursor/         ← Módulo 1: Fundação
│   ├── 02-spec-driven-development/    ← Módulo 2: Especificações
│   ├── 03-tdd/                        ← Módulo 3: TDD
│   ├── 04-pull-request-review/        ← Módulo 4: Revisão de PR
│   ├── 05-issue-analysis/             ← Módulo 5: Análise de Issues
│   ├── 06-prompt-engineering/         ← Módulo 6: Prompt Engineering
│   ├── 07-context-engineering/        ← Módulo 7: Context Engineering
│   ├── 08-owasp-top-10/               ← Módulo 8: Segurança OWASP
│   ├── 09-quality-gate/               ← Módulo 9: Quality Gates
│   ├── 10-security-analysis/          ← Módulo 10: Análise de Segurança
│   ├── 11-loop-engineering/           ← Módulo 11: Loop Engineering
│   ├── 12-hermes-agent/               ← Módulo 12: Hermes Agent
│   ├── 13-observability/              ← Módulo 13: Observabilidade
│   ├── 14-llm-as-judge/               ← Módulo 14: LLM as a Judge
│   └── 15-architecture/               ← Módulo 15: Arquitetura
└── workflows/                         ← Exemplos de integração entre módulos
```

## Como Navegar

Cada módulo tem seu próprio `README.md` com:
- Conceito e objetivo
- Pré-requisitos
- Exemplos práticos comentados
- Como testar localmente

## Pré-requisitos Globais

- Claude Code CLI instalado (`npm install -g @anthropic-ai/claude-code`)
- Node.js 18+
- Python 3.11+ (alguns módulos)
- Git configurado

## Status Atual

> Atualizado em: 2026-10-18

| # | Módulo | Status |
|---|--------|--------|
| 1 | Claude Code e Cursor | ✅ Concluído |
| 2 | Spec Driven Development | ✅ Concluído |
| 3 | TDD | ✅ Concluído |
| 4 | Pull Request Review | ⏳ Próximo |
| 5 | Issue Analysis | — |
| 6 | Prompt Engineering | — |
| 7 | Context Engineering | — |
| 8 | OWASP Top 10 | — |
| 9 | Quality Gate | — |
| 10 | Análises de Segurança | — |
| 11 | Loop Engineering | — |
| 12 | Hermes Agent | — |
| 13 | Observabilidade | — |
| 14 | LLM as a Judge | — |
| 15 | Arquitetura | — |

Para retomar: leia `PROGRESS.md` na raiz do projeto.

---

## Regras Globais para IA neste Projeto

- Sempre consultar o `README.md` do módulo antes de modificar qualquer arquivo
- Nunca remover exemplos existentes — apenas adicionar ou corrigir
- Manter comentários didáticos em português
- Ao gerar código, incluir caso de uso e como testar
- Sempre pedir permissão antes de iniciar um novo módulo
- Ao final de cada sessão, atualizar `PROGRESS.md`, `CLAUDE.md` (status) e a memória do projeto
