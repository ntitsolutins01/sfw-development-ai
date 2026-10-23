---
name: analyze-issue
description: Analisa uma issue (bug, feature ou task), decompõe em tasks atômicas com critérios de aceite verificáveis e gera stub de spec pronto para o Módulo 2.
disable-model-invocation: false
---

# analyze-issue

Você foi invocado via `/analyze-issue`.

## Passo 1 — Obter o conteúdo da issue

Verifique se o usuário passou um argumento:

- **URL do GitHub** (ex: `/analyze-issue https://github.com/org/repo/issues/123`):
  Execute `gh issue view 123 --repo org/repo` para obter o conteúdo.

- **Caminho de arquivo** (ex: `/analyze-issue docs/issues/issue-123.md`):
  Leia o arquivo informado.

- **Sem argumento:** peça ao usuário para colar o texto da issue diretamente na conversa.

## Passo 2 — Análise inicial

Com o conteúdo da issue, execute:

1. **Classifique o tipo:** Bug | Feature | Task técnica
2. **Identifique o escopo:** o que parece estar dentro e fora
3. **Liste ambiguidades:** cada informação faltante que impede implementação
4. **Formule perguntas de clarificação:** uma pergunta por ambiguidade

Apresente o resultado e pergunte: "Deseja responder as perguntas de clarificação ou devo assumir valores padrão razoáveis?"

## Passo 3 — Decomposição em tasks atômicas

Com as ambiguidades resolvidas, decomponha a issue em tasks:

- Cada task deve ser implementável em isolamento
- Cada task deve ser testável sem depender de outra
- Nomear como: `TASK-N: [verbo] + [objeto]`
- Identificar dependências entre tasks

## Passo 4 — Extração de critérios de aceite

Para cada task, extraia CAs no formato:
`"dado [contexto], quando [ação], então [resultado esperado]"`

Inclua obrigatoriamente:
- 1 CA para o caso feliz
- 1 CA para o caso de falha principal

## Passo 5 — Gerar stub de spec

Gere o arquivo de spec stub no formato do Módulo 2:

```markdown
# Spec — [Título da Issue]

**Tipo:** feature | bugfix | refactor
**Arquivo:** docs/specs/NNN-[slug].md

## Contexto
[1–2 frases: por que esta mudança é necessária]

## Escopo — dentro
[lista do que será implementado]

## Escopo — fora
[lista do que NÃO será implementado]

## Critérios de aceite
- CA-1: [critério]
- CA-2: [critério]
...

## Campos em aberto (para completar no Módulo 2)
- NFRs de performance e segurança
- Dependências técnicas
- Riscos identificados
```

Salve em `docs/specs/NNN-[slug-do-titulo].md` onde `NNN` é o próximo número sequencial disponível.

## Passo 6 — Resumo final

Apresente:
- Tipo da issue
- N tasks identificadas
- N CAs totais
- Caminho do spec stub gerado
- Próximo passo: "Abra o Módulo 2 para completar o spec"