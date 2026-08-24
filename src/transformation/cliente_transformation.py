import pandas as pd

def transform_cliente(
    df: pd.DataFrame,
    ) -> pd.DataFrame:

    df = df.copy()

    df["nome"] = (
        df["nome"]
        .astype(str)
        .str.strip()
    )

    df["cpf_cnpj"] = (
        df["cpf_cnpj"]
        .astype(str)
        .str.strip()
    )

    df["email"] = (
        df["email"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["telefone"] = (
        df["telefone"]
        .astype(str)
        .str.strip()
    )

    df["endereco"] = (
        df["endereco"]
        .astype(str)
        .str.strip()
    )

    df["cidade"] = (
        df["cidade"]
        .astype(str)
        .str.strip()
    )

    df["estado"] = (
        df["estado"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["cep"] = (
        df["cep"]
        .astype(str)
        .str.strip()
    )

    return df

