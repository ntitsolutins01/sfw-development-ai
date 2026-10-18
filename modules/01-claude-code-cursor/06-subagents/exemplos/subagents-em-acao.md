# Exemplos de Subagents em Ação

## Exemplo 1 — Review de Segurança em Paralelo

**Cenário:** Você acabou de implementar um endpoint de pagamento e quer:
- Revisar segurança do código novo
- Verificar se os testes existentes ainda passam
- Checar se há TODOs esquecidos no arquivo

**Sem subagents (sequencial, ~8 min):**
```
1. Revisar segurança... 3 min
2. Rodar testes... 4 min
3. Buscar TODOs... 1 min
= 8 minutos total
```

**Com subagents (paralelo, ~4 min):**
```
> vou fazer três coisas em paralelo para o arquivo pagamentos/service.py:
> - fork 1: revisar vulnerabilidades de segurança
> - fork 2: rodar os testes relacionados a pagamentos
> - fork 3: buscar TODOs e FIXMEs

[Os três rodam simultaneamente — resultado em ~4 min]
```

---

## Exemplo 2 — Pesquisa de Arquitetura

**Cenário:** Você precisa decidir entre três abordagens para autenticação.

```
> delegue pesquisas paralelas para três subagentes:
>
> Agente 1: pesquise as vantagens e desvantagens de JWT stateless
> Agente 2: pesquise session-based authentication com Redis
> Agente 3: pesquise OAuth2 com Authorization Code Flow
>
> Quero um comparativo das três abordagens ao final
```

**O que acontece:**
- Três fresh agents iniciam em paralelo
- Cada um pesquisa sua abordagem de forma independente
- O agente principal compila o comparativo quando todos terminam

---

## Exemplo 3 — Fork para Segunda Opinião

**Cenário:** Você está implementando algo e quer validar a abordagem sem
perder o contexto atual.

```
> estou implementando o cálculo de frete com tabela progressiva.
> abra um fork que herda esse contexto e verifique se a lógica em
> calcular_frete() em pedidos/services.py cobre os edge cases:
> - pedido com peso zero
> - CEP inválido
> - múltiplos itens com pesos diferentes
```

**O que acontece:**
- O fork herda todo o contexto: arquivos lidos, decisões tomadas, conversa
- Ele analisa especificamente os edge cases listados
- Você recebe o relatório sem interromper sua implementação

---

## Exemplo 4 — Geração de Testes em Paralelo com Implementação

**Cenário:** Você precisa implementar e testar ao mesmo tempo.

```
> vou implementar a função aplicar_desconto() em pedidos/services.py
> em paralelo, delegue para um fork a criação do arquivo de testes
> tests/test_desconto.py cobrindo:
> - desconto percentual válido (10%, 50%)
> - desconto maior que 100% (deve lançar ValueError)
> - desconto em pedido com valor zero
> - desconto com cupom expirado
```

**Resultado:** Quando você termina a implementação, os testes já estão prontos.
Se algum teste falhar, é sinal de que há um bug na implementação.

---

## Dica: Briefing de Subagent

Para fresh agents (que não herdam contexto), o briefing precisa ser completo:

**Briefing ruim:**
```
> revise o código de pagamentos
```
O agente não sabe: qual arquivo, o que revisar, como reportar.

**Briefing bom:**
```
> revise o arquivo src/pagamentos/service.py buscando:
> 1. vulnerabilidades de injeção SQL
> 2. dados sensíveis sendo logados
> 3. tokens/senhas hardcoded
> 
> Reporte cada achado com: arquivo, linha, severidade (crítico/alto/médio), descrição.
> O projeto é uma API Django — considere as convenções Django para contexto.
```
