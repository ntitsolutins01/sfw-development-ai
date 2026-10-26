# Exemplo: Gerenciando uma Sessão Longa

> Cenário: implementar o sistema completo de autenticação JWT (login + logout + middleware) em uma única sessão. Estimativa: 3–4 horas de trabalho, ~80 trocas de conversa.

---

## Fase 1 — Seed da sessão

**Prompt de abertura:**
```
Vamos implementar o sistema de autenticação JWT completo nesta sessão.

Spec: docs/specs/001-autenticacao-jwt.md (10 CAs)
Arquivos que serão criados/modificados:
- app/services/auth.py (novo)
- app/repositories/user_repository.py (novo)
- app/routes/auth.py (novo)
- tests/unit/test_auth_service.py (novo)
- tests/integration/test_auth_routes.py (novo)

Fora do escopo desta sessão: refresh token, rate limiting, MFA.

Sequência planejada:
1. testes (TDD — fase Red)
2. implementação (fase Green)
3. refatoração se necessário
4. revisão final contra os CAs

Pode começar pelos testes do auth_service usando os CAs do spec?
```

---

## Fase 2 — Trabalho (primeiros 30 exchanges)

A sessão flui normalmente. O modelo:
- Lê o spec
- Gera os testes
- Executa pytest (falhas esperadas — Red)
- Gera a implementação
- Executa pytest novamente (tudo verde — Green)

**Sinal de alerta aparece no exchange ~35:**
O modelo começa a responder sobre o middleware de autenticação sem mencionar que os testes do logout ainda não estão passando — sinal de que o início da conversa está sendo "diluído".

---

## Fase 3 — Compactação estratégica

**Após concluir auth_service.py e seus testes:**
```
/compact
```

**Verificação após o compact:**
```
Confirme o estado atual:
1. Quais arquivos foram criados e estão concluídos?
2. Quais CAs do spec estão cobertos pelos testes?
3. O que ainda falta implementar nesta sessão?
```

**Resposta esperada após compact:**
```
Estado atual:
1. Concluídos: app/services/auth.py, tests/unit/test_auth_service.py
2. CAs cobertos: CA-1 a CA-8 (login e logout)
3. Falta: app/routes/auth.py (endpoints HTTP), middleware, testes de integração (CA-9, CA-10)
```

O compact funcionou — o modelo tem o estado correto sem todo o ruído das tentativas intermediárias.

---

## Fase 4 — Continuação com contexto limpo

Com o contexto compactado, continue a implementação:
```
Perfeito. Agora implemente app/routes/auth.py com POST /auth/login e POST /auth/logout.
Use os serviços já implementados em app/services/auth.py.
```

A sessão continua mais leve e focada.

---

## Fase 5 — Persistência ao final

Ao concluir todos os CAs:
```
/salvar-contexto
```

Selecione "Módulo concluído" para atualizar os 3 mecanismos.

---

## Lição deste exemplo

O moment certo para `/compact` não é quando o contexto está "cheio" — é ao final de uma subtarefa bem definida. No exemplo:
- **Depois de concluir o auth_service** — subtarefa 1 concluída, contexto útil e limpo
- **Antes de iniciar as rotas** — nova subtarefa começa com contexto relevante

Compactar no meio de uma tarefa (ex: no meio da implementação do auth_service) perderia decisões em andamento. Compactar no final, antes de iniciar a próxima parte, é o momento ideal.