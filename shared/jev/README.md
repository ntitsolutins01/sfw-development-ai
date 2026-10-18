# shared/jev — Camada de Decisão para Pipelines com Retrieval

## O que é esta pasta

Implementação de referência do **JEV** — camada de decisão leve que atua
antes e entre as etapas caras de um pipeline RAG ou de qualquer fluxo que
combina retrieval vetorial + LLM.

Não é um módulo do curso — é uma biblioteca interna compartilhada.

Os módulos que constroem pipelines com retrieval importam daqui:

| Módulo | Por que precisa |
|--------|----------------|
| 12 — Hermes Agent | Agente com base de conhecimento: filtra saudações e chunks irrelevantes antes do LLM |
| 14 — LLM as a Judge | Avaliações em lote: descarta amostras fora do escopo antes de avaliar |
| 09 — Quality Gate | JEV é um exemplo concreto de quality gate em pipeline LLM (referência didática) |

---

## O problema que o JEV resolve

Sem JEV, um pipeline executa a sequência completa para qualquer entrada —
inclusive para "olá" ou chunks com similaridade 0.1:

```
"olá" → embed → busca vetorial → LLM
                                  ↑ custou tokens à toa
```

Com JEV, decisões triviais são tratadas antes, de forma determinística e barata:

```
"olá"
  └── [Intent Gate] → GREETING → resposta fixa ← para aqui, sem embedding, sem LLM

"qual o prazo de entrega?"
  └── [Intent Gate] → ANSWERABLE → segue
        └── embed → busca vetorial → chunks
              └── [Chunk Scorer] → filtra por similaridade
                    ├── chunks relevantes → LLM
                    └── chunks irrelevantes → descartados
```

---

## Os dois componentes

### 1. Intent Gate (`intent_gate.py`)

Classifica a **intenção da pergunta** antes de qualquer operação de embedding.

| Intent | Exemplo | Comportamento |
|--------|---------|---------------|
| `GREETING` | "olá", "bom dia", "hi" | Resposta fixa — sem retrieval, sem LLM |
| `META` | "o que você pode fazer?" | Resposta fixa descrevendo o sistema |
| `ANSWERABLE` | "qual é o prazo de entrega?" | Segue para o pipeline completo |

Retorna um `IntentDecision` com `short_circuit=True` quando a pergunta não
precisa chegar ao LLM.

### 2. Chunk Scorer (`chunk_scorer.py`)

Filtra os chunks recuperados pelo banco vetorial **antes do LLM**, usando
a distância cosseno que o ChromaDB (ou qualquer banco com `hnsw:space=cosine`)
já retorna gratuitamente.

```
similaridade = 1 - distância_cosseno

0.9 → muito relevante  ✅ aceito
0.5 → no limite        ✅ aceito (threshold padrão = 0.5)
0.3 → pouco relevante  ❌ rejeitado
```

Retorna um `ScoringResult` com `accepted` e `rejected`. Se `accepted` estiver
vazio, o pipeline retorna uma resposta estruturada sem acionar o LLM.

---

## Quando Vale a Pena Usar

| Situação | Usar JEV? |
|----------|-----------|
| Pipeline com retrieval vetorial e entrada livre do usuário | ✅ Sim |
| Agente que responde perguntas sobre documentos | ✅ Sim |
| Avaliações LLM em lote com filtragem de amostras | ✅ Sim (chunk scorer adaptado) |
| Chamada LLM simples sem retrieval | ❌ Não — não há chunks para filtrar |
| System prompt fixo sem input de usuário | ❌ Não — não há intent a classificar |

---

## Como Importar nos Módulos

```python
# Adicione shared/ ao PYTHONPATH (ou rode da raiz do projeto)
from shared.jev.intent_gate import IntentGate, IntentDecision
from shared.jev.chunk_scorer import ChunkScorer, ScoringResult

# Inicializar uma vez (reutilizar entre chamadas)
gate = IntentGate(enabled=True)
scorer = ChunkScorer(enabled=True, min_similarity=0.5)

# Usar no pipeline
decision = gate.classify(pergunta_do_usuario)

if decision.short_circuit:
    return decision.response   # resposta fixa, sem retrieval nem LLM

chunks = banco_vetorial.buscar(pergunta_do_usuario)
resultado = scorer.filter(chunks)

if not resultado.has_content:
    return "Não encontrei informações relevantes sobre isso."

resposta = llm.generate(system=SYSTEM_PROMPT, user=montar_contexto(resultado.accepted))
```

---

## Lendo os Logs

```
INFO  JEV intent=GREETING — short-circuit ativado
INFO  JEV intent=META — short-circuit ativado (pattern: como (você|voce) funciona)
INFO  JEV intent=ANSWERABLE — prossegue para retrieval
INFO  JEV chunk_scorer — aceitos: 3 / rejeitados: 1 (threshold=0.50)
INFO  JEV chunk_scorer: todos os chunks rejeitados
```

---

## Diferença em relação ao Prompt Caching

| | JEV | Prompt Caching |
|---|---|---|
| Onde atua | Antes/entre etapas do pipeline | Na chamada à API do LLM |
| O que decide | Se vale a pena chamar o LLM | Como chamar o LLM |
| Depende de | Input do usuário + chunks recuperados | System prompt estático |
| Sem LLM? | ✅ Totalmente determinístico | ❌ Ainda chama o LLM |

Use **JEV + Prompt Caching juntos** em pipelines de produção para máxima eficiência.

---

## Arquivos

| Arquivo | O que é |
|---------|---------|
| `intent_gate.py` | Classificador de intenção por string matching e regex |
| `chunk_scorer.py` | Filtro de chunks por similaridade cosseno |
| `exemplos/uso_pipeline.py` | Pipeline completo integrando os dois componentes |
| `exemplos/uso_agente.py` | Padrão de uso dentro de um loop de agente (módulo 12) |
