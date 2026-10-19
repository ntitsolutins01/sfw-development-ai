# Checklist de Self-Review — Feature Nova

> Preencha antes de executar `/code-review` ou abrir o PR.
> Marque `[x]` para concluído, `[N/A]` para não aplicável.

---

## Spec e Critérios de Aceite

- [ ] Existe um spec para esta feature em `docs/specs/`?
- [ ] Todos os critérios de aceite do spec estão implementados?
- [ ] Se algum CA foi alterado durante a implementação, o spec foi atualizado?

## Testes

- [ ] Cada CA tem ao menos um teste de caso feliz
- [ ] Cada CA tem ao menos um teste de caso de falha / borda
- [ ] `pytest` ou `npm test` está passando 100% no branch
- [ ] Nenhum teste foi desabilitado ou ignorado para fazer o build passar

## Segurança

- [ ] Inputs do usuário são validados antes de usar
- [ ] Nenhum dado sensível (senha, token, chave) está sendo logado
- [ ] Autenticação e autorização estão verificadas nos endpoints novos
- [ ] Nenhuma query SQL é montada por concatenação de string

## Código

- [ ] Nenhuma função tem mais de 30 linhas (se tiver, justifica a exceção)
- [ ] Nenhum bloco de código duplicado que poderia ser extraído
- [ ] Nomes de variáveis e funções descrevem o que fazem sem precisar de comentário
- [ ] Nenhum `TODO`, `FIXME` ou `print` de debug deixado no código

## Dependências e configuração

- [ ] Nenhuma dependência nova foi adicionada sem justificativa
- [ ] Variáveis de ambiente novas estão documentadas no `.env.example`
- [ ] Migrações de banco (se houver) estão reversíveis

## Descrição do PR

- [ ] Título segue o padrão `feat: <descrição em imperativo>`
- [ ] Descrição menciona o spec relacionado e o número dos CAs implementados
- [ ] Breaking changes estão destacados (se houver)