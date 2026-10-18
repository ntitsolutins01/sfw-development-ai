# criar-pr

## Objetivo
Gerar automaticamente título, descrição completa e checklist para um Pull Request
a partir dos commits e diff do branch atual.

## Quando usar
- Quando você terminou uma feature/fix e quer abrir um PR
- Quando quer uma descrição de PR bem estruturada sem escrever do zero

## O que ela faz

1. Executa `git log main...HEAD --oneline` para listar os commits
2. Executa `git diff main...HEAD --stat` para ver o resumo das mudanças
3. Lê os arquivos modificados para entender o contexto
4. Gera:
   - **Título** do PR (máx 70 chars, imperativo em inglês)
   - **Descrição** com: o que mudou, por que, como testar
   - **Checklist** de itens a verificar antes do merge
5. Exibe o resultado para revisão
6. Pergunta se deve criar o PR via `gh pr create`

## O que ela NÃO faz
- Não abre o PR sem confirmação explícita
- Não faz push do branch (você deve ter feito antes)
- Não preenche reviewers automaticamente

## Formato gerado

```markdown
## Resumo
- O que foi alterado em 2-3 bullets

## Motivação
Por que essa mudança foi necessária.

## Como testar
1. Passo 1
2. Passo 2
3. Verificar que X funciona

## Checklist
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Sem dados sensíveis no código
- [ ] Build passa localmente
```

## Argumentos aceitos
- `/criar-pr` — gera PR com base no branch atual vs main
- `/criar-pr --base develop` — compara com develop
- `/criar-pr --draft` — cria como draft (não pronto para review)

## Exemplo de uso

```
/criar-pr
```

Saída esperada:
```
Analisando 3 commits no branch feature/checkout-step...

Título gerado: "Add multi-step checkout flow with address validation"

Descrição:
## Resumo
- Implementado fluxo de checkout em 3 etapas
- Adicionada validação de CEP via API dos Correios
- Novo componente StepIndicator para progresso visual

...

Criar o PR agora? (sim/não)
```
