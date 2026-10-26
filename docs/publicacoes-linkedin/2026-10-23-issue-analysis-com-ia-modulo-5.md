# Issue Analysis com IA — Módulo 5

> Gerado em: 2026-10-23
> Skill: `/salvar-contexto` → Módulo concluído
> Tema: Módulo 5 — Issue Analysis com IA

---

## 💬 Comentário

**PT:** Módulo 5 do AIAD publicado: Issue Analysis com IA. Antes do spec, antes dos testes — a issue precisa ser decomposta em tasks atômicas com CAs verificáveis. O `/analyze-issue` faz isso em 6 passos. [link deste post] | Série completa: [link do post de lançamento]

**EN:** AIAD Module 5 is live: AI-powered Issue Analysis. Before the spec, before the tests — the issue needs to be decomposed into atomic tasks with verifiable ACs. The `/analyze-issue` skill does this in 6 steps. [link deste post] | Full series: [link do post de lançamento]

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

Transformei um fluxo de análise de issues em uma skill de 6 passos — do texto bruto ao spec pronto em minutos.

🔎 O problema: issues chegam mal definidas. "Upload não funciona", "precisamos de JWT", "refatorar o UserService" — sem escopo, sem critérios de aceite, sem definição de pronto. O time implementa e descobre os gaps no PR review ou na produção. O Módulo 5 do AIAD estrutura esse processo com IA: a issue é classificada (Bug / Feature / Task técnica), as ambiguidades são listadas com perguntas de clarificação, a issue é decomposta em tasks atômicas — cada uma implementável e testável de forma independente — e os critérios de aceite são extraídos no formato "dado/quando/então". Uma feature de JWT com 5 linhas de texto virou 4 tasks atômicas com 10 CAs verificáveis.

📋 A skill `/analyze-issue` implementa esse fluxo em 6 passos sequenciais. O passo 2 expõe as ambiguidades com perguntas diretas: quantos tokens são válidos simultaneamente? o logout invalida via blocklist no Redis ou só no cliente? Isso acontece antes de qualquer decomposição. O passo 5 gera o stub de spec no formato SDD e salva em `docs/specs/NNN-slug.md`. O stub já tem escopo dentro/fora, todos os CAs numerados e uma seção "campos em aberto" com o que falta para o spec estar completo. O resultado não é uma análise — é um artefato pronto para entrar no ciclo spec → testes → código do Módulo 2.

💬 Como o seu time lida com issues mal definidas? Existe uma etapa formal de análise antes do desenvolvimento começar, ou isso vai emergindo durante a implementação? Conta nos comentários.

#IssueAnalysis #CriteriosDeAceite #SpecDrivenDevelopment #RequirementsEngineering #AgileEngineering #ClaudeCode #AnthropicAPI #AIEngineering #SoftwareEngineering #DesenvolvimentoAgil #GenerativeAI #AIAssisted #LLMOps #TDD #ProductEngineering

---

## 📝 PUBLICAÇÃO — ENGLISH

I built a 6-step issue analysis skill — from raw text to a complete spec stub in minutes.

🔎 The problem: issues arrive half-formed. "Upload broken", "needs JWT", "refactor UserService" — no scope, no acceptance criteria, no definition of done. The team implements, discovers the gaps at PR review or in production. Module 5 of the AIAD project structures this with AI: the issue is classified (Bug / Feature / Tech task), ambiguities are surfaced with clarifying questions, the issue is decomposed into atomic tasks — each independently implementable and testable — and acceptance criteria are extracted in "given/when/then" format. A 5-line JWT feature request became 4 atomic tasks with 10 verifiable ACs.

📋 The `/analyze-issue` skill implements this as a 6-step pipeline. Step 2 exposes ambiguities with direct questions: how many tokens can be valid simultaneously? does logout invalidate via Redis blocklist or only client-side? This happens before any decomposition. Step 5 generates a spec stub in SDD Module 2 format and saves it to `docs/specs/NNN-slug.md`. The stub includes in/out scope, all ACs numbered, and a "fields open" section with what still needs to be filled before the spec is complete. The output isn't a document — it's an artifact ready to enter the spec → tests → code cycle.

💬 How does your team handle under-specified issues? Is there a formal analysis step before development starts, or does it unfold during implementation? Drop your approach in the comments.

#IssueAnalysis #AcceptanceCriteria #SpecDrivenDevelopment #RequirementsEngineering #AgileEngineering #ClaudeCode #AnthropicAPI #AIEngineering #SoftwareEngineering #ProductEngineering #GenerativeAI #AIAssisted #LLMOps #TDD #Agile

---

## 🎨 IMAGE PROMPT

A clean tech illustration showing a transformation pipeline on a dark background. On the left: a blurry sticky note or text bubble representing a vague, unstructured issue. In the center: a classification node branching into three labeled boxes (Bug, Feature, Task). From there, arrows flow into a decomposition tree with TASK-1, TASK-2, TASK-3 nodes connected by dependency arrows. On the right: a structured document icon with numbered acceptance criteria (CA-1, CA-2...) and a spec stub file. Neon cyan and purple accents, minimalist UI nodes, grid lines on dark background, professional. 1920x1080, landscape, LinkedIn cover format, no text.
