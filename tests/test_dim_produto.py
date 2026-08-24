import pandas as pd

from src.warehouse.dim_produto import transform_dim_produto

def test_transform_dim_produto_colunas():
    df = pd.DataFrame(
        {
            "id_produto": [1, 2],
            "nome_produto": [
                "Notebook Dell",
                "Mouse Logitech",
            ],
            "categoria": [
                "Informática",
                "Informática",
            ],
            "subcategoria": [
                "Notebook",
                "Mouse",
            ],
            "preco_venda": [
                3500.00,
                150.00,
            ],
            "preco_custo": [
                2800.00,
                90.00,
            ],
            "quantidade_estoque": [
                30,
                100,
            ],
        }
    )

    resultado = transform_dim_produto(df)

    assert resultado.columns.tolist() == [
        "id_produto",
        "nome_produto",
        "categoria",
        "subcategoria",
        "preco_venda",
        "preco_custo",
    ]


def test_transform_dim_produto_remove_duplicados():
    df = pd.DataFrame(
        {
            "id_produto": [1, 1, 2],
            "nome_produto": [
                "Notebook Dell",
                "Notebook Dell",
                "Mouse Logitech",
            ],
            "categoria": [
                "Informática",
                "Informática",
                "Informática",
            ],
            "subcategoria": [
                "Notebook",
                "Notebook",
                "Mouse",
            ],
            "preco_venda": [
                3500.00,
                3500.00,
                150.00,
            ],
            "preco_custo": [
                2800.00,
                2800.00,
                90.00,
            ],
        }
    )

    resultado = transform_dim_produto(df)

    assert len(resultado) == 2
    assert resultado["id_produto"].is_unique


def test_transform_dim_produto_ordena_por_id():
    df = pd.DataFrame(
        {
            "id_produto": [3, 1, 2],
            "nome_produto": [
                "Monitor",
                "Notebook",
                "Mouse",
            ],
            "categoria": [
                "Informática",
                "Informática",
                "Informática",
            ],
            "subcategoria": [
                "Monitor",
                "Notebook",
                "Mouse",
            ],
            "preco_venda": [
                900.00,
                3500.00,
                150.00,
            ],
            "preco_custo": [
                650.00,
                2800.00,
                90.00,
            ],
        }
    )

    resultado = transform_dim_produto(df)

    assert resultado["id_produto"].tolist() == [
        1,
        2,
        3,
    ]

