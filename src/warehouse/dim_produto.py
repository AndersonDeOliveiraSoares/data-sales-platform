from pathlib import Path
from src.utils.logger import get_logger
import pandas as pd


logger = get_logger("warehouse")

PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")

COLUMNS = [
"id_produto",
"nome_produto",
"categoria",
"subcategoria",
"preco_venda",
"preco_custo",
]

def read_processed_produto() -> pd.DataFrame:
    file_path = (
        PROCESSED_DIR / "produto.parquet"
    )

    return pd.read_parquet(file_path)

def transform_dim_produto(
    df: pd.DataFrame,
    ) -> pd.DataFrame:


    dim_produto = df[COLUMNS].copy()

    dim_produto = dim_produto.drop_duplicates(
        subset=["id_produto"]
    )

    dim_produto = dim_produto.sort_values(
        "id_produto"
    ).reset_index(drop=True)

    return dim_produto

def save_dim_produto(
    df: pd.DataFrame,
    ) -> None:

    WAREHOUSE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        WAREHOUSE_DIR / "dim_produto.parquet"
    )

    df.to_parquet(
        output_file,
        index=False,
    )

    logger.info(
        "dim_produto: %s registros -> %s",
        len(df),
        output_file,
    )

def run() -> None:
    df = read_processed_produto()

    dim_produto = transform_dim_produto(df)

    save_dim_produto(dim_produto)

    records = len(dim_produto)
    logger.info("Dimensão Produto concluída | records=%d", records, )
    return records


if __name__ == "__main__":
    run()
