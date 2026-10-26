# Templates de Prompt por Tipo de Tarefa

Use os templates abaixo como ponto de partida. Substitua os `[colchetes]` pelo contexto real do seu projeto.

---

## Quando usar cada template

| Tarefa | Template | Técnica base |
|--------|---------|--------------|
| Criar nova função ou endpoint | [`prompt-geracao-codigo.md`](prompt-geracao-codigo.md) | Zero-shot + CIFER |
| Corrigir bug ou comportamento inesperado | [`prompt-debug.md`](prompt-debug.md) | Chain-of-thought |
| Reorganizar código existente sem mudar comportamento | [`prompt-refatoracao.md`](prompt-refatoracao.md) | Constrained prompting |

---

## Convenção

Todos os templates seguem o formato CIFER com campos marcados:

```
## Contexto
[estado atual: linguagem, framework, arquivo, função existente]

## Instrução
[verbo + objeto específico]

## Formato
[onde entregar, como estruturar a saída]

## Exemplos
[padrão a seguir: código existente, entrada/saída esperada]

## Restrições
[o que não deve ser alterado ou adicionado]
```

Você não precisa preencher todos os campos para tarefas simples — mas quanto mais complexa a tarefa, mais campos importam.