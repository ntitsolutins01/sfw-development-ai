## 🤖 DAPIA — Desenvolvimento de Software com IA

> Repositório de referência do curso **DAPIA** (Pythonando): 15 módulos práticos que cobrem o ciclo completo de desenvolvimento de software assistido por inteligência artificial — do ambiente de trabalho com Claude Code até arquitetura orientada por IA.

![Claude Code](https://img.shields.io/badge/Claude_Code-CLI-D97757?style=for-the-badge&logo=anthropic&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=for-the-badge&logo=node.js&logoColor=white)
![DAPIA](https://img.shields.io/badge/Curso-DAPIA-7C3AED?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📑 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura](#️-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Quick Start](#️-quick-start)
- [Módulos](#-módulos)
- [Biblioteca Compartilhada](#-biblioteca-compartilhada)
- [Skills do Projeto](#️-skills-do-projeto)
- [Documentação](#-documentação)
- [Autor](#-autor)

---

## 📌 Sobre o Projeto

Repositório educacional com 15 módulos práticos do curso **DAPIA**. Cada módulo aborda um aspecto do desenvolvimento de software moderno assistido por IA — desde configurar o ambiente com Claude Code até construir agentes autônomos, pipelines RAG e sistemas com observabilidade.

Os módulos são independentes e progressivos. Você pode estudar em sequência ou ir direto ao módulo que precisar.

> 📖 Para retomar uma sessão de trabalho anterior, leia o [`PROGRESS.md`](PROGRESS.md).

---

## 🏗️ Arquitetura

```text
sfw-development-ai/
├── 📄 README.md
├── 📄 CLAUDE.md                          # Contexto e regras do projeto para a IA
├── 📄 PROGRESS.md                        # Registro de sessões e próximos passos
├── 📁 .claude/
│   ├── 📄 settings.json                  # Permissões do Claude Code
│   └── 📁 skills/                        # Skills do projeto
│       ├── brainstorm/                   # Maturação de ideias pré-spec
│       ├── escrever-prd/                 # Product Requirements Document
│       ├── escrever-trd/                 # Technical Requirements Document
│       ├── gerar-post/                   # Publicações LinkedIn
│       └── salvar-contexto/              # Persistência de sessão
├── 📁 modules/
│   ├── 01-claude-code-cursor/            # Fundação: configuração, skills, rules, MCP, subagents
│   ├── 02-spec-driven-development/       # Especificações: brainstorm → PRD → TRD → spec
│   ├── 03-tdd/                           # Test-Driven Development com IA
│   ├── 04-pull-request-review/           # Revisão de PR assistida por IA
│   ├── 05-issue-analysis/                # Análise de issues com IA
│   ├── 06-prompt-engineering/            # Engenharia de prompts
│   ├── 07-context-engineering/           # Engenharia de contexto
│   ├── 08-owasp-top-10/                  # Segurança: OWASP Top 10
│   ├── 09-quality-gate/                  # Quality gates em pipelines
│   ├── 10-security-analysis/             # Análise de segurança
│   ├── 11-loop-engineering/              # Loop engineering
│   ├── 12-hermes-agent/                  # Agente Hermes
│   ├── 13-observability/                 # Observabilidade
│   ├── 14-llm-as-judge/                  # LLM como avaliador
│   └── 15-architecture/                  # Arquitetura orientada por IA
├── 📁 shared/                            # Biblioteca interna reutilizável
│   ├── prompt-caching/                   # KV-cache para chamadas à API Anthropic
│   └── jev/                              # Camada de decisão: Intent Gate + Chunk Scorer
└── 📁 docs/                              # Documentação, specs, PRDs, TRDs e posts
```

---

## 🔧 Pré-requisitos

| Ferramenta | Versão mínima | Instalação |
|------------|---------------|------------|
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org) |
| **Claude Code CLI** | mais recente | `npm install -g @anthropic-ai/claude-code` |
| **Python** | 3.11+ | [python.org](https://python.org) (módulos 12–14) |
| **ANTHROPIC_API_KEY** | — | [console.anthropic.com](https://console.anthropic.com) |

---

## ▶️ Quick Start

### 1️⃣ Instalar o Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

### 2️⃣ Clonar o repositório

```bash
git clone https://github.com/ntitsolutins01/sfw-development-ai.git
cd sfw-development-ai
```

### 3️⃣ Configurar a chave de API

```bash
# Defina a variável de ambiente com sua chave Anthropic
export ANTHROPIC_API_KEY=sua-chave-aqui   # Linux/Mac
$env:ANTHROPIC_API_KEY="sua-chave-aqui"   # Windows PowerShell
```

### 4️⃣ Abrir o projeto no Claude Code

```bash
claude
```

O Claude Code lerá automaticamente o `CLAUDE.md` e carregará o contexto do projeto.

### 5️⃣ Começar pelo Módulo 1

```
Leia o README de modules/01-claude-code-cursor/ e me ajude a configurar o ambiente
```

---

## 📚 Módulos

| # | Módulo | Status | O que você aprende |
|---|--------|--------|-------------------|
| 1 | [Claude Code e Cursor](modules/01-claude-code-cursor/) | ✅ Concluído | Configuração, skills, rules, MCP servers, subagents |
| 2 | [Spec Driven Development](modules/02-spec-driven-development/) | ✅ Concluído | Brainstorm → PRD → TRD → spec → implementação → validação |
| 3 | TDD | — | Ciclo red-green-refactor assistido por IA |
| 4 | Pull Request Review | — | Revisão automática com checklist e severidade |
| 5 | Issue Analysis | — | Análise e decomposição de issues com IA |
| 6 | Prompt Engineering | — | Técnicas avançadas de engenharia de prompts |
| 7 | Context Engineering | — | Gerenciamento de contexto em sessões longas |
| 8 | OWASP Top 10 | — | Identificação e mitigação de vulnerabilidades |
| 9 | Quality Gate | — | Portões de qualidade em pipelines de software |
| 10 | Análises de Segurança | — | Análise estática e dinâmica de segurança |
| 11 | Loop Engineering | — | Loops autônomos e self-healing com IA |
| 12 | Hermes Agent | — | Agente autônomo com memória e ferramentas |
| 13 | Observabilidade | — | Logs, métricas e traces em sistemas com IA |
| 14 | LLM as a Judge | — | Avaliação de qualidade de respostas com LLM |
| 15 | Arquitetura | — | Padrões de arquitetura orientados por IA |

---

## 📦 Biblioteca Compartilhada

Módulos reutilizáveis usados pelos módulos 12, 13 e 14. Não são módulos do curso — são implementações de referência.

| Biblioteca | Localização | O que faz |
|-----------|-------------|-----------|
| **Prompt Caching** | [`shared/prompt-caching/`](shared/prompt-caching/) | KV-cache da API Anthropic: reduz latência e custo reutilizando system prompts estáticos entre chamadas |
| **JEV** | [`shared/jev/`](shared/jev/) | Camada de decisão pré-LLM: Intent Gate classifica inputs (GREETING/META/ANSWERABLE) e Chunk Scorer filtra contexto irrelevante antes da chamada ao modelo |

---

## 🛠️ Skills do Projeto

Skills disponíveis em `.claude/skills/` — invoque pelo nome como mensagem no Claude Code.

| Skill | Como invocar | O que faz |
|-------|-------------|-----------|
| **brainstorm** | `/brainstorm sobre <tema>` | Matura ideias, aponta trade-offs, não implementa nada até você pedir |
| **escrever-prd** | `/escrever-prd` | Gera PRD em `docs/prds/` com user stories, critérios de aceite e métricas |
| **escrever-trd** | `/escrever-trd` | Cria/atualiza `docs/trd.md` com stack, arquitetura, NFRs e ADRs |
| **gerar-post** | `/gerar-post sobre <tema>` | Gera publicação LinkedIn em PT e EN com prompt de imagem |
| **salvar-contexto** | `/salvar-contexto` | Salva o estado da sessão nos 3 mecanismos de persistência do projeto |

---

## 🗺️ Progresso

```text
✅ Módulo 1  — Claude Code e Cursor
✅ Módulo 2  — Spec Driven Development
—  Módulo 3  — TDD
—  Módulo 4  — Pull Request Review
—  Módulo 5  — Issue Analysis
—  Módulo 6  — Prompt Engineering
—  Módulo 7  — Context Engineering
—  Módulo 8  — OWASP Top 10
—  Módulo 9  — Quality Gate
—  Módulo 10 — Análises de Segurança
—  Módulo 11 — Loop Engineering
—  Módulo 12 — Hermes Agent
—  Módulo 13 — Observabilidade
—  Módulo 14 — LLM as a Judge
—  Módulo 15 — Arquitetura
```

> Para ver o histórico detalhado de sessões e o que está planejado para a próxima: [`PROGRESS.md`](PROGRESS.md)

---

## 📖 Documentação

| Documento | Descrição |
|-----------|-----------|
| 📄 [CLAUDE.md](CLAUDE.md) | Contexto, regras e status dos módulos para o Claude Code |
| 📄 [PROGRESS.md](PROGRESS.md) | Registro cronológico de sessões e próximos passos |
| 📄 [Como salvar contexto](docs/como-salvar-contexto.md) | Os 3 mecanismos de persistência de sessão do projeto |
| 📦 [Prompt Caching](shared/prompt-caching/README.md) | Como usar o KV-cache da API Anthropic |
| 🧭 [JEV — Camada de Decisão](shared/jev/README.md) | Intent Gate e Chunk Scorer: evitando chamadas desnecessárias ao LLM |

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um **fork** do repositório
2. Criar uma branch: `git checkout -b modulo/nome-do-modulo`
3. Fazer o commit: `git commit -m "feat: adiciona módulo X"`
4. Fazer o push: `git push origin modulo/nome-do-modulo`
5. Abrir um **Pull Request** 🚀

---

## 👤 Autor

Feito com 💙 por **Fábio Muniz**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/fabiomunizdeveloper/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/ntitsolutins01?tab=repositories)

---

**Versão:** 1.0.0 · **Status:** 🚧 Em desenvolvimento · **Módulos concluídos:** 2/15
