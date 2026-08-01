import logging
from typing import Any

import requests


def get_ibge_api(
    identifiers: dict[str, int],
    base_url: str,
) -> list[Any]:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando coleta de dados.")

    results = []

    for identifier in identifiers.values():
        endpoint = f"{base_url}{identifier}"

        logger.info("Consultando indicador %s.", identifier)

        try:
            response = requests.get(endpoint, timeout=30)
            response.raise_for_status()

            results.append(response.json())

        except requests.RequestException:
            logger.exception("Erro ao consultar o indicador %s.", identifier)
            raise

    logger.info("Coleta finalizada com sucesso.")

    return results
