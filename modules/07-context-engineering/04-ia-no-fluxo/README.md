# IA no Fluxo — Técnicas de Context Engineering

Quatro técnicas para gerenciar contexto ativamente em sessões de desenvolvimento.

---

## Técnica 1 — /compact

O `/compact` resume a conversa atual, preservando decisões e descartando ruído.

**Quando usar:**
- Sessão tem mais de 50 trocas
- Há muita saída de ferramentas (leituras de arquivo, git diffs, resultados de testes)
- Você concluiu uma subtarefa e vai iniciar outra diferente na mesma sessão
- Respostas começam a ignorar instruções do início da conversa

**Como usar:**
```
/compact
```

Após o compact, verifique se o modelo ainda tem o contexto crítico testando com:
```
Quais são os CAs que ainda precisamos implementar nesta sessão?
```

**O que /compact preserva:**
- Objetivo da sessão
- Decisões tomadas
- Código implementado (confirmado pelo modelo)
- Erros importantes e como foram resolvidos

**O que /compact descarta:**
- Outputs de ferramentas já processados
- Tentativas intermediárias descartadas
- Discussões sobre alternativas não escolhidas

**Alternativa:** se a sessão está muito grande e complexa, às vezes é mais eficiente abrir uma nova sessão com um seed focado na próxima subtarefa, do que compactar uma sessão carregada.

---

## Técnica 2 — Fork Agent

O fork herda o contexto completo da sessão atual e executa em paralelo, sem poluir a sessão principal.

**Quando usar:**
- Exploração que pode não levar a nada (pesquisa, investigação de bug)
- Tarefas paralelas independentes (documentação enquanto testa, etc.)
- Você quer uma segunda opinião sem contaminar o contexto atual

**Como usar no Claude Code:**
```
Use um fork agent para investigar se a biblioteca X resolve nosso problema.
Não implemente ainda — apenas pesquise e reporte.
```

**O que o fork herda:**
- Todo o contexto da sessão atual
- O cache de tokens (mais barato)
- Nenhum output do fork vai para a sessão principal automaticamente

**Quando o fork termina:** ele retorna um resultado. Você decide o que incorporar na sessão principal.

---

## Técnica 3 — Fresh Agent

O fresh agent começa do zero — sem contexto da sessão atual. Ideal para revisões independentes.

**Quando usar:**
- Revisão de PR que deve ser imparcial (sem viés de quem implementou)
- Verificação de segurança independente
- Qualquer tarefa onde você quer uma perspectiva fresca

**Como usar:**
```
Inicie um fresh agent para revisar o diff abaixo.
Contexto: [cole o contexto necessário, já que o agente não tem nenhum]
Diff: [cole o diff]
Critério: [spec ou checklist]
```

**Diferença fork vs fresh:**

| | Fork | Fresh |
|---|---|---|
| Contexto inicial | Herda tudo da sessão | Zero |
| Custo | Mais barato (cache) | Mais caro (sem cache) |
| Quando usar | Exploração paralela | Revisão independente |
| Viés | Tem o contexto de quem pediu | Sem viés da sessão |

---

## Técnica 4 — Gestão dos 3 Mecanismos de Persistência

No AIAD, o contexto entre sessões é persistido em 3 lugares. Cada um tem um papel distinto:

### Memory (`~/.claude/projects/.../memory/`)

**O que guarda:** fatos estáveis sobre o projeto — o que foi construído, decisões arquiteturais, convenções estabelecidas.

**Quando atualizar:** ao concluir um módulo ou tomar uma decisão importante que afeta sessões futuras.

**Formato ideal:** fatos afirmativos curtos, com contexto de por quê.

```markdown
## O que foi criado no Módulo 4
[estrutura de arquivos e decisões]

## Decisão: sem skill dedicada no Módulo 6
Técnicas de prompt engineering são conhecimento aplicado, não fluxo automatizável.
```

**Anti-padrão:** usar memory como log de sessão (cresce sem fim, difícil de ler).

---

### CLAUDE.md (raiz do projeto)

**O que guarda:** status atual dos módulos, regras do projeto, como navegar o repositório.

**Quando atualizar:** quando o status do projeto muda (módulo concluído, decisão que afeta o CLAUDE.md).

**Formato ideal:** tabela de status + regras de alto nível.

**Anti-padrão:** CLAUDE.md com >150 linhas — dilui as regras importantes.

---

### PROGRESS.md

**O que guarda:** histórico cronológico de sessões — o que foi feito, decisões tomadas, próxima sessão.

**Quando atualizar:** ao final de cada sessão.

**Formato ideal:** entrada por sessão com "O que foi feito", "Decisões tomadas", "Próxima sessão".

**Por que importa:** o prompt de retomada (`leia o PROGRESS.md`) é o mecanismo que garante que cada sessão começa com contexto relevante sem precisar repetir tudo.

---

## Escolhendo a técnica certa

```
Contexto está crescendo demais?
  └── Sim → /compact (ou nova sessão com seed)
  └── Não → continue

Tarefa é paralela ou exploratória?
  └── Sim → fork agent
  └── Não → continue na sessão principal

Revisão precisa ser imparcial?
  └── Sim → fresh agent com briefing completo
  └── Não → continue na sessão principal

Sessão vai terminar?
  └── Sim → persistir nos 3 mecanismos (/salvar-contexto)
  └── Não → continue
```