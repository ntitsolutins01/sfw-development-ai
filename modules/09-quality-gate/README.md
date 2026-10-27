# Módulo 9 — Quality Gate

## O que este módulo cobre

Quality gates são pontos de decisão automáticos no pipeline de desenvolvimento que bloqueiam a progressão se o código não atender a critérios definidos. A palavra-chave é **bloquear** — um gate que só avisa sem bloquear é uma recomendação, não um gate.

Este módulo documenta como configurar e usar três tipos de gate, como integrá-los ao workflow AIAD, e como o mesmo conceito se aplica a pipelines LLM — onde os gates decidem o que chega ao modelo e o que é barrado antes.

## Estrutura

| Pasta | Conteúdo |
|-------|----------|
| `01-conceito/` | O que são quality gates, 3 tipos, onde se encaixam no pipeline, extensão para LLM |
| `02-workflow/` | Pipeline define → implementar → integrar → monitorar → ajustar |
| `03-templates/` | Configurações prontas: pytest-cov, radon, GitHub Actions com todos os gates |
| `04-ia-no-fluxo/` | Skill `/quality-gate` — como usar o Claude Code para configurar, executar e interpretar gates |
| `05-exemplos/` | Antes/depois: coverage gate, complexity gate, LLM pipeline gate (JEV) |

## Pré-requisitos

- Módulos 1–8 concluídos (especialmente Módulo 3 — TDD e Módulo 8 — OWASP)
- Sistema de autenticação JWT implementado e com testes (resultado do Módulo 3)
- Python 3.11+, `pytest`, `pytest-cov`, `radon` instalados

## Skill deste módulo

```
/quality-gate [--all | --coverage | --complexity | --security]
```

Verifica os quality gates configurados no projeto, executa as ferramentas disponíveis, e reporta quais gates passaram, falharam ou estão ausentes. Para gates falhando ou ausentes, oferece gerar a configuração ou a correção.

Instalação: copie `.claude/skills/quality-gate/SKILL.md` para o mesmo caminho no seu projeto.

## Como navegar

Para entender o conceito → `01-conceito/README.md`  
Para o pipeline de configuração → `02-workflow/README.md`  
Para as configurações prontas → `03-templates/`  
Para executar na prática → `04-ia-no-fluxo/README.md`  
Para exemplos concretos → `05-exemplos/`  
Para o guia E2E → [`docs/guia-e2e.md`](../../docs/guia-e2e.md)