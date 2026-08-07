import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def execute_sql(
    engine: Engine,
    sql_file: Path,
) -> None:
    """
    Executa um arquivo SQL.

    A função lê um arquivo contendo comandos SQL e executa
    cada instrução sequencialmente utilizando uma conexão
    SQLAlchemy.

    Parameters
    ----------
    engine : Engine
        Engine utilizada para conexão com o banco de dados.

    sql_file : Path
        Caminho do arquivo SQL.

    Raises
    ------
    FileNotFoundError
        Caso o arquivo SQL não exista.

    RuntimeError
        Caso ocorra erro durante a execução do script SQL.
    """

    logger = logging.getLogger(__name__)

    logger.info("Executando script SQL: %s", sql_file)

    try:
        # Lê todo o conteúdo do arquivo SQL.
        sql = sql_file.read_text(encoding="utf-8")

        # Separa os comandos SQL utilizando ';'.
        statements = [
            statement.strip() for statement in sql.split(";") if statement.strip()
        ]

        # Abre uma transação.
        with engine.begin() as connection:
            # Executa cada comando SQL.
            for statement in statements:
                connection.execute(text(statement))

        logger.info("Script SQL executado com sucesso.")

    except FileNotFoundError:
        logger.error("Arquivo SQL não encontrado: %s", sql_file)

        raise

    except SQLAlchemyError as error:
        logger.exception("Erro ao executar script SQL.")

        raise RuntimeError("Erro ao executar script SQL.") from error
