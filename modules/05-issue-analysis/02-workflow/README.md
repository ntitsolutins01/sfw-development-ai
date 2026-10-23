# Fluxo de Issue Analysis com IA

## Visão geral

```
Issue bruta
    │
    ├─ Prompt 1: Análise inicial
    │  ↳ tipo, ambiguidades, perguntas de clarificação
    │
    ├─ [responder ou assumir valores padrão]
    │
    ├─ Prompt 2: Decomposição
    │  ↳ tasks atômicas e independentes
    │
    ├─ Prompt 3: Extração de CAs
    │  ↳ critérios verificáveis para cada task
    │
    ├─ Prompt 4: Priorização (opcional)
    │  ↳ impacto vs esforço
    │
    ├─ Prompt 5: Estimativa (opcional)
    │  ↳ complexidade relativa
    │
    └─ Prompt 6: Geração de spec stub
       ↳ docs/specs/NNN-nome.md pronto para o Módulo 2
```

---

## Fase 1 — Análise inicial

**Entrada:** issue bruta (texto, markdown ou link do GitHub)

**O que fazer:**
1. Use o **Prompt 1** com o texto completo da issue
2. A IA retorna: tipo (bug/feature/task), ambiguidades identificadas, perguntas de clarificação
3. Responda as perguntas ou documente os valores assumidos

**Critério de saída:** tipo definido, ambiguidades resolvidas ou documentadas.

---

## Fase 2 — Decomposição

**Entrada:** issue clarificada

**O que fazer:**
1. Use o **Prompt 2** com a issue clarificada
2. A IA decompõe em tasks atômicas

**O que é uma task atômica:**
- Implementável por uma pessoa em isolamento
- Testável independentemente
- Pode ser revisada em um PR separado (se necessário)
- Tem escopo claro de início e fim

**Sinal de que a decomposição está errada:** uma task depende de outra para ser testada.

---

## Fase 3 — Extração de CAs

**Entrada:** lista de tasks da fase 2

**O que fazer:**
1. Use o **Prompt 3** para cada task
2. Para cada CA, garanta o formato: `dado [contexto], quando [ação], então [resultado esperado]`

**Critérios de um bom CA:**
- Verificável: sim ou não, sem interpretação
- Específico: inclui valores concretos (status code, mensagem, comportamento)
- Independente: não depende de outro CA para ser verificado

**Exemplo de CA ruim:** `"O login deve funcionar corretamente"`
**Exemplo de CA bom:** `"dado credenciais válidas, quando POST /auth/login, então retorna 200 com token JWT no corpo"`

---

## Fase 4 — Geração do spec stub

**Entrada:** tasks + CAs das fases anteriores

**O que fazer:**
1. Use o **Prompt 6** para gerar o stub do spec
2. Salve em `docs/specs/NNN-nome-da-feature.md`
3. Abra o Módulo 2 e complete o spec com o fluxo SDD

**O stub gerado contém:**
- Título e contexto
- CAs já extraídos e formatados
- Campos "em aberto" para preencher no Módulo 2 (NFRs, dependências, out of scope)

---

## Integração com o restante do ciclo

```
Issue Analysis (M5)
    └─→ spec stub em docs/specs/
            └─→ Módulo 2 (completa o spec)
                    └─→ Módulo 3 (escreve os testes)
                            └─→ Módulo 4 (revisa o PR)
```

O valor da análise está em **não perder informação entre as fases**. Os CAs extraídos no Módulo 5 são os mesmos que vão para o spec (M2), os testes (M3) e a revisão (M4). A rastreabilidade é total.

---

## Quando NÃO analisar com IA

- Issue de 2 linhas com escopo absolutamente claro: vá direto para o spec
- Hotfix crítico em produção: corrija primeiro, documente depois
- Issues de infraestrutura pontual (ex: "trocar certificado SSL"): não precisa de decomposição

O fluxo completo é para issues de médio/alto escopo onde a ambiguidade gera retrabalho.

---

## Integração com GitHub

Se o projeto usa GitHub Issues, você pode passar a URL para `/analyze-issue`:

```
/analyze-issue https://github.com/org/repo/issues/123
```

A skill usa o `gh` CLI para buscar o conteúdo da issue automaticamente.