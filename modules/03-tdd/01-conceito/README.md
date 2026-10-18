# 01 — Conceito: TDD com IA

## O que é TDD

Test-Driven Development é a prática de escrever o teste antes do código que ele vai verificar. O ciclo tem 3 fases:

1. **Red** — escreva um teste que falha (o código não existe ainda)
2. **Green** — escreva o mínimo de código para o teste passar
3. **Refactor** — melhore o código sem quebrar os testes

O ciclo se repete para cada novo comportamento.

---

## As 3 Regras do TDD

Extraídas do trabalho de Robert Martin (Uncle Bob):

| Regra | O que significa na prática |
|-------|--------------------------|
| 1 | Não escreva código de produção a menos que seja para fazer um teste falho passar |
| 2 | Não escreva mais teste do que o suficiente para falhar (erro de compilação conta como falha) |
| 3 | Não escreva mais código do que o suficiente para fazer o teste passar |

Essas regras mantêm o ciclo curto e o código mínimo. O refactor é a fase onde você melhora o que foi feito com segurança.

---

## A Pirâmide de Testes

```
          ▲
         /E2E\         ← lentos, frágeis, poucos
        /─────\           testam o sistema completo
       /  INTEG \      ← médios, testam componentes juntos
      /──────────\
     /    UNIT    \    ← rápidos, isolados, muitos
    /──────────────\      testam uma unidade por vez
```

| Tipo | Velocidade | Isolamento | Quando usar |
|------|-----------|------------|-------------|
| **Unit** | < 1ms | Total (mocks) | Lógica de negócio, funções puras, validações |
| **Integration** | 10–500ms | Parcial | Repositórios, serviços com banco, APIs internas |
| **E2E** | 1–30s | Nenhum | Fluxos críticos do usuário, smoke tests |

Referência: 70% unit, 20% integration, 10% e2e. Ajuste conforme o projeto.

---

## TDD vs Testar Depois

| Critério | TDD | Testar Depois |
|----------|-----|---------------|
| Quando os testes são escritos | Antes do código | Após o código funcionar |
| O que guia o design | Os testes | A implementação |
| Cobertura típica | Alta — testes guiam cada comportamento | Variável — depende de disciplina |
| Custo de refactor | Baixo — testes garantem que nada quebrou | Alto — medo de quebrar algo não testado |
| Código morto | Raro — só existe código que passou em testes | Comum — código escrito sem teste |
| Com IA | ✅ Testes = contrato verificável | ⚠️ IA pode gerar código plausível mas incorreto |

---

## Por que TDD funciona especialmente bem com IA

**Sem TDD:** você pede para a IA implementar uma feature. A verificação é subjetiva — você lê o código e decide se parece correto. A IA pode gerar algo que soa plausível mas não satisfaz os requisitos.

**Com TDD:** você fornece os testes. A verificação é automática — verde ou vermelho. A IA tem um alvo concreto. Não há espaço para interpretação: ou os testes passam ou não passam.

Combinado com specs do Módulo 2, o fluxo fecha:

```
Critério de aceite do spec → Caso de teste → IA implementa → Teste verde
```

Cada passo é verificável de forma objetiva. A IA não precisa adivinhar o que você quer — os testes dizem.

---

## Auto-teste: você entendeu o conceito?

- [ ] Você consegue explicar o ciclo red-green-refactor em uma frase por fase?
- [ ] Você sabe diferenciar unit test de integration test pelo critério de isolamento?
- [ ] Você consegue mapear um critério de aceite de um spec em dois casos de teste (caso feliz + erro)?
- [ ] Você sabe por que escrever testes e código ao mesmo tempo com IA é um anti-padrão?

---

## Anti-padrões de TDD com IA

| Anti-padrão | Problema | O que fazer |
|-------------|---------|-------------|
| Pedir para IA escrever testes e código juntos | IA tende a escrever testes que validam a implementação que ela própria criou | Separe: primeiro testes, depois código |
| Testes que verificam detalhes de implementação | Quebram ao refatorar, mesmo com comportamento correto | Teste comportamento externo, não como foi feito internamente |
| 100% de cobertura como meta absoluta | Leva a testes sem valor criados só para atingir a métrica | Cobertura é sinal, não objetivo |
| Testes sem asserções claras | Passam sempre — não verificam nada útil | Cada teste deve ter pelo menos um `assert` que pode falhar |
| Mockar demais em testes de integração | Remove o valor do teste de integração | Mock apenas dependências externas (APIs de terceiros, e-mail, pagamento) |
| Modificar testes para fazê-los passar | Invalida o ciclo TDD — você está testando a implementação, não o contrato | Modifique o código; nunca modifique os testes para aceitar comportamento errado |
