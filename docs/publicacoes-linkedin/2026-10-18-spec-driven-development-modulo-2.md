# Spec Driven Development — Módulo 2 AIAD

> Gerado em: 2026-10-18
> Tema: Módulo 2 — Spec Driven Development + skills de pré-spec (/brainstorm, /escrever-prd, /escrever-trd)

---

## PUBLICAÇÃO — PORTUGUÊS

Adicionei o Módulo 2 ao AIAD — Spec Driven Development com um fluxo expandido que vai do brainstorm ao código.

🧠 O problema: quando você pede para uma IA implementar uma feature sem especificação, ela toma decisões por você. Qual banco usar, como tratar erros, quais campos são obrigatórios, o que retornar em falha. Cada decisão implícita é um ponto de divergência entre o que você queria e o que foi gerado. Spec Driven Development inverte isso: você define as decisões antes, a IA implementa dentro dos limites que você estabeleceu. O ciclo tem 4 passos fixos — escrever spec, revisar com IA (identifica ambiguidades e gaps), implementar dentro do escopo, validar cada critério de aceite. O spec não é burocracia — é o contrato que impede que a IA improvise onde não deve.

🔍 O fluxo expandido vai além do spec técnico: `/brainstorm` matura a ideia antes de qualquer implementação (dois modos: generalista e spec lens), `/escrever-prd` gera um PRD draft-first em `docs/prds/NNN-nome.md` com user stories, critérios de aceite e métricas, e `/escrever-trd` cria um TRD global único por projeto em `docs/trd.md` com stack, arquitetura, NFRs e ADRs. As três são skills do Claude Code instaladas em `.claude/skills/` — não são comandos globais, são contexto de projeto. O módulo inclui 4 templates de spec (feature, bugfix, refactor, api-endpoint), 6 prompts prontos para cada fase do ciclo e 3 specs reais preenchidos como referência.

📌 Qual é o maior custo de implementar sem spec em times que usam IA? Na minha experiência, não é o retrabalho — é o código correto que resolve o problema errado. O spec força a clareza antes que a IA entre no loop. Qual estratégia você usa para garantir que a IA implementa o que você realmente quer? Troca nos comentários.

🐙 GitHub: https://github.com/ntitsolutins01/sfw-development-ai

#SpecDrivenDevelopment #ClaudeCode #AIEngineering #PromptEngineering #SoftwareEngineering #TDD #GenerativeAI #LLMOps #Python #NodeJS #DevWorkflow #ProductRequirements #TechnicalSpec #AIAssisted #OpenSource

---

## PUBLICAÇÃO — ENGLISH

Added Module 2 to AIAD — Spec Driven Development with an expanded pre-spec flow that runs from brainstorm to working code.

🧠 The problem: when you ask an AI to implement a feature without a spec, it makes implicit decisions for you. Which database, how to handle errors, which fields are required, what to return on failure. Each implicit decision is a divergence point between what you wanted and what was generated. SDD inverts this: you define decisions upfront, the AI implements within bounds you set. The cycle has four fixed steps — write spec, review with AI (finds ambiguities and missing information), implement within defined scope, validate each acceptance criterion. The spec isn't ceremony — it's the contract that keeps the AI from improvising where it shouldn't.

🔍 The expanded flow adds a pre-spec layer: `/brainstorm` matures the idea before any implementation (two modes: generalist and spec lens), `/escrever-prd` generates a draft-first PRD at `docs/prds/NNN-name.md` with user stories, acceptance criteria, and metrics, and `/escrever-trd` creates a single global TRD at `docs/trd.md` with stack, architecture, NFRs, and ADRs. All three are Claude Code project-level skills installed in `.claude/skills/` — not global commands, project context. The module ships with 4 spec templates (feature, bugfix, refactor, api-endpoint), 6 ready prompts for each cycle phase, and 3 real filled-in specs as reference.

📌 What's the real cost of implementing without a spec when your team uses AI? In my experience, it's not rework — it's correct code solving the wrong problem. The spec forces clarity before the AI enters the loop. What's your strategy for ensuring the AI implements what you actually want? Drop it in the comments.

🐙 GitHub: https://github.com/ntitsolutins01/sfw-development-ai

#SpecDrivenDevelopment #ClaudeCode #AIEngineering #PromptEngineering #SoftwareEngineering #GenerativeAI #LLMOps #ProductRequirements #TechnicalSpec #AIAssisted #Python #NodeJS #DevWorkflow #RequirementsEngineering #OpenSource

---

## IMAGE PROMPT

A horizontal pipeline diagram showing two connected blocks on a dark background. Left block labeled "PRE-SPEC" contains three stacked cards: brainstorm (lightbulb icon, blue neon), PRD (document icon, purple neon), TRD (architecture diagram icon, teal neon). An arrow connects to the right block labeled "SPEC CYCLE" containing four numbered steps in a vertical flow: 1-WRITE (pencil), 2-REVIEW (magnifying glass), 3-IMPLEMENT (code brackets), 4-VALIDATE (checkmark). Connecting arrows between steps glow cyan. Background is deep dark navy. All labels in clean monospace font. Clean tech illustration, dark background, neon accents, minimalist, professional, no text, 1920x1080, landscape, LinkedIn cover format.
