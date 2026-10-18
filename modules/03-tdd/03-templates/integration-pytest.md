# Template — Integration Test com pytest (Python)

> **[TEMPLATE] Como usar este arquivo**
>
> Copie para `tests/integration/test_<nome>.py` no seu projeto.
> Testes de integração precisam de banco de dados ou serviço real (ou um container Docker).
> Spec de referência: `[PREENCHA: caminho do spec em docs/specs/]`
>
> **Diferença do unit test:** aqui você NÃO mocka o banco — você usa uma instância real
> (tipicamente SQLite em memória para testes, ou PostgreSQL via pytest-asyncpg).

---

```python
"""
Testes de integração para [PREENCHA: nome do módulo/repositório].
Spec de referência: docs/specs/[PREENCHA: nome-do-spec.md]

Dependências: pytest, pytest-asyncio, sqlalchemy (ou seu ORM)
Comando: pytest tests/integration/ -v
"""

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# [PREENCHA: importe o módulo sendo testado e os modelos do banco]
# from app.repositories.user_repository import UserRepository
# from app.models import Base, User


# ─────────────────────────────────────────────
# FIXTURES DE BANCO
# ─────────────────────────────────────────────

@pytest.fixture(scope="session")
def engine():
    """
    Banco SQLite em memória — criado uma vez por sessão de testes.
    Para PostgreSQL: use 'postgresql://user:pass@localhost:5432/test_db'
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    # [PREENCHA: substitua Base pelo Base do seu ORM]
    # Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """
    Sessão de banco isolada — cada teste começa com dados limpos.
    Usa rollback ao final para desfazer as mudanças do teste.
    """
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def [PREENCHA_repositorio](db_session):
    """
    [PREENCHA: descreva o repositório ou serviço com banco]
    """
    return [PREENCHA_Repositorio](db_session)


# ─────────────────────────────────────────────
# FACTORIES — dados de teste
# ─────────────────────────────────────────────

def criar_[PREENCHA_entidade](
    db_session,
    [PREENCHA_campo_1]="[PREENCHA_valor_default]",
    [PREENCHA_campo_2]="[PREENCHA_valor_default]",
    **kwargs
):
    """
    Factory para criar [PREENCHA: entidade] com valores padrão razoáveis.
    Passa kwargs para sobrescrever campos específicos por teste.
    """
    entidade = [PREENCHA_Modelo](
        [PREENCHA_campo_1]=[PREENCHA_campo_1],
        [PREENCHA_campo_2]=[PREENCHA_campo_2],
        **kwargs
    )
    db_session.add(entidade)
    db_session.flush()  # persiste sem commit — será desfeito no rollback
    return entidade


# ─────────────────────────────────────────────
# TESTES DE CRIAÇÃO
# ─────────────────────────────────────────────

class Test[PREENCHA_NomeDaOperacao]:
    """Testes para [PREENCHA: operação no banco]."""

    def test_[PREENCHA_criar_com_sucesso](self, [PREENCHA_repositorio], db_session):
        """
        CA: [PREENCHA: critério de aceite do spec]
        """
        # Arrange
        dados = {
            "[PREENCHA_campo]": "[PREENCHA_valor]",
        }

        # Act
        resultado = [PREENCHA_repositorio].[PREENCHA_metodo](dados)
        db_session.flush()

        # Assert
        assert resultado.id is not None
        assert resultado.[PREENCHA_campo] == "[PREENCHA_valor]"

        # Verificação no banco
        [PREENCHA_no_banco] = db_session.query([PREENCHA_Modelo]).get(resultado.id)
        assert [PREENCHA_no_banco] is not None


# ─────────────────────────────────────────────
# TESTES DE BUSCA
# ─────────────────────────────────────────────

    def test_[PREENCHA_buscar_existente](self, [PREENCHA_repositorio], db_session):
        """
        CA: [PREENCHA: critério de aceite]
        """
        # Arrange — usa factory para criar dado no banco
        [PREENCHA_entidade] = criar_[PREENCHA_entidade](
            db_session,
            [PREENCHA_campo]="[PREENCHA_valor]"
        )

        # Act
        resultado = [PREENCHA_repositorio].buscar_por_id([PREENCHA_entidade].id)

        # Assert
        assert resultado is not None
        assert resultado.[PREENCHA_campo] == "[PREENCHA_valor]"


    def test_[PREENCHA_buscar_inexistente_retorna_none](self, [PREENCHA_repositorio]):
        """
        Caso de borda: buscar ID que não existe deve retornar None (não lançar exceção).
        CA: [PREENCHA]
        """
        # Act
        resultado = [PREENCHA_repositorio].buscar_por_id(id=99999)

        # Assert
        assert resultado is None


# ─────────────────────────────────────────────
# TESTES DE CONSTRAINT / INTEGRIDADE
# ─────────────────────────────────────────────

    def test_[PREENCHA_viola_constraint](self, [PREENCHA_repositorio], db_session):
        """
        CA: [PREENCHA: critério que garante unicidade ou integridade]
        """
        # Arrange — cria o primeiro registro
        criar_[PREENCHA_entidade](db_session, [PREENCHA_campo]="[PREENCHA_valor_unico]")
        db_session.flush()

        # Act + Assert — tentar criar duplicata deve falhar
        with pytest.raises([PREENCHA_TipoDeExcecao]):
            [PREENCHA_repositorio].[PREENCHA_metodo]({"[PREENCHA_campo]": "[PREENCHA_valor_unico]"})
            db_session.flush()
```

---

## Checklist antes de passar para Green

- [ ] Banco de testes é diferente do banco de desenvolvimento (SQLite em memória ou variável de ambiente `TEST_DATABASE_URL`)
- [ ] Cada teste usa `rollback` via fixture — não deixa dados residuais
- [ ] Factories têm valores default razoáveis — cada teste sobrescreve só o que importa
- [ ] Testes de integração ficam em `tests/integration/`, separados dos unitários
- [ ] Rodar com `pytest tests/integration/ -v` antes de passar para Green
