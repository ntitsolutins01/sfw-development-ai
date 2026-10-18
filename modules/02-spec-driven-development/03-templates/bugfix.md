> **[TEMPLATE] Como usar este arquivo**
>
> Copie para `docs/specs/YYYY-MM-DD-bugfix-<slug>.md` e preencha todas as seções.
> Preencha a seção "Causa raiz" antes de propor a solução — corrigir sem entender a causa gera regressões.

---

# Spec — Bugfix: [Descrição curta do bug]

**Data:** YYYY-MM-DD
**Autor:** [nome]
**Ticket/Issue:** [link]
**Severidade:** [ ] Crítica  [ ] Alta  [ ] Média  [ ] Baixa
**Status:** [ ] Rascunho  [ ] Em revisão  [ ] Aprovado  [ ] Corrigido

---

## 1. Descrição do Bug

**Comportamento atual (incorreto):**
[Descreva o que o sistema faz errado. Seja específico.]

**Comportamento esperado (correto):**
[Descreva o que o sistema deveria fazer.]

**Como reproduzir:**
1. [passo 1]
2. [passo 2]
3. [resultado incorreto observado]

**Ambiente onde ocorre:**
- [ ] Produção
- [ ] Staging
- [ ] Local
- [ ] Todos

---

## 2. Causa Raiz

> Preencha após investigação. Não proponha solução antes de identificar a causa.

**Causa identificada:**
[Descreva a causa técnica do bug. Ex: "o campo X não é validado antes de Y, causando Z"]

**Arquivo(s) com o problema:**

| Arquivo | Linha(s) | Problema |
|---------|----------|---------|
| [caminho/arquivo.py] | [L42-L55] | [descrição] |

---

## 3. Solução Proposta

**Descrição da correção:**
[Descreva o que será alterado para corrigir o bug.]

**Por que esta solução não causa regressão:**
[Explique por que a correção não quebra outros comportamentos.]

### Arquivos que serão modificados

| Arquivo | Mudança |
|---------|---------|
| [caminho/arquivo.py] | [o que muda] |

---

## 4. Critérios de Aceite

- [ ] **CA1:** [o bug original não se reproduz mais — descreva o cenário]
- [ ] **CA2:** [comportamento adjacente não foi quebrado — descreva]
- [ ] **CA3:** [teste de regressão adicionado para este bug]

---

## 5. Teste de Regressão

> Descreva o teste que será adicionado para garantir que este bug não volte.

```python
# Exemplo de teste de regressão
def test_[nome_do_bug_corrigido]():
    # Arrange
    # Act
    # Assert
    pass
```

---

## 6. Riscos

| Risco | Probabilidade | Mitigação |
|-------|--------------|-----------|
| [risco 1] | [baixa/média/alta] | [como mitigar] |
