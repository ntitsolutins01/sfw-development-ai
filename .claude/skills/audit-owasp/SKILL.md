# audit-owasp

Você foi invocado via `/audit-owasp`.

## Passo 1 — Identificar o alvo

Verifique se o usuário informou um caminho de arquivo junto ao comando
(ex: `/audit-owasp app/services/auth.py`).

- **Se informou:** use esse(s) arquivo(s) como alvo
- **Se não informou:** use `AskUserQuestion` para perguntar qual arquivo auditar

Nunca prossiga sem ter o arquivo alvo identificado.

---

## Passo 2 — Ler o código

Use a ferramenta `Read` para ler o(s) arquivo(s) informado(s).

Se múltiplos arquivos foram informados, leia todos antes de iniciar a análise.

---

## Passo 3 — Analisar por categoria OWASP

Para cada uma das 10 categorias do OWASP Top 10 (2021), analise o código lido.

Use este critério por categoria:

### A01 — Broken Access Control
- Endpoints sem verificação de token
- Endpoints com token mas sem verificação de propriedade do recurso (IDOR)
- Verificações de permissão baseadas em parâmetro controlável pelo cliente

### A02 — Cryptographic Failures
- Segredos JWT/API hardcoded no código
- Segredos lidos de variável de ambiente sem validação de tamanho mínimo (32 chars)
- Algoritmo JWT `"none"` na lista de algoritmos aceitos
- Algoritmos fracos: MD5, SHA1, DES para dados sensíveis
- Senhas armazenadas sem hash ou com hash sem salt

### A03 — Injection
- Queries SQL construídas com concatenação de string ou f-string com input externo
- `eval()`, `exec()`, `subprocess.run()` com dados não sanitizados
- ORM usado com `.filter(text(f"..."))` passando dados do usuário

### A04 — Insecure Design
- Lógica de autenticação e autorização misturadas no mesmo handler
- Ausência de mecanismo de revogação de token (sem blocklist)
- Fluxo de reset de senha sem verificação de expiração do código

### A05 — Security Misconfiguration
- `debug=True` em configuração de produção
- Stack trace completo retornado em responses de erro
- Cabeçalhos de segurança ausentes (CORS permissivo, `*` em origins)
- Variáveis de ambiente sensíveis logadas na inicialização

### A06 — Vulnerable and Outdated Components
- **Nota:** não detectável por análise de código. Marque como:
  "SEM ACHADOS — verificação requer `pip audit` ou `safety check` externo"

### A07 — Identification and Authentication Failures
- Endpoints de login sem rate limiting
- Tokens JWT sem campo `exp` (sem expiração)
- Mensagens de erro diferentes para "email não existe" vs "senha incorreta"
- Logout que não invalida o token

### A08 — Software and Data Integrity Failures
- Desserialização de dados externos sem validação de schema
- `pickle.loads()` com dados de origem externa

### A09 — Security Logging and Monitoring Failures
- Falhas de autenticação sem log
- Logs de falha sem IP, email ou timestamp
- Dados sensíveis (senha, token completo) aparecendo em logs
- Ausência de log para login bem-sucedido

### A10 — Server-Side Request Forgery (SSRF)
- `requests.get(url)` onde `url` vem de input do usuário sem validação
- Fetch de recursos externos com URL controlável pelo cliente

---

## Passo 4 — Gerar o relatório

Produza o relatório estruturado no formato abaixo.
Use exatamente esta estrutura para cada categoria:

```
## Relatório OWASP Top 10 — [nome do arquivo]

### A01 — Broken Access Control
**Status:** ACHADO CRÍTICO | ACHADO ALTO | ACHADO MÉDIO | ACHADO BAIXO | SEM ACHADOS

**Evidência:**
```python
# trecho exato do código vulnerável (arquivo + linha se souber)
```

**Vetor:** [como seria explorado — passos concretos]

**Severidade:** CRÍTICO | ALTO | MÉDIO | BAIXO

**Correção:**
```python
# código corrigido
```

---

[repita para A02–A10]

---

## Sumário dos Achados

| Categoria | Severidade | Status |
|-----------|-----------|--------|
| A01 | ALTO | ACHADO |
| A02 | — | SEM ACHADOS |
...

**Total:** X CRÍTICO, Y ALTO, Z MÉDIO, W BAIXO
```

Critérios de severidade:
- **CRÍTICO**: exploração direta sem autenticação, dados sensíveis em risco imediato
- **ALTO**: requer condição adicional para explorar (ex: autenticação válida)
- **MÉDIO**: risco em contexto específico ou impacto limitado
- **BAIXO**: hardening, boas práticas sem risco imediato
- **INFO**: observação sem risco

---

## Passo 5 — Oferecer correção

Ao final do relatório, se houver achados CRÍTICO ou ALTO, pergunte ao usuário:

```
Encontrei X CRÍTICO e Y ALTO.
Deseja que eu gere as correções agora?
- Sim, corrigir todos os CRÍTICO e ALTO
- Sim, corrigir apenas [categoria específica]
- Não, vou corrigir manualmente
```

Se o usuário pedir correção, gere o código corrigido para cada achado com:
1. O trecho original (evidência)
2. O código corrigido completo (não apenas o diff)
3. Um teste pytest para o vetor corrigido
4. Instrução de instalação se a correção requer nova dependência

---

## Comportamento em Casos Especiais

**Arquivo muito grande (>300 linhas):** avise o usuário que a análise cobre o arquivo
completo, mas recomende auditar os módulos mais críticos individualmente para maior
precisão.

**A06 sempre:** nunca marque como "SEM ACHADOS" sem o aviso de que requer verificação
externa (`pip audit` ou `safety check`).

**A04 — Insecure Design:** indique suspeitas de design inseguro, mas deixe claro que
a decisão de redesign requer julgamento humano e visão arquitetural além do arquivo.