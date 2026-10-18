# Como Salvar Contexto Entre Sessões

Trabalhar com IA em projetos longos levanta uma questão prática:
**como você retoma amanhã de onde parou hoje sem precisar re-explicar tudo?**

Há três mecanismos disponíveis, cada um com uma função diferente.

---

## Os 3 Mecanismos

### 1. Memory do Claude Code

**Nome técnico:** Project Memory

**Onde fica:**
```
~/.claude/projects/<nome-do-projeto>/memory/
```
No caso deste projeto:
```
~/.claude/projects/C--Projetos-POCs-sfw-development-ai/memory/
    ├── MEMORY.md          ← índice (lido automaticamente)
    └── project-aiad.md   ← memória detalhada do projeto
```

**O que faz:**
Arquivos Markdown que o Claude Code lê automaticamente ao iniciar qualquer
sessão dentro deste projeto. Você não precisa pedir — a IA já chega sabendo
o que foi feito, as decisões tomadas e qual é o próximo passo.

**Quando atualizar:**
A cada módulo concluído ou a cada decisão importante de arquitetura.
Peça: *"atualize a memória do projeto com o que fizemos hoje"*.

**Limitação:**
Só o Claude Code lê automaticamente. Um humano que abrir o projeto não verá
essa pasta facilmente — ela fica fora do repositório (em `~/.claude/`).

---

### 2. Seção de Status no CLAUDE.md

**Nome técnico:** Living Documentation

**Onde fica:**
```
CLAUDE.md  (raiz do projeto)
```

**O que faz:**
O Claude Code lê o `CLAUDE.md` automaticamente ao abrir qualquer projeto.
Ao adicionar uma seção `## Status Atual` com a tabela de módulos e um
ponteiro para o `PROGRESS.md`, qualquer sessão futura começa contextualizada
— seja sua, seja de um colega de time.

Exemplo da seção adicionada neste projeto:
```markdown
## Status Atual

| # | Módulo | Status |
|---|--------|--------|
| 1 | Claude Code e Cursor | ✅ Concluído |
| 2 | Spec Driven Development | ⏳ Próximo |
...

Para retomar: leia `PROGRESS.md` na raiz do projeto.
```

**Quando atualizar:**
A cada módulo concluído — mude o status de `⏳ Próximo` para `✅ Concluído`
e marque o seguinte como próximo.

**Limitação:**
Precisa ser atualizado manualmente (ou pedindo para a IA atualizar).
Se esquecer de atualizar, o status fica desatualizado.

---

### 3. Arquivo PROGRESS.md

**Nome técnico:** Session Journal / Progress Log

**Onde fica:**
```
PROGRESS.md  (raiz do projeto)
```

**O que faz:**
Registro cronológico de sessões. Cada entrada documenta:
- O que foi criado ou modificado
- Decisões tomadas e por quê
- O que fica para a próxima sessão

Ao retomar o trabalho, você (ou a IA) lê este arquivo para se situar:

```bash
claude
> leia o PROGRESS.md e me coloque em contexto do que fizemos até agora
```

É o mecanismo mais legível para humanos — você pode abrir direto no editor
e entender o estado do projeto sem precisar acionar a IA.

**Quando atualizar:**
Ao final de cada sessão de trabalho. Sempre inclua a seção
"Próxima sessão" com o que deve ser feito no próximo encontro.

**Limitação:**
Não é lido automaticamente pela IA — você precisa pedir explicitamente.
Se não pedir, a IA não sabe que ele existe.

---

## Os 3 Juntos: Como se Complementam

```
┌──────────────────────────────┬──────────────────────────┬─────────────────────────┐
│          Mecanismo           │        Para quem         │    Atualizado quando    │
├──────────────────────────────┼──────────────────────────┼─────────────────────────┤
│ Memory (project-aiad.md)    │ Claude Code (automático) │ A cada módulo concluído │
├──────────────────────────────┼──────────────────────────┼─────────────────────────┤
│ Seção de status no CLAUDE.md │ Claude Code + você       │ A cada módulo concluído │
├──────────────────────────────┼──────────────────────────┼─────────────────────────┤
│ PROGRESS.md                  │ Você (leitura humana)    │ A cada sessão           │
└──────────────────────────────┴──────────────────────────┴─────────────────────────┘
```

Pense nos três como camadas:

```
PROGRESS.md          ← "o que foi feito" — detalhado, cronológico, para humanos
     │
     ▼
CLAUDE.md status     ← "onde estamos" — resumo visual, para humanos e IA
     │
     ▼
Memory               ← "o que a IA precisa saber" — automático, para a IA
```

---

## Como Retomar uma Sessão

### Opção A — Retomada rápida (confiar na memória automática)

```bash
cd C:/Projetos/POCs/sfw-development-ai
claude
> pode continuar de onde paramos?
```

A IA lerá a memória do projeto automaticamente e saberá o próximo passo.

### Opção B — Retomada explícita (mais segura)

```bash
cd C:/Projetos/POCs/sfw-development-ai
claude
> leia o PROGRESS.md e me diga em que ponto estamos e o que falta fazer
```

### Opção C — Retomada com verificação

```bash
claude
> leia o PROGRESS.md, confirme o status atual dos módulos e me pergunte
> por qual módulo quer continuar
```

---

## Como Encerrar uma Sessão Corretamente

Ao final de cada sessão de trabalho, peça:

```
> encerre a sessão: atualize o PROGRESS.md com o que fizemos hoje,
> atualize o status no CLAUDE.md e salve a memória do projeto
```

A IA atualizará os três mecanismos de uma vez.

---

## Por que não usar apenas um dos três?

| Só memory | A IA sabe, mas você não vê facilmente o estado do projeto |
|-----------|----------------------------------------------------------|
| Só CLAUDE.md | Status visível, mas sem histórico de decisões |
| Só PROGRESS.md | Histórico rico, mas a IA não lê automaticamente — precisa pedir |
| **Os três juntos** | Cada camada cobre o ponto cego da outra |
