import pandas as pd


def create_star_schema(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    # Dimensão Indicador
    dim_indicador = (
        df[
            [
                "id_indicador",
                "indicador",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_indicador.insert(
        0,
        "id_indicador_sk",
        range(1, len(dim_indicador) + 1),
    )

    # Dimensão Unidade
    dim_unidade = (
        df[
            [
                "id_unidade",
                "classe",
                "multiplicador",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_unidade["multiplicador"] = (
        dim_unidade["multiplicador"].fillna(1).astype("Int64")
    )

    dim_unidade.insert(
        0,
        "id_unidade_sk",
        range(1, len(dim_unidade) + 1),
    )

    dim_unidade.rename(
        columns={
            "id_unidade": "unidade",
        },
        inplace=True,
    )

    # Dimensão País
    dim_pais = (
        df[
            [
                "sigla_pais",
                "pais",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_pais.insert(
        0,
        "id_pais_sk",
        range(1, len(dim_pais) + 1),
    )

    # Dimensão Tempo
    dim_tempo = pd.DataFrame(
        {
            "ano": sorted(df["ano"].unique()),
        }
    ).reset_index(drop=True)

    dim_tempo.insert(
        0,
        "id_tempo",
        range(1, len(dim_tempo) + 1),
    )

    # Relacionamentos
    fato = df.copy()

    # Indicador
    fato = fato.merge(
        dim_indicador[
            [
                "id_indicador_sk",
                "id_indicador",
            ]
        ],
        on="id_indicador",
    )

    # Unidade
    fato = fato.merge(
        dim_unidade[
            [
                "id_unidade_sk",
                "unidade",
            ]
        ],
        left_on="id_unidade",
        right_on="unidade",
    )

    # País
    fato = fato.merge(
        dim_pais[
            [
                "id_pais_sk",
                "sigla_pais",
                "pais",
            ]
        ],
        on=[
            "sigla_pais",
            "pais",
        ],
    )

    # Tempo
    fato = fato.merge(
        dim_tempo,
        on="ano",
    )

    # Tabela fato
    fato = fato[
        [
            "id_indicador_sk",
            "id_unidade_sk",
            "id_pais_sk",
            "id_tempo",
            "valor",
        ]
    ].copy()

    fato.insert(
        0,
        "id_fato",
        range(1, len(fato) + 1),
    )

    return {
        "dim_indicador": dim_indicador,
        "dim_unidade": dim_unidade,
        "dim_pais": dim_pais,
        "dim_tempo": dim_tempo,
        "fato_indicador": fato,
    }
