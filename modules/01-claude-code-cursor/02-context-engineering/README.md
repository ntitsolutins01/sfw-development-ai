# 02 — Context Engineering

## O que é Context Engineering

Context Engineering é a prática de fornecer para a IA **exatamente o contexto
certo** para que ela tome decisões precisas. É a diferença entre pedir para alguém
"conserte isso" vs. "conserte este bug na função `calcular_total()` no arquivo
`pedidos.py`, que deve retornar o valor com desconto aplicado antes do imposto."

O Claude Code usa o arquivo `CLAUDE.md` como principal veículo de contexto.

## Como o CLAUDE.md Funciona

Ao iniciar, o Claude Code lê automaticamente todos os `CLAUDE.md` que encontrar:

```
~/.claude/CLAUDE.md              ← lido sempre (configurações globais)
│
└── /seu-projeto/
    ├── CLAUDE.md                ← lido ao abrir o projeto
    ├── src/
    │   └── CLAUDE.md            ← lido ao trabalhar em src/
    └── tests/
        └── CLAUDE.md            ← lido ao trabalhar em tests/
```

Cada arquivo é **acumulativo** — o contexto vai crescendo conforme você navega
nas pastas.

## Anatomia de um CLAUDE.md Eficaz

Um bom CLAUDE.md responde a estas perguntas:

1. **O que é este projeto?** — propósito em 2 linhas
2. **Como rodar?** — comandos exatos para instalar e executar
3. **Como testar?** — comandos exatos para os testes
4. **Quais são as convenções?** — estilo de código, nomes, estrutura
5. **O que NÃO fazer?** — antipadrões, decisões arquiteturais, restrições

## Camadas de Contexto

### Camada 1 — Global (`~/.claude/CLAUDE.md`)

Contém preferências pessoais que valem para **todos** os seus projetos.

```markdown
# Preferências Globais

## Estilo de Comunicação
- Responda sempre em português
- Seja direto e conciso
- Quando houver dúvida, pergunte antes de implementar

## Comportamento Padrão
- Nunca faça commit sem perguntar
- Sempre rode os testes antes de considerar algo pronto
- Prefira editar arquivos existentes a criar novos
```

### Camada 2 — Projeto (`/projeto/CLAUDE.md`)

Contém tudo que um desenvolvedor novo precisaria saber para contribuir.

### Camada 3 — Subpastas (`/projeto/src/CLAUDE.md`)

Contexto específico de um módulo ou domínio.

## Técnicas Avançadas

### Importar outros arquivos

```markdown
# Contexto do Projeto

<!-- Inclui o diagrama de arquitetura -->
@docs/arquitetura.md

<!-- Inclui as regras de negócio -->
@docs/regras-de-negocio.md
```

### Usar `#` para marcar seções críticas

```markdown
# IMPORTANTE: Regras que nunca devem ser quebradas

- Nunca modificar a tabela `pagamentos` diretamente — use o serviço PaymentService
- Toda alteração no domínio `pedidos` precisa de migration de banco
```

### Descrever a arquitetura com ASCII

```markdown
## Arquitetura

┌──────────┐     ┌──────────┐     ┌──────────┐
│  Frontend │────▶│   API    │────▶│    DB    │
│  (React)  │     │ (Django) │     │(Postgres)│
└──────────┘     └──────────┘     └──────────┘
```

## O que Incluir vs. Excluir

| Incluir | Não incluir |
|---------|-------------|
| Comandos de instalação e execução | Código completo de arquivos |
| Convenções de nomenclatura | Logs de debug |
| Decisões arquiteturais e o porquê | TODOs pessoais |
| Variáveis de ambiente necessárias | Senhas ou tokens |
| Como rodar os testes | Histórico de mudanças |
| Dependências principais | Documentação já em outros arquivos |

## Exemplos Práticos

Na pasta `exemplos/` você encontra:

- `CLAUDE.md.global` — template para `~/.claude/CLAUDE.md`
- `CLAUDE.md.api-python` — projeto de API em Python
- `CLAUDE.md.frontend-react` — projeto Frontend React
- `CLAUDE.md.subpasta` — CLAUDE.md para uma subpasta específica

## Como Testar seu Context Engineering

```bash
# 1. Abra o Claude Code em um projeto com CLAUDE.md
claude

# 2. Pergunte sobre o projeto sem dar contexto adicional
> qual é o comando para rodar os testes?
> qual banco de dados esse projeto usa?
> como está estruturado o projeto?

# Se o Claude responder corretamente sem você explicar,
# seu CLAUDE.md está bem escrito!

# 3. Ver o contexto que está sendo carregado
/context
```
