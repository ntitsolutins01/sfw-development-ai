# 06 — Subagents

## O que são Subagents

Subagents são **instâncias separadas do Claude Code** que executam tarefas
de forma independente, enquanto o agente principal continua trabalhando.

Pense como delegar trabalho para um colega: você passa a tarefa, ele trabalha
em paralelo, e você recebe o resultado quando ele termina — sem interromper
o que você estava fazendo.

## Por que usar Subagents

### Sem subagents (sequencial)
```
Você: "revise a segurança E rode os testes E verifique a cobertura"

IA:
1. Revisa segurança... (2 min)
2. Roda testes... (3 min)
3. Verifica cobertura... (1 min)
Total: 6 minutos
```

### Com subagents (paralelo)
```
Você: "revise a segurança E rode os testes E verifique a cobertura"

IA (agente principal):
  ├── Subagent A: Revisa segurança... (2 min)
  ├── Subagent B: Roda testes... (3 min)
  └── Subagent C: Verifica cobertura... (1 min)

Total: 3 minutos (limitado pelo mais lento)
```

## Tipos de Subagents

### 1. Fork — herda todo o contexto atual

Use quando a tarefa precisa saber tudo que aconteceu até agora.

```
Situação: você está no meio de uma implementação e quer uma segunda opinião
sem perder o contexto atual.

Você: "abra um fork para revisar a abordagem que estamos usando em pagamentos.py"

Fork herda: todos os arquivos lidos, decisões tomadas, contexto da conversa
```

**Quando usar fork:**
- Segunda opinião sobre uma decisão
- Pesquisa paralela que precisa do contexto
- Tarefas de análise do trabalho em andamento

### 2. Fresh Agent — começa do zero

Use quando a tarefa é independente e não precisa do contexto atual.

```
Situação: você quer pesquisar algo sem poluir seu contexto atual.

Você: "delegue para um novo agente a pesquisa sobre melhores práticas de rate limiting"

Fresh agent: começa sem nenhum contexto anterior
```

**Quando usar fresh agent:**
- Pesquisas independentes
- Tarefas que não têm relação com o trabalho atual
- Quando você quer isolamento completo

## Como Invocar Subagents no Claude Code

### Via prompt natural

```bash
# Dentro do Claude Code
> delegue para um subagente a tarefa de rodar os testes e me trazer o resultado

> use um fork para analisar em paralelo a cobertura de testes enquanto continuo aqui

> abra um agente especializado em segurança para revisar o arquivo pagamentos.py
```

### Comportamento esperado

```
Você: delegue para um agente a tarefa de verificar se há TODOs no código

Agente principal: Vou criar um subagente para essa busca.
[Subagent iniciado: buscando TODOs em todos os arquivos...]

Você: enquanto isso, me explique como funciona o fluxo de checkout

Agente principal: [explica o checkout]

[Notificação: Subagent concluiu]
Resultado: Encontrei 7 TODOs em 4 arquivos:
- src/pagamentos/service.py:45 - TODO: validar bandeira do cartão
- src/pedidos/models.py:12 - TODO: adicionar índice em data_criacao
...
```

## Casos de Uso Práticos

### 1. Pesquisa paralela

```
> quero entender três coisas ao mesmo tempo:
> 1. quais são as vulnerabilidades OWASP mais comuns em APIs Django?
> 2. como configurar rate limiting no Django REST Framework?
> 3. quais ferramentas de load test são mais usadas com Python?
> 
> delegue cada pesquisa para um subagente separado
```

### 2. Review em paralelo

```
> enquanto você implementa a feature de desconto, delegue para um fork
> a tarefa de revisar se a implementação atual de frete tem algum bug
```

### 3. Geração de testes em paralelo

```
> implemente a função calcular_total()
> em paralelo, delegue para um subagente a criação dos testes unitários
> baseado na especificação que você vai implementar
```

## Boas Práticas

1. **Fork para contexto compartilhado** — quando o subagente precisa saber o que aconteceu
2. **Fresh agent para isolamento** — quando a tarefa é completamente independente
3. **Seja específico no briefing** — um subagente sem contexto precisa de instruções completas
4. **Não delegue tarefas de 30 segundos** — o overhead de criar um agente não compensa
5. **Use para I/O bound** — esperar API, rodar testes, buscar arquivos — não para tarefas de raciocínio puro

## Como Saber se Vale a Pena Usar Subagents

| Situação | Recomendação |
|----------|--------------|
| Tarefa leva > 1 min e é independente | ✅ Use subagent |
| Precisa de contexto da conversa atual | ✅ Use fork |
| Tarefa leva < 30s | ❌ Faça direto |
| Tarefas dependentes entre si | ❌ Faça sequencialmente |
| Pesquisas independentes simultâneas | ✅ Fork paralelos |

## Limitações

- Subagents não têm acesso ao estado da conversa do agente principal (exceto forks)
- O resultado retorna como mensagem — não há estado compartilhado em tempo real
- Usar subagents consome tokens adicionais — pese o custo vs. benefício de tempo
