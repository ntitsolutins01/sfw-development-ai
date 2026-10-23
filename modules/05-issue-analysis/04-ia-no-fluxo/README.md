# IA no Fluxo de Issue Analysis — 6 Prompts

Cada prompt cobre uma etapa da análise. Use em sequência para issues complexas ou isolados para necessidades pontuais.

> **Como usar:** copie o prompt, substitua os `[colchetes]` e envie no Claude Code.

---

## Prompt 1 — Análise inicial

Use para entender o tipo, escopo e lacunas de informação da issue antes de qualquer outra etapa.

```
Analise a issue abaixo e responda:

1. **Tipo:** Bug, Feature ou Task técnica? Justifique em uma frase.
2. **Escopo aparente:** o que está dentro e o que parece estar fora?
3. **Ambiguidades:** liste cada informação ambígua ou ausente que impede a implementação.
4. **Perguntas de clarificação:** para cada ambiguidade, formule uma pergunta direta para o autor da issue.
5. **Analisabilidade:** esta issue pode ser decomposta em tasks verificáveis com as informações atuais? Se não, o que falta?

Issue:
[cole aqui o texto completo da issue]
```

---

## Prompt 2 — Decomposição em tasks atômicas

Use após resolver as ambiguidades do Prompt 1.

```
Decomposta a issue abaixo em tasks atômicas e independentes.

Regras para uma task atômica:
- Implementável por uma pessoa em isolamento
- Testável sem depender de outra task
- Escopo claro de início e fim (você sabe quando terminou)
- Pequena o suficiente para um PR separado se necessário

Para cada task, forneça:
- **ID:** TASK-N
- **Título:** verbo + objeto (ex: "Implementar validação de email no login")
- **Escopo:** o que exatamente está dentro desta task
- **Dependências:** de quais outras tasks depende (se houver)

Issue clarificada:
[cole aqui a issue com as ambiguidades resolvidas]
```

---

## Prompt 3 — Extração de critérios de aceite

Use após o Prompt 2 para detalhar cada task com CAs verificáveis.

```
Para cada task abaixo, extraia os critérios de aceite no formato:
"dado [contexto], quando [ação], então [resultado esperado]"

Regras para um bom CA:
- Verificável: sim ou não, sem interpretação
- Específico: inclui valores concretos (status code, mensagem, campo, comportamento)
- Independente: pode ser verificado sem executar outro CA antes

Inclua ao menos:
- 1 CA para o caso feliz (fluxo principal funcionando)
- 1 CA para o caso de falha (o que acontece quando algo está errado)

Tasks:
[cole aqui as tasks do Prompt 2]
```

---

## Prompt 4 — Priorização por impacto vs esforço

Use quando houver múltiplas tasks e for necessário decidir a ordem de implementação.

```
Avalie as tasks abaixo em duas dimensões:

**Impacto** (1–5): quanto valor entrega para o usuário ou sistema
- 5: bloqueia funcionalidade crítica ou entrega valor imediato alto
- 3: melhoria relevante mas não urgente
- 1: refinamento menor, baixo impacto direto

**Esforço** (1–5): complexidade estimada de implementação
- 5: mudanças em múltiplos sistemas, alto risco de regressão
- 3: implementação moderada, impacto localizado
- 1: mudança pontual, baixo risco

Calcule Prioridade = Impacto / Esforço e ordene as tasks.

Tasks:
[cole aqui as tasks com CAs do Prompt 3]

Contexto adicional (se houver):
[prazo, restrições técnicas, dependências externas]
```

---

## Prompt 5 — Estimativa de complexidade

Use para estimar esforço relativo entre as tasks (story points ou t-shirt).

```
Estime a complexidade relativa das tasks abaixo usando t-shirt sizing:
- **XS**: mudança pontual, < 2h, risco baixo
- **S**: implementação simples, 2–4h, bem compreendida
- **M**: implementação moderada, 4–8h, algumas incertezas
- **L**: implementação complexa, 1–2 dias, dependências ou riscos
- **XL**: implementação muito complexa ou com muitas incertezas — deve ser decomposta mais

Para cada task:
- Tamanho estimado
- Principal fator de incerteza (o que pode torná-la maior)
- Sugestão de decomposição adicional se > M

Tasks:
[cole aqui as tasks com CAs do Prompt 3]
```

---

## Prompt 6 — Geração de spec stub

Use ao final da análise para gerar o esqueleto do spec pronto para o Módulo 2.

```
Com base na análise completa da issue abaixo, gere um stub de spec no formato do Módulo 2.

O stub deve conter:
- **Título:** nome descritivo da feature/bugfix
- **Contexto:** por que esta mudança é necessária (1–2 frases)
- **Tipo:** feature | bugfix | refactor
- **Escopo — dentro:** lista do que será implementado
- **Escopo — fora:** lista do que NÃO será implementado
- **Critérios de aceite:** todos os CAs extraídos, numerados como CA-N
- **Campos em aberto:** NFRs, dependências e riscos a preencher no Módulo 2

O arquivo deve ser salvo em: docs/specs/NNN-[slug-do-titulo].md

Issue original:
[cole aqui a issue]

Tasks e CAs extraídos:
[cole aqui o resultado dos Prompts 2 e 3]
```

---

## Snippet para CLAUDE.md do projeto

Adicione ao `CLAUDE.md` do projeto para que a IA saiba que issues passam por análise antes do spec:

```markdown
## Fluxo de Issue Analysis

Antes de criar um spec (Módulo 2), toda issue passa por análise:
1. Classificar tipo (bug / feature / task)
2. Identificar ambiguidades e resolver
3. Decompor em tasks atômicas
4. Extrair CAs verificáveis por task
5. Gerar stub de spec em docs/specs/

Issues são registradas em: [GitHub Issues / Jira / Linear — ajuste conforme o projeto]
Spec fica em: docs/specs/
```