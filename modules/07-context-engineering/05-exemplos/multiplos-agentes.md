# Exemplo: Múltiplos Agentes com Contexto Controlado

> Cenário: você está implementando a feature de refresh token e quer, em paralelo, fazer a revisão de segurança do auth_service.py já implementado — sem que o contexto de revisão polua a sessão de implementação.

---

## O problema sem Context Engineering

Se você fizer tudo na mesma sessão:
```
Me ajude a implementar refresh token E revise o auth_service.py de segurança.
```

O modelo vai misturar os dois contextos. A revisão vai influenciar a implementação (pode estar certo), mas também pode introduzir ruído sobre vulnerabilidades em código que você está ativamente mudando.

---

## Solução: Fork + Fresh em paralelo

### Sessão principal — implementação do refresh token

Continua normalmente com o contexto da feature:
```
Implementar POST /auth/refresh seguindo o spec:
- CA-1: refresh_token válido → novo access_token
- CA-2: refresh_token expirado → 401
[resto do seed normal]
```

### Fork agent — pesquisa sobre estratégias de refresh token

```
Use um fork agent para pesquisar: qual é a estratégia mais segura para
armazenar refresh tokens — Redis com TTL vs banco de dados com revogação?

Não implemente nada. Apenas retorne:
1. Comparativo das duas estratégias (segurança, complexidade, performance)
2. Recomendação para uma API com <10k usuários
```

O fork herda o contexto da sessão, mas o resultado da pesquisa é retornado como texto — não polui a sessão.

### Fresh agent — revisão de segurança independente

```
[Fresh agent — sem contexto da sessão atual]

Revise o código abaixo como um especialista em segurança de APIs.
Foque em: JWT vulnerabilities, timing attacks, exposição de dados em erros.

Stack: Python 3.11 / FastAPI / python-jose / Redis

[cole app/services/auth.py]

Retorne os achados com severidade (CRÍTICO/ALTO/MÉDIO/BAIXO) e sugestão de correção.
```

O fresh agent não sabe que você está implementando refresh token. A revisão é completamente independente — sem viés de "o código que acabei de escrever".

---

## Incorporando os resultados

Após os dois agentes terminarem:

**Fork (pesquisa):** você decide adotar Redis com TTL para refresh tokens baseado na recomendação. Adiciona isso à sessão principal:
```
Com base na pesquisa, vamos usar Redis com TTL para os refresh tokens.
[continue a implementação]
```

**Fresh (revisão de segurança):** você recebe os achados. Se há algo CRÍTICO ou ALTO, resolve antes de continuar:
```
O fresh agent encontrou [achado]. Vamos corrigir isso antes de continuar
com o refresh token.
```

---

## Quando fork vs fresh

| Decisão | Fork | Fresh |
|---------|------|-------|
| Pesquisa que pode usar o contexto atual | ✅ | |
| Revisão que precisa ser imparcial | | ✅ |
| Tarefa paralela rápida | ✅ | |
| Tarefa que demora muito (>20 min) | | ✅ (mais limpo) |
| Exploração que pode não levar a nada | ✅ | |

---

## Lição deste exemplo

Agentes paralelos não são só sobre velocidade — são sobre **isolamento de contexto**. A revisão de segurança é mais valiosa quando feita por um agente que não sabe que você acabou de implementar aquele código. O fresh agent não vai ter viés de confirmação ("o código que acabei de ajudar a escrever está correto").

O fork, por outro lado, é mais barato (herda o cache) e útil quando a pesquisa se beneficia do contexto atual (ele sabe qual é a stack, quais as decisões já tomadas).