import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def execute_sql(
    engine: Engine,
    sql_file: Path,
) -> None:
    logger = logging.getLogger(__name__)

    logger.info("Executando script SQL: %s", sql_file)

    try:
        sql = sql_file.read_text(encoding="utf-8")

        statements = [
            statement.strip() for statement in sql.split(";") if statement.strip()
        ]

        with engine.begin() as connection:
            for statement in statements:
                connection.execute(text(statement))

        logger.info("Script SQL executado com sucesso.")

    except FileNotFoundError:
        logger.error("Arquivo SQL não encontrado: %s", sql_file)

        raise

    except SQLAlchemyError as error:
        logger.exception("Erro ao executar script SQL.")

        raise RuntimeError("Erro ao executar script SQL.") from error
