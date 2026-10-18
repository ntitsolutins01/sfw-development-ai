# Exemplo Pré-Spec — Concessionária de Carros Exóticos com IA

> **Cenário:** Dana, CEO de uma concessionária de carros clássicos e exóticos de alto padrão,
> quer usar IA para vender mais. As vendas acontecem no pátio, em leilões ou em entregas —
> os dados estão espalhados entre HubSpot e um sistema interno de estoque.
>
> Este exemplo mostra como o fluxo `/brainstorm → /escrever-prd → /escrever-trd`
> transforma esse problema em algo implementável.

---

## Contexto do negócio (primeira ligação com Dana)

Dana descreve quatro problemas:

1. **Reps odeiam atualizar o HubSpot.** Ficam no pátio, em leilões ou fazendo entregas — o CRM fica desatualizado.
2. **HubSpot e sistema de estoque não se falam.** Leads e conversas estão no HubSpot; cada carro vendido e para quem está no sistema da concessionária. Nenhum dos dois vê o outro.
3. **Não conseguem separar compradores reais de curiosos.** Recebem bastante lead inbound mas não têm como priorizar.
4. **Quando chega um carro raro, não sabem quem ligar.** Não há processo para notificar os prospects certos.

---

## Etapa 1 — `/brainstorm sobre concessionária de carros exóticos e IA`

O que a skill `/brainstorm` faz neste cenário:
- Decompõe os 4 problemas em oportunidades técnicas
- Mapeia o que é possível imediatamente vs. o que requer dados históricos
- Aponta dependências entre as soluções
- Recomenda por onde começar (sem implementar nada)

### Output simulado do brainstorm

```markdown
# Brainstorm — IA para Concessionária de Carros Exóticos
Data: 2026-10-18

## Decomposição dos problemas

### Problema 1: CRM desatualizado
Causa raiz: fricção no processo de atualização — reps em campo não têm fluxo adequado.
Oportunidades técnicas:
- Captura automática via integração (ligações, e-mails → HubSpot sem input manual)
- App mobile de atualização rápida com campos pré-preenchidos por IA
- [PREMISSA] HubSpot tem API para criar/atualizar negócios programaticamente

### Problema 2: Dados isolados (HubSpot ↔ sistema de estoque)
Causa raiz: dois sistemas sem integração bidirecional.
Oportunidades técnicas:
- Camada de integração que sincroniza negócios fechados (estoque → HubSpot)
- Enriquecimento de contato com histórico de compras (HubSpot ← estoque)
- [PREMISSA] Sistema de estoque tem API ou exportação regular de dados

### Problema 3: Qualificação de leads
Causa raiz: sem dados históricos de comportamento de compra, toda qualificação é manual.
Oportunidades técnicas:
- Score de propensão baseado em: fonte do lead, engajamento no CRM, histórico de compras,
  faixa de preço dos interesses declarados
- Classificação automática: Hot / Warm / Cold visível no HubSpot
- [PREMISSA] Requer 6-12 meses de dados históricos para treinar um modelo confiável;
  no início, regras heurísticas são suficientes

### Problema 4: Matching de carro raro com prospect certo
Causa raiz: sem integração e sem score, o conhecimento vive na cabeça dos reps.
Oportunidades técnicas:
- Quando carro novo chega no estoque: sistema cruza especificações com perfil de leads
  (modelos anteriores comprados, faixa de preço, marcas de interesse)
- Notificação automática para rep com lista ranqueada: "Top 5 contatos para ligar sobre este Ferrari"
- [PREMISSA] Perfis de interesse precisam ser estruturados no HubSpot (campo customizado)

## Trade-offs

| Abordagem | Prós | Contras |
|-----------|------|---------|
| Integração direta HubSpot ↔ estoque via API | Dados em tempo real | Depende da API do sistema de estoque |
| ETL batch (exportação diária) | Funciona mesmo sem API REST | Dados com atraso de até 24h |
| ML para scoring | Alta precisão com dados históricos | Precisa de 6-12 meses de dados; custo de treinamento |
| Regras heurísticas para scoring | Funciona imediatamente | Menos preciso; requer ajuste manual |

## Dependências entre as soluções

```
Integração (Problema 2)
    ↓ viabiliza
Scoring de leads (Problema 3)
    ↓ viabiliza
Matching de carro raro (Problema 4)
```

O Problema 1 (CRM desatualizado) pode ser atacado em paralelo — não bloqueia as demais.

## Onde começar — recomendação

**Fase 1 (semanas 1-4):** Integração HubSpot ↔ sistema de estoque
Motivo: é a fundação de tudo. Sem dados históricos de compra nos perfis, scoring
e matching são impossíveis.

**Fase 2 (semanas 5-8):** Score de propensão com regras heurísticas
Motivo: regras simples (lead de indicação > lead de formulário web; comprou > R$ 500k antes >
comprou < R$ 100k) já geram valor sem ML.

**Fase 3 (meses 3+):** Matching automático + notificação para reps
Motivo: após dados históricos acumulados, o matching fica preciso.

## O que os reps usariam na prática

- View "Hot Leads" no HubSpot com score visível — sem sair da ferramenta atual
- Push notification: "Ferrari 458 chegou — 3 contatos no perfil deste modelo"
- Briefing automático antes da ligação: histórico de compras + modelos de interesse

## Próximo passo sugerido

→ `/escrever-prd` para a Fase 1: Integração HubSpot ↔ Sistema de Estoque
```

---

## Etapa 2 — `/escrever-prd` para a Fase 1

O brainstorm definiu que a Fase 1 (integração) é a fundação. Agora documentamos O QUE construir.

### Output simulado do PRD

```markdown
---
prd_number: "001"
title: "Integração HubSpot ↔ Sistema de Estoque"
status: rascunho
depends_on: null
created_at: 2026-10-18
---

# PRD 001 — Integração HubSpot ↔ Sistema de Estoque

## 1. Contexto

**Problema:** Leads e conversas vivem no HubSpot; histórico de compras e estoque vivem no
sistema da concessionária. Os reps tomam decisões sem visibilidade do histórico de compras
dos contatos, e o sistema de estoque não sabe quem é o comprador além do nome no contrato.

**Por que agora:** A Fase 2 (scoring) e Fase 3 (matching) dependem dessa integração.
Sem ela, não há dado para alimentar os algoritmos de priorização.

## 2. Usuários

| Perfil | Necessidade |
|--------|-------------|
| Rep de vendas | Ver histórico de compras do contato no HubSpot antes de ligar |
| Gerente de vendas | Relatório de lifetime value por contato |
| Sistema de scoring (Fase 2) | Histórico de compras como feature do modelo |

## 3. User Stories

**US-01:** Como rep de vendas, quando abro um contato no HubSpot, quero ver os carros que ele
já comprou da concessionária, para personalizar minha abordagem.

**US-02:** Como gerente, quero que negócios fechados no sistema de estoque apareçam
automaticamente no HubSpot como atividades, para ter o histórico completo sem entrada manual.

**US-03:** Como rep, quando um negócio é fechado no HubSpot, quero que o cliente seja
vinculado automaticamente ao registro de venda no sistema de estoque.

## 4. Regras de Negócio

- RN-01: Sincronização HubSpot → Estoque: ao fechar um negócio no HubSpot, criar/atualizar
  registro do comprador no sistema de estoque com o ID do contato HubSpot
- RN-02: Sincronização Estoque → HubSpot: ao registrar uma venda no estoque, criar atividade
  no contato HubSpot correspondente com: modelo, ano, preço, data
- RN-03: Vinculação por e-mail como chave primária; se e-mail não existir no HubSpot,
  criar contato automaticamente
- RN-04: Conflito de dados: se dois registros tiverem o mesmo e-mail, notificar admin
  ao invés de mesclar automaticamente

## 5. Critérios de Aceite

- [ ] Rep abre contato no HubSpot e vê aba "Histórico de Compras" com lista de carros adquiridos
- [ ] Ao fechar negócio no sistema de estoque, atividade aparece no HubSpot em < 5 minutos
- [ ] Ao fechar negócio no HubSpot, comprador vinculado no sistema de estoque em < 5 minutos
- [ ] Conflito de e-mail gera notificação no Slack para o admin, sem mesclar registros
- [ ] Sincronização funciona mesmo quando um dos sistemas está temporariamente indisponível
  (retry com backoff exponencial, máximo 3 tentativas)

## 6. Fora do Escopo (Fase 1)

- Score de propensão de leads (Fase 2)
- Matching de carro com prospect (Fase 3)
- App mobile para atualização de CRM (backlog)
- Sincronização de estoque disponível (apenas vendas fechadas)

## 7. Métricas de Sucesso

- % de contatos no HubSpot com histórico de compras preenchido: meta > 90% em 30 dias
- Tempo entre venda no estoque e atividade no HubSpot: meta < 5 minutos p95
- Zero merges automáticos incorretos de contatos (conflitos tratados manualmente)
```

---

## Etapa 3 — `/escrever-trd` para decisões técnicas globais

O TRD é escrito uma vez e cobre restrições que valem para todas as fases do projeto.

### Output simulado do TRD (excerto relevante)

```markdown
# TRD — Sistema de IA para Concessionária

## 1. Stack

| Camada | Tecnologia | Decisão |
|--------|-----------|---------|
| Backend | Python 3.12 + FastAPI | ADR-001 |
| Banco intermediário | PostgreSQL 16 | — |
| Fila de mensagens | Redis + RQ (worker) | ADR-002 |
| Integração HubSpot | HubSpot API v3 (REST) | — |
| Deploy | Docker + Railway | — |

## 2. Arquitetura de Integração

```
HubSpot (webhook) → FastAPI → Fila Redis → Worker → Sistema de Estoque (API)
Sistema de Estoque (webhook/batch) → FastAPI → Fila Redis → Worker → HubSpot API
```

Decisão: fila de mensagens como buffer entre os dois sistemas. Motivo: absorve
picos de carga e garante retry em caso de indisponibilidade (RN-04 do PRD-001).

## 3. NFRs (Non-Functional Requirements)

| Requisito | Meta |
|-----------|------|
| Latência de sincronização | < 5 min p95 (SLA do PRD-001) |
| Disponibilidade | 99.5% (exceto janela de manutenção domingo 2-4h) |
| Retenção de dados | 5 anos (regulação de vendas) |
| Acesso à API | Apenas IPs da concessionária (allowlist) |

## 4. ADRs

### ADR-001 — Python + FastAPI como backend
**Status:** aceito
**Contexto:** Time tem experiência em Python. Integração com bibliotecas de ML para Fase 2.
**Decisão:** FastAPI por performance assíncrona e geração automática de docs OpenAPI.
**Consequências:** Runtime Python necessário no servidor; não usar Node para consistência.

### ADR-002 — Redis + RQ como fila de mensagens
**Status:** aceito
**Contexto:** Volume estimado: < 100 sincronizações/dia. Kafka seria overkill.
**Decisão:** Redis + RQ: operação simples, zero custo adicional de infraestrutura.
**Consequências:** Fila não é durável por padrão — configurar `persist=True` no RQ.
  Se volume escalar para > 10k/dia, reavaliar para SQS ou RabbitMQ.
```

---

## O que este exemplo demonstra

| Etapa | O que a skill fez | Output |
|-------|-----------------|--------|
| `/brainstorm` | Decomposição dos 4 problemas, trade-offs, dependências, recomendação de fase | `docs/brainstorms/2026-10-18-concessionaria-ia.md` |
| `/escrever-prd` | Documentou O QUE construir na Fase 1 com user stories, regras e CAs verificáveis | `docs/prds/001-integracao-hubspot-estoque.md` |
| `/escrever-trd` | Definiu stack, arquitetura de integração, NFRs e ADRs que valem para todo o projeto | `docs/trd.md` |

Após as três etapas, o spec técnico (Fase 1) pode ser escrito em `docs/specs/` usando os
critérios de aceite do PRD como base — e os testes TDD (Módulo 3) podem ser gerados
diretamente dos CAs.

---

## Resposta para Dana na primeira ligação

> Assumindo que o sistema de estoque tem exportação regular de dados (batch diário ou API).

Dana, por onde eu começaria: **a integração entre o HubSpot e o sistema de estoque é
a fundação de tudo**. Sem ela, os outros problemas não têm solução escalável — os reps
não podem priorizar leads que não têm histórico visível, e o sistema não pode recomendar
quem ligar quando um Ferrari chega no pátio.

O que eu construiria em três fases:

**Fase 1 (4 semanas) — Integração:** sincronização bidirecional entre HubSpot e o sistema
de estoque. Quando uma venda fechar em qualquer dos dois lados, o outro atualiza em menos
de 5 minutos. O rep abre o contato no HubSpot e vê todos os carros que aquela pessoa já
comprou da concessionária.

**Fase 2 (4 semanas) — Scoring:** com o histórico de compras disponível, aplico regras de
priorização: lead de indicação pontua mais que lead de formulário; alguém que comprou um
carro acima de R$ 500k tem perfil diferente de quem comprou R$ 80k; tempo sem contato
penaliza o score. Resultado: view "Hot Leads" no HubSpot com ranking visível — os reps
não precisam aprender nenhuma ferramenta nova.

**Fase 3 (ongoing) — Matching:** quando um carro raro chega no estoque, o sistema cruza
as especificações (marca, modelo, faixa de preço, ano) com os perfis dos leads e gera
uma lista: "Top 5 contatos para ligar sobre este carro". O rep recebe uma notificação
com o briefing já pronto — histórico de compras + modelos de interesse + último contato.

O que os reps usariam: a mesma interface do HubSpot que já usam, com um score visível
e uma notificação quando um carro do perfil de um cliente chega. Zero nova ferramenta.
