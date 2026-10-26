# Template — Debug

Use para investigar bugs, comportamentos inesperados e erros com causa não óbvia.

---

## Template

```
## Contexto
Arquivo/função com o problema: [ex: app/services/auth.py → função verify_token]
O que deveria acontecer: [comportamento esperado]
O que está acontecendo: [comportamento atual + erro ou output observado]
Quando foi introduzido: [se souber — "após o commit X" ou "sempre existiu"]

## Stack trace ou output (se disponível)
[cole aqui o erro completo — não resuma]

## Código relevante
[cole apenas o código diretamente relacionado ao bug — não o arquivo inteiro]

## Instrução
Antes de sugerir a correção, analise passo a passo:
1. Qual é o fluxo esperado?
2. Em que ponto o fluxo desvia do esperado?
3. Qual é a causa raiz (não o sintoma)?
Depois do raciocínio, mostre a correção mínima.

## Restrições
- Corrija apenas o bug descrito
- Não refatore o código ao redor
- Não adicione logging ou tratamento de erro além do necessário para a correção
- A interface pública da função não deve mudar
```

---

## Exemplo preenchido — token não sendo invalidado

```
## Contexto
Arquivo/função com o problema: app/services/auth.py → função logout(token: str)
O que deveria acontecer: JTI do token é adicionado à blocklist do Redis com TTL = tempo restante até exp
O que está acontecendo: a função retorna 200 e não levanta exceção, mas redis.exists(jti) retorna 0

## Stack trace ou output
Nenhum erro. O endpoint retorna HTTP 200. Redis inspecionado com redis-cli:
  127.0.0.1:6379> KEYS blocklist:*
  (empty array)

## Código relevante
def logout(token: str, redis_client: Redis) -> None:
    payload = verify_token(token)
    jti = payload.get("jti")
    exp = payload.get("exp")
    ttl = exp - int(datetime.utcnow().timestamp())
    redis_client.setex(f"blocklist:{jti}", ttl, "1")

## Instrução
Antes de sugerir a correção, analise passo a passo:
1. O que verify_token retorna quando o token é válido?
2. Em que ponto o setex poderia falhar silenciosamente?
3. O ttl pode ser negativo ou zero? O que acontece com setex nesses casos?
Depois do raciocínio, mostre a correção mínima.

## Restrições
- Corrija apenas o problema do Redis
- Não altere a assinatura de logout nem de verify_token
- Não adicione logging
```

---

## Variações por tipo de bug

**Bug com erro explícito (cole o traceback):**
```
## Contexto
Arquivo: app/services/auth.py
Erro ao chamar create_token(""):
  ValueError: user_id não pode ser vazio  ← esperado
  AttributeError: 'NoneType' object has no attribute 'encode'  ← inesperado

[cole o traceback completo]

Corrija o AttributeError. A validação do user_id vazio já existe e não deve mudar.
```

**Bug de performance (sem erro, mas lento):**
```
## Contexto
O endpoint POST /auth/login está retornando em média 850ms (esperado: < 200ms).
Perfil de tempo (adicione prints de timestamp):
  - validação de email: 2ms
  - query no banco: 15ms
  - bcrypt.checkpw: 820ms ← suspeito

Antes de sugerir a correção, analise por que bcrypt.checkpw leva 820ms
e se isso é esperado ou configurável.
```

**Bug intermitente (não reproduzível sempre):**
```
## Contexto
POST /auth/logout falha com KeyError: 'jti' em ~15% das requisições.
O token foi emitido pelo nosso create_token — por que o campo jti estaria ausente?

Analise passo a passo:
1. Há alguma condição em create_token onde jti não seria adicionado ao payload?
2. O campo jti pode ser removido por alguma transformação entre a emissão e o logout?
```