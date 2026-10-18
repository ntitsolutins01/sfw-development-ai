"""
Exemplo 1 — Pipeline completo integrando Intent Gate + Chunk Scorer.

Mostra o fluxo de decisão JEV end-to-end com três tipos de entrada:
  1. Saudação    → short-circuit no Intent Gate
  2. Pergunta meta → short-circuit no Intent Gate
  3. Pergunta real → passa pelo pipeline, chunks filtrados, chega ao LLM

Este exemplo usa chunks simulados (sem banco vetorial real) para que
você possa rodar e observar o comportamento sem infraestrutura.

Como rodar (da raiz do projeto):
    python shared/jev/exemplos/uso_pipeline.py

O que observar nos logs:
    Caso 1 → "JEV intent=GREETING — short-circuit ativado"
    Caso 2 → "JEV intent=META — short-circuit ativado"
    Caso 3 → "JEV intent=ANSWERABLE" + "JEV chunk_scorer — aceitos: X / rejeitados: Y"
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.jev.chunk_scorer import ChunkScorer, ScoringResult
from shared.jev.intent_gate import IntentGate, IntentDecision

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-5s %(name)s — %(message)s",
)

# ─── Chunks simulados ─────────────────────────────────────────────────────────
# Em produção, esses chunks vêm do banco vetorial (ChromaDB, Pinecone, etc.)
# O campo "distance" é a distância cosseno retornada pela busca.
CHUNKS_SIMULADOS = [
    {
        "text": "O prazo de entrega padrão é de 5 dias úteis para capitais.",
        "source": "politica-entrega.pdf",
        "distance": 0.12,   # similaridade: 0.88 ✅ muito relevante
    },
    {
        "text": "O prazo pode ser estendido em até 10 dias em datas comemorativas.",
        "source": "politica-entrega.pdf",
        "distance": 0.35,   # similaridade: 0.65 ✅ relevante
    },
    {
        "text": "A política de trocas e devoluções segue o Código de Defesa do Consumidor.",
        "source": "politica-trocas.pdf",
        "distance": 0.62,   # similaridade: 0.38 ❌ pouco relevante para "prazo de entrega"
    },
    {
        "text": "Produtos eletrônicos têm garantia de 12 meses.",
        "source": "garantias.pdf",
        "distance": 0.78,   # similaridade: 0.22 ❌ irrelevante
    },
]

# ─── Simulação do LLM ─────────────────────────────────────────────────────────
def llm_simular(chunks_aceitos: list[dict], pergunta: str) -> str:
    """Simula a chamada ao LLM mostrando quais chunks foram usados."""
    contexto = "\n".join(
        f"[{c['source']}] {c['text']}" for c in chunks_aceitos
    )
    return (
        f"(LLM chamado com {len(chunks_aceitos)} chunk(s))\n"
        f"Contexto recebido:\n{contexto}\n"
        f"Resposta gerada para: '{pergunta}'"
    )


# ─── Pipeline com JEV ─────────────────────────────────────────────────────────
def processar_pergunta(pergunta: str) -> str:
    gate = IntentGate(enabled=True)
    scorer = ChunkScorer(enabled=True, min_similarity=0.5)

    print(f"\n{'='*60}")
    print(f"Pergunta: '{pergunta}'")
    print('='*60)

    # Ponto 1 — Intent Gate
    decision = gate.classify(pergunta)
    if decision.short_circuit:
        print(f"  → Short-circuit ({decision.intent}): sem retrieval, sem LLM")
        return decision.response

    # Retrieval simulado (em produção: banco vetorial)
    print(f"  → {decision.intent}: prosseguindo para retrieval...")
    chunks = CHUNKS_SIMULADOS

    # Ponto 2 — Chunk Scorer
    resultado = scorer.filter(chunks)
    if not resultado.has_content:
        print("  → Todos os chunks rejeitados: sem contexto relevante")
        return "Não encontrei informações relevantes sobre isso nos documentos indexados."

    print(f"  → {len(resultado.accepted)} chunks aceitos, {len(resultado.rejected)} rejeitados")

    # LLM — só recebe chunks relevantes
    return llm_simular(resultado.accepted, pergunta)


if __name__ == "__main__":
    casos = [
        "olá",                          # → GREETING (short-circuit)
        "o que você pode fazer?",       # → META (short-circuit)
        "qual é o prazo de entrega?",   # → ANSWERABLE → chunks filtrados → LLM
    ]

    for pergunta in casos:
        resposta = processar_pergunta(pergunta)
        print(f"\nResposta final:\n{resposta}")
