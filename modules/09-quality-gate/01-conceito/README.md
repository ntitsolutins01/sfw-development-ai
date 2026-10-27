# Conceito — Quality Gates

## O que é um quality gate

Um quality gate é uma decisão binária automatizada: **passa** ou **bloqueia**. Se o código não atende ao critério configurado, o pipeline para — PR não é mergeado, build não avança, deploy não acontece.

Diferença entre gate e recomendação:
- **Recomendação:** "Cobertura está em 72%, considere adicionar testes" → o merge ocorre
- **Gate:** "Cobertura abaixo de 80% — build falhou" → o merge é bloqueado

Só a segunda versão garante que o critério seja atendido. Gates sem dentes não são gates.

## Os 3 Tipos de Gate

### 1. Análise Estática (código sem executar)

Examina o código sem rodá-lo. Detecta problemas estruturais que afetam manutenibilidade e segurança.

| Ferramenta | O que mede | Threshold típico |
|-----------|-----------|-----------------|
| `radon cc` | Complexidade ciclomática por função | Máximo C (≤ 10) |
| `flake8` / `ruff` | Estilo, imports não usados, variáveis indefinidas | Zero erros |
| `mypy` | Erros de tipagem estática | Zero erros em modo strict |
| `bandit` | Vulnerabilidades de segurança estática | Zero HIGH/MEDIUM |

Quando faz sentido: gate de PR, antes do merge. Rápido — executa em segundos.

### 2. Análise Dinâmica (código em execução)

Examina o comportamento do código durante a execução dos testes. Detecta lógica não testada.

| Ferramenta | O que mede | Threshold típico |
|-----------|-----------|-----------------|
| `pytest-cov` | Cobertura de linhas e branches | Mínimo 80% (linhas), 70% (branches) |
| `mutmut` | Cobertura de mutação (qualidade dos testes) | Mínimo 70% dos mutantes mortos |

Quando faz sentido: gate de PR. Mais lento que análise estática — executa os testes.

### 3. Performance (comportamento sob carga)

Examina o comportamento do sistema sob volume. Detecta regressões de latência e throughput.

| Ferramenta | O que mede | Threshold típico |
|-----------|-----------|-----------------|
| `locust` | Latência e taxa de erro sob carga | P95 < 500ms, error rate < 1% |
| `k6` | Throughput e latência por endpoint | SLA por endpoint definido |

Quando faz sentido: gate de staging, antes do deploy em produção. Mais lento — precisa de um serviço rodando.

## Onde os Gates se Encaixam

```
Commit → [Estático] → PR aberto → [Dinâmico + Segurança] → Staging → [Performance] → Produção
```

Integração com o workflow AIAD:
- **Estático** → complementa o `/code-review` do Módulo 1 e o `/review-pr` do Módulo 4
- **Dinâmico** → garante que o ciclo TDD do Módulo 3 não regrediu
- **Segurança** → o gate de segurança é o resultado do `/audit-owasp` do Módulo 8: zero CRÍTICO e ALTO

## Extensão: Quality Gates em Pipelines LLM

O mesmo princípio se aplica a pipelines com LLMs. Em vez de "o código atende ao threshold?", as perguntas são:
- "O input está dentro do escopo do sistema?" → se não, bloqueia antes da embedding
- "O contexto recuperado é relevante?" → se não, bloqueia antes do LLM
- "A resposta gerada tem qualidade suficiente?" → se não, bloqueia antes de retornar ao usuário

O `shared/jev/` implementa os dois primeiros gates:

| Gate JEV | Critério de passagem | O que bloqueia |
|----------|---------------------|----------------|
| Intent Gate | `intent == ANSWERABLE` | GREETING e META queries — short-circuit sem tocar o modelo |
| Chunk Scorer | `similarity >= threshold` | Chunks semanticamente distantes do input — removidos antes do LLM |

O terceiro gate — avaliação da resposta — é o tema do Módulo 14 (LLM as a Judge).

Isso é exatamente o mesmo princípio dos gates de CI/CD:
- Gate de cobertura: `coverage >= 80%` → senão, bloqueia o merge
- Gate de complexidade: `cyclomatic_complexity <= 10` → senão, falha o build
- Gate JEV (Intent): `intent == ANSWERABLE` → senão, retorna resposta fixa imediatamente
- Gate JEV (Chunk): `similarity >= 0.5` → senão, o chunk não vai para o prompt

## Anti-Padrões

| Anti-padrão | O que acontece | Como corrigir |
|-------------|---------------|---------------|
| Gates sem threshold real | `coverage >= 0%` — passa sempre | Defina um threshold que representa o mínimo aceitável |
| Thresholds impossíveis de atingir | `coverage >= 95%` em projeto legado → bloqueia tudo | Comece no coverage atual − 5%, suba gradualmente |
| Todos os gates no deploy de produção | Problemas detectados tarde, custo alto de corrigir | Move análise estática para commit, dinâmica para PR |
| Gates só em CI (nunca localmente) | Feedback loop longo — PR abre com falha | Makefile com os mesmos gates para rodar localmente |
| Gate de complexidade ignorado | Complexidade cresce silenciosamente | Gate deve bloquear PR, não só avisar |