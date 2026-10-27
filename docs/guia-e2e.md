# Guia E2E — Testando o Projeto Completo

Este guia percorre os 15 módulos do AIAD em sequência usando um **projeto de prova único**:
um sistema de autenticação JWT com endpoints de login e logout.

A ideia é simples: você pega o mesmo projeto e aplica cada módulo sobre ele — ao final dos 15, terá um ciclo completo de desenvolvimento assistido por IA, do ambiente à arquitetura.

> **Por que autenticação JWT?**
> É um domínio técnico real, tem regras de segurança observáveis, envolve banco de dados, API e lógica de negócio — o suficiente para exercitar todos os módulos sem ser trivial.

---

## Pré-requisitos

Antes de começar:

```bash
# 1. Instalar o Claude Code
npm install -g @anthropic-ai/claude-code

# 2. Clonar o repositório
git clone https://github.com/ntitsolutins01/sfw-development-ai.git
cd sfw-development-ai

# 3. Configurar a chave de API
export ANTHROPIC_API_KEY=sua-chave-aqui        # Linux/Mac
$env:ANTHROPIC_API_KEY="sua-chave-aqui"        # Windows PowerShell

# 4. Abrir o projeto no Claude Code
claude
```

---
<a id="modulo1"></a>
## Modulo 1 Claude Code e Cursor

**Objetivo:** configurar seu ambiente de desenvolvimento assistido por IA do zero.

**O que você vai fazer:**

1. Copie `modules/01-claude-code-cursor/01-configuracao/settings.example.json` para `.claude/settings.json` no seu projeto de prova
2. Copie `modules/01-claude-code-cursor/02-context-engineering/exemplos/CLAUDE.md.api-python` como base para o `CLAUDE.md` do projeto de prova — adapte para o sistema de autenticação
3. Copie a skill `code-review` de `modules/01-claude-code-cursor/03-skills/exemplos/code-review/` para `.claude/skills/code-review/` no projeto de prova
4. Copie `modules/01-claude-code-cursor/04-rules/exemplos/seguranca.md` para `.claude/rules/seguranca.md` — ela vai guiar decisões de segurança nos módulos seguintes
5. Abra o Claude Code no projeto de prova e confirme que as configurações foram aplicadas

**O que valida a conclusão:**
- [ ] `claude --version` retorna sem erro
- [ ] `.claude/settings.json` existe com ao menos uma permissão configurada
- [ ] `CLAUDE.md` existe na raiz do projeto de prova com regras do sistema de autenticação
- [ ] `/code-review` responde no Claude Code
- [ ] `seguranca.md` está ativa em `.claude/rules/`

**[Referência completa](../modules/01-claude-code-cursor/README.md)**

---

## Modulo 2 Spec Driven Development

**Objetivo:** escrever a especificação do sistema de autenticação antes de qualquer linha de código.

**O que você vai fazer:**

1. No Claude Code do projeto de prova, execute:
   ```
   /brainstorm sobre sistema de autenticação JWT com login e logout
   ```
   Leia o resultado e identifique decisões técnicas em aberto.

2. Copie o template de `modules/02-spec-driven-development/03-templates/feature.md` para `docs/specs/001-autenticacao-jwt.md` no projeto de prova

3. Preencha o spec. Critérios de aceite obrigatórios para este guia:
   - `POST /auth/login` retorna token JWT com credenciais corretas
   - `POST /auth/login` retorna 401 com credenciais incorretas (mesmo erro para e-mail inexistente)
   - Token expira em 24 horas
   - `POST /auth/logout` invalida o token na blocklist
   - Endpoint protegido rejeita token da blocklist

4. Abra `modules/02-spec-driven-development/04-ia-no-fluxo/README.md` → use o **Prompt 1** para revisar o spec. A IA vai apontar gaps e ambiguidades.

5. Corrija o spec com base na revisão.

**O que valida a conclusão:**
- [ ] `docs/specs/001-autenticacao-jwt.md` existe com todos os CAs preenchidos
- [ ] A IA revisou o spec e os gaps foram resolvidos
- [ ] Cada CA é verificável: sim ou não, sem ambiguidade

**[Referência completa](../modules/02-spec-driven-development/README.md)**

---

## Modulo 3 TDD

**Objetivo:** escrever os testes do spec antes de qualquer implementação e implementar para fazê-los passar.

**O que você vai fazer:**

1. Abra `modules/03-tdd/04-ia-no-fluxo/README.md` → use o **Prompt 1**. Cole os CAs do spec `001-autenticacao-jwt.md` e peça para a IA gerar os casos de teste em pytest.

2. Salve o arquivo gerado em `tests/test_auth_service.py` no projeto de prova.

3. Rode os testes e confirme que **todos falham** (Red):
   ```bash
   pytest tests/test_auth_service.py
   ```
   Se algum passar antes da implementação, o teste está errado — investigue.

4. Use o **Prompt 2** de `04-ia-no-fluxo/`. Cole o arquivo de testes e peça a implementação mínima. A IA vai criar `app/services/auth.py`.

5. Rode os testes novamente e confirme que **todos passam** (Green):
   ```bash
   pytest tests/test_auth_service.py
   ```

6. Use o **Prompt 3** para refatorar. Rode os testes após cada mudança.

7. Use o **Prompt 6** para verificar gaps — compare os testes com os CAs do spec.

**O que valida a conclusão:**
- [ ] Todos os CAs do spec têm ao menos dois testes (caso feliz + caso de falha)
- [ ] `pytest` mostrou falhas antes da implementação (Red confirmado)
- [ ] `pytest` mostra 100% verde após a implementação
- [ ] O refactor foi feito e os testes continuaram passando

**[Referência completa](../modules/03-tdd/README.md)**

---

## Modulo 4 Pull Request Review

**Objetivo:** revisar o código do Módulo 3 contra o spec do Módulo 2, verificar cobertura de testes e emitir uma decisão formal de aprovação.

**O que você vai fazer:**

1. Instale a skill `/review-pr` no projeto de prova:
   Copie `modules/04-pull-request-review/../../../.claude/skills/review-pr/SKILL.md` para `.claude/skills/review-pr/SKILL.md` no projeto de prova

2. Abra `modules/04-pull-request-review/03-templates/checklist-feature.md` e percorra cada item para o branch do JWT (resultado do Módulo 3)

3. No Claude Code com o branch `feature/autenticacao-jwt` ativo, execute:
   ```
   /code-review
   ```
   Corrija todos os achados CRÍTICO e ALTO antes de continuar.

4. Execute a revisão com spec:
   ```
   /review-pr docs/specs/001-autenticacao-jwt.md
   ```
   Corrija os CAs marcados como AUSENTE ou PARCIAL.

5. Re-execute `/review-pr` após as correções até obter `APROVADO`.

**O que valida a conclusão:**
- [ ] Checklist de self-review percorrido sem itens abertos
- [ ] `/code-review` executado — zero CRÍTICO, zero ALTO no resultado final
- [ ] `/review-pr` retorna APROVADO com todos os 5 CAs do spec marcados como cobertos
- [ ] `pytest` passando 100% após as correções

**[Referência completa](../modules/04-pull-request-review/README.md)**

---

## Modulo 5 Issue Analysis

**Objetivo:** usar IA para analisar uma issue mal definida, decompô-la em tasks atômicas com critérios de aceite verificáveis e gerar o stub de spec pronto para o Módulo 2.

**O que você vai fazer:**

1. Copie a skill `/analyze-issue` para o projeto de prova:
   Copie `.claude/skills/analyze-issue/SKILL.md` para `.claude/skills/analyze-issue/SKILL.md` no projeto de prova

2. Crie uma issue bruta de exemplo no projeto de prova (use este texto como ponto de partida):
   ```
   [FEAT] Adicionar suporte a refresh token

   Usuários ficam deslogados após 24h. Precisamos de refresh token
   para que a sessão seja renovada automaticamente.
   Prioridade: Média
   ```

3. Execute a análise de issue:
   ```
   /analyze-issue
   ```
   Cole o texto da issue quando solicitado. A IA vai classificar o tipo, identificar ambiguidades e fazer perguntas de clarificação.

4. Responda as perguntas de clarificação (ou peça para a IA assumir valores razoáveis). Use as perguntas de `modules/05-issue-analysis/04-ia-no-fluxo/README.md` como referência se preferir o fluxo manual.

5. Confirme a decomposição em tasks: a IA deve produzir ao menos 2 tasks atômicas com CAs no formato `dado/quando/então`.

6. Ao final, a IA vai gerar e salvar o arquivo `docs/specs/002-refresh-token.md` — verifique se o stub tem os campos obrigatórios (contexto, escopo, CAs, campos em aberto).

**O que valida a conclusão:**
- [ ] Issue classificada como Feature com tipo e escopo definidos
- [ ] Ao menos 2 tasks atômicas identificadas, cada uma testável em isolamento
- [ ] Cada task tem ao menos 1 CA para caso feliz e 1 para caso de falha
- [ ] `docs/specs/002-refresh-token.md` existe com CAs numerados (CA-1, CA-2...)
- [ ] Os campos em aberto do spec estão listados (prontos para o Módulo 2 completar)

**[Referência completa](../modules/05-issue-analysis/README.md)**

---

## Modulo 6 Prompt Engineering

**Objetivo:** aprender o framework CIFER e as 6 técnicas de engenharia de prompts para melhorar a qualidade de todas as interações com o Claude Code no ciclo AIAD.

**O que você vai fazer:**

1. Leia `modules/06-prompt-engineering/01-conceito/README.md` e identifique nos seus prompts atuais quais componentes do CIFER estão ausentes

2. Pegue um prompt que você usou nos módulos anteriores (ex: "gere testes para o auth service") e reescreva usando o template em `modules/06-prompt-engineering/03-templates/prompt-geracao-codigo.md`

3. Compare as duas respostas (prompt original vs. com CIFER) e identifique a diferença de precisão

4. Estude os comparativos de `modules/06-prompt-engineering/05-exemplos/`:
   - `antes-depois-geracao.md` — verify_token: prompt vago vs. CIFER completo
   - `antes-depois-debug.md` — token 401: lista genérica vs. chain-of-thought
   - `antes-depois-refatoracao.md` — AuthService: sem restrições vs. constrained

5. Aplique chain-of-thought em um bug real: se o seu sistema JWT tiver qualquer comportamento inesperado, use o template `prompt-debug.md` com a instrução "analise passo a passo antes de sugerir a correção"

6. Consulte a tabela "Onde cada técnica se encaixa" em `modules/06-prompt-engineering/02-workflow/README.md` e marque quais técnicas você usará em cada módulo restante

**O que valida a conclusão:**
- [ ] Framework CIFER identificado nos seus prompts — você sabe qual componente costuma faltar
- [ ] Ao menos um prompt reescrito com CIFER produziu resposta melhor na primeira tentativa
- [ ] Você consegue dizer quando usar few-shot vs. chain-of-thought vs. role prompting
- [ ] Comparativos antes/depois lidos — você identificou o anti-padrão em cada um

**[Referência completa](../modules/06-prompt-engineering/README.md)**

---

## Modulo 7 Context Engineering

**Objetivo:** estruturar as 4 camadas de contexto do Claude Code para que cada sessão comece com informação relevante e termine com o estado persistido — sem precisar re-explicar o projeto toda vez.

**O que você vai fazer:**

1. Leia `modules/07-context-engineering/01-conceito/README.md` — identifique quais das 4 camadas (memory, rules, CLAUDE.md, conversa) você já usa no projeto de prova e quais estão faltando

2. Revise o CLAUDE.md do projeto de prova usando o template em `modules/07-context-engineering/03-templates/claude-md-projeto.md`. Verifique se tem: stack, estrutura de pastas, regras de desenvolvimento, status atual e instrução de retomada

3. Abra uma nova sessão do Claude Code no projeto de prova e use o prompt de `modules/07-context-engineering/03-templates/prompt-retomada.md` para iniciar. Confirme que o modelo consegue responder corretamente: o que foi feito, o que falta, em qual arquivo trabalhar

4. Execute uma sessão de trabalho curta (implementar ou corrigir algo pequeno no JWT). Quando a sessão tiver >30 trocas, execute `/compact` e depois verifique se o modelo ainda conhece os CAs pendentes

5. Estude `modules/07-context-engineering/05-exemplos/multiplos-agentes.md` — identifique uma situação no seu projeto onde um fresh agent independente seria mais útil do que continuar na mesma sessão

6. Ao encerrar, use `/salvar-contexto` para persistir nos 3 mecanismos e verifique que a seção "Próxima sessão" do PROGRESS.md está específica o suficiente para uma boa retomada

**O que valida a conclusão:**
- [ ] CLAUDE.md do projeto de prova tem as 5 seções mínimas (stack, estrutura, regras, status, retomada)
- [ ] Prompt de retomada usado com sucesso — modelo confirmou o contexto antes de começar
- [ ] `/compact` executado e contexto essencial verificado após compactação
- [ ] Você sabe distinguir: quando usar `/compact` vs nova sessão vs fork vs fresh agent

**[Referência completa](../modules/07-context-engineering/README.md)**

---

## Modulo 8 OWASP Top 10

**Objetivo:** auditar o sistema JWT contra as 10 categorias OWASP, identificar vulnerabilidades com severidade, corrigir CRÍTICO e ALTO antes do deploy.

**O que você vai fazer:**

1. Copie a skill `/audit-owasp` para o projeto de prova:
   Copie `.claude/skills/audit-owasp/SKILL.md` para `.claude/skills/audit-owasp/SKILL.md` no projeto de prova

2. Leia `modules/08-owasp-top-10/01-conceito/README.md` — identifique quais das 6 categorias mapeadas para o projeto JWT você já mitigou (M3+M4) e quais precisam ser verificadas

3. Execute a auditoria no arquivo principal de autenticação:
   ```
   /audit-owasp app/services/auth.py
   ```
   Aguarde o relatório estruturado com achados por categoria (A01–A10)

4. Leia os exemplos em `modules/08-owasp-top-10/05-exemplos/` para entender os padrões dos 3 achados mais comuns no projeto JWT (A01, A02, A07)

5. Para cada achado CRÍTICO e ALTO, peça a correção diretamente ao Claude Code usando o template de `modules/08-owasp-top-10/03-templates/audit-owasp.md` — seção "Template de Prompt para Correção"

6. Após cada correção, re-execute `/audit-owasp` no arquivo corrigido e rode `pytest` para confirmar que nada quebrou

7. Documente os achados MÉDIO em `docs/security/findings/` usando o template `modules/08-owasp-top-10/03-templates/finding-report.md`

**O que valida a conclusão:**
- [ ] Auditoria executada em ao menos 2 arquivos (ex: `auth.py` e o router de autenticação)
- [ ] Zero CRÍTICO e zero ALTO nos arquivos auditados após as correções
- [ ] `pytest` passando 100% após todas as correções
- [ ] Ao menos 1 achado MÉDIO documentado em `docs/security/findings/`
- [ ] Você sabe explicar a diferença entre A01 (controle de acesso) e A07 (falhas de autenticação)

**[Referência completa](../modules/08-owasp-top-10/README.md)**

---

## Modulo 9 Quality Gate

**Objetivo:** configurar quality gates (cobertura, complexidade, segurança) no projeto JWT, integrá-los ao GitHub Actions, e entender como o mesmo conceito se aplica a pipelines LLM.

**O que você vai fazer:**

1. Copie a skill `/quality-gate` para o projeto de prova:
   Copie `.claude/skills/quality-gate/SKILL.md` para `.claude/skills/quality-gate/SKILL.md` no projeto de prova

2. Execute `/quality-gate` sem configuração prévia — a skill vai reportar todos os gates como AUSENTE e medir o estado atual. Anote a cobertura atual antes de configurar qualquer threshold

3. Configure o gate de cobertura no projeto de prova:
   - Copie o template de `modules/09-quality-gate/03-templates/pytest-cov.md` para `pyproject.toml`
   - Defina o threshold como (cobertura medida no passo 2) − 5%
   - Rode `pytest` e confirme que o gate passa com o threshold inicial

4. Configure o gate de complexidade:
   - Instale radon: `pip install radon`
   - Rode `radon cc app/ -s -a` e identifique as funções com maior complexidade
   - Se alguma função estiver em grade D ou F, refatore antes de configurar o gate
   - Adicione o target `complexity-check` ao Makefile usando o template de `03-templates/radon-complexity.md`

5. Execute `/quality-gate` novamente — desta vez os gates de cobertura e complexidade devem estar CONFIGURADOS. Confirme que ambos passam

6. Gere o workflow de GitHub Actions:
   - Copie o template de `modules/09-quality-gate/03-templates/github-actions-gates.md`
   - Salve em `.github/workflows/quality-gates.yml` no projeto de prova
   - Faça um commit — o workflow deve aparecer na aba Actions do GitHub

7. Leia `modules/09-quality-gate/05-exemplos/llm-pipeline-gate.md` e identifique onde no seu pipeline (se tiver um) um Intent Gate ou Chunk Scorer faria sentido

**O que valida a conclusão:**
- [ ] `/quality-gate` executado — cobertura e complexidade reportados como PASSOU
- [ ] `pyproject.toml` tem threshold de coverage configurado
- [ ] Makefile tem target `quality` que roda todos os gates
- [ ] `.github/workflows/quality-gates.yml` criado e gates passando no CI
- [ ] Você sabe explicar por que "gate que só avisa" não é um gate

**[Referência completa](../modules/09-quality-gate/README.md)**

---

## Modulo 10: Analises de Seguranca

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 11: Loop Engineering

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 12: Hermes Agent

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 13: Observabilidade

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 14: LLM as a Judge

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 15: Arquitetura

*(em breve — será preenchido quando o módulo for concluído)*

---

## Critério de conclusão do projeto

O projeto AIAD está testado e2e quando:

- [ ] Os 15 módulos deste guia estão preenchidos (sem `em breve`)
- [ ] O sistema de autenticação JWT foi especificado (Módulo 2), testado (Módulo 3), revisado em PR (Módulo 4), analisado em segurança (Módulos 8 e 10) e observado em produção (Módulo 13)
- [ ] Todos os checklists de validação acima estão marcados
