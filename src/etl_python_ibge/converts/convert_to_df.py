import logging
from typing import Any

import pandas as pd


def get_convert(
    data: list[list[dict[str, Any]]],
) -> pd.DataFrame:
    """
    Converte a resposta da API do IBGE em um DataFrame tabular.

    A API retorna uma lista de respostas, onde cada resposta contém um ou
    mais indicadores. Para cada indicador são extraídos:

    - informações do indicador;
    - informações da unidade;
    - informações do país;
    - ano da observação;
    - valor do indicador.

    Apenas registros cujo ano seja composto exclusivamente por dígitos e
    cujo valor possa ser convertido para número são incluídos no DataFrame.

    Args:
        data:
            Lista contendo as respostas da API do IBGE.

    Returns:
        pd.DataFrame:
            DataFrame contendo os indicadores convertidos.

    Raises:
        ValueError:
            Caso ocorra erro durante a conversão dos dados.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando convrsão e limpeza dos dados.")

    result = []

    try:
        # Percorre cada resposta retornada pela API.
        for response in data:
            # Percorre cada indicador presente na resposta.
            for indicator in response:
                unit = indicator.get("unidade", {})

                for serie in indicator.get("series", []):
                    country = serie.get("pais", {})

                    for records in serie.get("serie", []):
                        # Cada registro possui um ou mais pares ano/valor.
                        for ano, valor in records.items():
                            # Mantém apenas anos válidos (1990, 1995, 2000...).
                            if not ano.isdigit():
                                continue

                            valor = pd.to_numeric(
                                valor,
                                errors="coerce",
                            )

                            # Ignora valores não numéricos.
                            if pd.notna(valor):
                                result.append(
                                    {
                                        "id_indicador": indicator.get("id"),
                                        "indicador": indicator.get("indicador"),
                                        "id_unidade": unit.get("id"),
                                        "classe": unit.get("classe"),
                                        "multiplicador": unit.get("multiplicador"),
                                        "sigla_pais": country.get("id"),
                                        "pais": country.get("nome"),
                                        "ano": int(ano),
                                        "valor": valor,
                                    }
                                )

        logger.info("Finalizando a convrsão e limpeza dos dados.")

        return pd.DataFrame(result)

    except Exception as exc:
        logger.exception("Erro ao converter resposta da API do IBGE.")

        raise ValueError("Falha na conversão dos dados da API.") from exc
