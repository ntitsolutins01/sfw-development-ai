# Template — Gate de Cobertura com pytest-cov

## Instalação

```bash
pip install pytest pytest-cov
```

## Configuração em `pyproject.toml`

```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=app",                  # pasta a medir (ajuste para o seu projeto)
    "--cov-report=term-missing",  # mostra linhas não cobertas no terminal
    "--cov-report=html:coverage_html",  # relatório HTML em coverage_html/
    "--cov-fail-under=80",        # falha se coverage < 80%
]
testpaths = ["tests"]

[tool.coverage.run]
branch = true                     # mede branch coverage além de line coverage
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
```

## Configuração em `setup.cfg` (alternativa)

```ini
[tool:pytest]
addopts = --cov=app --cov-report=term-missing --cov-fail-under=80

[coverage:run]
branch = True
omit =
    */migrations/*
    */tests/*
    */__init__.py
```

## Makefile

```makefile
test:
	pytest

coverage:
	pytest --cov=app --cov-report=html
	@echo "Relatório HTML em coverage_html/index.html"

coverage-check:
	pytest --cov=app --cov-fail-under=80
	@echo "Gate de cobertura: PASSOU (>= 80%)"
```

## Prompt para o Claude Code calibrar o threshold

```
Execute pytest --cov=app --cov-report=term-missing no projeto e me diga:
1. Qual é a cobertura atual total?
2. Quais arquivos têm cobertura abaixo de 70%?
3. Quais linhas estão descobertas nos arquivos críticos (auth.py, services/)?

Com base nisso, sugira:
- O threshold inicial (cobertura atual - 5%)
- Quais 3 arquivos priorizar para aumentar coverage com o menor esforço
```

## Prompt para interpretar uma falha do gate

```
O gate de coverage falhou com este output:

[COLE O OUTPUT DO pytest --cov]

Analise:
1. Quais funções/métodos estão com as piores coberturas?
2. Qual é o caminho de código mais relevante que não está coberto?
3. Gere os 2 testes com maior impacto para aumentar a cobertura total
```

## Saída esperada quando o gate passa

```
---------- coverage: platform... ----------
Name                    Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------
app/services/auth.py       45      4      8      2    89%
app/routers/auth.py        28      2      4      1    91%
app/core/security.py       22      0      2      0   100%
---------------------------------------------------------
TOTAL                      95      6     14      3    92%

Required test coverage of 80% reached. Total coverage: 92%
```

## Saída quando o gate falha (exit code 2)

```
TOTAL                      95     24     14      6    71%

FAIL Required test coverage of 80% not reached. Total coverage: 71%
```

## Configuração por módulo (diferentes thresholds por pasta)

```toml
[tool.coverage.report]
# thresholds diferentes por componente crítico
fail_under = 80

[tool.pytest.ini_options]
# se quiser thresholds por arquivo (requer pytest-cov >= 4.0)
addopts = [
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
]
```