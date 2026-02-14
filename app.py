import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Abastece 2026")
st.title("⛽ Controle de Combustível")

ARQUIVO = "dados.csv"

if not os.path.exists(ARQUIVO):
  pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL']).to_csv(ARQUIVO, index=False)

with st.form("meu_form", clear_on_submit=True):
  data_input = st.date_input("Data", datetime.now())
  v_gnv = st.number_input("GNV (R$)")
  v_gas = st.number_input("Gasolina (R$)")
  submit = st.form_submit_button("SALVAR")
  if submit:
    data_formatada = data_input.strftime("%d/%m/%Y")
    total = v_gnv + v_gas

    df_novo = pd.DataFrame([{
        "DATA": data_formatada,
        "GNV": v_gnv,
        "GAS": v_gas,
        "TOTAL": total
    }])

    df_novo.to_csv(ARQUIVO, mode="a", header=False, index=False)

    st.success("Salvo com sucesso!")

st.divider()

# BOTÃO PARA APAGAR TODOS OS DADOS
if st.button("🗑️ Apagar todos os dados"):
    if os.path.exists(ARQUIVO):
        os.remove(ARQUIVO)
        st.success("Dados apagados com sucesso!")
        st.rerun()
