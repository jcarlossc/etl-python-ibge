import pytest
import requests

from etl_python_ibge.ibge_api.api_ibge import get_ibge_api


def test_get_ibge_api_success(monkeypatch):
    # Simula uma resposta válida da API.
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"valor": 100}

    # Substitui requests.get por uma função simulada.
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    # Indicadores utilizados no teste.
    identifiers = {
        "pib": 5938,
        "ipca": 1737,
    }

    # Executa a função.
    result = get_ibge_api(identifiers, "https://fake-api/")

    # Verifica os resultados retornados.
    assert len(result) == 2
    assert result[0]["valor"] == 100


def test_get_ibge_api_http_error(monkeypatch):
    # Simula uma resposta com erro HTTP.
    class MockResponse:
        def raise_for_status(self):
            raise requests.HTTPError()

    # Substitui requests.get por uma função simulada.
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    # Verifica se a exceção é propagada pela função.
    with pytest.raises(requests.HTTPError):
        get_ibge_api({"pib": 5938}, "https://fake-api/")
