# IA no Fluxo de PR Review — 6 Prompts

Cada prompt cobre uma dimensão específica da revisão. Use-os em sequência ou isolados conforme a necessidade.

> **Como usar:** copie o prompt, substitua os `[colchetes]` pelo conteúdo real e envie no Claude Code.

---

## Prompt 1 — Revisão geral do diff

Use quando quiser uma visão completa do que está mudando antes de entrar em detalhes.

```
Revise o seguinte diff de código e identifique problemas em quatro categorias:
bugs, segurança, performance e qualidade.

Para cada problema encontrado, informe:
- Categoria: BUGS | SEGURANÇA | PERFORMANCE | QUALIDADE
- Severidade: CRÍTICO | ALTO | MÉDIO | BAIXO
- Arquivo e linha aproximada
- Descrição do problema
- Sugestão de correção

Diff:
[cole aqui o resultado de: git diff main...HEAD]
```

---

## Prompt 2 — Conformidade com spec (CAs cobertos?)

Use depois do Prompt 1. Verifica se cada critério de aceite do spec está implementado.

```
Compare o diff abaixo com os critérios de aceite do spec.

Para cada CA, responda:
- [x] COBERTO — encontrei implementação no diff
- [ ] AUSENTE — não encontrei implementação
- [~] PARCIAL — implementação existe mas incompleta (explique o que falta)

Ao final, emita uma decisão: APROVADO ou SOLICITAR MUDANÇAS, com justificativa.

Spec (critérios de aceite):
[cole aqui os CAs do arquivo docs/specs/NNN-nome.md]

Diff:
[cole aqui o resultado de: git diff main...HEAD]
```

---

## Prompt 3 — Verificação de cobertura de testes

Use para garantir que cada CA tem teste correspondente.

```
Analise os testes no diff abaixo e verifique se cada critério de aceite está coberto.

Para cada CA, indique:
- O teste que o cobre (nome do método de teste)
- Se cobre o caso feliz e o caso de falha
- Se o teste realmente valida o comportamento (não só a implementação interna)

Se algum CA não tiver teste, classifique como ALTO e sugira o teste que deveria existir.

CAs do spec:
[liste os critérios de aceite]

Diff (incluindo arquivos de teste):
[cole aqui o resultado de: git diff main...HEAD]
```

---

## Prompt 4 — Análise de segurança focada

Use quando a mudança envolve autenticação, autorização, inputs de usuário ou dados sensíveis.

```
Faça uma revisão de segurança focada no diff abaixo.

Verifique especificamente:
1. Validação e sanitização de inputs do usuário
2. Exposição de dados sensíveis em logs ou respostas de API
3. Autenticação e autorização nos novos endpoints
4. Injeção SQL ou injeção de comandos
5. Vulnerabilidades de OWASP Top 10 relevantes para este contexto

Para cada achado: severidade, localização, descrição e correção sugerida.

Contexto da feature: [descreva brevemente o que o código faz]

Diff:
[cole aqui o resultado de: git diff main...HEAD]
```

---

## Prompt 5 — Revisão de performance

Use quando a mudança envolve queries, loops, I/O ou chamadas externas.

```
Analise o diff abaixo buscando problemas de performance.

Verifique:
1. Queries N+1 em loops (ORM ou SQL direto)
2. Operações custosas repetidas que poderiam ser cacheadas
3. Chamadas síncronas bloqueantes que deveriam ser assíncronas
4. Dados carregados em memória que poderiam ser paginados
5. Índices de banco ausentes para novas queries

Para cada achado: severidade, localização, impacto estimado e sugestão.

Contexto: [descreva o volume de dados e frequência de uso esperados]

Diff:
[cole aqui o resultado de: git diff main...HEAD]
```

---

## Prompt 6 — Sumário executivo para decisão final

Use ao final, depois de corrigir os achados das etapas anteriores. Gera o texto de aprovação ou solicitação de mudanças.

```
Com base no histórico de revisão abaixo, gere um sumário executivo para o PR.

O sumário deve conter:
1. O que foi implementado (2–3 linhas)
2. O que foi encontrado e corrigido durante a revisão
3. Pendências abertas (se houver)
4. Decisão final: APROVADO | APROVADO COM RESSALVAS | SOLICITAR MUDANÇAS
5. Justificativa da decisão em uma frase

Histórico de revisão:
[cole os relatórios dos prompts anteriores]

Status dos testes: [pytest passou / falhou — X testes, Y falhas]
```

---

## Snippet para CLAUDE.md do projeto

Adicione ao `CLAUDE.md` do projeto para que a IA saiba que PR review segue este fluxo:

```markdown
## Fluxo de PR Review

Ao revisar código ou PR, sempre seguir esta sequência:
1. Revisão geral (bugs, segurança, performance, qualidade)
2. Conformidade com spec (CAs cobertos?)
3. Cobertura de testes (cada CA tem teste?)
4. Decisão final com justificativa

Severidades: CRÍTICO (bloqueia merge) | ALTO (deve corrigir) | MÉDIO (discutir) | BAIXO (opcional)
Spec fica em: docs/specs/
```