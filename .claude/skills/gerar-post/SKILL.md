---
name: gerar-post
description: Gera publicação LinkedIn em PT e EN com prompt de imagem, com base no contexto atual ou em um tema informado. Use como "/gerar-post sobre X" ou apenas "/gerar-post" para usar o contexto da sessão.
disable-model-invocation: false
---

# gerar-post

Você foi invocado via `/gerar-post`.

## Passo 1 — Identificar o tema

Verifique se o usuário informou um tema junto ao comando (ex: `/gerar-post sobre JEV`, `/gerar-post sobre prompt caching`).

- **Se informou tema:** use esse tema como foco da publicação.
- **Se não informou:** use o contexto completo da conversa atual (o que foi construído, decidido ou discutido nesta sessão).

Não pergunte ao usuário — trabalhe com o que está disponível.

---

## Passo 2 — Gerar a publicação

Com base no tema ou contexto identificado, gere os 3 itens abaixo em sequência.

---

### Padrão de referência

Use como referência de tom, estrutura e densidade técnica este exemplo real:

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

### Regras de estrutura

**Linha de abertura:**
- Frase curta e direta que resume o que foi feito + por que importa
- Sem emoji ou com emoji leve (️)
- É o "headline" — o que aparece no feed antes do "ver mais"

**Parágrafo 1 — Problema + Solução**
- Começa com o problema concreto que existia antes
- Apresenta a solução com nomes técnicos reais (classes, padrões, ferramentas)
- Inclui detalhes de implementação específicos (não genéricos)
- Demonstra domínio: tradeoffs, números, comportamentos observáveis

**Parágrafo 2 — Implementação + Observabilidade**
- Deep dive: o que foi construído, como funciona, como pode ser verificado
- Menciona testes, logs, métricas, campos de resposta — qualquer coisa observável
- Termina posicionando a solução claramente ("X não é Y — é Z")

**Parágrafo 3 — Chamada de Impacto**
- Pergunta direta ao leitor sobre a mesma área técnica
- Frase de reforço que justifica o tema como relevante
- Convite explícito a comentar

**Emojis dos parágrafos — escolha por assunto:**

Não use emojis fixos. Escolha um emoji por parágrafo que seja semanticamente coerente com o conteúdo daquele bloco. Referência por domínio:

| Domínio | Parágrafo 1 (problema/solução) | Parágrafo 2 (implementação) | Parágrafo 3 (chamada) |
|---|---|---|---|
| Segurança / OWASP | 🔐 🛡️ ⚠️ | 🔎 🧪 🕵️ | 🚨 ❓ 💬 |
| Performance / otimização | ⚡ 🏎️ 📉 | 📊 🔬 🧮 | 🎯 ❓ 💬 |
| Arquitetura / design | 🏗️ 🧩 🗺️ | 🔧 ⚙️ 🛠️ | 🤔 ❓ 💬 |
| IA / LLM / agentes | 🤖 🧠 🦾 | 🔍 📡 🧬 | 💡 ❓ 💬 |
| Observabilidade / logs | 📡 📈 🔭 | 🔍 📋 🧾 | 👁️ ❓ 💬 |
| TDD / qualidade | 🧪 ✅ 🎯 | 🔍 📋 🧱 | 🤝 ❓ 💬 |
| DevOps / CI/CD | 🚀 🔄 🏭 | 🛠️ ⚙️ 📦 | 🔁 ❓ 💬 |
| Dados / ETL / RAG | 📦 🗃️ 🔁 | 🔎 📊 🧮 | 🗂️ ❓ 💬 |
| Anúncio / série / lançamento | 📣 🗓️ 🎬 | 📋 🗺️ 📍 | 👆 ❓ 💬 |

- Use **um único emoji** por parágrafo, no início da linha
- Nunca repita o mesmo emoji nos três parágrafos
- Se o tema misturar domínios, escolha o emoji mais próximo do conteúdo específico daquele bloco
- Para domínios não listados, escolha livremente — a regra é coerência semântica, não a tabela

**Rodapé:**
- Link do GitHub se existir (se não souber, omita a linha)
- 15 tags, mix obrigatório:
  - 4-5 tags de domínio específico do tema
  - 3-4 tags de linguagem/ferramenta usada
  - 3-4 tags de audiência ampla (AIEngineering, SoftwareEngineering, etc.)
  - 2-3 tags de tendência (GenerativeAI, LLMOps, etc.)

**Tamanho:** ~1500 caracteres por versão (sem contar tags e rodapé)
**Tom:** técnico e direto — sem frases motivacionais, sem "jornada", sem "incrível"

---

### 1. Publicação em Português

- Siga todas as regras acima
- Escreva nativamente em português técnico (não é tradução)
- Tags em inglês para termos sem tradução consolidada

### 2. Publicação em Inglês

- Siga todas as regras acima
- Adapte o vocabulário para o público técnico anglófono (não é tradução)
- Tags em inglês otimizadas para alcance global

### 3. Prompt de Imagem

Prompt em inglês para DALL-E, Midjourney ou Stable Diffusion:
- Descreva o conceito técnico visualmente (não abstrato)
- Estilo: `clean tech illustration, dark background, neon accents, minimalist, professional, no text`
- Inclua elementos visuais que representem o que foi implementado
- Resolução: `1920x1080, landscape, LinkedIn cover format`

---

### Formato de entrega

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

---

## Passo 3 — Salvar em arquivo

Após exibir a publicação no console, salve o conteúdo gerado em:

```
docs/publicacoes-linkedin/YYYY-MM-DD-<slug>.md
```

**Regras para o nome do arquivo:**
- `YYYY-MM-DD` = data atual no formato ISO
- `<slug>` = 3-5 palavras do tema em kebab-case, sem acentos (ex: `dapia-lancamento-serie`, `prompt-caching-api`, `jev-rag-routing`)

**Estrutura do arquivo:**

```markdown
# [Título descritivo da publicação]

> Gerado em: YYYY-MM-DD
> Skill: `/gerar-post`
> Tema: [tema ou contexto usado]

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

[conteúdo completo]

---

## 📝 PUBLICAÇÃO — ENGLISH

[conteúdo completo]

---

## 🎨 IMAGE PROMPT

[prompt]
```

**Comportamento:**
- Crie o diretório `docs/publicacoes-linkedin/` se não existir
- Salve sempre, sem perguntar — é parte do fluxo padrão
- Exiba no console E salve em arquivo em paralelo (não sequencial)
- Ao final, informe o caminho do arquivo salvo em uma linha
