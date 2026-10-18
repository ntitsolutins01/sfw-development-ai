# 03 — Templates de Teste

Três templates prontos para os tipos mais comuns de teste em TDD com IA.

## Como usar

> **[TEMPLATE] Como usar estes arquivos**
>
> 1. Identifique o tipo de teste que precisa escrever
> 2. Copie o template correspondente para o diretório de testes do seu projeto:
>    ```bash
>    # Python
>    cp modules/03-tdd/03-templates/unit-pytest.md tests/test_<nome>.py
>
>    # JavaScript
>    cp modules/03-tdd/03-templates/unit-jest.md src/__tests__/<nome>.test.ts
>    ```
> 3. Substitua os comentários `[PREENCHA]` com o conteúdo real
> 4. Use o Prompt 1 de `04-ia-no-fluxo/README.md` para gerar os casos de teste
>    a partir dos CAs do spec

---

## Qual template usar

| Situação | Template |
|----------|----------|
| Teste de função/método isolado em Python | `unit-pytest.md` |
| Teste de função/módulo isolado em JS/TS | `unit-jest.md` |
| Teste com banco de dados, serviço ou API interna | `integration-pytest.md` |

---

## Estrutura padrão: Arrange / Act / Assert

Todos os templates seguem o padrão AAA:

```
Arrange  →  prepare os dados e o contexto do teste
Act      →  execute a ação que está sendo testada
Assert   →  verifique o resultado esperado
```

Cada seção tem um comentário no template. Nunca remova os comentários — eles facilitam a leitura do teste por outras pessoas (e pela IA quando for revisar).

---

## Arquivos disponíveis

- `unit-pytest.md` — testes unitários com pytest (Python)
- `unit-jest.md` — testes unitários com jest/vitest (JavaScript/TypeScript)
- `integration-pytest.md` — testes de integração com pytest + fixtures de banco
