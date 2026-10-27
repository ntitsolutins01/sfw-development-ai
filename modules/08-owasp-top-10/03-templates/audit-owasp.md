# Template — Auditoria OWASP Top 10

Use este template quando não tiver a skill `/audit-owasp` instalada, ou quando quiser controle granular sobre cada categoria.

---

## Prompt de Auditoria Completa

```
Você é um especialista em segurança de aplicações web com expertise no OWASP Top 10 (2021).

Analise o código abaixo e produza um relatório de segurança estruturado.

**Código a auditar:**
[COLE O ARQUIVO AQUI]

**Contexto da aplicação:**
- Sistema de autenticação JWT (FastAPI + Python)
- Banco de dados: PostgreSQL via SQLAlchemy
- Endpoints: POST /auth/login, POST /auth/logout, GET /user/profile
- Ambiente alvo: produção

**Para cada categoria do OWASP Top 10 (A01–A10):**

1. Verifique se existe evidência de risco no código fornecido
2. Se sim:
   - Cite o trecho exato (linha ou bloco)
   - Descreva o vetor de ataque (como seria explorado)
   - Classifique a severidade: CRÍTICO / ALTO / MÉDIO / BAIXO / INFO
   - Forneça a correção específica (código corrigido, não apenas descrição)
3. Se não houver evidência: marque como "Sem achados neste código"

**Formato de saída por categoria:**

### A0X — Nome da Categoria
**Status:** ACHADO CRÍTICO | ACHADO ALTO | ACHADO MÉDIO | ACHADO BAIXO | SEM ACHADOS

**Evidência:**
```python
# linha(s) problemática(s)
```

**Vetor:**
[como seria explorado]

**Severidade:** CRÍTICO | ALTO | MÉDIO | BAIXO

**Correção:**
```python
# código corrigido
```

---

**Ao final, gere:**

## Sumário dos Achados

| Categoria | Severidade | Status |
|-----------|-----------|--------|
| A01 | ... | ... |
...

**Total:** X CRÍTICO, Y ALTO, Z MÉDIO, W BAIXO

**Prioridade imediata (CRÍTICO + ALTO):**
- [lista de ações]
```

---

## Prompt por Categoria (quando quiser auditar uma só)

### A01 — Broken Access Control

```
Analise o código abaixo verificando exclusivamente A01 — Broken Access Control.

Verifique:
- Endpoints que não verificam autenticação (token ausente ou não validado)
- Endpoints que verificam autenticação mas não verificam autorização (qualquer usuário autenticado acessa qualquer recurso)
- IDOR (Insecure Direct Object Reference): o código permite que user A acesse dados de user B via parâmetro `?user_id=B`?
- Verificações de permissão que podem ser bypassadas (ex: apenas no frontend, ou baseadas em parâmetro controlável pelo cliente)

[COLE O CÓDIGO]
```

### A02 — Cryptographic Failures

```
Analise o código abaixo verificando exclusivamente A02 — Cryptographic Failures.

Verifique:
- Segredos JWT hardcoded ou fracos (menos de 32 caracteres, palavras de dicionário)
- Algoritmo JWT `none` aceito (permite tokens não assinados)
- Algoritmos fracos: MD5, SHA1, DES para dados sensíveis
- Senhas armazenadas em texto plano ou com hash fraco (MD5, SHA1 sem salt)
- Dados sensíveis trafegando em logs, headers inseguros ou URLs
- Variáveis de ambiente com segredos lidos de forma insegura

[COLE O CÓDIGO]
```

### A03 — Injection

```
Analise o código abaixo verificando exclusivamente A03 — Injection.

Verifique:
- SQL injection: queries com concatenação de string ou f-string com input do usuário
- Queries parametrizadas ausentes (use de .format(), %, f"..." com dados externos)
- NoSQL injection: filtros MongoDB construídos com dados não sanitizados
- Command injection: subprocess, os.system, eval(), exec() com dados externos
- LDAP injection se aplicável

[COLE O CÓDIGO]
```

### A07 — Identification and Authentication Failures

```
Analise o código abaixo verificando exclusivamente A07 — Identification and Authentication Failures.

Verifique:
- Rate limiting ausente em endpoints de login (permite brute force)
- Tokens JWT sem expiração configurada (campo `exp` ausente)
- Tokens inválidos rejeitados com mensagem de erro diferente para "token expirado" vs "token inválido" (information leakage)
- Credenciais padrão ou de teste no código (admin/admin, test@test.com/password)
- Logout que não invalida o token (sem blocklist)
- Senhas com requisitos de complexidade ausentes

[COLE O CÓDIGO]
```

### A09 — Security Logging and Monitoring Failures

```
Analise o código abaixo verificando exclusivamente A09 — Security Logging and Monitoring Failures.

Verifique:
- Tentativas de login falhas sem log (ou log sem IP, email, timestamp)
- Erros de autenticação silenciados (bare except, pass em exceções de segurança)
- Logs com dados sensíveis (senha em texto, token completo)
- Ausência de log para: login bem-sucedido, logout, acesso a recursos protegidos, mudança de senha

[COLE O CÓDIGO]
```

---

## Template de Prompt para Correção

Após identificar um achado, use este template para gerar a correção:

```
Encontrei o seguinte achado de segurança no arquivo [arquivo]:

**Categoria:** OWASP [A0X] — [Nome]
**Severidade:** [CRÍTICO/ALTO]
**Evidência:**
```python
[trecho vulnerável]
```

Gere a correção que:
1. [comportamento esperado específico]
2. [restrição 1 — ex: manter interface existente]
3. [restrição 2 — ex: compatível com Python 3.11]
4. Inclua um teste pytest para o vetor corrigido

Não altere nenhum comportamento fora do escopo deste achado.
```