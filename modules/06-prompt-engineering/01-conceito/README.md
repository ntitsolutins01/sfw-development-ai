# Conceito — Prompt Engineering para Desenvolvedores

## O que é Engenharia de Prompts

Prompt engineering é o processo de estruturar entradas para um modelo de linguagem de forma que a saída seja previsível, relevante e utilizável sem iterações desnecessárias.

Para desenvolvedores, isso significa transformar a forma como você descreve problemas técnicos. O modelo não vê o seu código, o seu histórico de PRs ou o contexto da sprint — ele só vê o que você escreve. Quanto mais preciso o prompt, mais precisa a resposta.

## Por que importa

O mesmo problema gera respostas completamente diferentes dependendo de como é descrito:

**Prompt vago:**
```
implemente autenticação
```

**Prompt estruturado (framework CIFER):**
```
Contexto: API REST em Python/FastAPI. Tabela `users` com campos `id`, `email`,
`password_hash` (bcrypt). Spec completo em docs/specs/001-autenticacao-jwt.md.

Instrução: implemente a função `create_token(user_id: str) -> str`
no arquivo `app/services/auth.py`.

Formato: função pura com type hints, retorna o JWT como string.

Exemplos: token deve conter os campos `sub` (user_id), `exp` (+24h), `jti` (UUID4).

Restrições: use python-jose. Não adicione outros endpoints. Não trate erros além de
levantar ValueError se user_id for vazio.
```

O prompt vago produz um esqueleto genérico que vai precisar de 3–4 rodadas de correção. O estruturado produz código que funciona na primeira tentativa.

---

## Framework CIFER

Todo prompt eficaz para tarefas de desenvolvimento tem 5 componentes:

| Componente | O que é | Exemplo aplicado |
|-----------|---------|-----------------|
| **C**ontexto | Estado atual: framework, arquivo, função, tabela | "FastAPI, tabela `users` com `password_hash`" |
| **I**nstrução | O que fazer: um verbo + um objeto específico | "Implemente `create_token(user_id: str) -> str`" |
| **F**ormato | Como entregar: arquivo, função, teste, JSON, Markdown | "em `app/services/auth.py`, função pura" |
| **E**xemplos | Padrão a seguir: entrada/saída esperada, código existente | "token com campos `sub`, `exp`, `jti`" |
| **R**estrições | O que NÃO fazer | "não adicione endpoints além do solicitado" |

**Você não precisa dos 5 sempre.** Para tarefas simples, C + I basta. Para tarefas complexas (novos módulos, refatorações com risco), todos os 5 aumentam a precisão.

---

## As 6 Técnicas

### 1. Zero-shot

Instrução direta sem exemplos. Funciona para tarefas que o modelo já conhece bem.

```
# Zero-shot simples
Escreva um teste pytest para a função `create_token` que verifica
se o campo `exp` é igual a `iat + 86400`.
```

- **Use quando:** tarefas padrão (criar função, explicar erro, formatar código)
- **Evite quando:** saída com formato muito específico ou tarefas com muitas restrições

---

### 2. Few-shot

Fornece exemplos de entrada/saída antes da instrução. O modelo aprende o padrão pelos exemplos.

```
# Few-shot para gerar testes no estilo do projeto
Aqui estão dois testes existentes do projeto:

def test_login_com_credenciais_validas(client, usuario_valido):
    response = client.post("/auth/login", json=usuario_valido)
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_com_senha_incorreta(client, usuario_valido):
    payload = {**usuario_valido, "password": "errada"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401

Agora escreva um teste para o endpoint POST /auth/logout, verificando
que um token válido é invalidado na blocklist.
```

- **Use quando:** gerar código no estilo do projeto, criar testes, extrair dados em formato específico
- **Quantidade:** 2–3 exemplos são suficientes; mais que 5 polui o contexto

---

### 3. Chain-of-Thought (CoT)

Pede ao modelo para raciocinar passo a passo antes de responder. Aumenta a precisão em problemas complexos.

```
# CoT para debugging
O endpoint POST /auth/logout está retornando 200 mas o token não
está sendo adicionado à blocklist no Redis.

Antes de sugerir a correção, analise passo a passo:
1. Qual é o fluxo esperado de invalidação?
2. Em que ponto o token poderia deixar de ser persistido?
3. Como verificar se o Redis está sendo chamado?
Depois de concluir o raciocínio, mostre a correção.
```

- **Use quando:** debugging de erros difíceis, análise de performance, decisões arquiteturais
- **Como ativar:** "analise passo a passo antes de responder", "explique seu raciocínio antes da solução"

---

### 4. Role Prompting

Define um papel específico para o modelo antes da instrução. Muda o viés e o vocabulário da resposta.

```
# Role prompting para revisão de segurança
Aja como um engenheiro sênior especializado em segurança de APIs REST,
revisando o código de autenticação JWT abaixo.

Seu foco é: vetores de ataque na geração e validação do token,
exposição de informações sensíveis em erros, e timing attacks.

[código do auth_service.py]
```

- **Use quando:** revisões de código, análises de segurança, decisões de arquitetura, criação de documentação técnica
- **Seja específico:** "engenheiro sênior em segurança de APIs" é melhor que "especialista"

---

### 5. Structured Output

Especifica o formato exato da saída. Essencial quando a resposta vai ser processada ou comparada.

```
# Structured output para análise de issues
Analise a issue abaixo e retorne um JSON com este formato exato:

{
  "tipo": "bug | feature | task",
  "analisavel": true | false,
  "ambiguidades": ["item1", "item2"],
  "tasks": [
    {"id": "TASK-1", "titulo": "...", "dependencias": []}
  ]
}

Issue: [texto da issue]
```

- **Use quando:** integrar a saída em outro passo do fluxo, comparar múltiplas alternativas, gerar documentação
- **Dica:** cole um exemplo do JSON esperado para garantir o formato

---

### 6. Constrained Prompting

Lista explicitamente o que o modelo NÃO deve fazer. Evita over-engineering e mudanças não solicitadas.

```
# Constrained prompting para bug fix pontual
Corrija apenas o bug de timeout no upload descrito abaixo.

Não altere:
- a interface pública da função `upload_file`
- os outros endpoints do arquivo
- o esquema de banco de dados
- as importações existentes

Bug: arquivos > 1MB retornam 413 porque o nginx tem client_max_body_size = 1m.
Corrija apenas a configuração do nginx.
```

- **Use quando:** correções pontuais, refatorações com escopo limitado, qualquer tarefa onde você quer controle total sobre o que não muda
- **Regra:** se você sabe o que não quer que mude, liste explicitamente

---

## Anti-padrões

| Anti-padrão | Por que degrada a resposta | Correção |
|-------------|--------------------------|---------|
| **Prompt vago** — "implemente login" | Resposta genérica, sem contexto do projeto | Adicione C + I do CIFER |
| **Sem localização** — não informa arquivo/função | IA cria código em lugar errado ou cria novos arquivos | Informe caminho, função, classe alvo |
| **Tudo de uma vez** — "implemente toda a auth" | Resposta longa, incompleta, difícil de revisar | Divida em tarefas de uma função por vez |
| **Sem restrições** — não informa o que não mudar | IA adiciona código, abstrações e imports não solicitados | Use constrained prompting |
| **"Melhore este código"** — sem critério | Qualquer mudança é válida para o modelo | Defina o critério: performance? legibilidade? segurança? |
| **Contexto desatualizado** — código antigo no prompt | IA resolve problema que já foi corrigido | Sempre cole o estado atual, não o histórico |
| **Pergunta aberta** — "o que você acha?" | Resposta filosófica em vez de ação concreta | Formule como instrução com verbo: "liste", "compare", "corrija" |

---

## Auto-teste

Pegue o último prompt que você enviou para o Claude Code e responda:

- [ ] Qual componente CIFER está presente? Qual está ausente?
- [ ] Qual das 6 técnicas você usou (ou deveria ter usado)?
- [ ] Você listou o que NÃO devia ser alterado?
- [ ] A instrução tem um verbo + objeto específico?

Reescreva com os componentes faltantes e compare a resposta. A diferença costuma ser imediata.