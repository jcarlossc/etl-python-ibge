import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine


def execute_sql(
    engine: Engine,
    sql_file: Path,
) -> None:
    logger = logging.getLogger(__name__)

    logger.info("Executando script SQL: %s", sql_file)

    sql = sql_file.read_text(encoding="utf-8")

    statements = [
        statement.strip() for statement in sql.split(";") if statement.strip()
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

    logger.info("Script SQL executado com sucesso.")
