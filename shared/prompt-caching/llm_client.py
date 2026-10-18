"""
Cliente Anthropic com suporte a Prompt Caching (KV-cache).

Origem: baseado em rag-project/src/llm/llm_client.py
Usado por: módulos 12 (Hermes Agent), 13 (Observabilidade), 14 (LLM as Judge)

Pré-requisito:
    pip install anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."
"""
import logging
import os

import anthropic

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Cliente para a API da Anthropic com suporte opcional a prompt caching.

    O caching reduz latência e custo em cenários onde o system prompt é
    estático e reutilizado em múltiplas chamadas dentro de uma janela de 5 min.

    Args:
        model:        ID do modelo Anthropic. Ex: "claude-sonnet-4-6"
        max_tokens:   Limite de tokens na resposta gerada.
        prompt_cache: True  → ativa KV-caching no system prompt (ephemeral, TTL 5 min)
                      False → comportamento padrão sem cache
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        max_tokens: int = 1024,
        prompt_cache: bool = False,
    ) -> None:
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = model
        self.max_tokens = max_tokens
        self.prompt_cache = prompt_cache

    def generate(self, system: str, user: str) -> str:
        """
        Envia uma mensagem ao modelo e retorna o texto da resposta.

        O system prompt é enviado como bloco cacheável quando prompt_cache=True.
        O user message NUNCA é cacheado — ele muda a cada chamada.

        Args:
            system: Instrução estática que define o comportamento do modelo.
                    Deve ser a parte mais estável do prompt para maximizar HITs.
            user:   Conteúdo variável da chamada (pergunta, contexto, documento).

        Returns:
            Texto completo da resposta do modelo.
        """
        # Com cache: system como lista de blocos com cache_control.
        # Sem cache: string simples — comportamento padrão da API.
        system_payload = (
            [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
            if self.prompt_cache
            else system
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_payload,
            messages=[{"role": "user", "content": user}],
        )

        self._log_cache_status(response.usage)

        return "".join(b.text for b in response.content if b.type == "text")

    def _log_cache_status(self, usage: anthropic.types.Usage) -> None:
        """Registra o resultado do cache para cada chamada."""
        if not self.prompt_cache:
            return

        cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
        creation = getattr(usage, "cache_creation", None)
        cache_write = (
            getattr(creation, "ephemeral_5m_input_tokens", 0) or 0
            if creation
            else 0
        )

        if cache_read > 0:
            logger.info("Prompt cache HIT — %d tokens reutilizados", cache_read)
        elif cache_write > 0:
            logger.info(
                "Prompt cache WRITE — %d tokens gravados no cache (TTL 5 min)",
                cache_write,
            )
        else:
            logger.info(
                "Prompt cache: sem hit nem write "
                "(prompt abaixo do threshold ou TTL expirado)"
            )
