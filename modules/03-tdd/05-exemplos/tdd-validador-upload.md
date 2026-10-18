# Exemplo TDD — Validador de Arquivo para Upload (Python / pytest)

> **Conectado ao spec:** `modules/02-spec-driven-development/05-exemplos/spec-bugfix-timeout-upload.md`
>
> O spec de bugfix identificou o problema: nginx rejeitava arquivos > 1MB e o servidor
> carregava o arquivo inteiro em memória. A correção envolve validação no lado do servidor
> antes do upload e leitura em chunks.
>
> Este exemplo mostra TDD para o validador que implementa essa lógica.

---

## Fase Red — Testes que Falham

Critérios de aceite do spec mapeados para casos de teste:

| CA do spec | Caso de teste |
|-----------|---------------|
| Arquivo ≤ 50MB é aceito | `test_file_within_limit_is_accepted` |
| Arquivo > 50MB retorna 413 | `test_file_exceeding_limit_returns_413` |
| Tipos permitidos: jpg, png, pdf, docx | `test_allowed_file_types_are_accepted` |
| Tipo não permitido retorna 415 | `test_invalid_file_type_returns_415` |
| Arquivo vazio retorna 400 | `test_empty_file_returns_400` |
| Arquivo lido em chunks de 8KB | `test_file_is_read_in_chunks` |

```python
# tests/test_file_validator.py
"""
Fase Red — testes escritos ANTES da implementação.
Spec: modules/02-spec-driven-development/05-exemplos/spec-bugfix-timeout-upload.md
"""

import pytest
from io import BytesIO
from unittest.mock import MagicMock, patch

from app.validators.file_validator import FileValidator, FileValidationError


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def validator():
    return FileValidator(
        max_size_mb=50,
        allowed_types=["image/jpeg", "image/png", "application/pdf",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
        chunk_size_kb=8,
    )


def make_file(size_bytes: int, content_type: str = "image/jpeg", filename: str = "test.jpg"):
    """Factory para criar arquivo de upload simulado."""
    file = MagicMock()
    file.content_type = content_type
    file.filename = filename
    file.size = size_bytes
    file.read = MagicMock(return_value=b"x" * size_bytes)
    return file


# ─────────────────────────────────────────────
# TESTES DE TAMANHO
# ─────────────────────────────────────────────

class TestFileSizeValidation:

    def test_file_within_limit_is_accepted(self, validator):
        """
        CA: Arquivo com tamanho ≤ 50MB é aceito.
        """
        # Arrange
        arquivo = make_file(size_bytes=10 * 1024 * 1024)  # 10MB

        # Act
        resultado = validator.validate(arquivo)

        # Assert
        assert resultado.is_valid is True


    def test_file_at_exact_limit_is_accepted(self, validator):
        """
        Caso de borda: arquivo exatamente em 50MB deve ser aceito.
        """
        # Arrange
        arquivo = make_file(size_bytes=50 * 1024 * 1024)  # exatamente 50MB

        # Act
        resultado = validator.validate(arquivo)

        # Assert
        assert resultado.is_valid is True


    def test_file_exceeding_limit_returns_413(self, validator):
        """
        CA: Arquivo > 50MB retorna erro 413 (Payload Too Large).
        """
        # Arrange
        arquivo = make_file(size_bytes=51 * 1024 * 1024)  # 51MB

        # Act + Assert
        with pytest.raises(FileValidationError) as exc_info:
            validator.validate(arquivo)

        assert exc_info.value.status_code == 413
        assert "50MB" in exc_info.value.detail


    def test_empty_file_returns_400(self, validator):
        """
        CA: Arquivo vazio (0 bytes) retorna 400.
        """
        # Arrange
        arquivo = make_file(size_bytes=0)

        # Act + Assert
        with pytest.raises(FileValidationError) as exc_info:
            validator.validate(arquivo)

        assert exc_info.value.status_code == 400


# ─────────────────────────────────────────────
# TESTES DE TIPO
# ─────────────────────────────────────────────

class TestFileTypeValidation:

    @pytest.mark.parametrize("content_type,filename", [
        ("image/jpeg", "foto.jpg"),
        ("image/png",  "imagem.png"),
        ("application/pdf", "documento.pdf"),
        (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "contrato.docx"
        ),
    ])
    def test_allowed_file_types_are_accepted(self, validator, content_type, filename):
        """
        CA: Tipos permitidos (jpg, png, pdf, docx) são aceitos.
        """
        # Arrange
        arquivo = make_file(
            size_bytes=1024,
            content_type=content_type,
            filename=filename,
        )

        # Act
        resultado = validator.validate(arquivo)

        # Assert
        assert resultado.is_valid is True


    def test_invalid_file_type_returns_415(self, validator):
        """
        CA: Tipo não permitido (ex: .exe) retorna 415 (Unsupported Media Type).
        """
        # Arrange
        arquivo = make_file(
            size_bytes=1024,
            content_type="application/x-msdownload",
            filename="malware.exe",
        )

        # Act + Assert
        with pytest.raises(FileValidationError) as exc_info:
            validator.validate(arquivo)

        assert exc_info.value.status_code == 415


    def test_content_type_mismatch_with_extension_is_rejected(self, validator):
        """
        Caso de borda de segurança: arquivo com extensão .jpg mas content-type errado
        deve ser rejeitado (previne bypass de validação).
        """
        # Arrange
        arquivo = make_file(
            size_bytes=1024,
            content_type="application/x-msdownload",  # .exe disfarçado de .jpg
            filename="imagem.jpg",
        )

        # Act + Assert
        with pytest.raises(FileValidationError) as exc_info:
            validator.validate(arquivo)

        assert exc_info.value.status_code == 415


# ─────────────────────────────────────────────
# TESTES DE LEITURA EM CHUNKS
# ─────────────────────────────────────────────

class TestChunkReading:

    def test_file_is_read_in_chunks(self, validator):
        """
        CA: Arquivo é lido em chunks de 8KB para evitar uso excessivo de memória.
        Solução do spec: não carregar o arquivo inteiro em memória.
        """
        # Arrange
        tamanho = 100 * 1024  # 100KB
        arquivo = MagicMock()
        arquivo.content_type = "image/jpeg"
        arquivo.filename = "foto.jpg"
        arquivo.size = tamanho

        chunks_lidos = []
        arquivo.read = MagicMock(side_effect=lambda n: chunks_lidos.append(n) or b"x" * n)

        # Act
        validator.read_in_chunks(arquivo)

        # Assert
        assert all(chunk_size == 8 * 1024 for chunk_size in chunks_lidos[:-1])
```

---

## Fase Green — Implementação Mínima

Prompt usado:

```
Os testes acima estão falhando. Implemente FileValidator com os métodos validate
e read_in_chunks. max_size_mb, allowed_types e chunk_size_kb são parâmetros do __init__.
FileValidationError deve ter status_code e detail. Implemente o mínimo para os testes passarem.
```

---

## Fase Refactor — Melhorias Aplicadas

Após Green:
- `_validate_size` e `_validate_type` extraídos como métodos privados do `validate`
- Constante `CHUNK_SIZE = chunk_size_kb * 1024` calculada no `__init__` (não recalculada a cada leitura)
- Mensagem de erro de tamanho inclui tanto o limite quanto o tamanho enviado

Todos os testes continuaram passando.

---

## O que este exemplo demonstra

1. Como usar `@pytest.mark.parametrize` para testar múltiplos tipos de arquivo sem repetir código
2. Como testar comportamento de segurança (content-type mismatch) que vem de decisão do spec
3. Como testar que um arquivo é lido em chunks (verificar o padrão de chamadas ao mock)
4. Como fixtures + factory (`make_file`) mantêm os testes curtos e focados
