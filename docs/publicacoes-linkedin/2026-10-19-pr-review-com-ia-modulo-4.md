# PR Review com IA — Conformidade com Spec e Decisão Formal

> Gerado em: 2026-10-19
> Skill: `/gerar-post`
> Tema: Módulo 4 — Pull Request Review com IA (AIAD)

---

## 💬 Comentário

> Postar como comentário no post de lançamento da série (https://lnkd.in/p/dpJ8fi3V):

**PT:** Módulo 4 do AIAD publicado — PR Review com conformidade de spec. A skill `/review-pr` mapeia cada critério de aceite do spec contra o diff e emite decisão formal: APROVADO ou SOLICITAR MUDANÇAS. Fecha o ciclo com os Módulos 2 (spec) e 3 (TDD). Detalhes neste post: [link deste post]

**EN:** Module 4 of AIAD is live — spec-aware PR Review. The `/review-pr` skill maps each acceptance criterion from the spec against the diff and emits a formal decision: APPROVED or REQUEST CHANGES. Closes the loop with Modules 2 (spec) and 3 (TDD). Full breakdown here: [link deste post]

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

Revisão de PR inconsistente é um problema de processo, não de atenção.

🔎 O problema concreto: revisores diferentes cobrem coisas diferentes. Você verifica segurança hoje, amanhã foca só na lógica, e cobertura de testes raramente entra no checklist. A IA resolve a consistência — mas a parte interessante não é a revisão de qualidade geral. É a revisão de conformidade com spec. A skill `/review-pr` recebe o caminho do spec (gerado no Módulo 2) e mapeia cada critério de aceite contra o diff: coberto (com arquivo e teste encontrado), ausente ou parcial. O resultado não é uma lista de sugestões — é uma decisão: `APROVADO`, `APROVADO COM RESSALVAS` ou `SOLICITAR MUDANÇAS`.

✅ O fluxo tem três fases sequenciais. Self-review com checklist tipado (feature, bugfix ou refactor) antes de qualquer ferramenta. Depois `/code-review` para qualidade geral: bugs, segurança, performance — cada achado classificado em `CRÍTICO / ALTO / MÉDIO / BAIXO`, com os dois primeiros bloqueando o merge. Por último `/review-pr docs/specs/NNN-nome.md`: compara o diff com os CAs do spec e verifica se cada CA tem teste correspondente. No Módulo 3 você escreveu os testes antes da implementação. Aqui você verifica se a implementação honrou o contrato. O revisor humano entra depois de `APROVADO` pela IA — focado no que ela não cobre: julgamento de design e impacto sistêmico.

💬 Como você define que um PR está pronto para merge? "Os testes passam" não é suficiente se o spec tinha 5 CAs e 2 não foram implementados. O gap entre testes verdes e spec coberto é mais comum do que parece — deixa nos comentários como você garante conformidade antes do merge.

#PullRequest #CodeReview #SpecDrivenDevelopment #TDD #ClaudeCode #Git #Python #SoftwareEngineering #AIEngineering #DevProductivity #DeveloperTools #GenerativeAI #LLMOps #AIAD #AIWorkflow

---

## 📝 PUBLICAÇÃO — ENGLISH

Inconsistent PR review is a process problem, not an attention problem.

🔎 The concrete issue: different reviewers cover different things — security one day, business logic another, test coverage almost never. AI solves the consistency half. But the interesting part isn't general quality review — it's spec compliance. The `/review-pr` skill takes the path to the spec (written in Module 2) and maps each acceptance criterion against the diff: covered (with the implementing file and test named), absent, or partial. The output isn't a list of suggestions — it's a decision: `APPROVED`, `APPROVED WITH NOTES`, or `REQUEST CHANGES`.

✅ The flow runs in three sequential phases. Self-review with a typed checklist (feature, bugfix, or refactor) before any tooling. Then `/code-review` for general quality: bugs, security, performance — each finding tagged `CRITICAL / HIGH / MEDIUM / LOW`, with the first two blocking merge. Finally `/review-pr docs/specs/NNN-name.md`: compares the diff to each AC from the spec and verifies that each AC has a corresponding test. In Module 3 you wrote the tests before the implementation. Here you verify that the implementation honored the contract. The human reviewer enters after the AI returns `APPROVED` — focused on what the model can't evaluate: design judgment and systemic impact.

💬 How do you define a PR as ready to merge? "Tests pass" isn't enough if the spec had 5 ACs and 2 were never implemented. The gap between green tests and covered spec is more common than it looks — drop your approach in the comments.

#PullRequest #CodeReview #SpecDrivenDevelopment #TDD #ClaudeCode #Git #Python #SoftwareEngineering #AIEngineering #DevProductivity #DeveloperTools #GenerativeAI #LLMOps #AIAD #AIWorkflow

---

## 🎨 IMAGE PROMPT

Three-panel horizontal pipeline on a dark background. Left panel: a code diff view with colored additions and deletions in a terminal-style font, neon green and red lines. Center panel: a spec document with checkboxes — some checked in bright green, one unchecked in amber, labeled "Acceptance Criteria". Right panel: a large formal decision badge with "APPROVED" in neon green bold text, connected by bright flow arrows from left to right. Minimalist tech illustration style, no humans, no text labels except the badge, neon accents on dark background, clean geometric layout. 1920x1080, landscape, LinkedIn cover format.
