import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Abastece 2026", layout="centered")

st.title("⛽ Abastece 2026")

ARQUIVO = "dados_abastecimento.csv"

if not os.path.exists(ARQUIVO):
df_vazio = pd.DataFrame(columns=['DATA', 'GNV (R$)', 'GAS (R$)', 'TOTAL (R$)'])
df_vazio.to_csv(ARQUIVO, index=False)

with st.form("form_abastece", clear_on_submit=True):
data_input = st.date_input("Data", datetime.now())
c1, c2 = st.columns(2)
with c1:
v_gnv = st.number_input("GNV (R$)", min_value=0.0, format="%.2f")
with c2:
v_gas = st.number_input("Gasolina (R$)", min_value=0.0, format="%.2f")

st.divider()

if os.path.exists(ARQUIVO):
df_view = pd.read_csv(ARQUIVO)
if not df_view.empty:
st.metric("TOTAL ACUMULADO", f"R$ {df_view['TOTAL (R$)'].sum():.2f}")
st.dataframe(df_view, use_container_width=True)
