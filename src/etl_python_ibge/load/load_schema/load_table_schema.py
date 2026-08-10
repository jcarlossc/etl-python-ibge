import logging

import pandas as pd
from sqlalchemy.engine import Engine

from etl_python_ibge.load.tabble_load.load_table import load_table


def load_star_schema(
    star_schema: dict[str, pd.DataFrame],
    engine: Engine,
) -> None:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando carga do modelo estrela.")

    try:
        load_table(
            dataframe=star_schema["dim_indicador"],
            table_name="dim_indicador",
            engine=engine,
        )

        load_table(
            dataframe=star_schema["dim_unidade"],
            table_name="dim_unidade",
            engine=engine,
        )

        load_table(
            dataframe=star_schema["dim_pais"],
            table_name="dim_pais",
            engine=engine,
        )

        load_table(
            dataframe=star_schema["dim_tempo"],
            table_name="dim_tempo",
            engine=engine,
        )

        load_table(
            dataframe=star_schema["fato_indicador"],
            table_name="fato_indicador",
            engine=engine,
        )

        logger.info("Modelo estrela carregado com sucesso.")

    except RuntimeError:
        logger.exception("Erro durante a carga do modelo estrela.")

        raise
