---
name: escrever-trd
description: Cria e mantém o TRD (Technical Requirements Document) em docs/trd.md — documento técnico global do projeto com stack, arquitetura, requisitos não-funcionais, dependências externas, padrões e decisões. Escrito uma vez por projeto, consultado em cada spec.
disable-model-invocation: false
---

# escrever-trd

## Objetivo
Criar e manter o **TRD (Technical Requirements Document)** em `docs/trd.md` — o documento técnico global do projeto. Diferente do PRD (por feature) e do spec (por implementação), o TRD é escrito **uma vez por projeto** e captura o que vale para tudo: stack, arquitetura, requisitos não-funcionais, dependências externas, padrões e decisões arquiteturais (ADRs).

## Quando usar

| Situação | Modo |
|----------|------|
| Início de projeto novo | Criação |
| Stack, arquitetura ou padrões mudaram | Edição |
| Uma decisão técnica importante foi tomada | Decisão (ADR) |

## Quando NÃO usar
- Feature específica (use `03-templates/feature.md`)
- Decisão local de uma feature (registre no próprio spec, não no TRD)
- Documentar o que é óbvio pelo código (o TRD captura decisões, não código)

## O que ela faz

**Modo Criação (5 etapas):**
1. Analisa automaticamente o projeto: linguagem, frameworks, banco, estrutura de pastas
2. Faz mini-entrevista (máximo 5 perguntas) apenas sobre o que não pode inferir
3. Gera o TRD completo com 6 seções
4. Escaneia `docs/adrs/` para registrar ADRs existentes
5. Salva em `docs/trd.md`

**Modo Edição:**
- Re-analisa o projeto, identifica divergências com o TRD existente
- Entrevista apenas sobre o delta (não repete perguntas já respondidas)
- Atualiza as seções relevantes

**Modo Decisão (ADR):**
- Gera ADR em `docs/adrs/NNN-titulo.md`
- Atualiza a tabela de Decisões Globais no `docs/trd.md`

## O que ela NÃO faz
- Não cobre features específicas (escopo do PRD e dos specs)
- Não cria ADRs fora do Modo Decisão
- Não altera ADRs com status `aceito` — apenas o campo `status` pode mudar
- Não infere requisitos não-funcionais sem perguntar (SLAs precisam de valores reais)

## As 6 seções do TRD

| Seção | Conteúdo |
|-------|----------|
| **Stack** | Linguagem, runtime, framework, banco, ferramentas — com versões |
| **Arquitetura** | Padrão (MVC, Clean, Hexagonal), estrutura de pastas, módulos principais |
| **Requisitos Não-Funcionais** | Latência (p95), disponibilidade, escalabilidade, segurança — com valores mensuráveis |
| **Dependências Externas** | APIs de terceiros, SLAs, rate limits, estratégia de fallback |
| **Padrões** | Testes, formatter, linter, erros, logging, autenticação |
| **Decisões Globais** | Tabela de ADRs com links para `docs/adrs/` |

## Como o TRD alimenta os specs
A seção **Restrições** de cada spec em `03-templates/` referencia o TRD em vez de repetir as restrições globais:

```markdown
## 6. Restrições (no spec feature.md)
- Performance: ver TRD seção 3 — meta p95 < 200ms
- Autenticação: ver TRD seção 5 — JWT HS256, expiração 1h
```

## O que é um ADR e quando criar
ADR (Architecture Decision Record) documenta decisões **duráveis, de amplo impacto e caras de reverter**.

| Vale um ADR | Não vale um ADR |
|-------------|----------------|
| Escolha do banco de dados | Qual biblioteca de datas usar |
| Estratégia de autenticação | Decisão de uma feature específica |
| Padrão arquitetural (MVC, Clean) | Ajuste de timeout |
| Convenção de API (REST, GraphQL) | Nomeação de variável |

## Argumentos aceitos
- `/escrever-trd` — detecta modo automaticamente (criação, edição ou decisão)
- `/escrever-trd` + descrição de decisão — ativa Modo Decisão diretamente

## Exemplo de uso

**Criação:**
```
/escrever-trd
```

**Registrar decisão:**
```
/escrever-trd

Decidimos usar PostgreSQL como banco principal — pode registrar como ADR?
Alternativas consideradas: MySQL (descartado por falta de suporte a JSONB) e MongoDB (descartado por modelo relacional do domínio).
```

Saída esperada (resumida):
```
Analisando projeto...
Encontrei: Python 3.11, FastAPI, Poetry, pytest

Mini-entrevista (3 perguntas):
1. Qual a meta de latência (p95) para os endpoints principais?
2. Qual SLA de disponibilidade esperado?
3. Haverá autenticação via JWT ou outro mecanismo?

[após respostas]

docs/trd.md criado.
docs/adrs/001-banco-postgresql.md criado.

PRÓXIMO PASSO:
→ spec técnico  a seção Restrições de cada spec deve referenciar o TRD
                (modules/02-spec-driven-development/03-templates/)
```

---

## Instruções operacionais

### Passo 1 — Detectar modo

- `docs/trd.md` não existe → **Modo Criação**
- `docs/trd.md` existe + usuário quer atualizar → **Modo Edição**
- Usuário quer registrar decisão arquitetural → **Modo Decisão**

### Modo Criação

**Etapa 1 — Análise automática:** leia `package.json`, `requirements.txt`, `pyproject.toml`, migrations, estrutura de pastas para inferir linguagem, framework, banco, ferramentas de teste.

**Etapa 2 — Mini-entrevista:** máximo 5 perguntas. Pergunte apenas o que não pode ser inferido. Nunca pergunte o que já foi inferido na etapa anterior.

**Etapa 3 — Gerar TRD:** escreva `docs/trd.md` com as 6 seções. Use valores mensuráveis nos NFRs — nunca "deve ser rápido", sempre "p95 < 200ms a 100 req/s".

**Estrutura do `docs/trd.md`:**
```markdown
# TRD — Technical Requirements Document
> Atualizado em: YYYY-MM-DD | Versão: 1.0

## 1. Stack
| Componente | Tecnologia | Versão | Notas |

## 2. Arquitetura
Padrão: [padrão]
Estrutura de pastas: [árvore]
Módulos principais: [tabela]

## 3. Requisitos Não-Funcionais
| Requisito | Meta | Condição |

## 4. Dependências Externas
| Serviço | Propósito | SLA / Rate limit | Fallback |

## 5. Padrões
Testes, estilo, erros, logging, autenticação

## 6. Decisões Globais (ADRs)
| # | Título | Data | Status | Arquivo |
```

### Modo Edição

Re-analise o projeto. Identifique divergências com o TRD existente. Entreviste apenas sobre o delta. Atualize versão e data.

### Modo Decisão (ADR)

**Estrutura do ADR** em `docs/adrs/NNN-titulo-em-kebab-case.md`:
```markdown
# ADR-NNN: [Título]
> Data: YYYY-MM-DD | Status: proposto | aceito | depreciado | substituído por ADR-NNN

## Contexto
## Decisão
## Consequências (positivas / trade-offs)
## Alternativas consideradas
| Alternativa | Por que descartada |
```

ADRs `aceito` são imutáveis — apenas o campo `status` pode mudar.

Após criar o ADR, atualize a tabela da seção 6 do `docs/trd.md`.

### Passo final — Orientar

```
PRÓXIMO PASSO:
→ spec técnico  a seção Restrições de cada spec referencia o TRD
                (modules/02-spec-driven-development/03-templates/)
```
