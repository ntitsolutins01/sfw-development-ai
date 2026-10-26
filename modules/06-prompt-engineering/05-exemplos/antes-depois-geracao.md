# Exemplo: Antes e Depois — Geração de Código

> Problema: implementar a função `verify_token` que valida um JWT e retorna o payload.

---

## ❌ Prompt antes (anti-padrão)

```
implemente verify_token para validar jwt
```

**Resposta típica:**

```python
import jwt

def verify_token(token):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")
```

**Problemas com esta resposta:**
- Chave hardcoded como `"secret"` — vulnerabilidade crítica de segurança
- `Exception` genérica em vez de HTTPException com status code correto
- Sem verificação de blocklist
- Sem type hints
- Biblioteca `jwt` (PyJWT) quando o projeto usa `python-jose`
- Função não sabe onde será usada (não retorna o tipo certo)

**Resultado:** 3–4 rodadas de correção para chegar no código utilizável.

---

## ✅ Prompt depois (framework CIFER)

```
## Contexto
Python 3.11 / FastAPI 0.110. Arquivo: app/services/auth.py.
Importações já existentes no arquivo:
  from jose import JWTError, jwt
  from fastapi import HTTPException, status
  import os, redis

A chave de assinatura está em os.environ["JWT_SECRET_KEY"].
O Redis está em redis.Redis(host="localhost", port=6379) disponível como `redis_client`.
Tokens são assinados com HS256.

## Instrução
Implemente verify_token(token: str, redis_client: Redis) -> dict
que valida o JWT e retorna o payload.

## Formato
Função em app/services/auth.py. Type hints completos. Sem novos arquivos.

## Exemplos
O payload de um token válido tem esta estrutura:
  {"sub": "user-uuid", "exp": 1700000000, "jti": "uuid4-string"}

## Restrições
- Levante HTTPException(status_code=401, detail="Token inválido") para qualquer problema
- Verifique se o JTI está na blocklist do Redis antes de retornar o payload
- Não crie outros arquivos
- Não adicione logging
- Use python-jose (já importado), não PyJWT
```

**Resposta típica:**

```python
def verify_token(token: str, redis_client: Redis) -> dict:
    """Valida JWT e retorna payload. Levanta 401 se inválido ou revogado."""
    try:
        payload = jwt.decode(
            token,
            os.environ["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    jti = payload.get("jti")
    if jti and redis_client.exists(f"blocklist:{jti}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revogado"
        )

    return payload
```

**Por que funcionou:**
- Usa a biblioteca correta (python-jose) porque foi especificada
- HTTPException com status code correto porque o contexto FastAPI foi informado
- Verifica blocklist porque foi incluído na instrução
- Type hints porque foi pedido no formato
- Sem código extra porque as restrições foram explícitas

**Resultado:** código pronto para uso na primeira tentativa.

---

## O que mudou entre os dois prompts

| Componente | Antes | Depois |
|-----------|-------|--------|
| Contexto | ausente | framework + arquivo + importações existentes |
| Instrução | vaga ("implementar") | específica (nome da função, parâmetros, retorno) |
| Formato | ausente | tipo de retorno, localização |
| Exemplos | ausente | estrutura do payload |
| Restrições | ausente | biblioteca, não criar arquivos, comportamento de erro |