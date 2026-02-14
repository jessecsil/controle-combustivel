import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Abastece 2026")
st.title("⛽ Controle de Combustível")

ARQUIVO = "dados.csv"

# Cria CSV se não existir
if not os.path.exists(ARQUIVO):
    pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL']).to_csv(ARQUIVO, index=False)

# FORMULÁRIO DE CADASTRO
with st.form("meu_form", clear_on_submit=True):
    data_input = st.date_input("Data", datetime.now())
    v_gnv = st.number_input("GNV (R$)")
    v_gas = st.number_input("Gasolina (R$)")
    submit = st.form_submit_button("SALVAR")

    if submit:
        total = v_gnv + v_gas
        data_formatada = data_input.strftime("%d/%m/%Y")

        df_novo = pd.DataFrame([{
            "DATA": data_formatada,
            "GNV": v_gnv,
            "GAS": v_gas,
            "TOTAL": total
        }])

        df_novo.to_csv(ARQUIVO, mode="a", header=False, index=False)
        st.success("Salvo com sucesso!")

st.divider()

# BOTÃO PARA LIMPAR DADOS
if st.button("🗑️ Apagar todos os dados"):
    if os.path.exists(ARQUIVO):
        os.remove(ARQUIVO)
        st.success("Dados apagados com sucesso!")
        st.experimental_rerun()

# EXIBIÇÃO DOS DADOS
if os.path.exists(ARQUIVO):
    df_view = pd.read_csv(ARQUIVO, dtype=str)

    # Converte DATA para datetime para filtros e gráficos
    df_view["DATA"] = pd.to_datetime(df_view["DATA"], dayfirst=True)

    # Ordena do mais recente para o mais antigo
    df_view = df_view.sort_values(by="DATA", ascending=False)

    # FILTRO POR PERÍODO
    st.subheader("Filtrar por período")
    min_date = df_view["DATA"].min()
    max_date = df_view["DATA"].max()
    start_date = st.date_input("De", min_date)
    end_date = st.date_input("Até", max_date)

    df_filtrado = df_view[(df_view["DATA"] >= pd.to_datetime(start_date)) &
                          (df_view["DATA"] <= pd.to_datetime(end_date))]

    # Cria coluna apenas para exibição da data sem hora
    df_filtrado["DATA_EXIB"] = df_filtrado["DATA"].dt.strftime("%d/%m/%Y")

    # Formata colunas monetárias para exibição
    df_exibir = df_filtrado.copy()
    for col in ["GNV", "GAS", "TOTAL"]:
        df_exibir[col] = df_exibir[col].astype(float).apply(lambda x: f"R$ {x:.2f}")

    # Exibe tabela apenas com DATA_EXIB
    st.subheader("Registros Salvos")
    st.dataframe(df_exibir[["DATA_EXIB", "GNV", "GAS", "TOTAL"]].rename(columns={"DATA_EXIB":"DATA"}))

    # TOTAL ACUMULADO
    total_gnv = df_filtrado["GNV"].astype(float).sum()
    total_gas = df_filtrado["GAS"].astype(float).sum()
    total_geral = df_filtrado["TOTAL"].astype(float).sum()

    st.subheader("Totais")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total GNV", f"R$ {total_gnv:.2f}")
    col2.metric("Total Gasolina", f"R$ {total_gas:.2f}")
    col3.metric("Total Geral", f"R$ {total_geral:.2f}")

    # GRÁFICO MENSAL DENTRO DE UM EXPANDER
    with st.expander("📊 Mostrar gráfico de gastos mensais"):
        df_view["GNV_NUM"] = df_view["GNV"].astype(float)
        df_view["GAS_NUM"] = df_view["GAS"].astype(float)
        df_view["MES"] = df_view["DATA"].dt.to_period("M")
        df_grafico = df_view.groupby("MES")[["GNV_NUM", "GAS_NUM"]].sum()
        df_grafico.rename(columns={"GNV_NUM":"GNV", "GAS_NUM":"Gasolina"}, inplace=True)
        df_grafico.index = df_grafico.index.astype(str)
        st.bar_chart(df_grafico)
