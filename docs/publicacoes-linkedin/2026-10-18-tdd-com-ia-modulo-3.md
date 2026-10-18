# TDD com IA — Módulo 3 AIAD

> Gerado em: 2026-10-18
> Skill: `/gerar-post`
> Tema: Módulo 3 — TDD com IA: ciclo red-green-refactor assistido por IA com specs do Módulo 2

---

## 💬 Comentário

> Postar como comentário no post de lançamento da série (https://lnkd.in/p/dpJ8fi3V):

**PT:** Módulo 3 publicado — TDD com IA: ciclo red-green-refactor com 6 prompts prontos, 3 templates (unit-pytest, unit-jest, integration-pytest) e 3 exemplos reais ligados aos specs do Módulo 2. Verificação binária: verde ou vermelho, sem interpretação. [link deste post]

**EN:** Module 3 is up — TDD with AI: red-green-refactor cycle with 6 ready prompts, 3 templates (unit-pytest, unit-jest, integration-pytest), and 3 real examples linked to Module 2 specs. Binary verification: green or red, no room for interpretation. [link deste post]

---

## 📝 PUBLICAÇÃO — PORTUGUÊS

Adicionei o Módulo 3 ao AIAD — TDD com IA muda o critério de verificação de subjetivo para objetivo.

🧪 O problema: quando você pede para uma IA implementar uma feature sem testes, a verificação é subjetiva — você lê o código e decide se parece certo. A IA pode gerar algo plausível que não satisfaz os requisitos. TDD inverte isso: os testes definem o contrato antes de qualquer linha de produção. Você fornece os critérios de aceite do spec (Módulo 2), a IA gera os casos de teste com o Prompt 1, você confirma que todos falham — só então a IA implementa. O critério de sucesso é binário: verde ou vermelho. Não há espaço para interpretação.

🔍 O módulo tem 6 prompts prontos para cada fase do ciclo: Prompt 1 transforma CAs em testes (Red), Prompt 2 implementa o mínimo para fazê-los passar (Green), Prompt 3 refatora sem quebrar testes (Refactor), Prompt 4 gera mocks para dependências externas, Prompt 5 cria fixtures e factories, Prompt 6 identifica gaps de cobertura comparando testes com o spec original. Três templates de teste (unit-pytest, unit-jest, integration-pytest) seguem o padrão Arrange/Act/Assert com comentários que a IA lê ao revisar. Três exemplos reais — autenticação JWT, validação de upload, GET /users/{id} — percorrem o ciclo completo ligados diretamente aos specs do Módulo 2.

💡 A IA não improvisa onde não deve quando os testes dizem exatamente o que deve ser verdade. Qual é o custo de pedir para a IA implementar sem testes no seu workflow? O retrabalho, o código correto que resolve o problema errado, ou algo diferente? Troca nos comentários.

#TDD #TestDrivenDevelopment #ClaudeCode #AIEngineering #SpecDrivenDevelopment #pytest #jest #SoftwareQuality #GenerativeAI #LLMOps #SoftwareEngineering #DevWorkflow #Python #TypeScript #AIAD

---

## 📝 PUBLICAÇÃO — ENGLISH

Added Module 3 to AIAD — TDD with AI shifts verification from subjective to objective.

🧪 The problem: when you ask an AI to implement without tests, verification is subjective — you read the code and decide if it looks right. The AI can produce something plausible that doesn't actually satisfy the requirements. TDD flips this: tests define the contract before any production code exists. You provide acceptance criteria from the spec (Module 2), the AI generates test cases using Prompt 1, you confirm every test fails — then the AI implements. The success criterion is binary: green or red. No room for interpretation.

🔍 The module ships with 6 prompts for each phase of the TDD cycle: Prompt 1 converts acceptance criteria into failing tests (Red), Prompt 2 implements the minimum to make them pass (Green), Prompt 3 refactors without breaking tests (Refactor), Prompt 4 generates mocks for external dependencies, Prompt 5 creates fixtures and factories, Prompt 6 identifies coverage gaps by comparing the test suite against the original spec. Three test templates (unit-pytest, unit-jest, integration-pytest) follow the Arrange/Act/Assert pattern with section comments the AI reads when reviewing. Three real worked examples — JWT auth, upload validation, GET /users/{id} — trace the full Red→Green→Refactor cycle, each linked directly to specs from Module 2.

💡 The AI doesn't improvise where it shouldn't when the tests say exactly what must be true. What's the real cost of asking AI to implement without tests in your workflow — rework, correct code solving the wrong problem, or something else? Drop it in the comments.

#TDD #TestDrivenDevelopment #ClaudeCode #AIEngineering #SpecDrivenDevelopment #pytest #jest #SoftwareQuality #GenerativeAI #LLMOps #SoftwareEngineering #DevWorkflow #Python #TypeScript #AIAD

---

## 🎨 IMAGE PROMPT

A clean tech illustration on a dark background showing a circular TDD cycle with three nodes: a red glowing circle labeled with a failing test icon, a green glowing circle with a checkmark representing passing tests, and a blue/purple node representing refactored code connected back to the first. In the center of the cycle, a neon-outlined document icon represents the spec/acceptance criteria feeding into the loop. To the right, a vertical stack of six faintly glowing prompt blocks numbered 1–6 in neon cyan, connected by a thin arrow to the cycle entrance. The overall composition suggests a closed-loop, contract-driven development process driven by structured prompts. Style: clean tech illustration, dark background, neon accents, minimalist, professional, no text. Resolution: 1920x1080, landscape, LinkedIn cover format.
