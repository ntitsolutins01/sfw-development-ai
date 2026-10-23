# Exemplo: Análise de Issue — Task de Refatoração

> Contexto: após o Módulo 4 (PR Review), o revisor identificou que `UserService` mistura lógica de negócio com queries de banco — dívida técnica que deve ser tratada antes do próximo módulo de segurança.

---

## Issue original (bruta)

```
[TASK] Refatorar UserService para separar acesso a banco

O UserService está muito grande e mistura lógica com queries SQL.
Isso dificulta os testes e vai ser um problema quando precisarmos
trocar o banco de dados.

Prioridade: Média
```

---

## Resultado do Prompt 1 — Análise inicial

```
**Tipo:** Task técnica — refatoração sem mudança de comportamento externo.

**Escopo aparente:**
- Dentro: separar queries de banco da lógica de negócio em UserService
- Fora: não está claro se inclui testes novos ou apenas preservação dos existentes

**Ambiguidades:**
1. "Trocar o banco de dados" — qual é a arquitetura alvo? Repository Pattern? ORM abstraction?
2. Quais métodos de UserService têm o problema?
3. Interface pública de UserService vai mudar?

**Respostas assumidas:**
1. Repository Pattern — UserRepository isola todas as queries
2. Todos os métodos que chamam o banco diretamente
3. Interface pública NÃO muda (refatoração interna)
```

---

## Resultado do Prompt 2 — Decomposição

```
**TASK-1:** Criar UserRepository com interface AbstractUserRepository
- Escopo: ABC com métodos find_by_id, find_by_email, create, update, delete
- Dependências: nenhuma

**TASK-2:** Migrar queries de UserService para UserRepository
- Escopo: mover todas as chamadas SQL/ORM de UserService para UserRepository
- Dependências: TASK-1

**TASK-3:** Injetar UserRepository em UserService
- Escopo: UserService recebe UserRepository via construtor (DI), não instancia diretamente
- Dependências: TASK-1, TASK-2
```

---

## Resultado do Prompt 3 — Critérios de aceite

```
**Critério principal (não-regressão):**
- CA-1: todos os testes existentes de UserService passam sem modificação após a refatoração
- CA-2: a interface pública de UserService é idêntica à original (mesmas assinaturas de método)

**TASK-1:**
- CA-3: AbstractUserRepository define pelo menos: find_by_id(id), find_by_email(email),
  create(data), update(id, data), delete(id)
- CA-4: UserRepository implementa todos os métodos de AbstractUserRepository

**TASK-3:**
- CA-5: UserService aceita UserRepository via construtor com tipo AbstractUserRepository
- CA-6: instanciar UserService sem UserRepository lança TypeError descritivo
```

---

## Lição deste exemplo

Tasks de refatoração têm um critério de aceite principal diferente de features e bugs: **os testes existentes passam sem modificação**.

Isso é deliberado — se você precisar modificar um teste para fazer a refatoração passar, ou você mudou o comportamento externo (não é mais refatoração) ou o teste estava testando implementação em vez de comportamento.

A IA ajuda especialmente a definir o escopo negativo: o que **não** vai mudar — interface pública, comportamento dos endpoints, estrutura dos dados retornados.