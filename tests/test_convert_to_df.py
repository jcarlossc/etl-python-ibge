import pandas as pd

from etl_python_ibge.converts.convert_to_df import get_convert


def test_get_convert_success():
    # Dados simulando a resposta da API do IBGE.
    data = [
        [
            {
                "id": 77857,
                "indicador": "Internet",
                "unidade": {
                    "id": "%",
                    "classe": "N",
                    "multiplicador": 1,
                },
                "series": [
                    {
                        "pais": {
                            "id": "BR",
                            "nome": "Brasil",
                        },
                        "serie": [
                            {
                                "2020": "81.34",
                                "2021": "80.69",
                            }
                        ],
                    }
                ],
            }
        ]
    ]

    # Executa a função de conversão.
    df = get_convert(data)

    # Verifica se o retorno é um DataFrame.
    assert isinstance(df, pd.DataFrame)

    # Verifica a quantidade de registros convertidos.
    assert len(df) == 2

    # Verifica se as colunas esperadas foram criadas.
    assert list(df.columns) == [
        "id_indicador",
        "indicador",
        "id_unidade",
        "classe",
        "multiplicador",
        "sigla_pais",
        "pais",
        "ano",
        "valor",
    ]

    # Verifica os valores da primeira linha.
    assert df.iloc[0]["ano"] == 2020
    assert df.iloc[0]["valor"] == 81.34


def test_get_convert_ignore_invalid_year():
    # Dados contendo um intervalo de anos e um ano válido.
    data = [
        [
            {
                "id": 1,
                "indicador": "Teste",
                "unidade": {},
                "series": [
                    {
                        "pais": {},
                        "serie": [
                            {
                                "1990-1995": "15",
                                "2020": "20",
                            }
                        ],
                    }
                ],
            }
        ]
    ]

    # Executa a conversão.
    df = get_convert(data)

    # Apenas o ano válido deve permanecer.
    assert len(df) == 1
    assert df.iloc[0]["ano"] == 2020


def test_get_convert_ignore_invalid_value():
    # Dados contendo um valor inválido e um valor válido.
    data = [
        [
            {
                "id": 1,
                "indicador": "Teste",
                "unidade": {},
                "series": [
                    {
                        "pais": {},
                        "serie": [
                            {
                                "2020": "...",
                                "2021": "15",
                            }
                        ],
                    }
                ],
            }
        ]
    ]

    # Executa a conversão.
    df = get_convert(data)

    # Apenas o valor numérico deve ser convertido.
    assert len(df) == 1
    assert df.iloc[0]["ano"] == 2021
