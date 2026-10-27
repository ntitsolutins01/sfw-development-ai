# Exemplo — Quality Gate em Pipeline LLM (JEV)

## Contexto

O `shared/jev/` implementa dois quality gates aplicados antes que qualquer input
chegue ao LLM. O conceito é idêntico ao de quality gates de CI/CD: critério
objetivo → decisão binária → bloqueia ou deixa passar.

O pipeline sem JEV:
```
Input → Embedding → Vector Search → LLM → Resposta
```
Cada requisição passa pela pipeline completa — uma saudação ("oi") custa o mesmo
que uma pergunta substantiva sobre um documento.

O pipeline com JEV:
```
Input → [Intent Gate] → Embedding → [Chunk Scorer] → LLM → Resposta
          ↓ GREETING/META                ↓ similarity < 0.5
        Resposta fixa               Chunk descartado
        (< 1ms)
```

## Os dois gates

### Gate 1 — Intent Gate (`shared/jev/intent_gate.py`)

**Critério:** `intent == ANSWERABLE`  
**O que bloqueia:** inputs GREETING (`"oi"`, `"bom dia"`) e META (`"o que você faz?"`)  
**Ação de bloqueio:** retorna resposta fixa sem tocar o vector store ou o LLM  
**Custo quando bloqueia:** < 1ms (regex + lookup set)

```python
from shared.jev.intent_gate import IntentGate, Intent

gate = IntentGate()
result = gate.classify("oi, tudo bem?")

print(result.intent)        # Intent.GREETING
print(result.short_circuit) # True → não vai para o LLM
print(result.response)      # "Olá! Posso ajudar com perguntas sobre os documentos."
```

Analogia com CI/CD:
```
# CI/CD
if coverage < 80%:
    fail_build()

# Intent Gate
if intent != ANSWERABLE:
    return_fixed_response()  # sem embedding, sem LLM
```

### Gate 2 — Chunk Scorer (`shared/jev/chunk_scorer.py`)

**Critério:** `similarity >= threshold` (padrão: 0.5)  
**O que bloqueia:** chunks semanticamente distantes do input  
**Ação de bloqueio:** chunk é removido do contexto antes de montar o prompt  
**Custo quando bloqueia:** 0 tokens de contexto para o LLM

```python
from shared.jev.chunk_scorer import ChunkScorer

scorer = ChunkScorer(threshold=0.5)
chunks = vector_store.search(query, top_k=5)
filtered = scorer.filter(query, chunks)

print(f"Chunks recuperados: {len(chunks)}")     # 5
print(f"Chunks aprovados: {len(filtered)}")      # 3 (2 descartados por baixa similaridade)
```

Analogia com CI/CD:
```
# CI/CD
if cyclomatic_complexity > 10:
    fail_build()

# Chunk Scorer
if similarity < threshold:
    discard_chunk()  # não vai para o prompt do LLM
```

## Observabilidade dos Gates

Ambos os gates são observáveis — o campo `jev` na resposta documenta cada decisão:

```json
{
  "answer": "A expiração do token é configurada em ACCESS_TOKEN_EXPIRE_MINUTES.",
  "jev": {
    "intent": "ANSWERABLE",
    "short_circuited": false,
    "chunks_retrieved": 5,
    "chunks_accepted": 3,
    "chunks_rejected": 2,
    "similarity_threshold": 0.5,
    "scores": [0.82, 0.71, 0.63, 0.41, 0.38]
  }
}
```

Equivalente ao relatório de quality gates de CI/CD:
```
Gate de cobertura: PASSOU (92%)
Gate de complexidade: PASSOU (max score: 8)
Gate de segurança: PASSOU (0 HIGH/MEDIUM)
```

## Configurando os Thresholds

O mesmo princípio de calibração se aplica:

**Threshold muito baixo (0.2):** todos os chunks passam → contexto irrelevante no prompt → respostas genéricas  
**Threshold muito alto (0.8):** quase nenhum chunk passa → contexto insuficiente → respostas sem embasamento  
**Threshold inicial:** meça a distribuição de scores em queries reais, defina em ~P30 dos scores  

```python
# Como calibrar o threshold do Chunk Scorer
scores = []
for query, chunks in sample_queries:
    for chunk in chunks:
        scores.append(scorer.score(query, chunk))

import statistics
print(f"P30: {sorted(scores)[int(len(scores)*0.30)]:.2f}")  # threshold inicial
print(f"P50: {statistics.median(scores):.2f}")
print(f"P70: {sorted(scores)[int(len(scores)*0.70)]:.2f}")
```

## Comparativo: Gates de CI/CD vs Gates de LLM Pipeline

| Dimensão | Gate de CI/CD | Gate de LLM Pipeline |
|----------|--------------|---------------------|
| O que mede | Qualidade do código | Qualidade do input/contexto |
| Critério | `coverage >= 80%` | `intent == ANSWERABLE` |
| Ação de bloqueio | Falha o build | Short-circuit ou descarte |
| Observabilidade | Relatório de coverage/complexidade | Campo `jev` na resposta |
| Calibração | Threshold baseado em métricas de código | Threshold baseado em distribuição de scores |
| Trade-off | Muito rígido → bloqueia PRs legítimos | Muito rígido → contexto insuficiente |

## Referência de Código

Os arquivos completos com implementação, testes e exemplos de uso estão em `shared/jev/`:

```
shared/jev/
├── intent_gate.py          ← IntentGate com regex e lookup set
├── chunk_scorer.py         ← ChunkScorer com threshold configurável
├── exemplos/
│   ├── uso_pipeline.py     ← pipeline completo com ambos os gates
│   └── uso_agente.py       ← loop de agente com gates e caching
└── README.md               ← documentação completa do JEV
```

Para o Módulo 14 (LLM as a Judge): o terceiro gate — avaliar a qualidade da resposta gerada antes de retorná-la ao usuário — é documentado lá com exemplos de métricas (fidelidade, relevância, ausência de alucinações).