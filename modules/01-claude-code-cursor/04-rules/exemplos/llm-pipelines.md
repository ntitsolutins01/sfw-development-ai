# Rules — Pipelines com Retrieval e LLM

Aplicam-se sempre que for gerado código que combina **busca vetorial + LLM**
(RAG, agentes com base de conhecimento, avaliadores em lote).

## Intent Gate — Classificação Antes do Pipeline

- SEMPRE usar `shared/jev/intent_gate.py` como primeira etapa de pipelines que recebem input livre do usuário
- Classificar a intenção ANTES de qualquer embedding ou busca vetorial
- Perguntas `GREETING` e `META` nunca devem chegar ao retrieval nem ao LLM

```python
# ✅ CORRETO — intent gate como primeira etapa
from shared.jev.intent_gate import IntentGate

gate = IntentGate(enabled=True)
decision = gate.classify(pergunta_do_usuario)

if decision.short_circuit:
    return decision.response      # resposta fixa — sem retrieval, sem LLM, sem custo

chunks = banco_vetorial.buscar(pergunta_do_usuario)  # só chega aqui se ANSWERABLE

# ❌ ERRADO — vai direto para retrieval sem classificar
chunks = banco_vetorial.buscar(pergunta_do_usuario)  # "olá" gasta embedding e busca
resposta = llm.generate(system=..., user=chunks)
```

## Chunk Scorer — Filtragem Antes do LLM

- SEMPRE usar `shared/jev/chunk_scorer.py` antes de passar chunks para o LLM
- Nunca enviar ao LLM chunks com similaridade < threshold sem filtragem explícita
- O campo `distance` da busca vetorial (ChromaDB, Pinecone, Weaviate) já contém esse valor — use-o

```python
# ✅ CORRETO — filtragem antes do LLM
from shared.jev.chunk_scorer import ChunkScorer

scorer = ChunkScorer(enabled=True, min_similarity=0.5)
resultado = scorer.filter(chunks_do_banco)

if not resultado.has_content:
    return "Não encontrei informações relevantes sobre isso."

resposta = llm.generate(
    system=SYSTEM_PROMPT,
    user=montar_contexto(resultado.accepted),  # só chunks relevantes
)

# ❌ ERRADO — envia todos os chunks sem filtrar
resposta = llm.generate(
    system=SYSTEM_PROMPT,
    user=montar_contexto(chunks_do_banco),  # inclui chunks com similarity 0.1
)
```

## Threshold do Chunk Scorer

- Valor padrão `0.5` é ponto de partida conservador — ajuste conforme o domínio
- Para bases com embeddings de alta qualidade (domínio específico): pode subir para `0.6`–`0.7`
- Para bases genéricas ou com vocabulário técnico incomum: manter em `0.4`–`0.5`
- NUNCA usar `0.0` como threshold em produção — equivale a desativar a filtragem

## Pipeline Completo Esperado

Todo pipeline RAG neste projeto deve seguir esta sequência:

```
input do usuário
    │
    ▼
[1] Intent Gate         ← shared/jev/intent_gate.py
    │ GREETING/META → resposta fixa (fim)
    │ ANSWERABLE ↓
    ▼
[2] Embedding + Retrieval
    │
    ▼
[3] Chunk Scorer        ← shared/jev/chunk_scorer.py
    │ sem conteúdo → resposta estruturada (fim)
    │ com conteúdo ↓
    ▼
[4] LLM                 ← shared/prompt_caching/llm_client.py (com caching)
    │
    ▼
resposta ao usuário
```

## Objetos Tipados — Não Usar Dicts Soltos

- `IntentDecision` e `ScoringResult` já são dataclasses tipadas — use-os como retorno
- Nunca retornar `{"intent": "GREETING"}` como dict solto quando `IntentDecision` está disponível
- Isso garante que o type checker detecta usos incorretos em tempo de desenvolvimento
