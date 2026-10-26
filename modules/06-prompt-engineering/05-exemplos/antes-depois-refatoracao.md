# Exemplo: Antes e Depois — Refatoração

> Problema: AuthService mistura lógica de negócio com queries de banco. Objetivo: separar usando Repository Pattern.

---

## ❌ Prompt antes (anti-padrão)

```
refatore o AuthService para ficar mais limpo e testável
```

**Resposta típica:**

```python
# Resposta: o modelo "melhora" o código de várias formas não solicitadas:
# - renomeia métodos (login → authenticate)
# - adiciona logging
# - muda a assinatura das funções
# - cria novos arquivos sem perguntar
# - "melhora" o tratamento de erro
# - os testes existentes quebram porque as assinaturas mudaram
```

**Problemas com esta resposta:**
- "Mais limpo e testável" é subjetivo — o modelo interpreta como quiser
- Nenhuma restrição sobre o que não pode mudar
- Os testes existentes provavelmente vão quebrar
- Você não pediu Repository Pattern — o modelo pode usar um padrão diferente

**Resultado:** refatoração que quebra os testes e exige revisão manual de cada mudança.

---

## ✅ Prompt depois (Constrained prompting + critério de não-regressão)

```
## Contexto
Arquivo: app/services/auth.py
Problema: AuthService tem 180 linhas misturando lógica de negócio (validar credenciais,
gerar token) com queries diretas ao banco (self.db.query(User)...).
Arquitetura alvo: Repository Pattern — UserRepository isola todas as queries.

## Código atual
class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, email: str, password: str) -> str:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return create_token(str(user.id))

    def logout(self, token: str) -> None:
        payload = verify_token(token)
        jti = payload["jti"]
        exp = payload["exp"]
        ttl = exp - int(datetime.utcnow().timestamp())
        redis.setex(f"blocklist:{jti}", ttl, "1")

## Instrução
Refatore AuthService para receber UserRepository via construtor (DI)
em vez de Session. UserRepository deve ter interface AbstractUserRepository.

## Formato
Dois arquivos:
- app/repositories/user_repository.py — AbstractUserRepository + UserRepository
- app/services/auth.py — AuthService refatorado

## Critério de não-regressão
Os testes abaixo devem passar sem modificação após a refatoração:

def test_login_com_credenciais_validas(auth_service, usuario_fixture):
    token = auth_service.login("joao@example.com", "senha123")
    assert token is not None

def test_login_credenciais_invalidas(auth_service):
    with pytest.raises(InvalidCredentialsError):
        auth_service.login("nao@existe.com", "qualquer")

## Restrições
- A interface pública de AuthService (login, logout) não deve mudar
- Os testes acima devem passar sem nenhuma modificação
- Não adicione features novas (logging, métricas, cache)
- Não altere o esquema do banco de dados
- Não crie mais arquivos além dos dois listados acima
```

**Resposta típica:**

```python
# app/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from app.models import User

class AbstractUserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        ...

class UserRepository(AbstractUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def find_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

# app/services/auth.py
class AuthService:
    def __init__(self, user_repo: AbstractUserRepository):
        self.user_repo = user_repo

    def login(self, email: str, password: str) -> str:
        user = self.user_repo.find_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return create_token(str(user.id))

    def logout(self, token: str) -> None:
        # logout não usa banco — sem mudança
        payload = verify_token(token)
        jti = payload["jti"]
        exp = payload["exp"]
        ttl = exp - int(datetime.utcnow().timestamp())
        redis.setex(f"blocklist:{jti}", ttl, "1")
```

**Por que funcionou:**
- A instrução foi específica: Repository Pattern, dois arquivos exatos
- O critério de não-regressão forçou o modelo a preservar a interface pública
- As restrições impediram adições não solicitadas
- Os testes continuam funcionando porque `AuthService.login` e `AuthService.logout` têm a mesma assinatura

**Resultado:** refatoração limpa, escopo controlado, testes verdes sem modificação.

---

## A regra de ouro da refatoração

> Um prompt de refatoração sem critério de não-regressão é um convite para o modelo reescrever o código como quiser.

Sempre inclua:
1. **A arquitetura alvo** (Repository Pattern, não "mais limpo")
2. **Os testes que não podem quebrar** (ou a interface que não pode mudar)
3. **O que está fora do escopo** (logging, features novas, etc.)

Com esses três elementos, o modelo entrega a refatoração exata que você pediu.