"""
JEV — Intent Gate: classifica a intenção da pergunta antes do pipeline RAG.

Origem: baseado em rag-project/src/jev/intent_gate.py
Usado por: módulos 12 (Hermes Agent), 14 (LLM as Judge)

Decisões possíveis:
  GREETING   → saudação — resposta fixa, sem retrieval nem LLM.
  META       → pergunta sobre o próprio sistema — resposta fixa.
  ANSWERABLE → pergunta substantiva — prossegue pelo pipeline completo.

Pré-requisito:
    Nenhuma dependência externa — stdlib pura (re, dataclasses, logging).
"""
import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ─── Saudações reconhecidas ───────────────────────────────────────────────────
# Comparação exata após normalização (strip + lowercase + remoção de pontuação).
# Adicione novas saudações aqui conforme necessário.
_GREETINGS = {
    "oi", "olá", "ola", "hi", "hello", "hey",
    "bom dia", "boa tarde", "boa noite",
    "good morning", "good afternoon", "good evening",
    "tudo bem", "tudo bom",
}

# ─── Padrões de pergunta META (sobre o próprio sistema) ───────────────────────
# Regex compilados em IGNORECASE. Adicione novos padrões aqui.
_META_PATTERNS = [
    r"o que (você|voce) (pode|faz|sabe|é|e)",
    r"como (você|voce) funciona",
    r"quais? documentos",
    r"o que (está|esta|tem) indexado",
    r"me (ajuda|ajude|explica|explique)",
    r"what can you do",
    r"how do you work",
]

# ─── Respostas fixas ──────────────────────────────────────────────────────────
# Personalize para o domínio do seu agente.
_META_RESPONSE = (
    "Sou um assistente especializado nos documentos indexados nesta base. "
    "Faça uma pergunta sobre o conteúdo e responderei citando as fontes."
)

_GREETING_RESPONSE = (
    "Olá! Faça uma pergunta sobre os documentos indexados e farei o meu melhor "
    "para responder com base no conteúdo disponível."
)


@dataclass
class IntentDecision:
    """Resultado da classificação de intenção.

    Attributes:
        intent:        Categoria da pergunta: "GREETING" | "META" | "ANSWERABLE"
        short_circuit: True = não chamar retrieval nem LLM — resposta já está em `response`
        response:      Texto pronto para retornar ao usuário (só quando short_circuit=True)
    """
    intent: str
    short_circuit: bool
    response: str | None = None


class IntentGate:
    """Classifica a intenção da pergunta antes de qualquer embedding ou busca vetorial.

    Uso:
        gate = IntentGate(enabled=True)
        decision = gate.classify("qual é o prazo de entrega?")

        if decision.short_circuit:
            return decision.response  # resposta fixa, pipeline encerrado

        # caso contrário: prossegue para retrieval
    """

    def __init__(self, enabled: bool = True) -> None:
        """
        Args:
            enabled: False desativa completamente — tudo é classificado como ANSWERABLE.
                     Útil para testes ou para desabilitar via config sem alterar o código.
        """
        self.enabled = enabled
        self._meta_re = [re.compile(p, re.IGNORECASE) for p in _META_PATTERNS]

    def classify(self, question: str) -> IntentDecision:
        """Classifica a intenção da pergunta.

        Args:
            question: Texto da pergunta do usuário, qualquer tamanho.

        Returns:
            IntentDecision com intent, short_circuit e response (quando aplicável).
        """
        if not self.enabled:
            return IntentDecision(intent="ANSWERABLE", short_circuit=False)

        # Normaliza: remove espaços, converte para minúsculas, remove pontuação final
        normalized = question.strip().lower().rstrip("?!. ")

        if normalized in _GREETINGS:
            logger.info("JEV intent=GREETING — short-circuit ativado")
            return IntentDecision(
                intent="GREETING",
                short_circuit=True,
                response=_GREETING_RESPONSE,
            )

        for pattern in self._meta_re:
            if pattern.search(normalized):
                logger.info(
                    "JEV intent=META — short-circuit ativado (pattern: %s)",
                    pattern.pattern,
                )
                return IntentDecision(
                    intent="META",
                    short_circuit=True,
                    response=_META_RESPONSE,
                )

        logger.info("JEV intent=ANSWERABLE — prossegue para retrieval")
        return IntentDecision(intent="ANSWERABLE", short_circuit=False)
