---
name: brainstorm
description: Modo de maturação de ideias — pesquisa, analisa criticamente, aponta trade-offs e sugere melhorias sem criar ou executar nada. Use antes de qualquer spec ou implementação quando a ideia ainda não está suficientemente especificada.
disable-model-invocation: false
---

# brainstorm

## Objetivo
Maturar uma ideia antes de qualquer spec ou implementação. Pesquisa, analisa criticamente, aponta trade-offs e sugere alternativas **sem criar arquivos ou executar código** até o usuário pedir explicitamente.

## Quando usar
- A ideia existe mas ainda não está clara o suficiente para escrever um spec
- Você quer explorar alternativas antes de se comprometer com uma abordagem
- Há suposições implícitas que precisam ser questionadas antes de implementar
- Você quer entender trade-offs entre tecnologias ou padrões

## Quando NÃO usar
- Bug com causa já identificada (vá direto para `03-templates/bugfix.md`)
- Feature simples e bem entendida (vá direto para o spec técnico)
- Você só quer documentar algo que já foi decidido (use `/escrever-trd` modo Decisão)

## O que ela faz

1. Recebe o tema a explorar (feature, sistema, arquitetura, workflow)
2. Pesquisa o conceito: abordagens conhecidas, padrões da indústria
3. Questiona suposições implícitas no pedido
4. Aponta trade-offs de cada alternativa
5. Identifica gaps — o que ainda precisa ser decidido antes de implementar
6. Marca claramente o que é fato vs. o que é inferência (`[INFERIDO]`)
7. Ao concluir, orienta o próximo passo no fluxo SDD

## O que ela NÃO faz
- Não cria arquivos nem executa código durante a análise
- Não valida o que você já pensa — questionar é o valor
- Não toma decisões por você — apresenta as opções e os trade-offs

## Dois modos de operação

| Modo | Quando ativa | Foco |
|------|-------------|------|
| **Generalista** | ideia abstrata, produto, processo | problema real, alternativas, premissas |
| **Spec Lens** | feature técnica, sistema, refactor | requisitos negócio vs. técnicos, stack, versões — a base para escrever o spec, não o spec em si |

## Persistência de sessão
Ao final, se quiser preservar a análise, peça para salvar:

```
docs/brainstorms/YYYY-MM-DD-<slug>.md
```

Ao referenciar um brainstorm existente, a sessão é retomada do ponto onde parou.

## Argumentos aceitos
- `/brainstorm` — inicia sessão, pergunta o que explorar
- `/brainstorm sobre <tema>` — já inicia com o tema definido

## Exemplo de uso

```
/brainstorm sobre autenticação — estamos pensando em JWT vs session-based
para um SaaS multi-tenant, precisamos avaliar os trade-offs
```

Saída esperada (resumida):
```
Analisando: JWT vs session-based para SaaS multi-tenant

TRADE-OFFS JWT:
✓ Stateless — sem consulta ao banco por requisição
✓ Funciona bem com múltiplos serviços
✗ Revogação imediata impossível sem denylist (anula o stateless)

TRADE-OFFS SESSION:
✓ Revogação imediata simples
✗ Requer Redis compartilhado para escalar horizontalmente

[INFERIDO] Você precisa de revogação imediata (ex: logout forçado de todos os dispositivos)?
[INFERIDO] Há plano de microsserviços no futuro próximo?

PRÓXIMO PASSO:
→ /escrever-prd  se a decisão tem impacto de produto
→ /escrever-trd  para registrar a decisão como ADR
```

---

## Instruções operacionais

Você entrou no **modo de maturação de ideias**.

Regra absoluta: **não crie arquivos, não execute código, não implemente nada** até o usuário pedir explicitamente.

Ao ser invocado sem tema, pergunte:
- O que está sendo explorado?
- Qual o contexto atual do projeto?

A partir da resposta:

1. Pesquise o conceito — abordagens conhecidas, padrões da indústria
2. Questione suposições — o que o usuário assume e pode não ser verdade
3. Aponte trade-offs — para cada abordagem, o que se ganha e o que se perde
4. Identifique gaps — o que precisa ser decidido antes de implementar
5. Sugira alternativas que o usuário pode não ter considerado
6. Marque inferências com `[INFERIDO]` — separe fatos de suposições

**Modo Spec Lens** (ativado quando o tema é feature, sistema ou refactor):
- Separe requisitos de negócio de requisitos técnicos
- Verifique stack e versões externamente antes de registrar como fato
- O output é a base para o spec — preserve decisões descartadas e itens pendentes

**Estrutura do arquivo de sessão** (quando solicitado salvar):

```markdown
# Brainstorm: [tema]
> Data: YYYY-MM-DD | Status: em-andamento | concluido

## Decisões tomadas
- [decisão] — [racional]

## Alternativas descartadas
- [alternativa] — [por que descartada]

## Premissas a validar
- [ ] [premissa]

## Itens pendentes
- [ ] [item]
```

**Ao concluir**, sempre oriente o próximo passo:

```
Próximos passos no fluxo SDD:
→ /escrever-prd   se a ideia tem impacto de produto (user stories, critérios de aceite)
→ /escrever-trd   se define stack, arquitetura ou padrões globais do projeto
→ spec template   se já está claro o suficiente para implementar
                  (modules/02-spec-driven-development/03-templates/)
```
