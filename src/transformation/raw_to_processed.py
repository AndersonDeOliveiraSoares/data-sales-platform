from pathlib import Path
from src.transformation.cliente_transformation import (
    transform_cliente,
)
from src.transformation.produto_transformation import (
transform_produto,
)
from src.transformation.pedido_transformation import (
transform_pedido,
)
from src.transformation.item_pedido_transformation import (
transform_item_pedido,
)
from src.utils.logger import get_logger
import pandas as pd

logger = get_logger("transformation")




RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


TABLES = [
    "cliente",
    "produto",
    "pedido",
    "item_pedido",
]


def read_raw_table(
    table_name: str,
) -> pd.DataFrame:

    file_path = RAW_DIR / f"{table_name}.parquet"

    return pd.read_parquet(file_path)


def save_processed_table(
    df: pd.DataFrame,
    table_name: str,
) -> None:

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        PROCESSED_DIR / f"{table_name}.parquet"
    )

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
    total_records = 0
    for table_name in TABLES:
        df = read_raw_table(table_name)

        if table_name == "cliente":
            df = transform_cliente(df)
        elif table_name == "produto":
            df = transform_produto(df)
        elif table_name == "pedido":
            df = transform_pedido(df)
        elif table_name == "item_pedido":
            df = transform_item_pedido(df)

        save_processed_table(
            df,
            table_name,
        )
        total_records += len(df)
        logger.info("Transformation concluída | records=%d", total_records, )
        return total_records


if __name__ == "__main__":
    run()