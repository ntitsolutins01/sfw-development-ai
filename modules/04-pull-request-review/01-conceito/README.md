# O que é Pull Request Review eficiente

## O problema com revisões manuais

Revisão de PR manual sofre de três problemas:

1. **Inconsistência** — o que você verifica hoje depende do seu humor, do seu foco e de quanto tempo tem disponível
2. **Fadiga** — após 3–4 PRs seguidos, a atenção cai e problemas passam
3. **Escopo implícito** — revisores diferentes têm critérios diferentes; não existe um contrato explícito do que "revisão aprovada" significa

IA não resolve tudo, mas garante que o mesmo checklist seja percorrido toda vez.

---

## O que verificar em um PR

Um PR bem revisado cobre cinco dimensões:

### 1. Correção funcional
- A implementação cobre todos os critérios de aceite do spec?
- Os casos de borda descritos no spec estão tratados?
- A lógica de negócio está correta?

### 2. Cobertura de testes
- Todos os CAs têm ao menos um teste (caso feliz + caso de falha)?
- Os testes realmente testam comportamento, não implementação?
- Algum caminho do código fica sem cobertura?

### 3. Segurança
- Inputs do usuário são validados e sanitizados?
- Dados sensíveis estão sendo logados ou expostos?
- Autenticação e autorização estão corretas?
- Vulnerabilidades OWASP Top 10 estão mitigadas?

### 4. Performance
- Existem queries N+1?
- Operações custosas estão sendo feitas em loops desnecessários?
- Chamadas externas síncronas podem bloquear o sistema?

### 5. Qualidade e manutenção
- O código é legível sem precisar de comentários?
- Funções têm responsabilidade única?
- Não existe duplicação que deveria ser extraída?

---

## Categorias de severidade

Todo achado numa revisão deve ter severidade explícita. Use este modelo:

| Severidade | Significado | Ação |
|------------|-------------|------|
| `CRÍTICO` | Pode causar incidente em produção, perda de dados ou brecha de segurança | Bloqueia o merge — deve ser corrigido antes de qualquer aprovação |
| `ALTO` | Bug funcional, falha de segurança não-crítica, comportamento incorreto | Deve ser corrigido antes do merge |
| `MÉDIO` | Problema real mas sem impacto imediato em produção | Deve ser discutido; pode ser aceito com justificativa |
| `BAIXO` | Sugestão de melhoria, estilo, legibilidade | Opcional; autor decide |

> **Regra prática:** se você não consegue justificar a severidade em uma frase, rebaixe uma categoria.

---

## Anti-padrões de revisão

### ❌ Revisar apenas formatação
Comentar sobre indentação e nomes de variáveis mas não verificar se a lógica está correta.

### ❌ Aprovar sem ler o spec
Aprovar uma feature sem verificar se ela implementa o que foi especificado — o spec é o contrato.

### ❌ Comentários vagos
`"Isso pode ser melhorado"` — melhorado como? Sempre inclua: o problema, por que é um problema, e uma sugestão concreta.

### ❌ Bloquear por preferência pessoal
Marcar como ALTO ou CRÍTICO algo que é preferência de estilo pessoal. Use BAIXO e deixe o autor decidir.

### ❌ Revisar sem contexto
Revisar o diff sem ler o spec e sem rodar os testes localmente — você está revisando código sem saber o que ele deveria fazer.

---

## Por que IA ajuda na revisão

IA não substitui o revisor humano — ela executa o checklist sistemático que você deveria executar mas raramente consegue manter consistente:

- **Não fatiga:** o 10º PR recebe a mesma atenção que o 1º
- **Não tem viés de autoria:** não aprova porque foi você quem escreveu
- **Cobre todas as categorias:** segurança, performance, qualidade — toda vez
- **Compara com o spec:** verifica cada CA explicitamente, não por inferência

O revisor humano foca então no que a IA não consegue: julgamento de design, impacto no sistema mais amplo, alinhamento com a estratégia do produto.

---

## Auto-teste

Responda antes de prosseguir:

1. Qual é a diferença entre severidade CRÍTICO e ALTO?
2. Por que revisar o spec antes de revisar o código?
3. Cite dois anti-padrões de revisão e como evitá-los.