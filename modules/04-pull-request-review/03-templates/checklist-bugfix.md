# Checklist de Self-Review — Bugfix

> Preencha antes de executar `/code-review` ou abrir o PR.

---

## Entendimento do Bug

- [ ] A causa raiz foi identificada (não apenas o sintoma)?
- [ ] Existe um spec ou issue descrevendo o comportamento esperado?
- [ ] O bug está reproduzível antes da correção (teste que falha)?

## Correção

- [ ] A correção ataca a causa raiz, não o sintoma?
- [ ] Outros lugares no código com o mesmo padrão problemático foram verificados?
- [ ] A correção não quebra nenhum comportamento existente?

## Testes

- [ ] Existe um teste de regressão que falha com o bug e passa com a correção?
- [ ] `pytest` ou `npm test` está passando 100% no branch
- [ ] O teste de regressão está no arquivo adequado (não em um arquivo temporário)

## Código

- [ ] A mudança é mínima — apenas o necessário para corrigir o bug
- [ ] Nenhuma refatoração desnecessária foi incluída no mesmo PR
- [ ] Nenhum `print` ou log de debug foi deixado

## Descrição do PR

- [ ] Título segue o padrão `fix: <descrição do bug corrigido>`
- [ ] Descrição menciona: o comportamento incorreto, a causa raiz e a correção
- [ ] Issue relacionada está linkada (se existir)
- [ ] Versões ou ambientes afetados estão documentados