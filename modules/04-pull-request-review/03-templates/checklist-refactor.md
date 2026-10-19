# Checklist de Self-Review — Refatoração

> Preencha antes de executar `/code-review` ou abrir o PR.
> Refatoração não muda comportamento externo — todos os testes existentes devem continuar passando sem modificação.

---

## Definição de escopo

- [ ] O objetivo da refatoração está claro: o que está melhorando e por quê?
- [ ] O escopo está limitado — sem adicionar features junto?
- [ ] Existe um spec ou ADR documentando a decisão de refatorar?

## Comportamento preservado

- [ ] Todos os testes existentes passam sem modificação?
- [ ] Nenhuma interface pública foi alterada (ou breaking changes estão documentados)?
- [ ] O comportamento externo (inputs/outputs das funções públicas) é idêntico?

## Qualidade da refatoração

- [ ] A mudança realmente melhora legibilidade, testabilidade ou manutenção?
- [ ] A abstração nova faz sentido no domínio (não é over-engineering)?
- [ ] Nomes novos (classes, funções, variáveis) são mais descritivos que os antigos?

## Testes

- [ ] `pytest` ou `npm test` está passando 100% sem alterar nenhum teste existente
- [ ] Se algum teste precisou ser atualizado, a razão está documentada
- [ ] Novos testes foram adicionados para cobrir caminhos que antes ficavam sem teste?

## Código

- [ ] Nenhuma lógica de negócio foi adicionada ou removida
- [ ] Nenhum `TODO`, `FIXME` ou log de debug deixado

## Descrição do PR

- [ ] Título segue o padrão `refactor: <o que foi reorganizado>`
- [ ] Descrição explica: o problema antes, a solução após, e por que agora
- [ ] Breaking changes de interface estão destacados (se houver)