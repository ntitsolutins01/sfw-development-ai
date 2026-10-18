# Módulo 2 — Spec Driven Development

> **Conceito:** escrever a especificação antes do código — e usar a IA para gerar, revisar e validar essa especificação em cada etapa do ciclo.

---

## O Problema que este Módulo Resolve

Quando você pede para uma IA implementar uma feature sem especificação, ela toma decisões por você: qual banco de dados usar, como tratar erros, quais campos são obrigatórios, o que retornar em caso de falha. Cada decisão implícita é um ponto de divergência entre o que você queria e o que foi gerado.

Spec Driven Development inverte isso: você define as decisões antes, e a IA implementa dentro dos limites que você estabeleceu.

---

## O que você vai aprender

| Subseção | Conteúdo |
|----------|----------|
| `01-conceito/` | O que é um spec, quando usar, diferença de ticket/story |
| `02-workflow/` | Fluxo completo: brainstorm → PRD → TRD → spec → revisão → implementação → validação |
| `03-templates/` | Templates prontos: feature, bugfix, refactor, API endpoint |
| `04-ia-no-fluxo/` | Prompts para revisar, implementar e validar specs com IA |
| `05-exemplos/` | 3 specs reais preenchidos com comentários |
| `06-pre-spec/` | Skills `/brainstorm`, `/escrever-prd` e `/escrever-trd` — etapas antes do spec técnico |

---

## Pré-requisitos

- Módulo 1 concluído (Claude Code configurado com `settings.json` e `CLAUDE.md`)
- Familiaridade com o conceito de ticket/user story (não é pré-requisito técnico)

---

## Quando Usar SDD

| Situação | O que fazer |
|----------|-------------|
| Feature nova com mais de 1 arquivo impactado | ✅ Fluxo completo |
| Bugfix com causa conhecida e localizada | ⚠️ Só o spec (`03-templates/bugfix.md`) |
| Refactor que muda interface pública | ✅ Fluxo completo |
| Endpoint de API novo | ✅ Fluxo completo |
| Correção de typo ou ajuste de estilo | ❌ Não precisa de spec |
| Ideia ainda não clara, sem saber a abordagem | `/brainstorm` antes de qualquer spec |
| Feature com impacto de produto, precisa alinhar o time | `/escrever-prd` antes do spec técnico |
| Início de projeto ou mudança de stack/arquitetura | `/escrever-trd` para registrar restrições globais |

---

## O Ciclo SDD com IA

```
┌─────────────────────────────────────────────────────────┐
│               PRÉ-SPEC  (opcional por feature)          │
│                                                         │
│   /brainstorm       matura a ideia, aponta trade-offs   │
│          │          → docs/brainstorms/                  │
│          ▼                                              │
│   /escrever-prd     define O QUE construir (produto)    │
│          │          → docs/prds/NNN-nome.md             │
│          ▼                                              │
│   /escrever-trd     restrições técnicas globais         │
│                     → docs/trd.md  (uma vez / projeto)  │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│               SPEC TÉCNICO  (obrigatório)               │
│                                                         │
│   1. ESCREVER SPEC      templates em 03-templates/      │
│          │              → docs/specs/                   │
│          ▼                                              │
│   2. REVISAR COM IA     aponta ambiguidades e gaps      │
│          │              prompts em 04-ia-no-fluxo/      │
│          ▼                                              │
│   3. IMPLEMENTAR        dentro dos limites do spec      │
│          │                                              │
│          ▼                                              │
│   4. VALIDAR            verifica cada critério de aceite│
└─────────────────────────────────────────────────────────┘
```

---

## Integração com Outros Módulos

- **Módulo 3 (TDD):** o spec define os casos de teste antes do código
- **Módulo 4 (Pull Request Review):** o spec é o critério de aceite da revisão de PR
- **Módulo 5 (Issue Analysis):** issues bem analisadas geram specs mais completos
