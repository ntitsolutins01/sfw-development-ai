# 04 — IA no Fluxo SDD

Prompts prontos para as etapas de **spec técnico** do ciclo SDD: gerar, revisar, implementar e validar.

> Para as etapas anteriores ao spec técnico (brainstorm, PRD, TRD), use as skills dedicadas:
> - `/brainstorm` — maturar a ideia antes de especificar
> - `/escrever-prd` — documento de produto com user stories e critérios de aceite
> - `/escrever-trd` — restrições técnicas globais do projeto
>
> Documentação completa em `06-pre-spec/README.md`.

---

## Prompt 1 — Gerar spec a partir de um ticket ou issue

Use quando você tem um ticket/issue e quer transformar em um spec estruturado.

```
Você vai me ajudar a escrever um spec de [feature/bugfix/refactor/api-endpoint].

Contexto do ticket:
---
[cole o texto do ticket ou issue aqui]
---

Com base nesse contexto, preencha o template abaixo. Para cada seção, faça as perguntas que um desenvolvedor faria antes de implementar. Se houver informações faltando no ticket, indique com [PENDENTE: descreva o que falta].

Use o template:
- Contexto e motivação
- Escopo (o que está dentro e fora)
- Comportamento esperado (fluxo principal + casos de borda)
- Critérios de aceite verificáveis
- Arquivos impactados
- Restrições

Não implemente nada — apenas estruture o spec.
```

---

## Prompt 2 — Revisar spec antes de implementar

Use depois de escrever o spec, antes de passar para implementação.

```
Revise o spec abaixo como um desenvolvedor sênior que vai implementar este código.

Identifique e liste:
1. **Ambiguidades** — partes que admitem mais de uma interpretação
2. **Gaps** — informações necessárias para implementar que estão faltando
3. **Casos de borda não cobertos** — cenários que os critérios de aceite não contemplam
4. **Conflitos** — requisitos contraditórios entre si ou com padrões conhecidos
5. **Riscos** — decisões técnicas que podem causar problemas futuros

Para cada problema encontrado, sugira como corrigir o spec (não a implementação).
Não implemente nada ainda.

--- SPEC ---
[cole o spec aqui]
```

---

## Prompt 3 — Implementar a partir do spec

Use com o spec já revisado e aprovado.

```
Implemente o que está descrito no spec abaixo.

Regras:
- Siga os critérios de aceite rigorosamente
- Se encontrar ambiguidade durante a implementação, pare e pergunte — não assuma
- Não implemente nada fora do escopo definido
- Mantenha os padrões de código já existentes no projeto

Antes de começar, confirme:
1. Quais arquivos você vai criar ou modificar
2. Se há dependências que precisam ser verificadas

--- SPEC ---
[cole o spec revisado aqui]
```

---

## Prompt 4 — Validar implementação contra o spec

Use depois da implementação para verificar conformidade.

```
Compare a implementação atual com o spec original abaixo.

Para cada critério de aceite, informe:
- ✅ Satisfeito — com breve justificativa
- ❌ Não satisfeito — com o que está faltando
- ⚠️ Parcial — com o que está implementado e o que falta

Ao final, liste qualquer divergência entre o comportamento implementado e o que o spec define, mesmo que não esteja explicitamente em um critério de aceite.

--- SPEC ---
[cole o spec original aqui]
```

---

## Prompt 5 — Gerar casos de teste a partir do spec

Use para gerar testes baseados nos critérios de aceite (complementa o Módulo 3).

```
A partir dos critérios de aceite do spec abaixo, gere casos de teste para [pytest/jest/outro framework].

Para cada critério de aceite:
- Crie pelo menos um teste que verifica o comportamento esperado
- Crie um teste para o caso de falha correspondente
- Use o padrão Arrange / Act / Assert com comentários

Não implemente a feature — apenas os testes.

--- SPEC ---
[cole o spec aqui]
```

---

## Prompt 6 — Gerar spec a partir de código existente

Use para documentar código legado que não tem spec.

```
Analise o código abaixo e gere um spec retroativo descrevendo o comportamento atual.

O spec deve conter:
- O que este código faz (comportamento, não implementação)
- Inputs aceitos e outputs produzidos
- Casos de erro tratados
- Dependências e contratos externos
- Casos de borda identificados

Este spec será usado como linha de base antes de um refactor.

--- CÓDIGO ---
[cole o código aqui]
```

---

## Dica: CLAUDE.md com instruções de SDD

Adicione ao seu `CLAUDE.md` de projeto para que o Claude Code pergunte pelo spec automaticamente:

```markdown
## Regra de Desenvolvimento

Antes de implementar qualquer mudança não trivial (mais de 10 linhas ou mais de 1 arquivo),
pergunte: "Existe um spec para isso em docs/specs/?"

Se não houver spec:
1. Sugira criar um usando os templates em modules/02-spec-driven-development/03-templates/
2. Aguarde o spec antes de implementar
3. Após implementar, valide contra os critérios de aceite do spec
```
