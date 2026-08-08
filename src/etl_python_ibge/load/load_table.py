import logging

import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def load_table(
    dataframe: pd.DataFrame,
    table_name: str,
    engine: Engine,
) -> None:
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
