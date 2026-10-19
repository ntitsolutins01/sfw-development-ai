# Exemplo: PR Review — Refatoração do Serviço de Usuário

> Baseado no spec `modules/02-spec-driven-development/05-exemplos/spec-api-endpoint-usuarios.md`.

---

## Contexto do PR

**Branch:** `refactor/user-service-repository-pattern`
**Título:** `refactor: extract UserRepository to decouple business logic from database`
**Objetivo:** separar queries de banco da lógica de negócio em `UserService`

---

## Resultado do `/code-review`

```
## Revisão de Código — refactor/user-service-repository-pattern — 2026-10-19

### Resumo
0 críticos, 0 altos, 1 médio, 1 baixo

### Achados

#### [MÉDIO] Interface de repositório não definida explicitamente — user_repository.py
Problema: UserRepository é uma classe concreta sem interface (ABC).
Se no futuro houver outro repositório (ex: para testes com mock), não existe
contrato para seguir.
Sugestão: Extraia `AbstractUserRepository(ABC)` com os métodos obrigatórios.
Isso facilita testes com `FakeUserRepository` sem tocar no banco.

#### [BAIXO] Docstring copiada da classe antiga — user_service.py:5
Problema: `"""Manages user CRUD operations and database queries"""` — a parte
sobre queries já não é responsabilidade do service.
Sugestão: `"""Manages user business logic. Database access via UserRepository."""`
```

---

## Verificação de comportamento preservado

Para refatorações, o critério principal é: **todos os testes existentes passam sem modificação?**

```
## Revisão com Spec — refactor/user-service-repository-pattern

Nota: este é um PR de refatoração. Não há spec de feature nova.
Verificando preservação de comportamento pelos testes existentes.

### Testes existentes
- [x] test_get_user_by_id — passou sem modificação
- [x] test_get_user_not_found — passou sem modificação
- [x] test_create_user — passou sem modificação
- [x] test_update_user — passou sem modificação
- [x] test_delete_user — passou sem modificação

### Interface pública (verificação manual)
- [x] UserService.get_user(id) — assinatura idêntica
- [x] UserService.create_user(data) — assinatura idêntica
- [x] UserService.update_user(id, data) — assinatura idêntica
- [x] UserService.delete_user(id) — assinatura idêntica

### Decisão
APROVADO COM RESSALVAS — comportamento preservado, todos os testes passando.
Ressalva: interface de repositório sem ABC — documentada como melhoria futura.
```

---

## Lição deste exemplo

Refatorações são as mais fáceis de revisar com IA porque o critério de sucesso é binário: **os testes passam sem modificação?**

O revisor humano foca no que a IA não consegue avaliar: a abstração `UserRepository` faz sentido no domínio? É a complexidade certa para o tamanho do projeto? Vai facilitar ou complicar a vida da equipe daqui a 6 meses?