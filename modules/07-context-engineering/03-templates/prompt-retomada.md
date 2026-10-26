# Template — Prompt de Retomada de Sessão

Use no início de cada nova sessão para fazer o seed de contexto a partir do que foi persistido anteriormente.

---

## Template padrão (início de nova sessão)

```
Leia o PROGRESS.md e me coloque em contexto.
Foque na seção "Próxima sessão" da última entrada.
Confirme em 3 linhas:
1. O que foi concluído na última sessão
2. O que está planejado para agora
3. Se há alguma pendência ou decisão aberta que afeta esta sessão
```

---

## Template para retomada após interrupção longa (>1 semana)

```
Leia o PROGRESS.md (última entrada), o CLAUDE.md (status atual) e
o arquivo de memory do projeto.

Me dê um resumo de contexto:
1. O que foi construído até agora (3–5 pontos)
2. Qual é o próximo passo planejado
3. Alguma decisão recente que impacta o trabalho de hoje

Depois confirme: vamos continuar com [tópico esperado]?
```

---

## Template para retomada de tarefa específica (não de módulo)

```
Contexto desta sessão: vamos implementar [feature específica].

Para me colocar em contexto, leia:
- docs/specs/[NNN-nome-do-spec].md (spec da feature)
- [arquivo principal que será modificado]
- [arquivo de testes existente, se houver]

Confirme os CAs do spec antes de começar.
```

---

## Template para continuar trabalho interrompido (mesma semana)

```
Continuando de onde paramos. Contexto:
- Estávamos implementando [função/feature]
- O último estado era: [descreva brevemente o que estava feito]
- O próximo passo era: [o que faltava]

Leia [arquivo relevante] e confirme o estado atual antes de continuar.
```

---

## Exemplo preenchido — retomada do Módulo 7

```
Leia o PROGRESS.md e me coloque em contexto.
Foque na seção "Próxima sessão" da Sessão 9.
Confirme:
1. O que foi entregue no Módulo 6 (Prompt Engineering)
2. O que está planejado para o Módulo 7 (Context Engineering)
3. Se há alguma pendência nos módulos anteriores

Depois disso podemos começar o Módulo 7.
```

---

## Por que o prompt de retomada importa

Sem um prompt de retomada estruturado, o modelo começa a sessão sem saber:
- Em que ponto do projeto você está
- Quais decisões já foram tomadas
- O que está no escopo desta sessão vs o que vem depois

O CLAUDE.md carrega as regras do projeto, mas não o estado atual. O PROGRESS.md tem o estado, mas precisa ser lido explicitamente. O prompt de retomada é o mecanismo que conecta os dois.