# 02 — Workflow SDD com IA

## O Fluxo Completo (com pré-spec)

```
[/brainstorm]            matura a ideia — trade-offs, alternativas, premissas
      │                  → docs/brainstorms/YYYY-MM-DD-slug.md (opcional)
      ▼
[/escrever-prd]          define O QUE construir (produto)
      │                  → docs/prds/NNN-nome.md
      ▼
[/escrever-trd]          define restrições técnicas globais (UMA VEZ por projeto)
      │                  → docs/trd.md + docs/adrs/
      ▼
[spec técnico]           define COMO implementar (por feature/bugfix)
      │                  → docs/specs/YYYY-MM-DD-tipo-slug.md
      │
      └── ver 06-pre-spec/README.md para documentação completa das 3 primeiras etapas
```

> As etapas de brainstorm, PRD e TRD são **opcionais por feature** mas recomendadas.
> O TRD é escrito uma única vez no início do projeto.
> A partir do spec técnico, o fluxo abaixo é obrigatório.

---

## O Ciclo em 4 Etapas (a partir do spec técnico)

```
┌──────────────────────────────────────────────────────────────────┐
│  ETAPA 1 — ESCREVER O SPEC                                       │
│  Você preenche o template com: contexto, escopo, comportamento,  │
│  critérios de aceite, impacto e restrições.                      │
│  Ferramenta: qualquer editor + templates de 03-templates/        │
└──────────────────────────────────┬───────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│  ETAPA 2 — REVISAR COM IA                                        │
│  Você entrega o spec para o Claude Code e pede uma revisão.      │
│  A IA aponta: ambiguidades, gaps, conflitos, casos não cobertos. │
│  Você ajusta o spec antes de implementar.                        │
│  Ferramenta: Claude Code (ver prompts em 04-ia-no-fluxo/)        │
└──────────────────────────────────┬───────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│  ETAPA 3 — IMPLEMENTAR                                           │
│  Você entrega o spec revisado para a IA implementar.             │
│  A IA trabalha dentro dos limites definidos no spec.             │
│  Ferramenta: Claude Code (ver prompts em 04-ia-no-fluxo/)        │
└──────────────────────────────────┬───────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│  ETAPA 4 — VALIDAR                                               │
│  Você pede para a IA verificar se a implementação satisfaz       │
│  cada critério de aceite do spec.                                │
│  Ferramenta: Claude Code + testes (Módulo 3)                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Etapa 1 — Escrever o Spec

Use os templates de `03-templates/` como ponto de partida. Escolha o tipo:

- `feature.md` — nova funcionalidade
- `bugfix.md` — correção de bug
- `refactor.md` — refatoração com mudança de interface
- `api-endpoint.md` — novo endpoint REST/GraphQL

**Dica:** preencha o spec antes de abrir o editor de código. Se você não consegue preencher os critérios de aceite, ainda não entendeu o que precisa ser feito.

---

## Etapa 2 — Revisar com IA

Antes de implementar, entregue o spec para revisão. A IA vai encontrar problemas que você não viu.

**Prompt de revisão:**

```
Revise o spec abaixo antes de implementarmos. Identifique:
1. Ambiguidades que impediriam uma implementação correta
2. Casos de borda não cobertos pelos critérios de aceite
3. Conflitos com padrões comuns de [Python/Node/etc]
4. Informações faltando sobre impacto ou restrições

Não implemente nada ainda — apenas liste os problemas encontrados.

--- SPEC ---
[cole o spec aqui]
```

**O que fazer com o resultado:** ajuste o spec com base no feedback. Repita até a IA não encontrar mais problemas críticos.

---

## Etapa 3 — Implementar

Com o spec revisado, peça a implementação.

**Prompt de implementação:**

```
Implemente o que está descrito no spec abaixo.
Siga rigorosamente os critérios de aceite.
Se encontrar ambiguidade durante a implementação, pare e pergunte — não assuma.

--- SPEC ---
[cole o spec revisado aqui]
```

**O que monitorar durante a implementação:**
- A IA está seguindo os critérios de aceite ou tomando decisões próprias?
- A IA está pedindo permissão para decisões fora do escopo?
- Os arquivos impactados batem com o que você listou no spec?

---

## Etapa 4 — Validar

Após a implementação, peça uma validação contra o spec original.

**Prompt de validação:**

```
Compare a implementação atual com o spec abaixo.
Para cada critério de aceite, informe: ✅ satisfeito / ❌ não satisfeito / ⚠️ parcial.
Liste qualquer divergência entre o que foi implementado e o que o spec define.

--- SPEC ---
[cole o spec original aqui]
```

---

## Integração com o CLAUDE.md do Projeto

Se você usa SDD em todos os projetos, adicione ao seu `CLAUDE.md`:

```markdown
## Workflow de Desenvolvimento

Antes de implementar qualquer feature, bugfix ou refactor não trivial:
1. Preencha o spec usando os templates em `docs/specs/`
2. Peça revisão do spec antes de implementar
3. Implemente dentro dos limites do spec
4. Valide a implementação contra os critérios de aceite
```

---

## Integração com Módulos do Curso

| Módulo | Como o spec se conecta |
|--------|------------------------|
| **Módulo 3 — TDD** | Critérios de aceite do spec viram casos de teste |
| **Módulo 4 — PR Review** | Spec é o critério de aceite da revisão |
| **Módulo 5 — Issue Analysis** | Issue bem analisada gera spec mais completo |
