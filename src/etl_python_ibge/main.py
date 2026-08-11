import logging

from etl_python_ibge.pipeline.get_pipeline import run_pipeline


def main() -> None:
    """
    Ponto de entrada principal da aplicação.

    Executa o pipeline ETL do IBGE.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando aplicação.")

    run_pipeline()

    logger.info("Aplicação finalizada com sucesso.")


if __name__ == "__main__":
    main()
