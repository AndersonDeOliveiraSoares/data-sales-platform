WITH vendas_diarias AS (
    SELECT
        f.data,
        SUM(f.receita) AS receita,
        SUM(f.lucro) AS lucro
    FROM dw.fact_vendas f
    GROUP BY
        f.data
)

SELECT
    data,
    receita,
    lucro,
    SUM(receita) OVER (
        ORDER BY data
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS receita_acumulada,
    SUM(lucro) OVER (
        ORDER BY data
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS lucro_acumulado
FROM vendas_diarias
ORDER BY data;