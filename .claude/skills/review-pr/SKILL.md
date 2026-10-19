---
name: review-pr
description: Revisão de PR com conformidade de spec — compara o diff com critérios de aceite, verifica cobertura de testes e emite decisão formal de aprovação ou solicitação de mudanças.
disable-model-invocation: false
---

# review-pr

Você foi invocado via `/review-pr`.

## Passo 1 — Identificar contexto

Verifique se o usuário passou um spec como argumento (ex: `/review-pr docs/specs/001-autenticacao-jwt.md`).

- **Se passou spec:** use o arquivo informado como fonte de CAs
- **Se não passou spec:** execute a revisão sem conformidade de spec (apenas qualidade + testes) e avise que a revisão completa requer `/review-pr <caminho-do-spec>`

## Passo 2 — Coletar o diff

Execute:
```bash
git diff main...HEAD
```

Se o branch base não for `main`, use `git diff origin/HEAD...HEAD` como fallback.

Se o diff estiver vazio, informe o usuário: "Nenhuma mudança encontrada em relação ao main. Verifique se está no branch correto."

## Passo 3 — Revisão em 4 dimensões

Analise o diff nas seguintes dimensões e registre os achados:

### 3a. Bugs e qualidade
- Lógica incorreta, condições de corrida, null pointer
- Funções com responsabilidade múltipla
- Duplicação que deveria ser extraída

### 3b. Segurança
- Inputs do usuário sem validação ou sanitização
- Dados sensíveis em logs ou respostas de API
- Autenticação/autorização ausente em endpoints novos
- Vulnerabilidades OWASP Top 10

### 3c. Testes
- Cada CA tem teste de caso feliz?
- Cada CA tem teste de caso de falha?
- Os testes validam comportamento ou apenas implementação interna?

### 3d. Conformidade com spec (se spec foi informado)
- Leia o spec e extraia os critérios de aceite
- Para cada CA, verifique se existe implementação no diff
- Para cada CA, verifique se existe teste correspondente

## Passo 4 — Emitir relatório

Formato obrigatório:

```
## Revisão de PR — [nome do branch] — [data]

### Achados

#### [SEVERIDADE] Descrição curta — arquivo:linha
**Problema:** o que está errado e por quê é um problema
**Sugestão:** correção concreta com exemplo de código se aplicável

[repita para cada achado]

---

### Conformidade com Spec
[apenas se spec foi informado]

- [x] CA-N: descrição → arquivo de implementação + nome do teste
- [ ] CA-N: descrição → AUSENTE — o que falta

---

### Resumo
- X críticos, Y altos, Z médios, W baixos
- CAs cobertos: N/Total [apenas se spec foi informado]

### Decisão
APROVADO | APROVADO COM RESSALVAS | SOLICITAR MUDANÇAS

Justificativa: [uma frase explicando a decisão]
```

## Regras de decisão

| Condição | Decisão |
|----------|---------|
| Zero CRÍTICO, zero ALTO, todos os CAs cobertos | APROVADO |
| Zero CRÍTICO, zero ALTO, ressalvas documentadas | APROVADO COM RESSALVAS |
| Qualquer CRÍTICO ou ALTO, ou CA ausente | SOLICITAR MUDANÇAS |

## Severidades

- `CRÍTICO`: pode causar incidente, perda de dados ou brecha de segurança — bloqueia merge
- `ALTO`: bug funcional ou falha de segurança não-crítica — deve corrigir antes do merge
- `MÉDIO`: problema real sem impacto imediato — discutir com o autor
- `BAIXO`: sugestão de melhoria ou estilo — opcional