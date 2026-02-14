import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Abastece 2026")
st.title("Abastece 2026")

ARQUIVO = "dados.csv"

if not os.path.exists(ARQUIVO):
df_vazio = pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL'])
df_vazio.to_csv(ARQUIVO, index=False)

with st.form("form_abastece", clear_on_submit=True):
data_input = st.date_input("Data", datetime.now())
v_gnv = st.number_input("GNV (R$)", min_value=0.0)
v_gas = st.number_input("Gasolina (R$)", min_value=0.0)
submit = st.form_submit_button("SALVAR REGISTRO")

st.divider()

if os.path.exists(ARQUIVO):
df_view = pd.read_csv(ARQUIVO)
st.dataframe(df_view, use_container_width=True)
