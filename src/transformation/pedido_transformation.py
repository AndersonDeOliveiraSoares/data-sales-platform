import pandas as pd

def transform_pedido(df: pd.DataFrame,) -> pd.DataFrame:

    df = df.copy()

    df["data_pedido"] = pd.to_datetime(
        df["data_pedido"],
        errors="raise",
    )

    df["status_pedido"] = (
        df["status_pedido"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["forma_pagamento"] = (
        df["forma_pagamento"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["valor_total"] = pd.to_numeric(
        df["valor_total"],
        errors="raise",
    )

    df["valor_frete"] = pd.to_numeric(
        df["valor_frete"],
        errors="raise",
    )

    df["ano"] = df["data_pedido"].dt.year
    df["mes"] = df["data_pedido"].dt.month
    df["dia"] = df["data_pedido"].dt.day

    return df