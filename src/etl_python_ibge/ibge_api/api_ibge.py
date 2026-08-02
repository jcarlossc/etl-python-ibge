import logging
from typing import Any

import requests


def get_ibge_api(
    identifiers: dict[str, int],
    base_url: str,
) -> list[Any]:
    """
    Consulta indicadores da API do IBGE e retorna os resultados em formato JSON.

    A função percorre todos os identificadores informados, realiza uma
    requisição HTTP para cada indicador e armazena o conteúdo JSON de
    cada resposta em uma lista.

    Caso alguma requisição apresente erro de conexão, timeout ou código
    HTTP inválido, a exceção é registrada no log e propagada para a camada
    superior da aplicação.

    Args:
        identifiers:
            Dicionário contendo os indicadores do IBGE.
            Exemplo:
            {
                "pib": 5938,
                "ipca": 1737
            }

        base_url:
            URL base da API do IBGE.

    Returns:
        list[Any]:
            Lista contendo os objetos JSON retornados pela API.

    Raises:
        requests.RequestException:
            Caso ocorra qualquer erro durante a comunicação com a API.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando coleta de dados.")

    # Lista que armazenará todas as respostas da API.
    results = []

    for identifier in identifiers.values():
        # Monta a URL completa do endpoint.
        endpoint = f"{base_url}{identifier}"

        logger.info("Consultando indicador %s.", identifier)

        try:
            # Realiza a requisição HTTP.
            response = requests.get(endpoint, timeout=30)

            # Gera exceção caso o status HTTP seja diferente de 200.
            response.raise_for_status()

            # Armazena o JSON retornado.
            results.append(response.json())

        except requests.RequestException:
            logger.exception("Erro ao consultar o indicador %s.", identifier)
            raise

    logger.info("Coleta finalizada com sucesso.")

    return results
