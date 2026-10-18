# Sistema de persistência de contexto em 3 camadas + skill /salvar-contexto

> Gerado em: 2026-10-17
> Skill: `/gerar-post`
> Tema: Sistema de persistência de contexto entre sessões (DAPIA)

---

## 📝 PUBLICAÇÃO — ENGLISH

I built a 3-layer context persistence system for AI-assisted development sessions — and a skill that saves everything through an interactive menu.

🧠 The problem is straightforward: every new Claude Code session starts cold. You spend the first few minutes re-explaining the project, where you left off, what decisions were made. The fix was a 3-layer architecture with distinct responsibilities: Project Memory (auto-loaded by Claude Code on every session start), a status section in CLAUDE.md (readable by both humans and the model, with a module table and pointer to the journal), and PROGRESS.md (a chronological session journal with what was built, decisions taken, and a "Next session" section). Each layer covers the blind spot of the others — memory loads context automatically, CLAUDE.md surfaces current state, PROGRESS.md holds the human-readable history.

🔍 The /salvar-contexto skill unifies all 3 layers into a single invocation point. It uses AskUserQuestion to render an interactive selection menu — not a text list, an actual UI component inside the Claude Code interface — with 4 modes: module completed (updates all 3 mechanisms), pause (PROGRESS.md only), important decision (memory + PROGRESS.md), and end of session (all 3 with a "Next session" section). Each mode reads the relevant files and updates only what's pertinent. A second menu triggers automatic LinkedIn post generation with a reference structure, PT and EN previews, and an image prompt.

📌 How do you manage context across long AI-assisted development sessions? Re-explain everything each time, rely solely on CLAUDE.md, or do you have your own approach? This "project memory" problem is underrated in LLM workflows — drop your approach in the comments.

#ClaudeCode #AIEngineering #LLMOps #ContextEngineering #GenerativeAI #SoftwareEngineering #DeveloperTools #AIWorkflow #PromptEngineering #MLOps #LLMDevelopment #AIAssistant #DevProductivity #OpenSource #MachineLearning
