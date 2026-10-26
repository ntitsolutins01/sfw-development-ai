# Módulo 6 — Prompt Engineering

> Posição no ciclo AIAD: **transversal** — as técnicas deste módulo melhoram a qualidade de cada interação em todos os outros módulos.

Escrever prompts bem estruturados é a diferença entre uma resposta genérica e uma resposta que funciona na primeira tentativa. Este módulo cobre as técnicas essenciais de engenharia de prompts aplicadas ao ciclo de desenvolvimento de software.

---

## O que você vai aprender

- Como estruturar prompts com o framework **CIFER** (Contexto, Instrução, Formato, Exemplos, Restrições)
- As 6 técnicas principais: zero-shot, few-shot, chain-of-thought, role prompting, structured output, constrained prompting
- Onde cada técnica se encaixa no ciclo AIAD
- Anti-padrões que degradam a qualidade das respostas
- Como iterar e refinar prompts sistematicamente

---

## Posição no Ciclo AIAD

```text
M1: Ambiente    M2: Spec    M3: TDD    M4: PR Review    M5: Issues
     ↑               ↑          ↑            ↑               ↑
     └───────────────┴──────────┴────────────┴───────────────┘
                         M6: Prompt Engineering
                    (melhora todas as interações acima)
```

Prompt Engineering não é um passo sequencial — é uma camada transversal que aumenta a precisão de qualquer interação com a IA.

---

## Estrutura do Módulo

| Subseção | O que cobre |
|----------|-------------|
| [`01-conceito/`](01-conceito/README.md) | Framework CIFER, 6 técnicas, anti-padrões |
| [`02-workflow/`](02-workflow/README.md) | Ciclo de otimização: escrever → testar → medir → refinar |
| [`03-templates/`](03-templates/README.md) | Templates prontos por tipo de tarefa de desenvolvimento |
| [`04-ia-no-fluxo/`](04-ia-no-fluxo/README.md) | 6 técnicas com exemplos aplicados ao ciclo AIAD |
| [`05-exemplos/`](05-exemplos/) | Comparativos antes/depois para o mesmo problema |

---

## Skill deste Módulo

Este módulo não tem skill dedicada — as técnicas são aplicadas diretamente nos prompts que você escreve nas skills dos outros módulos (`/analyze-issue`, `/review-pr`, `/escrever-prd`, etc.).

---

## Como usar na prática

**Cenário:** você quer melhorar a qualidade das respostas que recebe do Claude Code ao trabalhar no ciclo AIAD.

**Passos:**

1. Leia [`01-conceito/README.md`](01-conceito/README.md) — aprenda o framework CIFER e identifique quais componentes você costuma omitir nos seus prompts
2. Leia [`02-workflow/README.md`](02-workflow/README.md) — entenda o ciclo de otimização e onde cada técnica se encaixa nas fases do AIAD
3. Copie o template relevante de [`03-templates/`](03-templates/README.md) para o tipo de tarefa que está fazendo (geração de código, debug ou refatoração)
4. Estude os comparativos de [`05-exemplos/`](05-exemplos/) — veja como o mesmo problema produz resultados completamente diferentes com prompts ruins vs bem estruturados
5. Aplique as técnicas de [`04-ia-no-fluxo/`](04-ia-no-fluxo/README.md) na próxima interação com o Claude Code e compare o resultado

**Checklist de conclusão:**

- [ ] Framework CIFER compreendido — você consegue identificar os 5 componentes em qualquer prompt
- [ ] Você reescreveu ao menos um prompt seus usando o framework e percebeu diferença na resposta
- [ ] Você identificou 2 anti-padrões nos seus prompts atuais
- [ ] Templates de geração, debug e refatoração testados no projeto de prova (sistema JWT)
- [ ] Você sabe quando usar few-shot vs chain-of-thought vs role prompting