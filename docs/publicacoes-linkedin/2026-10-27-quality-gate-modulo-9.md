# Quality Gate — Módulo 9

> Gerado em: 2026-10-27
> Skill: `/salvar-contexto` → Módulo concluído
> Tema: Módulo 9 — Quality Gate

---

## 💬 Comentário

**PT:** Módulo 9 do AIAD publicado: Quality Gate. A diferença entre gate e recommendation, calibração de thresholds, verify_token de D(14)→A(3) via complexidade ciclomática, e por que Intent Gate + Chunk Scorer são o mesmo conceito em pipelines LLM. [link deste post] | Série: [link do post de lançamento]

**EN:** AIAD Module 9 is live: Quality Gate. The difference between gate and recommendation, threshold calibration, verify_token from D(14)→A(3) via cyclomatic complexity, and why Intent Gate + Chunk Scorer are the exact same concept in LLM pipelines. [link deste post] | Series: [link do post de lançamento]

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

A diferença entre quality gate e quality recommendation — e por que a maioria dos projetos tem a segunda achando que tem o primeiro.

🎯 O problema: uma badge de cobertura no README é uma recomendação. `--cov-fail-under=80` com exit code 2 é um gate. A distinção importa porque só o segundo impede regressões. O Módulo 9 documenta três gates com dentes: estático (`radon cc app/ -s --min C` — saída vazia = passou, qualquer função listada = build falhou), dinâmico (`pytest --cov=app --cov-fail-under=80` — exit code 2 bloqueia o CI), e segurança (`bandit -r app/ -ll` + `pip-audit`). A regra de calibração: threshold inicial = medição atual − 5%. Nunca começar no target ambicioso que bloqueia tudo no dia 1 — o resultado é o time desabilitar o gate para "consertar depois".

🔧 O exemplo de complexidade ilustra bem. `verify_token` tinha complexidade D (score 14) — acima do threshold C (≤ 10). O gate falhou. A função tinha 4 responsabilidades: decodificar assinatura JWT, extrair `user_id` do payload, verificar blocklist, resolver usuário ativo no banco. Separar em `_decode_token` + `_extract_user_id` + `_resolve_active_user` trouxe cada função para grade A (score 3). Complexidade média caiu de B (7.67) para A (3.5). Bônus: cada função auxiliar passou a ser testável em isolamento — sem precisar montar o AuthService inteiro para testar a lógica de expiração. O mesmo conceito se aplica a pipelines LLM: o Intent Gate do JEV é um gate que bloqueia inputs GREETING antes da embedding. O Chunk Scorer bloqueia chunks com similarity < 0.5 antes do prompt. Critério objetivo → decisão binária → bloqueia ou deixa passar.

🤝 Qual a sua regra para calibrar thresholds de quality gate? Começa conservador e aperta gradualmente, ou já define o alvo final e aceita a avalanche inicial de falhas? Conta nos comentários.

#QualityGate #ClaudeCode #AIAssistedDevelopment #SoftwareQuality #CyclomaticComplexity #TestCoverage #PythonTesting #AIEngineering #SoftwareEngineering #DevOps #FastAPI #CIcd #GenerativeAI #LLMOps #DevSecOps

---

## 📝 PUBLICAÇÃO — ENGLISH

The difference between a quality gate and a quality recommendation — and why most projects have the second while thinking they have the first.

🎯 The problem: a coverage badge in the README is a recommendation. `--cov-fail-under=80` with exit code 2 is a gate. The distinction matters because only the second one actually prevents regressions. Module 9 documents three gates with teeth: static (`radon cc app/ -s --min C` — empty output = passed, any function listed = build failed), dynamic (`pytest --cov=app --cov-fail-under=80` — exit code 2 blocks CI), and security (`bandit -r app/ -ll` + `pip-audit`). The calibration rule: initial threshold = current measurement − 5%. Never start at an ambitious target that blocks everything on day 1 — the team will just disable the gate to "fix later."

🔧 The complexity example makes this concrete. `verify_token` had complexity grade D (score 14) — above the grade C threshold (≤ 10). Gate failed. The function had 4 responsibilities: decode JWT signature, extract `user_id` from payload, check blocklist, resolve active user from the database. Splitting into `_decode_token` + `_extract_user_id` + `_resolve_active_user` brought each function to grade A (score 3). Average complexity dropped from B (7.67) to A (3.5). Bonus: each auxiliary function is now testable in isolation — no need to wire up the full AuthService to test expiration logic. The same concept extends to LLM pipelines: JEV's Intent Gate is a gate that blocks GREETING inputs before the embedding step. The Chunk Scorer blocks chunks with similarity < 0.5 before the prompt. Objective criterion → binary decision → block or pass.

🤝 How do you calibrate quality gate thresholds — start conservative and tighten gradually, or set the final target immediately and absorb the initial wave of failures? Drop your approach in the comments.

#QualityGate #ClaudeCode #AIAssistedDevelopment #SoftwareQuality #CyclomaticComplexity #TestCoverage #PythonTesting #AIEngineering #SoftwareEngineering #DevOps #FastAPI #CIcd #GenerativeAI #LLMOps #DevSecOps

---

## 🎨 IMAGE PROMPT

A clean tech illustration on a dark background showing a CI/CD pipeline with three gate checkpoints. The pipeline flows left to right: Code → [Static Gate: radon gauge showing grade A in green] → PR Merge → [Coverage Gate: progress bar at 90% in cyan, with a red X at 71% below the threshold line] → Staging → [Security Gate: shield icon in green]. Below the pipeline: a mirrored LLM pipeline showing Input → [Intent Gate: GREETING blocked with red X, ANSWERABLE passing with green check] → [Chunk Scorer: similarity bars, two below threshold dropped in red, three passing in cyan] → LLM. Minimalist, dark background, neon cyan and green accents with red for failures, professional. 1920x1080, landscape, LinkedIn cover format, no text.
