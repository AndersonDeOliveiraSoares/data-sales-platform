import pandas as pd

from src.warehouse.dim_cliente import transform_dim_cliente

def test_transform_dim_cliente_colunas():
    df = pd.DataFrame(
        {
            "id_cliente": [2, 1],
            "nome": ["Maria", "Anderson"],
            "cidade": ["Niterói", "Rio de Janeiro"],
            "estado": ["RJ", "RJ"],
            "email": [
                "maria@email.com",
                "anderson@email.com",
            ],
        }
    )

    resultado = transform_dim_cliente(df)

    assert resultado.columns.tolist() == [
        "id_cliente",
        "nome",
        "cidade",
        "estado",
    ]


def test_transform_dim_cliente_remove_duplicados():

    df = pd.DataFrame(
        {
            "id_cliente": [1, 1, 2],
            "nome": [
                "Anderson",
                "Anderson",
                "Maria",
            ],
            "cidade": [
                "Rio de Janeiro",
                "Rio de Janeiro",
                "Niterói",
            ],
            "estado": ["RJ", "RJ", "RJ"],
        }
    )

    resultado = transform_dim_cliente(df)

    assert len(resultado) == 2
    assert resultado["id_cliente"].is_unique

def test_transform_dim_cliente_ordena_por_id():

    df = pd.DataFrame(
        {
            "id_cliente": [3, 1, 2],
            "nome": [
                "Carlos",
                "Anderson",
                "Maria",
            ],
            "cidade": [
                "Rio de Janeiro",
                "Rio de Janeiro",
                "Niterói",
            ],
            "estado": ["RJ", "RJ", "RJ"],
        }
    )

    resultado = transform_dim_cliente(df)

    assert resultado["id_cliente"].tolist() == [
        1,
        2,
        3,
    ]
