# Exemplo: PR Review — Autenticação JWT

> Continuação dos Módulos 2 e 3. O spec está em `modules/02-spec-driven-development/05-exemplos/spec-feature-autenticacao.md`.
> Os testes foram escritos no Módulo 3 (`modules/03-tdd/05-exemplos/tdd-servico-autenticacao.md`).

---

## Contexto do PR

**Branch:** `feature/autenticacao-jwt`
**Título:** `feat: add JWT authentication with login and logout endpoints`
**Spec:** `docs/specs/001-autenticacao-jwt.md`

**Critérios de aceite do spec:**
- CA-1: `POST /auth/login` retorna 200 e token JWT com credenciais válidas
- CA-2: `POST /auth/login` retorna 401 com mensagem genérica para credenciais inválidas
- CA-3: Token JWT expira em 24h (campo `exp` no payload)
- CA-4: `POST /auth/logout` adiciona o token à blocklist no Redis
- CA-5: Endpoint protegido retorna 401 se token estiver na blocklist

---

## Fase 1 — Self-review (resultado)

O autor percorreu `checklist-feature.md` e encontrou:

| Item | Status | Observação |
|------|--------|-----------|
| Spec preenchido | ✅ | `docs/specs/001-autenticacao-jwt.md` |
| Todos os CAs implementados | ⚠️ | CA-4 estava incompleto — `logout` salvava no Redis mas não verificava TTL |
| Testes para todos os CAs | ✅ | 5 CAs × 2 testes cada = 10 testes |
| `pytest` passando 100% | ✅ | Após corrigir CA-4 |
| Nenhum dado sensível logado | ❌ encontrado | `auth.py:34` logava o token completo — corrigido antes do PR |

---

## Fase 2 — Resultado do `/code-review`

```
## Revisão de Código — feature/autenticacao-jwt — 2026-10-19

### Resumo
0 críticos, 1 alto, 2 médios, 1 baixo

### Achados

#### [ALTO] Senha comparada sem hash constante — auth_service.py:18
Problema: `if user.password == input_password` compara diretamente.
Comparação direta vaza timing de execução — permite ataques de timing para
inferir se e-mail existe mesmo sem a senha.
Sugestão: Use `bcrypt.checkpw(input_password.encode(), user.password_hash)`
com comparação em tempo constante.

#### [MÉDIO] Token JWT não valida audience — auth_service.py:42
Problema: `jwt.decode` não verifica o campo `aud` do token.
Sugestão: Adicione `audience="api.seudominio.com"` ao decode para evitar
tokens emitidos por outro serviço serem aceitos.

#### [MÉDIO] Blocklist sem TTL — redis_client.py:15
Problema: Tokens na blocklist ficam para sempre no Redis — cresce indefinidamente.
Sugestão: Defina o TTL da entrada no Redis igual ao tempo de expiração do token:
`redis.setex(token_jti, token_ttl_seconds, "revoked")`

#### [BAIXO] Mensagem de erro muito detalhada em desenvolvimento — auth_service.py:67
Problema: Stack trace completo retornado na resposta quando DEBUG=True.
Sugestão: Sempre retornar mensagem genérica na API; log interno pode ter detalhes.
```

**Ação do autor:**
- Corrigiu [ALTO]: trocou comparação direta por `bcrypt.checkpw`
- Corrigiu [MÉDIO] blocklist: adicionou TTL calculado a partir da expiração do token
- Aceitou [MÉDIO] audience como dívida técnica documentada no spec
- Corrigiu [BAIXO]: removeu debug mode da resposta da API

---

## Fase 3 — Resultado do `/review-pr docs/specs/001-autenticacao-jwt.md`

```
## Revisão com Spec — feature/autenticacao-jwt

### Critérios de Aceite
- [x] CA-1: POST /auth/login retorna 200 e token JWT com credenciais válidas
      → auth_service.py:12-28, test_login_success
- [x] CA-2: POST /auth/login retorna 401 com mensagem genérica
      → auth_service.py:30-35, test_login_invalid_credentials
- [x] CA-3: Token expira em 24h
      → auth_service.py:44 (exp = now + 86400), test_token_expiry
- [x] CA-4: POST /auth/logout invalida token na blocklist
      → redis_client.py:15-22, test_logout_adds_to_blocklist
- [x] CA-5: Endpoint protegido rejeita token da blocklist
      → middleware.py:38-45, test_protected_endpoint_rejects_blocklisted_token

### Cobertura de Testes
- [x] test_login_success — cobre CA-1 (caso feliz)
- [x] test_login_wrong_password — cobre CA-2 (caso de falha)
- [x] test_login_nonexistent_email — cobre CA-2 (mesmo erro para email inexistente)
- [x] test_token_expiry — cobre CA-3
- [x] test_logout_adds_to_blocklist — cobre CA-4
- [x] test_logout_invalid_token — cobre CA-4 (token inválido no logout)
- [x] test_protected_endpoint_rejects_blocklisted_token — cobre CA-5
- [x] test_protected_endpoint_accepts_valid_token — cobre CA-5 (caso feliz)

### Decisão
APROVADO — todos os 5 CAs implementados e cobertos por testes.
```

---

## Sumário executivo (Prompt 6)

```
## PR Review — feature/autenticacao-jwt

### O que foi implementado
Sistema completo de autenticação JWT com endpoints POST /auth/login e
POST /auth/logout. Tokens expiram em 24h e tokens revogados são
armazenados em blocklist no Redis com TTL calculado automaticamente.

### O que foi encontrado e corrigido
- Comparação de senha sem hash constante → corrigido para bcrypt.checkpw
- Blocklist sem TTL → corrigido com setex baseado na expiração do token
- Token completo sendo logado → removido do log em self-review
- Mensagem de erro detalhada em modo debug → removida da resposta da API

### Pendências abertas
- Validação de audience no JWT: documentada como dívida técnica no spec
  (impacto: baixo para ambiente single-service atual)

### Decisão final
APROVADO — todos os CAs do spec estão implementados, cobertos por testes
e o código não tem achados CRÍTICO ou ALTO após as correções.
```