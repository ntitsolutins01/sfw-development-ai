# Workflow — Ciclo de Otimização de Prompts

## O Ciclo

```
        ┌─────────────────────────────────┐
        │                                 │
   Escrever ──► Testar ──► Medir ──► Refinar
        │                                 │
        └─────────────────────────────────┘
                    (iterar)
```

Prompts não saem prontos na primeira versão. O processo é iterativo: você escreve, testa com um problema real, mede a qualidade da resposta e refina o que não funcionou.

---

## Fase 1 — Escrever

Use o framework CIFER como checklist antes de enviar qualquer prompt:

```
[ ] C — dei o contexto necessário? (framework, arquivo, estado atual)
[ ] I — a instrução tem um verbo + objeto específico?
[ ] F — especifiquei o formato da saída?
[ ] E — forneci exemplos do padrão esperado?
[ ] R — listei o que NÃO deve ser feito?
```

Para tarefas simples, C + I basta. Para tarefas com risco de mudanças indesejadas, inclua R.

---

## Fase 2 — Testar

Teste o mesmo prompt com variações do problema para verificar se ele generaliza:

| Teste | O que verifica |
|-------|----------------|
| **Caso feliz** | A instrução principal funcionou? |
| **Caso de borda** | O prompt se comporta bem quando o contexto muda levemente? |
| **Sem contexto** | O que acontece se você remove o C do CIFER? |
| **Sem restrições** | O que acontece se você remove o R? |

O objetivo não é fazer um prompt perfeito para um caso — é fazer um prompt que funciona para uma classe de problemas.

---

## Fase 3 — Medir

Avalie a resposta em 4 dimensões:

| Dimensão | Pergunta | Pontuação |
|----------|---------|-----------|
| **Precisão** | A resposta resolve o problema sem mudanças adicionais? | 0–5 |
| **Escopo** | A resposta ficou dentro do que foi pedido (sem extras)? | 0–5 |
| **Formato** | A saída está no formato especificado? | 0–5 |
| **Iterações** | Quantas rodadas de correção foram necessárias? | 0 = ideal |

**Meta:** chegar em 4+ nas 3 primeiras dimensões com 0 iterações adicionais.

---

## Fase 4 — Refinar

Identifique qual componente do CIFER causou o problema e corrija:

| Problema observado | Componente deficiente | Correção |
|-------------------|----------------------|---------|
| Código em arquivo errado | **F** — formato | Adicione o caminho exato |
| Resposta genérica | **C** — contexto | Adicione framework, versão, estrutura |
| Código extra não solicitado | **R** — restrições | Liste o que não deve ser alterado |
| Formato de saída errado | **E** — exemplos | Mostre um exemplo do formato esperado |
| Instrução ambígua | **I** — instrução | Use verbo + objeto específico |

---

## Onde cada técnica se encaixa no ciclo AIAD

| Módulo AIAD | Tarefa típica | Técnica recomendada |
|-------------|--------------|---------------------|
| M2 — Spec | Gerar critérios de aceite a partir de uma descrição | **Few-shot** (mostre 2 CAs existentes) |
| M2 — Spec | Revisar spec e apontar gaps | **Role prompting** ("aja como QA sênior") |
| M3 — TDD | Gerar testes a partir dos CAs | **Few-shot** (mostre testes existentes do projeto) |
| M3 — TDD | Gerar implementação a partir dos testes | **Zero-shot** com CIFER completo |
| M3 — TDD | Debug: teste falhando sem causa óbvia | **Chain-of-thought** |
| M4 — PR Review | Revisão de qualidade geral | **Role prompting** + **Structured output** |
| M4 — PR Review | Verificar conformidade com spec | **Zero-shot** com CIFER completo |
| M5 — Issues | Analisar issue e extrair CAs | **Structured output** (JSON com campos definidos) |
| M5 — Issues | Decompor em tasks atômicas | **Chain-of-thought** |
| Qualquer | Corrigir bug pontual sem mudar outros arquivos | **Constrained prompting** |

---

## Salvando prompts que funcionam

Quando você escreve um prompt que funciona muito bem, salve-o como template. Dois formatos úteis:

**1. Template no CLAUDE.md do projeto**

```markdown
## Templates de prompt testados

### Gerar teste unitário
Contexto: [framework, arquivo de teste]
Instrução: escreva um teste para `[função]` que verifica [comportamento]
Formato: pytest, seguindo o padrão dos testes em `tests/`
Exemplos: [cole 1 teste existente]
Restrições: não use mocks para dependências que têm implementação real
```

**2. Template como arquivo em `03-templates/`**

Para prompts reutilizáveis entre projetos, salve no módulo 6 como referência permanente.

---

## Diagnóstico rápido

Se a resposta não foi boa, faça estas perguntas em ordem:

1. **A instrução foi específica?** Tinha verbo + objeto? → Se não: reescreva o I
2. **O contexto estava presente?** O modelo sabia o estado atual? → Se não: adicione C
3. **O formato foi especificado?** → Se não: adicione F
4. **O modelo adicionou coisas que não foram pedidas?** → Se sim: adicione R
5. **O problema é complexo e precisa de raciocínio?** → Se sim: use CoT