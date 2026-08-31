from sqlalchemy import text

from src.database.connection import engine


def get_sales_by_product(
    ano: int | None = None,
    mes: int | None = None,
):
    query = text(
        """
        SELECT
            id_produto,
            nome_produto,
            SUM(quantidade) AS quantidade_vendida,
            SUM(subtotal) AS receita,
            SUM(
                subtotal -
                (quantidade * preco_custo)
            ) AS lucro
        FROM dw.fact_vendas
        WHERE
            (:ano IS NULL OR ano = :ano)
            AND
            (:mes IS NULL OR mes = :mes)
        GROUP BY
            id_produto,
            nome_produto
        ORDER BY receita DESC
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "ano": ano,
                "mes": mes,
            },
        )

        return result.mappings().all()


def get_sales_by_customer(
    ano: int | None = None,
    mes: int | None = None,
):
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
        WHERE
            (:ano IS NULL OR f.ano = :ano)
            AND
            (:mes IS NULL OR f.mes = :mes)
        GROUP BY
            c.id_cliente,
            c.nome
        ORDER BY receita DESC
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "ano": ano,
                "mes": mes,
            },
        )

        return result.mappings().all()


def get_sales_summary(
    ano: int | None = None,
    mes: int | None = None,
):
    query = text(
        """
        SELECT
            SUM(quantidade) AS quantidade_vendida,
            SUM(subtotal) AS receita_total,
            SUM(quantidade * preco_custo) AS custo_total,
            SUM(subtotal)
                - SUM(quantidade * preco_custo)
                AS lucro_total,
            ROUND(
                (
                    (
                        SUM(subtotal)
                        - SUM(quantidade * preco_custo)
                    )
                    / NULLIF(SUM(subtotal), 0)
                ) * 100,
                2
            ) AS margem
        FROM dw.fact_vendas
        WHERE
            (:ano IS NULL OR ano = :ano)
            AND
            (:mes IS NULL OR mes = :mes)
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "ano": ano,
                "mes": mes,
            },
        )

        return result.mappings().one()


def get_sales_by_month():
    query = text(
        """
        SELECT
            ano,
            mes,
            SUM(quantidade) AS quantidade_vendida,
            SUM(subtotal) AS receita,
            SUM(quantidade * preco_custo) AS custo,
            SUM(subtotal)
                - SUM(quantidade * preco_custo)
                AS lucro
        FROM dw.fact_vendas
        GROUP BY
            ano,
            mes
        ORDER BY
            ano,
            mes
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return result.mappings().all()

def get_available_years():
    query = text(
        """
        SELECT DISTINCT
            ano
        FROM dw.fact_vendas
        WHERE ano IS NOT NULL
        ORDER BY ano DESC
        """
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            row["ano"]
            for row in result.mappings().all()
        ]