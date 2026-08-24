import pandas as pd

from src.transformation.pedido_transformation import (
transform_pedido,
)

def test_transform_pedido():

    df = pd.DataFrame(
        {
            "id_pedido": [1],
            "id_cliente": [1],
            "data_pedido": ["2026-08-20"],
            "status_pedido": [" finalizado "],
            "valor_total": ["3520.00"],
            "valor_frete": ["20.00"],
            "forma_pagamento": [" pix "],
        }
    )

    result = transform_pedido(df)

    assert len(result) == 1
    assert result["status_pedido"].iloc[0] == "FINALIZADO"
    assert result["forma_pagamento"].iloc[0] == "PIX"
    assert result["valor_total"].iloc[0] == 3520.00
    assert result["valor_frete"].iloc[0] == 20.00

    assert pd.api.types.is_datetime64_any_dtype(
        result["data_pedido"]
    )

def test_transform_pedido_cria_colunas_de_data():

    df = pd.DataFrame(
        {
            "id_pedido": [1],
            "id_cliente": [1],
            "data_pedido": ["2026-08-20"],
            "status_pedido": ["FINALIZADO"],
            "valor_total": [3520.00],
            "valor_frete": [20.00],
            "forma_pagamento": ["PIX"],
        }
    )

    result = transform_pedido(df)

    assert result["ano"].iloc[0] == 2026
    assert result["mes"].iloc[0] == 8
    assert result["dia"].iloc[0] == 20

def test_transform_pedido_limpa_status():
    df = pd.DataFrame(
        {
            "id_pedido": [1],
            "id_cliente": [1],
            "data_pedido": ["2026-08-20"],
            "status_pedido": ["  pendente  "],
            "valor_total": [100.00],
            "valor_frete": [20.00],
            "forma_pagamento": ["  cartao  "],
        }
    )

    result = transform_pedido(df)

    assert result["status_pedido"].iloc[0] == "PENDENTE"
    assert result["forma_pagamento"].iloc[0] == "CARTAO"