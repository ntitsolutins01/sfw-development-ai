> **[TEMPLATE] Como usar este arquivo**
>
> Copie para `docs/specs/YYYY-MM-DD-refactor-<slug>.md` e preencha todas as seções.
> Refactor sem spec tende a escalar. A seção "Escopo" é especialmente importante: delimite onde o refactor para.

---

# Spec — Refactor: [Nome do Componente/Módulo]

**Data:** YYYY-MM-DD
**Autor:** [nome]
**Ticket/Issue:** [link ou N/A]
**Muda interface pública?** [ ] Sim  [ ] Não
**Status:** [ ] Rascunho  [ ] Em revisão  [ ] Aprovado  [ ] Implementado

---

## 1. Motivação

**Por que refatorar agora?**
[Descreva o problema que o refactor resolve: dívida técnica, performance, legibilidade, testabilidade, etc.]

**Estado atual (o problema):**
[Descreva como o código está hoje e por que isso é um problema.]

**Estado esperado (a melhoria):**
[Descreva como o código estará após o refactor e o benefício concreto.]

---

## 2. Escopo

### Está dentro do escopo

- [componente / módulo / função que será refatorado]
- [outro item]

### Está fora do escopo

- [o que NÃO será tocado — explícito para evitar scope creep]
- [outro item]

**Limite do refactor:**
[Descreva em uma frase onde este refactor para. Ex: "vai até a camada de serviço, não toca o banco de dados"]

---

## 3. Mudanças de Interface

> Se a interface pública não muda, pule esta seção.

### Antes

```python
# Assinatura / contrato atual
def [nome_função](param1, param2):
    ...
```

### Depois

```python
# Assinatura / contrato novo
def [nome_função](param1: Tipo, param2: Tipo) -> TipoRetorno:
    ...
```

**Compatibilidade retroativa:** [ ] Mantida  [ ] Quebrada (lista callers abaixo)

**Callers que precisam ser atualizados:**

| Arquivo | Linha | Mudança necessária |
|---------|-------|--------------------|
| [arquivo] | [linha] | [o que muda] |

---

## 4. Arquivos Impactados

| Arquivo | Tipo de mudança |
|---------|-----------------|
| [caminho/arquivo.py] | [reescrita / renomeação / extração / remoção] |

---

## 5. Critérios de Aceite

- [ ] **CA1:** comportamento externo idêntico ao atual (todos os testes existentes passam)
- [ ] **CA2:** [melhoria mensurável — ex: "complexidade ciclomática < 5", "cobertura > 80%"]
- [ ] **CA3:** [outro critério específico deste refactor]

---

## 6. Estratégia de Migração

> Como fazer a transição sem quebrar nada em produção?

- [ ] Adicionar nova implementação ao lado da atual
- [ ] Migrar callers um por um
- [ ] Remover implementação antiga
- [ ] Outro: [descreva]

**Pode ser feito em um único PR?** [ ] Sim  [ ] Não → [descreva como dividir]

---

## 7. Como Verificar que Nada Quebrou

```bash
# Comando para rodar os testes de regressão
[ex: pytest tests/ -v --tb=short]
```
