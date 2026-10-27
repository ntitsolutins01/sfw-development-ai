# quality-gate

Você foi invocado via `/quality-gate`.

## Passo 1 — Identificar o escopo

Verifique se o usuário especificou um gate específico:
- `--coverage` → apenas gate de cobertura
- `--complexity` → apenas gate de complexidade
- `--security` → apenas gate de segurança
- `--all` ou sem argumento → todos os gates

Se não especificou, execute todos.

---

## Passo 2 — Detectar configuração existente

Antes de executar, leia:
1. `pyproject.toml` — configuração de pytest-cov, ruff, mypy
2. `setup.cfg` — configuração alternativa
3. `Makefile` — targets de quality gates existentes
4. `.github/workflows/` — pipelines de CI configurados

Para cada gate, determine:
- **Configurado:** threshold definido, ferramenta instalada → executar
- **Ausente:** ferramenta não encontrada ou threshold não definido → reportar como AUSENTE e oferecer configuração

---

## Passo 3 — Executar os gates disponíveis

Para cada gate configurado, execute via Bash e capture o resultado.

### Gate de Cobertura (pytest-cov)

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=[threshold]
```

Se o threshold não estiver configurado, execute sem `--cov-fail-under` para medir o estado atual.

Interpretar:
- Exit code 0 → PASSOU
- Exit code 2 → FALHOU (coverage abaixo do threshold)
- Comando não encontrado → AUSENTE

### Gate de Complexidade (radon)

```bash
radon cc app/ -s --min C
```

Interpretar:
- Saída vazia → PASSOU (nenhuma função acima de grade C)
- Saída com funções listadas → FALHOU
- Comando não encontrado → AUSENTE

### Gate de Segurança Estática (bandit)

```bash
bandit -r app/ -ll
```

Interpretar:
- Exit code 0 → PASSOU
- Exit code 1 → FALHOU (HIGH ou MEDIUM encontrado)
- Comando não encontrado → AUSENTE

### Gate de Dependências (pip-audit)

```bash
pip-audit --requirement requirements.txt
```

Interpretar:
- Exit code 0 → PASSOU
- Exit code 1 → FALHOU (CVE encontrado)
- Comando não encontrado → AUSENTE

---

## Passo 4 — Gerar o relatório

Produza o relatório no seguinte formato para cada gate:

```
## Quality Gate Report — [nome do projeto]

### Cobertura de Testes
**Status:** PASSOU ✅ | FALHOU ❌ | AUSENTE ⚠️

[Se PASSOU:]
Cobertura atual: X% (threshold: Y%)

[Se FALHOU:]
Cobertura atual: X% (threshold: Y%, gap: −Z%)
Arquivos mais críticos:
- [arquivo] — X% ([N] linhas descobertas)
...
Próximo passo: gerar os testes com maior impacto?

[Se AUSENTE:]
pytest-cov não encontrado ou threshold não configurado.
Instale com: pip install pytest-cov
Configure em pyproject.toml: --cov-fail-under=80

---

### Complexidade Ciclomática
**Status:** PASSOU ✅ | FALHOU ❌ | AUSENTE ⚠️

[Se FALHOU:]
Funções acima do threshold (grade C, score > 10):
- [arquivo:linha] [nome] — [grade] ([score])
Próximo passo: gerar refatoração?

---

### Segurança Estática (bandit)
**Status:** PASSOU ✅ | FALHOU ❌ | AUSENTE ⚠️

[Se FALHOU:]
[achados HIGH e MEDIUM]

---

### Dependências (pip-audit)
**Status:** PASSOU ✅ | FALHOU ❌ | AUSENTE ⚠️

---

## Sumário

| Gate | Status | Ação necessária |
|------|--------|----------------|
| Cobertura ≥ N% | PASSOU ✅ / FALHOU ❌ / AUSENTE ⚠️ | ... |
| Complexidade ≤ C | ... | ... |
| Segurança (bandit) | ... | ... |
| Dependências (pip-audit) | ... | ... |
| GitHub Actions | CONFIGURADO ✅ / AUSENTE ⚠️ | ... |

N FALHOU, N PASSOU, N AUSENTE
```

---

## Passo 5 — Oferecer ações

Ao final do relatório, para cada gate com status FALHOU ou AUSENTE, ofereça:

**Para FALHOU:**
- Coverage: "Gerar os N testes com maior impacto de cobertura?"
- Complexidade: "Gerar refatoração para [função] que reduz complexidade para abaixo de 10?"
- Segurança: "Mostrar a correção para cada achado?"

**Para AUSENTE:**
- "Gerar a configuração para [gate] no pyproject.toml?"
- "Gerar o workflow de GitHub Actions com todos os gates?"

Aguarde a resposta do usuário antes de executar qualquer correção ou geração de configuração.

---

## Comportamento Especial

**Projeto sem nenhum gate configurado:** reporte todos como AUSENTE e pergunte:
"Nenhum quality gate configurado. Deseja configurar o conjunto básico (coverage + complexidade + bandit)? Vou gerar o pyproject.toml e o workflow de GitHub Actions."

**Pasta `app/` não encontrada:** procure por `src/`, `lib/` ou o padrão do projeto antes de reportar que não há código para auditar. Se não encontrar, peça ao usuário que informe a pasta principal.

**Sem requirements.txt:** o gate de pip-audit reporta AUSENTE e sugere: "Gere um requirements.txt com `pip freeze > requirements.txt` antes de executar pip-audit."