import logging

import pandas as pd
from sqlalchemy.engine import Engine

# from sqlalchemy.exc import SQLAlchemyError


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
