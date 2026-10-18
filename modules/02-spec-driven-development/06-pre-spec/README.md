# 06 — Pré-Spec: Brainstorm → PRD → TRD

> **Em uma frase:** antes de escrever qualquer spec técnico, use estas três skills para
> garantir que você está especificando a coisa certa, do jeito certo, com as restrições certas.

---

## O problema que este bloco resolve

Você abre o Claude Code, descreve uma feature e pede para implementar. O código gerado funciona — mas não é o que você queria. Por quê?

Porque a IA tomou dezenas de decisões implícitas no caminho: qual banco usar, como tratar erros, quais campos são obrigatórios, o que retornar em caso de falha. Sem um documento de contexto, ela inventa o que falta.

Este bloco resolve isso em 3 etapas antes de qualquer spec técnico:

```
VOCÊ AINDA NÃO SABE BEM O QUE QUER?
         │
         ▼
   /brainstorm          ← matura a ideia, aponta trade-offs, não implementa nada

VOCÊ SABE O QUE QUER, MAS PRECISA DOCUMENTAR PARA O TIME?
         │
         ▼
   /escrever-prd        ← define O QUE construir (visão de produto)

VOCÊ PRECISA DEFINIR OU REGISTRAR DECISÕES TÉCNICAS GLOBAIS?
         │
         ▼
   /escrever-trd        ← define restrições técnicas que valem para todo o projeto
```

---

## O fluxo completo

```
/brainstorm
     │  matura a ideia, pesquisa, aponta trade-offs
     │  output: docs/brainstorms/YYYY-MM-DD-slug.md (opcional)
     │
     ▼
/escrever-prd
     │  define O QUE construir (problema, user stories, critérios de aceite)
     │  output: docs/prds/NNN-nome.md
     │
     ▼
/escrever-trd   ← escrito UMA VEZ por projeto, não por feature
     │  define restrições técnicas globais (stack, arquitetura, NFRs)
     │  output: docs/trd.md + docs/adrs/ (decisões)
     │
     ▼
spec técnico    ← templates em 03-templates/
     │  define COMO implementar (feature, bugfix, refactor, API)
     │  output: docs/specs/YYYY-MM-DD-tipo-slug.md
     │
     ▼
revisão com IA  ← prompts em 04-ia-no-fluxo/
     │
     ▼
implementação
     │
     ▼
validação
```

---

## Quando usar cada skill

| Situação | Skill |
|----------|-------|
| A ideia ainda não está clara, tem dúvidas sobre a abordagem | `/brainstorm` |
| Precisa documentar uma feature para o time antes de implementar | `/escrever-prd` |
| É o início de um projeto novo sem TRD | `/escrever-trd` |
| Tomou uma decisão técnica importante (banco, auth, padrão) | `/escrever-trd` modo Decisão |
| A ideia já está clara e quer ir direto para o spec técnico | `03-templates/` |
| Bug localizado com causa conhecida | `03-templates/bugfix.md` diretamente |

---

## Skill 1 — `/brainstorm`

### O que é

Modo de maturação de ideias. Pesquisa, analisa criticamente, aponta trade-offs e sugere melhorias **sem criar ou executar nada** até você pedir explicitamente.

### Quando usar

- Antes de qualquer feature, sistema ou refactor ainda não suficientemente especificado
- Quando você tem uma ideia mas não sabe se é a abordagem certa
- Quando quer explorar alternativas antes de se comprometer com uma direção

### Quando NÃO usar

- Bug com causa já identificada (vá direto para `bugfix.md`)
- Feature simples e bem entendida (vá direto para o spec)
- Apenas para documentar algo que já foi decidido

### Como usar

```
/brainstorm

[descreva o que quer explorar — feature, problema, abordagem técnica, etc.]
```

Ou com tema direto:

```
/brainstorm sobre autenticação — estamos pensando em JWT vs session-based, precisamos avaliar os trade-offs para um SaaS multi-tenant
```

### O que você recebe

- Análise crítica da ideia com alternativas
- Trade-offs de cada abordagem
- Premissas implícitas que precisam ser validadas
- Perguntas que um desenvolvedor sênior faria antes de implementar
- Itens pendentes que precisam ser decididos
- Ao final: orientação para o próximo passo (`/escrever-prd` ou `/escrever-trd`)

### Dois modos

| Modo | Quando ativa | Foco |
|------|-------------|------|
| **Generalista** | ideia abstrata, produto, processo | problema, alternativas, premissas |
| **Spec Lens** | feature técnica, sistema, refactor | requisitos de negócio vs. técnicos, stack, versões |

### Exemplo de output (resumido)

```
Analisando: autenticação JWT vs session para SaaS multi-tenant

TRADE-OFFS JWT:
✓ Stateless — sem consulta ao banco por requisição
✓ Funciona bem com múltiplos serviços / microsserviços
✗ Revogação imediata impossível sem denylist (anula o stateless)
✗ Payload viaja em cada requisição — tamanho importa

TRADE-OFFS SESSION:
✓ Revogação imediata simples
✓ Payload no servidor — cliente só carrega ID
✗ Requer Redis ou banco compartilhado para escalar horizontalmente
✗ Acoplamento ao estado do servidor

PREMISSAS A VALIDAR:
[INFERIDO] Você precisa de revogação imediata (ex: logout forçado)?
[INFERIDO] Há plano de microsserviços no futuro?

PRÓXIMO PASSO: /escrever-prd para documentar a decisão ou /escrever-trd para registrar como ADR
```

---

## Skill 2 — `/escrever-prd`

### O que é

Cria o **PRD (Product Requirements Document)** — o documento humano da feature. Captura o problema, a solução de produto, as user stories com regras e casos de borda, os critérios de aceite e as métricas de sucesso.

**O PRD não cobre implementação técnica.** Decisões técnicas vão para o TRD e para os specs.

### Quando usar

- Feature nova com impacto de produto (usuário vai notar)
- Quando o time precisa alinhar O QUE será construído antes de discutir COMO
- Quando há user stories com regras de negócio complexas
- Quando há múltiplos stakeholders que precisam validar antes da implementação

### Quando NÃO usar

- Bugfix (vá para `03-templates/bugfix.md`)
- Refactor interno sem impacto visível para o usuário
- Feature trivial de 1 arquivo e comportamento óbvio

### Como usar

```
/escrever-prd

[descreva a feature ou cole o ticket/issue]
```

### O que você recebe

Arquivo gerado em `docs/prds/NNN-nome-da-feature.md` com:

- **Problema:** o que está errado ou faltando hoje
- **Solução de produto:** o que será construído
- **Escopo:** o que está dentro e fora
- **User Stories** com rules e edge cases
- **Critérios de aceite** verificáveis por teste
- **Métricas de sucesso** com baseline e meta
- **Fluxo de negócio** de ponta a ponta
- **Milestones** com critérios de conclusão

### Comportamento draft-first

O PRD é gerado **imediatamente**, sem perguntas prévias. Informações inferidas são marcadas com `[PREMISSA]` inline para você revisar pontualmente — não precisar responder 10 perguntas antes de ver o documento.

### Status do PRD

| Status | Significado |
|--------|-------------|
| `rascunho` | gerado, ainda não revisado |
| `pronto` | revisado, aprovado para implementar |
| `em-progresso` | implementação em andamento |
| `concluido` | implementado e validado — **imutável** |

### Exemplo de estrutura gerada

```markdown
---
prd_number: 001
title: "Autenticação com JWT"
status: rascunho
depends_on: []
created_at: 2026-10-18
---

# PRD-001: Autenticação com JWT

## 1. Problema
A API atual não tem autenticação. Qualquer cliente pode acessar qualquer endpoint...

## 4. Funcionalidades e User Stories

### US-001-01: Login com email e senha
**Como** usuário cadastrado,
**quero** fazer login com email e senha,
**para que** eu possa acessar recursos protegidos da plataforma.

**Rules:**
- O token gerado expira em 1 hora
- ...

**Edge cases:**
- Email inexistente → mesma mensagem de "credencial inválida" (não revelar existência)
- ...
```

### Como o PRD alimenta o spec técnico

Os **critérios de aceite do PRD** são o ponto de partida direto para a seção **CA** do template `feature.md`:

```
PRD                          →   Spec (feature.md)
US-001-01 critério 1         →   CA1: [mesmo comportamento em linguagem técnica]
US-001-01 edge case email    →   CA2: login com email inexistente retorna 401
```

---

## Skill 3 — `/escrever-trd`

### O que é

Cria o **TRD (Technical Requirements Document)** em `docs/trd.md` — o documento técnico global do projeto. Diferente do PRD (que é por feature), o TRD é **escrito uma vez** e consultado em todos os specs.

Captura: stack com versões, padrão arquitetural, requisitos não-funcionais mensuráveis, dependências externas, padrões de código e decisões globais (ADRs).

### Quando usar

| Situação | Modo |
|----------|------|
| Início de projeto novo sem TRD | Criação |
| Stack ou arquitetura mudou | Edição |
| Decisão técnica importante foi tomada (banco, auth, padrão) | Decisão (ADR) |

### Quando NÃO usar

- Feature específica (use spec em `03-templates/`)
- Decisão local de uma feature (registre no próprio spec)
- Documentar o que é óbvio pelo código (o TRD captura decisões, não o código)

### Como usar

```
/escrever-trd
```

Para registrar uma decisão:

```
/escrever-trd

Decisão: vamos usar PostgreSQL como banco principal — pode registrar como ADR?
```

### O que você recebe

**Modo Criação / Edição:** `docs/trd.md` com 6 seções:

| Seção | O que contém |
|-------|-------------|
| Stack | Linguagem, runtime, framework, banco, ferramentas — com versões |
| Arquitetura | Padrão (MVC, Hexagonal...), estrutura de pastas, módulos principais |
| Requisitos Não-Funcionais | Latência (p95), disponibilidade, escalabilidade, segurança — **com valores mensuráveis** |
| Dependências Externas | APIs de terceiros, SLAs, rate limits, estratégia de fallback |
| Padrões | Testes, formatter, linter, tratamento de erros, logging, autenticação |
| Decisões Globais | Tabela de ADRs com links |

**Modo Decisão:** ADR em `docs/adrs/NNN-titulo.md` + atualização da tabela no TRD.

### Como o TRD alimenta os specs

A seção **Restrições** de cada spec em `03-templates/` **não repete** as restrições técnicas globais — apenas referencia o TRD:

```markdown
## 6. Restrições (no spec feature.md)

- **Performance:** ver TRD seção 3 — meta p95 < 200ms
- **Segurança:** ver TRD seção 3 — OWASP Top 10 mitigado
- **Autenticação:** ver TRD seção 5 — JWT HS256, expiração 1h
```

### O que é um ADR

ADR (Architecture Decision Record) documenta decisões técnicas **duráveis, de amplo impacto e caras de reverter**:

| Vale um ADR | Não vale um ADR |
|-------------|----------------|
| Escolha do banco de dados | Qual biblioteca de datas usar |
| Estratégia de autenticação | Como nomear variáveis |
| Padrão arquitetural (MVC, Clean) | Decisão de uma feature específica |
| Convenção de API (REST, GraphQL) | Ajuste de timeout |

ADRs com status `aceito` são imutáveis — apenas o status pode mudar (`depreciado` / `substituído`).

---

## Exemplo completo do fluxo

### Cenário: construir um sistema de upload de arquivos

**Etapa 1 — Brainstorm**
```
/brainstorm sobre upload de arquivos — precisamos suportar até 50MB,
múltiplos formatos, com preview e armazenamento em nuvem
```
Resultado: análise de S3 vs GCS vs Cloudflare R2, trade-offs de upload direto vs presigned URLs, itens pendentes (CDN? versionamento?)

**Etapa 2 — PRD**
```
/escrever-prd

Feature: upload de arquivos para projetos
- Usuários podem fazer upload de documentos (PDF, DOCX, XLSX) e imagens
- Limite de 50MB por arquivo
- Preview automático para imagens
```
Resultado: `docs/prds/001-upload-arquivos.md` com user stories, edge cases (arquivo corrompido, formato não suportado, usuário sem espaço) e métricas (% de uploads bem-sucedidos)

**Etapa 3 — TRD** (se for o início do projeto)
```
/escrever-trd
```
Resultado: `docs/trd.md` com stack (FastAPI, PostgreSQL, Redis, S3), NFRs (upload de 50MB < 30s, disponibilidade 99.9%) e padrões

**Etapa 4 — Spec técnico**
Usando `03-templates/feature.md` com as seções preenchidas a partir do PRD e TRD:
- Critérios de aceite = CAs do PRD-001
- Restrições = referências ao TRD seções 3 e 5

---

## Estrutura de arquivos gerados

```
docs/
├── brainstorms/
│   └── 2026-10-18-upload-arquivos.md     ← /brainstorm (opcional)
├── prds/
│   └── 001-upload-arquivos.md            ← /escrever-prd
├── trd.md                                 ← /escrever-trd
├── adrs/
│   └── 001-armazenamento-s3.md           ← /escrever-trd modo Decisão
└── specs/
    └── 2026-10-18-feature-upload.md      ← 03-templates/feature.md
```

---

## Exemplos completos de pré-spec

| Arquivo | Cenário | O que demonstra |
|---------|---------|----------------|
| [`exemplo-concessionaria-carros.md`](exemplo-concessionaria-carros.md) | IA para vender mais carros exóticos | Fluxo completo em contexto de negócio real: 4 problemas → brainstorm → PRD → TRD → resposta para o CEO |
