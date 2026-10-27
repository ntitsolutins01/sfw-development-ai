# OWASP Top 10 — Módulo 8

> Gerado em: 2026-10-26
> Skill: `/salvar-contexto` → Módulo concluído
> Tema: Módulo 8 — OWASP Top 10

---

## 💬 Comentário

**PT:** Módulo 8 do AIAD publicado: OWASP Top 10 com IA. Pipeline `/audit-owasp`, 3 achados concretos no projeto JWT (A01 IDOR + A02 algoritmo none + A07 sem rate limit invisível) e por que cada um passa em code review. [link deste post] | Série: [link do post de lançamento]

**EN:** AIAD Module 8 is live: OWASP Top 10 with AI. The `/audit-owasp` pipeline, 3 concrete findings in the JWT project (A01 IDOR + A02 none algorithm + A07 invisible brute force) and why each one passes code review. [link deste post] | Series: [link do post de lançamento]

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

Documentei como auditar código contra o OWASP Top 10 com Claude Code — não como checklist, mas como pipeline de análise sistemática.

🔐 O problema: auditorias OWASP manuais são lentas e inconsistentes. O auditor conhece as 10 categorias mas precisa lembrar os sub-padrões de cada uma enquanto lê o código. Três achados no projeto JWT ilustram o custo: A01 — `/user/profile` sem autenticação, qualquer `user_id` no parâmetro retorna o perfil de qualquer usuário (IDOR puro). A02 — `JWT_SECRET = "secret"` com 6 caracteres + `algorithms=["HS256", "none"]` na validação do token; o segundo é devastador: com algoritmo `none`, o servidor aceita tokens sem assinatura — o atacante constrói `header.payload.` com qualquer `user_id` e nenhuma criptografia envolvida. A07 — `POST /auth/login` sem rate limiting e sem logging; brute force com wordlist de senhas comuns é completamente invisível porque nenhuma tentativa falha gera log. Esses três achados passam em code review porque cada linha individualmente parece intencional.

🕵️ O Módulo 8 documenta o pipeline `/audit-owasp`: 5 etapas (scan → analyze → triage → fix → verify) aplicadas em uma única invocação. Para cada uma das 10 categorias OWASP, a skill aplica critérios específicos — A02 verifica segredo hardcoded, tamanho mínimo (32 chars), e lista de algoritmos aceitos; A07 verifica rate limiting, campo `exp` no JWT, e presença de logs estruturados com IP+email+timestamp. O relatório sai com severidade por categoria (CRÍTICO → INFO), o vetor de ataque em passos concretos, e a oferta de gerar a correção com teste imediatamente. A correção do A02 com algoritmo `none` é uma mudança de 1 linha (`"none"` removido da lista) — o valor está em saber que aquela linha existe e o que ela permite.

🚨 Qual foi o achado OWASP mais insidioso que você encontrou — o tipo que passa em code review porque parece intencional? Conta nos comentários.

#OWASP #WebSecurity #ClaudeCode #AIAssistedDevelopment #AppSec #JWT #PythonSecurity #AIEngineering #SoftwareEngineering #SecurityTesting #FastAPI #GenerativeAI #LLMOps #CyberSecurity #DevSecOps

---

## 📝 PUBLICAÇÃO — ENGLISH

I documented how to audit code against OWASP Top 10 with Claude Code — not as a checklist, but as a systematic analysis pipeline.

🔐 The problem: manual OWASP audits are slow and inconsistent. Three findings in the JWT project show the cost. A01 — `/user/profile` with no authentication, any `user_id` in the query param returns that user's profile (textbook IDOR). A02 — `JWT_SECRET = "secret"` (6 characters) plus `algorithms=["HS256", "none"]` in token validation; the second one is devastating: with algorithm `none`, the server accepts unsigned tokens — the attacker builds `header.payload.` with any `user_id` and no cryptography involved. A07 — `POST /auth/login` with no rate limiting and no logging; a credential stuffing attack against a wordlist of common passwords is completely invisible because no failed attempt generates a log. All three pass code review because every individual line looks intentional.

🕵️ Module 8 documents the `/audit-owasp` pipeline: 5 steps (scan → analyze → triage → fix → verify) applied in a single invocation. For each of the 10 OWASP categories, the skill applies specific criteria — A02 checks for hardcoded secrets, minimum length (32 chars), and the accepted algorithms list; A07 checks for rate limiting, `exp` field in JWT, and structured logging with IP+email+timestamp. The report comes out with severity per category (CRITICAL → INFO), the attack vector in concrete steps, and an offer to generate the fix with a test immediately. The A02 fix for algorithm `none` is a one-line change (`"none"` removed from the list) — the value is knowing that line exists and what it permits.

🚨 What's the most insidious OWASP finding you've encountered — the kind that passes code review because it looks intentional? Drop it in the comments.

#OWASP #WebSecurity #ClaudeCode #AIAssistedDevelopment #AppSec #JWT #PythonSecurity #AIEngineering #SoftwareEngineering #SecurityTesting #FastAPI #GenerativeAI #LLMOps #CyberSecurity #DevSecOps

---

## 🎨 IMAGE PROMPT

A clean tech illustration on a dark background showing a security audit pipeline. On the left: a Python code file with three highlighted vulnerability zones glowing in red (one labeled "A01 IDOR", one "A02 none algorithm", one "A07 no rate limit"). In the center: a vertical pipeline with 5 labeled stages — SCAN, ANALYZE, TRIAGE, FIX, VERIFY — each connected by glowing arrows. On the right: a structured report panel showing a severity matrix (CRITICAL in red, HIGH in orange, MEDIUM in yellow, LOW in green). Minimalist, dark background, neon red and cyan accents, professional. 1920x1080, landscape, LinkedIn cover format, no text.
