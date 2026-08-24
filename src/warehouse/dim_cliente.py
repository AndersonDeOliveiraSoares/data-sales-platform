from pathlib import Path
from src.utils.logger import get_logger
import pandas as pd


logger = get_logger("warehouse")
PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")

COLUMNS = [
"id_cliente",
"nome",
"cidade",
"estado",
]

def read_processed_cliente() -> pd.DataFrame:

    file_path = (
        PROCESSED_DIR / "cliente.parquet"
    )

    return pd.read_parquet(file_path)

def transform_dim_cliente(
df: pd.DataFrame,
) -> pd.DataFrame:

    dim_cliente = df[COLUMNS].copy()

    dim_cliente = dim_cliente.drop_duplicates(
        subset=["id_cliente"]
    )

    dim_cliente = dim_cliente.sort_values(
        "id_cliente"
    ).reset_index(drop=True)

    return dim_cliente


def save_dim_cliente(
    df: pd.DataFrame,
    ) -> None:


    WAREHOUSE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        WAREHOUSE_DIR / "dim_cliente.parquet"
    )

    df.to_parquet(
        output_file,
        index=False,
    )

    logger.info(
        "dim_cliente: %s registros -> %s",
        len(df),
        output_file,
    )


def run() -> None:

    df = read_processed_cliente()

    dim_cliente = transform_dim_cliente(df)

    save_dim_cliente(dim_cliente)

if __name__ == "__main__":
    run()
