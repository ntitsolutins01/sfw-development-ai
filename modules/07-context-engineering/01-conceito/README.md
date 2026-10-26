# Conceito — Context Engineering

## O que é Contexto

Em Claude Code, contexto é tudo o que o modelo leva em conta ao gerar uma resposta: a conversa atual, os arquivos lidos, as regras carregadas, a memória do projeto. Diferente de um banco de dados, o contexto é efêmero — o que não está na janela de contexto no momento da resposta simplesmente não existe para o modelo.

Context Engineering é o processo de decidir conscientemente o que entra nessa janela, em que momento, e como garantir que informações importantes persistam entre sessões.

---

## As 4 Camadas de Contexto em Claude Code

```text
┌─────────────────────────────────────────────────────────┐
│  Camada 4: Conversa atual                               │
│  (janela de contexto — efêmero, desaparece ao fechar)   │
├─────────────────────────────────────────────────────────┤
│  Camada 3: CLAUDE.md hierárquico                        │
│  (global → projeto → subpasta — carregado automaticamente)│
├─────────────────────────────────────────────────────────┤
│  Camada 2: Rules (.claude/rules/)                       │
│  (restrições comportamentais — sempre ativas)           │
├─────────────────────────────────────────────────────────┤
│  Camada 1: Memory (.claude/projects/.../memory/)        │
│  (fatos persistentes entre sessões — lidos sob demanda) │
└─────────────────────────────────────────────────────────┘
```

### Camada 1 — Memory

Fatos sobre o projeto que não mudam sessão a sessão: decisões arquiteturais, o que foi construído, convenções estabelecidas. Não é carregada automaticamente — você a referencia explicitamente quando precisar.

**O que vai aqui:** quem é o usuário, o que foi construído em cada módulo, decisões importantes e seus motivos, convenções do projeto.

**O que NÃO vai aqui:** estado temporário da sessão, código específico, histórico de commits, tarefas em andamento.

### Camada 2 — Rules

Instruções comportamentais que se aplicam a toda interação dentro do escopo. Uma rule ativa nunca precisa ser repetida no prompt.

**O que vai aqui:** restrições de segurança (não usar `eval`, sempre validar inputs), padrões de código (type hints em Python, imports organizados), restrições de projeto (nunca commitar `.env`).

**O que NÃO vai aqui:** contexto de negócio, estado do projeto, decisões que mudam por feature.

### Camada 3 — CLAUDE.md

Contexto de projeto carregado automaticamente toda vez que você abre o Claude Code naquela pasta. É o lugar para o que o modelo precisa saber para trabalhar bem neste projeto.

**O que vai aqui:** stack técnica, convenções de código, regras do projeto, status dos módulos, como navegar o repositório.

**O que NÃO vai aqui:** tudo que já está em Rules, detalhes de implementação específicos, histórico de sessões.

**Hierarquia:** global (`~/.claude/CLAUDE.md`) → projeto (`projeto/CLAUDE.md`) → subpasta (`projeto/src/CLAUDE.md`). Todos são carregados, mais específico tem prioridade.

### Camada 4 — Conversa atual

O que está happening agora: perguntas, respostas, arquivos lidos, resultados de ferramentas. Esta é a camada que cresce durante a sessão e precisa ser gerenciada ativamente.

---

## O Problema da Janela Finita

Toda sessão começa com espaço e termina cheia. Quando o contexto fica grande demais, três coisas acontecem:

1. **Latência aumenta** — o modelo processa mais tokens por resposta
2. **Custo aumenta** — cada token no contexto é cobrado
3. **Qualidade pode diminuir** — informações antigas no início da conversa recebem menos atenção (attention dilution)

O modelo não "esquece" o início da conversa, mas prioriza informações recentes. Um contexto longo e não gerenciado é um contexto onde informações importantes competem com ruído.

---

## Trade-off: Contexto Rico vs Contexto Relevante

| | Contexto rico | Contexto relevante |
|---|---|---|
| **O que é** | Tudo disponível no contexto | Apenas o necessário para a tarefa atual |
| **Vantagem** | Modelo tem toda a informação | Respostas mais focadas e rápidas |
| **Risco** | Attention dilution, custo alto | Informação importante pode estar fora |
| **Quando usar** | Tarefas exploratórias, revisões amplas | Implementação de feature específica |

A regra prática: **contexto rico para decidir, contexto relevante para implementar**.

---

## Anti-padrões de Contexto

| Anti-padrão | Consequência | Correção |
|-------------|-------------|---------|
| **CLAUDE.md gigante** (>200 linhas) | Dilui as regras importantes | Mova detalhes para Rules e Memory |
| **Nenhuma persistência** | Cada sessão começa do zero | Use os 3 mecanismos: CLAUDE.md + Memory + PROGRESS.md |
| **Repetir contexto no prompt** | Duplicação, tokens desperdiçados | Se está no CLAUDE.md, não repita no prompt |
| **Sessão eterna** | Contexto cresce sem fim | Use `/compact` ou abra nova sessão com seed |
| **Fresh agent sem briefing** | Agente começa sem contexto | Inclua o essencial no prompt do agente |
| **Memory como log** | Memory fica grande e irrelevante | Memory guarda fatos, PROGRESS.md guarda histórico |