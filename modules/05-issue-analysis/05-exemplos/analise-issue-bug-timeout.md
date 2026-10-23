# Exemplo: Análise de Issue — Bug de Timeout em Upload

> Baseado no spec `modules/02-spec-driven-development/05-exemplos/spec-bugfix-timeout-upload.md`.

---

## Issue original (bruta)

```
[BUG] Upload de arquivos grandes falha

Usuários estão reclamando que o upload de arquivos não funciona.
Estamos recebendo erros no Sentry.

Prioridade: Alta
```

---

## Resultado do Prompt 1 — Análise inicial

```
**Tipo:** Bug — comportamento quebrado reportado por usuários.

**Ambiguidades críticas:**
1. "Arquivos grandes" — qual tamanho específico falha?
2. "Não funciona" — qual é o erro exato? 413? 504? 500?
3. "Erros no Sentry" — qual é a stack trace?
4. Desde quando? Foi introduzido por um deploy recente?
5. Frequência — todos os usuários ou subconjunto específico?

**Perguntas de clarificação:**
1. Qual status code retorna quando falha? (413 Payload Too Large, 504 Gateway Timeout, outro?)
2. Qual é o tamanho mínimo de arquivo que reproduz o bug?
3. Qual é a stack trace no Sentry?
4. Quando o bug foi reportado pela primeira vez?
```

**Respostas obtidas do time:**
1. Dois erros: 413 para arquivos > 1MB e 504 para uploads que demoram > 30s
2. Tamanho mínimo reproduzível: ~5MB consistentemente
3. Stack trace: `nginx: client intended to send too large body` + `upstream timed out (110: Connection timed out)`
4. Apareceu após deploy da semana passada (mudança de configuração do nginx)
5. Todos os usuários afetados

---

## Resultado do Prompt 2 — Decomposição

```
**TASK-1:** Corrigir limite de tamanho no nginx (causa do 413)
- Escopo: aumentar client_max_body_size para 100MB, testar limites
- Dependências: nenhuma

**TASK-2:** Corrigir timeout no nginx (causa do 504)
- Escopo: aumentar proxy_read_timeout e proxy_send_timeout, implementar upload chunked
- Dependências: nenhuma (pode ser feita em paralelo)

**TASK-3:** Adicionar validação de tamanho na aplicação
- Escopo: rejeitar arquivos > 100MB com mensagem descritiva antes de chegar ao nginx
- Dependências: TASK-1 (define o novo limite)
```

---

## Resultado do Prompt 3 — Critérios de aceite

```
**TASK-1 + TASK-2 (testes integrados):**
- CA-1: upload de arquivo de 50MB retorna 200 em menos de 120 segundos
- CA-2: upload de arquivo de 100MB retorna 200 (limite máximo aceito)
- CA-3: upload de arquivo de 101MB retorna 413 com mensagem: "Arquivo excede o limite de 100MB"

**TASK-3:**
- CA-4: dado arquivo > 100MB, quando tentativa de upload, então retorna 413 com corpo JSON:
  `{"error": "file_too_large", "max_size_mb": 100, "received_size_mb": X}`
- CA-5: dado arquivo ≤ 100MB, quando upload iniciado, então progresso é reportado via SSE a cada 10%
```