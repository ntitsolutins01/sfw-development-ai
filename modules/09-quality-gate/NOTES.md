# Módulo 9 — Quality Gate (Notas para Implementação)

> Este módulo ainda não foi implementado.
> Este arquivo registra decisões e referências para quando ele for criado.

---

## O que será coberto (referência do curso DAPIA)

- Portões de qualidade em pipelines de software
- Teste de carga
- Complexidade ciclomática
- Cobertura de testes (coverage)

---

## Referência: JEV como Quality Gate em Pipelines LLM

Quando este módulo for criado, o **JEV** (`shared/jev/`) deve ser apresentado
como exemplo concreto do conceito de quality gate aplicado a pipelines LLM.

### Por que o JEV é um quality gate

Um quality gate é uma decisão binária que controla se o fluxo prossegue
ou é interrompido com base em critérios objetivos. O JEV tem dois gates:

| Gate | Critério de passagem | O que bloqueia |
|------|---------------------|----------------|
| Intent Gate | `intent == ANSWERABLE` | Saudações e perguntas meta |
| Chunk Scorer | `similarity >= threshold` | Chunks semanticamente distantes |

Isso é o mesmo princípio de um quality gate de CI/CD:
- Gate de cobertura: `coverage >= 80%` → senão, bloqueia o merge
- Gate de complexidade: `cyclomatic_complexity <= 10` → senão, falha o build
- Gate JEV: `similarity >= 0.5` → senão, não passa para o LLM

### Como usar no módulo 9

```
Exemplos a cobrir no módulo:

1. Quality gates tradicionais (CI/CD)
   - Cobertura de testes: pytest-cov com threshold mínimo
   - Complexidade ciclomática: radon com limite máximo
   - Teste de carga: locust com SLA de latência

2. Quality gates em pipelines LLM (extensão do conceito)
   - Intent gate: bloqueia inputs fora do escopo
   - Chunk scorer: bloqueia contexto irrelevante
   - LLM as Judge (módulo 14): avalia qualidade da resposta gerada

Referência de código: shared/jev/ (já implementado)
```

---

## Pré-requisitos quando implementar

- [ ] `shared/jev/` já existe — importar exemplos de lá
- [ ] `shared/prompt_caching/` já existe — usar junto nos exemplos LLM
- [ ] Módulo 14 (LLM as Judge) também se relaciona — verificar se foi criado
