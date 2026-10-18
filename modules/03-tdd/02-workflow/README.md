# 02 — Workflow TDD com IA

## Fluxo Completo: SDD + TDD

A integração entre o Módulo 2 (SDD) e o Módulo 3 (TDD) fecha o ciclo de desenvolvimento com IA:

```
┌──────────────────────────────────────────────────────────────┐
│                   PRÉ-SPEC (Módulo 2)                        │
│  /brainstorm → /escrever-prd → /escrever-trd                 │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                  SPEC TÉCNICO (Módulo 2)                     │
│  Critérios de aceite definidos → docs/specs/                 │
└──────────────────────────────┬───────────────────────────────┘
                               │  cada CA vira um ou mais testes
┌──────────────────────────────▼───────────────────────────────┐
│                   CICLO TDD (Módulo 3)                       │
│                                                              │
│   1. ESCREVER TESTES (Red)                                   │
│      IA gera testes a partir dos CAs do spec                 │
│      → você revisa e complementa                             │
│               │                                              │
│               ▼                                              │
│   2. IMPLEMENTAR (Green)                                     │
│      IA implementa o mínimo para os testes passarem          │
│               │                                              │
│               ▼                                              │
│   3. REFATORAR (Refactor)                                    │
│      IA melhora o código; testes garantem que nada quebrou   │
└──────────────────────────────────────────────────────────────┘
```

---

## Mapeando CAs do Spec para Casos de Teste

Cada critério de aceite do spec gera um ou mais casos de teste. Regra: **um CA = pelo menos dois testes** (caso feliz + caso de falha).

Exemplo baseado no spec de autenticação do Módulo 2:

| Critério de aceite (spec) | Casos de teste |
|--------------------------|----------------|
| `[ ] POST /auth/login retorna token JWT com credenciais corretas` | `test_login_returns_jwt_token_on_valid_credentials` |
| `[ ] POST /auth/login retorna 401 com senha incorreta` | `test_login_returns_401_on_wrong_password` |
| `[ ] Token expira em 24 horas` | `test_token_expires_after_24_hours` |
| `[ ] POST /auth/logout invalida o token` | `test_logout_invalidates_token` |
| Caso de borda: usuário inexistente retorna mesmo erro que senha errada | `test_nonexistent_user_returns_same_error_as_wrong_password` |

Casos de borda do spec viram testes separados. Se o spec define que dois erros devem retornar a mesma resposta (decisão de segurança), esse comportamento precisa de um teste próprio.

---

## Fase Red — Escrever os Testes

**Entrada:** critérios de aceite do spec
**Saída:** arquivo de testes que falha ao rodar

O que fazer nesta fase:

1. Copie os CAs do spec
2. Peça para a IA gerar os casos de teste (ver Prompt 1 em `04-ia-no-fluxo/`)
3. Revise: cada CA tem teste? Casos de borda estão cobertos?
4. Rode os testes — **confirme que falham**
5. Se algum teste passar antes de implementar, ele está testando algo errado

O que verificar antes de passar para Green:
- [ ] Todos os CAs têm pelo menos um teste
- [ ] Casos de borda do spec têm testes próprios
- [ ] Rode `pytest` ou `npm test` — todos devem falhar com `AssertionError` ou equivalente
- [ ] Nenhum teste passa por acidente (ex: testar que função retorna `None` quando não existe)

---

## Fase Green — Implementar

**Entrada:** arquivo de testes falhando
**Saída:** implementação mínima que faz todos os testes passarem

O que fazer nesta fase:

1. Forneça os testes para a IA
2. Peça para a IA implementar o mínimo para os testes passarem (ver Prompt 2)
3. Rode os testes — confirme que todos passam
4. Verifique: a IA não modificou os testes?

O que verificar após esta fase:
- [ ] `pytest` ou `npm test` mostra todos verdes
- [ ] Nenhum teste foi alterado — apenas o código de produção
- [ ] A IA não implementou mais do que o necessário para os testes passarem
- [ ] Não há `pass`, `return None` ou implementações vazias passando em testes que deveriam verificar comportamento real

---

## Fase Refactor — Melhorar

**Entrada:** código funcionando com testes verdes
**Saída:** código melhorado, testes ainda verdes

O que fazer nesta fase:

1. Identifique o que quer melhorar: legibilidade, performance, separação de responsabilidades
2. Peça para a IA refatorar (ver Prompt 3)
3. Rode os testes após cada mudança
4. Se um teste quebrar durante o refactor, desfaça a última mudança

O que verificar após esta fase:
- [ ] Todos os testes ainda passam
- [ ] A cobertura não diminuiu
- [ ] O comportamento externo não mudou — só a estrutura interna

---

## Quando Você Escreve vs Quando a IA Escreve

| Situação | Quem escreve os testes |
|----------|----------------------|
| CAs claros no spec, comportamento direto | IA gera, você revisa |
| Lógica de domínio crítica (financeiro, segurança) | Você escreve, IA complementa |
| Testes de integração com banco ou API externa | Você define a fixture/mock, IA gera o teste |
| Casos de borda não óbvios identificados na revisão | Você aponta, IA gera |
| Regras de negócio sutis (ex: cálculo com arredondamento) | Você escreve — risco de IA normalizar o comportamento errado |

---

## CLAUDE.md com Regra de TDD

Adicione ao `CLAUDE.md` do seu projeto para forçar o fluxo:

```markdown
## Regra de TDD

Antes de implementar qualquer mudança de lógica:
1. Pergunte se existem testes para o comportamento em questão
2. Se não existirem, gere os testes primeiro e confirme que falham
3. Só então implemente o código
4. Ao final, confirme que todos os testes passam com `pytest` ou `npm test`

Nunca modifique testes existentes para fazê-los passar — modifique o código.
Testes não podem ser removidos ou comentados para resolver falhas.
```
