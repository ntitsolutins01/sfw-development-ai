# Workflow — Ciclo de Gestão de Contexto

## O Ciclo Completo

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Seed    │ ──► │ Trabalho │ ──► │ Compactar│ ──► │ Persistir│ ──► │ Retomar  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
                      ▲                                                    │
                      └────────────────────────────────────────────────────┘
```

---

## Fase 1 — Seed

O início de qualquer sessão de trabalho. O objetivo é colocar no contexto exatamente o que será necessário — nem mais, nem menos.

**Para sessão nova em projeto conhecido:**
```
Leia o PROGRESS.md e me coloque em contexto. Vamos continuar o [módulo X].
```

**Para sessão nova em projeto desconhecido:**
```
Leia o README.md, o CLAUDE.md e os últimos 3 commits. Me diga:
1. O que este projeto faz
2. Qual é o estado atual
3. Quais são as convenções de código
```

**Para tarefa específica:**
```
Para esta sessão, vamos implementar apenas [feature Y].
Contexto necessário: [arquivo A], [spec B], [teste C].
Não é necessário carregar mais nada além disso.
```

**O que um bom seed inclui:**
- O objetivo da sessão (uma frase)
- Os arquivos diretamente relevantes (não "tudo")
- As decisões que afetam a tarefa
- O que NÃO precisa ser feito nesta sessão

---

## Fase 2 — Trabalho

Durante a sessão, o contexto cresce organicamente. Você não precisa gerenciar manualmente — mas precisa notar quando começa a haver ruído.

**Sinais de que o contexto está ficando grande demais:**
- Respostas começam a ignorar instruções do início da conversa
- O modelo "esquece" uma decisão que foi tomada 20 trocas atrás
- Latência visivelmente maior entre respostas
- Você está tendo que repetir contexto que já foi dado

Quando notar qualquer um desses sinais, é hora de compactar.

---

## Fase 3 — Compactar

O `/compact` no Claude Code sumariza a conversa atual, preservando as informações essenciais e descartando o ruído (logs de ferramentas, respostas intermediárias, tentativas descartadas).

**Quando usar:**
- Após completar uma subtarefa dentro de uma sessão longa
- Quando o contexto tem muita saída de ferramentas (leituras de arquivo, git diffs)
- Antes de iniciar uma nova subtarefa diferente na mesma sessão

**O que `/compact` preserva:**
- Decisões tomadas
- Código implementado
- Erros encontrados e como foram resolvidos
- O objetivo atual da sessão

**O que `/compact` descarta:**
- Outputs de ferramentas já processados
- Tentativas intermediárias descartadas
- Discussões resolvidas
- Logs repetitivos

**Alternativa ao `/compact`:** abra uma nova sessão com seed específico para a próxima subtarefa. Às vezes é mais limpo do que compactar uma sessão grande.

---

## Fase 4 — Persistir

Ao final de cada sessão ou ao concluir um módulo, atualize os 3 mecanismos de persistência:

| Mecanismo | O que persistir | Quando |
|-----------|----------------|--------|
| **Memory** (`project-aiad.md`) | Decisões, estrutura criada, convenções estabelecidas | Ao concluir um módulo ou tomar decisão importante |
| **CLAUDE.md** | Status dos módulos, regras que mudam | Quando o status do projeto muda |
| **PROGRESS.md** | O que foi feito, o que falta, próxima sessão | Ao final de cada sessão |

No AIAD, este processo é automatizado pela skill `/salvar-contexto`.

---

## Fase 5 — Retomar

O início da próxima sessão. Um bom retorno não exige que o modelo "lembre" — exige que o contexto certo seja carregado.

**Prompt padrão de retomada:**
```
Leia o PROGRESS.md e me coloque em contexto. Foque na seção "Próxima sessão"
da última entrada. Confirme o que estava planejado antes de começar.
```

**Retomada após interrupção longa (>1 semana):**
```
Leia o PROGRESS.md (última sessão), o CLAUDE.md (status atual) e
a memory do projeto. Me dê um resumo de 3 linhas do estado atual
e o que foi decidido recentemente antes de continuarmos.
```

---

## Estratégia por Tipo de Tarefa

| Tipo de tarefa | Estratégia recomendada |
|----------------|----------------------|
| **Feature completa (1 sessão)** | Seed com spec + testes. Compactar após a implementação. Persistir ao final. |
| **Feature longa (múltiplas sessões)** | Seed mínimo por sessão. Persistir ao final de cada subtarefa. Retomar com PROGRESS.md. |
| **Bug fix pontual** | Seed com arquivo + erro. Nenhuma compactação necessária (sessão curta). |
| **Revisão de código** | Fresh agent com diff + spec. Resultado independente sem poluir a sessão principal. |
| **Pesquisa / exploração** | Fork agent. O ruído da exploração não entra na sessão principal. |
| **Refatoração de módulo** | Seed com interface pública + testes. Compactar entre subtarefas. |