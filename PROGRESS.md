# PROGRESS — sfw-development-ai

Registro cronológico de sessões de trabalho.
Para retomar: leia a sessão mais recente e siga "Próxima sessão".

---

## Sessão 1 — 2026-10-17

### O que foi feito

**Módulo 1: Claude Code e Cursor — CONCLUÍDO**

Criada a estrutura completa do módulo 1 com 6 subseções e documentação didática:

| Subseção | Arquivos | Destaque |
|----------|----------|----------|
| `01-configuracao/` | README, settings.example.json, settings.local.example.json, keybindings.example.json | 30+ padrões de permissão comentados |
| `02-context-engineering/` | README + 3 exemplos de CLAUDE.md | Camadas global/projeto/subpasta |
| `03-skills/` | README + 3 skills prontas | code-review, criar-pr, rodar-testes |
| `04-rules/` | README + 3 arquivos de rules | python, segurança, llm-apis |
| `05-mcp-servers/` | README + 2 exemplos de settings | GitHub, Postgres, Slack, Terraform |
| `06-subagents/` | README + exemplos de cenários | fork vs fresh agent, 4 casos reais |

**Correção aplicada:** todos os arquivos de exemplo (`CLAUDE.md.*` e `rules/*.md`) receberam bloco `[EXEMPLO] Como usar este arquivo` no topo com: onde salvar, como ativar, como testar.

**shared/prompt-caching/ — CRIADO**

Biblioteca interna reutilizável para KV-caching da API Anthropic:
- `llm_client.py` — baseado em `rag-project/src/llm/llm_client.py`, com método `_log_cache_status` extraído
- `exemplos/uso_simples.py` — comparativo com/sem cache, observável nos logs
- `exemplos/uso_agente.py` — loop de agente analisando 3 arquivos (padrão para módulos 12/13/14)

**Decisões desta sessão:**
- `shared/` não é módulo do curso — é biblioteca interna usada pelos módulos 12, 13 e 14
- Rule `llm-apis.md` criada para que a IA aplique caching automaticamente ao gerar clientes Anthropic
- Mecanismo de 3 camadas para persistência de contexto criado (este arquivo + CLAUDE.md + memory)

### Decisão registrada

**[2026-10-17] `disable-model-invocation: false` na skill `/salvar-contexto`**

Skills de projeto em `.claude/skills/` não criam comandos `/` na CLI do Claude Code — apenas skills globais instaladas via plugin funcionam com `/`. A flag `disable-model-invocation: true` impedia até mesmo a invocação pelo Claude em resposta ao pedido explícito do usuário. Alterada para `false` para que o Claude possa invocar a skill quando o usuário digitar `/salvar-contexto` como mensagem de chat.

---

### Próxima sessão

**Módulo 2 — Spec Driven Development**

O que será coberto:
- O que é Spec Driven Development e por que engenheiros usam
- Workflow: spec → revisão → implementação → validação
- Estrutura de um spec de feature bem escrito
- Templates de spec (feature, bugfix, refactor, API)
- Como usar a IA para gerar e revisar specs
- Integração com o módulo 4 (Pull Request Review)

Para iniciar: abra o Claude Code, leia este arquivo e diga "pode começar o módulo 2".

---

## Sessão 2 — 2026-10-17 (continuação)

### O que foi feito

**Skill `/gerar-post` — CRIADA**

Nova skill independente para geração de publicações LinkedIn sem passar pelo fluxo de salvar contexto:

| Arquivo | Localização |
|---------|-------------|
| `SKILL.md` | `.claude/skills/gerar-post/SKILL.md` |

Comportamento:
- `/gerar-post` → usa o contexto da sessão atual como tema
- `/gerar-post sobre X` → foca no tema informado
- Gera PT + EN + image prompt diretamente, sem menu de contexto
- Salva arquivo em `docs/publicacoes-linkedin/YYYY-MM-DD-<slug>.md` (adicionado pelo usuário)

**Melhorias aplicadas na skill pelo usuário:**
- Tabela de emojis por domínio (segurança, performance, IA, TDD, DevOps, etc.)
- Passo 3 automático: salvar post gerado em `docs/publicacoes-linkedin/`

**Publicações geradas nesta sessão:**
- Sobre o sistema de persistência de contexto em 3 camadas + skill `/salvar-contexto`
- Sobre o Módulo 1 — framework de configuração Claude Code com 6 camadas

### Decisões tomadas

- Skill dedicada `gerar-post` é mais limpa do que passar pelo menu do `salvar-contexto` quando o objetivo é só o post
- Posts salvos automaticamente em `docs/publicacoes-linkedin/` para histórico e reutilização

### Próxima sessão

**Módulo 2 — Spec Driven Development**

O que será coberto:
- O que é Spec Driven Development e por que engenheiros usam
- Workflow: spec → revisão → implementação → validação
- Estrutura de um spec de feature bem escrito
- Templates de spec (feature, bugfix, refactor, API)
- Como usar a IA para gerar e revisar specs
- Integração com o módulo 4 (Pull Request Review)

Para retomar: leia o PROGRESS.md e me coloque em contexto

---

## Template para próximas sessões

```
## Sessão N — YYYY-MM-DD

### O que foi feito
- Módulo X: [nome] — CONCLUÍDO / EM ANDAMENTO
- [lista do que foi criado/corrigido]
- Decisões tomadas: [o que foi decidido e por quê]

### Próxima sessão
- Módulo Y — [o que será coberto]
- Pendências: [itens não concluídos desta sessão]
```
