# Templates de Issue

## Qual template usar

| Tipo | Template | Quando usar |
|------|----------|-------------|
| Algo quebrado | `issue-bug.md` | Comportamento atual difere do esperado |
| Nova capacidade | `issue-feature.md` | Sistema não tem a funcionalidade ainda |
| Trabalho técnico | `issue-task.md` | Refatoração, migração, configuração, dívida técnica |

## Convenção de título

| Tipo | Prefixo | Exemplo |
|------|---------|---------|
| Bug | `[BUG]` | `[BUG] POST /auth/login retorna 500 com senha contendo @` |
| Feature | `[FEAT]` | `[FEAT] Autenticação JWT com login e logout` |
| Task | `[TASK]` | `[TASK] Migrar UserService para padrão Repository` |

## Labels recomendados

- `type: bug` / `type: feature` / `type: task`
- `priority: critical` / `priority: high` / `priority: medium` / `priority: low`
- `module: 02-spec` / `module: 03-tdd` (para rastreabilidade no AIAD)