---
name: salvar-contexto
description: Salva o contexto da sessão de trabalho nos 3 mecanismos do projeto (memory, CLAUDE.md, PROGRESS.md). Invoque quando quiser registrar progresso, uma pausa, uma decisão importante ou encerrar a sessão.
disable-model-invocation: false
---

# salvar-contexto

Você foi invocado via `/salvar-contexto`.

## Passo 1 — Apresentar menu de seleção

Use a ferramenta `AskUserQuestion` para apresentar as opções abaixo como
seleção interativa — **não liste como texto simples**, renderize o menu.

Pergunta: "O que deseja registrar agora?"

Opções:

| # | Label | Descrição |
|---|-------|-----------|
| 1 | Módulo concluído | Um módulo foi finalizado. Atualiza os 3 mecanismos: memory (detalhes completos), CLAUDE.md (status ✅) e PROGRESS.md (nova entrada de sessão). |
| 2 | Pausa — em andamento | Interrupção temporária, nada concluído ainda. Atualiza só o PROGRESS.md com o que foi feito e o que falta. Memory e CLAUDE.md ficam intocados. |
| 3 | Decisão importante | Uma decisão arquitetural ou de design foi tomada. Salva na memory (decisão + porquê) e adiciona ao PROGRESS.md da sessão atual. |
| 4 | Fim de sessão | Encerramento completo. Atualiza os 3 mecanismos com resumo da sessão e seção "Próxima sessão". |

---

## Passo 2 — Executar conforme seleção

### Opção 1 — Módulo concluído

1. Leia o estado atual:
   - `PROGRESS.md` (sessão em andamento)- `~/.claude/projects/C--Projetos-POCs-sfw-development-ai/memory/project-aiad.md`
   - `CLAUDE.md` (tabela de status)

2. **Atualize a memory** (`project-aiad.md`):
   - Marque o módulo como `[x]` na lista de status
   - Adicione em "O que foi criado": estrutura de arquivos, decisões tomadas
   - Marque o próximo módulo como "PRÓXIMO"

3. **Atualize o `CLAUDE.md`**:
   - Mude o módulo de `⏳ Próximo` para `✅ Concluído`
   - Marque o seguinte como `⏳ Próximo`
   - Atualize a data no campo `> Atualizado em:`

4. **Atualize o `README.md`** (raiz do projeto):
   - Na tabela `## 📚 Módulos`: mude o status do módulo de `—` para `✅ Concluído` e adicione o link para a pasta (`[Nome](modules/XX-nome/)`)
   - Na seção `## 🗺️ Progresso`: mude `—  Módulo X` para `✅ Módulo X`
   - No rodapé: atualize o contador `Módulos concluídos: N/15`
   - Na seção `## 🔄 Executando o Projeto Completo (E2E)` → tabela "Passos detalhados":
     - Substitua `*(em breve)*` pelo link `[📖 Como executar](docs/guia-e2e.md#módulo-X--nome)`

5a. **Atualize o `docs/guia-e2e.md`**:
   - Localize a seção `## Modulo X: Nome` correspondente (precedida por `<a id="modulo-X"></a>`)
   - Substitua o bloco `*(em breve)*` pelo guia completo do módulo, seguindo a estrutura dos módulos 1–3:
     - **Objetivo:** uma linha descrevendo o que o módulo entrega
     - **O que você vai fazer:** passos numerados com comandos, arquivos a copiar e prompts a usar
     - **O que valida a conclusão:** checklist com critérios objetivos (sim/não)
     - Linha de referência — use exatamente este formato (o texto "Referência completa" é o link, sem texto extra):
       ```
       **[Referência completa](../modules/XX-nome/README.md)**
       ```

5. **Atualize o `PROGRESS.md`**:
   - Adicione nova entrada `## Sessão N — YYYY-MM-DD`
   - Seções: "O que foi feito", "Decisões tomadas", "Próxima sessão"
   - Numere a sessão corretamente (leia as entradas anteriores)

---

### Opção 2 — Pausa / em andamento

1. Leia o `PROGRESS.md` atual.

2. **Atualize apenas o `PROGRESS.md`**:
   - Localize a sessão em andamento (a mais recente sem "Próxima sessão")
   - Adicione uma subseção `### Estado atual (pausa)`
   - Liste o que foi feito até agora
   - Liste o que falta concluir para fechar o módulo

3. Não altere memory nem CLAUDE.md — nada foi concluído.

---

### Opção 3 — Decisão importante

1. Use `AskUserQuestion` para perguntar:
   **"Descreva a decisão tomada:"** (campo de texto livre)

2. **Atualize a memory** (`project-aiad.md`):
   - Adicione a decisão em `## Decisões tomadas nesta sessão`
   - Formato: `- [data] Decisão: X. Motivo: Y.`

3. **Atualize o `PROGRESS.md`**:
   - Localize a sessão atual
   - Adicione subseção `### Decisão registrada`
   - Registre a decisão com contexto

4. Não altere CLAUDE.md — status de módulo não mudou.

---

### Opção 4 — Fim de sessão

1. Leia o estado atual dos 3 mecanismos.

2. **Atualize a memory** (`project-aiad.md`):
   - Adicione tudo que foi criado ou decidido na sessão
   - Atualize o status dos módulos
   - Atualize "Convenção de Sessão" se necessário

3. **Atualize o `CLAUDE.md`**:
   - Reflita qualquer mudança de status de módulo
   - Atualize a data

4. **Atualize o `PROGRESS.md`**:
   - Complete a sessão atual com resumo detalhado
   - Adicione seção `### Próxima sessão` com:
     - Módulo a iniciar
     - O que será coberto
     - Comando para retomar: `> leia o PROGRESS.md e me coloque em contexto`

5. Confirme ao usuário: "Contexto salvo nos 3 mecanismos." com um resumo de 2 linhas do que foi atualizado.

---

## Passo 3 — Publicação LinkedIn (executar após qualquer opção do Passo 2)

Após concluir a atualização, use `AskUserQuestion` com uma nova pergunta:

**"Deseja criar uma publicação para o LinkedIn com base no trabalho realizado?"**

Opções:
- **Sim, criar publicação** — gera preview em português e inglês com prompt de imagem
- **Não, encerrar** — encerra a skill sem gerar publicação

---

### Se "Sim, criar publicação"

Com base no contexto completo da sessão (o que foi criado, decidido e implementado),
gere os seguintes itens em sequência.

---

#### Padrão de referência

Use como referência de tom, estrutura e densidade técnica este exemplo real
de publicação sobre o JEV (trabalho deste mesmo projeto):

```
️ I added JEV to my RAG project — a typed decision layer that routes
queries before they touch the LLM.

🧠 The problem: every /ask call ran the full pipeline regardless of what
was asked. A greeting like "hi" cost the same as a substantive document
question — embedding, vector search, and an LLM call. JEV fixes this
with two independent decision points. The Intent Gate classifies the
question before any embedding: GREETING and META queries short-circuit
immediately with a fixed response, never touching the vector store or
the model. ANSWERABLE queries proceed normally. No ML model needed —
compiled regex and a lookup set, resolving in microseconds. The Chunk
Scorer sits between retrieval and the LLM: ChromaDB already computes
cosine distance for every retrieved chunk, but the project was ignoring
those scores and sending all top-k chunks to the model. Now each chunk
is scored (similarity = 1 − distance), and anything below the threshold
is dropped before the LLM call.

🔍 Both decisions are fully observable. Every /ask response now includes
a jev field: intent classification, short_circuited flag, chunks
retrieved vs accepted vs rejected, and the similarity threshold applied.
That makes the routing behavior auditable in real time. The full
implementation is covered by 30 unit tests that run without API keys or
models. JEV isn't a replacement for the LLM — it's a classifier and
router that reserves expensive generative calls for queries that
actually need them.

📌 What decision or routing layers have you built in front of your LLM
pipelines? Handling this at the query level before hitting the model is
an underrated optimization — drop your approach in the comments.

🐙 GitHub: https://lnkd.in/ecEUf74x

#RAG #JEV #LLMOps #AIEngineering #Python #GenerativeAI #AIArchitecture
#VectorDatabase #ChromaDB #FastAPI #MachineLearning #NLP #OpenSource
#SoftwareEngineering #PromptEngineering
```

---

#### Regras de estrutura (extraídas do padrão de referência)

**Linha de abertura (antes do 1º parágrafo):**
- Frase curta e direta que resume o que foi feito + por que importa
- Sem emoji ou com emoji leve (️)
- Funciona como "headline" — o que aparece no feed antes do "ver mais"

**Parágrafo 1 — 🧠 Problema + Solução**
- Começa com o problema concreto que existia antes
- Apresenta a solução com nomes técnicos reais (classes, padrões, ferramentas)
- Inclui detalhes de implementação específicos (não genéricos)
- Demonstra domínio: menciona tradeoffs, números, comportamentos observáveis

**Parágrafo 2 — 🔍 Implementação + Observabilidade**
- Deep dive: o que foi construído, como funciona, como pode ser verificado
- Menciona testes, logs, métricas, campos de resposta — qualquer coisa observável
- Termina posicionando a solução claramente ("X não é Y — é Z")

**Parágrafo 3 — 📌 Chamada de Impacto**
- Pergunta direta ao leitor sobre a mesma área técnica
- Frase de reforço que justifica o tema como relevante
- Convite explícito a comentar ("drop your approach in the comments")

**Rodapé:**
- Link do GitHub ou recurso relevante (se existir)
- 15 tags exatas, mix obrigatório:
  - 4-5 tags de domínio específico do tema
  - 3-4 tags de linguagem/ferramenta usada
  - 3-4 tags de audiência ampla (AIEngineering, SoftwareEngineering, etc.)
  - 2-3 tags de tendência (GenerativeAI, LLMOps, etc.)

**Tamanho:** ~1500 caracteres por versão (sem contar tags e rodapé)
**Tom:** técnico e direto — sem frases motivacionais, sem "jornada", sem "incrível"

---

#### 1. Publicação em Português

- Siga todas as regras acima
- Não é tradução do inglês — escreva nativamente em português técnico
- Tags em português quando existirem equivalentes relevantes; inglês para termos sem tradução consolidada

#### 2. Publicação em Inglês

- Siga todas as regras acima
- Não é tradução do português — adapte o vocabulário para o público técnico anglófono
- Tags em inglês otimizadas para alcance global no LinkedIn

#### 3. Prompt de Imagem

Gere um prompt em inglês para gerador de imagens (DALL-E, Midjourney, Stable Diffusion):
- Descreva o conceito técnico central visualmente (não abstrato)
- Estilo obrigatório: `clean tech illustration, dark background, neon accents, minimalist, professional, no text`
- Inclua elementos visuais que representem o que foi implementado (ex: grafos, pipelines, código, agentes)
- Resolução sugerida: `1920x1080, landscape, LinkedIn cover format`

---

**Formato de entrega:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 PUBLICAÇÃO — PORTUGUÊS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[linha de abertura]

🧠 [parágrafo 1]

🔍 [parágrafo 2]

📌 [parágrafo 3]

🐙 GitHub: [link se existir]

#tag1 #tag2 ... #tag15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 PUBLICAÇÃO — ENGLISH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[abertura]

🧠 [parágrafo 1]

🔍 [parágrafo 2]

📌 [parágrafo 3]

🐙 GitHub: [link se existir]

#tag1 #tag2 ... #tag15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 IMAGE PROMPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[prompt em inglês]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
