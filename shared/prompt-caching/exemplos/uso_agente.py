"""
Exemplo 2 — Cache dentro de um loop de agente.

Padrão relevante para o Módulo 12 (Hermes Agent):
um agente que processa múltiplos itens com o mesmo system prompt.

Cenário: agente de análise de segurança que avalia N arquivos de código.
O system prompt (critérios de análise) é fixo — só o código muda a cada iteração.

Como rodar (da raiz do projeto):
    export ANTHROPIC_API_KEY="sk-ant-..."
    python shared/prompt-caching/exemplos/uso_agente.py

O que observar:
    Iteração 1  → WRITE (cache gravado)
    Iteração 2+ → HIT   (cache reutilizado — mais rápido e mais barato)
"""
import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.prompt_caching.llm_client import LLMClient

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-5s %(name)s — %(message)s",
)

# ─── System prompt do agente ─────────────────────────────────────────────────
# Este bloco é ESTÁTICO: o mesmo para todos os arquivos analisados.
# Ideal para caching — será gravado no cache na primeira chamada
# e reutilizado nas seguintes dentro do TTL de 5 minutos.

AGENT_SYSTEM_PROMPT = """
Você é um agente de análise de segurança de código.

Sua tarefa é identificar vulnerabilidades no código enviado e produzir
um relatório estruturado com o seguinte formato exato:

ARQUIVO: <nome do arquivo>
SEVERIDADE_GERAL: CRÍTICA | ALTA | MÉDIA | BAIXA | OK
VULNERABILIDADES:
  - [SEVERIDADE] Descrição breve | Linha aproximada | Como corrigir

Regras:
- Analise apenas o código enviado — não invente contexto externo
- Se não houver vulnerabilidades, escreva: VULNERABILIDADES: nenhuma
- Responda sempre em português brasileiro
- Seja objetivo: máximo 3 linhas por vulnerabilidade
"""


@dataclass
class ArquivoCodigo:
    nome: str
    conteudo: str


@dataclass
class ResultadoAnalise:
    arquivo: str
    relatorio: str
    duracao_segundos: float


def analisar_arquivos(
    arquivos: list[ArquivoCodigo],
    prompt_cache: bool = True,
) -> list[ResultadoAnalise]:
    """
    Processa uma lista de arquivos com o agente de segurança.

    O system prompt é o mesmo para todos — com cache ativo, apenas
    a primeira chamada paga o custo de processamento do system prompt.
    """
    client = LLMClient(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        prompt_cache=prompt_cache,
    )

    resultados = []
    for arquivo in arquivos:
        print(f"\n  Analisando: {arquivo.nome}")
        inicio = time.perf_counter()

        relatorio = client.generate(
            system=AGENT_SYSTEM_PROMPT,   # estático → cacheado após 1ª chamada
            user=f"Analise o arquivo '{arquivo.nome}':\n\n{arquivo.conteudo}",
        )

        duracao = time.perf_counter() - inicio
        resultados.append(
            ResultadoAnalise(
                arquivo=arquivo.nome,
                relatorio=relatorio,
                duracao_segundos=duracao,
            )
        )
        print(f"  Concluído em {duracao:.2f}s")

    return resultados


# ─── Dados de exemplo ────────────────────────────────────────────────────────

ARQUIVOS_PARA_ANALISAR = [
    ArquivoCodigo(
        nome="auth/login.py",
        conteudo="""
def login(request):
    email = request.POST['email']
    senha = request.POST['senha']
    query = f"SELECT * FROM users WHERE email='{email}' AND senha='{senha}'"
    user = db.execute(query).fetchone()
    if user:
        session['user_id'] = user['id']
        return redirect('/dashboard')
    return render('login.html', {'erro': 'Credenciais inválidas'})
""",
    ),
    ArquivoCodigo(
        nome="config/settings.py",
        conteudo="""
SECRET_KEY = "minha-chave-super-secreta-123"
DATABASE_URL = "postgresql://admin:senha123@prod-db.empresa.com/producao"
DEBUG = True
ALLOWED_HOSTS = ['*']
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
""",
    ),
    ArquivoCodigo(
        nome="api/pedidos.py",
        conteudo="""
from flask import request, jsonify

def criar_pedido():
    dados = request.json
    produto_id = dados['produto_id']
    quantidade = dados['quantidade']
    # Sem validação de autenticação
    pedido = Pedido(produto_id=produto_id, quantidade=quantidade)
    db.session.add(pedido)
    db.session.commit()
    return jsonify({'id': pedido.id})
""",
    ),
]


if __name__ == "__main__":
    print("=" * 60)
    print("Agente de Segurança — Loop com Prompt Caching")
    print(f"Arquivos a analisar: {len(ARQUIVOS_PARA_ANALISAR)}")
    print("=" * 60)

    inicio_total = time.perf_counter()
    resultados = analisar_arquivos(ARQUIVOS_PARA_ANALISAR, prompt_cache=True)
    duracao_total = time.perf_counter() - inicio_total

    print("\n" + "=" * 60)
    print("RELATÓRIO FINAL")
    print("=" * 60)
    for r in resultados:
        print(f"\n{r.relatorio}")
        print(f"(analisado em {r.duracao_segundos:.2f}s)")

    print("\n" + "=" * 60)
    print(f"Total: {len(resultados)} arquivos em {duracao_total:.2f}s")
    print("Observe nos logs: 1ª iteração → WRITE, demais → HIT")
    print("=" * 60)
