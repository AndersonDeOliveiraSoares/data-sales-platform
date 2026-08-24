from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.database.connection import engine
from src.utils.logger import get_logger

logger = get_logger("ingestion")

RAW_DIR = Path("data/raw")


TABLES = [
    "cliente",
    "produto",
    "pedido",
    "item_pedido",
]


def extract_table(table_name: str) -> pd.DataFrame:
    query = text(f"SELECT * FROM {table_name}")

    with engine.connect() as connection:
        return pd.read_sql(query, connection)


def save_table_as_parquet(
    df: pd.DataFrame,
    table_name: str,
) -> None:

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = RAW_DIR / f"{table_name}.parquet"

    df.to_parquet(
        output_file,
        index=False,
    )

    logger.info(
        "%s: %s registros -> %s",
        table_name,
        len(df),
        output_file,
    )


def run() -> None:

    for table_name in TABLES:

        df = extract_table(table_name)

        save_table_as_parquet(
            df,
            table_name,
        )


if __name__ == "__main__":
    run()