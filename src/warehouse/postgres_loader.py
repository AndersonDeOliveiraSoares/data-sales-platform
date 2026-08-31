from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.database.connection import engine
from src.utils.logger import get_logger

logger = get_logger("warehouse")

WAREHOUSE_DIR = Path("data/warehouse")

TABLES = [
"dim_cliente",
"dim_produto",
"dim_data",
"fact_vendas",
]

def read_warehouse_table(
    table_name: str,
    ) -> pd.DataFrame:

    file_path = (
        WAREHOUSE_DIR
        / f"{table_name}.parquet"
    )

    return pd.read_parquet(file_path)


def load_table(
    df: pd.DataFrame,
    table_name: str,
    ) -> None:

    with engine.begin() as connection:

        connection.execute(
            text(
                f'TRUNCATE TABLE '
                f'"dw"."{table_name}" '
                f'RESTART IDENTITY CASCADE'
            )
        )

        df.to_sql(
            table_name,
            connection,
            schema="dw",
            if_exists="append",
            index=False,
        )

    logger.info(
        "%s carregada no PostgreSQL | records=%d",
        table_name,
        len(df),
    )


def run() -> int:

    total_records = 0

    for table_name in TABLES:

        df = read_warehouse_table(
            table_name
        )

        load_table(
            df,
            table_name,
        )

        total_records += len(df)

    logger.info(
        "PostgreSQL DW carregado | records=%d",
        total_records,
    )

    return total_records
