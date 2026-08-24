from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")


def test_raw_files_exist():

    expected_files = [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]

    for file_name in expected_files:
        file_path = RAW_DIR / file_name

        assert file_path.exists()


def test_processed_files_exist():

    expected_files = [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]

    for file_name in expected_files:
        file_path = PROCESSED_DIR / file_name

        assert file_path.exists()


def test_warehouse_files_exist():

    expected_files = [
        "dim_cliente.parquet",
        "dim_produto.parquet",
        "dim_data.parquet",
        "fact_vendas.parquet",
    ]

    for file_name in expected_files:
        file_path = WAREHOUSE_DIR / file_name

        assert file_path.exists()


def test_raw_record_counts():

    expected_counts = {
        "cliente": 10,
        "produto": 20,
        "pedido": 15,
        "item_pedido": 30,
    }

    for table_name, expected_count in expected_counts.items():

        file_path = RAW_DIR / f"{table_name}.parquet"

        df = pd.read_parquet(file_path)

        assert len(df) == expected_count


def test_processed_record_counts():

    expected_counts = {
        "cliente": 10,
        "produto": 20,
        "pedido": 15,
        "item_pedido": 30,
    }

    for table_name, expected_count in expected_counts.items():

        file_path = (
            PROCESSED_DIR
            / f"{table_name}.parquet"
        )

        df = pd.read_parquet(file_path)

        assert len(df) == expected_count


def test_warehouse_record_counts():

    expected_counts = {
        "dim_cliente": 10,
        "dim_produto": 20,
        "dim_data": 15,
        "fact_vendas": 30,
    }

    for table_name, expected_count in expected_counts.items():

        file_path = (
            WAREHOUSE_DIR
            / f"{table_name}.parquet"
        )

        df = pd.read_parquet(file_path)

        assert len(df) == expected_count


def test_fact_vendas_relationships():

    fact_vendas = pd.read_parquet(
        WAREHOUSE_DIR / "fact_vendas.parquet"
    )

    dim_cliente = pd.read_parquet(
        WAREHOUSE_DIR / "dim_cliente.parquet"
    )

    dim_produto = pd.read_parquet(
        WAREHOUSE_DIR / "dim_produto.parquet"
    )

    dim_data = pd.read_parquet(
        WAREHOUSE_DIR / "dim_data.parquet"
    )

    assert fact_vendas["id_cliente"].isin(
        dim_cliente["id_cliente"]
    ).all()

    assert fact_vendas["id_produto"].isin(
        dim_produto["id_produto"]
    ).all()

    assert fact_vendas["data"].isin(
        dim_data["data"]
    ).all()