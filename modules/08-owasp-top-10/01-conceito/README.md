# Conceito — OWASP Top 10 com Assistência de IA

## O que é o OWASP Top 10

O OWASP Top 10 é uma lista de consenso publicada pela Open Web Application Security Project (OWASP) que documenta as 10 categorias de risco de segurança mais críticas em aplicações web. A versão atual é de 2021.

A lista não é exaustiva — é um ponto de partida. Cobrir as 10 categorias não garante uma aplicação segura, mas negligenciá-las é praticamente garantia de vulnerabilidade conhecida e explorável.

## As 10 Categorias (OWASP 2021)

| # | Categoria | Descrição resumida |
|---|-----------|-------------------|
| A01 | Broken Access Control | Usuários acessam recursos ou executam ações além das suas permissões |
| A02 | Cryptographic Failures | Dados sensíveis expostos por criptografia fraca, ausente ou mal configurada |
| A03 | Injection | Dados não confiáveis executados como código (SQL, NoSQL, OS, LDAP) |
| A04 | Insecure Design | Falhas arquiteturais que nenhum controle de implementação resolve |
| A05 | Security Misconfiguration | Configurações padrão inseguras, permissões excessivas, stack traces expostos |
| A06 | Vulnerable and Outdated Components | Dependências com vulnerabilidades conhecidas (CVEs publicados) |
| A07 | Identification and Authentication Failures | Brute force, sessões não expiradas, credenciais fracas ou expostas |
| A08 | Software and Data Integrity Failures | Atualizações, pipelines e serialização sem verificação de integridade |
| A09 | Security Logging and Monitoring Failures | Falhas não registradas, logs insuficientes, sem alertas de segurança |
| A10 | Server-Side Request Forgery (SSRF) | Servidor faz requisições para destinos controlados pelo atacante |

## Mapeamento para o Projeto JWT

O sistema de autenticação JWT usado no projeto de prova é diretamente afetado por 6 das 10 categorias:

| Categoria | Risco concreto no projeto JWT |
|-----------|-------------------------------|
| A01 | Endpoint protegido acessível sem token válido ou sem verificação de `user_id` |
| A02 | Segredo JWT fraco (`"secret"`, `"123456"`), algoritmo `none` não rejeitado |
| A03 | SQL injection nas queries de busca de usuário se usadas com f-strings |
| A05 | Debug mode ativo em produção, stack trace completo exposto no response |
| A07 | Sem rate limiting em `POST /auth/login`, tokens sem expiração configurada |
| A09 | Tentativas de login com credenciais inválidas não são logadas com IP |

## Por Que IA Muda o Jogo

Uma auditoria OWASP manual exige que o auditor:
1. Conheça as 10 categorias e seus sub-padrões de memória
2. Leia cada arquivo de código procurando padrões de risco categoria por categoria
3. Documente achados com severidade, evidência e recomendação
4. Mantenha contexto entre arquivos para identificar riscos compostos

O Claude Code faz isso em uma única invocação com o prompt correto. A vantagem não é só velocidade — é **consistência**: o modelo aplica o mesmo critério a cada arquivo, sem fadiga de revisão nem viés de "já vi isso antes, deve estar ok".

**O que a IA faz bem:**
- Identificar padrões de código que violam categorias OWASP (A01, A02, A03, A07)
- Sugerir correções específicas com código funcional e justificativa técnica
- Priorizar achados por severidade (CRÍTICO → ALTO → MÉDIO → BAIXO)
- Explicar o vetor de ataque de cada achado em linguagem acessível

**O que requer julgamento humano:**
- **A04** (Insecure Design) — exige visão arquitetural que vai além de arquivos individuais; a IA identifica sintomas, não a causa raiz de design
- **A06** (Outdated Components) — requer verificar CVEs em bases externas (`pip audit`, Snyk, Dependabot); a IA não tem acesso a CVEs em tempo real
- Falsos negativos em lógica de negócio complexa onde o risco depende de contexto de produto

## Anti-Padrão: OWASP Como Checklist Binário

O anti-padrão mais comum é usar OWASP como formulário a assinar: "percorremos os 10 itens, nenhum marcado como N/A, estamos seguros". Isso falha por três razões:

1. **Contexto importa**: A01 em um endpoint público com dados financeiros é CRÍTICO; o mesmo padrão em um sistema interno de uso exclusivo pode ser BAIXO
2. **Composição de riscos**: dois riscos MÉDIO combinados podem criar um vetor CRÍTICO (ex: log insuficiente + nenhum rate limit = brute force indetectável)
3. **Cobertura de código**: o checklist verifica se a categoria foi considerada, não se cada arquivo foi auditado

Use o OWASP como **framework de análise sistemática**, não como checklist de conformidade.