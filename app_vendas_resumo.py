import streamlit as st
from datetime import datetime
import requests

# ----------- CONFIGURAÇÕES FIXAS -----------

# Preços e custos
PRECO_ICE = 200_000
CUSTO_ICE = 100_000
PRECO_GARRAFA = 50_000
CUSTO_GARRAFA = 15_000
WEBHOOK_URL = "https://discord.com/api/webhooks/1385662720979898448/Yu1ww83kqU4g7hoq0YSZR9f013chW-VxIbiv9NmRqlCg__EbzZY8x5Y2m3ZXS-9RAFN6"

# ----------- FUNÇÕES DE ESTILO VISUAL -----------

def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    import base64
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def show_logo(image_path):
    st.markdown(
        f"<div style='text-align:center'><img src='data:image/png;base64,{base64_encode(image_path)}' width='150'></div>",
        unsafe_allow_html=True
    )

def base64_encode(path):
    with open(path, "rb") as f:
        import base64
        return base64.b64encode(f.read()).decode()

# ----------- APLICAR ESTILO E LOGO -----------

set_background("club77_background_faded.png")
show_logo("club77_logo.png")

# ----------- INTERFACE DO APLICATIVO -----------

st.title("💎 Club 77 - Controle de Vendas")
st.markdown("---")

# Entrada do nome do vendedor
vendedor = st.text_input("👤 Nome do Vendedor")

# Botão de entrada
if st.button("✅ Iniciar Turno"):
    st.session_state['turno_ativo'] = True
    st.success("Turno iniciado!")

# Se turno estiver ativo, exibir interface principal
if st.session_state.get('turno_ativo'):

    st.subheader("📦 Registro de Vendas")

    qtd_ice = st.number_input("Quantidade de ICE 77", min_value=0, step=1)
    qtd_garrafa = st.number_input("Quantidade de Garrafas", min_value=0, step=1)
    qtd_outros = st.number_input("Quantidade de Outros", min_value=0, step=1)
    valor_outros = st.number_input("Valor unitário de 'Outros'", min_value=0, step=1000)

    # Cálculo
    venda_ice = qtd_ice * PRECO_ICE
    custo_ice = qtd_ice * CUSTO_ICE

    venda_garrafa = qtd_garrafa * PRECO_GARRAFA
    custo_garrafa = qtd_garrafa * CUSTO_GARRAFA

    venda_outros = qtd_outros * valor_outros
    custo_outros = 0

    total_venda = venda_ice + venda_garrafa + venda_outros
    total_custo = custo_ice + custo_garrafa + custo_outros
    lucro = total_venda - total_custo

    st.markdown("---")
    st.subheader("💰 Resultado Parcial")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Vendido", f"R$ {total_venda:,.0f}")
    col2.metric("Total de Custo", f"R$ {total_custo:,.0f}")
    col3.metric("Total a Enviar", f"R$ {lucro:,.0f}")

    # Botão para finalizar o turno
    if st.button("🚪 Finalizar Turno e Enviar Relatório"):
        hoje = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        relatorio = f"""📊 RELATÓRIO DE VENDAS - {hoje}

👤 Vendedor: {vendedor}

Quantidade Vendida:
- ICE 77: {qtd_ice}
- Garrafas: {qtd_garrafa}
- Outros: {qtd_outros} (R$ {valor_outros:,} cada)

Totais:
- Total Vendido: R$ {total_venda:,}
- Total de Custo: R$ {total_custo:,}
- Total a Enviar: R$ {lucro:,}

➡️ Enviar para Miranda Magnata ID-7684"""

        # Enviar para o Discord
        try:
            requests.post(WEBHOOK_URL, json={"content": f"```{relatorio}```"})
            st.success("✅ Turno finalizado e relatório enviado para o Discord!")
        except:
            st.error("❌ Erro ao enviar o relatório para o Discord.")

        st.session_state['turno_ativo'] = False
