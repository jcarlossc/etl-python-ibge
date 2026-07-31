import pytest
import requests

from etl_python_ibge.utils.retry.get_retry import retry


def test_retry_success():
    """Deve retornar o resultado quando a função executa com sucesso."""

    def connect():
        return "OK"

    result = retry(connect)

    assert result == "OK"


def test_retry_success_after_retry(monkeypatch):
    """
    Deve executar novamente a função quando ocorrer
    uma falha temporária.
    """

    calls = {"count": 0}

    def connect():
        calls["count"] += 1

        if calls["count"] == 1:
            raise requests.RequestException("Erro temporário")

        return "OK"

    # Evita que o teste espere realmente.
    monkeypatch.setattr("time.sleep", lambda _: None)

    result = retry(connect)

    assert result == "OK"

    # Deve executar duas vezes.
    assert calls["count"] == 2


def test_retry_max_attempts(monkeypatch):
    """
    Deve relançar a exceção quando todas
    as tentativas falharem.
    """

    def connect():
        raise requests.RequestException("Falha")

    monkeypatch.setattr("time.sleep", lambda _: None)

    with pytest.raises(requests.RequestException):
        retry(connect, max_attempts=3)
