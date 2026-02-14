import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Abastece 2026")
st.title("⛽ Controle de Combustível")

ARQUIVO = "dados.csv"

# Cria o CSV se não existir
if not os.path.exists(ARQUIVO):
    pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL']).to_csv(ARQUIVO, index=False)

# FORMULÁRIO DE ENTRADA
with st.form("meu_form", clear_on_submit=True):
    data_input = st.date_input("Data", datetime.now())
    
    # Mostra a data selecionada no formato DD/MM/YYYY
    data_formatada_para_exibir = data_input.strftime("%d/%m/%Y")
    st.markdown(f"**Data selecionada:** {data_formatada_para_exibir}")

    v_gnv = st.number_input("GNV (R$)")
    v_gas = st.number_input("Gasolina (R$)")
    submit = st.form_submit_button("SALVAR")

    if submit:
        total = v_gnv + v_gas

        df_novo = pd.DataFrame([{
            "DATA": data_formatada_para_exibir,  # salva no formato DD/MM/YYYY
            "GNV": v_gnv,
            "GAS": v_gas,
            "TOTAL": total
        }])

        # Salva no CSV
        df_novo.to_csv(ARQUIVO, mode="a", header=False, index=False)
        st.success("Salvo com sucesso!")

st.divider()

# BOTÃO PARA LIMPAR DADOS
if st.button("🗑️ Apagar todos os dados"):
    if os.path.exists(ARQUIVO):
        os.remove(ARQUIVO)
        st.success("Dados apagados com sucesso!")
        st.experimental_rerun()  # Recarrega o app

# EXIBIÇÃO DOS DADOS
if os.path.exists(ARQUIVO):
    df_view = pd.read_csv(ARQUIVO, dtype=str)
    df_view["DATA"] = df_view["DATA"].apply(lambda x: x.replace("-", "/"))
    
    st.subheader("Registros Salvos")
    st.dataframe(df_view)
