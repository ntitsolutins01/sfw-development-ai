# Spec — Bugfix: Timeout em upload de arquivos grandes

> **Exemplo didático** — spec de bugfix preenchido completo.
> Use como referência para aprender a preencher o template `03-templates/bugfix.md`.

**Data:** 2026-10-18
**Autor:** equipe backend
**Ticket/Issue:** #198
**Severidade:** [x] Alta
**Status:** [x] Aprovado

---

## 1. Descrição do Bug

**Comportamento atual (incorreto):**
O endpoint `POST /files/upload` retorna `504 Gateway Timeout` para arquivos acima de ~5MB. O upload falha com a conexão ainda aberta no cliente.

**Comportamento esperado (correto):**
O endpoint deve aceitar arquivos de até 50MB sem timeout. Arquivos acima de 50MB devem retornar `413 Payload Too Large` imediatamente, antes de iniciar o upload.

**Como reproduzir:**
1. Gerar um arquivo de teste: `dd if=/dev/zero of=teste.bin bs=1M count=10`
2. Enviar via curl: `curl -X POST http://localhost:8000/files/upload -F "file=@teste.bin"`
3. Após ~30 segundos, a conexão fecha com `504`

**Ambiente onde ocorre:**
- [x] Produção
- [x] Staging
- [ ] Local (não reproduz localmente por ausência de proxy)

---

## 2. Causa Raiz

**Causa identificada:**
O nginx está configurado com `client_max_body_size 1m` e `proxy_read_timeout 30s`. Uploads acima de 1MB são rejeitados pelo nginx antes de chegar ao FastAPI. O timeout de 30s faz o nginx fechar a conexão enquanto o cliente ainda está enviando o corpo da requisição, resultando em `504`.

O código da aplicação (`routes/files.py:L34`) lê o arquivo em memória inteira com `await file.read()`, o que para arquivos grandes causa memory pressure antes mesmo do timeout.

**Arquivo(s) com o problema:**

| Arquivo | Linha(s) | Problema |
|---------|----------|---------|
| `nginx/nginx.conf` | L18-L19 | `client_max_body_size 1m` e `proxy_read_timeout 30s` muito restritivos |
| `routes/files.py` | L34 | `await file.read()` carrega arquivo inteiro na memória |

---

## 3. Solução Proposta

**Descrição da correção:**
1. Atualizar `nginx.conf`: `client_max_body_size 50m` e `proxy_read_timeout 120s`
2. Substituir `await file.read()` por leitura em chunks de 1MB com `async for chunk in file`
3. Adicionar validação de tamanho antes da leitura: rejeitar com `413` se `Content-Length > 50MB`

**Por que esta solução não causa regressão:**
- A mudança no nginx só aumenta os limites — não afeta uploads menores que 1MB
- A leitura por chunks produz o mesmo resultado final, apenas com menor uso de memória
- A validação de tamanho é um novo comportamento explícito, não quebra fluxos existentes

### Arquivos que serão modificados

| Arquivo | Mudança |
|---------|---------|
| `nginx/nginx.conf` | aumentar `client_max_body_size` e `proxy_read_timeout` |
| `routes/files.py` | leitura em chunks + validação de tamanho |

---

## 4. Critérios de Aceite

- [ ] **CA1:** upload de arquivo de 10MB completa com sucesso e retorna `200`
- [ ] **CA2:** upload de arquivo de 50MB completa com sucesso e retorna `200`
- [ ] **CA3:** upload de arquivo de 51MB retorna `413` imediatamente (antes de transferir o arquivo)
- [ ] **CA4:** uso de memória durante upload de 50MB não excede 10MB (leitura em chunks)
- [ ] **CA5:** uploads abaixo de 1MB continuam funcionando normalmente (sem regressão)

---

## 5. Teste de Regressão

```python
# tests/test_upload.py
import pytest
from fastapi.testclient import TestClient

def test_upload_arquivo_grande_completa(client: TestClient, tmp_path):
    # Arquivo de 10MB
    arquivo = tmp_path / "grande.bin"
    arquivo.write_bytes(b"0" * 10 * 1024 * 1024)

    with open(arquivo, "rb") as f:
        response = client.post("/files/upload", files={"file": f})

    assert response.status_code == 200

def test_upload_acima_do_limite_retorna_413(client: TestClient, tmp_path):
    # Arquivo de 51MB
    arquivo = tmp_path / "enorme.bin"
    arquivo.write_bytes(b"0" * 51 * 1024 * 1024)

    with open(arquivo, "rb") as f:
        response = client.post("/files/upload", files={"file": f})

    assert response.status_code == 413

def test_upload_pequeno_nao_regrediu(client: TestClient, tmp_path):
    # Arquivo de 100KB — comportamento original não pode quebrar
    arquivo = tmp_path / "pequeno.bin"
    arquivo.write_bytes(b"0" * 100 * 1024)

    with open(arquivo, "rb") as f:
        response = client.post("/files/upload", files={"file": f})

    assert response.status_code == 200
```

---

## 6. Riscos

| Risco | Probabilidade | Mitigação |
|-------|--------------|-----------|
| Aumento de `client_max_body_size` pode elevar consumo de disco em pico | Baixa | Monitorar disk usage após deploy |
| Timeout de 120s pode manter conexões abertas por mais tempo | Baixa | Aceitável dado o tamanho máximo de 50MB |
