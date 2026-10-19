# Templates de Checklist

## Qual template usar

| Tipo de mudança | Template |
|-----------------|----------|
| Feature nova ou adição de funcionalidade | `checklist-feature.md` |
| Correção de bug | `checklist-bugfix.md` |
| Refatoração (sem mudança de comportamento externo) | `checklist-refactor.md` |

Se a mudança mistura tipos (ex: bugfix + refactor), use o template do tipo dominante e adicione os itens relevantes do outro.

---

## Como usar os templates

1. Copie o template para o seu PR (como descrição ou como arquivo temporário)
2. Percorra cada item **antes** de executar `/code-review` ou `/review-pr`
3. Marque `[x]` nos itens concluídos e `[N/A]` nos que não se aplicam
4. Para itens não marcados, adicione uma justificativa

O self-review não substitui a revisão por IA — ele garante que você entregue um PR limpo antes de pedir revisão.

---

## Convenção de nome para branches e PRs

| Tipo | Branch | Título do PR |
|------|--------|--------------|
| Feature | `feature/<nome-curto>` | `feat: <descrição em imperativo>` |
| Bugfix | `fix/<nome-curto>` | `fix: <descrição do bug corrigido>` |
| Refactor | `refactor/<nome-curto>` | `refactor: <o que foi reorganizado>` |

Exemplos:
- `feature/autenticacao-jwt` → `feat: add JWT authentication with login and logout`
- `fix/token-expiry` → `fix: correct token expiration to 24h instead of 24 minutes`
- `refactor/auth-service` → `refactor: extract token validation to dedicated class`