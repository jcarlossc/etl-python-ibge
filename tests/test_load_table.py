from unittest.mock import Mock

import pandas as pd
import pytest
from etl_python_ibge.load.tabble_load.load_table import load_table
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def test_load_table_success(monkeypatch):
    """
    Testa a carga de um DataFrame com sucesso.
    """

    dataframe = pd.DataFrame(
        {
            "id_indicador": [77818, 77819],
            "indicador": [
                "Turismo",
                "Educação",
            ],
        }
    )

    engine = Engine

    # Guarda os argumentos recebidos pelo to_sql.
    captured = {}

    def mock_to_sql(**kwargs):
        captured.update(kwargs)

    # Substitui temporariamente o to_sql pelo mock.
    monkeypatch.setattr(
        dataframe,
        "to_sql",
        mock_to_sql,
    )

    load_table(
        dataframe=dataframe,
        table_name="dim_indicador",
        engine=engine,
    )

    # Verifica o nome da tabela.
    assert captured["name"] == "dim_indicador"

    # Verifica a conexão.
    assert captured["con"] is engine

    # Verifica que os dados devem ser adicionados.
    assert captured["if_exists"] == "append"

    # Verifica que o índice do DataFrame não será enviado.
    assert captured["index"] is False

    # Verifica o tamanho dos lotes.
    assert captured["chunksize"] == 1000

    # Verifica o método utilizado para inserção.
    assert captured["method"] == "multi"


def test_load_table_sqlalchemy_error(monkeypatch):
    """
    Testa o tratamento de erro durante a carga da tabela.
    """

    dataframe = pd.DataFrame(
        {
            "id_indicador": [77818],
            "indicador": ["Turismo"],
        }
    )

    engine = Mock()

    # Cria um mock que gera um erro SQLAlchemy.
    mock_to_sql = Mock(side_effect=SQLAlchemyError("Erro de conexão com o banco."))

    # Substitui o método to_sql pelo mock.
    monkeypatch.setattr(
        dataframe,
        "to_sql",
        mock_to_sql,
    )

    # Verifica se a função transforma
    # SQLAlchemyError em RuntimeError.
    with pytest.raises(
        RuntimeError,
        match="Erro ao carregar a tabela 'dim_indicador'.",
    ):
        load_table(
            dataframe=dataframe,
            table_name="dim_indicador",
            engine=engine,
        )
