from decimal import Decimal

import pandas as pd

from src.transformation.produto_transformation import (
transform_produto,
)

def test_transform_produto():
    df = pd.DataFrame(
        {
            "id_produto": [1],
            "nome_produto": ["  Notebook Dell  "],
            "categoria": [" informatica "],
            "subcategoria": [" notebook "],
            "preco_venda": [3500.00],
            "preco_custo": [2800.00],
            "quantidade_estoque": [30],
        }
    )

    result = transform_produto(df)

    assert len(result) == 1

    assert result["nome_produto"].iloc[0] == "Notebook Dell"
    assert result["categoria"].iloc[0] == "Informatica"
    assert result["subcategoria"].iloc[0] == "Notebook"

    assert result["preco_venda"].iloc[0] == 3500.00
    assert result["preco_custo"].iloc[0] == 2800.00
    assert result["quantidade_estoque"].iloc[0] == 30

def test_transform_produto_remove_espacos():
    df = pd.DataFrame(
        {
            "id_produto": [1],
            "nome_produto": ["  Notebook Dell  "],
            "categoria": [" informatica "],
            "subcategoria": [" notebook "],
            "preco_venda": [3500.00],
            "preco_custo": [2800.00],
            "quantidade_estoque": [30],
        }
    )

    result = transform_produto(df)

    assert result["nome_produto"].iloc[0] == "Notebook Dell"

def test_transform_produto_converte_numericos():
    df = pd.DataFrame(
        {
            "id_produto": [1],
            "nome_produto": ["Notebook Dell"],
            "categoria": ["Informatica"],
            "subcategoria": ["Notebook"],
            "preco_venda": ["3500.00"],
            "preco_custo": ["2800.00"],
            "quantidade_estoque": ["30"],
        }
    )

    result = transform_produto(df)

    assert pd.api.types.is_numeric_dtype(
        result["preco_venda"]
    )

    assert pd.api.types.is_numeric_dtype(
        result["preco_custo"]
    )

    assert pd.api.types.is_numeric_dtype(
        result["quantidade_estoque"]
    )
