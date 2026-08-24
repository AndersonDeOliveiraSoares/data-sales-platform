from pathlib import Path
from src.utils.logger import get_logger
import pandas as pd


logger = get_logger("warehouse")

PROCESSED_DIR = Path("data/processed")
WAREHOUSE_DIR = Path("data/warehouse")


def read_processed_pedido() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "pedido.parquet"

    return pd.read_parquet(file_path)


def transform_dim_data(
    df: pd.DataFrame,
) -> pd.DataFrame:

    datas = pd.to_datetime(
        df["data_pedido"]
    ).dt.normalize()

    dim_data = pd.DataFrame(
        {
            "data": datas.drop_duplicates()
        }
    )

    dim_data["ano"] = dim_data["data"].dt.year
    dim_data["mes"] = dim_data["data"].dt.month
    dim_data["nome_mes"] = dim_data["data"].dt.month_name()
    dim_data["trimestre"] = dim_data["data"].dt.quarter
    dim_data["dia"] = dim_data["data"].dt.day
    dim_data["dia_semana"] = dim_data["data"].dt.dayofweek + 1
    dim_data["nome_dia_semana"] = (
        dim_data["data"].dt.day_name()
    )
    dim_data = dim_data.sort_values(
        "data"
    ).reset_index(drop=True)
    return dim_data


def save_dim_data(
    df: pd.DataFrame,
) -> None:

    WAREHOUSE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    output_file = (
        WAREHOUSE_DIR / "dim_data.parquet"
    )
    df.to_parquet(
        output_file,
        index=False,
    )
    logger.info(
        "dim_data: %s registros -> %s",
        len(df),
        output_file,
    )

def run() -> None:

    df = read_processed_pedido()
    dim_data = transform_dim_data(df)
    save_dim_data(dim_data)


if __name__ == "__main__":
    run()