# 04 — IA no Fluxo TDD

Prompts prontos para cada fase do ciclo TDD. Use em sequência: Red → Green → Refactor.

> Estes prompts complementam os do Módulo 2 (`04-ia-no-fluxo/`). Se você ainda não tem um spec,
> volte ao Módulo 2 e escreva o spec antes de gerar os testes.

---

## Prompt 1 — Gerar testes a partir dos critérios de aceite

Use na **fase Red**: transforma os CAs do spec em casos de teste antes de qualquer implementação.

```
Você vai gerar os testes para o spec abaixo. Ainda não existe implementação — o objetivo
é criar testes que **falham** e definem o contrato.

Regras:
- Use [pytest / jest — escolha um] e o padrão Arrange / Act / Assert com comentários
- Para cada critério de aceite, crie pelo menos dois testes: caso feliz + caso de falha
- Casos de borda do spec devem ter testes próprios
- Não implemente nada — apenas os testes
- Se precisar de fixtures, crie-as acima dos testes com nome descritivo
- Não mocke dependências do próprio sistema — só dependências externas (e-mail, pagamento, API de terceiros)

Ao final, liste quais CAs cobertos e quais ficaram sem teste por falta de informação.

--- SPEC ---
[cole o spec aqui]
```

---

## Prompt 2 — Implementar para os testes passarem (Red → Green)

Use na **fase Green**: fornece os testes e pede a implementação mínima.

```
Os testes abaixo estão falhando. Implemente o código mínimo para fazê-los passar.

Regras:
- Implemente APENAS o suficiente para os testes passarem — nada além
- Não modifique os testes — modifique apenas o código de produção
- Se encontrar ambiguidade nos testes, pare e pergunte antes de assumir
- Siga os padrões do projeto (nomes de arquivo, estrutura de pastas)

Antes de implementar, liste:
1. Quais arquivos você vai criar ou modificar
2. Dependências necessárias (bibliotecas, serviços)

--- TESTES ---
[cole o arquivo de testes aqui]
```

---

## Prompt 3 — Refatorar sem quebrar testes (Green → Refactor)

Use na **fase Refactor**: melhora o código mantendo todos os testes verdes.

```
O código abaixo faz todos os testes passarem. Refatore-o para melhorar [legibilidade /
performance / separação de responsabilidades — escolha o que se aplica].

Regras:
- Não modifique os testes
- Após o refactor, todos os testes devem continuar passando
- Não adicione funcionalidade nova — apenas melhore a estrutura existente
- Se identificar um smell de código que exige mudança de interface, aponte mas não faça — isso é uma nova iteração do ciclo

--- CÓDIGO ---
[cole o código a ser refatorado]

--- TESTES ---
[cole os testes que devem continuar passando]
```

---

## Prompt 4 — Gerar mocks e stubs para dependências externas

Use quando o código depende de serviço externo (API de pagamento, e-mail, etc.).

```
O código abaixo chama [PREENCHA: nome da dependência externa]. Crie um mock/stub
para usar nos testes unitários.

O mock deve:
- Reproduzir a interface exata da dependência (mesmos métodos e tipos de retorno)
- Ter versões configuráveis para sucesso e falha
- Não fazer chamadas de rede reais

Framework: [pytest com unittest.mock / jest com vi.fn() — escolha um]

--- CÓDIGO ---
[cole o código que usa a dependência]

--- INTERFACE DA DEPENDÊNCIA (se souber) ---
[cole a documentação ou tipo da dependência, ou descreva os métodos usados]
```

---

## Prompt 5 — Gerar fixtures e factories

Use quando os testes precisam de dados consistentes e reutilizáveis.

```
Gere fixtures / factories para os testes abaixo.

Requisitos:
- Cada fixture deve ter valores default razoáveis
- Parâmetros opcionais para sobrescrever campos específicos por teste
- Fixtures de banco devem garantir isolamento entre testes (rollback ou banco em memória)
- Factories de objeto não devem persistir no banco por padrão — receber a sessão como argumento

Framework: [pytest / jest — escolha um]

--- TESTES QUE PRECISAM DAS FIXTURES ---
[cole os testes que estão sem dados de teste]

--- MODELOS / TIPOS ---
[cole a definição das entidades ou tipos de dado]
```

---

## Prompt 6 — Identificar gaps de cobertura

Use depois de uma primeira rodada de testes para encontrar o que falta.

```
Analise os testes abaixo e compare com o spec original.

Identifique:
1. **CAs sem teste** — critérios de aceite do spec que não têm nenhum teste correspondente
2. **Casos de borda não cobertos** — cenários possíveis que os testes não exercitam
3. **Casos de erro não testados** — caminhos de falha que não têm asserção
4. **Testes frágeis** — testes que testam detalhes de implementação e podem quebrar em refactors

Para cada gap, sugira o caso de teste que deveria existir. Não implemente — só liste.

--- SPEC ---
[cole o spec]

--- TESTES EXISTENTES ---
[cole os testes atuais]
```

---

## Dica: CLAUDE.md para forçar TDD

```markdown
## Regra de TDD

Antes de implementar qualquer mudança de lógica:
1. Pergunte se existem testes para o comportamento em questão
2. Se não existirem, gere os testes primeiro — use o Prompt 1 de modules/03-tdd/04-ia-no-fluxo/
3. Confirme que os testes falham antes de implementar
4. Só então implemente usando o Prompt 2
5. Nunca modifique testes para fazê-los passar
```
