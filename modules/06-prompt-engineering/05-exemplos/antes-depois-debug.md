# Exemplo: Antes e Depois — Debug

> Problema: POST /auth/login retorna 200, mas o token gerado é rejeitado imediatamente pelo middleware.

---

## ❌ Prompt antes (anti-padrão)

```
meu token está dando 401 logo depois de fazer login, como corrijo?
```

**Resposta típica:**

```
Possíveis causas:
1. Token expirado
2. Chave secreta diferente entre geração e validação
3. Algoritmo diferente
4. Clock skew

Verifique se o JWT_SECRET_KEY é o mesmo nas duas funções.
```

**Problemas com esta resposta:**
- Lista genérica que você poderia ter buscado no Google
- Não analisa o código real — não sabe qual é a causa específica
- Não prioriza as causas (qual é mais provável?)
- Não sugere como confirmar o diagnóstico

**Resultado:** você vai checar as 4 opções manualmente até achar o problema.

---

## ✅ Prompt depois (Chain-of-Thought + contexto)

```
O endpoint POST /auth/login retorna 200 com um token. Ao usar o token
no header Authorization: Bearer <token> em qualquer endpoint protegido,
recebo 401 "Token inválido" imediatamente — o token foi gerado há menos
de 1 segundo.

Antes de sugerir a correção, analise passo a passo:
1. Quais são as causas possíveis para um token recém-emitido ser rejeitado?
2. Qual delas é mais provável dado o código abaixo?
3. Como confirmar a causa raiz sem debugger (ex: print do payload decodificado)?

# app/services/auth.py
def create_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now() + timedelta(hours=24),
        "jti": str(uuid4())
    }
    return jwt.encode(payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            os.environ["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
```

**Resposta típica:**

```
Raciocínio passo a passo:

1. Causas possíveis para um token recém-emitido ser rejeitado:
   - Chave secreta diferente entre emissão e validação
   - Algoritmo diferente
   - Clock skew (relógio do servidor desalinhado)
   - exp calculado no passado (uso de datetime.now() em vez de datetime.utcnow())

2. Causa mais provável dado o código:
   datetime.now() em create_token usa o horário local do servidor, mas jwt.decode
   do python-jose valida exp em UTC. Se o servidor estiver em um fuso horário
   atrás de UTC (ex: UTC-3, Brasília), o campo exp está sendo calculado 3 horas
   no passado em relação ao UTC — o token já nasce expirado.

3. Como confirmar sem debugger:
   Adicione temporariamente:
     from datetime import timezone
     print(f"exp calculado: {datetime.now()}")
     print(f"utcnow: {datetime.utcnow()}")
   Se diferirem, é exatamente este o problema.

Correção:
Substitua datetime.now() por datetime.utcnow() em create_token:
  "exp": datetime.utcnow() + timedelta(hours=24)
```

**Por que funcionou:**
- O CoT forçou o modelo a priorizar as causas com base no código real
- A instrução "analise passo a passo antes de sugerir a correção" evitou um diagnóstico superficial
- O código foi incluído no prompt — o modelo analisou o problema específico, não o genérico
- Resultado: diagnóstico correto na primeira tentativa, com como confirmar antes de corrigir

---

## Lição

O anti-padrão de debug mais comum é perguntar pela solução sem fornecer o problema concreto. O modelo não tem acesso ao seu código — ele vai gerar uma lista genérica de possibilidades.

Chain-of-thought força o modelo a:
1. Analisar o código específico que você forneceu
2. Priorizar causas com base no contexto real
3. Sugerir como confirmar antes de corrigir

Isso reduz o ciclo de debug de "várias tentativas" para "diagnóstico + correção em uma rodada".