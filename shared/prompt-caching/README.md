# shared/prompt-caching — Referência de Prompt Caching

## O que é esta pasta

Implementação de referência do **KV-caching** (Prompt Caching da Anthropic).
Não é um módulo do curso — é uma biblioteca interna compartilhada.

Os módulos que fazem chamadas à API da Anthropic importam daqui:

| Módulo | Por que precisa |
|--------|----------------|
| 12 — Hermes Agent | O agente faz chamadas repetidas com o mesmo system prompt |
| 13 — Observabilidade | Monitora HITs e WRITEs do cache como métrica de custo |
| 14 — LLM as a Judge | Avaliações em lote: mesmo system prompt, user message diferente a cada avaliação |

---

## O que é Prompt Caching

Toda chamada à API da Anthropic recalcula internamente vetores de atenção
(**K** e **V** — *key* e *value*) para cada token do prompt. Sem cache,
esse cálculo acontece do zero mesmo quando o system prompt é idêntico.

O `cache_control: ephemeral` instrui a Anthropic a **guardar esses vetores
por 5 minutos**. Chamadas seguintes com o mesmo system prompt pulam o cálculo
e reutilizam os vetores armazenados.

```
Sem cache:
  Chamada 1 → calcula system prompt (512 tokens) + user message
  Chamada 2 → calcula system prompt (512 tokens) + user message   ← desperdício
  Chamada 3 → calcula system prompt (512 tokens) + user message   ← desperdício

Com cache:
  Chamada 1 → calcula system prompt → WRITE no cache (TTL 5 min)
  Chamada 2 → HIT: reutiliza vetores + calcula só o user message  ← mais rápido e barato
  Chamada 3 → HIT: reutiliza vetores + calcula só o user message  ← mais rápido e barato
```

**Resultado prático:**
- Latência menor a partir da segunda chamada
- Tokens lidos do cache são cobrados a ~10% do preço normal pela Anthropic

---

## Quando Vale a Pena Usar

| Situação | Usar cache? |
|----------|------------|
| System prompt > 1024 tokens e estático entre chamadas | ✅ Sim |
| Agente em loop com mesmo system prompt | ✅ Sim |
| Avaliações LLM em lote (mesmo critério, textos diferentes) | ✅ Sim |
| System prompt muda a cada chamada | ❌ Não — não haverá HIT |
| Chamada única e esporádica | ❌ Não vale o overhead |
| System prompt pequeno (< 1024 tokens) | ❌ API ignora o cache abaixo do threshold |

---

## Como Importar nos Módulos

```python
# Adicione shared/ ao PYTHONPATH antes de importar
# (ou rode a partir da raiz do projeto)

from shared.prompt_caching.llm_client import LLMClient

client = LLMClient(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    prompt_cache=True,          # ativa o KV-caching
)

resposta = client.generate(
    system="Você é um assistente especializado em...",  # texto estático → será cacheado
    user="Pergunta ou contexto variável do usuário",    # texto variável → nunca cacheado
)
```

---

## Lendo os Logs

```
INFO  Prompt cache HIT   — 512 tokens reutilizados
INFO  Prompt cache WRITE — 512 tokens gravados no cache (TTL 5 min)
INFO  Prompt cache: sem hit nem write (prompt abaixo do threshold ou TTL expirado)
```

| Log | O que significa |
|-----|----------------|
| `HIT` | Vetores reutilizados — chamada mais rápida e barata |
| `WRITE` | Primeira chamada ou TTL expirado — vetores calculados e gravados |
| `sem hit nem write` | Prompt abaixo de 1024 tokens, ou TTL expirou sem chamada intermediária |

---

## Arquivos

| Arquivo | O que é |
|---------|---------|
| `llm_client.py` | Implementação completa pronta para uso |
| `exemplos/uso_simples.py` | Chamada básica com e sem cache — comparativo direto |
| `exemplos/uso_agente.py` | Cache dentro de um loop de agente (padrão do módulo 12) |
