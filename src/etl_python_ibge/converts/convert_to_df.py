import logging
from typing import Any

import pandas as pd


def get_convert(
    data: list[list[dict[str, Any]]],
) -> pd.DataFrame:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando convrsão e limpeza dos dados.")

    result = []

    try:
        for response in data:
            for indicator in response:
                unit = indicator.get("unidade", {})

                for serie in indicator.get("series", []):
                    country = serie.get("pais", {})

                    for records in serie.get("serie", []):
                        for ano, valor in records.items():
                            if not ano.isdigit():
                                continue

                            valor = pd.to_numeric(
                                valor,
                                errors="coerce",
                            )

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
