import pandas as pd
import streamlit as st

from src.analytics.service import (
    get_sales_summary_service,
    get_sales_by_product_service,
    get_sales_by_customer_service,
    get_sales_by_month_service,
)


st.set_page_config(
    page_title="Data Sales Platform",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Data Sales Platform")
st.subheader("Visão Geral de Vendas")


# ============================================================
# FILTROS
# ============================================================

col_filtro1, col_filtro2 = st.columns(2)

with col_filtro1:
    ano = st.selectbox(
        "Ano",
        options=[2026],
        index=0,
    )

with col_filtro2:
    mes = st.selectbox(
        "Mês",
        options=list(range(1, 13)),
        index=7,
        format_func=lambda x: f"{x:02d}",
    )


# ============================================================
# RESUMO
# ============================================================

summary = get_sales_summary_service(
    ano=ano,
    mes=mes,
)


# ============================================================
# KPIs
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    quantidade = summary["quantidade_vendida"] or 0

    st.metric(
        "Quantidade Vendida",
        quantidade,
    )

with col2:
    receita = summary["receita_total"] or 0

    st.metric(
        "Receita",
        f"R$ {receita:,.2f}",
    )

with col3:
    lucro = summary["lucro_total"] or 0

    st.metric(
        "Lucro",
        f"R$ {lucro:,.2f}",
    )

with col4:
    margem = summary["margem"] or 0

    st.metric(
        "Margem",
        f"{margem:.2f}%",
    )


st.divider()


# ============================================================
# RANKING DE PRODUTOS
# ============================================================

st.subheader("🏆 Ranking de Produtos")


produtos = get_sales_by_product_service(
    ano=ano,
    mes=mes,
)


if produtos:
    df_produtos = pd.DataFrame(produtos)

    st.dataframe(
        df_produtos,
        use_container_width=True,
    )

    st.subheader("💰 Receita por Produto")

    st.bar_chart(
        df_produtos.set_index("nome_produto")["receita"]
    )

else:
    st.info(
        f"Nenhuma venda encontrada para {mes:02d}/{ano}."
    )


st.divider()


# ============================================================
# RANKING DE CLIENTES
# ============================================================

st.subheader("👥 Ranking de Clientes")


clientes = get_sales_by_customer_service(
    ano=ano,
    mes=mes,
)


if clientes:
    df_clientes = pd.DataFrame(clientes)

    st.dataframe(
        df_clientes,
        use_container_width=True,
    )

    st.subheader("💰 Receita por Cliente")

    st.bar_chart(
        df_clientes.set_index("nome_cliente")["receita"]
    )

else:
    st.info(
        f"Nenhuma venda encontrada para {mes:02d}/{ano}."
    )


st.divider()


# ============================================================
# EVOLUÇÃO MENSAL
# ============================================================

st.subheader("📈 Evolução Mensal de Vendas")


vendas_mensais = get_sales_by_month_service()

df_mensal = pd.DataFrame(vendas_mensais)


if not df_mensal.empty:
    df_mensal["periodo"] = (
        df_mensal["ano"].astype(str)
        + "-"
        + df_mensal["mes"].astype(str).str.zfill(2)
    )

    st.line_chart(
        df_mensal.set_index("periodo")["receita"]
    )

else:
    st.info(
        "Não existem dados mensais disponíveis."
    )