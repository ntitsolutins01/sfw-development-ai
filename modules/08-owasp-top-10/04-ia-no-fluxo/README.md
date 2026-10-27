# IA no Fluxo — Skill `/audit-owasp`

## O que a skill faz

`/audit-owasp [arquivo]` executa um pipeline de 5 etapas sobre o arquivo informado:

1. **Scan**: lê o arquivo e mapeia endpoints, dependências e dados sensíveis
2. **Analyze**: aplica cada uma das 10 categorias OWASP ao código lido
3. **Report**: gera relatório estruturado com achados por categoria e severidade
4. **Fix**: para achados CRÍTICO e ALTO, oferece gerar a correção imediatamente
5. **Verify**: após correções, re-executa a análise para confirmar resolução

## Como Invocar

```
/audit-owasp app/services/auth.py
```

Se omitir o caminho, a skill vai perguntar qual arquivo auditar.

Para auditar múltiplos arquivos:
```
/audit-owasp app/services/auth.py app/routers/auth.py app/middleware/jwt.py
```

## Exemplo de Saída

```
## Relatório OWASP Top 10 — app/services/auth.py

### A01 — Broken Access Control
**Status:** ACHADO ALTO

**Evidência:**
```python
# linha 87
@app.get("/user/profile")
async def get_profile(user_id: int):
    return db.get_user(user_id)
```

**Vetor:** Qualquer cliente pode solicitar o perfil de qualquer usuário trocando
`user_id` no parâmetro. Não há verificação de token nem de propriedade do recurso.

**Severidade:** ALTO

**Correção:**
```python
@app.get("/user/profile")
async def get_profile(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.get_user(user_id)
```

---

### A02 — Cryptographic Failures
**Status:** ACHADO CRÍTICO

**Evidência:**
```python
# linha 12
JWT_SECRET = "secret"
```

**Vetor:** Segredo JWT de 6 caracteres. Um atacante pode forçar tokens válidos
com um ataque de dicionário ou brute force em minutos, criando sessões para
qualquer usuário sem precisar das credenciais.

**Severidade:** CRÍTICO

**Correção:**
```python
JWT_SECRET = os.environ["JWT_SECRET"]  # mínimo 32 chars aleatórios
```

---

[...continua para A03–A10...]

## Sumário

| Categoria | Severidade | Status |
|-----------|-----------|--------|
| A01 | ALTO | ACHADO |
| A02 | CRÍTICO | ACHADO |
| A03 | — | SEM ACHADOS |
| A04 | — | SEM ACHADOS (requer análise arquitetural) |
| A05 | MÉDIO | ACHADO |
| A06 | — | SEM ACHADOS (use pip audit para verificar) |
| A07 | ALTO | ACHADO |
| A08 | — | SEM ACHADOS |
| A09 | MÉDIO | ACHADO |
| A10 | — | SEM ACHADOS |

**Total:** 1 CRÍTICO, 2 ALTO, 2 MÉDIO

Deseja que eu gere as correções para os achados CRÍTICO e ALTO agora?
```

## Como Usar os Resultados

### Corrigir CRÍTICO primeiro, sempre

Para cada achado CRÍTICO, peça a correção diretamente:

```
Gere a correção para o achado A02 (JWT_SECRET hardcoded).
Requisitos:
- Ler da variável de ambiente JWT_SECRET
- Validar na inicialização que a variável existe e tem >= 32 caracteres
- Adicionar erro descritivo se ausente
- Não quebrar os testes existentes
```

### Verificar após cada correção

Não acumule todas as correções para verificar no final. Após cada correção:

```
Reanalize o arquivo app/services/auth.py focando em A02.
O achado anterior era JWT_SECRET = "secret". Verifique se foi resolvido.
```

### Documentar os achados

Para achados que serão corrigidos em outro momento (MÉDIO, BAIXO), documente usando
o template em `03-templates/finding-report.md`. Salve em `docs/security/findings/SEC-001.md`.

## Limitações a Conhecer

**A06 (Outdated Components)** não é detectável por análise de código:
```bash
# Verificação separada
pip audit
# ou
safety check
```

**A04 (Insecure Design)** requer visão arquitetural. A skill vai indicar suspeitas
(ex: "não há separação entre autenticação e autorização"), mas a decisão de redesign
precisa de julgamento humano.

**Falsos negativos em lógica customizada:** se a validação de token estiver em um
decorator ou middleware importado de outro arquivo, a skill vai marcar "SEM ACHADOS"
para A01 — é necessário fornecer o arquivo do middleware também.

## Workflow Recomendado por PR

1. Antes de abrir o PR: `/audit-owasp [arquivos modificados]`
2. Corrigir todos os CRÍTICO e ALTO
3. Documentar os MÉDIO em `docs/security/findings/`
4. Re-executar para confirmar zero CRÍTICO e zero ALTO
5. Incluir no PR description: "OWASP audit: 0 CRÍTICO, 0 ALTO, N MÉDIO documentados"