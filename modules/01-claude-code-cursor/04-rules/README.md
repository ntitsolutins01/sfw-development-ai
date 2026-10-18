# 04 — Rules (Regras)

## O que são Rules

Rules são instruções de comportamento que a IA deve seguir **sempre** dentro
de um escopo. Diferente do CLAUDE.md (que descreve o projeto), as rules definem
**como a IA deve agir**: o que pode, o que não pode, qual estilo usar.

## CLAUDE.md vs Rules — Qual a diferença?

| CLAUDE.md | Rules |
|-----------|-------|
| Descreve **o projeto** | Define **o comportamento** |
| "Este projeto usa Django 5.0" | "Nunca use `bare except`" |
| "Rodar testes: `pytest`" | "Sempre escreva type hints" |
| Contexto factual | Restrições e padrões |

Na prática, o CLAUDE.md pode conter uma seção de rules — são complementares.

## Onde ficam as Rules

Rules ficam no próprio `CLAUDE.md`, em uma seção dedicada:

```markdown
# Meu Projeto

## Como rodar
...

## Rules (Regras para a IA)

### Python
- Sempre usar type hints em funções públicas
- Nunca usar `bare except` — sempre especificar a exceção
- Imports organizados: stdlib, third-party, local (separados por linha em branco)
```

Ou em um arquivo separado incluído via `@`:

```markdown
# CLAUDE.md
@.claude/rules/python.md
@.claude/rules/seguranca.md
```

## Tipos de Rules

### 1. Rules de Estilo de Código

```markdown
## Rules — Python

- Type hints obrigatórios em todas as funções públicas
- Docstrings apenas quando o nome da função não for autoexplicativo
- f-strings para formatação de strings (não `.format()` nem `%`)
- `pathlib.Path` em vez de `os.path`
- `dataclasses` ou `pydantic` para modelos de dados (não dicts soltos)
```

### 2. Rules de Segurança

```markdown
## Rules — Segurança

- Nunca escrever segredos, tokens ou senhas no código
- Input do usuário SEMPRE sanitizado antes de usar em queries
- Nunca usar `eval()` ou `exec()` com input externo
- CORS configurado explicitamente — não usar wildcard em produção
- Logs nunca devem conter dados pessoais (CPF, email, cartão)
```

### 3. Rules de Arquitetura

```markdown
## Rules — Arquitetura

- Regras de negócio ficam em services/, não em views/ ou models/
- Dependências externas (APIs, banco) acessadas via interfaces/abstrações
- Não importar de apps vizinhas diretamente — use eventos ou interfaces
- Cada função faz UMA coisa — máximo 30 linhas por função
```

### 4. Rules de Testes

```markdown
## Rules — Testes

- Todo bugfix vem acompanhado de um teste que reproduz o bug
- Testes nomeados: `test_deve_<comportamento>_quando_<condição>`
- Não usar `sleep()` em testes — use mocks para tempo
- Testes de integração marcados com `@pytest.mark.integration`
```

## Como Testar suas Rules

```bash
# 1. Adicione as rules no CLAUDE.md do projeto
# 2. Abra o Claude Code
claude

# 3. Peça para gerar código que violaria a rule
> crie uma função que recebe um user_id e busca no banco

# A IA deve seguir as rules automaticamente:
# - Incluir type hint em user_id
# - Usar query parametrizada (não concatenação de string)
# - Colocar lógica em services/, não em views/

# 4. Se a IA violar uma rule, reforce-a com linguagem mais diretiva
# "NUNCA faça X" é mais eficaz que "prefira não fazer X"
```

## Exemplos Práticos

Na pasta `exemplos/` você encontra rules prontas:

- `python.md` — rules para projetos Python
- `typescript.md` — rules para projetos TypeScript/React
- `seguranca.md` — rules de segurança universais
- `testes.md` — rules para escrita de testes

## Boas Práticas para Escrever Rules

1. **Use linguagem imperativa**: "Use X", "Nunca faça Y", "Sempre inclua Z"
2. **Seja específico**: "funções acima de 30 linhas devem ser refatoradas" > "funções curtas"
3. **Explique o porquê quando não for óbvio**: "Não use wildcard em CORS — pode expor dados em subdomínios comprometidos"
4. **Organize por categoria**: segurança, estilo, arquitetura, testes
5. **Teste suas rules**: peça para a IA gerar código e veja se ela as segue
