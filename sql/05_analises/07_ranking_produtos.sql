WITH vendas_produto AS (
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
)

SELECT
    RANK() OVER (
        ORDER BY receita DESC
    ) AS ranking,
    id_produto,
    nome_produto,
    quantidade_vendida,
    receita,
    lucro
FROM vendas_produto
ORDER BY ranking;