# Exemplo: Análise de Issue — Feature de Autenticação JWT

> Esta é a issue que originou o sistema JWT dos Módulos 2, 3 e 4.
> O spec gerado no final alimenta `modules/02-spec-driven-development/05-exemplos/spec-feature-autenticacao.md`.

---

## Issue original (bruta)

```
[FEAT] Sistema de autenticação para a API

Precisamos de autenticação na API. Os usuários devem conseguir fazer login
e logout. Tokens JWT parecem uma boa solução.

Prioridade: Alta
```

---

## Resultado do Prompt 1 — Análise inicial

```
**Tipo:** Feature — nova capacidade que o sistema não tem.

**Escopo aparente:**
- Dentro: endpoints de login e logout com JWT
- Fora: não está claro se inclui registro de usuário, recuperação de senha, MFA

**Ambiguidades identificadas:**
1. Expiração do token não definida — quanto tempo um token é válido?
2. Mecanismo de invalidação ausente — como revogar tokens antes da expiração?
3. Usuários pré-existentes ou registro também está no escopo?
4. Mensagem de erro não especificada — mesma mensagem para usuário inexistente e senha errada?
5. Endpoints protegidos não listados — quais rotas exigem autenticação?

**Perguntas de clarificação:**
1. Quanto tempo um token JWT deve ser válido após emissão?
2. O logout deve invalidar o token imediatamente (blocklist) ou apenas no cliente?
3. O registro de novos usuários está no escopo desta issue?
4. Para 401, deve retornar mensagem genérica (evita user enumeration) ou específica?
5. Quais endpoints existentes precisarão de autenticação?

**Analisabilidade:** NÃO com as informações atuais — faltam respostas para 1 e 2 no mínimo.
```

**Respostas assumidas:**
1. Token válido por 24 horas
2. Logout invalida via blocklist no Redis (segurança > simplicidade)
3. Registro fora do escopo — usuários pré-existentes no banco
4. Mensagem genérica para 401 (evita user enumeration)
5. Endpoints protegidos definidos na próxima sprint

---

## Resultado do Prompt 2 — Decomposição

```
**TASK-1:** Implementar endpoint POST /auth/login
- Escopo: validação de credenciais, geração de JWT com exp 24h, resposta 200/401
- Dependências: nenhuma

**TASK-2:** Implementar blocklist de tokens no Redis
- Escopo: armazenar JTI (JWT ID) com TTL calculado, verificar se token está revogado
- Dependências: nenhuma (pode ser desenvolvida em paralelo com TASK-1)

**TASK-3:** Implementar endpoint POST /auth/logout
- Escopo: receber token válido, adicionar à blocklist (TASK-2), retornar 200
- Dependências: TASK-2

**TASK-4:** Implementar middleware de autenticação
- Escopo: verificar token JWT em headers, rejeitar tokens expirados ou na blocklist
- Dependências: TASK-1 (formato do token), TASK-2 (blocklist)
```

---

## Resultado do Prompt 3 — Critérios de aceite

```
**TASK-1 — POST /auth/login:**
- CA-1: dado e-mail e senha válidos, quando POST /auth/login, então retorna 200 com token JWT no corpo
- CA-2: dado e-mail inexistente, quando POST /auth/login, então retorna 401 com mensagem "Credenciais inválidas"
- CA-3: dado senha incorreta, quando POST /auth/login, então retorna 401 com a mesma mensagem genérica do CA-2
- CA-4: dado token gerado, quando decodificado, então campo exp = hora_emissão + 86400 segundos

**TASK-2 — Blocklist Redis:**
- CA-5: dado JTI de token válido, quando adicionado à blocklist, então redis.exists(jti) retorna True
- CA-6: dado JTI na blocklist, então TTL da entrada é ≤ tempo de expiração original do token

**TASK-3 — POST /auth/logout:**
- CA-7: dado token válido no header Authorization, quando POST /auth/logout, então retorna 200 e JTI adicionado à blocklist
- CA-8: dado token inválido ou ausente, quando POST /auth/logout, então retorna 401

**TASK-4 — Middleware:**
- CA-9: dado token válido e não revogado, quando requisição a endpoint protegido, então requisição prossegue normalmente
- CA-10: dado token na blocklist, quando requisição a endpoint protegido, então retorna 401 com mensagem "Token revogado"
```

---

## Resultado do Prompt 6 — Spec stub gerado

```markdown
# Spec — Autenticação JWT com Login e Logout

**Tipo:** feature
**Arquivo:** docs/specs/001-autenticacao-jwt.md

## Contexto
A API não tem autenticação. Esta feature implementa JWT com endpoints de login
e logout e blocklist de tokens revogados no Redis.

## Escopo — dentro
- POST /auth/login: validação de credenciais e emissão de JWT (24h)
- POST /auth/logout: invalidação de token via blocklist no Redis
- Middleware de autenticação para endpoints protegidos

## Escopo — fora
- Registro de novos usuários
- Recuperação de senha
- MFA (multi-factor authentication)

## Critérios de aceite
- CA-1: POST /auth/login retorna 200 e token JWT com credenciais válidas
- CA-2: POST /auth/login retorna 401 com mensagem genérica para e-mail inexistente
- CA-3: POST /auth/login retorna 401 com mesma mensagem genérica para senha incorreta
- CA-4: Token JWT tem expiração de 24h (campo exp no payload)
- CA-5 a CA-6: Blocklist Redis com TTL correto
- CA-7: POST /auth/logout invalida token na blocklist
- CA-8: POST /auth/logout rejeita token inválido com 401
- CA-9: Middleware aceita token válido não revogado
- CA-10: Middleware rejeita token revogado com 401

## Campos em aberto (para o Módulo 2)
- NFRs de performance: latência máxima do login?
- Quais endpoints específicos serão protegidos pelo middleware?
- Estratégia de rotação de chave JWT
```

> O spec completo, revisado e validado, está em:
> [`modules/02-spec-driven-development/05-exemplos/spec-feature-autenticacao.md`](../../02-spec-driven-development/05-exemplos/spec-feature-autenticacao.md)