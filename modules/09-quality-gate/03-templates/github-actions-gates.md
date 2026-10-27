# Template — GitHub Actions com Quality Gates

Pipeline completo com gates em ordem de velocidade (mais rápidos primeiro).

## `.github/workflows/quality-gates.yml`

```yaml
name: Quality Gates

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]

jobs:
  # Gate 1: Análise Estática (mais rápido — secondos)
  static-analysis:
    name: Static Analysis Gate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install ruff mypy

      - name: Lint (ruff)
        run: ruff check app/

      - name: Type check (mypy)
        run: mypy app/ --ignore-missing-imports

  # Gate 2: Cobertura de Testes (médio — depende da suite de testes)
  coverage:
    name: Coverage Gate (>= 80%)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-cov

      - name: Run tests with coverage
        run: pytest --cov=app --cov-report=xml --cov-fail-under=80

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        if: always()
        with:
          file: ./coverage.xml

  # Gate 3: Complexidade Ciclomática (rápido — segundos)
  complexity:
    name: Complexity Gate (max grade C)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install radon
        run: pip install radon

      - name: Check cyclomatic complexity
        run: |
          OUTPUT=$(radon cc app/ -s --min C)
          if [ -n "$OUTPUT" ]; then
            echo "GATE FALHOU: Funções com complexidade > 10 encontradas:"
            echo "$OUTPUT"
            exit 1
          fi
          echo "GATE PASSOU: Nenhuma função acima da complexidade 10"

  # Gate 4: Segurança Estática (rápido — segundos)
  security-static:
    name: Security Gate (bandit)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install bandit
        run: pip install bandit

      - name: Run bandit security scan
        run: bandit -r app/ -ll  # falha em HIGH e MEDIUM (-ll = level LOW ignorado)
```

## Gate de Dependências Vulneráveis (separado)

```yaml
  # Gate 5: Dependências com CVE (pip-audit)
  dependency-audit:
    name: Dependency Audit Gate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install pip-audit
        run: pip install pip-audit

      - name: Audit dependencies
        run: pip-audit --requirement requirements.txt
        # falha automaticamente se qualquer CVE for encontrado
```

## Gate de Teste de Carga (só em staging — job manual)

```yaml
  # Gate 6: Latência sob carga (workflow separado, disparado manualmente ou em merge para main)
  load-test:
    name: Load Test Gate (P95 < 500ms)
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch'  # só manual
    steps:
      - uses: actions/checkout@v4

      - name: Install locust
        run: pip install locust

      - name: Run load test
        run: |
          locust --headless \
            --users 50 \
            --spawn-rate 10 \
            --run-time 60s \
            --host http://staging.example.com \
            --locustfile tests/load/locustfile.py \
            --html load_report.html \
            --exit-code-on-error 1

      - name: Upload load test report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: load-test-report
          path: load_report.html
```

## Makefile equivalente (para rodar localmente)

```makefile
# Rodar todos os gates localmente antes de abrir PR
gates: lint typecheck test complexity security

lint:
	ruff check app/

typecheck:
	mypy app/ --ignore-missing-imports

test:
	pytest --cov=app --cov-fail-under=80

complexity:
	@OUTPUT=$$(radon cc app/ -s --min C); \
	if [ -n "$$OUTPUT" ]; then echo "FALHOU:\n$$OUTPUT"; exit 1; fi; \
	echo "Complexidade: PASSOU"

security:
	bandit -r app/ -ll

deps:
	pip-audit --requirement requirements.txt

.PHONY: gates lint typecheck test complexity security deps
```