# O que é Issue Analysis eficiente

## O problema com issues brutas

Issues brutas têm três problemas recorrentes:

1. **Escopo implícito** — "melhorar a performance" pode significar otimizar uma query ou reescrever a arquitetura inteira
2. **CAs ausentes** — sem critério de aceite, qualquer implementação pode ser considerada "correta"
3. **Ambiguidade de comportamento** — "o usuário não consegue fazer login" pode ser um bug de senha, de sessão expirada, de bloqueio de conta ou de infraestrutura

IA não inventa os requisitos — mas consegue identificar sistematicamente o que está faltando e fazer as perguntas certas antes de começar.

---

## Os 3 tipos de issue

### Bug
Algo que funcionava (ou deveria funcionar) está quebrado.

**Elementos obrigatórios:**
- Comportamento atual (o que acontece)
- Comportamento esperado (o que deveria acontecer)
- Passos para reproduzir
- Ambiente (versão, browser, SO)
- Frequência (sempre / às vezes / uma vez)

**Critério de analisabilidade:** você consegue reproduzir o bug seguindo os passos?

---

### Feature
Uma nova capacidade que o sistema não tem.

**Elementos obrigatórios:**
- Quem vai usar (papel / persona)
- O que querem fazer (ação)
- Por que precisam disso (valor)
- O que está fora do escopo (negativo)
- Restrições não funcionais (performance, segurança, compatibilidade)

**Critério de analisabilidade:** você consegue dizer "pronto" sem ambiguidade?

---

### Task técnica
Trabalho de engenharia sem impacto direto no comportamento externo.

**Elementos obrigatórios:**
- Estado atual do código (o que existe)
- Estado desejado (o que será diferente)
- Motivação (por que agora)
- Critério de não-regressão (como provar que nada quebrou)

**Critério de analisabilidade:** os testes existentes continuam passando sem modificação?

---

## O triângulo da analisabilidade

Uma issue é analisável quando tem os três vértices:

```
        Escopo
       /      \
      /        \
CAs ────────── Definição
               de Done
```

- **Escopo:** o que está dentro e o que está fora
- **CAs:** como verificar que está implementado corretamente
- **Definição de Done:** quando o trabalho pode ser considerado encerrado

Se um dos três estiver faltando, a análise começa completando o que falta.

---

## Anti-padrões de issue

### ❌ Issue sem comportamento esperado
`"O upload está lento"` — comparado com o quê? Em qual condição? Para qual tamanho de arquivo?

### ❌ Issue sem escopo de negativo
`"Melhorar o sistema de autenticação"` — inclui MFA? Recuperação de senha? SSO? Sem negativo explícito, o escopo é infinito.

### ❌ Issue com múltiplos problemas
`"Fix login bug and add remember me"` — bug e feature na mesma issue não permitem deploy independente, dificultam a revisão e impossibilitam rastreabilidade.

### ❌ Issue orientada a solução, não ao problema
`"Adicionar índice na coluna email da tabela users"` — por que? Qual problema isso resolve? Qual é o comportamento esperado antes e depois?

### ❌ CA impossível de verificar
`"O sistema deve ser rápido"` — rápido como? Medir em quê? Com qual volume de dados?

---

## Por que IA ajuda na análise

- **Padrão recognition:** identifica qual tipo de informação está faltando comparando com o padrão do tipo de issue
- **Geração de perguntas:** formula as perguntas de clarificação certas antes de começar
- **Decomposição consistente:** divide issues complexas em tasks atômicas seguindo critérios objetivos
- **Extração de CAs:** transforma descrição narrativa em critérios verificáveis no formato `dado X, quando Y, então Z`

---

## Auto-teste

Responda antes de prosseguir:

1. Qual é a diferença entre um bug e uma task técnica?
2. Por que "o sistema deve ser rápido" não é um critério de aceite válido?
3. Uma issue com 3 bugs diferentes deveria ser uma ou três issues? Por quê?