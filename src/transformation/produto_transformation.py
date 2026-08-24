import pandas as pd


def transform_produto(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    # Padroniza o nome do produto
    df["nome_produto"] = (
        df["nome_produto"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Padroniza categoria
    df["categoria"] = (
        df["categoria"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Padroniza subcategoria
    df["subcategoria"] = (
        df["subcategoria"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Garante tipos numéricos
    df["preco_venda"] = pd.to_numeric(
        df["preco_venda"],
        errors="coerce",
    )

    df["preco_custo"] = pd.to_numeric(
        df["preco_custo"],
        errors="coerce",
    )

    df["quantidade_estoque"] = pd.to_numeric(
        df["quantidade_estoque"],
        errors="coerce",
    ).astype("Int64")

    # Calcula margem bruta em valor
    df["margem_bruta"] = (
        df["preco_venda"]
        - df["preco_custo"]
    )

    # Calcula margem percentual
    df["margem_percentual"] = (
        df["margem_bruta"]
        / df["preco_venda"]
        * 100
    ).round(2)

    return df