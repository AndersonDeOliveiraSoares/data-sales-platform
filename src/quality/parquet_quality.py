from pathlib import Path

import pandas as pd
from src.utils.logger import get_logger

logger = get_logger("quality")

RAW_DIR = Path("data/raw")


REQUIRED_COLUMNS = {
    "cliente": [
        "id_cliente",
        "nome",
        "cpf_cnpj",
        "email",
    ],
    "produto": [
        "id_produto",
        "nome_produto",
        "preco_venda",
        "preco_custo",
        "quantidade_estoque",
    ],
    "pedido": [
        "id_pedido",
        "id_cliente",
        "data_pedido",
        "valor_total",
        "valor_frete",
    ],
    "item_pedido": [
        "id_item_pedido",
        "id_pedido",
        "id_produto",
        "quantidade",
        "preco_unitario",
        "subtotal",
    ],
}


NON_NEGATIVE_COLUMNS = {
    "produto": [
        "preco_venda",
        "preco_custo",
        "quantidade_estoque",
    ],
    "pedido": [
        "valor_total",
        "valor_frete",
    ],
    "item_pedido": [
        "preco_unitario",
        "subtotal",
    ],
}


POSITIVE_COLUMNS = {
    "item_pedido": [
        "quantidade",
    ],
}


UNIQUE_COLUMNS = {
    "cliente": [
        "id_cliente",
        "cpf_cnpj",
        "email",
    ],
    "produto": [
        "id_produto",
    ],
    "pedido": [
        "id_pedido",
    ],
    "item_pedido": [
        "id_item_pedido",
    ],
}


def validate_required_columns(
    df: pd.DataFrame,
    table_name: str,
) -> None:

    required_columns = REQUIRED_COLUMNS[table_name]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{table_name}: "
            f"colunas obrigatórias ausentes: "
            f"{missing_columns}"
        )


def validate_not_null(
    df: pd.DataFrame,
    table_name: str,
) -> None:

    required_columns = REQUIRED_COLUMNS[table_name]

    null_columns = [
        column
        for column in required_columns
        if df[column].isnull().any()
    ]

    if null_columns:
        raise ValueError(
            f"{table_name}: "
            f"colunas obrigatórias possuem valores nulos: "
            f"{null_columns}"
        )


def validate_non_negative(
    df: pd.DataFrame,
    table_name: str,
    columns: list[str],
) -> None:

    invalid_columns = [
        column
        for column in columns
        if (df[column] < 0).any()
    ]

    if invalid_columns:
        raise ValueError(
            f"{table_name}: "
            f"valores negativos encontrados em: "
            f"{invalid_columns}"
        )


def validate_positive(
    df: pd.DataFrame,
    table_name: str,
    columns: list[str],
) -> None:

    invalid_columns = [
        column
        for column in columns
        if (df[column] <= 0).any()
    ]

    if invalid_columns:
        raise ValueError(
            f"{table_name}: "
            f"valores devem ser maiores que zero em: "
            f"{invalid_columns}"
        )


def validate_duplicates(
    df: pd.DataFrame,
    table_name: str,
    columns: list[str],
) -> None:

    invalid_columns = [
        column
        for column in columns
        if df[column].duplicated().any()
    ]

    if invalid_columns:
        raise ValueError(
            f"{table_name}: "
            f"valores duplicados encontrados em: "
            f"{invalid_columns}"
        )


def validate_table(
table_name: str,
) -> int:

    file_path = (
        RAW_DIR / f"{table_name}.parquet"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {file_path}"
        )

    df = pd.read_parquet(file_path)

    validate_required_columns(
        df,
        table_name,
    )

    validate_not_null(
        df,
        table_name,
    )

    if table_name in NON_NEGATIVE_COLUMNS:

        validate_non_negative(
            df,
            table_name,
            NON_NEGATIVE_COLUMNS[table_name],
        )

    if table_name in POSITIVE_COLUMNS:

        validate_positive(
            df,
            table_name,
            POSITIVE_COLUMNS[table_name],
        )

    if table_name in UNIQUE_COLUMNS:

        validate_duplicates(
            df,
            table_name,
            UNIQUE_COLUMNS[table_name],
        )

    records = len(df)

    logger.info(
        "%s: OK | records=%d",
        table_name,
        records,
    )

    return records

def run() -> int:

    total_records = 0

    for table_name in REQUIRED_COLUMNS:

        records = validate_table(
            table_name,
        )

        total_records += records

    logger.info(
        "Data Quality concluída | "
        "records=%d",
        total_records,
    )

    return total_records


if __name__ == "__main__":
    run()
