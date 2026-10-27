# Exemplo — Gate de Complexidade Ciclomática

## Contexto

O `verify_token` do sistema JWT acumulou responsabilidades ao longo do tempo:
verifica assinatura, valida expiração, verifica a blocklist, resolve o usuário no banco.
O resultado é uma função com complexidade D (score 14) — acima do threshold C (≤ 10).

---

## Estado Inicial

```bash
$ radon cc app/services/auth.py -s --min C

app/services/auth.py
    F 45:0 verify_token - D (14)

$ radon cc app/services/auth.py -s -a
app/services/auth.py
    F 12:0 create_access_token - A (3)
    F 45:0 verify_token - D (14)   ← GATE FALHA AQUI
    F 78:0 authenticate_user - B (6)

    Average complexity: B (7.67)
```

**Gate:** `radon cc app/ -s --min C` → retorna saída não-vazia → exit code 1 → build falha.

---

## Código Vulnerável

```python
# app/services/auth.py — ANTES

def verify_token(token: str, db: Session) -> User:
    """Verifica o token e retorna o usuário autenticado."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    if not isinstance(user_id, int):
        raise HTTPException(status_code=401, detail="Invalid token payload")

    if blocklist.is_blocked(token):
        raise HTTPException(status_code=401, detail="Token revoked")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive")

    return user
# Complexidade: 14 (7 condicionais + try/except + 2 branches do except)
```

---

## Prompt Usado

```
verify_token tem complexidade ciclomática D (score 14). O gate exige máximo C (score ≤ 10).

Código atual:

[código acima]

Refatore para:
1. Reduzir a complexidade total para abaixo de 10 (grade B ou A)
2. Extrair responsabilidades em funções auxiliares com nomes descritivos
3. Manter a mesma interface pública: recebe (token: str, db: Session), retorna User
4. Não alterar os códigos e mensagens de HTTPException (testes existentes verificam isso)
5. Não quebrar nenhum teste existente
6. Atualizar os testes para cobrir as novas funções auxiliares se necessário
```

---

## DEPOIS — Código Refatorado

```python
# app/services/auth.py — DEPOIS

def _decode_token(token: str) -> dict:
    """Decodifica e valida a assinatura do JWT."""
    # Complexidade: 3
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def _extract_user_id(payload: dict) -> int:
    """Extrai e valida o user_id do payload."""
    # Complexidade: 3
    user_id = payload.get("user_id")
    if user_id is None or not isinstance(user_id, int):
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return user_id


def _resolve_active_user(user_id: int, db: Session) -> User:
    """Busca o usuário e verifica se está ativo."""
    # Complexidade: 3
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive")
    return user


def verify_token(token: str, db: Session) -> User:
    """Verifica o token e retorna o usuário autenticado."""
    # Complexidade: 3 (apenas coordenação)
    if blocklist.is_blocked(token):
        raise HTTPException(status_code=401, detail="Token revoked")
    payload = _decode_token(token)
    user_id = _extract_user_id(payload)
    return _resolve_active_user(user_id, db)
```

---

## Resultado após a refatoração

```bash
$ radon cc app/services/auth.py -s --min C
# Saída vazia → nenhuma função acima de C → gate passa

$ radon cc app/services/auth.py -s -a
app/services/auth.py
    F 12:0 create_access_token - A (3)
    F 45:0 _decode_token - A (3)
    F 58:0 _extract_user_id - A (3)
    F 68:0 _resolve_active_user - A (3)
    F 80:0 verify_token - A (3)
    F 95:0 authenticate_user - B (6)

    Average complexity: A (3.5)    ← de B (7.67) para A (3.5)
```

**verify_token: D (14) → A (3)**  
**Gate: FALHOU → PASSOU ✅**

---

## O Que Mudou

| Antes | Depois |
|-------|--------|
| `verify_token` faz tudo (decode + extract + blocklist + resolve) | 4 funções com responsabilidade única |
| Complexidade D (14) | Complexidade A (3) em cada função |
| Difícil testar casos individuais | Cada função auxiliar testável em isolamento |
| Gate falhou | Gate passou ✅ |

**Bonus:** as funções auxiliares `_decode_token`, `_extract_user_id` e `_resolve_active_user` agora podem ser testadas independentemente — o número total de casos de teste não aumentou, mas cada teste ficou mais específico e legível.