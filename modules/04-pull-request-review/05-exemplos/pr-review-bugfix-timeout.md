# Exemplo: PR Review — Bugfix de Timeout em Upload

> Baseado no spec `modules/02-spec-driven-development/05-exemplos/spec-bugfix-timeout-upload.md`.

---

## Contexto do PR

**Branch:** `fix/upload-timeout-nginx`
**Título:** `fix: increase nginx timeout and add chunked upload to prevent 413/504 errors`
**Spec:** `docs/specs/002-bugfix-timeout-upload.md`

**Critérios de aceite do spec:**
- CA-1: Upload de arquivos até 100MB não retorna 413 (payload too large)
- CA-2: Upload de arquivos até 100MB não retorna 504 (timeout)
- CA-3: Arquivos > 100MB retornam 413 com mensagem clara
- CA-4: Progresso do upload é reportado ao cliente em tempo real

---

## Resultado do `/code-review`

```
## Revisão de Código — fix/upload-timeout-nginx — 2026-10-19

### Resumo
0 críticos, 0 altos, 1 médio, 2 baixos

### Achados

#### [MÉDIO] Sem validação de tipo MIME antes do upload — upload_service.py:22
Problema: Apenas o tamanho é verificado, não o tipo do arquivo.
Um arquivo malicioso pode ser enviado com extensão válida mas conteúdo executável.
Sugestão: Adicione validação de MIME type com `python-magic` ou verifique a
assinatura dos primeiros bytes: `filetype.guess(file_header)`.

#### [BAIXO] Timeout configurado em código — upload_service.py:45
Problema: `UPLOAD_TIMEOUT = 300` hardcoded em vez de variável de ambiente.
Sugestão: `UPLOAD_TIMEOUT = int(os.getenv("UPLOAD_TIMEOUT_SECONDS", "300"))`

#### [BAIXO] Log de filename sem sanitização — upload_service.py:67
Problema: Nome do arquivo do usuário logado diretamente — pode injetar caracteres
de controle nos logs.
Sugestão: `logger.info("Upload started: %s", filename.encode("ascii", "replace"))`
```

---

## Resultado do `/review-pr docs/specs/002-bugfix-timeout-upload.md`

```
## Revisão com Spec — fix/upload-timeout-nginx

### Critérios de Aceite
- [x] CA-1: Upload até 100MB sem 413
      → nginx.conf: client_max_body_size 100m
      → test_upload_100mb_no_413
- [x] CA-2: Upload até 100MB sem 504
      → nginx.conf: proxy_read_timeout 300s
      → upload_service.py: chunked upload implementado
      → test_upload_100mb_no_timeout
- [x] CA-3: Arquivos > 100MB retornam 413 com mensagem
      → upload_service.py:18: validação de tamanho com mensagem descritiva
      → test_upload_oversized_returns_413_with_message
- [ ] CA-4: Progresso reportado ao cliente em tempo real
      AUSENTE: não encontrei implementação de SSE ou WebSocket para progresso.
      O chunked upload existe mas o progresso não é enviado ao cliente.

### Decisão
SOLICITAR MUDANÇAS — CA-4 não implementado.
```

**Ação do autor:** implementou SSE (Server-Sent Events) para reportar progresso. Re-executou `/review-pr` após a correção e obteve APROVADO.