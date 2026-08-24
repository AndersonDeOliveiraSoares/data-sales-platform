import pandas as pd
import pytest

from src.warehouse.fact_vendas import transform_fact_vendas

@pytest.fixture
def dados_fact_vendas():
    pedido = pd.DataFrame(
    {
    "id_pedido": [1, 2],
    "id_cliente": [1, 2],
    "data_pedido": [
    "2026-08-10 10:00:00",
    "2026-08-11 11:00:00",
    ],
    "valor_frete": [20.00, 25.00],
    "status_pedido": [
    "FINALIZADO",
    "ENVIADO",
    ],
    "forma_pagamento": [
    "PIX",
    "CARTAO",
    ],
    }
    )

    item_pedido = pd.DataFrame(
        {
            "id_item_pedido": [1, 2, 3],
            "id_pedido": [1, 1, 2],
            "id_produto": [1, 2, 1],
            "quantidade": [2, 1, 3],
            "preco_unitario": [
                100.00,
                50.00,
                100.00,
            ],
            "subtotal": [
                200.00,
                50.00,
                300.00,
            ],
        }
    )

    dim_cliente = pd.DataFrame(
        {
            "id_cliente": [1, 2],
            "nome": [
                "Anderson",
                "Maria",
            ],
            "cidade": [
                "Rio de Janeiro",
                "Niterói",
            ],
            "estado": [
                "RJ",
                "RJ",
            ],
        }
    )

    dim_produto = pd.DataFrame(
        {
            "id_produto": [1, 2],
            "nome_produto": [
                "Produto A",
                "Produto B",
            ],
            "categoria": [
                "Informática",
                "Informática",
            ],
            "subcategoria": [
                "Notebook",
                "Mouse",
            ],
            "preco_custo": [
                60.00,
                30.00,
            ],
        }
    )

    dim_data = pd.DataFrame(
        {
            "data": pd.to_datetime(
                [
                    "2026-08-10",
                    "2026-08-11",
                ]
            ),
            "ano": [2026, 2026],
            "mes": [8, 8],
            "trimestre": [3, 3],
            "dia": [10, 11],
        }
    )

    return (
        pedido,
        item_pedido,
        dim_cliente,
        dim_produto,
        dim_data,
    )


def test_transform_fact_vendas_quantidade_registros(
    dados_fact_vendas,
    ):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )
    assert len(fact_vendas) == 3


def test_transform_fact_vendas_colunas(
dados_fact_vendas,
):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )
    expected_columns = [
        "id_item_pedido",
        "id_pedido",
        "id_cliente",
        "id_produto",
        "data",
        "ano",
        "mes",
        "trimestre",
        "dia",
        "quantidade",
        "preco_unitario",
        "preco_custo",
        "subtotal",
        "custo_total",
        "receita",
        "lucro",
        "margem",
        "valor_frete",
        "status_pedido",
        "forma_pagamento",
        "nome",
        "cidade",
        "estado",
        "nome_produto",
        "categoria",
        "subcategoria",
    ]

    assert fact_vendas.columns.tolist() == expected_columns


def test_transform_fact_vendas_calcula_custo_total(
    dados_fact_vendas,
    ):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )


    assert fact_vendas.loc[
        fact_vendas["id_item_pedido"] == 1,
        "custo_total",
    ].iloc[0] == 120.00

def test_transform_fact_vendas_calcula_receita(
dados_fact_vendas,
):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )


    assert fact_vendas.loc[
        fact_vendas["id_item_pedido"] == 1,
        "receita",
    ].iloc[0] == 200.00


def test_transform_fact_vendas_calcula_lucro(
    dados_fact_vendas,
    ):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )
    assert fact_vendas.loc[
        fact_vendas["id_item_pedido"] == 1,
        "lucro",
    ].iloc[0] == 80.00

def test_transform_fact_vendas_calcula_margem(
    dados_fact_vendas,
    ):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )

    margem = fact_vendas.loc[
        fact_vendas["id_item_pedido"] == 1,
        "margem",
    ].iloc[0]

    assert margem == pytest.approx(0.40)

def test_transform_fact_vendas_data(
    dados_fact_vendas,
    ):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )
    data = fact_vendas.loc[
        fact_vendas["id_item_pedido"] == 1,
        "data",
    ].iloc[0]

    assert data == pd.Timestamp("2026-08-10")

def test_transform_fact_vendas_dimensoes(
    dados_fact_vendas,
    ):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )

    registro = fact_vendas[
        fact_vendas["id_item_pedido"] == 1
    ].iloc[0]

    assert registro["nome"] == "Anderson"
    assert registro["cidade"] == "Rio de Janeiro"
    assert registro["nome_produto"] == "Produto A"
    assert registro["categoria"] == "Informática"

def test_transform_fact_vendas_sem_nulos_nas_chaves(
    dados_fact_vendas,
    ):
    fact_vendas = transform_fact_vendas(
    pedido=dados_fact_vendas[0],
    item_pedido=dados_fact_vendas[1],
    dim_cliente=dados_fact_vendas[2],
    dim_produto=dados_fact_vendas[3],
    dim_data=dados_fact_vendas[4],
    )

    assert fact_vendas["id_pedido"].notna().all()
    assert fact_vendas["id_cliente"].notna().all()
    assert fact_vendas["id_produto"].notna().all()
    assert fact_vendas["data"].notna().all()
