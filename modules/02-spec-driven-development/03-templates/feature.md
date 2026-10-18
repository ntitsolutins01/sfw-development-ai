> **[TEMPLATE] Como usar este arquivo**
>
> Copie para `docs/specs/YYYY-MM-DD-feature-<slug>.md` e preencha todas as seções.
> Não implemente nada antes de ter os critérios de aceite preenchidos.
> Use o prompt de revisão antes de passar para implementação.

---

# Spec — Feature: [Nome da Feature]

**Data:** YYYY-MM-DD
**Autor:** [nome]
**Ticket/Issue:** [link ou N/A]
**Status:** [ ] Rascunho  [ ] Em revisão  [ ] Aprovado  [ ] Implementado

---

## 1. Contexto

> Por que essa feature está sendo criada? Qual problema resolve para o usuário ou para o sistema?

[Descreva o problema ou necessidade que motivou esta feature. 2-4 frases.]

**Estado atual do sistema:**
[Descreva como o sistema se comporta hoje, antes desta mudança.]

---

## 2. Escopo

### Está dentro do escopo

- [item 1]
- [item 2]

### Está fora do escopo

- [item 1 — o que não será feito nesta feature]
- [item 2]

---

## 3. Comportamento Esperado

> Descreva o que o sistema faz após a mudança. Use linguagem de comportamento, não de implementação.

### Fluxo principal

1. [passo 1]
2. [passo 2]
3. [passo 3]

### Fluxos alternativos

| Situação | Comportamento esperado |
|----------|----------------------|
| [caso de borda 1] | [o que acontece] |
| [caso de borda 2] | [o que acontece] |

---

## 4. Critérios de Aceite

> Cada critério deve ser verificável — idealmente por um teste automatizado.

- [ ] **CA1:** [critério verificável — ex: "Dado X, quando Y, então Z"]
- [ ] **CA2:** [critério verificável]
- [ ] **CA3:** [critério verificável]

---

## 5. Impacto

### Arquivos que serão modificados

| Arquivo / Módulo | Tipo de mudança |
|-----------------|-----------------|
| [caminho/arquivo.py] | [adição / modificação / remoção] |

### Contratos externos afetados

| Contrato | Mudança |
|----------|---------|
| [API / schema / evento] | [descrição da mudança] |

### Dependências

- [bibliotecas, serviços ou módulos que esta feature depende]

---

## 6. Restrições

- **Performance:** [ex: "deve responder em menos de 200ms em p95"]
- **Segurança:** [ex: "não expõe dados de outros usuários"]
- **Compatibilidade:** [ex: "deve funcionar com Python 3.11+"]
- **Outras:** [ex: "não pode quebrar o endpoint /health"]

---

## 7. Como Testar

```bash
# Comando para executar os testes desta feature
[ex: pytest tests/test_feature.py -v]
```

**Teste manual (smoke test):**
1. [passo para verificar manualmente o comportamento]
2. [passo 2]
