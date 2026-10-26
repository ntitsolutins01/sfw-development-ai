# Template — Context Seed para Tarefa Específica

Use para iniciar uma sessão focada em uma tarefa específica, sem carregar o contexto completo do projeto.

---

## O que é um context seed

Um seed é o conjunto mínimo de informações que o modelo precisa para executar uma tarefa específica bem. Diferente da retomada de sessão (que carrega o estado geral do projeto), o seed é cirúrgico — carrega apenas o que é relevante para a próxima hora de trabalho.

**Analogia:** o CLAUDE.md é o manual do projeto. O seed é o briefing para a reunião de amanhã.

---

## Template de seed para implementação

```
## Tarefa desta sessão
Implementar: [função / endpoint / feature]
Arquivo alvo: [caminho completo]
Spec de referência: [caminho do spec ou cole os CAs relevantes]

## Contexto necessário
- Stack: [linguagem, framework, bibliotecas relevantes]
- Estado atual do arquivo: [cole as importações e definições existentes]
- Dependências: [outras funções/classes que esta tarefa usa]

## Critérios de aceite para esta sessão
- CA-N: [critério]
- CA-N: [critério]

## Fora do escopo desta sessão
- [o que não será feito agora]
- [o que vem depois]
```

---

## Template de seed para debugging

```
## Tarefa desta sessão
Corrigir: [descrição do bug]
Arquivo com o problema: [caminho + função]

## Contexto necessário
- Comportamento esperado: [o que deveria acontecer]
- Comportamento atual: [o que está acontecendo]
- Erro (se disponível): [stack trace completo]
- Código relevante: [cole apenas o trecho com o bug]

## Fora do escopo
- Não refatorar além da correção
- Não alterar outros arquivos além do indicado
```

---

## Template de seed para revisão

```
## Tarefa desta sessão
Revisar: [o que será revisado — diff, arquivo, PR]
Critério de revisão: [spec / checklist / dimensões de qualidade]

## Contexto necessário
- Spec de referência: [cole os CAs ou caminho do arquivo]
- Código a revisar: [cole o diff ou conteúdo]

## Formato esperado da revisão
- Achados com severidade (CRÍTICO / ALTO / MÉDIO / BAIXO)
- Decisão: APROVADO / APROVADO COM RESSALVAS / SOLICITAR MUDANÇAS
```

---

## Exemplo preenchido — seed para implementar refresh token

```
## Tarefa desta sessão
Implementar: endpoint POST /auth/refresh
Arquivo alvo: app/routes/auth.py (adicionar rota) + app/services/auth.py (adicionar lógica)
Spec de referência:

CAs relevantes:
- CA-1: dado refresh_token válido não expirado, quando POST /auth/refresh,
  então retorna novo access_token com exp = agora + 24h
- CA-2: dado refresh_token expirado, quando POST /auth/refresh, então retorna 401
- CA-3: dado refresh_token na blocklist, quando POST /auth/refresh, então retorna 401

## Contexto necessário
Stack: Python 3.11 / FastAPI 0.110 / python-jose / Redis
Estado atual de app/services/auth.py (importações):
  from jose import JWTError, jwt
  from datetime import datetime, timedelta
  from uuid import uuid4
  import os, redis

Funções existentes que serão usadas:
  - verify_token(token, redis_client) -> dict
  - create_token(user_id) -> str

## Fora do escopo desta sessão
- Não implementar revogação de refresh tokens ainda
- Não alterar os endpoints /auth/login e /auth/logout
- Não criar tabela de banco para refresh tokens — usar Redis
```

---

## Dica: seed vs CLAUDE.md

O CLAUDE.md já carrega o contexto geral do projeto automaticamente. Não repita no seed o que já está no CLAUDE.md.

O seed complementa o CLAUDE.md com:
- O objetivo específico desta sessão
- Os arquivos que serão tocados
- Os CAs que devem ser atendidos
- O que está fora do escopo