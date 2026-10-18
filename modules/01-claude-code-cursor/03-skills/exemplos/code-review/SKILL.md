# code-review

## Objetivo
Revisar o código do branch atual (diff em relação ao main) buscando bugs,
problemas de segurança, performance e qualidade, reportando com severidade.

## Quando usar
- Antes de abrir um Pull Request
- Após implementar uma nova feature ou correção
- Quando quiser uma segunda opinião sobre o código

## O que ela faz

1. Executa `git diff main...HEAD` para obter as mudanças do branch
2. Analisa cada arquivo modificado buscando:
   - **Bugs**: lógica incorreta, condições de corrida, null pointer
   - **Segurança**: injeção SQL, XSS, dados sensíveis expostos, OWASP Top 10
   - **Performance**: N+1 queries, loops desnecessários, chamadas síncronas bloqueantes
   - **Qualidade**: funções muito longas, duplicação, nomes confusos
3. Classifica cada achado por severidade:
   - `CRÍTICO`: impede o merge, pode causar incidente
   - `ALTO`: deve ser corrigido antes do merge
   - `MÉDIO`: recomendado corrigir, mas não bloqueia
   - `BAIXO`: sugestão de melhoria
4. Reporta em formato estruturado com: arquivo, linha, severidade, descrição e sugestão de correção

## O que ela NÃO faz
- Não faz commit ou push automaticamente
- Não corrige os problemas encontrados (apenas reporta)
- Não analisa arquivos fora do diff (histórico do projeto)

## Formato do Relatório

```
## Revisão de Código — [nome do branch] — [data]

### Resumo
- X achados críticos, Y altos, Z médios, W baixos

### Achados

#### [CRÍTICO] SQL Injection em users.py:45
**Problema:** Query montada com concatenação de string recebe input do usuário.
**Sugestão:** Use parâmetros preparados: `cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])`

#### [ALTO] ...
```

## Argumentos aceitos
- `/code-review` — revisa diff em relação ao main
- `/code-review --branch develop` — revisa em relação ao develop
- `/code-review --only security` — filtra apenas achados de segurança

## Exemplo de uso

```
/code-review
```

Saída esperada:
```
Rodando git diff main...HEAD...
Encontrei 12 arquivos modificados, analisando...

## Revisão de Código — feature/pagamentos — 17/10/2026

### Resumo
- 0 críticos, 1 alto, 3 médios, 2 baixos

### Achados

#### [ALTO] Dado sensível em log — pagamentos/service.py:78
**Problema:** Número de cartão sendo logado no nível INFO.
**Sugestão:** Mascare o cartão antes de logar: `card_number[-4:]`
...
```
