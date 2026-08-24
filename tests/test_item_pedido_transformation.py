import pandas as pd
import pytest

from src.transformation.item_pedido_transformation import (
transform_item_pedido,
)

def test_transform_item_pedido():
    df = pd.DataFrame(
        {
            "id_item_pedido": [1],
            "id_pedido": [1],
            "id_produto": [1],
            "quantidade": ["2"],
            "preco_unitario": ["3500.00"],
            "subtotal": ["7000.00"],
        }
    )

    result = transform_item_pedido(df)

    assert result["quantidade"].iloc[0] == 2
    assert result["preco_unitario"].iloc[0] == 3500.00
    assert result["subtotal"].iloc[0] == 7000.00

def test_transform_item_pedido_quantidade_inteiro():
    df = pd.DataFrame(
        {
            "id_item_pedido": [1],
            "id_pedido": [1],
            "id_produto": [1],
            "quantidade": ["2"],
            "preco_unitario": ["100.00"],
            "subtotal": ["200.00"],
        }
    )

    result = transform_item_pedido(df)

    assert pd.api.types.is_integer_dtype(
        result["quantidade"]
    )


def test_transform_item_pedido_valores_numericos():

    df = pd.DataFrame(
        {
            "id_item_pedido": [1],
            "id_pedido": [1],
            "id_produto": [1],
            "quantidade": ["3"],
            "preco_unitario": ["100.50"],
            "subtotal": ["301.50"],
        }
    )

    result = transform_item_pedido(df)

    assert pd.api.types.is_numeric_dtype(
        result["preco_unitario"]
    )

    assert pd.api.types.is_numeric_dtype(
        result["subtotal"]
    )

def test_transform_item_pedido_preserva_quantidade():

    df = pd.DataFrame(
        {
            "id_item_pedido": [1, 2],
            "id_pedido": [1, 1],
            "id_produto": [1, 2],
            "quantidade": [2, 5],
            "preco_unitario": [100.00, 50.00],
            "subtotal": [200.00, 250.00],
        }
    )

    result = transform_item_pedido(df)

    assert result["quantidade"].tolist() == [2, 5]

def test_transform_item_pedido_detecta_valor_invalido():

    df = pd.DataFrame(
        {
            "id_item_pedido": [1],
            "id_pedido": [1],
            "id_produto": [1],
            "quantidade": ["abc"],
            "preco_unitario": ["100.00"],
            "subtotal": ["200.00"],
        }
    )

    with pytest.raises((ValueError, TypeError)):
        transform_item_pedido(df)
