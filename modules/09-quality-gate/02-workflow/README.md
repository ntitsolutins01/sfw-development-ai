# Workflow — Configurando Quality Gates

## O pipeline de 5 etapas

```
Definir → Implementar → Integrar → Monitorar → Ajustar
```

### 1. Definir

Antes de configurar ferramentas, decidir o que importa para este projeto:

```
Para cada gate, responder:
1. Qual métrica representa qualidade para este projeto?
2. Qual é o mínimo aceitável agora (threshold inicial)?
3. Onde no pipeline este gate deve bloquear?
4. O que acontece quando falha? (mensagem de erro, link para docs)
```

**Ponto de partida para thresholds:**

| Gate | Como definir o threshold inicial |
|------|--------------------------------|
| Coverage | Execute `pytest --cov` hoje. Threshold = resultado atual − 5% |
| Complexidade | Execute `radon cc -s .` hoje. Threshold = grade mais comum − 1 letra |
| Latência (P95) | Meça em staging. Threshold = medição atual × 1.2 (20% de margem) |

O objetivo inicial é não piorar. A partir daí, apertar gradualmente.

### 2. Implementar

Configurar as ferramentas localmente primeiro — sempre.

**Cobertura:**
```bash
# instalar
pip install pytest-cov

# configurar em pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=app --cov-report=term-missing --cov-fail-under=80"

# rodar
pytest
# → falha com exit code 2 se coverage < 80%
```

**Complexidade:**
```bash
# instalar
pip install radon

# checar complexidade
radon cc app/ -s -a
# → grade A (1-5), B (6-10), C (11-15), D (16-20), E (21-25), F (26+)

# gate: falhar se qualquer função tiver grade > C (complexidade > 10)
radon cc app/ -s --min C
# → exit code 1 se alguma função tiver complexidade >= 11
```

**Verificar antes de abrir PR (Makefile):**
```makefile
quality:
	pytest
	radon cc app/ -s --min C
	ruff check app/

.PHONY: quality
```

### 3. Integrar

Adicionar os gates ao pipeline de CI. Ver template completo em `03-templates/github-actions-gates.md`.

Ordem de execução (da mais rápida para a mais lenta):
1. Análise estática (`ruff`, `mypy`) → segundos
2. Testes + coverage → segundos a minutos
3. Complexidade (`radon`) → segundos
4. Análise de segurança (`bandit`, resultado OWASP) → segundos a minutos
5. Teste de carga (`locust`) → minutos (só em staging)

Gates mais rápidos primeiro: falha rápida tem feedback loop mais curto.

### 4. Monitorar

Após configurar os gates, acompanhar tendências:

- **Coverage caindo**: nova feature sem teste passou pelo gate? Threshold muito baixo
- **Complexidade aumentando**: refactor necessário, ou threshold está errado
- **Gate de complexidade bloqueando PRs frequentemente**: threshold muito rígido para o estágio atual do projeto

Uma semana de dados já revela se os thresholds estão calibrados.

### 5. Ajustar

Apertar gradualmente à medida que o projeto amadurece:

| Métrica | Progressão sugerida |
|---------|-------------------|
| Coverage | +5% a cada quarter até 85–90% |
| Complexidade | Grade D → C → B ao longo de refactoring cycles |
| Latência P95 | Revise SLA após cada mudança de infraestrutura |

Nunca apertar de uma vez — mudanças grandes em threshold criam avalanche de falhas e resistência do time.

## Integração com o Workflow AIAD

```
Spec (M2) → Testes (M3) → PR Review (M4) → OWASP (M8) → Quality Gates (M9) → Deploy
```

Gates que reaproveitam artefatos dos módulos anteriores:
- **Gate dinâmico** = testes do Módulo 3 + threshold de coverage
- **Gate de segurança** = resultado do `/audit-owasp` do Módulo 8 como requisito de PR
- **Gate de design** = feedback do `/review-pr` do Módulo 4 sobre complexidade percebida

## Decisão: Gate no PR vs Gate no Deploy

| Situação | Gate no PR | Gate no Deploy |
|---------|-----------|---------------|
| Análise estática | ✅ (rápido, feedback imediato) | ❌ (tarde demais) |
| Coverage | ✅ (bloqueia o merge) | ⚠️ (só se não tiver no PR) |
| Segurança (OWASP) | ✅ (zero CRÍTICO/ALTO como requisito) | ✅ (gate adicional de staging) |
| Latência | ❌ (precisa de serviço rodando) | ✅ (em staging antes de produção) |

Regra: **quanto mais cedo o gate, mais barato o fix.** Detectar cobertura baixa no commit é mais barato que detectar em staging.