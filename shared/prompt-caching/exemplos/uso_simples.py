"""
Exemplo 1 — Uso simples: comparativo com e sem cache.

Demonstra a diferença de comportamento entre prompt_cache=False e True
em duas chamadas consecutivas com o mesmo system prompt.

Como rodar (da raiz do projeto):
    export ANTHROPIC_API_KEY="sk-ant-..."
    python shared/prompt-caching/exemplos/uso_simples.py

O que observar nos logs:
    Primeira chamada  → "Prompt cache WRITE" (vetores gravados)
    Segunda chamada   → "Prompt cache HIT"   (vetores reutilizados, mais rápido)
"""
import logging
import sys
import time
from pathlib import Path

# Garante que shared/ está no path quando rodado diretamente
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.prompt_caching.llm_client import LLMClient

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-5s %(name)s — %(message)s",
)

# System prompt estático — representa instruções fixas de um agente ou assistente.
# Deve ser > 1024 tokens para o cache ser ativado pela API.
SYSTEM_PROMPT = """
Você é um assistente especializado em análise de código Python.
Sua função é revisar trechos de código e identificar:

1. Bugs e erros lógicos
2. Violações de PEP 8
3. Problemas de performance
4. Riscos de segurança (injeção, dados sensíveis expostos)

Regras de resposta:
- Sempre liste os problemas em ordem de severidade (crítico → baixo)
- Para cada problema: descreva o que é, por que importa, e como corrigir
- Se o código estiver correto, diga explicitamente "Sem problemas encontrados"
- Responda sempre em português brasileiro
"""


def demonstrar_sem_cache() -> None:
    print("\n" + "=" * 60)
    print("SEM CACHE — cada chamada recalcula o system prompt")
    print("=" * 60)

    client = LLMClient(model="claude-haiku-4-5-20251001", prompt_cache=False)

    for i in range(1, 3):
        print(f"\n  Chamada {i}:")
        inicio = time.perf_counter()
        resposta = client.generate(
            system=SYSTEM_PROMPT,
            user=f"Revise este código: x = input('valor: '); print(eval(x))",
        )
        duracao = time.perf_counter() - inicio
        print(f"  Duração: {duracao:.2f}s")
        print(f"  Resposta: {resposta[:120]}...")


def demonstrar_com_cache() -> None:
    print("\n" + "=" * 60)
    print("COM CACHE — system prompt cacheado por 5 minutos")
    print("=" * 60)

    client = LLMClient(model="claude-haiku-4-5-20251001", prompt_cache=True)

    for i in range(1, 3):
        print(f"\n  Chamada {i}:")
        inicio = time.perf_counter()
        resposta = client.generate(
            system=SYSTEM_PROMPT,
            # O user message muda a cada chamada — isso é intencional
            user=f"Revise este código (chamada {i}): x = input('valor: '); print(eval(x))",
        )
        duracao = time.perf_counter() - inicio
        print(f"  Duração: {duracao:.2f}s")
        print(f"  Resposta: {resposta[:120]}...")
        # Pequena pausa para que a segunda chamada ainda esteja dentro do TTL de 5 min
        if i == 1:
            time.sleep(1)


if __name__ == "__main__":
    demonstrar_sem_cache()
    demonstrar_com_cache()

    print("\n" + "=" * 60)
    print("Observe nos logs acima:")
    print("  - SEM cache: nenhum log de HIT/WRITE (sem cache ativo)")
    print("  - COM cache: 1ª chamada → WRITE, 2ª chamada → HIT")
    print("=" * 60)
