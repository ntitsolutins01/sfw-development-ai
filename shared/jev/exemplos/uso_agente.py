"""
Exemplo 2 — JEV dentro de um loop de agente (padrão do Módulo 12).

Cenário: agente de suporte que responde perguntas de múltiplos usuários
em sequência. O JEV garante que saudações e perguntas sem contexto
relevante não chegam ao LLM — fundamental em produção onde volume é alto.

Este exemplo combina JEV + Prompt Caching (ver shared/prompt-caching/):
  - Intent Gate filtra antes do retrieval
  - Chunk Scorer filtra antes do LLM
  - Prompt Caching reutiliza os vetores KV do system prompt estático

Como rodar (da raiz do projeto):
    export ANTHROPIC_API_KEY="sk-ant-..."
    python shared/jev/exemplos/uso_agente.py

Sem ANTHROPIC_API_KEY configurado, o exemplo roda em modo simulado
e mostra apenas as decisões do JEV sem chamar a API real.
"""
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.jev.chunk_scorer import ChunkScorer
from shared.jev.intent_gate import IntentGate

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-5s %(name)s — %(message)s",
)

logger = logging.getLogger(__name__)

# ─── Constantes do agente ─────────────────────────────────────────────────────

# System prompt ESTÁTICO — bom candidato para Prompt Caching
# (ver shared/prompt-caching/llm_client.py)
AGENT_SYSTEM_PROMPT = """
Você é um assistente de suporte especializado nos documentos desta base de conhecimento.
Responda apenas com base nos documentos fornecidos. Cite sempre a fonte.
Se não encontrar a informação, diga explicitamente que não sabe.
Responda em português brasileiro.
"""

# Base de conhecimento simulada
# Em produção: ChromaDB, Pinecone, Weaviate, etc.
BASE_DE_CONHECIMENTO = [
    {"text": "O horário de atendimento é de segunda a sexta, das 8h às 18h.", "source": "faq.pdf", "distance": 0.10},
    {"text": "Para cancelar um pedido, acesse Meus Pedidos > Cancelar.", "source": "faq.pdf", "distance": 0.15},
    {"text": "O prazo de reembolso é de até 7 dias úteis após aprovação.", "source": "politica.pdf", "distance": 0.20},
    {"text": "Produtos em promoção não aceitam cupons adicionais.", "source": "promocoes.pdf", "distance": 0.55},
    {"text": "A política de privacidade foi atualizada em janeiro de 2026.", "source": "privacidade.pdf", "distance": 0.80},
]


@dataclass
class RespostaAgente:
    pergunta: str
    resposta: str
    jev_intent: str
    short_circuited: bool
    chunks_aceitos: int = 0
    chunks_rejeitados: int = 0


def buscar_chunks(pergunta: str) -> list[dict]:
    """Simula busca vetorial. Em produção: substituir por chamada ao banco vetorial."""
    return BASE_DE_CONHECIMENTO


def chamar_llm(system: str, chunks: list[dict], pergunta: str) -> str:
    """Chama o LLM real ou simula se a API key não estiver configurada."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        contexto = "\n".join(f"[{c['source']}] {c['text']}" for c in chunks)
        return (
            f"(modo simulado — configure ANTHROPIC_API_KEY para chamada real)\n"
            f"Contexto usado ({len(chunks)} chunks):\n{contexto}"
        )

    # Com API key real: usa o LLMClient com prompt caching
    from shared.prompt_caching.llm_client import LLMClient
    client = LLMClient(model="claude-haiku-4-5-20251001", prompt_cache=True)
    contexto = "\n".join(f"[{c['source']}] {c['text']}" for c in chunks)
    return client.generate(
        system=system,
        user=f"Contexto:\n{contexto}\n\nPergunta: {pergunta}",
    )


def processar_com_agente(pergunta: str) -> RespostaAgente:
    """Processa uma pergunta pelo pipeline completo com JEV."""
    gate = IntentGate(enabled=True)
    scorer = ChunkScorer(enabled=True, min_similarity=0.5)

    # Ponto 1 — Intent Gate
    decision = gate.classify(pergunta)
    if decision.short_circuit:
        return RespostaAgente(
            pergunta=pergunta,
            resposta=decision.response,
            jev_intent=decision.intent,
            short_circuited=True,
        )

    # Retrieval
    chunks = buscar_chunks(pergunta)

    # Ponto 2 — Chunk Scorer
    resultado = scorer.filter(chunks)
    if not resultado.has_content:
        return RespostaAgente(
            pergunta=pergunta,
            resposta="Não encontrei informações relevantes nos documentos disponíveis.",
            jev_intent=decision.intent,
            short_circuited=True,
            chunks_aceitos=0,
            chunks_rejeitados=len(chunks),
        )

    # LLM — só recebe chunks relevantes
    resposta = chamar_llm(AGENT_SYSTEM_PROMPT, resultado.accepted, pergunta)

    return RespostaAgente(
        pergunta=pergunta,
        resposta=resposta,
        jev_intent=decision.intent,
        short_circuited=False,
        chunks_aceitos=len(resultado.accepted),
        chunks_rejeitados=len(resultado.rejected),
    )


# ─── Simulação de fila de perguntas ──────────────────────────────────────────

FILA_DE_PERGUNTAS = [
    "oi",                                        # GREETING — short-circuit
    "como você funciona?",                       # META — short-circuit
    "qual o horário de atendimento?",            # ANSWERABLE — LLM
    "como cancelo um pedido?",                   # ANSWERABLE — LLM
    "bom dia",                                   # GREETING — short-circuit
    "qual é o prazo de reembolso?",              # ANSWERABLE — LLM
]


if __name__ == "__main__":
    print("=" * 65)
    print("Agente de Suporte com JEV — processando fila de perguntas")
    print(f"Total: {len(FILA_DE_PERGUNTAS)} perguntas")
    print("=" * 65)

    resultados = [processar_com_agente(p) for p in FILA_DE_PERGUNTAS]

    # Relatório final
    print("\n" + "=" * 65)
    print("RELATÓRIO")
    print("=" * 65)

    short_circuits = sum(1 for r in resultados if r.short_circuited)
    chamadas_llm = sum(1 for r in resultados if not r.short_circuited)

    for r in resultados:
        status = f"[{r.jev_intent}]" + (" → short-circuit" if r.short_circuited else f" → LLM ({r.chunks_aceitos} chunks)")
        print(f"\n  Pergunta : {r.pergunta}")
        print(f"  JEV      : {status}")
        print(f"  Resposta : {r.resposta[:100]}{'...' if len(r.resposta) > 100 else ''}")

    print(f"\n{'─'*65}")
    print(f"  Short-circuits (sem LLM): {short_circuits}/{len(resultados)}")
    print(f"  Chamadas ao LLM         : {chamadas_llm}/{len(resultados)}")
    print(f"  Economia estimada       : {short_circuits/len(resultados)*100:.0f}% das chamadas evitadas")
    print("=" * 65)
