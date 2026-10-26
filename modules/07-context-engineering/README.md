# Módulo 7 — Context Engineering

> Posição no ciclo AIAD: **transversal** — as técnicas deste módulo se aplicam a todas as sessões de trabalho, especialmente as longas.

Context Engineering é a prática de gerenciar o que o modelo vê, quando vê, e quanto tempo isso persiste. Prompts bem escritos (M6) resolvem uma interação. Context Engineering resolve uma sessão, um projeto, e a transição entre eles.

---

## O que você vai aprender

- As 4 camadas de contexto em Claude Code e quando cada uma é a ferramenta certa
- O problema da janela finita: o que acontece quando o contexto fica grande demais
- Estratégias de seed, compactação, persistência e retomada de contexto
- Quando usar `/compact`, fork agent, fresh agent e memory
- Como o AIAD usa context engineering em todas as suas sessões

---

## Posição no Ciclo AIAD

```text
Sessão 1              Sessão 2              Sessão N
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ seed        │      │ retomada    │      │ retomada    │
│ trabalho    │  ──► │ trabalho    │  ──► │ trabalho    │
│ persistir   │      │ persistir   │      │ persistir   │
└─────────────┘      └─────────────┘      └─────────────┘
       ↑
Context Engineering garante que cada sessão começa com contexto
relevante e termina com o estado persistido corretamente.
```

---

## Estrutura do Módulo

| Subseção | O que cobre |
|----------|-------------|
| [`01-conceito/`](01-conceito/README.md) | 4 camadas de contexto, janela finita, anti-padrões |
| [`02-workflow/`](02-workflow/README.md) | Ciclo seed → trabalho → compactar → persistir → retomar |
| [`03-templates/`](03-templates/README.md) | Templates de CLAUDE.md, prompt de retomada, context seed |
| [`04-ia-no-fluxo/`](04-ia-no-fluxo/README.md) | `/compact`, fork agent, fresh agent, memory vs CLAUDE.md |
| [`05-exemplos/`](05-exemplos/) | Sessão longa, múltiplos agentes, retomada de sessão interrompida |

---

## Como usar na prática

**Cenário:** você está desenvolvendo uma feature que vai levar 3 sessões. Quer garantir que cada sessão começa com contexto relevante e termina com o estado persistido.

**Passos:**

1. Leia [`01-conceito/README.md`](01-conceito/README.md) — entenda as 4 camadas e identifique qual mecanismo você já usa e qual está faltando
2. Monte o seu CLAUDE.md usando o template de [`03-templates/claude-md-projeto.md`](03-templates/claude-md-projeto.md)
3. No início de cada nova sessão, use o prompt de [`03-templates/prompt-retomada.md`](03-templates/prompt-retomada.md) para fazer o seed de contexto
4. Quando a sessão crescer (>50 trocas), aplique `/compact` seguindo as orientações de [`04-ia-no-fluxo/README.md`](04-ia-no-fluxo/README.md)
5. Ao final de cada sessão, atualize os 3 mecanismos de persistência com `/salvar-contexto`
6. Estude [`05-exemplos/sessao-longa.md`](05-exemplos/sessao-longa.md) para ver como o AIAD aplica essas técnicas nas suas próprias sessões

**Checklist de conclusão:**

- [ ] Você consegue nomear as 4 camadas de contexto em Claude Code e o propósito de cada uma
- [ ] CLAUDE.md do projeto de prova tem as seções mínimas (regras, stack, decisões, status)
- [ ] Você usou o prompt de retomada para iniciar uma sessão a partir do PROGRESS.md
- [ ] Você sabe quando usar fork agent vs fresh agent vs continuar na mesma sessão
- [ ] Você aplicou `/compact` em uma sessão longa e verificou que o contexto essencial foi preservado