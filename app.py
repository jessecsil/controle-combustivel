import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------- Função para formatar valores como moeda ----------------
def moeda_brasil(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ----------------------- Configuração da página -----------------------
st.markdown("""
<h3 style='text-align: left;'>
⛽ Abasteceu ⛽
</h3>
""", unsafe_allow_html=True)

st.markdown("<h6 style='text-align:left;'>Controle de Combustível</h6>", unsafe_allow_html=True)


ARQUIVO = "dados.csv"

# ----------------------- Cria CSV se não existir -----------------------
if not os.path.exists(ARQUIVO):
    pd.DataFrame(columns=['DATA', 'GNV', 'GAS', 'TOTAL']).to_csv(ARQUIVO, index=False)

# ----------------------- Formulário de cadastro -----------------------
with st.form("meu_form", clear_on_submit=True):
    st.markdown("<h5>📋 Registrar Abastecimento</h5>", unsafe_allow_html=True)

    # Data do abastecimento
    data_input = st.date_input("Data", datetime.now())

    # Valores iniciais
    valor_inicial = 0.00

    # Campos de entrada para GNV e Gasolina
    v_gnv = st.number_input(
        label="GNV (R$)",
        min_value=0.0,
        value=valor_inicial,
        step=0.01,
        format="%.2f"
    )
    v_gas = st.number_input(
        label="Gasolina (R$)",
        min_value=0.0,
        value=valor_inicial,
        step=0.01,
        format="%.2f"
    )

    # Botão de salvar
    submit = st.form_submit_button("💾 SALVAR")

    if submit:
        # Calcula total somente após clicar em SALVAR
        total = v_gnv + v_gas

        # Formata a data
        data_formatada = data_input.strftime("%d/%m/%Y")

        # Cria DataFrame para salvar
        df_novo = pd.DataFrame([{
            "DATA": data_formatada,
            "GNV": v_gnv,
            "GAS": v_gas,
            "TOTAL": total
        }])

        # Salva no CSV
        df_novo.to_csv(ARQUIVO, mode="a", header=False, index=False)

        # Formata os valores para exibir ao usuário
        gnv_formatado = moeda_brasil(v_gnv)
        gas_formatado = moeda_brasil(v_gas)
        total_formatado = moeda_brasil(total)

        # Mensagem de sucesso
        st.success("✅ Salvo com sucesso!")

        # Exibe os valores formatados
        st.markdown(
            f"""
            <div style='font-size:14px;'>
                <strong>GNV:</strong> {gnv_formatado} <br>
                <strong>Gasolina:</strong> {gas_formatado} <br>
                <strong>Total:</strong> {total_formatado}
            </div>
            """,
            unsafe_allow_html=True
        )



# ----------------------- Botão limpar dados -----------------------
if st.button("🗑️ Apagar todos os dados"):
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
    st.subheader("📅 Filtrar por período")
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
        df_style["GNV"] = df_style["GNV"].astype(float).apply(moeda_brasil)
        df_style["GAS"] = df_style["GAS"].astype(float).apply(moeda_brasil)
        df_style["TOTAL"] = df_style["TOTAL"].astype(float).apply(moeda_brasil)


        # ----------------------- Tabela limpa -----------------------
        st.subheader("📊 Registros Salvos")
        st.dataframe(df_style)  # Tabela sem fundo colorido

       # ----------------------- Totais -----------------------
        total_gnv = df_filtrado["GNV"].astype(float).sum()
        total_gas = df_filtrado["GAS"].astype(float).sum()
        total_geral = df_filtrado["TOTAL"].astype(float).sum()

        # Totais menores e organizados em linhas com moeda brasileira
        st.markdown(f"""
        <div style='font-size:18px;'>
        <strong>Total GNV:</strong> {moeda_brasil(total_gnv)} <br>
        <strong>Total Gasolina:</strong> {moeda_brasil(total_gas)} <br>
        <strong>Total Geral:</strong> {moeda_brasil(total_geral)}
        </div>
        """, unsafe_allow_html=True)

       # ----------------------- Gráfico mensal -----------------------
with st.expander("📈 Mostrar gráfico de gastos mensais"):
    # Converte colunas para float
    df_view["GNV_NUM"] = df_view["GNV"].astype(float)
    df_view["GAS_NUM"] = df_view["GAS"].astype(float)

    # Cria coluna mês
    df_view["MES"] = df_view["DATA"].dt.to_period("M")

    # Agrupa por mês
    df_grafico = df_view.groupby("MES")[["GNV_NUM", "GAS_NUM"]].sum()
    df_grafico.rename(columns={"GNV_NUM":"GNV", "GAS_NUM":"Gasolina"}, inplace=True)
    df_grafico.index = df_grafico.index.astype(str)

    # Soma dos totais para o gráfico
    total_gnv = df_grafico["GNV"].sum()
    total_gas = df_grafico["Gasolina"].sum()

    # Dados para o gráfico de pizza
    labels = ["GNV", "Gasolina"]
    sizes = [total_gnv, total_gas]
    colors = ['#ffcc00', '#0099ff']
    explode = (0.1, 0)  # Explodir a fatia do GNV para destacar

    # Plotando o gráfico de pizza
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Para deixar o gráfico com aspecto de círculo

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

