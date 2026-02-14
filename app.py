import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Abastece 2026", page_icon="⛽")

DB = 'dados_combustivel.csv'

def carregar_dados():
if os.path.exists(DB):
try:
return pd.read_csv(DB)
except:
return pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL'])
return pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL'])

if 'dados' not in st.session_state:
st.session_state.dados = carregar_dados()

st.title("⛽ Abastece 2026")

FORMULÁRIO SIMPLES
with st.form("meu_form"):
dt = st.date_input("Data", datetime.now())
gnv = st.number_input("Valor GNV (R$)", min_value=0.0, format="%.2f")
gas = st.number_input("Valor Gasolina (R$)", min_value=0.0, format="%.2f")
salvar = st.form_submit_button("SALVAR AGORA")

EXIBIÇÃO
df = st.session_state.dados
if not df.empty:
st.divider()
st.metric("Total Acumulado", f"R$ {df['TOTAL'].sum():.2f}")
