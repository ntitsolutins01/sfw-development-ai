# Claude Code — Framework de configuração com 6 camadas

> Gerado em: 2026-10-17
> Skill: `/gerar-post`
> Tema: Módulo 1 — Claude Code e Cursor (AIAD)

---

## 📝 PUBLICAÇÃO — ENGLISH

I structured a 6-layer configuration framework for Claude Code — and most developers use none of them.

🧠 Without configuration, Claude Code starts every session cold, the model instruction has to be retyped. Module 1 of the workflow de desenvolvimento de software assistido por IA project maps out the 6 layers that turn Claude Code from "AI chat in a terminal" into an engineering platform: `settings.json` controls what the model can physically execute — 30+ documented patterns, with `rm -rf` and `git push --force` on the denylist by default, `git status` and `npm test` on the allowlist. `CLAUDE.md` operates at 3 levels: global (personal preferences), project (repo-specific rules), and subfolder (local overrides). Skills are named automation flows using Claude Code tools, with `AskUserQuestion` enabling real interactive menus. Rules are behavioral constraints injected into context automatically. MCP servers wire up GitHub, Postgres, Slack, and Terraform. Subagents run as fork (inherits context and KV cache) or fresh (starts clean).

🔍 Each layer has a different blast radius. `settings.json` is the only layer where an action is physically blocked — the others influence behavior, not permission. One non-obvious discovery documented in the module: project Skills in `.claude/skills/` do NOT register `/` CLI commands — only globally installed plugin Skills do. The `disable-model-invocation: false` flag is required for Claude to invoke a project skill when the user types the name as a chat message. This behavior is undocumented in the CLI and only surfaces when you test it. The module ships ready-to-use examples: CLAUDE.md templates (global, Django, React), rules files (Python, security, LLM APIs, RAG pipelines), and 3 working skills (code-review, criar-pr, rodar-testes).

📌 How do you handle Claude Code configuration across projects — starting from scratch each time, or do you maintain a baseline CLAUDE.md you replicate across repos? Zero configuration isn't neutrality: it's the model running without context and without defined constraints. Drop in the comments what you wish you had set up from day one.

#ClaudeCode #AIEngineering #DeveloperTools #ContextEngineering #LLMOps #GenerativeAI #SoftwareEngineering #AIWorkflow #PromptEngineering #MLOps #DevTools #AIAssistant #DevProductivity #OpenSource #MachineLearning
