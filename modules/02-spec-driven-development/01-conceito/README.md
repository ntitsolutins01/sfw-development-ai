# 01 — O que é Spec Driven Development

## Definição

Um **spec** (especificação) é um documento estruturado que descreve o comportamento esperado de uma mudança de software **antes** de qualquer linha de código ser escrita.

Não é um documento de arquitetura. Não é um ticket de Jira. É a resposta às perguntas que a IA (e qualquer desenvolvedor) faria antes de implementar:

- O que exatamente essa mudança faz?
- Quais são os critérios de aceite?
- Quais casos de borda existem?
- O que **não** faz parte do escopo?
- Quais sistemas são afetados?

---

## Spec vs. Ticket vs. User Story

| | Spec | Ticket / Issue | User Story |
|---|------|----------------|------------|
| **Foco** | Comportamento técnico | Trabalho a ser feito | Necessidade do usuário |
| **Autor** | Desenvolvedor | PM / Dev | PM / Designer |
| **Nível** | Técnico | Gerencial | Negócio |
| **Critérios de aceite** | Explícitos e testáveis | Às vezes ausentes | Geralmente vagos |
| **Quando escrever** | Antes de codar | Antes de planejar | Antes de detalhar |

Um ticket diz *o quê* precisa ser feito. Um spec diz *como* será feito e *como* saberemos que está certo.

---

## O que um Bom Spec Contém

Todo spec bem escrito responde 6 perguntas:

```
1. CONTEXTO        Por que essa mudança existe?
2. ESCOPO          O que está dentro e fora dessa mudança?
3. COMPORTAMENTO   Como o sistema se comporta depois da mudança?
4. ACEITE          Como verificamos que está correto?
5. IMPACTO         Quais arquivos, serviços ou contratos são afetados?
6. RESTRIÇÕES      Quais limitações técnicas ou de negócio existem?
```

---

## Por que SDD funciona com IA

Quando você fornece um spec para o Claude Code implementar, você elimina a classe inteira de erros que vêm de suposições implícitas:

```
❌ SEM SPEC
"Crie um endpoint de login"
→ IA decide: JWT ou session? Expiração de 1h ou 24h?
  Hash bcrypt ou argon2? Campo "username" ou "email"?
  Retorna 401 ou 403 em credencial inválida?

✅ COM SPEC
"Implemente o endpoint POST /auth/login conforme o spec abaixo:
- Aceita: { email: string, password: string }
- Retorna 200 + { token: JWT, expires_in: 3600 } em sucesso
- Retorna 401 + { error: 'invalid_credentials' } em falha
- Usa bcrypt para verificação, JWT com expiração de 1h
- Não expõe se o email existe ou não (mesmo erro para ambos)"
→ IA implementa dentro dos limites que você definiu
```

---

## Anti-padrões de Spec

Evite esses erros ao escrever specs:

| Anti-padrão | Exemplo ruim | Exemplo melhor |
|-------------|-------------|----------------|
| **Critério vago** | "deve ser rápido" | "resposta < 200ms em p95 com 100 req/s" |
| **Escopo aberto** | "e outras melhorias relacionadas" | (liste ou remova) |
| **Sem caso de erro** | só o caminho feliz | inclua pelo menos 2 casos de falha |
| **Sem contexto** | implementa do zero sem explicar o sistema | descreva o estado atual antes da mudança |
| **Spec como código** | lista de linhas a modificar | descreva comportamento, não implementação |

---

## Como Testar seu Entendimento

Após ler um spec que você escreveu, responda:

1. Outro desenvolvedor conseguiria implementar isso sem te perguntar nada?
2. Há pelo menos 1 critério de aceite verificável por teste automatizado?
3. Você consegue listar o que **não** está no escopo?

Se alguma resposta for "não", o spec ainda está incompleto.
