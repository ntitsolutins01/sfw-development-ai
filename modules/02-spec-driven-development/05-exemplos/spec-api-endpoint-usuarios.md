# Spec — API Endpoint: GET /users/{id}

> **Exemplo didático** — spec de API endpoint preenchido completo.
> Use como referência para aprender a preencher o template `03-templates/api-endpoint.md`.

**Data:** 2026-10-18
**Autor:** equipe backend
**Ticket/Issue:** #203
**Autenticação necessária?** [x] Sim
**Status:** [x] Aprovado

---

## 1. Contexto

**Propósito do endpoint:**
Retornar os dados públicos de um usuário pelo seu ID. Usado pelo frontend para exibir o perfil de outros usuários e por serviços internos para enriquecer dados de colaboração.

**Quem vai consumir:**
- [x] Frontend web (perfil de usuário)
- [ ] App mobile
- [x] Serviço interno (serviço de notificações)
- [ ] Cliente externo

---

## 2. Contrato

### Request

```
MÉTODO: GET
URL:    /users/{id}
```

**Headers obrigatórios:**

| Header | Valor esperado |
|--------|----------------|
| `Authorization` | `Bearer <token>` |

**Path params:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `id` | UUID | Sim | ID do usuário a consultar |

**Body:** não se aplica (GET)

---

### Response — Sucesso

**Status:** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "João Silva",
  "email": "joao@example.com",
  "avatar_url": "https://cdn.example.com/avatars/joao.png",
  "created_at": "2026-01-15T10:30:00Z"
}
```

> **Nota:** o campo `password_hash` e outros campos internos NUNCA aparecem na resposta, mesmo que o solicitante seja admin.

---

### Response — Erros

| Status | Quando ocorre | Body |
|--------|--------------|------|
| `401 Unauthorized` | token ausente ou inválido | `{ "error": "unauthorized" }` |
| `404 Not Found` | usuário com o ID não existe | `{ "error": "not_found", "resource": "user" }` |
| `422 Unprocessable Entity` | `{id}` não é um UUID válido | `{ "error": "validation_error", "details": [{ "field": "id", "message": "must be a valid UUID" }] }` |

> **Decisão de segurança:** não retornar `403` para usuários que existem mas não têm permissão de acesso — retornar `404` para não vazar que o ID existe.

---

## 3. Regras de Negócio

- Qualquer usuário autenticado pode consultar qualquer outro usuário (perfil público)
- O campo `email` é retornado apenas se o solicitante é o próprio usuário ou tem role `admin`
- Usuários com `status = "deleted"` retornam `404` (como se não existissem)
- O campo `avatar_url` pode ser `null` se o usuário não configurou avatar

---

## 4. Critérios de Aceite

- [ ] **CA1:** `GET /users/{id_valido}` com token válido retorna `200` + objeto do usuário
- [ ] **CA2:** campos `password_hash`, `reset_token` e outros campos internos nunca aparecem na resposta
- [ ] **CA3:** campo `email` aparece na resposta quando solicitante é o próprio usuário
- [ ] **CA4:** campo `email` **não** aparece quando solicitante é outro usuário sem role `admin`
- [ ] **CA5:** `GET /users/{id_inexistente}` retorna `404`
- [ ] **CA6:** `GET /users/{id_de_usuario_deletado}` retorna `404`
- [ ] **CA7:** `GET /users/nao-e-um-uuid` retorna `422` com detalhe do campo inválido
- [ ] **CA8:** `GET /users/{id}` sem token retorna `401`

---

## 5. Impacto

**Arquivos a criar/modificar:**

| Arquivo | Mudança |
|---------|---------|
| `routes/users.py` | adicionar o endpoint `GET /{id}` |
| `schemas/user.py` | criar schema `UserPublicResponse` (sem campos internos) e `UserPrivateResponse` (com email) |
| `services/user_service.py` | adicionar método `get_by_id(id, requester_id)` |
| `tests/test_users.py` | adicionar testes para os 8 critérios de aceite |

**Banco de dados:** sem mudança (apenas leitura)

---

## 6. Segurança

- [x] Valida que `{id}` é UUID antes de consultar o banco (evita SQL injection por tipo)
- [x] Não expõe `password_hash` em nenhuma resposta
- [x] Usuários deletados retornam `404` (não `403`) para não vazar existência
- [x] Logs não contêm `password_hash` ou tokens

---

## 7. Como Testar

```bash
# Obter token primeiro
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "senha123"}' | jq -r .token)

# Consultar usuário existente
curl http://localhost:8000/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $TOKEN"

# Consultar usuário inexistente (deve retornar 404)
curl http://localhost:8000/users/00000000-0000-0000-0000-000000000000 \
  -H "Authorization: Bearer $TOKEN"

# Testar validação de UUID (deve retornar 422)
curl http://localhost:8000/users/nao-e-um-uuid \
  -H "Authorization: Bearer $TOKEN"

# Rodar todos os testes do módulo
pytest tests/test_users.py -v
```
