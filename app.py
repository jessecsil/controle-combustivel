import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Abastece 2026")
st.title("⛽ Controle de Combustível")

ARQUIVO = "dados.csv"

Cria o arquivo se não existir
if not os.path.exists(ARQUIVO):
  pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL']).to_csv(ARQUIVO, index=False)

with st.form("meu_form", clear_on_submit=True):
  data_input = st.date_input("Data", datetime.now())
  v_gnv = st.number_input("GNV (R$)")
  v_gas = st.number_input("Gasolina (R$)")
  submit = st.form_submit_button("SALVAR")

st.divider()

Exibição da tabela com correção automática de data
if os.path.exists(ARQUIVO):
  df_view = pd.read_csv(ARQUIVO)
