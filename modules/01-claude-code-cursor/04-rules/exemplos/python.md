> **[EXEMPLO] Como usar este arquivo**
>
> Você tem duas formas de incluir estas rules no seu projeto:
>
> **Opção 1 — Via `@` no CLAUDE.md (recomendado para manter organizado)**
> ```markdown
> <!-- No seu CLAUDE.md do projeto, adicione esta linha: -->
> @.claude/rules/python.md
> ```
> ```bash
> # Salve este arquivo em:
> mkdir -p .claude/rules
> cp python.md .claude/rules/python.md
> ```
>
> **Opção 2 — Copiar diretamente no CLAUDE.md**
> ```markdown
> <!-- No seu CLAUDE.md do projeto, adicione uma seção: -->
> ## Rules — Python
> (cole o conteúdo abaixo aqui)
> ```
>
> **Como testar:**
> ```bash
> claude   # abra no projeto onde adicionou as rules
>
> > crie uma função que recebe um id de usuário e retorna o nome
> # Esperado: a função deve ter type hint (user_id: int) -> str
> # Se não tiver, a rule não está sendo lida — verifique o caminho do @
>
> > crie um try/except para chamar uma API externa
> # Esperado: nunca um "bare except:", sempre "except requests.RequestException as e:"
> ```

---

# Rules — Python

## Tipagem

- Type hints obrigatórios em todas as funções e métodos públicos
- Use `from __future__ import annotations` para forward references
- Prefira tipos concretos: `list[str]` em vez de `List[str]` (Python 3.10+)
- Para tipos opcionais: `str | None` em vez de `Optional[str]`

```python
# ✅ CORRETO
def buscar_usuario(user_id: int) -> Usuario | None:
    ...

# ❌ ERRADO — sem type hints
def buscar_usuario(user_id):
    ...
```

## Exceções

- NUNCA use `bare except` — sempre especifique a exceção
- Nunca silenciar exceções com `except Exception: pass`
- Use exceções customizadas para erros de domínio

```python
# ✅ CORRETO
try:
    resultado = operacao_critica()
except ValueError as e:
    logger.error("Valor inválido: %s", e)
    raise

# ❌ ERRADO — bare except
try:
    resultado = operacao_critica()
except:
    pass
```

## Strings

- Use f-strings para interpolação (não `.format()` nem `%`)
- Para strings multilinha: triple-quotes com indentação correta
- Não concatenar strings em loops — use `"".join()`

```python
# ✅ CORRETO
mensagem = f"Usuário {user.nome} criado com sucesso"

# ❌ ERRADO
mensagem = "Usuário " + user.nome + " criado com sucesso"
```

## Imports

Organize sempre nesta ordem (separados por linha em branco):

```python
# 1. Stdlib
import os
import sys
from datetime import datetime

# 2. Third-party
import django
from rest_framework import serializers

# 3. Local
from apps.pedidos.models import Pedido
```

## Caminhos de Arquivo

- Use `pathlib.Path` em vez de `os.path`

```python
# ✅ CORRETO
from pathlib import Path
arquivo = Path("data") / "relatorio.csv"

# ❌ ERRADO
import os
arquivo = os.path.join("data", "relatorio.csv")
```

## Modelos de Dados

- Use `dataclasses` ou `pydantic` para dados estruturados — não dicts soltos
- Para validação de input: sempre Pydantic
- Para DTOs internos: dataclasses são suficientes

```python
# ✅ CORRETO
from pydantic import BaseModel

class CriarPedidoInput(BaseModel):
    usuario_id: int
    itens: list[ItemInput]

# ❌ ERRADO — dict solto sem estrutura
def criar_pedido(dados: dict):
    usuario_id = dados["usuario_id"]
    ...
```

## Tamanho de Funções

- Máximo de 30 linhas por função (excluindo docstring)
- Se uma função precisa de mais, extraia subfunções com nomes descritivos
- Uma função deve fazer UMA coisa

## Logging

- Use `logging` padrão — não `print()` em produção
- Nunca logar dados sensíveis (senhas, tokens, CPF, cartão)
- Nível adequado: DEBUG para rastreamento, INFO para fluxo normal, ERROR para falhas

```python
import logging
logger = logging.getLogger(__name__)

# ✅ CORRETO
logger.info("Pedido %s criado para usuário %s", pedido.id, usuario.id)

# ❌ ERRADO — dado sensível
logger.info("Usuário autenticado: email=%s, senha=%s", email, senha)
```
