import pandas as pd


def calculate_sales_indicators(
    fact_vendas: pd.DataFrame,
) -> dict:

    receita_total = fact_vendas["receita"].sum()

    custo_total = fact_vendas["custo_total"].sum()

    lucro_total = fact_vendas["lucro"].sum()

    quantidade_vendida = fact_vendas["quantidade"].sum()

    margem = (
        lucro_total / receita_total
        if receita_total > 0
        else 0
    )

    quantidade_pedidos = fact_vendas[
        "id_pedido"
    ].nunique()

    ticket_medio = (
        receita_total / quantidade_pedidos
        if quantidade_pedidos > 0
        else 0
    )

    return {
        "receita_total": receita_total,
        "custo_total": custo_total,
        "lucro_total": lucro_total,
        "quantidade_vendida": quantidade_vendida,
        "margem": margem,
        "ticket_medio": ticket_medio,
    }