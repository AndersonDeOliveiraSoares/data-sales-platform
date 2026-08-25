from pathlib import Path

import pandas as pd
import pytest

from src.pipeline import run

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")

@pytest.fixture(scope="module")
def pipeline():
    print("\n=== PIPELINE FIXTURE ===")
    print("Executando pipeline...")

    run()

    print("\n=== PARQUETS APOS PIPELINE ===")

    for file_name in [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]:
        file_path = RAW_DIR / file_name

        if file_path.exists():
            df = pd.read_parquet(file_path)
            print(f"{file_path}: {len(df)} registros")
        else:
            print(f"{file_path}: NAO EXISTE")

    for file_name in [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]:
        file_path = PROCESSED_DIR / file_name

        if file_path.exists():
            df = pd.read_parquet(file_path)
            print(f"{file_path}: {len(df)} registros")
        else:
            print(f"{file_path}: NAO EXISTE")

    for file_name in [
        "dim_cliente.parquet",
        "dim_produto.parquet",
        "dim_data.parquet",
        "fact_vendas.parquet",
    ]:
        file_path = WAREHOUSE_DIR / file_name

        if file_path.exists():
            df = pd.read_parquet(file_path)
            print(f"{file_path}: {len(df)} registros")
        else:
            print(f"{file_path}: NAO EXISTE")

def test_raw_files_exist(pipeline):
    expected_files = [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]

    for file_name in expected_files:
        file_path = RAW_DIR / file_name

        assert file_path.exists()

def test_processed_files_exist(pipeline):

    expected_files = [
        "cliente.parquet",
        "produto.parquet",
        "pedido.parquet",
        "item_pedido.parquet",
    ]

    for file_name in expected_files:
        file_path = PROCESSED_DIR / file_name

        assert file_path.exists()

def test_warehouse_files_exist(pipeline):

    expected_files = [
        "dim_cliente.parquet",
        "dim_produto.parquet",
        "dim_data.parquet",
        "fact_vendas.parquet",
    ]

    for file_name in expected_files:
        file_path = WAREHOUSE_DIR / file_name

        assert file_path.exists()

def test_raw_record_counts(pipeline):

    print("\n=== TESTE RAW RECORD COUNTS ===")

    expected_counts = {
        "cliente": 10,
        "produto": 20,
        "pedido": 15,
        "item_pedido": 30,
    }

    for table_name, expected_count in expected_counts.items():

        file_path = RAW_DIR / f"{table_name}.parquet"

        df = pd.read_parquet(file_path)

        print(
            f"{file_path}: "
            f"{len(df)} registros "
            f"(esperado: {expected_count})"
        )

        assert len(df) == expected_count

def test_processed_record_counts(pipeline):
    print("\n=== TESTE PROCESSED RECORD COUNTS ===")

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

        print(
            f"{file_path}: "
            f"{len(df)} registros "
            f"(esperado: {expected_count})"
        )

        assert len(df) == expected_count

def test_warehouse_record_counts(pipeline):
    print("\n=== TESTE WAREHOUSE RECORD COUNTS ===")

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

        print(
            f"{file_path}: "
            f"{len(df)} registros "
            f"(esperado: {expected_count})"
        )

        assert len(df) == expected_count


def test_fact_vendas_relationships(pipeline):
    print("\n=== TESTE FACT VENDAS RELATIONSHIPS ===")

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

    print(
        f"fact_vendas: {len(fact_vendas)} registros"
    )

    print(
        f"dim_cliente: {len(dim_cliente)} registros"
    )

    print(
        f"dim_produto: {len(dim_produto)} registros"
    )

    print(
        f"dim_data: {len(dim_data)} registros"
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

