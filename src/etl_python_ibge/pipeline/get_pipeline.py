import logging
from functools import partial
from pathlib import Path

from etl_python_ibge.converts.convert_to_df import get_convert
from etl_python_ibge.database.get_connection import get_engine
from etl_python_ibge.ibge_api.api_ibge import get_ibge_api
from etl_python_ibge.load.load_schema.load_table_schema import load_star_schema
from etl_python_ibge.sql.execute.execute_sql import execute_sql
from etl_python_ibge.star_schema.get_star_schema import create_star_schema
from etl_python_ibge.utils.config_settings.Settings import get_settings
from etl_python_ibge.utils.load_yaml.loader_yaml import load_all_configs
from etl_python_ibge.utils.loggers.logger import setup_logger
from etl_python_ibge.utils.retry.get_retry import retry


def run_pipeline() -> None:
    # ------------------------------------------------------------------
    # 1. Carrega as configurações
    # ------------------------------------------------------------------

    logger = logging.getLogger(__name__)

    try:
        config_path = Path("config")

    except Exception:
        logger.exception("Erro ao carregar as configurações.")
        raise

    # ------------------------------------------------------------------
    # 2. Configura o logger
    # ------------------------------------------------------------------

    try:
        configs = load_all_configs(config_path)

        setup_logger(
            configs["logging"],
            configs["paths"]["logs"]["file"],
        )

    except Exception:
        logger.exception("Erro ao configurar o logger.")
        raise

    # ------------------------------------------------------------------
    # 3. Consome a API do IBGE
    # ------------------------------------------------------------------

    logger.info("Iniciando pipeline ETL do IBGE")

    try:
        logger.info("Iniciando coleta dos dados do IBGE.")

        ibge_data = retry(
            partial(
                get_ibge_api,
                configs["identifiers"]["identifiers"],
                configs["identifiers"]["url"],
            ),
            max_attempts=3,
            delay=2,
        )

        logger.info("Dados obtidos com sucesso da API do IBGE.")

    except Exception:
        logger.exception("Erro durante a coleta dos dados do IBGE.")
        raise

    # ------------------------------------------------------------------
    # 4. Converte os dados para DataFrame
    # ------------------------------------------------------------------

    try:
        logger.info("Convertendo dados para DataFrame.")

        ibge_df = get_convert(ibge_data)

        logger.info(
            "Conversão concluída. Total de registros: %s",
            len(ibge_df),
        )

    except Exception:
        logger.exception("Erro durante a conversão dos dados.")
        raise

    # ------------------------------------------------------------------
    # 5. Cria o Star Schema
    # ------------------------------------------------------------------

    try:
        logger.info("Criando modelo dimensional Star Schema.")

        ibge_star_schema = create_star_schema(ibge_df)

        logger.info(
            "Star Schema criado com sucesso. Tabelas: %s",
            list(ibge_star_schema.keys()),
        )

    except Exception:
        logger.exception("Erro ao criar o Star Schema.")
        raise

    # ------------------------------------------------------------------
    # 6. Cria conexão com o banco de dados
    # ------------------------------------------------------------------

    engine = None

    try:
        logger.info("Criando conexão com o banco de dados.")

        # Representa as configurações da aplicação (.env).
        settings = get_settings()

        engine = get_engine(settings)

        logger.info("Conexão com o banco de dados criada com sucesso.")

        # --------------------------------------------------------------
        # 7. Cria as tabelas do Star Schema
        # --------------------------------------------------------------

        logger.info("Executando script de criação do Star Schema.")

        execute_sql(
            engine=engine,
            sql_file=Path("src/etl_python_ibge/sql/create_star/create_star_schema.sql"),
        )

        logger.info("Estrutura do banco criada com sucesso.")

        # --------------------------------------------------------------
        # 8. Carrega os dados no banco
        # --------------------------------------------------------------

        logger.info("Iniciando carga do Star Schema.")

        load_star_schema(
            star_schema=ibge_star_schema,
            engine=engine,
        )

        logger.info("Carga do Star Schema concluída com sucesso.")

    except Exception:
        logger.exception("Erro durante a criação ou carga do banco de dados.")
        raise

    finally:
        # --------------------------------------------------------------
        # 9. Libera os recursos
        # --------------------------------------------------------------

        if engine is not None:
            engine.dispose()

            logger.info("Conexão com o banco de dados encerrada.")

    logger.info("Pipeline ETL finalizado com sucesso.")
