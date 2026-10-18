# Rules — Integração com APIs de LLM

Aplicam-se sempre que for gerado código que chama a API da Anthropic
ou qualquer outro provider de LLM (OpenAI, Gemini, etc.).

## Prompt Caching (Anthropic)

- SEMPRE usar `shared/prompt_caching/llm_client.py` como base ao integrar com a API Anthropic
- Ativar `prompt_cache=True` quando o system prompt for estático entre chamadas
- O system prompt vai no argumento `system` — o conteúdo variável vai no `user`
- NUNCA colocar dados da chamada atual (documentos, perguntas, contexto dinâmico) dentro do bloco cacheado

```python
# ✅ CORRETO — system estático cacheado, user variável fora do cache
from shared.prompt_caching.llm_client import LLMClient

client = LLMClient(model="claude-sonnet-4-6", prompt_cache=True)
resposta = client.generate(
    system="Você é um revisor de código. Identifique bugs e problemas de segurança.",
    user=f"Revise este código:\n{codigo_do_usuario}",   # variável: não cacheado
)

# ❌ ERRADO — conteúdo variável misturado no system prompt (cache nunca terá HIT)
resposta = client.generate(
    system=f"Você é um revisor. Analise: {codigo_do_usuario}",
    user="faça a revisão",
)
```

## Chaves de API

- NUNCA escrever `ANTHROPIC_API_KEY` ou qualquer chave de API no código
- Sempre ler de variável de ambiente: `os.environ["ANTHROPIC_API_KEY"]`
- O `LLMClient` já faz isso internamente — não passe a chave como argumento

## Modelo Padrão

- Usar `claude-sonnet-4-6` como padrão para tarefas de produção
- Usar `claude-haiku-4-5-20251001` para prototipagem e testes (mais barato e rápido)
- Nunca hardcodar o modelo no meio do código — passar como parâmetro ou ler de config

## Logging

- O `LLMClient` já loga HITs e WRITEs do cache — não duplicar esses logs
- Para depuração de custo, verificar os campos `usage.cache_read_input_tokens`
  e `usage.cache_creation.ephemeral_5m_input_tokens` na resposta da API

## Threshold mínimo

- O cache da Anthropic exige no mínimo **~1024 tokens** no system prompt para ativar
- System prompts curtos (< 1024 tokens) não terão HIT nem WRITE mesmo com `prompt_cache=True`
- Isso não é um erro — o log "sem hit nem write" é o comportamento esperado
