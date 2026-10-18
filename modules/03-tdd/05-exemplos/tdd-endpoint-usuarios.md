# Exemplo TDD — Endpoint GET /users/{id} (Python / pytest)

> **Conectado ao spec:** `modules/02-spec-driven-development/05-exemplos/spec-api-endpoint-usuarios.md`
>
> O spec define um endpoint GET /users/{id} com visibilidade condicional do e-mail,
> tratamento especial para usuários deletados e autenticação obrigatória.
>
> Este exemplo cobre testes de integração para o endpoint usando FastAPI + TestClient.

---

## Fase Red — Testes que Falham

Critérios de aceite do spec mapeados para casos de teste:

| CA do spec | Caso de teste |
|-----------|---------------|
| Retorna dados do usuário com token válido | `test_returns_user_data_with_valid_token` |
| Retorna 401 sem token | `test_returns_401_without_token` |
| Retorna 401 com token inválido | `test_returns_401_with_invalid_token` |
| Retorna 404 para usuário deletado (não 403) | `test_deleted_user_returns_404_not_403` |
| Email visível apenas para próprio usuário | `test_email_visible_only_to_own_user` |
| Email oculto para outros usuários | `test_email_hidden_for_other_users` |
| Admin vê email de qualquer usuário | `test_admin_sees_email_of_any_user` |
| Retorna 404 para ID inexistente | `test_nonexistent_id_returns_404` |

```python
# tests/integration/test_users_endpoint.py
"""
Fase Red — testes de integração para GET /users/{id}.
Spec: modules/02-spec-driven-development/05-exemplos/spec-api-endpoint-usuarios.md

Dependências: fastapi, httpx, pytest-asyncio
Comando: pytest tests/integration/test_users_endpoint.py -v
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.models import User


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def usuario_comum():
    return User(
        id="user-456",
        name="Ana Costa",
        email="ana@email.com",
        role="user",
        is_deleted=False,
    )


@pytest.fixture
def usuario_deletado():
    return User(
        id="user-789",
        name="Carlos Lima",
        email="carlos@email.com",
        role="user",
        is_deleted=True,
    )


@pytest.fixture
def token_proprio():
    """Token do próprio usuário (user-456)."""
    return "Bearer token_do_usuario_456"


@pytest.fixture
def token_outro_usuario():
    """Token de outro usuário (user-999), não admin."""
    return "Bearer token_do_usuario_999"


@pytest.fixture
def token_admin():
    """Token de usuário com role=admin."""
    return "Bearer token_admin"


# ─────────────────────────────────────────────
# TESTES DE AUTENTICAÇÃO
# ─────────────────────────────────────────────

class TestAutenticacao:

    def test_returns_401_without_token(self, client):
        """
        CA: Requisição sem Authorization header retorna 401.
        """
        # Act
        resposta = client.get("/users/user-456")

        # Assert
        assert resposta.status_code == 401


    def test_returns_401_with_invalid_token(self, client):
        """
        CA: Token inválido ou expirado retorna 401.
        """
        # Act
        resposta = client.get(
            "/users/user-456",
            headers={"Authorization": "Bearer token_invalido_aqui"}
        )

        # Assert
        assert resposta.status_code == 401


# ─────────────────────────────────────────────
# TESTES DE DADOS RETORNADOS
# ─────────────────────────────────────────────

class TestDadosRetornados:

    def test_returns_user_data_with_valid_token(
        self, client, usuario_comum, token_proprio
    ):
        """
        CA: Com token válido, retorna os campos: id, name, email, role, created_at.
        """
        # Arrange
        with patch("app.repositories.UserRepository.find_by_id",
                   return_value=usuario_comum):

            # Act
            resposta = client.get(
                "/users/user-456",
                headers={"Authorization": token_proprio}
            )

        # Assert
        assert resposta.status_code == 200
        dados = resposta.json()
        assert dados["id"] == "user-456"
        assert dados["name"] == "Ana Costa"
        assert "created_at" in dados


    def test_email_visible_only_to_own_user(
        self, client, usuario_comum, token_proprio
    ):
        """
        CA: Campo email é visível quando o requisitante é o próprio usuário.
        Regra de negócio do spec: email é dado sensível.
        """
        # Arrange
        with patch("app.repositories.UserRepository.find_by_id",
                   return_value=usuario_comum):

            # Act
            resposta = client.get(
                "/users/user-456",
                headers={"Authorization": token_proprio}
            )

        # Assert
        assert resposta.status_code == 200
        assert resposta.json()["email"] == "ana@email.com"


    def test_email_hidden_for_other_users(
        self, client, usuario_comum, token_outro_usuario
    ):
        """
        CA: Campo email é omitido quando o requisitante é outro usuário (não admin).
        """
        # Arrange
        with patch("app.repositories.UserRepository.find_by_id",
                   return_value=usuario_comum):

            # Act
            resposta = client.get(
                "/users/user-456",
                headers={"Authorization": token_outro_usuario}
            )

        # Assert
        assert resposta.status_code == 200
        assert "email" not in resposta.json()


    def test_admin_sees_email_of_any_user(
        self, client, usuario_comum, token_admin
    ):
        """
        CA: Administrador vê o email de qualquer usuário.
        """
        # Arrange
        with patch("app.repositories.UserRepository.find_by_id",
                   return_value=usuario_comum):

            # Act
            resposta = client.get(
                "/users/user-456",
                headers={"Authorization": token_admin}
            )

        # Assert
        assert resposta.status_code == 200
        assert resposta.json()["email"] == "ana@email.com"


# ─────────────────────────────────────────────
# TESTES DE CASOS DE BORDA
# ─────────────────────────────────────────────

class TestCasosDeBorda:

    def test_deleted_user_returns_404_not_403(
        self, client, usuario_deletado, token_admin
    ):
        """
        Decisão de segurança do spec (seção 4.3):
        Usuário deletado retorna 404 e não 403 — não revela que o usuário
        existiu mas foi removido. Admin não é exceção a essa regra.
        """
        # Arrange
        with patch("app.repositories.UserRepository.find_by_id",
                   return_value=usuario_deletado):

            # Act
            resposta = client.get(
                "/users/user-789",
                headers={"Authorization": token_admin}
            )

        # Assert
        assert resposta.status_code == 404
        # Garante que não retornou 403 (que revelaria a existência)
        assert resposta.status_code != 403


    def test_nonexistent_id_returns_404(self, client, token_proprio):
        """
        CA: ID inexistente retorna 404.
        """
        # Arrange
        with patch("app.repositories.UserRepository.find_by_id",
                   return_value=None):

            # Act
            resposta = client.get(
                "/users/id-que-nao-existe",
                headers={"Authorization": token_proprio}
            )

        # Assert
        assert resposta.status_code == 404
```

---

## Fase Green — Implementação Mínima

Prompt usado:

```
Os testes acima estão falhando. Implemente o endpoint GET /users/{id} em FastAPI.
Regras de visibilidade do email:
- Visível para o próprio usuário
- Visível para admin (role="admin")
- Oculto para outros usuários (campo ausente na resposta)
Usuário is_deleted=True deve retornar 404 (não 403).
Implemente o mínimo para os testes passarem.
```

---

## Fase Refactor — Melhorias Aplicadas

Após Green:
- `_can_see_email(requester, target)` extraído como função auxiliar
- `_get_user_or_404` extraído para reutilizar entre endpoints futuros
- Schema `UserResponse` e `UserPublicResponse` separados (com e sem email)

Todos os 8 testes continuaram passando.

---

## O que este exemplo demonstra

1. Testes de integração com `TestClient` do FastAPI — sem servidor real
2. Como testar regra de visibilidade condicional de campo (email visível/oculto por papel)
3. Como garantir que uma decisão de segurança do spec (404 vs 403 para usuário deletado) tem teste próprio
4. Como usar `patch` para isolar o repositório sem banco de dados no teste de integração
