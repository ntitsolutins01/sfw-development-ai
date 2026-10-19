# Fluxo de Revisão com IA

## Visão geral

```
[autor]                    [IA]                      [revisor humano]
   │                         │                              │
   ├─ self-review ──────────→│                              │
   │  (checklist local)      │                              │
   │                         │                              │
   ├─ /code-review ─────────→│                              │
   │                    revisão geral                       │
   │                  (bugs/segurança/perf)                 │
   │←── relatório ───────────┤                              │
   │                         │                              │
   ├─ corrige achados         │                              │
   │                         │                              │
   ├─ /review-pr <spec> ────→│                              │
   │                  revisão com spec                      │
   │                  (CAs cobertos?)                       │
   │←── decisão ─────────────┤                              │
   │                         │                              │
   ├─ corrige pendências      │                              │
   │                         │                              │
   ├─ abre PR ───────────────────────────────────────────→ │
   │                                                        │
   │                                                   revisão humana
   │                                                (design/contexto)
   │←── aprovação ou mudanças ──────────────────────────── │
```

---

## Fase 1 — Self-review (antes de abrir o PR)

Antes de envolver qualquer pessoa ou ferramenta, o próprio autor percorre o checklist do template correspondente (`03-templates/`).

**O que fazer:**
1. Abra o template adequado ao tipo de mudança (feature, bugfix, refactor)
2. Percorra cada item do checklist
3. Corrija o que encontrar
4. Rode os testes: `pytest` ou `npm test`

**Critério de saída:** todos os itens do checklist marcados ou justificados.

---

## Fase 2 — Revisão geral com `/code-review`

Com o branch ativo no Claude Code, execute:

```
/code-review
```

A skill analisa o `git diff main...HEAD` e reporta achados por severidade.

**O que fazer com o relatório:**
- **CRÍTICO:** corrigir antes de qualquer outra coisa
- **ALTO:** corrigir antes de continuar
- **MÉDIO:** avaliar e documentar decisão se não corrigir
- **BAIXO:** opcional — decidir e seguir em frente

Rode os testes após cada correção para garantir que não quebrou nada.

---

## Fase 3 — Revisão com spec usando `/review-pr`

Com o spec do Módulo 2 disponível, execute:

```
/review-pr docs/specs/001-nome-da-feature.md
```

A skill compara o diff com cada critério de aceite do spec e produz:

```
## Revisão com Spec — feature/autenticacao-jwt

### Critérios de Aceite
- [x] POST /auth/login retorna token JWT com credenciais corretas
- [x] POST /auth/login retorna 401 com credenciais incorretas
- [x] Token expira em 24 horas
- [ ] POST /auth/logout invalida o token na blocklist
      ↳ ALTO: implementação não encontrada para invalidação de token

### Cobertura de Testes
- [x] test_login_success — cobre CA 1
- [x] test_login_invalid_credentials — cobre CA 2
- [x] test_token_expiry — cobre CA 3
- [ ] test_logout_blocklist — AUSENTE (CA 4 sem teste)

### Decisão
SOLICITAR MUDANÇAS — 1 CA não implementado, 1 teste ausente
```

---

## Fase 4 — Revisão humana (após aprovação da IA)

Quando `/review-pr` retorna `APROVADO`, o PR está pronto para revisão humana.

O revisor humano foca no que a IA não cobre:
- **Alinhamento estratégico:** essa é a solução certa para o problema?
- **Impacto sistêmico:** como essa mudança afeta outros sistemas?
- **Decisões de design:** as abstrações fazem sentido no contexto do projeto?
- **Dívida técnica:** essa mudança aumenta ou reduz dívida técnica?

---

## Integrando o spec na revisão

O spec do Módulo 2 tem critérios de aceite explícitos. Use-os como base de comparação:

```markdown
# spec: 001-autenticacao-jwt.md

## Critérios de aceite
- CA-1: POST /auth/login retorna 200 e token JWT com credenciais válidas
- CA-2: POST /auth/login retorna 401 com mensagem genérica para credenciais inválidas
- CA-3: Token JWT expira em 24h (campo `exp` no payload)
- CA-4: POST /auth/logout adiciona o token à blocklist no Redis
- CA-5: Endpoint protegido retorna 401 se token estiver na blocklist
```

Para cada CA, `/review-pr` verifica:
1. **Existe implementação?** — busca no diff por código relacionado ao CA
2. **Existe teste?** — busca no diff por teste que cobre o CA
3. **O teste está correto?** — analisa se o teste realmente valida o comportamento esperado

---

## Checklist de aprovação final

Antes de marcar o PR como pronto para merge:

- [ ] Self-review feito com o template adequado
- [ ] `/code-review` executado — zero CRÍTICO, zero ALTO
- [ ] `/review-pr <spec>` executado — todos os CAs cobertos
- [ ] Todos os testes passando no branch
- [ ] Descrição do PR atualizada com o que foi implementado
- [ ] Spec atualizado se houve mudança nos CAs durante a implementação