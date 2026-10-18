# Template — Unit Test com pytest (Python)

> **[TEMPLATE] Como usar este arquivo**
>
> Copie para `tests/test_<nome_do_modulo>.py` no seu projeto.
> Substitua todos os blocos `[PREENCHA]` com o conteúdo real.
> Spec de referência: `[PREENCHA: caminho do spec em docs/specs/]`

---

```python
"""
Testes unitários para [PREENCHA: nome do módulo/função].
Spec de referência: docs/specs/[PREENCHA: nome-do-spec.md]
"""

import pytest
from unittest.mock import MagicMock, patch

# [PREENCHA: importe o módulo que será testado]
# from app.services.auth import AuthService


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def [PREENCHA_nome_do_objeto]():
    """
    [PREENCHA: descreva o que esta fixture prepara]
    """
    # Arrange — crie e retorne o objeto necessário para os testes
    return [PREENCHA]


# ─────────────────────────────────────────────
# CASO FELIZ
# ─────────────────────────────────────────────

class Test[PREENCHA_NomeDoComportamento]:
    """Testes para [PREENCHA: descreva o comportamento sendo testado]."""

    def test_[PREENCHA_caso_feliz](self, [PREENCHA_fixture]):
        """
        CA: [PREENCHA: cole o critério de aceite do spec]
        """
        # Arrange
        [PREENCHA]  # prepare os dados de entrada

        # Act
        resultado = [PREENCHA]  # execute a função/método sendo testado

        # Assert
        assert resultado == [PREENCHA]  # verifique o resultado esperado


# ─────────────────────────────────────────────
# CASOS DE ERRO
# ─────────────────────────────────────────────

    def test_[PREENCHA_caso_de_erro](self, [PREENCHA_fixture]):
        """
        CA: [PREENCHA: cole o critério de aceite de falha do spec]
        """
        # Arrange
        [PREENCHA]  # prepare os dados que causam o erro

        # Act + Assert
        with pytest.raises([PREENCHA_TipoDeExcecao]):
            [PREENCHA]  # execute a ação que deve lançar a exceção


    def test_[PREENCHA_caso_de_erro_com_mensagem](self, [PREENCHA_fixture]):
        """
        Quando [PREENCHA: condição], deve retornar [PREENCHA: resultado].
        """
        # Arrange
        [PREENCHA]

        # Act
        resultado = [PREENCHA]

        # Assert
        assert resultado.status_code == [PREENCHA]
        assert resultado.detail == "[PREENCHA: mensagem esperada]"


# ─────────────────────────────────────────────
# CASOS DE BORDA
# ─────────────────────────────────────────────

    def test_[PREENCHA_caso_de_borda](self, [PREENCHA_fixture]):
        """
        Caso de borda: [PREENCHA: descreva o cenário de borda]
        """
        # Arrange
        [PREENCHA]

        # Act
        resultado = [PREENCHA]

        # Assert
        assert [PREENCHA]


# ─────────────────────────────────────────────
# TESTES COM MOCK
# ─────────────────────────────────────────────

class Test[PREENCHA_NomeDoComportamentoComMock]:
    """Testes com dependências mockadas."""

    def test_[PREENCHA_com_mock](self):
        """
        CA: [PREENCHA: critério de aceite]
        Dependência mockada: [PREENCHA: qual dependência e por quê]
        """
        # Arrange
        mock_[PREENCHA] = MagicMock()
        mock_[PREENCHA].return_value = [PREENCHA]

        # Act
        with patch("[PREENCHA: caminho.do.modulo.Dependencia]", mock_[PREENCHA]):
            resultado = [PREENCHA]

        # Assert
        assert resultado == [PREENCHA]
        mock_[PREENCHA].assert_called_once_with([PREENCHA])


# ─────────────────────────────────────────────
# PARAMETRIZE — múltiplos cenários
# ─────────────────────────────────────────────

@pytest.mark.parametrize("[PREENCHA_entrada],[PREENCHA_saida_esperada]", [
    ([PREENCHA_valor_1], [PREENCHA_resultado_1]),
    ([PREENCHA_valor_2], [PREENCHA_resultado_2]),
    ([PREENCHA_valor_3], [PREENCHA_resultado_3]),
])
def test_[PREENCHA_multiplos_cenarios]([PREENCHA_entrada], [PREENCHA_saida_esperada]):
    """
    CA: [PREENCHA: critério de aceite que cobre múltiplos cenários]
    """
    # Act
    resultado = [PREENCHA]([PREENCHA_entrada])

    # Assert
    assert resultado == [PREENCHA_saida_esperada]
```

---

## Checklist antes de passar para Green

- [ ] Cada CA do spec tem pelo menos um teste
- [ ] Casos de borda do spec têm testes próprios
- [ ] Todos os testes falham ao rodar (`pytest tests/test_<nome>.py`)
- [ ] Nenhum teste passa sem implementação (isso indicaria que o teste não está verificando nada)
- [ ] Fixtures isolam os dados de teste — nenhum teste depende de estado de outro
