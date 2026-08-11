from unittest.mock import MagicMock, patch

from etl_python_ibge.pipeline.get_pipeline import run_pipeline


@patch("etl_python_ibge.pipeline.get_pipeline.load_star_schema")
@patch("etl_python_ibge.pipeline.get_pipeline.execute_sql")
@patch("etl_python_ibge.pipeline.get_pipeline.get_engine")
@patch("etl_python_ibge.pipeline.get_pipeline.get_settings")
@patch("etl_python_ibge.pipeline.get_pipeline.create_star_schema")
@patch("etl_python_ibge.pipeline.get_pipeline.get_convert")
@patch("etl_python_ibge.pipeline.get_pipeline.retry")
@patch("etl_python_ibge.pipeline.get_pipeline.setup_logger")
@patch("etl_python_ibge.pipeline.get_pipeline.load_all_configs")
def test_run_pipeline_success(
    mock_load_configs,
    mock_setup_logger,
    mock_retry,
    mock_get_convert,
    mock_create_star_schema,
    mock_get_settings,
    mock_get_engine,
    mock_execute_sql,
    mock_load_star_schema,
):
    """Testa a execução completa do pipeline com sucesso."""

    # Configura as configurações falsas.
    mock_load_configs.return_value = {
        "logging": {},
        "paths": {
            "logs": {
                "file": "test.log",
            },
        },
        "identifiers": {
            "identifiers": [77818],
            "url": "https://example.com",
        },
    }

    # Dados fictícios retornados pela API.
    mock_retry.return_value = {
        "dados": "dados fictícios",
    }

    # DataFrame fictício.
    mock_df = MagicMock()
    mock_df.__len__.return_value = 10

    mock_get_convert.return_value = mock_df

    # Star Schema fictício.
    mock_star_schema = {
        "dim_indicador": MagicMock(),
        "dim_unidade": MagicMock(),
        "dim_pais": MagicMock(),
        "dim_tempo": MagicMock(),
        "fato_indicador": MagicMock(),
    }

    mock_create_star_schema.return_value = mock_star_schema

    # Configuração falsa do banco.
    mock_settings = MagicMock()

    mock_get_settings.return_value = mock_settings

    # Engine falso.
    mock_engine = MagicMock()

    mock_get_engine.return_value = mock_engine

    # Executa o pipeline.
    run_pipeline()

    # Verifica se as configurações foram carregadas.
    mock_load_configs.assert_called_once()

    # Verifica se o logger foi configurado.
    mock_setup_logger.assert_called_once_with(
        {},
        "test.log",
    )

    # Verifica se a API foi executada através do retry.
    mock_retry.assert_called_once()

    # Verifica a conversão para DataFrame.
    mock_get_convert.assert_called_once_with(
        mock_retry.return_value,
    )

    # Verifica a criação do Star Schema.
    mock_create_star_schema.assert_called_once_with(
        mock_df,
    )

    # Verifica a criação das configurações do banco.
    mock_get_settings.assert_called_once()

    # Verifica a criação da conexão.
    mock_get_engine.assert_called_once_with(
        mock_settings,
    )

    # Verifica a execução do SQL.
    mock_execute_sql.assert_called_once()

    # Verifica o carregamento das tabelas.
    mock_load_star_schema.assert_called_once_with(
        star_schema=mock_star_schema,
        engine=mock_engine,
    )

    # Verifica se a conexão foi encerrada.
    mock_engine.dispose.assert_called_once()
