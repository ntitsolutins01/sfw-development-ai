# Template — CLAUDE.md para Projeto Novo

Use este template como ponto de partida ao criar o CLAUDE.md de um projeto novo. Mantenha-o enxuto: o objetivo é dar contexto suficiente para o modelo trabalhar bem, não documentar tudo.

> **Regra prática:** se você precisar de mais de 100 linhas, provavelmente tem conteúdo que deveria estar em Rules (restrições) ou Memory (detalhes históricos), não no CLAUDE.md.

---

## Template

```markdown
# [Nome do Projeto] — Contexto para o Claude Code

## Stack

- **Linguagem:** [ex: Python 3.11]
- **Framework:** [ex: FastAPI 0.110]
- **Banco de dados:** [ex: PostgreSQL 15 via SQLAlchemy]
- **Testes:** [ex: pytest 8]
- **Infraestrutura:** [ex: Docker Compose em dev, Railway em prod]

## Estrutura do projeto

[Apenas as pastas que o modelo precisa conhecer]

```
[nome-projeto]/
├── app/
│   ├── services/    ← lógica de negócio
│   ├── models/      ← SQLAlchemy models
│   └── routes/      ← FastAPI routers
├── tests/
│   ├── unit/
│   └── integration/
└── docs/specs/      ← specs das features
```

## Regras de desenvolvimento

- [regra 1 — ex: type hints obrigatórios em todas as funções]
- [regra 2 — ex: testes antes da implementação (TDD)]
- [regra 3 — ex: spec em docs/specs/ antes de qualquer feature nova]
- [regra 4 — ex: nunca commitar .env ou credenciais]

## Status atual

> Atualizado em: [YYYY-MM-DD]

- [x] [feature concluída 1]
- [x] [feature concluída 2]
- [ ] [próxima feature] ← em andamento
- [ ] [feature futura]

## Convenções de código

- Nomes de arquivo: snake_case
- Classes: PascalCase
- Testes: `test_[o_que_testa]_[contexto].py`
- Specs: `docs/specs/NNN-nome-da-feature.md`

## Para retomar uma sessão anterior

Leia o `PROGRESS.md` na raiz e siga a seção "Próxima sessão".
```

---

## Exemplo preenchido — sistema de autenticação JWT

```markdown
# auth-api — Contexto para o Claude Code

## Stack

- **Linguagem:** Python 3.11
- **Framework:** FastAPI 0.110
- **Banco de dados:** PostgreSQL 15 via SQLAlchemy 2
- **Cache:** Redis 7 (blocklist de tokens)
- **Testes:** pytest 8 com pytest-asyncio
- **Infraestrutura:** Docker Compose em dev

## Estrutura do projeto

```
auth-api/
├── app/
│   ├── services/auth.py     ← login, logout, verify_token
│   ├── repositories/        ← UserRepository (Repository Pattern)
│   ├── models/user.py       ← User SQLAlchemy model
│   └── routes/auth.py       ← POST /auth/login, POST /auth/logout
├── tests/
│   ├── unit/test_auth_service.py
│   └── integration/test_auth_routes.py
└── docs/specs/001-autenticacao-jwt.md
```

## Regras de desenvolvimento

- Type hints obrigatórios em todas as funções e métodos
- TDD: testes antes da implementação, sempre
- Spec em docs/specs/ antes de qualquer feature nova
- Nunca commitar .env ou JWT_SECRET_KEY

## Status atual

> Atualizado em: 2026-10-26

- [x] POST /auth/login (JWT com expiração 24h)
- [x] Blocklist Redis (logout com invalidação imediata)
- [x] Middleware de autenticação
- [ ] Refresh token ← próxima feature

## Convenções

- Nomes de arquivo: snake_case
- Repository Pattern: toda query de banco passa pelo repositório
- Erros de autenticação: sempre HTTPException(401, "Credenciais inválidas") — mesma mensagem para email inexistente e senha errada (evita user enumeration)

## Para retomar

Leia o PROGRESS.md e me coloque em contexto.
```

---

## O que NÃO colocar no CLAUDE.md

| Não coloque | Coloque em |
|-------------|-----------|
| Restrições de segurança permanentes | `.claude/rules/seguranca.md` |
| Padrões de código (type hints, imports) | `.claude/rules/python.md` |
| Histórico de decisões e motivos | Memory do projeto |
| Registro de sessões anteriores | `PROGRESS.md` |
| Documentação detalhada de cada função | Docstrings no código |