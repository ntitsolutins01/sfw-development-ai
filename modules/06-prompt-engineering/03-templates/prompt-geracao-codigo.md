# Template — Geração de Código

Use para criar novas funções, classes ou endpoints a partir de uma especificação.

---

## Template

```
## Contexto
Linguagem/framework: [ex: Python 3.11 / FastAPI 0.110]
Arquivo de destino: [ex: app/services/auth.py]
Estado atual do arquivo: [cole as importações e classes existentes, ou "arquivo novo"]
Spec de referência: [ex: docs/specs/001-autenticacao-jwt.md — cole os CAs relevantes]

## Instrução
Implemente [nome_da_função(params: tipos) -> tipo_retorno] no arquivo acima.

## Formato
- Função pura com type hints em todos os parâmetros e no retorno
- Docstring de uma linha descrevendo o contrato (não o passo a passo)
- Sem arquivos adicionais além do indicado

## Exemplos
[Se houver funções similares no projeto, cole uma aqui como referência de estilo]

## Restrições
- Não crie outros arquivos além de [arquivo de destino]
- Não adicione imports além dos necessários para esta função
- Não trate erros além do especificado nos CAs
- [adicione restrições específicas do projeto]
```

---

## Exemplo preenchido — função `create_token`

```
## Contexto
Linguagem/framework: Python 3.11 / FastAPI 0.110
Arquivo de destino: app/services/auth.py
Estado atual do arquivo:
  from datetime import datetime, timedelta
  from uuid import uuid4
  import os

Spec de referência (CAs relevantes):
  CA-4: dado token gerado, quando decodificado, então campo exp = hora_emissão + 86400 segundos
  CA-5: token deve conter os campos sub (user_id), exp e jti (UUID4)

## Instrução
Implemente create_token(user_id: str) -> str no arquivo app/services/auth.py.

## Formato
- Função pura com type hints
- Usa python-jose para assinar com HS256
- A chave de assinatura vem de os.environ["JWT_SECRET_KEY"]
- Retorna o token como string

## Exemplos
Estrutura de outras funções no projeto:
  def hash_password(password: str) -> str:
      """Retorna o hash bcrypt da senha."""
      return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

## Restrições
- Não crie outros arquivos
- Não adicione endpoint, rota ou middleware
- Não adicione logging ou tratamento de exceção além de ValueError para user_id vazio
- Use python-jose, não PyJWT
```

---

## Variações por complexidade

**Tarefa simples (C + I suficiente):**
```
Arquivo: app/utils/validators.py
Escreva is_valid_email(email: str) -> bool usando regex básico (não instale bibliotecas).
```

**Tarefa com estilo específico (adicione F + E):**
```
Arquivo: app/services/auth.py
Formato: siga o estilo da função hash_password acima — docstring de 1 linha, sem comentários inline.
Escreva verify_token(token: str) -> dict que decodifica o JWT e retorna o payload.
```

**Tarefa com risco de expansão de escopo (adicione R):**
```
Implemente apenas o endpoint POST /auth/logout.
Não crie middleware, não modifique rotas existentes, não adicione validação além do especificado.
```