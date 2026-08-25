from pathlib import Path

import pandas as pd
from src.utils.logger import get_logger

logger = get_logger("warehouse")
PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")

def read_processed_pedido() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "pedido.parquet"

    return pd.read_parquet(file_path)


def read_processed_item_pedido() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "item_pedido.parquet"
    return pd.read_parquet(file_path)

def read_dim_cliente() -> pd.DataFrame:
    file_path = WAREHOUSE_DIR / "dim_cliente.parquet"
    return pd.read_parquet(file_path)


def read_dim_produto() -> pd.DataFrame:
    file_path = WAREHOUSE_DIR / "dim_produto.parquet"
    return pd.read_parquet(file_path)


def read_dim_data() -> pd.DataFrame:
    file_path = WAREHOUSE_DIR / "dim_data.parquet"

    return pd.read_parquet(file_path)

def transform_fact_vendas(
    pedido: pd.DataFrame,
    item_pedido: pd.DataFrame,
    dim_cliente: pd.DataFrame,
    dim_produto: pd.DataFrame,
    dim_data: pd.DataFrame,
    ) -> pd.DataFrame:

    fact_vendas = item_pedido.merge(
        pedido[
            [
                "id_pedido",
                "id_cliente",
                "data_pedido",
                "valor_frete",
                "status_pedido",
                "forma_pagamento",
            ]
        ],
        on="id_pedido",
        how="inner",
    )

    fact_vendas["data"] = pd.to_datetime(
        fact_vendas["data_pedido"]
    ).dt.normalize()

    fact_vendas = fact_vendas.merge(
        dim_cliente[
            [
                "id_cliente",
                "nome",
                "cidade",
                "estado",
            ]
        ],
        on="id_cliente",
        how="left",
    )

    fact_vendas = fact_vendas.merge(
        dim_produto[
            [
                "id_produto",
                "nome_produto",
                "categoria",
                "subcategoria",
                "preco_custo",
            ]
        ],
        on="id_produto",
        how="left",
    )

    fact_vendas = fact_vendas.merge(
        dim_data[
            [
                "data",
                "ano",
                "mes",
                "trimestre",
                "dia",
            ]
        ],
        on="data",
        how="left",
    )

    fact_vendas["custo_total"] = (
        fact_vendas["preco_custo"]
        * fact_vendas["quantidade"]
    )

    fact_vendas["receita"] = (
        fact_vendas["subtotal"]
    )

    fact_vendas["lucro"] = (
        fact_vendas["receita"]
        - fact_vendas["custo_total"]
    )

    fact_vendas["margem"] = (
        fact_vendas["lucro"]
        / fact_vendas["receita"]
    )

    columns = [
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

    fact_vendas = fact_vendas[columns]

    fact_vendas = fact_vendas.sort_values(
        [
            "data",
            "id_pedido",
            "id_item_pedido",
        ]
    ).reset_index(drop=True)

    return fact_vendas

def save_fact_vendas(
    df: pd.DataFrame,
    ) -> None:

    WAREHOUSE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        WAREHOUSE_DIR / "fact_vendas.parquet"
    )

    df.to_parquet(
        output_file,
        index=False,
    )

    logger.info(
        "fact_vendas: %s registros -> %s",
        len(df),
        output_file,
    )


def run() -> None:
    pedido = read_processed_pedido()

    item_pedido = read_processed_item_pedido()

    dim_cliente = read_dim_cliente()

    dim_produto = read_dim_produto()

    dim_data = read_dim_data()

    fact_vendas = transform_fact_vendas(
        pedido=pedido,
        item_pedido=item_pedido,
        dim_cliente=dim_cliente,
        dim_produto=dim_produto,
        dim_data=dim_data,
    )

    save_fact_vendas(fact_vendas)

    records = len(fact_vendas)
    logger.info("Fact Vendas concluída | records=%d", records, )
    return records

if __name__ == "__main__":
    run()
