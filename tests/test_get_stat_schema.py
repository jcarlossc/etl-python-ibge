import pandas as pd
import pytest

from etl_python_ibge.star_schema.get_star_schema import create_star_schema


def test_create_star_schema_success():
    # Cria um DataFrame de exemplo.
    df = pd.DataFrame(
        {
            "id_indicador": [77818, 77818],
            "indicador": [
                "Turismo",
                "Turismo",
            ],
            "id_unidade": [
                "turistas",
                "turistas",
            ],
            "classe": [
                "N",
                "N",
            ],
            "multiplicador": [
                1,
                1,
            ],
            "sigla_pais": [
                "BR",
                "BR",
            ],
            "pais": [
                "Brasil",
                "Brasil",
            ],
            "ano": [
                2000,
                2001,
            ],
            "valor": [
                100,
                200,
            ],
        }
    )

    # Cria o modelo estrela.
    result = create_star_schema(df)

    # Verifica se o retorno é um dicionário.
    assert isinstance(result, dict)

    # Verifica se todas as tabelas foram criadas.
    assert "dim_indicador" in result
    assert "dim_unidade" in result
    assert "dim_pais" in result
    assert "dim_tempo" in result
    assert "fato_indicador" in result


def test_create_star_schema_empty_dataframe():
    # Cria um DataFrame vazio.
    df = pd.DataFrame()

    # Verifica se uma exceção é lançada.
    with pytest.raises(ValueError):
        create_star_schema(df)


def test_create_star_schema_invalid_type():
    # Verifica se um tipo inválido gera exceção.
    with pytest.raises(TypeError):
        create_star_schema([])
