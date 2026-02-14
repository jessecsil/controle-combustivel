import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Abastece 2026")
st.title("⛽ Controle de Combustível")

ARQUIVO = "dados.csv"

# Cria arquivo se não existir
if not os.path.exists(ARQUIVO):
    pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL']).to_csv(ARQUIVO, index=False)

# FORMULÁRIO DE CADASTRO
with st.form("meu_form", clear_on_submit=True):
    data_input = st.date_input("Data", datetime.now())
    v_gnv = st.number_input("GNV (R$)")
    v_gas = st.number_input("Gasolina (R$)")
    submit = st.form_submit_button("SALVAR")

    if submit:
        # Formata a data no padrão brasileiro
        data_formatada = data_input.strftime("%d/%m/%Y")
        total = v_gnv + v_gas

        # Cria novo registro
        df_novo = pd.DataFrame([{
            "DATA": data_formatada,
            "GNV": v_gnv,
            "GAS": v_gas,
            "TOTAL": total
        }])

        # Salva no CSV
        df_novo.to_csv(ARQUIVO, mode="a", header=False, index=False)
        st.success("Salvo com sucesso!")

st.divider()

# BOTÃO PARA APAGAR TODOS OS DADOS
if st.button("🗑️ Apagar todos os dados"):
    if os.path.exists(ARQUIVO):
        os.remove(ARQUIVO)
        st.success("Dados apagados com sucesso!")
        st.experimental_rerun()  # Recarrega o app para criar arquivo vazio novamente

# EXIBE OS DADOS
if os.path.exists(ARQUIVO):
    df_view = pd.read_csv(ARQUIVO)

    # Garantir que a coluna DATA fique como string no formato 14/02/2026
    df_view["DATA"] = df_view["DATA"].astype(str)

    # Exibir tabela no Streamlit
    st.dataframe(df_view)
