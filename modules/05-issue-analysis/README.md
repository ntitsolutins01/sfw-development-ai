# Módulo 5 — Issue Analysis com IA

> **Conceito:** usar IA para transformar issues brutas e ambíguas em tasks verificáveis com critérios de aceite — e gerar o stub de spec pronto para o Módulo 2.

---

## O Problema que este Módulo Resolve

Issues brutas são ambíguas por natureza. "Fix the login" não é acionável. "POST /auth/login retorna 500 quando a senha contém caracteres especiais" é acionável. A diferença não é óbvia para quem escreveu a issue — mas é crítica para quem vai implementar.

Sem análise, você vai para o Módulo 2 (spec) sem entender o escopo real, e vai para o Módulo 3 (TDD) sem saber quais casos cobrir. Com análise, você começa o spec com os CAs já extraídos e os limites de escopo definidos.

---

## Posição no Ciclo AIAD

```
Issue bruta (GitHub/Jira/Linear)
    ↓
Módulo 5 (Issue Analysis)
    ↓  tasks atômicas + CAs + stub de spec
Módulo 2 (Spec)
    ↓  spec completo com CAs revisados
Módulo 3 (TDD)
    ↓  testes cobrindo os CAs
Módulo 4 (PR Review)
    ↓  revisão com conformidade ao spec
Merge
```

---

## O que você vai aprender

| Subseção | Conteúdo |
|----------|----------|
| `01-conceito/` | Tipos de issue, o que torna uma issue analisável, anti-padrões |
| `02-workflow/` | Fluxo completo: issue raw → análise → decomposição → spec stub |
| `03-templates/` | Templates de issue bem escrita: bug, feature, task técnica |
| `04-ia-no-fluxo/` | 6 prompts para cada etapa da análise |
| `05-exemplos/` | 3 análises reais ligadas aos exemplos dos Módulos 2–4 |

---

## Skill deste Módulo

| Skill | Como invocar | O que faz |
|-------|-------------|-----------|
| **analyze-issue** | `/analyze-issue` | Analisa issue, decompõe em tasks com CAs e gera stub de spec para o Módulo 2 |

---

## Pré-requisitos

- Módulo 1 concluído (Claude Code configurado)
- Módulo 2 concluído (entendimento de specs e critérios de aceite)
- Uma issue para analisar (texto, arquivo ou link do GitHub)

---

## Como usar na prática

### Cenário: analisar a issue que originou o sistema de autenticação JWT

**Passo 1 — Instalar a skill `/analyze-issue`**

Copie `.claude/skills/analyze-issue/SKILL.md` para `.claude/skills/analyze-issue/SKILL.md` no seu projeto de prova.

**Passo 2 — Identificar e copiar a issue**

Pegue uma issue real do seu backlog — pode ser uma do GitHub, Jira ou Linear. Para este guia, use a issue de exemplo em `05-exemplos/analise-issue-feature-auth.md`.

**Passo 3 — Análise inicial com Prompt 1**

Abra `04-ia-no-fluxo/README.md`, use o **Prompt 1** colando o texto da issue. A IA vai:
- Classificar o tipo (bug / feature / task)
- Identificar ambiguidades e informações faltando
- Listar perguntas de clarificação

Responda as perguntas ou assuma os valores padrão se a issue for sua.

**Passo 4 — Decomposição com Prompt 2**

Use o **Prompt 2** com a issue clarificada. A IA vai decompor em tasks atômicas e independentes.

**Passo 5 — Gerar CAs com Prompt 3**

Use o **Prompt 3** para extrair critérios de aceite verificáveis para cada task.

**Passo 6 — Gerar stub de spec com Prompt 6**

Use o **Prompt 6** para gerar o esqueleto do spec em `docs/specs/NNN-nome.md` — pronto para ser completado no Módulo 2.

**O que valida a conclusão:**
- [ ] Issue classificada por tipo com ambiguidades identificadas
- [ ] Issue decomposta em tasks atômicas (cada task implementável em isolamento)
- [ ] Cada task tem ao menos 2 CAs verificáveis (caso feliz + caso de falha)
- [ ] Stub de spec gerado em `docs/specs/` pronto para o Módulo 2

**[Referência completa](README.md)**