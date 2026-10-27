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

## Sessão 3 — 2026-10-18

### O que foi feito

**Módulo 2: Spec Driven Development — CONCLUÍDO**

6 subseções criadas com documentação completa:

| Subseção | Destaque |
|----------|----------|
| `01-conceito/` | spec vs ticket vs user story, componentes, anti-padrões, self-test |
| `02-workflow/` | fluxo expandido completo: brainstorm → PRD → TRD → spec → revisão → implementação → validação |
| `03-templates/` | 4 templates prontos: feature, bugfix, refactor, api-endpoint |
| `04-ia-no-fluxo/` | 6 prompts prontos para cada etapa do ciclo + snippet de CLAUDE.md |
| `05-exemplos/` | 3 specs reais preenchidos: autenticação JWT, timeout upload, GET /users/{id} |
| `06-pre-spec/` | documentação completa das 3 skills de pré-spec com decisão tree e fluxo ponta a ponta |

**3 skills de pré-spec instaladas em `.claude/skills/`:**

| Skill | Arquivo gerado | O que faz |
|-------|---------------|-----------|
| `/brainstorm` | `docs/brainstorms/YYYY-MM-DD-<slug>.md` | Matura ideias, aponta trade-offs, nunca implementa |
| `/escrever-prd` | `docs/prds/NNN-nome.md` | PRD draft-first com user stories, CAs, métricas |
| `/escrever-trd` | `docs/trd.md` + `docs/adrs/` | TRD global + ADRs para decisões com impacto amplo |

**README.md da raiz criado** seguindo layout do rag-project:
- Badges, sumário com âncoras, arquitetura em árvore, tabela de módulos com status
- Tabela de skills do projeto, progresso visual, seção de autor com badges

**Repositório GitHub criado e módulos 1 e 2 publicados:**
- URL: https://github.com/ntitsolutins01/sfw-development-ai
- Commit 1: módulo 1 (estrutura base + shared/ + skills salvar-contexto/gerar-post)
- Commit 2: módulo 2 + skills brainstorm/escrever-prd/escrever-trd

### Decisões tomadas

- Skills do Fabricio Veronez (brainstorm, PRD, TRD) adaptadas como skills de projeto (não via NPX) para integração total com o fluxo SDD deste projeto
- TRD é documento global único por projeto — não se repete por feature
- Docs gerados pelas skills (brainstorms/, prds/, specs/, trd.md, adrs/) são ignorados pelo `.gitignore` — são artefatos de trabalho, não código
- Fluxo expandido integrado no `02-workflow/README.md`, não como nova subseção isolada

### Próxima sessão

**Módulo 3 — TDD (Test-Driven Development com IA)**

O que será coberto:
- Ciclo red-green-refactor assistido por IA
- Como usar specs do Módulo 2 para gerar testes antes da implementação
- Prompts para cada fase do ciclo TDD
- Templates de teste (unit, integration, e2e)
- Exemplos reais com pytest/jest

Para retomar: leia o PROGRESS.md e me coloque em contexto

---

## Sessão 4 — 2026-10-18

### O que foi feito

**Módulo 3: TDD com IA — CONCLUÍDO**

O módulo já existia com toda a estrutura e conteúdo. Nesta sessão foi finalizado com:

| O que foi adicionado | Onde |
|---------------------|------|
| Seção "Como usar na prática" | `modules/03-tdd/README.md` |
| Seção "Como usar na prática" | `modules/01-claude-code-cursor/README.md` |
| Seção "Como usar na prática" | `modules/02-spec-driven-development/README.md` |

Cada seção tem passos numerados com referências a arquivos específicos do módulo e checklist de conclusão — padrão a ser seguido em todos os módulos futuros.

**Rebrand: DAPIA → AIAD**

Projeto renomeado para AIAD (AI-Assisted Development) em todos os arquivos:
- 12 arquivos Markdown atualizados
- Arquivos renomeados: `2026-10-17-dapia-*` → `2026-10-17-aiad-*`
- Memory renomeada: `project-dapia.md` → `project-aiad.md`
- Badge AIAD adicionado ao README principal

### Decisões tomadas

- **AIAD** é o nome oficial do projeto — sigla mais limpa que DAPIA
- Seção "Como usar na prática" é padrão obrigatório em todos os módulos futuros
- Módulo 3 considerado concluído após adição da camada prática

### Próxima sessão

**Módulo 4 — Pull Request Review**

O que será coberto:
- O que um revisor de PR deve verificar com e sem IA
- Prompts prontos para revisão automática de PR
- Integração com specs do Módulo 2 (spec como critério de aceite)
- Integração com testes do Módulo 3 (cobertura como gate)
- Templates de checklist de revisão
- Skill `/code-review` e `/review-pr`

Para retomar: leia o PROGRESS.md e me coloque em contexto

---

## Sessão 5 — 2026-10-18

### O que foi feito

**Ciclo de publicação LinkedIn — CONCLUÍDO**

Estrutura de posts da série AIAD organizada e vinculada:

| Arquivo | O que foi feito |
|---------|----------------|
| `2026-10-17-aiad-lancamento-serie-15-modulos.md` | `💬 Comentário` adicionado para vincular ao post do Módulo 1 quando publicado |
| `2026-10-17-claude-code-6-layers-config.md` | `💬 Comentário` para postar no lançamento da série + GitHub removido |
| `2026-10-17-context-persistence-3-layers.md` | `💬 Comentário de Extensão` (extensão do Módulo 1) + versão PT adicionada + melhorias |
| `2026-10-18-spec-driven-development-modulo-2.md` | `💬 Comentário` para lançamento + GitHub removido |
| `2026-10-18-tdd-com-ia-modulo-3.md` | Criado + `💬 Comentário` para lançamento + GitHub removido |

**Padrão de série estabelecido:**
- Cada post tem seção `## 💬 Comentário` com texto PT + EN pronto para postar no post de lançamento
- Post de persistência de contexto tem `## 💬 Comentário de Extensão` — vincula ao post do Módulo 1 como extensão natural
- Placeholder `[link deste post]` a ser substituído pelo link real no momento da publicação
- GitHub removido dos posts de módulo (fica só no post de lançamento da série)

### Decisões tomadas

- Posts de módulo não carregam link do GitHub — sobrecarrega o post; o link fica no lançamento da série
- Post de persistência de contexto é extensão do Módulo 1, não um post independente — `💬 Comentário de Extensão` deixa isso explícito
- Padrão `💬 Comentário` passa a ser gerado automaticamente pelo `/gerar-post` em módulos futuros

### Próxima sessão

**Módulo 4 — Pull Request Review**

O que será coberto:
- O que um revisor de PR deve verificar com e sem IA
- Prompts prontos para revisão automática de PR
- Integração com specs do Módulo 2 (spec como critério de aceite)
- Integração com testes do Módulo 3 (cobertura como gate)
- Templates de checklist de revisão
- Skill `/code-review` e `/review-pr`

Para retomar: leia o PROGRESS.md e me coloque em contexto

---

## Sessão 6 — 2026-10-19

### O que foi feito

**Infraestrutura de documentação E2E — EM ANDAMENTO (Módulo 4 ainda não iniciado)**

| O que foi criado/corrigido | Detalhe |
|---------------------------|---------|
| `docs/guia-e2e.md` | Arquivo criado — guia E2E completo com JWT auth como projeto de prova; módulos 1–3 detalhados com objetivo, passos, checklist e link de referência |
| `README.md` — seção E2E | Coluna "O que cobre" adicionada com descrição objetiva dos 15 módulos; links "Como executar" corrigidos |
| Âncoras de navegação | Cabeçalhos simplificados para ASCII puro (`## Modulo N Nome`, sem acento, sem `:`) para compatibilidade VS Code + GitHub |
| Links "Referência completa" | Padronizados como `**[Referência completa](../modules/XX/README.md)**` em todos os módulos do guia |
| `salvar-contexto/SKILL.md` | Padrões de cabeçalho e link atualizados para módulos futuros |

### Estado atual (pausa)

**O que foi feito:** guia E2E criado e navegação corrigida. Commit e push realizados.

**O que falta para fechar esta camada:**
- Nenhuma pendência de documentação — guia E2E está funcional
- Próximo passo real: iniciar Módulo 4 (Pull Request Review)

---

## Sessão 7 — 2026-10-19

### O que foi feito

**Módulo 4: Pull Request Review — CONCLUÍDO**

| Subseção | Destaque |
|----------|----------|
| `01-conceito/` | 5 dimensões de revisão (funcional, testes, segurança, performance, qualidade), 4 categorias de severidade, anti-padrões |
| `02-workflow/` | Fluxo completo com diagrama: self-review → /code-review → /review-pr → revisão humana |
| `03-templates/` | 3 checklists prontos: feature, bugfix, refactor |
| `04-ia-no-fluxo/` | 6 prompts: revisão geral, conformidade spec, cobertura de testes, segurança, performance, sumário executivo |
| `05-exemplos/` | 3 revisões reais: JWT auth (continuação M2+M3), bugfix timeout, refatoração UserRepository |

**Skill `/review-pr` criada** em `.claude/skills/review-pr/SKILL.md`:
- Coleta diff com `git diff main...HEAD`
- Revisa em 4 dimensões: bugs/qualidade, segurança, testes, conformidade com spec
- Emite decisão formal: APROVADO / APROVADO COM RESSALVAS / SOLICITAR MUDANÇAS

### Decisões tomadas

- `/code-review` (Módulo 1) e `/review-pr` (Módulo 4) são complementares: code-review cobre qualidade geral, review-pr adiciona conformidade com spec
- Módulo 4 fecha o ciclo SDD+TDD: spec (M2) → testes (M3) → revisão (M4)
- Exemplos conectados à série JWT dos módulos anteriores — narrativa contínua

### Próxima sessão

**Módulo 5 — Issue Analysis**

O que será coberto:
- Como usar IA para analisar issues e decompor em tasks verificáveis
- Prompts para extrair critérios de aceite de uma issue
- Templates de issue bem escrita (bug, feature, task)
- Integração com spec do Módulo 2 (issue → spec)
- Exemplos reais de análise de issue com IA

Para retomar: leia o PROGRESS.md e me coloque em contexto

---

## Sessão 8 — 2026-10-23

### O que foi feito

**Módulo 5: Issue Analysis — CONCLUÍDO**

| Subseção | Destaque |
|----------|----------|
| `01-conceito/` | 3 tipos de issue (Bug/Feature/Task), triângulo de analisabilidade (Escopo + CAs + DoD), anti-padrões |
| `02-workflow/` | Fluxo completo: análise → clarificação → decomposição → CAs → spec stub |
| `03-templates/` | 3 templates prontos: issue-bug.md, issue-feature.md, issue-task.md |
| `04-ia-no-fluxo/` | 6 prompts: análise inicial, decomposição, extração de CAs, priorização, estimativa, geração de spec stub |
| `05-exemplos/` | 3 análises reais: JWT auth feature, upload timeout bug, UserService refactor task |

**Skill `/analyze-issue` criada** em `.claude/skills/analyze-issue/SKILL.md`:
- Aceita URL do GitHub, caminho de arquivo ou texto colado
- 6 passos: obter issue → análise inicial → decomposição → CAs → spec stub → resumo
- Salva spec stub em `docs/specs/NNN-[slug].md`

**Tracking files atualizados:**
- `README.md` — Módulo 5 ✅ Concluído, skill `analyze-issue` na tabela, E2E link adicionado, contador 5/15
- `CLAUDE.md` — Módulo 5 ✅, Módulo 6 ⏳ Próximo, data atualizada
- `docs/guia-e2e.md` — seção `## Modulo 5 Issue Analysis` preenchida com objetivo, passos e checklist

### Decisões tomadas

- `/analyze-issue` sem argumento → pede para o usuário colar o texto (mais flexível que só aceitar URLs)
- Spec stub salvo em `docs/specs/NNN-[slug].md` para integração direta com o Módulo 2
- Exemplos do módulo usam a série JWT (continuidade com módulos anteriores) + bug upload + refactor UserService

### Próxima sessão

**Módulo 6 — Prompt Engineering**

O que será coberto:
- Técnicas avançadas de engenharia de prompts (zero-shot, few-shot, chain-of-thought, etc.)
- Como estruturar prompts para tarefas de desenvolvimento de software
- Prompts para cada fase do ciclo AIAD
- Anti-padrões e como identificá-los
- Exemplos comparativos: prompt ruim vs prompt bem estruturado

Para retomar: leia o PROGRESS.md e me coloque em contexto

---

## Sessão 9 — 2026-10-26

### O que foi feito

**Módulo 6: Prompt Engineering — CONCLUÍDO**

| Subseção | Destaque |
|----------|----------|
| `01-conceito/` | Framework CIFER (Contexto/Instrução/Formato/Exemplos/Restrições), 6 técnicas, tabela de anti-padrões |
| `02-workflow/` | Ciclo escrever→testar→medir→refinar, tabela de técnicas por módulo AIAD, diagnóstico rápido |
| `03-templates/` | 3 templates prontos: geração de código (zero-shot+CIFER), debug (CoT), refatoração (constrained) |
| `04-ia-no-fluxo/` | 6 técnicas com prompts reais do projeto JWT + como combinar técnicas |
| `05-exemplos/` | 3 comparativos antes/depois: verify_token (geração), token 401 (debug), AuthService (refatoração) |

**Decisão de design:** sem skill dedicada — as técnicas são aplicadas diretamente nos prompts das skills dos outros módulos.

### Decisões tomadas

- Módulo 6 sem skill própria: as técnicas são conhecimento aplicado, não automatizável em uma skill
- Framework CIFER como denominador comum de todos os templates (C + I mínimo, todos os 5 para tarefas complexas)
- Exemplos conectados à série JWT — mesmo projeto de prova dos módulos anteriores

### Próxima sessão

**Módulo 7 — Context Engineering**

O que será coberto:
- Gerenciamento de contexto em sessões longas com Claude Code
- Como e quando usar CLAUDE.md, Rules, skills e memória do projeto
- Técnicas para manter contexto relevante sem poluir o contexto
- Estratégias de chunking e sumarização para projetos grandes
- Como o módulo 7 se integra com os módulos anteriores (specs, testes, PRs)

Para retomar: leia o PROGRESS.md e me coloque em contexto

---

## Sessão 10 — 2026-10-26

### O que foi feito

**Módulo 7: Context Engineering — CONCLUÍDO**

| Subseção | Destaque |
|----------|----------|
| `01-conceito/` | 4 camadas de contexto (memory/rules/CLAUDE.md/conversa), problema da janela finita, trade-off rico vs relevante, anti-padrões |
| `02-workflow/` | Ciclo seed→trabalho→compactar→persistir→retomar, estratégia por tipo de tarefa |
| `03-templates/` | 3 templates: CLAUDE.md mínimo viável (com exemplo JWT), prompt de retomada (4 variações), context seed (implementação/debug/revisão) |
| `04-ia-no-fluxo/` | /compact (quando, o que preserva), fork agent vs fresh agent (comparativo), gestão dos 3 mecanismos de persistência |
| `05-exemplos/` | Sessão longa (quando usar /compact), múltiplos agentes (fork pesquisa + fresh revisão), retomada de sessão (PROGRESS.md específico) |

### Decisões tomadas

- Módulo 7 usa o próprio AIAD como exemplo principal: os 3 mecanismos do projeto (memory + CLAUDE.md + PROGRESS.md) são a implementação concreta dos conceitos ensinados
- Templates de retomada têm 4 variações por situação: padrão, interrupção longa, tarefa específica, continuação da mesma semana

### Próxima sessão

**Módulo 8 — OWASP Top 10**

O que será coberto:
- As 10 vulnerabilidades mais críticas segundo OWASP e como identificá-las com IA
- Injection, Broken Auth, XSS, IDOR e as demais categorias aplicadas ao projeto JWT
- Prompts para análise de segurança por categoria OWASP
- Templates de checklist de segurança por tipo de endpoint
- Exemplos de vulnerabilidades no projeto JWT e como corrigi-las com IA

Para retomar: leia o PROGRESS.md e me coloque em contexto

---

## Sessão 11 — 2026-10-26

### O que foi feito

**Módulo 8: OWASP Top 10 — CONCLUÍDO**

| Subseção | Destaque |
|----------|----------|
| `01-conceito/` | As 10 categorias OWASP 2021, mapeamento para o projeto JWT (6 de 10 aplicáveis), por que IA muda a auditoria, anti-padrão do checklist binário |
| `02-workflow/` | Pipeline inventory → analyze → triage → fix → verify, tabela de severidade (CRÍTICO→INFO), integração no fluxo AIAD após M4, cadência recomendada |
| `03-templates/` | Prompt de auditoria completa, prompts por categoria (A01/A02/A03/A07/A09), template de correção, finding-report.md |
| `04-ia-no-fluxo/` | Como invocar `/audit-owasp`, exemplo de saída completa, como usar os resultados, limitações (A06 requer pip audit, A04 requer visão arquitetural) |
| `05-exemplos/` | A01 Broken Access Control (IDOR em /user/profile), A02 Crypto Failures (JWT_SECRET fraco + algoritmo none), A07 Auth Failures (sem rate limit + sem log) |

**Skill `/audit-owasp` criada** em `.claude/skills/audit-owasp/SKILL.md`:
- Aceita arquivo(s) como argumento ou pergunta se não informado
- 5 etapas: scan → analyze (10 categorias) → report estruturado → fix (CRÍTICO/ALTO) → verify
- Critérios detalhados por categoria no SKILL.md
- A06 sempre marcada como "requer pip audit externo"

### Decisões tomadas

- Exemplos focam em A01, A02 e A07 — as 3 categorias com maior impacto direto no projeto JWT
- A04 (Insecure Design) e A06 (Outdated Components) documentadas com limitação explícita: precisam de julgamento humano e ferramentas externas respectivamente
- Rate limit padrão sugerido de 5/min por IP com nota sobre Redis para produção com múltiplos workers

### Próxima sessão

**Módulo 9 — Quality Gate**

O que será coberto:
- O que são quality gates e onde se encaixam no pipeline CI/CD
- Cobertura de testes como gate (threshold mínimo)
- Análise estática (linting, type checking) como gate
- Integração com resultados do OWASP audit (M8) como gate de segurança
- Configuração de gates no GitHub Actions / pipeline local

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
