# Workflow — Pipeline de Auditoria OWASP

## O pipeline de 5 etapas

```
Inventory → Analyze → Triage → Fix → Verify
```

### 1. Inventory

Antes de auditar, mapear o que existe na aplicação. O objetivo é ter uma lista de superfície de ataque — o que pode ser atacado e onde os dados sensíveis vivem.

```
Liste todos os endpoints HTTP do projeto, indicando para cada um:
- método (GET/POST/PUT/DELETE)
- se requer autenticação
- quais dados sensíveis recebe ou retorna (tokens, senhas, PII)
- quais dependências externas usa (banco, cache, serviços externos)
```

**Saída esperada:** tabela de endpoints com metadados de risco. Usada como input para o passo seguinte.

### 2. Analyze

Aplicar cada categoria OWASP ao código inventariado. Use a skill `/audit-owasp [arquivo]` para análise completa, ou o template em `03-templates/audit-owasp.md` para o fluxo manual.

A análise por categoria segue este padrão de saída:
- **Evidência**: trecho de código exato que constitui o risco (arquivo + linha)
- **Vetor**: como um atacante exploraria isso (passos concretos)
- **Severidade**: CRÍTICO / ALTO / MÉDIO / BAIXO / INFO
- **Recomendação**: código ou configuração específica para corrigir

### 3. Triage

Priorizar os achados por severidade e impacto:

| Severidade | Critério | Ação |
|------------|---------|------|
| CRÍTICO | Exploração direta sem autenticação, dados sensíveis em risco imediato | Bloquear deploy, corrigir antes do merge |
| ALTO | Requer condição adicional ou autenticação para explorar | Corrigir no sprint atual |
| MÉDIO | Risco em contexto específico ou com baixo impacto | Corrigir antes da próxima release |
| BAIXO | Hardening, boas práticas sem risco imediato | Backlog |
| INFO | Observação sem risco, melhoria sugerida | Documentar |

**Regra prática:** zero CRÍTICO e zero ALTO são pré-condição para deploy em produção.

### 4. Fix

Para cada achado CRÍTICO e ALTO, gerar a correção com o Claude Code:

```
Encontrei este achado OWASP A07 no arquivo app/services/auth.py:

[cole o trecho vulnerável]

Gere a correção que:
1. Adiciona rate limiting de 5 tentativas/minuto por IP
2. Adiciona log estruturado para tentativas falhas (email, IP, timestamp)
3. Mantém a interface existente (mesmos parâmetros e retorno)
4. Inclui um teste unitário para o caso de rate limit excedido
```

Sempre especifique:
- O achado (categoria + evidência)
- O comportamento esperado após a correção
- As restrições (não quebrar interface existente, manter compatibilidade)
- Se quer testes para o vetor corrigido

### 5. Verify

Após as correções:
1. Re-executar `/audit-owasp` no arquivo corrigido — confirmar que os achados sumiram
2. Rodar `pytest` para confirmar que nada quebrou
3. Se o achado não tinha teste cobrindo o vetor, adicionar um

## Integração no Workflow AIAD

O OWASP audit entra entre o PR Review (M4) e o deploy:

```
Spec (M2) → Testes (M3) → PR Review (M4) → OWASP Audit (M8) → Deploy
```

Também se encaixa no Módulo 5 (Issue Analysis): quando a issue tem componente de segurança, `/analyze-issue` deve classificar o tipo como `[SECURITY]` e recomendar auditoria OWASP antes da implementação.

## Cadência Recomendada

| Momento | O que auditar | Categorias em foco |
|---------|---------------|-------------------|
| Novo endpoint | O endpoint e suas dependências diretas | A01, A03, A07 |
| Nova dependência | O pacote adicionado e como é usado | A06 |
| Antes do deploy | Toda a aplicação | Top 10 completo |
| Incidente de segurança | Módulo afetado + adjacentes | Categoria do incidente + A09 |
| Refactor de autenticação | Auth service e middlewares | A02, A07, A01 |

## O Que Não Fazer

- **Não auditar só na véspera do deploy**: achados CRÍTICO neste ponto param o release inteiro
- **Não ignorar achados MÉDIO**: eles se acumulam e criam vetores compostos ao longo do tempo
- **Não confundir "sem achados" com "seguro"**: a auditoria é tão boa quanto o código fornecido — código morto, endpoints esquecidos e configs de infraestrutura ficam de fora da análise de arquivo