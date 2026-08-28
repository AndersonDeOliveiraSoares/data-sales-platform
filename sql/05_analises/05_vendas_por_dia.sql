SELECT
    f.data,
    d.ano,
    d.mes,
    d.dia,
    d.dia_semana,
    d.nome_dia_semana,
    SUM(f.quantidade) AS quantidade_vendida,
    SUM(f.receita) AS receita,
    SUM(f.custo_total) AS custo_total,
    SUM(f.lucro) AS lucro,
    ROUND(
        SUM(f.lucro) / NULLIF(SUM(f.receita), 0),
        4
    ) AS margem
FROM dw.fact_vendas f
INNER JOIN dw.dim_data d
    ON f.data = d.data
GROUP BY
    f.data,
    d.ano,
    d.mes,
    d.dia,
    d.dia_semana,
    d.nome_dia_semana
ORDER BY
    f.data;