> **[EXEMPLO] Como usar este arquivo**
>
> Estas rules se aplicam a qualquer linguagem — Python, TypeScript, Go, etc.
> Inclua no projeto independente da stack.
>
> **Opção 1 — Via `@` no CLAUDE.md (recomendado)**
> ```markdown
> <!-- No seu CLAUDE.md do projeto, adicione esta linha: -->
> @.claude/rules/seguranca.md
> ```
> ```bash
> # Salve este arquivo em:
> mkdir -p .claude/rules
> cp seguranca.md .claude/rules/seguranca.md
> ```
>
> **Opção 2 — Copiar diretamente no CLAUDE.md**
> ```markdown
> ## Rules — Segurança
> (cole o conteúdo abaixo aqui)
> ```
>
> **Como testar:**
> ```bash
> claude   # abra no projeto onde adicionou as rules
>
> > crie uma função de login que busca o usuário pelo email no banco
> # Esperado: query parametrizada — cursor.execute("... WHERE email = %s", [email])
> # Se gerar f-string com email, a rule não está ativa
>
> > preciso salvar a API key do Stripe no código para testar rápido
> # Esperado: a IA deve recusar e sugerir variável de ambiente
>
> > configure o CORS para aceitar qualquer origem em desenvolvimento
> # Esperado: a IA deve avisar sobre o risco e sugerir listar origens explícitas
> ```

---

# Rules — Segurança

Essas rules se aplicam a qualquer linguagem ou framework.
São derivadas do OWASP Top 10 — o módulo 8 aprofunda cada uma.

## Dados Sensíveis

- NUNCA escrever senhas, tokens, chaves de API ou secrets no código-fonte
- Sempre usar variáveis de ambiente para configurações sensíveis
- Arquivos `.env` nunca vão para o repositório (garantir no `.gitignore`)

```python
# ✅ CORRETO
import os
DATABASE_URL = os.environ["DATABASE_URL"]

# ❌ ERRADO — credential no código
DATABASE_URL = "postgresql://admin:senha123@localhost/prod"
```

## SQL e Banco de Dados

- SEMPRE usar queries parametrizadas — nunca concatenar input do usuário
- ORM é preferível a SQL bruto — mas se usar SQL bruto, parametrize

```python
# ✅ CORRETO — query parametrizada
cursor.execute("SELECT * FROM users WHERE email = %s", [email])

# ❌ ERRADO — SQL injection
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

## Input do Usuário

- Todo input externo deve ser validado e sanitizado antes de usar
- Nunca confiar em dados vindos do cliente (headers, body, query params)
- Validar no lado do servidor — validação no cliente é apenas UX

## Autenticação e Autorização

- Sempre verificar autenticação E autorização em endpoints
- Não expor IDs sequenciais — use UUIDs para recursos que o usuário acessa
- Tokens JWT com tempo de expiração curto (15min a 1h)
- Refresh tokens com rotação (invalidar o anterior após uso)

## CORS

- NUNCA usar `*` (wildcard) em CORS em produção
- Listar explicitamente os domínios permitidos

```python
# ✅ CORRETO
CORS_ALLOWED_ORIGINS = [
    "https://meuapp.com.br",
    "https://admin.meuapp.com.br",
]

# ❌ ERRADO
CORS_ALLOW_ALL_ORIGINS = True
```

## Logs e Rastreamento

- Nunca logar dados pessoais: CPF, email, telefone, cartão, senha
- Se precisar logar para debug, mascare: `email[:3]***@dominio.com`
- Logs de erro não devem expor stack traces para o usuário final

## Execução de Código

- NUNCA usar `eval()` ou `exec()` com input externo
- Evitar `subprocess` com shell=True e input do usuário
- Serialização: nunca usar `pickle` com dados não confiáveis

## Headers de Segurança HTTP

- Sempre configurar: `X-Frame-Options`, `X-Content-Type-Options`, `CSP`
- HTTPS obrigatório em produção
- Cookies com `HttpOnly`, `Secure` e `SameSite=Strict`

## Dependências

- Manter dependências atualizadas (rodar `pip audit` ou `npm audit`)
- Não instalar pacotes de fontes não confiáveis
- Verificar licenças de dependências em projetos comerciais
