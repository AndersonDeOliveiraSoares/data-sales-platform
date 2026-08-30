from sqlalchemy import text

from src.database.connection import engine


def get_sales_by_product():
    query = text(
        """
        SELECT
            id_produto,
            nome_produto,
            SUM(quantidade) AS quantidade_vendida,
            SUM(receita) AS receita,
            SUM(lucro) AS lucro
        FROM dw.fact_vendas
        GROUP BY
            id_produto,
            nome_produto
        ORDER BY receita DESC
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return result.mappings().all()


def get_sales_by_customer():
    query = text(
        """
        SELECT
            c.id_cliente,
            c.nome AS nome_cliente,
            SUM(f.quantidade) AS quantidade_vendida,
            SUM(f.subtotal) AS receita,
            SUM(
                f.subtotal -
                (f.quantidade * f.preco_custo)
            ) AS lucro
        FROM dw.fact_vendas f
        JOIN dw.dim_cliente c
            ON f.id_cliente = c.id_cliente
        GROUP BY
            c.id_cliente,
            c.nome
        ORDER BY receita DESC
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return result.mappings().all()

def get_sales_summary():
    query = text(
        """
        SELECT
            SUM(quantidade) AS quantidade_vendida,
            SUM(subtotal) AS receita_total,
            SUM(
                subtotal -
                (quantidade * preco_custo)
            ) AS lucro_total
        FROM dw.fact_vendas
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return result.mappings().one()

def get_sales_summary():
    query = text(
        """
        SELECT
            SUM(quantidade) AS quantidade_vendida,
            SUM(subtotal) AS receita_total,
            SUM(quantidade * preco_custo) AS custo_total,
            SUM(subtotal) - SUM(quantidade * preco_custo) AS lucro_total,
            ROUND(
                (
                    (SUM(subtotal) - SUM(quantidade * preco_custo))
                    / NULLIF(SUM(subtotal), 0)
                ) * 100,
                2
            ) AS margem
        FROM dw.fact_vendas
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return result.mappings().one()