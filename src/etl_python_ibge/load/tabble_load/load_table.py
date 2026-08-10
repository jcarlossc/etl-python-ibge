import logging

import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def load_table(
    dataframe: pd.DataFrame,
    table_name: str,
    engine: Engine,
) -> None:
    """
    Carrega os dados de um DataFrame em uma tabela MySQL.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dados que serão carregados.

    table_name : str
        Nome da tabela de destino.

    engine : Engine
        Engine SQLAlchemy utilizada para conexão com o banco.

    Raises
    ------
    RuntimeError
        Caso ocorra erro durante a carga dos dados.
    """

    logger = logging.getLogger(__name__)

    logger.info(
        "Iniciando carga da tabela '%s'.",
        table_name,
    )

    try:
        dataframe.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=1000,
            method="multi",
        )

        logger.info(
            "Tabela '%s' carregada com sucesso. Registros: %d.",
            table_name,
            len(dataframe),
        )

    except SQLAlchemyError as error:
        logger.exception(
            "Erro ao carregar a tabela '%s'.",
            table_name,
        )

        raise RuntimeError(f"Erro ao carregar a tabela '{table_name}'.") from error
