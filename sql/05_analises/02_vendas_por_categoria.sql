SELECT
    categoria,
    SUM(quantidade) AS quantidade_vendida,
    SUM(receita) AS receita,
    SUM(custo_total) AS custo_total,
    SUM(lucro) AS lucro,
    ROUND(
        SUM(lucro) / NULLIF(SUM(receita), 0),
        4
    ) AS margem
FROM dw.fact_vendas
GROUP BY
    categoria
ORDER BY
    receita DESC;