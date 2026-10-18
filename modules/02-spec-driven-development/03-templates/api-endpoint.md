> **[TEMPLATE] Como usar este arquivo**
>
> Copie para `docs/specs/YYYY-MM-DD-api-<slug>.md` e preencha todas as seções.
> A seção "Contrato" é a mais importante: defina request, response e erros antes de qualquer implementação.

---

# Spec — API Endpoint: [MÉTODO /caminho/do/endpoint]

**Data:** YYYY-MM-DD
**Autor:** [nome]
**Ticket/Issue:** [link ou N/A]
**Autenticação necessária?** [ ] Sim  [ ] Não
**Status:** [ ] Rascunho  [ ] Em revisão  [ ] Aprovado  [ ] Implementado

---

## 1. Contexto

**Propósito do endpoint:**
[O que este endpoint faz e para qual caso de uso ele existe.]

**Quem vai consumir:**
[ ] Frontend web  [ ] App mobile  [ ] Serviço interno  [ ] Cliente externo  [ ] Outro: ____

---

## 2. Contrato

### Request

```
MÉTODO: [GET | POST | PUT | PATCH | DELETE]
URL:    /[caminho]/{param_obrigatorio}
```

**Headers obrigatórios:**

| Header | Valor esperado |
|--------|----------------|
| `Content-Type` | `application/json` |
| `Authorization` | `Bearer <token>` (se autenticado) |

**Path params:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `{id}` | UUID | Sim | ID do recurso |

**Query params:**

| Param | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `page` | int | 1 | Página de paginação |
| `limit` | int | 20 | Itens por página (máx: 100) |

**Body (se aplicável):**

```json
{
  "campo_obrigatorio": "string",
  "campo_opcional": "string | null"
}
```

---

### Response — Sucesso

**Status:** `200 OK` (ou `201 Created` para criação)

```json
{
  "id": "uuid",
  "campo": "valor",
  "created_at": "2026-10-18T00:00:00Z"
}
```

---

### Response — Erros

| Status | Quando ocorre | Body |
|--------|--------------|------|
| `400 Bad Request` | request inválido | `{ "error": "validation_error", "details": [...] }` |
| `401 Unauthorized` | token ausente ou inválido | `{ "error": "unauthorized" }` |
| `403 Forbidden` | sem permissão para o recurso | `{ "error": "forbidden" }` |
| `404 Not Found` | recurso não existe | `{ "error": "not_found" }` |
| `409 Conflict` | conflito de estado | `{ "error": "conflict", "message": "..." }` |
| `422 Unprocessable Entity` | dados válidos mas regra de negócio falhou | `{ "error": "unprocessable", "message": "..." }` |
| `500 Internal Server Error` | erro inesperado | `{ "error": "internal_error" }` |

---

## 3. Regras de Negócio

- [regra 1 — ex: "um usuário só pode acessar seus próprios recursos"]
- [regra 2 — ex: "o campo X é imutável após criação"]
- [regra 3]

---

## 4. Critérios de Aceite

- [ ] **CA1:** request válido retorna `[status]` com body conforme contrato
- [ ] **CA2:** request sem autenticação retorna `401`
- [ ] **CA3:** [campo inválido] retorna `400` com mensagem de erro legível
- [ ] **CA4:** [regra de negócio] é aplicada e retorna `[status]` correspondente
- [ ] **CA5:** endpoint documentado no OpenAPI/Swagger

---

## 5. Impacto

**Arquivos a criar/modificar:**

| Arquivo | Mudança |
|---------|---------|
| `routes/[recurso].py` | novo endpoint |
| `services/[recurso].py` | lógica de negócio |
| `schemas/[recurso].py` | validação de request/response |
| `tests/test_[recurso].py` | testes do endpoint |

**Banco de dados:**
[ ] Sem mudança  [ ] Nova tabela  [ ] Nova coluna  [ ] Nova migration

---

## 6. Segurança

- [ ] Valida e sanitiza todos os inputs
- [ ] Não expõe dados de outros usuários
- [ ] Rate limiting aplicado
- [ ] Logs não contêm dados sensíveis (senha, token, PII)

---

## 7. Como Testar

```bash
# Smoke test com curl
curl -X [MÉTODO] http://localhost:8000/[caminho] \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"campo": "valor"}'

# Rodar testes automatizados
pytest tests/test_[recurso].py -v
```
