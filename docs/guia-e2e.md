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

## Modulo 4: Pull Request Review

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 5: Issue Analysis

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 6: Prompt Engineering

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 7: Context Engineering

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 8: OWASP Top 10

*(em breve — será preenchido quando o módulo for concluído)*

---

## Modulo 9: Quality Gate

*(em breve — será preenchido quando o módulo for concluído)*

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
