# Exemplo — A01: Broken Access Control

## Contexto

O sistema JWT tem um endpoint `GET /user/profile` que retorna o perfil de um usuário.
O bug: qualquer usuário autenticado pode acessar o perfil de qualquer outro usuário
trocando o `user_id` no parâmetro.

---

## ANTES — Código Vulnerável

```python
# app/routers/users.py

@router.get("/user/profile")
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at
    }
```

**Por que é vulnerável:**

1. O endpoint não exige token — qualquer cliente HTTP pode acessá-lo
2. Mesmo que exigisse token, não verifica se o `user_id` solicitado pertence ao usuário autenticado
3. Um atacante pode enumerar todos os perfis fazendo `GET /user/profile?user_id=1`, `?user_id=2`, etc. (IDOR — Insecure Direct Object Reference)

**Vetor de ataque:**
```bash
# Atacante acessa perfil de qualquer usuário sem autenticação
curl "https://api.example.com/user/profile?user_id=42"
# Retorna email, nome e data de criação de qualquer usuário
```

---

## Prompt Usado

```
Encontrei este achado OWASP A01 no arquivo app/routers/users.py:

```python
@router.get("/user/profile")
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email, "name": user.name}
```

Vetor: endpoint sem autenticação + sem verificação de propriedade (IDOR).

Gere a correção que:
1. Exige token JWT válido para acessar o endpoint
2. Permite que o usuário acesse apenas o próprio perfil
3. Permite acesso a qualquer perfil se o usuário tiver role "admin"
4. Retorna 401 se sem token, 403 se token válido mas user_id não pertence ao usuário
5. Mantém o mesmo formato de resposta
6. Inclui dois testes: acesso ao próprio perfil (200) e acesso ao perfil alheio (403)
```

---

## DEPOIS — Código Corrigido

```python
# app/routers/users.py

@router.get("/user/profile")
async def get_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),  # 401 se sem token
    db: Session = Depends(get_db)
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at
    }
```

```python
# tests/test_users.py

def test_get_own_profile_returns_200(client, auth_headers, test_user):
    response = client.get(
        f"/user/profile?user_id={test_user.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email

def test_get_other_profile_returns_403(client, auth_headers, other_user):
    response = client.get(
        f"/user/profile?user_id={other_user.id}",
        headers=auth_headers
    )
    assert response.status_code == 403

def test_get_profile_without_token_returns_401(client, test_user):
    response = client.get(f"/user/profile?user_id={test_user.id}")
    assert response.status_code == 401

def test_admin_can_get_any_profile(client, admin_headers, test_user):
    response = client.get(
        f"/user/profile?user_id={test_user.id}",
        headers=admin_headers
    )
    assert response.status_code == 200
```

---

## O Que Mudou

| Antes | Depois |
|-------|--------|
| Sem autenticação | `Depends(get_current_user)` → 401 se sem token |
| Sem verificação de propriedade | `current_user.id != user_id` → 403 se não é o dono |
| Sem exceção para admin | `current_user.role != "admin"` → admin acessa qualquer perfil |
| Sem testes de acesso | 4 testes cobrindo os vetores principais |

**Severidade original:** ALTO  
**Após correção:** SEM ACHADOS