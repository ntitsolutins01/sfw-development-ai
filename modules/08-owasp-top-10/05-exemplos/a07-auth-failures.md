# Exemplo — A07: Identification and Authentication Failures

## Contexto

O endpoint `POST /auth/login` não tem rate limiting. Um atacante pode tentar
milhares de combinações de senha por minuto sem nenhuma restrição, e as tentativas
falhas não são logadas — tornando o ataque completamente invisível.

---

## ANTES — Código Vulnerável

```python
# app/routers/auth.py

@router.post("/auth/login")
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
```

**Por que é vulnerável:**

1. **Sem rate limiting:** nenhum controle no número de tentativas por IP ou por email. Um atacante pode fazer 10.000 requisições por minuto.

2. **Sem logging de falhas:** tentativas com credenciais inválidas não geram nenhum log. É impossível detectar um ataque de brute force — o sistema fica cego.

3. **Combinação devastadora:** brute force invisível. O atacante testa um wordlist de senhas comuns contra emails reais (obtidos de data breaches) e descobre credenciais sem que nenhum alerta dispare.

**Simulação do ataque:**
```bash
# Ataque de credential stuffing com lista de senhas comuns
while read password; do
    curl -s -X POST https://api.example.com/auth/login \
        -d '{"email":"user@example.com","password":"'$password'"}'
done < common_passwords.txt
# Nenhuma resposta diferente de 401 até encontrar a senha correta
# Nenhum log, nenhum alerta, nenhum bloqueio
```

---

## Prompt Usado

```
Encontrei este achado OWASP A07 no arquivo app/routers/auth.py:

```python
@router.post("/auth/login")
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
```

Vetores:
1. Sem rate limiting — permite brute force ilimitado
2. Sem log de tentativas falhas — ataque invisível

Gere a correção que:
1. Adiciona rate limiting de 5 tentativas por minuto por IP (use slowapi)
2. Adiciona log estruturado para tentativas falhas: email, IP, timestamp, motivo
3. Adiciona log para login bem-sucedido: user_id, IP, timestamp
4. Mantém a interface existente (mesmo request/response)
5. Retorna 429 com mensagem clara quando rate limit é atingido
6. Inclui testes para: login válido (200), credenciais erradas (401), rate limit (429)
```

---

## DEPOIS — Código Corrigido

```python
# app/routers/auth.py

import logging
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)

@router.post("/auth/login")
@limiter.limit("5/minute")
async def login(
    request: Request,
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    client_ip = request.client.host
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        logger.warning(
            "failed_login_attempt",
            extra={
                "email": credentials.email,
                "ip": client_ip,
                "reason": "invalid_credentials" if user else "user_not_found"
            }
        )
        # Mesma mensagem independente do motivo — não revela se email existe
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(
        "successful_login",
        extra={"user_id": user.id, "ip": client_ip}
    )
    token = create_access_token({"sub": str(user.id), "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
```

```python
# app/main.py (registro do handler de rate limit)

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

```python
# tests/test_auth.py

def test_login_valid_credentials_returns_token(client, test_user):
    response = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "correct_password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password_returns_401(client, test_user):
    response = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "wrong_password"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_nonexistent_email_same_message(client):
    response = client.post("/auth/login", json={
        "email": "naoexiste@example.com",
        "password": "qualquer"
    })
    assert response.status_code == 401
    # Mesma mensagem — não revela que o email não existe
    assert response.json()["detail"] == "Invalid credentials"

def test_login_rate_limit_returns_429(client, test_user):
    # 5 tentativas válidas passam, a 6ª é bloqueada
    for _ in range(5):
        client.post("/auth/login", json={
            "email": test_user.email,
            "password": "wrong"
        })
    response = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "wrong"
    })
    assert response.status_code == 429

def test_failed_login_generates_warning_log(client, test_user, caplog):
    with caplog.at_level(logging.WARNING):
        client.post("/auth/login", json={
            "email": test_user.email,
            "password": "wrong"
        })
    assert "failed_login_attempt" in caplog.text
```

---

## O Que Mudou

| Antes | Depois |
|-------|--------|
| Sem rate limiting | `@limiter.limit("5/minute")` por IP → 429 na 6ª tentativa |
| Sem logging de falhas | `logger.warning("failed_login_attempt", email, ip, reason)` |
| Sem logging de sucesso | `logger.info("successful_login", user_id, ip)` |
| Erro diferente para email inexistente | Mesma mensagem independente do motivo (sem user enumeration) |
| Sem testes de segurança | 5 testes: happy path, 401, enumeration prevention, 429, log |

**Severidade original:** ALTO  
**Após correção:** SEM ACHADOS

## Nota sobre Configuração do Rate Limit

O limite de 5/minuto por IP é um ponto de partida. Dependendo do produto:
- **Muito restritivo** para usuários com IP compartilhado (NAT corporativo, VPN): considere limite por `(IP, email)` em vez de só por IP
- **Muito permissivo** para sistemas de alta segurança: considere 3/minuto com backoff exponencial
- **Produção:** armazene o contador no Redis em vez de memória do processo (o padrão da slowapi) para funcionar com múltiplos workers