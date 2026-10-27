# Context Engineering — Módulo 7

> Gerado em: 2026-10-26
> Skill: `/salvar-contexto` → Módulo concluído
> Tema: Módulo 7 — Context Engineering

---

## 💬 Comentário

**PT:** Módulo 7 do AIAD publicado: Context Engineering. 4 camadas, ciclo seed→compact→persistir→retomar, e por que cada sessão do Claude Code começa do zero se você não fizer nada a respeito. [link deste post] | Série: [link do post de lançamento]

**EN:** AIAD Module 7 is live: Context Engineering. 4 layers, seed→compact→persist→resume cycle, and why every Claude Code session starts blind if you don't architect around it. [link deste post] | Series: [link do post de lançamento]

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

Toda sessão do Claude Code começa com zero contexto. Documentei a arquitetura de 4 camadas que resolve isso entre sessões.

🧠 O problema: sem gestão de contexto, você passa os primeiros 10 minutos de cada sessão re-explicando o projeto — stack, convenções, o que foi decidido, o que não foi. E em sessões longas (>50 trocas), informações do início da conversa competem com outputs de ferramentas, tentativas descartadas e branches exploratórios. O modelo não "esquece", mas prioriza o que está mais próximo. Resultado: decisões importantes tomadas no exchange 3 recebem menos atenção que ruído do exchange 45. A solução é uma arquitetura de 4 camadas: **Memory** (fatos que persistem entre sessões — decisões arquiteturais, o que foi construído), **Rules** (restrições comportamentais sempre ativas — nunca precisam ser repetidas no prompt), **CLAUDE.md** (contexto de projeto carregado automaticamente — stack, status, como navegar), e a **Conversa** (a janela ativa, gerenciada com seed + compact + persistência).

📡 O Módulo 7 documenta o ciclo completo: seed (contexto mínimo necessário para a tarefa específica, não tudo), work, compact (`/compact` quando a sessão tem ruído — preserva decisões e código, descarta outputs de ferramentas já processados e tentativas descartadas), persist (3 mecanismos: memory para fatos estáveis, CLAUDE.md para status, PROGRESS.md para histórico de sessões), e resume (prompt estruturado que carrega o estado correto). Fork agent herda o contexto da sessão atual para exploração paralela sem poluir a sessão principal. Fresh agent começa do zero para revisões que precisam ser imparciais. O próprio AIAD demonstra isso: 10 sessões, 7 módulos concluídos, cada retomada precisa porque o PROGRESS.md tem arquivo + função + CAs pendentes na seção "Próxima sessão" — não "continuar o módulo".

💬 Como você gerencia o contexto entre sessões de trabalho com IA? Existe algum mecanismo de persistência no seu fluxo, ou cada sessão começa do zero? Conta nos comentários.

#ContextEngineering #ClaudeCode #AIAssistedDevelopment #DeveloperProductivity #LLMContext #AnthropicAPI #AIEngineering #SoftwareEngineering #ContextWindow #GenerativeAI #LLMOps #AIFirst #Python #FastAPI #PromptEngineering

---

## 📝 PUBLICAÇÃO — ENGLISH

Every Claude Code session starts with zero context. I documented the 4-layer architecture that solves this across sessions.

🧠 The problem: without context engineering, you spend the first 10 minutes of each session re-explaining the project — stack, conventions, what was decided, what wasn't. And in long sessions (>50 exchanges), information from early in the conversation competes with tool outputs, discarded attempts, and exploratory branches. The model doesn't "forget", but it prioritizes what's closest. Decisions made at exchange 3 get less attention than noise at exchange 45. The solution is a 4-layer architecture: **Memory** (facts that persist between sessions — architectural decisions, what was built), **Rules** (behavioral constraints always active — never need repeating in a prompt), **CLAUDE.md** (project context loaded automatically — stack, status, how to navigate), and the **Conversation** (the active window, managed with seed + compact + persistence).

📡 Module 7 documents the full cycle: seed (minimum context for the specific task, not everything), work, compact (`/compact` when the session has noise — preserves decisions and code, discards already-processed tool outputs and discarded attempts), persist (3 mechanisms: memory for stable facts, CLAUDE.md for status, PROGRESS.md for session history), and resume (structured prompt that loads the right state). Fork agent inherits the current session's context for parallel exploration without polluting the main session. Fresh agent starts clean for reviews that need to be unbiased. The AIAD project itself demonstrates this: 10 sessions, 7 modules complete, each resume is precise because PROGRESS.md has file + function + pending ACs in "Next session" — not "continue the module".

💬 How do you manage context across AI working sessions? Is there a persistence mechanism in your workflow, or does each session start from scratch? Drop your approach in the comments.

#ContextEngineering #ClaudeCode #AIAssistedDevelopment #DeveloperProductivity #LLMContext #AnthropicAPI #AIEngineering #SoftwareEngineering #ContextWindow #GenerativeAI #LLMOps #AIFirst #Python #FastAPI #PromptEngineering

---

## 🎨 IMAGE PROMPT

A clean tech illustration on a dark background showing a 4-layer stack architecture for context management. Bottom layer labeled "Memory" (solid persistent foundation, neon purple), second layer "Rules" (constraint grid lines, cyan), third layer "CLAUDE.md" (document icon, glowing), top layer "Conversation" (active session with flowing data particles). On the right side: a circular lifecycle diagram showing seed → work → compact → persist → resume with arrows connecting each step. Between sessions: a gap with dotted lines and an arrow showing context "surviving" the gap via the 3 persistence mechanisms. Minimalist, dark background, neon cyan and purple accents, professional. 1920x1080, landscape, LinkedIn cover format, no text.
