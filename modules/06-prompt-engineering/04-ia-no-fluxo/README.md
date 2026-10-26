# IA no Fluxo — 6 Técnicas com Exemplos do Ciclo AIAD

Cada técnica abaixo tem: quando usar, prompt de referência aplicado ao projeto JWT e o anti-padrão a evitar.

> **Como usar:** copie o prompt, substitua os `[colchetes]` e envie no Claude Code.

---

## Técnica 1 — Zero-shot com CIFER

**Quando usar:** tarefas bem definidas, código padrão, sem estilo específico do projeto.

```
## Contexto
Python 3.11 / FastAPI. Arquivo: app/dependencies.py.
Já existe: função get_db() que retorna Session do SQLAlchemy.

## Instrução
Escreva a dependency get_current_user(token: str = Depends(oauth2_scheme)) -> User
que decodifica o JWT, busca o usuário no banco e levanta HTTPException 401 se
o token for inválido, expirado ou estiver na blocklist.

## Formato
Função em app/dependencies.py. Type hints completos. Sem arquivos novos.

## Restrições
Não crie endpoint. Não modifique get_db(). Não adicione logging.
```

**Anti-padrão a evitar:**
```
# ❌ Sem contexto, sem localização
escreva uma dependency de autenticação para fastapi
```

---

## Técnica 2 — Few-shot para testes no estilo do projeto

**Quando usar:** gerar testes novos que precisam seguir o estilo e convenções dos testes existentes.

```
Aqui estão dois testes existentes do projeto (siga exatamente este estilo):

# tests/test_auth.py
def test_login_retorna_token_com_credenciais_validas(client, usuario_fixture):
    response = client.post("/auth/login", json={
        "email": usuario_fixture.email,
        "password": "senha_correta"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_retorna_401_com_senha_errada(client, usuario_fixture):
    response = client.post("/auth/login", json={
        "email": usuario_fixture.email,
        "password": "senha_errada"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"

---

Agora escreva os testes para POST /auth/logout. Critérios de aceite:
- CA-7: token válido → 200 e JTI adicionado à blocklist
- CA-8: token inválido ou ausente → 401
- CA-9: token já revogado → 401
```

**Anti-padrão a evitar:**
```
# ❌ Sem exemplos — o modelo vai inventar um estilo próprio
escreva testes para o endpoint de logout
```

---

## Técnica 3 — Chain-of-Thought para debugging

**Quando usar:** bug sem causa óbvia, comportamento intermitente, erro em múltiplos níveis.

```
O endpoint POST /auth/login retorna 200 com um token, mas ao usar o token
em um endpoint protegido, recebo 401 "Token inválido" imediatamente.
O token foi emitido há menos de 1 segundo.

Antes de sugerir a correção, analise passo a passo:
1. Quais são as causas possíveis para um token recém-emitido ser rejeitado?
2. Qual delas é mais provável considerando o código abaixo?
3. Como você confirmaria a causa raiz sem debugger?

Código do middleware de autenticação:
[cole o código de verify_token e do middleware]
```

**Anti-padrão a evitar:**
```
# ❌ Pedir a solução antes do diagnóstico
meu token está dando 401, como corrijo?
```

---

## Técnica 4 — Role Prompting para revisão

**Quando usar:** revisões de código, análises de segurança, decisões arquiteturais onde o viés importa.

```
Aja como um engenheiro sênior especializado em segurança de APIs,
revisando o código de autenticação JWT abaixo para produção.

Seu foco é:
1. Vulnerabilidades na geração e validação do token
2. Exposição de informações sensíveis em mensagens de erro
3. Timing attacks na comparação de credenciais
4. Problemas com a implementação da blocklist no Redis

Para cada problema encontrado, informe:
- Severidade: CRÍTICO / ALTO / MÉDIO / BAIXO
- Descrição técnica do risco
- Correção sugerida

Código a revisar:
[cole app/services/auth.py]
```

**Anti-padrão a evitar:**
```
# ❌ Papel vago, sem foco
você é um expert. revise este código.
```

---

## Técnica 5 — Structured Output para análise

**Quando usar:** a saída vai ser processada por outro passo do fluxo — integrar com spec, criar issue, comparar alternativas.

```
Analise o diff abaixo e retorne um JSON com este formato exato:

{
  "decisao": "APROVADO" | "APROVADO_COM_RESSALVAS" | "SOLICITAR_MUDANCAS",
  "achados": [
    {
      "severidade": "CRITICO" | "ALTO" | "MEDIO" | "BAIXO",
      "arquivo": "caminho/arquivo.py",
      "linha": 42,
      "descricao": "descrição técnica do problema",
      "sugestao": "como corrigir"
    }
  ],
  "cas_cobertas": ["CA-1", "CA-3"],
  "cas_ausentes": ["CA-2", "CA-4"]
}

Spec de referência: [cole os CAs do spec]

Diff do PR:
[cole o output de git diff main...HEAD]
```

**Anti-padrão a evitar:**
```
# ❌ Sem formato definido — difícil de processar depois
analise este diff e diga se está ok
```

---

## Técnica 6 — Constrained Prompting para mudanças cirúrgicas

**Quando usar:** correções pontuais, hotfix, qualquer situação onde você precisa de controle total sobre o escopo.

```
Corrija apenas o problema descrito abaixo. Não faça nenhuma outra mudança.

Problema: o campo `exp` no token JWT está sendo calculado como
`datetime.now() + timedelta(hours=24)` usando horário local.
Deve ser `datetime.utcnow() + timedelta(hours=24)`.

Arquivo: app/services/auth.py, linha 23.

Não altere:
- nenhuma outra linha do arquivo
- outros arquivos
- testes
- imports (datetime já está importado)
```

**Anti-padrão a evitar:**
```
# ❌ Sem restrições — o modelo vai "melhorar" o código ao redor
corrija o cálculo do exp no token
```

---

## Combinando técnicas

Para tarefas complexas, combine técnicas:

```
# Few-shot + Constrained + Structured Output
# Cenário: extrair CAs de uma nova issue no mesmo formato das issues anteriores

Aqui estão dois exemplos de análise que já fizemos (padrão a seguir):

EXEMPLO 1 — Issue: "login falha com email maiúsculo"
→ CA-1: dado email "JOAO@EXAMPLE.COM", quando POST /auth/login, então retorna 200
→ CA-2: dado email com espaços " joao@example.com ", quando login, então normaliza e retorna 200

EXEMPLO 2 — Issue: "logout não invalida token"
→ CA-1: dado token válido, quando POST /auth/logout, então redis.exists(jti) retorna True
→ CA-2: dado token inválido, quando POST /auth/logout, então retorna 401

---

Agora analise esta issue e extraia os CAs no mesmo formato:

Issue: "Refresh token não está sendo renovado após 23h"

Restrições:
- Extraia apenas CAs verificáveis (sim/não sem interpretação)
- Não invente comportamento não descrito na issue
- Máximo 5 CAs
```