# 03 — Templates de Spec

Quatro templates prontos para os tipos mais comuns de mudança.

## Como usar

> **[TEMPLATE] Como usar estes arquivos**
>
> 1. Copie o template correspondente ao tipo de mudança:
>    ```bash
>    cp modules/02-spec-driven-development/03-templates/feature.md docs/specs/YYYY-MM-DD-nome-da-feature.md
>    ```
> 2. Preencha cada seção — não deixe campos em branco, escreva "N/A" se não aplicável
> 3. **Se você veio do `/escrever-prd`:** os critérios de aceite do PRD já estão prontos —
>    transporte-os para a seção `## 4. Critérios de Aceite` adaptando para linguagem técnica.
>    A seção `## 6. Restrições` deve referenciar o `docs/trd.md` em vez de repetir restrições globais.
> 4. Use o prompt de revisão (ver `02-workflow/README.md`) antes de implementar
> 5. Mantenha o spec junto ao PR como critério de aceite

---

## Qual template usar

| Situação | Template |
|----------|----------|
| Nova funcionalidade | `feature.md` |
| Correção de bug | `bugfix.md` |
| Refatoração com mudança de contrato | `refactor.md` |
| Novo endpoint REST ou GraphQL | `api-endpoint.md` |

---

## Convenção de nome de arquivo

```
docs/specs/YYYY-MM-DD-<tipo>-<slug>.md

Exemplos:
  docs/specs/2026-10-18-feature-autenticacao-oauth.md
  docs/specs/2026-10-18-bugfix-timeout-upload.md
  docs/specs/2026-10-18-api-endpoint-usuarios.md
```

---

## Arquivos disponíveis

- `feature.md` — feature nova
- `bugfix.md` — correção de bug
- `refactor.md` — refatoração
- `api-endpoint.md` — endpoint de API
