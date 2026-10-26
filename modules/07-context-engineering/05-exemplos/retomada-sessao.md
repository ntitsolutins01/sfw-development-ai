# Exemplo: Retomada de Sessão Interrompida

> Cenário: você estava implementando o middleware de autenticação (último CAs do spec JWT) quando a sessão foi interrompida. Voltou 2 dias depois. Como retomar sem perder o fio?

---

## O que foi persistido ao final da sessão anterior

### PROGRESS.md (última entrada)

```markdown
## Sessão 7 — 2026-10-19

### O que foi feito
- auth_service.py concluído com login e logout
- Testes unitários passando (CA-1 a CA-8)
- UserRepository implementado com Repository Pattern

### Estado atual (pausa)
O que foi feito: auth_service + repository + testes unitários
O que falta: middleware de autenticação (CA-9 e CA-10) + testes de integração

### Próxima sessão
Módulo 3 — TDD: implementar middleware get_current_user em app/dependencies.py
CAs pendentes:
- CA-9: middleware aceita token válido não revogado → requisição prossegue
- CA-10: middleware rejeita token revogado → retorna 401 "Token revogado"
```

### CLAUDE.md (status)

```markdown
## Status atual
- [x] POST /auth/login
- [x] POST /auth/logout
- [ ] Middleware get_current_user ← em andamento
```

---

## Prompt de retomada (2 dias depois)

```
Leia o PROGRESS.md e me coloque em contexto.
Foque na seção "Próxima sessão" da última entrada.

Confirme:
1. O que foi concluído na sessão anterior
2. Exatamente o que falta para fechar o spec JWT
3. Em qual arquivo devo trabalhar

Depois leia app/services/auth.py para ver o estado atual do código
antes de começarmos.
```

---

## O que o modelo retorna

```
Contexto da sessão anterior:

1. **Concluído:** auth_service.py (login + logout), UserRepository (Repository Pattern),
   testes unitários CA-1 a CA-8 passando

2. **Falta:** middleware get_current_user em app/dependencies.py
   - CA-9: token válido não revogado → requisição prossegue normalmente
   - CA-10: token na blocklist → HTTPException 401 "Token revogado"

3. **Arquivo:** app/dependencies.py (função get_current_user como FastAPI Dependency)

Lerei app/services/auth.py para ver as funções disponíveis antes de começar.
[lê o arquivo]

verify_token(token, redis_client) já está implementado — o middleware pode usá-la diretamente.
Podemos começar pela escrita dos testes do middleware (TDD)?
```

O modelo retomou exatamente onde parou, com contexto correto, sem precisar re-explicar a história do projeto.

---

## Por que funcionou

**PROGRESS.md fez o trabalho pesado:** a seção "Próxima sessão" era específica — arquivo, função, CAs. Não era genérica ("continuar a implementação").

**CLAUDE.md confirmou o estado:** o checkbox em aberto no CLAUDE.md sinalizou imediatamente que o middleware era a última peça.

**Prompt pediu confirmação antes de agir:** "confirme o que está planejado antes de começar" evita que o modelo assuma e parta para a implementação sem verificar o contexto.

---

## Anti-padrão: retomada sem seed

```
# ❌ Voltando depois de 2 dias sem seed
vamos continuar de onde paramos
```

O modelo não sabe onde pararam. Vai perguntar o que está sendo feito, ou pior, vai assumir algo errado. O contexto da sessão anterior não existe mais — cada nova sessão começa do zero.

---

## Lição deste exemplo

A qualidade da retomada depende da qualidade da persistência. Se o PROGRESS.md tem "próxima sessão" vaga ("continuar o módulo"), a retomada vai ser vaga. Se tem arquivo + função + CAs pendentes, a retomada é precisa.

O investimento de 2 minutos para escrever uma boa seção "próxima sessão" no PROGRESS.md vale horas de reconstrução de contexto.