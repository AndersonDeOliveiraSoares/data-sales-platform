from pathlib import Path

import pandas as pd

from src.pipeline import run

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")

EXPECTED_RAW = {
"cliente.parquet": 10,
"produto.parquet": 20,
"pedido.parquet": 15,
"item_pedido.parquet": 30,
}

EXPECTED_PROCESSED = {
"cliente.parquet": 10,
"produto.parquet": 20,
"pedido.parquet": 15,
"item_pedido.parquet": 30,
}

EXPECTED_WAREHOUSE = {
"dim_cliente.parquet": 10,
"dim_produto.parquet": 20,
"dim_data.parquet": 15,
"fact_vendas.parquet": 30,
}

def test_pipeline_integration():

    run()

    for file_name, expected_records in EXPECTED_RAW.items():

        file_path = RAW_DIR / file_name

        assert file_path.exists(), (
            f"Arquivo RAW não foi gerado: {file_path}"
        )

        df = pd.read_parquet(file_path)

        assert len(df) == expected_records, (
            f"{file_name}: esperado {expected_records} "
            f"registros, encontrado {len(df)}"
        )

    for file_name, expected_records in EXPECTED_PROCESSED.items():

        file_path = PROCESSED_DIR / file_name

        assert file_path.exists(), (
            f"Arquivo PROCESSED não foi gerado: {file_path}"
        )

        df = pd.read_parquet(file_path)

        assert len(df) == expected_records, (
            f"{file_name}: esperado {expected_records} "
            f"registros, encontrado {len(df)}"
        )

    for file_name, expected_records in EXPECTED_WAREHOUSE.items():

        file_path = WAREHOUSE_DIR / file_name

        assert file_path.exists(), (
            f"Arquivo WAREHOUSE não foi gerado: {file_path}"
        )

        df = pd.read_parquet(file_path)

        assert len(df) == expected_records, (
            f"{file_name}: esperado {expected_records} "
            f"registros, encontrado {len(df)}"
        )

    fact_vendas = pd.read_parquet(
        WAREHOUSE_DIR / "fact_vendas.parquet"
    )

    assert fact_vendas["id_cliente"].notna().all()
    assert fact_vendas["id_produto"].notna().all()
    assert fact_vendas["data"].notna().all()

    assert (fact_vendas["receita"] >= 0).all()
    assert (fact_vendas["custo_total"] >= 0).all()

    assert fact_vendas["margem"].notna().all()

