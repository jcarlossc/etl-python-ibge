from unittest.mock import patch

from etl_python_ibge.main import main


@patch("etl_python_ibge.main.run_pipeline")
def test_main(mock_run_pipeline):
    """Testa se o main executa o pipeline."""

    # Executa o ponto de entrada da aplicação.
    main()

    # Verifica se o pipeline foi chamado uma vez.
    mock_run_pipeline.assert_called_once()
