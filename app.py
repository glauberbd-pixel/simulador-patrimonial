import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="Glauber & Associados | Inteligência Patrimonial", layout="wide")
st.markdown("<style>.main { background-color: #0c0c0c; color: #e0e0e0; }</style>", unsafe_allow_html=True)

# Conexão com a Planilha Google
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

st.title("🏛️ GLAUBER & ASSOCIADOS")
st.markdown("### Simulador de Eficiência Tributária")

# --- BARRA LATERAL: CAPTURA DE DADOS ---
with st.sidebar:
    st.header("👤 Seus Dados")
    nome_cliente = st.text_input("Nome Completo")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Renda e Despesas")
    aluguel_bruto = st.number_input("Renda Mensal de Aluguéis (R$)", value=20000.0)
    
    with st.expander("📝 Detalhar Despesas PF", expanded=True):
        taxa_adm = st.number_input("Taxa Imobiliária", value=aluguel_bruto*0.1)
        iptu_dono = st.number_input("IPTU (Pago pelo Dono)", value=500.0)
        dependentes = st.number_input("Nº de Dependentes", value=1, step=1)

    botao_calcular = st.button("CALCULAR ECONOMIA 🚀", type="primary")

# --- LÓGICA E RESULTADOS ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Por favor, preencha o Nome e WhatsApp para ver o resultado.")
    else:
        # Cálculo Simplificado
        imposto_pf = (aluguel_bruto - taxa_adm - iptu_dono) * 0.275 - 896
        imposto_pj = aluguel_bruto * 0.1133
        economia = imposto_pf - imposto_pj

        st.success(f"### ECONOMIA MENSAL ESTIMADA: R$ {economia:,.2f}")

        # 1. SALVAR NA PLANILHA GOOGLE
        try:
            df_novo = pd.DataFrame([{"Data": pd.Timestamp.now(), "Nome": nome_cliente, "Whats": whats_cliente, "Economia": economia}])
            conn.create(data=df_novo)
            st.toast("Dados registrados na sua planilha! 📊")
        except:
            pass

        # 2. BOTÃO WHATSAPP
        st.markdown("---")
        msg = f"Olá Glauber, meu nome é {nome_cliente}. Fiz a simulação e minha economia seria de R$ {economia:,.2f}. Quero saber mais!"
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("Falar com o Especialista Agora 📲", link_wa)
