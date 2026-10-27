# IA no Fluxo — Skill `/quality-gate`

## O que a skill faz

`/quality-gate` verifica o estado dos quality gates do projeto em 4 etapas:

1. **Detect**: lê as configurações existentes (pyproject.toml, .github/workflows/, Makefile)
2. **Run**: executa as ferramentas disponíveis (pytest-cov, radon, bandit, pip-audit)
3. **Report**: gera relatório com status de cada gate (PASSOU / FALHOU / AUSENTE)
4. **Fix**: para gates falhando ou ausentes, oferece gerar a configuração ou a correção

## Como Invocar

```
/quality-gate
```

Executa todos os gates disponíveis. Para um gate específico:

```
/quality-gate --coverage
/quality-gate --complexity
/quality-gate --security
```

## Exemplo de Saída

```
## Quality Gate Report — sfw-development-ai/app/

### Cobertura de Testes
Status: FALHOU

Cobertura atual: 71%
Threshold configurado: 80%
Gap: −9%

Arquivos mais críticos:
- app/services/token_blocklist.py — 42% (12 linhas descobertas)
- app/routers/auth.py — 68% (9 linhas descobertas)
- app/core/security.py — 100% ✅

Próximo passo: gerar os 3 testes com maior impacto? (sim/não)

---

### Complexidade Ciclomática
Status: FALHOU

Funções acima do threshold (grade C, score > 10):
- app/services/auth.py:45 verify_token — D (14)

Próximo passo: gerar refatoração para verify_token? (sim/não)

---

### Análise de Segurança (bandit)
Status: PASSOU ✅

Nenhuma vulnerabilidade HIGH ou MEDIUM encontrada.

---

### Dependências (pip-audit)
Status: AUSENTE — pip-audit não encontrado

Instale com: pip install pip-audit
Execute: pip-audit --requirement requirements.txt

---

## Sumário

| Gate | Status | Ação necessária |
|------|--------|----------------|
| Cobertura ≥ 80% | FALHOU | Adicionar 3 testes |
| Complexidade ≤ C | FALHOU | Refatorar verify_token |
| Segurança (bandit) | PASSOU ✅ | — |
| Dependências (pip-audit) | AUSENTE | Instalar e configurar |
| GitHub Actions | AUSENTE | Gerar workflow? |

2 FALHOU, 1 PASSOU, 2 AUSENTE
```

## Como Usar os Resultados

### Corrigir coverage insuficiente

```
O gate de coverage falhou: 71% com threshold de 80%.
Os arquivos mais críticos são token_blocklist.py (42%) e auth.py (68%).

Para token_blocklist.py, gere testes que cubram:
1. Adicionar token à blocklist
2. Verificar se token está na blocklist (presente e ausente)
3. Comportamento quando a blocklist está vazia

Mantenha o padrão pytest existente (fixtures, conftest.py).
```

### Corrigir função com complexidade alta

```
verify_token tem complexidade D (score 14).
Código atual:

[cole o código da função]

Refatore para:
1. Reduzir a complexidade para abaixo de 10 (grade B)
2. Extrair responsabilidades em funções auxiliares com nomes descritivos
3. Manter a mesma interface pública (mesmos parâmetros e retorno)
4. Não quebrar nenhum teste existente
```

### Gerar configuração ausente

```
O gate de GitHub Actions está ausente.
Gere um workflow .github/workflows/quality-gates.yml que:
1. Rode em PRs para main
2. Execute lint (ruff), typecheck (mypy), testes com coverage >= 80%,
   complexidade (radon max C) e bandit
3. Gates mais rápidos primeiro
4. Mostre o relatório de coverage no PR
```

## Fluxo Recomendado de Adoção

Para projetos sem nenhum gate configurado:

**Semana 1:** Medir o estado atual (sem falhar nada)
```
/quality-gate  # apenas medir, sem thresholds
```

**Semana 2:** Adicionar gates com thresholds baixos (coverage atual − 5%)
```
Configure pyproject.toml com coverage = [resultado da semana 1 - 5%]
```

**Semana 3:** Adicionar ao GitHub Actions
```
/quality-gate  # gerar workflow
```

**Em diante:** Apertar thresholds a cada quarter

## Quando a IA Ajuda vs Quando Requer Julgamento

**IA ajuda:**
- Calibrar threshold inicial com base na medição atual
- Identificar quais testes adicionar para o maior ganho de coverage
- Refatorar funções para reduzir complexidade
- Gerar configuração de GitHub Actions

**Requer julgamento humano:**
- Decidir se a complexidade de uma função é inerente ao domínio ou evitável
- Decidir quando apertar thresholds (impacto no time)
- Decidir se um achado do bandit é falso positivo no contexto do projeto
- Definir SLAs de latência para o teste de carga