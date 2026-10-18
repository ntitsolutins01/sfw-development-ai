# rodar-testes

## Objetivo
Executar a suite de testes do projeto, interpretar os resultados e reportar
o que passou, o que falhou e sugerir correções para falhas.

## Quando usar
- Após fazer qualquer mudança de código
- Antes de abrir um PR
- Quando um teste misteriosamente falha em CI mas não localmente

## O que ela faz

1. Detecta o tipo de projeto (Python/pytest, Node/vitest, etc.)
2. Executa o comando de teste adequado com flag de cobertura
3. Analisa a saída:
   - Lista testes que falharam com o erro exato
   - Calcula percentual de cobertura por módulo
   - Identifica arquivos sem cobertura alguma
4. Para cada falha: explica a causa provável e sugere correção
5. Apresenta resumo final com status geral (verde/amarelo/vermelho)

## Detecção automática de frameworks

| Arquivo presente | Framework assumido | Comando |
|------------------|--------------------|---------|
| `pytest.ini` / `pyproject.toml` com `[pytest]` | pytest | `pytest --cov` |
| `package.json` com `"vitest"` | vitest | `npm test -- --coverage` |
| `package.json` com `"jest"` | jest | `npm test -- --coverage` |
| `go.mod` | go test | `go test ./... -cover` |

## O que ela NÃO faz
- Não modifica código para fazer testes passarem (apenas sugere)
- Não ignora testes — reporta todas as falhas

## Formato do relatório

```
## Resultado dos Testes — [data/hora]

Status: ✅ PASSOU / ⚠️ FALHOU

### Resumo
- 47 passou, 2 falhou, 1 pulado
- Cobertura geral: 78%

### Falhas

#### tests/test_pedidos.py::test_calcular_total_com_desconto
**Erro:** AssertionError: expected 90.0, got 100.0
**Causa provável:** O desconto não está sendo aplicado antes do cálculo do frete.
**Sugestão:** Verifique a ordem das operações em `calcular_total()`.

### Cobertura por Módulo
| Módulo | Cobertura |
|--------|-----------|
| apps/pedidos | 92% |
| apps/usuarios | 85% |
| apps/pagamentos | 41% ⚠️ |
```

## Argumentos aceitos
- `/rodar-testes` — roda todos os testes
- `/rodar-testes pedidos` — roda só os testes do módulo pedidos
- `/rodar-testes --falhas-apenas` — mostra só o que falhou

## Exemplo de uso

```
/rodar-testes
```
