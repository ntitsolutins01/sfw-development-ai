# Sistema de persistência de contexto em 3 camadas + skill /salvar-contexto

> Gerado em: 2026-10-17
> Skill: `/gerar-post`
> Tema: Sistema de persistência de contexto entre sessões (AIAD)

---

## 💬 Comentário de Extensão

> Postar como comentário no post do Módulo 1 ([link do post Módulo 1]):

**PT:** Extensão das camadas CLAUDE.md e Skills do Módulo 1 — ao começar a construir a série, precisei resolver um problema real: cada nova sessão começava do zero. Construí um sistema de persistência em 3 camadas por cima dessas configurações: Project Memory (carregada automaticamente), seção de status no CLAUDE.md e journal de sessões no PROGRESS.md. Mais uma skill `/salvar-contexto` com menu interativo que atualiza as 3 camadas de uma vez. Detalhes neste post: [link deste post]

**EN:** Extension on the CLAUDE.md and Skills layers from Module 1 — when I started building the series, I had to solve a real problem: every new session started cold. I built a 3-layer persistence system on top of those configurations: Project Memory (auto-loaded), a status section in CLAUDE.md, and a session journal in PROGRESS.md. Plus a `/salvar-contexto` skill with an interactive menu that saves all 3 layers at once. Full breakdown here: [link deste post]

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

As 6 camadas de configuração do Módulo 1 resolvem o problema do ambiente — mas não resolvem o problema da memória entre sessões.

🗂️ O problema concreto: ao iniciar o trabalho no AIAD com Claude Code, cada nova sessão começava do zero. Precisava re-explicar o projeto, em que módulo estava, quais decisões tinham sido tomadas. A solução foi um sistema de persistência em 3 camadas com responsabilidades distintas: Project Memory (arquivos `.md` em `~/.claude/projects/`, carregados automaticamente pelo Claude Code em cada sessão), seção de status no `CLAUDE.md` do projeto (tabela de módulos com ✅/⏳, legível por humanos e pela IA), e `PROGRESS.md` (journal cronológico com o que foi construído, decisões tomadas e seção "Próxima sessão"). Cada camada cobre o ponto cego das outras — memory carrega contexto sem pedir, CLAUDE.md mostra o estado atual, PROGRESS.md guarda o histórico legível.

⚙️ A skill `/salvar-contexto` unifica as 3 camadas em um único ponto de invocação. Usa `AskUserQuestion` para renderizar um menu de seleção interativo — não lista de texto, um componente de UI dentro da interface do Claude Code — com 4 modos: módulo concluído (atualiza os 3 mecanismos), pausa (só PROGRESS.md), decisão importante (memory + PROGRESS.md) e fim de sessão (os 3 com seção "Próxima sessão"). Um segundo menu dispara geração automática de publicação no LinkedIn com preview PT e EN e prompt de imagem. A skill não é um wrapper de prompt — é uma especificação de comportamento com regras de output verificáveis.

💬 Como você gerencia contexto em sessões longas de desenvolvimento assistido por IA? Re-explica tudo a cada vez, depende só do CLAUDE.md ou tem uma abordagem própria? O problema de "project memory" é subestimado em workflows com LLM — deixa nos comentários.

#ClaudeCode #ContextEngineering #AIEngineering #LLMOps #GenerativeAI #SoftwareEngineering #PromptEngineering #DevWorkflow #AIAssistant #LLMDevelopment #DevProductivity #DeveloperTools #AIWorkflow #AIAD #OpenSource

---

## 📝 PUBLICAÇÃO — ENGLISH

The 6 configuration layers from Module 1 solve the environment problem — they don't solve the memory problem between sessions.

🗂️ The concrete issue: when I started building AIAD with Claude Code, every new session started cold. I had to re-explain the project, which module I was on, which decisions had been made. The fix was a 3-layer persistence architecture with distinct responsibilities: Project Memory (`.md` files in `~/.claude/projects/`, auto-loaded by Claude Code on every session start), a status section in the project's `CLAUDE.md` (module table with ✅/⏳ markers, readable by both humans and the model), and `PROGRESS.md` (a chronological session journal with what was built, decisions taken, and a "Next session" section). Each layer covers the blind spot of the others — memory loads context automatically, CLAUDE.md surfaces current state, PROGRESS.md holds the human-readable history.

⚙️ The `/salvar-contexto` skill unifies all 3 layers into a single invocation point. It uses `AskUserQuestion` to render an interactive selection menu — not a text list, an actual UI component inside the Claude Code interface — with 4 modes: module completed (updates all 3 mechanisms), pause (PROGRESS.md only), important decision (memory + PROGRESS.md), and end of session (all 3 with a "Next session" section). A second menu triggers automatic LinkedIn post generation with PT and EN previews and an image prompt. The skill isn't a prompt wrapper — it's a behavior specification with verifiable output rules.

📌 How do you manage context across long AI-assisted development sessions? Re-explain everything each time, rely solely on CLAUDE.md, or do you have your own approach? The "project memory" problem is underrated in LLM workflows — drop your approach in the comments.

#ClaudeCode #ContextEngineering #AIEngineering #LLMOps #GenerativeAI #SoftwareEngineering #PromptEngineering #DevWorkflow #AIAssistant #LLMDevelopment #DevProductivity #DeveloperTools #AIWorkflow #AIAD #OpenSource
