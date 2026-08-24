import pandas as pd

def transform_item_pedido(
df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()
    
    df["quantidade"] = pd.to_numeric(
        df["quantidade"],
        errors="raise",
    ).astype(int)

    df["preco_unitario"] = pd.to_numeric(
        df["preco_unitario"],
        errors="raise",
    )

    df["subtotal"] = pd.to_numeric(
        df["subtotal"],
        errors="raise",
    )

    return df
