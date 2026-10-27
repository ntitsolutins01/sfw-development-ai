# Exemplo — Gate de Cobertura

## Contexto

O sistema JWT tem um serviço de blocklist de tokens (`token_blocklist.py`). Quando
o usuário faz logout, o token é adicionado à blocklist. Endpoints protegidos verificam
a blocklist antes de aceitar o token.

O gate de coverage está configurado em 80%. O serviço existe mas não tem testes —
a cobertura total cai para 71% e o gate falha.

---

## Estado inicial

```bash
$ pytest --cov=app --cov-fail-under=80 --cov-report=term-missing

Name                              Stmts  Miss  Cover   Missing
--------------------------------------------------------------
app/services/auth.py                 45     4    91%   88, 92, 103, 107
app/services/token_blocklist.py      28    16    43%   12-18, 22-28, 31-38
app/routers/auth.py                  32     8    75%   45-52, 67-69
app/core/security.py                 22     0   100%
--------------------------------------------------------------
TOTAL                               127    28    78%   ← abaixo do threshold

FAIL Required test coverage of 80% not reached. Total coverage: 78%
```

**Arquivos mais críticos:**
- `token_blocklist.py` — 43% (lógica de negócio central sem um único teste)
- `routers/auth.py` — 75% (caminho de logout e erro 401 não testados)

---

## Prompt Usado

```
O gate de coverage falhou: 78% com threshold de 80%.
O arquivo mais crítico é token_blocklist.py (43%).

Aqui está o código atual:

```python
# app/services/token_blocklist.py

from datetime import datetime, timedelta
from typing import Optional
import threading

class TokenBlocklist:
    def __init__(self):
        self._blocklist: dict[str, datetime] = {}
        self._lock = threading.Lock()

    def add(self, token: str, expires_at: datetime) -> None:
        with self._lock:
            self._blocklist[token] = expires_at
            self._cleanup_expired()

    def is_blocked(self, token: str) -> bool:
        with self._lock:
            if token not in self._blocklist:
                return False
            if datetime.utcnow() > self._blocklist[token]:
                del self._blocklist[token]
                return False
            return True

    def _cleanup_expired(self) -> None:
        now = datetime.utcnow()
        expired = [t for t, exp in self._blocklist.items() if now > exp]
        for t in expired:
            del self._blocklist[t]
```

Gere testes para token_blocklist.py que:
1. Cubram os 4 casos: add, is_blocked (presente/expirado/ausente), cleanup
2. Usem pytest com fixtures
3. Não precisem de banco de dados ou infraestrutura externa
4. Cubram pelo menos 90% das linhas do arquivo
```

---

## DEPOIS — Testes Gerados

```python
# tests/test_token_blocklist.py

import pytest
from datetime import datetime, timedelta
from app.services.token_blocklist import TokenBlocklist


@pytest.fixture
def blocklist():
    return TokenBlocklist()


@pytest.fixture
def valid_token():
    return "eyJhbGciOiJIUzI1NiJ9.valid.token"


@pytest.fixture
def future_expiry():
    return datetime.utcnow() + timedelta(hours=1)


@pytest.fixture
def past_expiry():
    return datetime.utcnow() - timedelta(seconds=1)


def test_new_blocklist_is_empty(blocklist, valid_token):
    assert not blocklist.is_blocked(valid_token)


def test_add_token_marks_it_as_blocked(blocklist, valid_token, future_expiry):
    blocklist.add(valid_token, future_expiry)
    assert blocklist.is_blocked(valid_token)


def test_expired_token_is_not_blocked(blocklist, valid_token, past_expiry):
    blocklist.add(valid_token, past_expiry)
    # token expirou — is_blocked deve retornar False e remover da lista
    assert not blocklist.is_blocked(valid_token)


def test_unknown_token_is_not_blocked(blocklist):
    assert not blocklist.is_blocked("token-inexistente")


def test_cleanup_removes_expired_tokens(blocklist, future_expiry, past_expiry):
    blocklist.add("token-valido", future_expiry)
    blocklist.add("token-expirado", past_expiry)

    # Trigger cleanup via add
    blocklist.add("outro-token", future_expiry)

    # Token expirado deve ser removido
    assert not blocklist.is_blocked("token-expirado")
    # Token válido deve permanecer
    assert blocklist.is_blocked("token-valido")


def test_multiple_tokens_managed_independently(blocklist, future_expiry):
    blocklist.add("token-a", future_expiry)
    blocklist.add("token-b", future_expiry)

    assert blocklist.is_blocked("token-a")
    assert blocklist.is_blocked("token-b")
    assert not blocklist.is_blocked("token-c")
```

---

## Resultado após os testes

```bash
$ pytest --cov=app --cov-fail-under=80 --cov-report=term-missing

Name                              Stmts  Miss  Cover   Missing
--------------------------------------------------------------
app/services/auth.py                 45     4    91%   88, 92, 103, 107
app/services/token_blocklist.py      28     1    96%   38
app/routers/auth.py                  32     8    75%   45-52, 67-69
app/core/security.py                 22     0   100%
--------------------------------------------------------------
TOTAL                               127    13    90%   ← passou o threshold

Required test coverage of 80% reached. Total coverage: 90%  ✅
```

**Coverage total: 78% → 90% (+12%)**  
**`token_blocklist.py`: 43% → 96%**  
**Gate: FALHOU → PASSOU ✅**

---

## O Que Mudou

| Antes | Depois |
|-------|--------|
| `token_blocklist.py` sem testes | 6 testes cobrindo todos os caminhos |
| Coverage total: 78% | Coverage total: 90% |
| Gate falhou (exit code 2) | Gate passou (exit code 0) |
| Lógica de expiração não verificada | Caso de expiração explicitamente testado |