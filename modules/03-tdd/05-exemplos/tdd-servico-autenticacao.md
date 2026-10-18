# Exemplo TDD — Serviço de Autenticação (Python / pytest)

> **Conectado ao spec:** `modules/02-spec-driven-development/05-exemplos/spec-feature-autenticacao.md`
>
> Este exemplo mostra o ciclo completo Red → Green → Refactor para o serviço de autenticação
> especificado no Módulo 2. Leia o spec antes de continuar.

---

## Fase Red — Testes que Falham

Os critérios de aceite do spec mapeados para casos de teste:

| CA do spec | Caso de teste |
|-----------|---------------|
| POST /auth/login retorna token JWT com credenciais corretas | `test_login_returns_jwt_token_on_valid_credentials` |
| POST /auth/login retorna 401 com senha incorreta | `test_login_returns_401_on_wrong_password` |
| POST /auth/login retorna 401 com e-mail inexistente | `test_login_returns_same_error_for_nonexistent_email` |
| Token contém `user_id`, `email`, `exp` | `test_token_payload_contains_required_fields` |
| Token expira em 24 horas | `test_token_expires_after_24_hours` |
| POST /auth/logout invalida o token na blocklist | `test_logout_adds_token_to_blocklist` |
| Endpoint protegido rejeita token da blocklist | `test_blocked_token_is_rejected_on_protected_endpoint` |

```python
# tests/test_auth_service.py
"""
Fase Red — testes escritos ANTES da implementação.
Spec: modules/02-spec-driven-development/05-exemplos/spec-feature-autenticacao.md
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from jose import jwt

from app.services.auth import AuthService
from app.exceptions import InvalidCredentialsError


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def mock_user_repo():
    repo = MagicMock()
    repo.find_by_email.return_value = {
        "id": "user-123",
        "email": "comprador@email.com",
        "hashed_password": "$2b$12$hashed_password_here",
    }
    return repo


@pytest.fixture
def mock_blocklist():
    return MagicMock()


@pytest.fixture
def auth_service(mock_user_repo, mock_blocklist):
    return AuthService(
        user_repo=mock_user_repo,
        blocklist=mock_blocklist,
        secret_key="test-secret-key",
        algorithm="HS256",
    )


# ─────────────────────────────────────────────
# TESTES DE LOGIN
# ─────────────────────────────────────────────

class TestLogin:

    def test_login_returns_jwt_token_on_valid_credentials(
        self, auth_service, mock_user_repo
    ):
        """
        CA: POST /auth/login com credenciais corretas retorna token JWT.
        """
        # Arrange
        mock_user_repo.find_by_email.return_value = {
            "id": "user-123",
            "email": "comprador@email.com",
            "hashed_password": "$2b$12$real_bcrypt_hash",
        }

        # Act
        resultado = auth_service.login("comprador@email.com", "senha_correta")

        # Assert
        assert resultado["access_token"] is not None
        assert resultado["token_type"] == "bearer"

        payload = jwt.decode(
            resultado["access_token"],
            "test-secret-key",
            algorithms=["HS256"]
        )
        assert payload["user_id"] == "user-123"
        assert payload["email"] == "comprador@email.com"


    def test_token_expires_after_24_hours(self, auth_service, mock_user_repo):
        """
        CA: Token expira em 24 horas.
        """
        # Arrange
        mock_user_repo.find_by_email.return_value = {
            "id": "user-123",
            "email": "comprador@email.com",
            "hashed_password": "$2b$12$real_bcrypt_hash",
        }

        # Act
        resultado = auth_service.login("comprador@email.com", "senha_correta")

        # Assert
        payload = jwt.decode(
            resultado["access_token"],
            "test-secret-key",
            algorithms=["HS256"]
        )
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        agora = datetime.now(timezone.utc)
        diferenca = exp - agora

        assert timedelta(hours=23, minutes=55) < diferenca <= timedelta(hours=24)


    def test_login_returns_401_on_wrong_password(self, auth_service):
        """
        CA: POST /auth/login com senha incorreta retorna 401.
        """
        # Act + Assert
        with pytest.raises(InvalidCredentialsError):
            auth_service.login("comprador@email.com", "senha_errada")


    def test_nonexistent_email_returns_same_error_as_wrong_password(
        self, auth_service, mock_user_repo
    ):
        """
        Caso de borda (decisão de segurança do spec):
        E-mail inexistente e senha errada devem retornar o mesmo erro.
        Isso impede enumeração de usuários.
        """
        # Arrange
        mock_user_repo.find_by_email.return_value = None  # usuário não existe

        # Act + Assert
        with pytest.raises(InvalidCredentialsError) as exc_info_inexistente:
            auth_service.login("nao_existe@email.com", "qualquer_senha")

        # Verifica que a mensagem é idêntica à de senha errada
        with pytest.raises(InvalidCredentialsError) as exc_info_senha_errada:
            auth_service.login("comprador@email.com", "senha_errada")

        assert str(exc_info_inexistente.value) == str(exc_info_senha_errada.value)


# ─────────────────────────────────────────────
# TESTES DE LOGOUT
# ─────────────────────────────────────────────

class TestLogout:

    def test_logout_adds_token_to_blocklist(self, auth_service, mock_blocklist):
        """
        CA: POST /auth/logout invalida o token na blocklist.
        """
        # Arrange
        token_valido = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"

        # Act
        auth_service.logout(token_valido)

        # Assert
        mock_blocklist.add.assert_called_once_with(token_valido)


    def test_blocked_token_is_rejected(self, auth_service, mock_blocklist):
        """
        CA: Token na blocklist é rejeitado em endpoints protegidos.
        """
        # Arrange
        token_bloqueado = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.bloqueado"
        mock_blocklist.contains.return_value = True

        # Act + Assert
        with pytest.raises(InvalidCredentialsError):
            auth_service.verify_token(token_bloqueado)
```

---

## Fase Green — Implementação Mínima

Prompt usado (ver `04-ia-no-fluxo/` → Prompt 2):

```
Os testes acima estão falhando. Implemente AuthService com os métodos login, logout
e verify_token. Implemente apenas o suficiente para os testes passarem.
Não modifique os testes.
```

Resultado esperado: `pytest tests/test_auth_service.py` → 7 passed, 0 failed.

---

## Fase Refactor — Melhorias Aplicadas

Após Green, a IA identificou e aplicou com aprovação:
- Extração de `_verify_password` como método privado (repetido em `login` e `verify_token`)
- `_build_token_payload` como método privado (clareza na geração do JWT)
- Constante `TOKEN_EXPIRY_HOURS = 24` em vez de número literal

Os 7 testes continuaram passando após o refactor.

---

## O que este exemplo demonstra

1. O ciclo Red → Green → Refactor com testes reais (não hipotéticos)
2. Como o caso de borda de segurança do spec (erro idêntico para e-mail inexistente vs senha errada) vira um teste próprio
3. Como mockar dependências externas (repositório, blocklist) para isolar o serviço
4. Como verificar comportamento de tempo (expiração do JWT) sem depender do relógio real
