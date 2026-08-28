WITH vendas_produto AS (
    SELECT
        categoria,
        id_produto,
        nome_produto,
        SUM(quantidade) AS quantidade_vendida,
        SUM(receita) AS receita,
        SUM(lucro) AS lucro
    FROM dw.fact_vendas
    GROUP BY
        categoria,
        id_produto,
        nome_produto
),

ranking AS (
    SELECT
        categoria,
        id_produto,
        nome_produto,
        quantidade_vendida,
        receita,
        lucro,
        ROW_NUMBER() OVER (
            PARTITION BY categoria
            ORDER BY receita DESC
        ) AS posicao
    FROM vendas_produto
)

SELECT
    categoria,
    id_produto,
    nome_produto,
    quantidade_vendida,
    receita,
    lucro
FROM ranking
WHERE posicao = 1
ORDER BY categoria;