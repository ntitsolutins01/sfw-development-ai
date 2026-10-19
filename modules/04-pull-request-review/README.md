# Módulo 4 — Pull Request Review com IA

> **Conceito:** usar IA para revisar Pull Requests de forma sistemática — verificando conformidade com o spec, cobertura de testes e qualidade do código antes de qualquer merge.

---

## O Problema que este Módulo Resolve

Revisões de PR manuais são inconsistentes: um dia você verifica segurança, outro dia foca só na lógica, e cobertura de testes raramente é checada formalmente. Com IA, a revisão segue um checklist completo toda vez — sem fadiga, sem viés, sem esquecer categorias.

O Módulo 4 fecha o ciclo SDD+TDD: o spec (Módulo 2) define o que deve ser implementado, os testes (Módulo 3) verificam que funciona, e o PR Review verifica que a implementação cobre os critérios de aceite e não introduz problemas novos.

---

## O que você vai aprender

| Subseção | Conteúdo |
|----------|----------|
| `01-conceito/` | O que verificar em um PR, categorias de severidade, anti-padrões de revisão |
| `02-workflow/` | Fluxo completo: self-review → revisão por IA → revisão humana → merge |
| `03-templates/` | Checklists prontos para feature, bugfix e refatoração |
| `04-ia-no-fluxo/` | 6 prompts prontos para cada etapa da revisão |
| `05-exemplos/` | 3 revisões reais ligadas aos exemplos dos Módulos 2 e 3 |

---

## Integração com os Módulos Anteriores

```
Módulo 2 (Spec) ──→ spec com CAs definidos
                          ↓
Módulo 3 (TDD)  ──→ testes cobrindo os CAs
                          ↓
Módulo 4 (PR)   ──→ revisão verifica:
                     ✓ implementação cobre os CAs do spec?
                     ✓ testes cobrem todos os casos?
                     ✓ código não introduz bugs ou vulnerabilidades?
                          ↓
                     APROVADO ou SOLICITAR MUDANÇAS
```

---

## Skills deste Módulo

| Skill | Como invocar | O que faz |
|-------|-------------|-----------|
| **code-review** | `/code-review` | Revisão geral: bugs, segurança, performance, qualidade |
| **review-pr** | `/review-pr` | Revisão com spec: conformidade com CAs, cobertura de testes, decisão formal |

> A skill `/code-review` já existe em `modules/01-claude-code-cursor/03-skills/exemplos/code-review/`.
> A skill `/review-pr` é criada neste módulo em `.claude/skills/review-pr/SKILL.md`.

---

## Pré-requisitos

- Módulo 1 concluído (Claude Code configurado)
- Módulo 2 concluído (entendimento de specs e critérios de aceite)
- Módulo 3 concluído (TDD — testes escritos antes da implementação)
- Branch com mudanças prontas para revisar

---

## Como usar na prática

### Cenário: revisar o PR do sistema de autenticação JWT (continuação do Módulo 3)

**Pré-condição:** você tem um branch com a implementação do `auth_service.py` e os testes passando (resultado do Módulo 3).

**Passo 1 — Instalar a skill `/review-pr`**

Copie `.claude/skills/review-pr/SKILL.md` para o seu projeto de prova:
```
.claude/skills/review-pr/SKILL.md
```

**Passo 2 — Self-review antes de abrir o PR**

Abra `03-templates/checklist-feature.md`, percorra cada item e corrija o que encontrar antes de pedir revisão da IA.

**Passo 3 — Revisão geral com `/code-review`**

No Claude Code, com o branch do JWT ativo:
```
/code-review
```
Corrija todos os achados CRÍTICO e ALTO antes de continuar.

**Passo 4 — Revisão com spec usando `/review-pr`**

```
/review-pr docs/specs/001-autenticacao-jwt.md
```
A IA vai comparar o diff com cada critério de aceite do spec e indicar quais estão cobertos e quais estão faltando.

**Passo 5 — Corrigir e re-revisar**

Corrija os problemas encontrados, rode os testes (`pytest`) e execute `/review-pr` novamente até obter aprovação.

**O que valida a conclusão:**
- [ ] Self-review feito com o checklist de feature
- [ ] `/code-review` executado — zero achados CRÍTICO ou ALTO no resultado final
- [ ] `/review-pr` executado com o spec — todos os CAs marcados como cobertos
- [ ] Testes continuam passando após as correções

**[Referência completa](README.md)**