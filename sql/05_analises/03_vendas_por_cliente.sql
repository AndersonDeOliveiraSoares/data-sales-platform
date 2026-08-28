SELECT
    id_cliente,
    nome,
    cidade,
    estado,
    COUNT(DISTINCT id_pedido) AS quantidade_pedidos,
    SUM(quantidade) AS quantidade_itens,
    SUM(receita) AS receita,
    SUM(custo_total) AS custo_total,
    SUM(lucro) AS lucro,
    ROUND(
        SUM(lucro) / NULLIF(SUM(receita), 0),
        4
    ) AS margem
FROM dw.fact_vendas
GROUP BY
    id_cliente,
    nome,
    cidade,
    estado
ORDER BY
    receita DESC;