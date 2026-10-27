# Template — Gate de Complexidade com radon

## O que é complexidade ciclomática

Complexidade ciclomática mede o número de caminhos de execução independentes em uma função. Cada `if`, `elif`, `for`, `while`, `except`, `and`, `or` adiciona 1 ao contador.

Escala radon:

| Complexidade | Grade | Interpretação |
|-------------|-------|---------------|
| 1–5 | A | Simples, baixo risco |
| 6–10 | B | Complexidade moderada, aceitável |
| 11–15 | C | Complexidade elevada — considere refatorar |
| 16–20 | D | Alta — refatorar antes do merge |
| 21–25 | E | Muito alta — problema sério |
| 26+ | F | Não testável de forma confiável |

**Threshold recomendado:** máximo grade C (complexidade ≤ 10) para código novo. Código legado: comece em D e vá apertando.

## Instalação

```bash
pip install radon
```

## Uso Básico

```bash
# Mostrar complexidade de todas as funções com grade e score
radon cc app/ -s

# Mostrar apenas funções com grade C ou pior (11+)
radon cc app/ -s --min C

# Resumo agregado por arquivo
radon cc app/ -s -a

# Gate: exit code 1 se alguma função tiver complexidade > 10
radon cc app/ --min C --show-complexity
```

## Makefile

```makefile
complexity:
	radon cc app/ -s -a

complexity-check:
	@echo "Verificando complexidade ciclomática (max: B, score 10)..."
	@radon cc app/ -s --min C; \
	if [ $$? -ne 0 ]; then \
		echo "FALHOU: Funções com complexidade > 10 encontradas"; \
		exit 1; \
	else \
		echo "PASSOU: Nenhuma função acima da grade C"; \
	fi

.PHONY: complexity complexity-check
```

## Script Python para gate (mais controle)

```python
# scripts/check_complexity.py
import subprocess
import sys

MAX_COMPLEXITY = 10

result = subprocess.run(
    ["radon", "cc", "app/", "-s", "--min", "C"],
    capture_output=True,
    text=True
)

if result.stdout.strip():
    print("GATE FALHOU — Funções com complexidade > 10:")
    print(result.stdout)
    sys.exit(1)
else:
    print("GATE PASSOU — Nenhuma função acima da complexidade 10")
    sys.exit(0)
```

## pyproject.toml (via ruff para algumas métricas)

```toml
[tool.ruff]
select = [
    "C901",  # complexidade ciclomática via McCabe
]

[tool.ruff.mccabe]
max-complexity = 10  # equivalente ao radon grade B/C
```

## Prompt para o Claude Code identificar candidatos a refatoração

```
Execute radon cc app/ -s -a e me mostre:
1. As 5 funções com maior complexidade ciclomática
2. Para cada uma, explique quais ramos de código contribuem para a complexidade
3. Sugira como refatorar a função com maior complexidade para reduzir a score abaixo de 10,
   mantendo todos os testes existentes passando
```

## Prompt para interpretar uma falha do gate

```
O gate de complexidade falhou com este output:

[COLE O OUTPUT DO radon cc]

Para a função com maior complexidade:
1. Mostre o código atual
2. Identifique quais condicionais contribuem mais para a complexidade
3. Proponha uma refatoração que:
   - Reduza a complexidade para abaixo de 10
   - Não altere o comportamento observável
   - Não quebre os testes existentes
```

## Saída esperada

```bash
$ radon cc app/ -s --min C
app/services/auth.py
    F 45:0 verify_token - D (14)   # ← gate falha aqui

$ radon cc app/ -s -a
app/services/auth.py
    F 45:0 verify_token - B (8)    # ← após refatoração: passou
    F 12:0 create_token - A (3)

    Average complexity: A (5.5)
```