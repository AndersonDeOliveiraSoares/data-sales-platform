from pathlib import Path

import pandas as pd

from src.pipeline import run


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")


def test_pipeline_integration():

    run()
    print("\n=== PARQUET APÓS RUN() NO TESTE DE INTEGRAÇÃO ===")

    for file_name in [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]:
        file_path = RAW_DIR / file_name

        df = pd.read_parquet(file_path)

        print(
            f"{file_path}: {len(df)} registros"
        )

    fact_vendas = pd.read_parquet(
        WAREHOUSE_DIR / "fact_vendas.parquet"
    )

    print(
        f"fact_vendas: {len(fact_vendas)} registros"
    )

    expected_raw_files = [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]

    expected_processed_files = [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]

    expected_warehouse_files = [
        "dim_cliente.parquet",
        "dim_produto.parquet",
        "dim_data.parquet",
        "fact_vendas.parquet",
    ]

    for file_name in expected_raw_files:
        assert (
            RAW_DIR / file_name
        ).exists()

    for file_name in expected_processed_files:
        assert (
            PROCESSED_DIR / file_name
        ).exists()

    for file_name in expected_warehouse_files:
        assert (
            WAREHOUSE_DIR / file_name
        ).exists()

    fact_vendas = pd.read_parquet(
        WAREHOUSE_DIR / "fact_vendas.parquet"
    )

    assert len(fact_vendas) == 30

    assert fact_vendas["id_cliente"].notna().all()
    assert fact_vendas["id_produto"].notna().all()
    assert fact_vendas["data"].notna().all()

    assert (fact_vendas["receita"] >= 0).all()
    assert (fact_vendas["custo_total"] >= 0).all()

    assert fact_vendas["margem"].notna().all()