# 03 — Skills

## O que são Skills

Skills são **comandos personalizados** que você invoca com `/nome-da-skill`.
São como macros inteligentes: encapsulam um conjunto de instruções que você
repetiria toda vez que pedisse aquela tarefa.

Pense assim:
- Sem skill: toda vez que pedir "revise meu código" você explica do zero o que quer
- Com skill: `/code-review` já sabe exatamente o que verificar, como reportar e o que fazer

## Onde ficam as Skills

```
~/.claude/skills/              ← skills globais (valem em qualquer projeto)
│   └── code-review/
│       └── SKILL.md
│
/seu-projeto/.claude/skills/   ← skills do projeto (só valem aqui)
    └── rodar-migracao/
        └── SKILL.md
```

## Anatomia de uma Skill

Cada skill é uma **pasta** com um arquivo `SKILL.md` dentro:

```
minha-skill/
└── SKILL.md     ← instruções da skill (obrigatório)
```

O `SKILL.md` é um arquivo Markdown com as instruções que o Claude Code
vai seguir quando você invocar `/minha-skill`.

### Estrutura Recomendada do SKILL.md

```markdown
# Nome da Skill

## Objetivo
O que essa skill faz — em uma frase.

## Quando usar
Situações onde faz sentido invocar esta skill.

## O que ela faz (passo a passo)
1. Primeiro passo
2. Segundo passo
3. ...

## O que ela NÃO faz
Limites claros do escopo.

## Argumentos aceitos (opcional)
Como passar argumentos: `/skill argumento`

## Exemplo de uso
/skill
```

## Como Criar uma Skill

### Passo 1 — Escolha onde colocar

```bash
# Skill global (qualquer projeto)
mkdir -p ~/.claude/skills/minha-skill

# Skill do projeto (só este projeto)
mkdir -p .claude/skills/minha-skill
```

### Passo 2 — Crie o SKILL.md

```bash
# Edite o arquivo com suas instruções
code ~/.claude/skills/minha-skill/SKILL.md
```

### Passo 3 — Invoque

```bash
# Dentro do Claude Code
claude
> /minha-skill
```

## Como Testar uma Skill

```bash
# 1. Abrir o Claude Code
claude

# 2. Listar skills disponíveis
/help

# 3. Invocar a skill
/minha-skill

# 4. Se algo der errado, leia o SKILL.md e ajuste as instruções
# As instruções são processadas como prompt — seja específico!
```

## Exemplos Práticos

A pasta `exemplos/` contém skills prontas para usar:

| Skill | O que faz |
|-------|-----------|
| `code-review/` | Revisa o diff atual por bugs e problemas de qualidade |
| `rodar-testes/` | Executa a suite de testes e resume os resultados |
| `criar-pr/` | Gera título, descrição e checklist para um Pull Request |
| `explicar-codigo/` | Explica o arquivo atual em linguagem simples |
| `resumir-commits/` | Resume os commits do branch atual em changelog |

## Dicas de Escrita

1. **Seja específico no objetivo** — "revisa código" é vago; "verifica bugs, segurança e performance no diff atual" é preciso
2. **Liste os passos** — a IA seguirá melhor instruções numeradas
3. **Defina o output** — diga exatamente o formato da resposta esperada
4. **Diga o que NÃO fazer** — limites são tão importantes quanto o escopo
5. **Inclua um exemplo** — mostra o resultado esperado na prática
