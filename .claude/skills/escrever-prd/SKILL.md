---
name: escrever-prd
description: Cria e edita PRDs (Product Requirements Documents) — o documento humano da feature, fonte de verdade da intenção de produto. Opera em modo draft-first, gerando o documento completo imediatamente com premissas marcadas para revisão.
disable-model-invocation: false
---

# escrever-prd

## Objetivo
Criar o **PRD (Product Requirements Document)** — o documento que captura o problema, a solução de produto, as user stories com regras e casos de borda, e os critérios de aceite. É o documento humano da feature: define O QUE construir, não COMO.

## Quando usar
- Feature nova com impacto de produto (o usuário vai notar a mudança)
- O time precisa alinhar O QUE será construído antes de discutir COMO
- Há user stories com regras de negócio complexas ou casos de borda não óbvios
- Há múltiplos stakeholders que precisam validar antes da implementação

## Quando NÃO usar
- Bugfix (use `03-templates/bugfix.md` diretamente)
- Refactor interno sem impacto visível para o usuário
- Feature trivial com comportamento óbvio e escopo de 1 arquivo

## O que ela faz

1. Detecta se é criação (novo PRD) ou edição (PRD existente referenciado)
2. Verifica se o pedido cobre mais de uma feature — se sim, propõe split
3. Escaneia `docs/prds/` para determinar o próximo número sequencial
4. Gera o PRD completo imediatamente (draft-first), marcando premissas com `[PREMISSA]`
5. Salva em `docs/prds/NNN-nome-em-kebab-case.md`
6. Orienta o próximo passo no fluxo SDD

## O que ela NÃO faz
- Não cobre decisões técnicas de implementação (stack, padrões, arquitetura) — isso é o TRD
- Não decompõe em tasks executáveis
- Não transiciona status manualmente
- Não altera PRDs com `status: concluido` — esses são imutáveis

## Status do PRD

| Status | Significado |
|--------|-------------|
| `rascunho` | gerado, ainda não revisado |
| `pronto` | revisado, aprovado para implementar |
| `em-progresso` | implementação em andamento |
| `concluido` | implementado e validado — imutável |

## Como o PRD alimenta o spec técnico
Os critérios de aceite do PRD são o ponto de partida direto para a seção **CA** do template `03-templates/feature.md`. Não reescreva — transporte e adapte para linguagem técnica.

## Argumentos aceitos
- `/escrever-prd` — inicia coleta do contexto da feature
- `/escrever-prd` + descrição inline — gera diretamente a partir da descrição

## Exemplo de uso

```
/escrever-prd

Feature: autenticação com JWT
- Usuários fazem login com email e senha
- Token expira em 1 hora
- Logout invalida o token imediatamente
```

Saída esperada (resumida):
```
Gerando PRD-001...

docs/prds/001-autenticacao-jwt.md criado.

## PRD-001: Autenticação com JWT
status: rascunho

### US-001-01: Login com email e senha
Como usuário cadastrado,
quero fazer login com email e senha,
para que eu possa acessar recursos protegidos.

Rules:
- Token JWT expira em 1 hora
- [PREMISSA] Refresh token será implementado nesta mesma feature?

Edge cases:
- Email inexistente → 401 "invalid_credentials" (não revela existência do email)
- Conta desativada → 401 "account_disabled"

Critérios de aceite:
- [ ] Login com credenciais válidas retorna 200 + { token, expires_in: 3600 }
- [ ] Login com email inexistente retorna 401
...

PRÓXIMO PASSO:
→ /escrever-trd  para definir restrições técnicas (se não existe TRD ainda)
→ feature.md     para o spec de implementação (modules/02-spec-driven-development/03-templates/)
```

---

## Instruções operacionais

### Passo 1 — Detectar modo

- **Modo Criação:** nenhum PRD existente mencionado → crie novo
- **Modo Edição:** PRD existente referenciado → edite preservando `prd_number`, IDs de user stories e milestones

PRDs com `status: concluido` são **imutáveis**. Mudanças requerem novo PRD.

### Passo 2 — Analisar escopo

Antes de gerar:
- Pedido cobre múltiplas features independentes? → proponha split e aguarde confirmação
- Há dependência de outro PRD? → registre em `depends_on`

### Passo 3 — Gerar draft-first

Gere o documento completo imediatamente. Marque premissas com `> **[PREMISSA]:** texto` para revisão pontual. Não faça perguntas antes de gerar.

**Numeração:** escaneie `docs/prds/` para o próximo número. Se não existir, comece com `001`.
**Nome do arquivo:** `docs/prds/NNN-nome-em-kebab-case.md`

**Frontmatter obrigatório:**
```yaml
---
prd_number: NNN
title: "Título"
status: rascunho
depends_on: []
created_at: YYYY-MM-DD
---
```

**Estrutura obrigatória:**
```markdown
# PRD-NNN: [Título]

## 1. Problema
## 2. Solução de Produto
## 3. Escopo (dentro / fora)
## 4. Funcionalidades e User Stories
   ### US-NNN-NN: [Título]
   Como / quero / para que
   Rules: [regras de negócio]
   Edge cases: [casos → comportamento]
   Critérios de aceite: [ ] verificáveis
## 5. Métricas de Sucesso
## 6. Fluxo de Negócio
## 7. Milestones
```

### Passo 4 — Salvar e orientar

Salve em `docs/prds/NNN-nome.md`. Se o diretório não existir, crie-o.

Ao final, oriente:
```
PRÓXIMO PASSO:
→ /escrever-trd  se não existe TRD (define stack e restrições técnicas globais)
→ feature.md     os CAs do PRD alimentam diretamente a seção CA do spec técnico
                 (modules/02-spec-driven-development/03-templates/feature.md)
```
