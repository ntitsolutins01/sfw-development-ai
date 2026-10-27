# Template — Relatório de Achado de Segurança

Use este template para documentar cada achado identificado na auditoria OWASP.
Salve em `docs/security/findings/` no projeto de prova.

---

```markdown
# Achado de Segurança — [ID]

**ID:** SEC-[número sequencial]  
**Data:** YYYY-MM-DD  
**Auditor:** [nome ou "Claude Code + revisão humana"]  
**Status:** ABERTO | EM CORREÇÃO | RESOLVIDO | ACEITO (risco aceito)

---

## Identificação

| Campo | Valor |
|-------|-------|
| Categoria OWASP | A0X — Nome |
| Severidade | CRÍTICO / ALTO / MÉDIO / BAIXO |
| Arquivo | `app/services/auth.py` |
| Linha(s) | 42–58 |
| Ambiente | Produção / Staging / Ambos |

---

## Evidência

Trecho exato do código que constitui o risco:

```python
# código vulnerável aqui
```

---

## Vetor de Ataque

Descrição de como um atacante exploraria este achado:

1. [passo 1]
2. [passo 2]
3. [impacto final — o que o atacante obtém]

**Pré-condição:** [o que o atacante precisa ter para explorar — ex: "nenhuma, endpoint público"]

---

## Impacto

- **Confidencialidade:** ALTO / MÉDIO / BAIXO / NENHUM
- **Integridade:** ALTO / MÉDIO / BAIXO / NENHUM
- **Disponibilidade:** ALTO / MÉDIO / BAIXO / NENHUM

---

## Correção Recomendada

```python
# código corrigido aqui
```

**Dependências necessárias:** [ex: `pip install slowapi`]  
**Configuração adicional:** [ex: variável de ambiente, migration de banco]

---

## Plano de Correção

- **Responsável:** [nome]
- **Prazo:** [data]
- **Branch:** `fix/sec-[id]-[slug]`
- **PR:** [link quando aberto]

---

## Verificação

- [ ] Código corrigido e revisado
- [ ] Teste cobrindo o vetor adicionado
- [ ] `/audit-owasp` re-executado — achado não aparece mais
- [ ] `pytest` passando 100%
- [ ] Deploy realizado em [ambiente] em [data]
```