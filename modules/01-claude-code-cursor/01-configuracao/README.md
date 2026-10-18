# 01 — Configuração Inicial

## O que é

O Claude Code é uma CLI (Command Line Interface) que transforma seu terminal em um
agente de desenvolvimento. Ele lê arquivos, executa comandos, escreve código e
toma decisões — tudo guiado por você.

O Cursor é um editor de código com IA embutida que usa os mesmos modelos.
Ambos se beneficiam das mesmas práticas de configuração.

## Instalação Passo a Passo

### 1. Instalar o Node.js (caso não tenha)

```bash
# Verificar se já tem
node --version   # precisa ser 18+

# Se não tiver, baixar em https://nodejs.org
```

### 2. Instalar o Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 3. Autenticar com sua conta Anthropic

```bash
claude login
# Vai abrir o browser para autorizar — siga as instruções
```

### 4. Verificar que tudo funcionou

```bash
claude --version
# Saída esperada: claude-code/x.x.x
```

## Estrutura de Arquivos de Configuração

O Claude Code usa arquivos em camadas. A ordem de prioridade é:

```
~/.claude/                     ← configurações GLOBAIS (valem para todos os projetos)
│   settings.json
│   CLAUDE.md
│   skills/
│   keybindings.json
│
/seu-projeto/.claude/          ← configurações do PROJETO (valem só aqui)
    settings.json
    settings.local.json        ← configurações locais (não commitar)
    skills/
    hooks/
```

> **Regra de ouro:** global define padrões, projeto sobrescreve o que precisa.

## settings.json — O Arquivo de Permissões

O `settings.json` controla o que o Claude Code pode ou não executar sem pedir
confirmação.

### Como funciona

Quando você pede algo ao Claude Code e ele precisa rodar um comando bash,
ele verifica:

1. O comando está na lista `allow`? → executa automaticamente
2. Está na lista `deny`? → recusa e explica
3. Não está em nenhuma? → pergunta ao usuário antes de executar

### Sintaxe

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",           // qualquer comando git
      "Bash(npm run:*)",       // qualquer npm run <script>
      "Bash(pytest:*)",        // qualquer pytest
      "Bash(ls:*)",            // listagem de arquivos
      "Bash(cat src/*)",       // ler arquivos só da pasta src/
      "Read(*)",               // ler qualquer arquivo
      "Edit(src/**)"           // editar só dentro de src/
    ],
    "deny": [
      "Bash(rm -rf:*)",        // nunca deletar recursivamente
      "Bash(git push --force:*)" // nunca force push
    ]
  }
}
```

### Exemplos de padrões úteis

| Padrão | O que permite |
|--------|---------------|
| `Bash(git:*)` | Todos os comandos git |
| `Bash(git commit:*)` | Só git commit |
| `Bash(npm:*)` | Todos os npm |
| `Bash(python src/*.py:*)` | Rodar arquivos Python só em src/ |
| `Read(*)` | Ler qualquer arquivo |
| `Edit(src/**)` | Editar recursivamente em src/ |
| `Write(tests/**)` | Criar/sobrescrever em tests/ |

### Como testar sua configuração

```bash
# Abrir o Claude Code no projeto
claude

# Pedir algo que deve ser permitido automaticamente
> liste os arquivos do projeto

# Pedir algo que deve pedir confirmação
> delete todos os arquivos .log

# Ver as permissões atuais
/config
```

## keybindings.json — Atalhos de Teclado

Permite criar atalhos personalizados para ações frequentes.

Arquivo em: `~/.claude/keybindings.json`

```json
[
  {
    "key": "ctrl+shift+r",
    "command": "claude:run-skill",
    "args": { "skill": "code-review" }
  },
  {
    "key": "ctrl+shift+t",
    "command": "claude:run-skill",
    "args": { "skill": "run-tests" }
  }
]
```

### Como testar

```bash
# Abrir o Claude Code
claude

# Pressionar o atalho que você configurou
# Ctrl+Shift+R → deve iniciar a skill de code-review
```

## Dicas de Produtividade

### Alias no terminal (opcional, mas recomendado)

```bash
# No seu ~/.bashrc ou ~/.zshrc
alias cc="claude"
alias ccf="claude --fast"   # modo mais rápido (Opus)
```

### Abrir sempre no contexto do projeto

```bash
# Sempre rodar de dentro do diretório do projeto
cd /meu-projeto
claude
```

### Ver o que o Claude Code está fazendo

```bash
# Rodar com log verboso para entender as decisões
claude --verbose
```

## Arquivos de Exemplo

- `settings.example.json` — configuração completa comentada
- `settings.local.example.json` — variáveis locais (tokens, paths)
- `keybindings.example.json` — atalhos de teclado práticos
