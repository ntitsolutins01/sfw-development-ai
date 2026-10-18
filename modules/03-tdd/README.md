# Módulo 3 — TDD com IA

> **Conceito:** escrever os testes antes do código — e usar a IA para implementar o código que faz os testes passarem.

---

## O Problema que este Módulo Resolve

Quando você pede para a IA implementar código diretamente, a verificação é subjetiva: você lê o código e decide se parece correto. TDD muda o critério de verificação: os testes definem o contrato, a IA implementa para satisfazê-lo, e o resultado é verde ou vermelho — sem leitura subjetiva.

Com specs do Módulo 2, o ciclo fecha completamente: os critérios de aceite do spec se tornam os casos de teste. A IA sabe exatamente o que deve ser verdade ao final.

---

## O que você vai aprender

| Subseção | Conteúdo |
|----------|----------|
| `01-conceito/` | Ciclo red-green-refactor, pirâmide de testes, TDD vs testar depois, anti-padrões |
| `02-workflow/` | Fluxo TDD com IA integrado ao SDD do Módulo 2 |
| `03-templates/` | Templates de testes: unit (pytest/jest), integration |
| `04-ia-no-fluxo/` | 6 prompts prontos para cada fase do ciclo TDD |
| `05-exemplos/` | 3 exemplos reais ligados aos specs do Módulo 2 |

---

## Pré-requisitos

- Módulo 1 concluído (Claude Code configurado)
- Módulo 2 concluído (entendimento de specs e critérios de aceite)
- Familiaridade básica com pytest ou jest — os exemplos explicam o que for necessário

---

## Relação com o Módulo 2

TDD é a camada executável do SDD. Os critérios de aceite do spec viram casos de teste:

```
Spec (Módulo 2)                   TDD (Módulo 3)
──────────────────────────────────────────────────
Critério de aceite             →  Caso de teste
Comportamento esperado         →  assert / expect
Caso de borda                  →  teste de edge case
Critério de falha              →  teste de erro
```

---

## O Ciclo TDD com IA

```
┌─────────────────────────────────────────────────┐
│                CICLO TDD + IA                   │
│                                                 │
│  1. ESCREVER TESTES  ←── critérios do spec      │
│         │            (você ou IA a partir dos CAs) │
│         ▼                                       │
│  🔴 RED — testes falham (código não existe)     │
│         │                                       │
│         ▼                                       │
│  2. IMPLEMENTAR  ←── prompt: "faça esses testes │
│         │            passarem"                  │
│         ▼                                       │
│  🟢 GREEN — todos os testes passam              │
│         │                                       │
│         ▼                                       │
│  3. REFATORAR  ←── IA refatora sem quebrar      │
│                    testes                       │
└─────────────────────────────────────────────────┘
```

---

## Como usar na prática

Siga estes passos partindo de um spec do Módulo 2:

**1. Tenha um spec pronto**

Você precisa de um spec com critérios de aceite preenchidos em `docs/specs/`. Se ainda não tem, volte ao Módulo 2.

**2. Gere os testes (fase Red)**

Abra `04-ia-no-fluxo/README.md` → use o **Prompt 1**. Cole os critérios de aceite do spec e peça para a IA gerar os casos de teste. Escolha o framework:
- Python → copie a estrutura de `03-templates/unit-pytest.md`
- JavaScript/TypeScript → copie de `03-templates/unit-jest.md`

**3. Confirme que os testes falham**

```bash
# Python
pytest tests/test_<nome>.py

# JavaScript
npm test
```

Todo teste deve falhar. Se algum passar antes da implementação, ele está testando algo errado — investigue antes de continuar.

**4. Implemente o código (fase Green)**

Use o **Prompt 2** de `04-ia-no-fluxo/README.md`. Cole o arquivo de testes e peça para a IA implementar o mínimo para fazê-los passar. Rode os testes novamente — todos devem ficar verdes.

**5. Refatore com segurança (fase Refactor)**

Use o **Prompt 3**. Cole o código implementado e os testes, peça para a IA melhorar legibilidade ou estrutura. Rode os testes após cada mudança — se quebrar algo, desfaça a última alteração.

**6. Verifique gaps de cobertura**

Use o **Prompt 6** para comparar os testes gerados com o spec original. A IA vai apontar CAs sem teste, casos de borda não cobertos e testes frágeis.

**7. Critério de sucesso**

Você concluiu o módulo quando:
- [ ] Todos os CAs do spec têm pelo menos dois testes (caso feliz + caso de falha)
- [ ] Os testes falharam antes da implementação (Red confirmado)
- [ ] `pytest` ou `npm test` mostra 100% verde após a implementação
- [ ] O refactor foi feito e os testes continuaram passando
- [ ] Você consegue explicar por que nunca se modifica um teste para fazê-lo passar

---

## Integração com Outros Módulos

- **Módulo 2 (SDD):** specs fornecem os critérios de aceite → casos de teste
- **Módulo 4 (Pull Request Review):** testes são critério de aceite na revisão de PR
- **Módulo 9 (Quality Gate):** cobertura mínima como gate antes de merge
