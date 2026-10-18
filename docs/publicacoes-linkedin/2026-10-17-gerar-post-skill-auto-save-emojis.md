# gerar-post skill — Auto-save e emojis semânticos por domínio

> Gerado em: 2026-10-17
> Skill: `/gerar-post`
> Tema: Skill customizado no Claude Code para geração de posts LinkedIn com salvamento automático e emojis variáveis por domínio

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

Criei um skill customizado no Claude Code para gerar posts técnicos no LinkedIn — com salvamento automático em arquivo e emojis por domínio.

🧩 O problema era consistência: cada sessão de trabalho gerava publicações com estrutura manual, emojis fixos (sempre 🧠/🔍/📌) e sem histórico persistido. O skill `gerar-post` resolve isso com uma instrução executável em `SKILL.md`: define padrão de abertura, três parágrafos com regras por bloco, 15 tags com mix obrigatório de domínio/ferramenta/audiência/tendência, e uma tabela de emojis semânticos por domínio — segurança usa 🔐/🛡️, performance usa ⚡/📉, IA usa 🤖/🧠, anúncios usam 📣/🗓️. Nenhum emoji se repete nos três parágrafos.

⚙️ O output vai para `docs/publicacoes-linkedin/YYYY-MM-DD-<slug>.md`, com o diretório criado automaticamente se não existir — Passo 3 do skill, executado em paralelo com a exibição no console. O Claude Code lê o `SKILL.md` como instrução de comportamento, não como template: cada invocação de `/gerar-post` adapta tom, emojis e densidade técnica ao tema da sessão. O resultado é auditável pelo histórico de arquivos no repositório. O skill não é um prompt wrapper — é uma especificação de comportamento com regras de output verificáveis.

💡 Se você usa Claude Code no dia a dia e ainda não tem skills customizados para tarefas recorrentes, está re-derivando contexto a cada sessão. Qual fluxo do seu workflow mais se beneficiaria de uma instrução persistida? Deixe nos comentários.

#ClaudeCode #SkillEngineering #AIEngineering #PromptEngineering #DevWorkflow #Python #NodeJS #GenerativeAI #LLMOps #ContentAutomation #DAPIA #SoftwareDevelopment #AIAssisted #Automation #OpenSource

---

## 📝 PUBLICAÇÃO — ENGLISH

Built a custom Claude Code skill to generate technical LinkedIn posts — with automatic file saving and domain-aware emoji selection.

🧩 The problem was consistency: each working session produced LinkedIn content with manual structure, fixed emojis (always the same 🧠/🔍/📌), and no persistent output history. The `gerar-post` skill fixes this with an executable instruction in `SKILL.md`: it defines an opening-line rule, three paragraph blocks with per-block criteria, a 15-tag mix requirement (domain/tool/audience/trend), and a semantic emoji table by domain — security gets 🔐/🛡️, performance gets ⚡/📉, AI gets 🤖/🧠, announcements get 📣/🗓️. No emoji repeats across the three paragraphs.

⚙️ Output lands in `docs/publicacoes-linkedin/YYYY-MM-DD-<slug>.md`, with the directory created automatically if it doesn't exist — Step 3 of the skill, executed in parallel with the console output. Claude Code reads `SKILL.md` as behavioral instruction, not as a template: each `/gerar-post` invocation adapts tone, emoji choice, and technical density to the session's subject. The output is auditable through the file history in the repository. The skill isn't a prompt wrapper — it's a behavior spec with verifiable output rules.

💡 If you use Claude Code daily and don't have custom skills for recurring tasks, you're re-deriving context on every session. Which workflow in your stack would benefit most from a persisted behavioral instruction? Drop it in the comments.

#ClaudeCode #SkillEngineering #AIEngineering #PromptEngineering #DevWorkflow #Python #NodeJS #GenerativeAI #LLMOps #ContentAutomation #DAPIA #SoftwareDevelopment #AIAssisted #Automation #OpenSource

---

## 🎨 IMAGE PROMPT

A clean tech illustration showing a SKILL.md file at the center of a dark background, surrounded by three glowing output blocks connected by neon cyan arrows — each block representing a paragraph with a different colored emoji icon (puzzle piece in purple, gear in teal, lightbulb in yellow). Below the blocks, a file path string `docs/publicacoes-linkedin/2026-10-17-slug.md` glows in neon green, indicating automatic file creation. The overall composition conveys a behavioral spec driving structured, repeatable output. Style: clean tech illustration, dark background, neon accents, minimalist, professional, no text. Resolution: 1920x1080, landscape, LinkedIn cover format.
