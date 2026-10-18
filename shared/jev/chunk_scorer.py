"""
JEV — Chunk Scorer: filtra chunks por similaridade mínima após o retrieval.

Origem: baseado em rag-project/src/jev/chunk_scorer.py
Usado por: módulos 12 (Hermes Agent), 14 (LLM as Judge)

O banco vetorial com hnsw:space=cosine retorna distância cosseno por chunk:
  - 0.0 = idêntico à query
  - 1.0 = ortogonal (sem relação semântica)

Conversão: similaridade = 1 - distância_cosseno

Chunks abaixo do threshold (padrão: 0.5) são descartados antes de chegar ao LLM.
Isso reduz ruído, custo de tokens e alucinações por contexto irrelevante.

Pré-requisito:
    Nenhuma dependência externa — stdlib pura (dataclasses, logging).
    Cada chunk deve ter o campo "distance" com a distância cosseno retornada pelo banco.
"""
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ScoringResult:
    """Resultado da filtragem de chunks por similaridade.

    Attributes:
        accepted:  Chunks com similaridade >= threshold — serão enviados ao LLM.
        rejected:  Chunks com similaridade < threshold — descartados.
        threshold: Valor de corte usado nesta filtragem.
    """
    accepted: list[dict] = field(default_factory=list)
    rejected: list[dict] = field(default_factory=list)
    threshold: float = 0.5

    @property
    def has_content(self) -> bool:
        """True se ao menos um chunk foi aceito — pipeline pode seguir para o LLM."""
        return len(self.accepted) > 0


class ChunkScorer:
    """Filtra chunks recuperados pelo banco vetorial antes de enviá-los ao LLM.

    Exemplo de uso em pipeline:
        scorer = ChunkScorer(enabled=True, min_similarity=0.5)
        resultado = scorer.filter(chunks_do_banco)

        if not resultado.has_content:
            return "Não encontrei informações relevantes sobre isso."

        resposta = llm.generate(
            system=SYSTEM_PROMPT,
            user=montar_contexto(resultado.accepted),  # só chunks relevantes
        )

    Ajustando o threshold:
        0.3 → aceita mais chunks — mais contexto, mais ruído, mais tokens
        0.5 → equilíbrio padrão (ponto de partida recomendado)
        0.7 → aceita menos chunks — mais precisão, risco de perder conteúdo relevante
    """

    def __init__(self, enabled: bool = True, min_similarity: float = 0.5) -> None:
        """
        Args:
            enabled:        False desativa a filtragem — todos os chunks são aceitos.
                            Útil para testes ou para desabilitar via config.
            min_similarity: Limiar de similaridade cosseno [0.0–1.0].
                            Chunks abaixo deste valor são descartados.
        """
        self.enabled = enabled
        self.min_similarity = min_similarity

    def filter(self, chunks: list[dict]) -> ScoringResult:
        """Filtra uma lista de chunks pelo threshold de similaridade.

        Args:
            chunks: Lista de dicts retornados pelo banco vetorial.
                    Cada chunk deve ter o campo "distance" (distância cosseno).
                    Se "distance" estiver ausente, o chunk é tratado como irrelevante
                    (distance=1.0 → similarity=0.0).

        Returns:
            ScoringResult com accepted, rejected e threshold aplicado.
        """
        if not self.enabled:
            logger.info("JEV chunk_scorer desativado — todos os chunks aceitos")
            return ScoringResult(
                accepted=chunks,
                rejected=[],
                threshold=self.min_similarity,
            )

        result = ScoringResult(threshold=self.min_similarity)

        for chunk in chunks:
            # distance cosseno [0.0, 1.0] → similarity = 1 - distance
            distance = chunk.get("distance", 1.0)
            similarity = 1.0 - distance

            if similarity >= self.min_similarity:
                result.accepted.append(chunk)
            else:
                result.rejected.append(chunk)

        if not result.has_content:
            logger.info(
                "JEV chunk_scorer — todos os %d chunks rejeitados (threshold=%.2f)",
                len(chunks),
                self.min_similarity,
            )
        else:
            logger.info(
                "JEV chunk_scorer — aceitos: %d / rejeitados: %d (threshold=%.2f)",
                len(result.accepted),
                len(result.rejected),
                self.min_similarity,
            )

        return result
