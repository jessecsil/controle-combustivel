import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ----------------------- Configuração da página -----------------------
st.set_page_config(page_title="⛽ Abastece 2026", layout="wide")
st.markdown("<h5 style='text-align:center;'>⛽ Controle de Combustível</h5>", unsafe_allow_html=True)


ARQUIVO = "dados.csv"

# ----------------------- Cria CSV se não existir -----------------------
if not os.path.exists(ARQUIVO):
    pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL']).to_csv(ARQUIVO, index=False)

# ----------------------- Formulário de cadastro -----------------------
with st.form("meu_form", clear_on_submit=True):
    st.subheader("📋 Registrar Abastecimento</h2>")
    data_input = st.date_input("Data", datetime.now())

    v_gnv_input = st.text_input("GNV (R$)", placeholder="Digite o valor")
    v_gas_input = st.text_input("Gasolina (R$)", placeholder="Digite o valor")

    # Converte para float ou assume 0
    v_gnv = float(v_gnv_input.replace(",", ".").strip()) if v_gnv_input.strip() != "" else 0.0
    v_gas = float(v_gas_input.replace(",", ".").strip()) if v_gas_input.strip() != "" else 0.0

    submit = st.form_submit_button("💾 SALVAR")
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
        st.success("✅ Salvo com sucesso!")

st.divider()

# ----------------------- Botão limpar dados -----------------------
if st.button("🗑️ Apagar todos os dados</h2>"):
    if os.path.exists(ARQUIVO):
        os.remove(ARQUIVO)
        st.success("✅ Dados apagados com sucesso!")
        st.stop()  # Interrompe execução para evitar erros

# ----------------------- Exibição dos dados -----------------------
if os.path.exists(ARQUIVO):
    df_view = pd.read_csv(ARQUIVO, dtype=str)
    if not df_view.empty:
        df_view["DATA"] = pd.to_datetime(df_view["DATA"], dayfirst=True)
        df_view = df_view.sort_values(by="DATA", ascending=False)
    else:
        df_view["DATA"] = pd.to_datetime([])

    # ----------------------- Filtrar por período -----------------------
    st.subheader("📅 Filtrar por período</h2>")
    if df_view.empty:
        min_date = datetime.now().date()
        max_date = datetime.now().date()
    else:
        min_date = df_view["DATA"].min().date()
        max_date = df_view["DATA"].max().date()

    start_date = st.date_input("De", min_date)
    end_date = st.date_input("Até", max_date)

    if not df_view.empty:
        df_filtrado = df_view[(df_view["DATA"] >= pd.to_datetime(start_date)) &
                              (df_view["DATA"] <= pd.to_datetime(end_date))]

        df_filtrado["DATA_EXIB"] = df_filtrado["DATA"].dt.strftime("%d/%m/%Y")

        # ----------------------- Preparar tabela -----------------------
        df_style = df_filtrado[["DATA_EXIB", "GNV", "GAS", "TOTAL"]].copy()
        df_style = df_style.rename(columns={"DATA_EXIB": "DATA"})  # Renomeia antes do style
        df_style["GNV"] = df_style["GNV"].astype(float)
        df_style["GAS"] = df_style["GAS"].astype(float)
        df_style["TOTAL"] = df_style["TOTAL"].astype(float)

        # ----------------------- Tabela limpa -----------------------
        st.subheader("📊 Registros Salvos</h2>")
        st.dataframe(df_style)  # Tabela sem fundo colorido

        # ----------------------- Totais -----------------------
        total_gnv = df_filtrado["GNV"].astype(float).sum()
        total_gas = df_filtrado["GAS"].astype(float).sum()
        total_geral = df_filtrado["TOTAL"].astype(float).sum()

        st.subheader("💰 Totais</h2>")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total GNV", f"R$ {total_gnv:.2f}")
        col2.metric("Total Gasolina", f"R$ {total_gas:.2f}")
        col3.metric("Total Geral", f"R$ {total_geral:.2f}")

        # ----------------------- Gráfico mensal -----------------------
        with st.expander("📈 Mostrar gráfico de gastos mensais</h2>"):
            df_view["GNV_NUM"] = df_view["GNV"].astype(float)
            df_view["GAS_NUM"] = df_view["GAS"].astype(float)
            df_view["MES"] = df_view["DATA"].dt.to_period("M")
            df_grafico = df_view.groupby("MES")[["GNV_NUM", "GAS_NUM"]].sum()
            df_grafico.rename(columns={"GNV_NUM":"GNV", "GAS_NUM":"Gasolina"}, inplace=True)
            df_grafico.index = df_grafico.index.astype(str)
            st.bar_chart(df_grafico)
