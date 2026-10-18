# Spec — Feature: Autenticação com JWT

> **Exemplo didático** — spec preenchido completo para uma feature de autenticação.
> Use como referência para aprender a preencher o template `03-templates/feature.md`.

**Data:** 2026-10-18
**Autor:** equipe backend
**Ticket/Issue:** #142
**Status:** [x] Aprovado

---

## 1. Contexto

A API atual não tem autenticação. Qualquer cliente pode chamar qualquer endpoint. Precisamos proteger os endpoints antes do lançamento público.

**Estado atual do sistema:**
Todos os endpoints são públicos. Não há conceito de sessão, usuário autenticado ou token. O modelo `User` já existe no banco mas não tem campo de senha.

---

## 2. Escopo

### Está dentro do escopo

- Endpoint `POST /auth/login` — autentica email + senha, retorna JWT
- Endpoint `POST /auth/logout` — invalida o token (adiciona à denylist)
- Middleware de autenticação que protege rotas marcadas
- Campo `password_hash` no modelo `User`
- Proteção dos endpoints existentes `/users/me` e `/projects/`

### Está fora do escopo

- Cadastro de usuário (já existe em `POST /users`)
- Refresh token (será feito na próxima sprint)
- Login social (OAuth, Google, GitHub)
- Recuperação de senha

---

## 3. Comportamento Esperado

### Fluxo principal — login

1. Cliente envia `POST /auth/login` com `{ email, password }`
2. Sistema busca o usuário pelo email
3. Sistema verifica o hash da senha com bcrypt
4. Sistema gera JWT com `user_id`, `email` e `exp` (1 hora)
5. Sistema retorna `{ token, expires_in: 3600 }`

### Fluxos alternativos

| Situação | Comportamento esperado |
|----------|----------------------|
| Email não cadastrado | Retorna `401` com `{ error: "invalid_credentials" }` — não indica se o email existe |
| Senha incorreta | Retorna `401` com `{ error: "invalid_credentials" }` — mesma mensagem do caso acima |
| Token expirado em rota protegida | Retorna `401` com `{ error: "token_expired" }` |
| Token inválido em rota protegida | Retorna `401` com `{ error: "invalid_token" }` |
| Logout com token já inválido | Retorna `200` — idempotente |

---

## 4. Critérios de Aceite

- [ ] **CA1:** `POST /auth/login` com credenciais válidas retorna `200` + `{ token: string, expires_in: 3600 }`
- [ ] **CA2:** `POST /auth/login` com email inexistente retorna `401` + `{ error: "invalid_credentials" }`
- [ ] **CA3:** `POST /auth/login` com senha errada retorna `401` + `{ error: "invalid_credentials" }` (mesmo body do CA2)
- [ ] **CA4:** Token gerado é um JWT válido com claims `user_id`, `email`, `exp`
- [ ] **CA5:** `GET /users/me` sem token retorna `401`
- [ ] **CA6:** `GET /users/me` com token válido retorna os dados do usuário autenticado
- [ ] **CA7:** `POST /auth/logout` invalida o token — chamadas subsequentes com ele retornam `401`
- [ ] **CA8:** Senhas são armazenadas como hash bcrypt (nunca em texto puro)

---

## 5. Impacto

### Arquivos que serão modificados

| Arquivo | Tipo de mudança |
|---------|-----------------|
| `models/user.py` | adição do campo `password_hash: str` |
| `routes/auth.py` | criação (novo arquivo) |
| `middleware/auth.py` | criação (novo arquivo) |
| `services/auth_service.py` | criação (novo arquivo) |
| `routes/users.py` | adição do middleware nas rotas protegidas |
| `migrations/0003_add_password_hash.py` | nova migration |

### Contratos externos afetados

| Contrato | Mudança |
|----------|---------|
| `GET /users/me` | passa a exigir `Authorization: Bearer <token>` |
| `GET /projects/` | passa a exigir `Authorization: Bearer <token>` |

---

## 6. Restrições

- **Segurança:** não diferenciar "email não existe" de "senha errada" na resposta (previne enumeração de usuários)
- **Hash:** usar bcrypt com `rounds=12` — não usar MD5, SHA1 ou SHA256 direto
- **JWT:** usar `HS256`, chave via variável de ambiente `JWT_SECRET` (mínimo 32 caracteres)
- **Expiração:** 1 hora (`exp = now + 3600`)
- **Denylist de tokens:** armazenar no Redis, TTL igual ao `exp` do token

---

## 7. Como Testar

```bash
# Rodar os testes de autenticação
pytest tests/test_auth.py -v

# Smoke test manual
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "senha123"}'

# Usar o token retornado
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer <token_do_login>"
```
