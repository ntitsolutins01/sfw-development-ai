# Módulo 8 — OWASP Top 10

## O que este módulo cobre

O OWASP Top 10 é a lista das 10 categorias de vulnerabilidade mais críticas em aplicações web, publicada pela Open Web Application Security Project Foundation. A versão atual é de 2021 e serve como base de referência para auditorias, revisões de código e certificações.

Este módulo documenta como usar o Claude Code para auditar código contra as 10 categorias de forma sistemática — não como checklist manual, mas como pipeline de análise assistido por IA.

**Premissa central:** a IA consegue manter o catálogo OWASP completo em contexto enquanto lê o código, identificar padrões que violam cada categoria e propor correções com justificativa técnica. O que levaria horas de auditoria manual pode ser feito em minutos com o prompt certo.

## Estrutura

| Pasta | Conteúdo |
|-------|----------|
| `01-conceito/` | O que é OWASP Top 10, mapeamento para o projeto JWT, por que IA muda o jogo |
| `02-workflow/` | Pipeline de auditoria: inventory → analyze → triage → fix → verify |
| `03-templates/` | Templates de prompt para auditoria OWASP e documentação de achados |
| `04-ia-no-fluxo/` | Skill `/audit-owasp` — prompts passo a passo na prática |
| `05-exemplos/` | Antes/depois: A01, A02 e A07 no projeto JWT |

## Pré-requisitos

- Módulos 1–7 concluídos (especialmente Módulo 4 — PR Review e Módulo 6 — Prompt Engineering)
- Código do sistema de autenticação JWT implementado (resultado do Módulo 3)
- Familiaridade básica com conceitos de segurança web (HTTP, autenticação, criptografia)

## Skill deste módulo

```
/audit-owasp [arquivo]
```

Executa análise OWASP Top 10 sobre o arquivo informado, categoriza os achados por criticidade e gera relatório estruturado com recomendações de correção.

Instalação: copie `.claude/skills/audit-owasp/SKILL.md` para o mesmo caminho no seu projeto.

## Como navegar

Para aprender o conceito → `01-conceito/README.md`  
Para o pipeline de auditoria → `02-workflow/README.md`  
Para os prompts → `03-templates/`  
Para executar na prática → `04-ia-no-fluxo/README.md`  
Para exemplos concretos → `05-exemplos/`  
Para o guia E2E → [`docs/guia-e2e.md`](../../docs/guia-e2e.md)