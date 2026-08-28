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