# Exemplo — A02: Cryptographic Failures

## Contexto

O sistema JWT tem dois problemas criptográficos clássicos:
1. Segredo JWT hardcoded com valor trivial (`"secret"`)
2. Decode do token aceita o algoritmo `"none"` — permite tokens sem assinatura

---

## ANTES — Código Vulnerável

```python
# app/core/security.py

JWT_SECRET = "secret"  # hardcoded, 6 caracteres, trivialmente quebrável
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        # BUG: aceita "none" como algoritmo — tokens sem assinatura passam
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256", "none"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Por que é vulnerável:**

**Problema 1 — Segredo fraco:**
`"secret"` está em qualquer wordlist de senha. Um atacante que capturou um token JWT
pode quebrar o segredo offline com `hashcat` ou `jwt-cracker` em segundos e forjar
tokens válidos para qualquer `user_id`.

**Problema 2 — Algoritmo `none`:**
O JWT RFC permite um algoritmo especial `none` que indica "sem assinatura". Algumas
implementações aceitam isso. Se aceito, um atacante pode criar um token com qualquer
payload e simplesmente omitir a assinatura — o servidor aceita como válido.

**Vetor de ataque para o algoritmo `none`:**
```python
# Atacante cria token sem assinatura
header = base64url_encode({"alg": "none", "typ": "JWT"})
payload = base64url_encode({"sub": "1", "user_id": 999, "exp": 9999999999})
forged_token = f"{header}.{payload}."  # assinatura vazia

# Servidor aceita porque "none" está na lista de algoritmos permitidos
```

---

## Prompt Usado

```
Encontrei dois achados OWASP A02 no arquivo app/core/security.py:

1. JWT_SECRET = "secret" — hardcoded e trivialmente quebrável
2. algorithms=["HS256", "none"] — aceita tokens sem assinatura

Gere a correção que:
1. Lê JWT_SECRET de variável de ambiente obrigatória
2. Valida na inicialização que o segredo tem >= 32 caracteres
3. Remove "none" da lista de algoritmos aceitos — apenas "HS256"
4. Mantém a interface pública das funções (create_access_token e verify_token)
5. Levanta erro descritivo na inicialização se JWT_SECRET ausente ou fraco
6. Inclui teste que confirma rejeição de token com algoritmo "none"
```

---

## DEPOIS — Código Corrigido

```python
# app/core/security.py

import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException

_JWT_SECRET = os.environ.get("JWT_SECRET")
if not _JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable is required")
if len(_JWT_SECRET) < 32:
    raise RuntimeError("JWT_SECRET must be at least 32 characters")

_ALGORITHM = "HS256"  # único algoritmo aceito — nunca "none"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, _JWT_SECRET, algorithm=_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

```python
# tests/test_security.py

import pytest
import base64
import json

def test_verify_token_rejects_none_algorithm(client):
    # Constrói token com algoritmo "none" manualmente
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "none", "typ": "JWT"}).encode()
    ).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(
        json.dumps({"sub": "1", "user_id": 1}).encode()
    ).rstrip(b"=").decode()
    forged_token = f"{header}.{payload}."

    response = client.get(
        "/user/profile?user_id=1",
        headers={"Authorization": f"Bearer {forged_token}"}
    )
    assert response.status_code == 401

def test_startup_fails_without_jwt_secret(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    with pytest.raises(RuntimeError, match="JWT_SECRET environment variable is required"):
        import importlib
        import app.core.security
        importlib.reload(app.core.security)

def test_startup_fails_with_weak_jwt_secret(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "fraco")
    with pytest.raises(RuntimeError, match="at least 32 characters"):
        import importlib
        import app.core.security
        importlib.reload(app.core.security)
```

---

## O Que Mudou

| Antes | Depois |
|-------|--------|
| `JWT_SECRET = "secret"` hardcoded | Lido de `os.environ["JWT_SECRET"]` |
| Sem validação do segredo | Erro na inicialização se ausente ou < 32 chars |
| `algorithms=["HS256", "none"]` | `algorithms=["HS256"]` — algoritmo único e explícito |
| Sem testes para vetores criptográficos | 3 testes: none algorithm, secret ausente, secret fraco |

**Severidade original:** CRÍTICO  
**Após correção:** SEM ACHADOS

## Nota sobre Rotação de Segredo

A correção acima torna o segredo obrigatório e forte, mas não resolve rotação de segredo em produção. Para isso, é necessário suporte a múltiplos segredos durante o período de transição (tokens gerados com o segredo antigo ainda precisam ser aceitos até expirarem). Isso é um achado A04 (Insecure Design) documentado separadamente.