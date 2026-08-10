from unittest.mock import patch

import pandas as pd
import pytest

from etl_python_ibge.load.load_schema.load_table_schema import (
    load_star_schema,
)


# Cria um modelo estrela falso para o teste
@pytest.fixture
def star_schema():
    return {
        "dim_indicador": pd.DataFrame({"id": [1]}),
        "dim_unidade": pd.DataFrame({"id": [1]}),
        "dim_pais": pd.DataFrame({"id": [1]}),
        "dim_tempo": pd.DataFrame({"ano": [2020]}),
        "fato_indicador": pd.DataFrame({"valor": [100]}),
    }


def test_load_star_schema_success(star_schema):
    # Mock evita realmente inserir dados no MySQL
    with patch(
        "etl_python_ibge.load.load_schema.load_table_schema.load_table"
    ) as mock_load_table:
        # Executa a função
        result = load_star_schema(
            star_schema=star_schema,
            engine=None,
        )

    # A função não deve retornar nada
    assert result is None

    # load_table deve ser chamado 5 vezes
    assert mock_load_table.call_count == 5


def test_load_star_schema_loads_all_tables(star_schema):
    # Mock da função responsável pela carga
    with patch(
        "etl_python_ibge.load.load_schema.load_table_schema.load_table"
    ) as mock_load_table:
        load_star_schema(
            star_schema=star_schema,
            engine=None,
        )

    # Verifica os nomes das tabelas carregadas
    table_names = [call.kwargs["table_name"] for call in mock_load_table.call_args_list]

    assert table_names == [
        "dim_indicador",
        "dim_unidade",
        "dim_pais",
        "dim_tempo",
        "fato_indicador",
    ]


def test_load_star_schema_passes_correct_dataframes(star_schema):
    # Mock para não executar a carga real
    with patch(
        "etl_python_ibge.load.load_schema.load_table_schema.load_table"
    ) as mock_load_table:
        load_star_schema(
            star_schema=star_schema,
            engine=None,
        )

    # Verifica se cada DataFrame correto foi enviado
    assert (
        mock_load_table.call_args_list[0].kwargs["dataframe"]
        is star_schema["dim_indicador"]
    )

    assert (
        mock_load_table.call_args_list[1].kwargs["dataframe"]
        is star_schema["dim_unidade"]
    )

    assert (
        mock_load_table.call_args_list[2].kwargs["dataframe"] is star_schema["dim_pais"]
    )

    assert (
        mock_load_table.call_args_list[3].kwargs["dataframe"]
        is star_schema["dim_tempo"]
    )

    assert (
        mock_load_table.call_args_list[4].kwargs["dataframe"]
        is star_schema["fato_indicador"]
    )


def test_load_star_schema_runtime_error(star_schema):
    # Simula um erro durante a carga
    with patch(
        "etl_python_ibge.load.load_schema.load_table_schema.load_table"
    ) as mock_load_table:
        mock_load_table.side_effect = RuntimeError("Erro ao carregar tabela")

        # Verifica se o erro é propagado
        with pytest.raises(RuntimeError, match="Erro ao carregar tabela"):
            load_star_schema(
                star_schema=star_schema,
                engine=None,
            )
