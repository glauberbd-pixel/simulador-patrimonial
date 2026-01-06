import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO VISUAL PREMIUM (BLACK & GOLD) ---
st.set_page_config(page_title="Holding Patrimônio | Inteligência Tributária", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0c0c0c; color: #e0e0e0; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 10px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 28px !important; }
    .stTable { background-color: #1a1a1a; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Conexão com a Planilha
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

# TÍTULO SOLICITADO
st.title("🏛️ HOLDING PATRIMÔNIO")
st.subheader("Simulador Expert de Estrutura Patrimonial (2026)")

# --- BARRA LATERAL (ENTRADA DE DADOS) ---
with st.sidebar:
    st.header("👤 Identificação")
    nome_cliente = st.text_input("Nome do Investidor")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Renda Mensal Bruta")
    aluguel_bruto = st.number_input("Renda de Aluguéis (R$)", value=20000.0, step=1000.0)
    
    with st.expander("📝 Detalhar Despesas PF", expanded=True):
        taxa_adm = st.number_input("Taxa Imobiliária (Adm)", value=aluguel_bruto*0.1)
        iptu_dono = st.number_input("IPTU/Taxas (Dono)", value=500.0)
        saude_educ = st.number_input("Saúde/Educação", value=1500.0)

    with st.expander("🏢 Detalhar Custos Holding", expanded=False):
        pj_contador = st.number_input("Honorários Contábeis", value=650.0)
        pj_taxas = st.number_input("Tarifas/Taxas PJ", value=50.0)

    botao_calcular = st.button("GERAR RAIO-X DETALHADO 🚀", type="primary")

# --- LÓGICA DE CÁLCULO E LAYOUT ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Por favor, preencha o Nome e WhatsApp na barra lateral.")
    else:
        # Cálculos de Imposto
        imposto_pf = ((aluguel_bruto - taxa_adm - iptu_dono - saude_educ) * 0.275) - 896
        imposto_pj_presumido = aluguel_bruto * 0.1133
        imposto_pj_real = (aluguel_bruto * 0.32) * 0.34 # Estimativa simplificada
        
        economia = imposto_pf - imposto_pj_presumido

        # 1. MÉTRICAS EM CARTÕES (Como na imagem 1000201857.png)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pessoa Física (Líquido)", f"R$ {aluguel_bruto - imposto_pf:,.2f}", f"Imposto: R$ {imposto_pf:,.2f}", delta_color="inverse")
        with col2:
            st.metric("Presumido (Líquido)", f"R$ {aluguel_bruto - imposto_pj_presumido:,.2f}", f"Economia: R$ {economia:,.2f}")
        with col3:
            st.metric("Lucro Real (Líquido)", f"R$ {aluguel_bruto - imposto_pj_real:,.2f}", f"Imposto: R$ {imposto_pj_real:,.2f}", delta_color="inverse")

        # 2. TABELA COMPARATIVA (CHECKLIST)
        st.markdown("### 📋 Detalhamento Lado a Lado (Checklist)")
        df_comp = pd.DataFrame({
            "Etapa do Cálculo": ["1. (+) Receita Bruta", "2. (-) Despesas Operacionais", "3. (=) Base de Cálculo", "4. (-) IMPOSTO TOTAL", "5. (=) DINHEIRO NO BOLSO"],
            "Pessoa Física": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm + iptu_dono:,.2f}", f"R$ {aluguel_bruto - taxa_adm - iptu_dono:,.2f}", f"R$ {imposto_pf:,.2f}", f"R$ {aluguel_bruto - imposto_pf:,.2f}"],
            "Holding (Presumido)": [f"R$ {aluguel_bruto:,.2f}", f"R$ {pj_contador + pj_taxas:,.2f}", f"R$ {aluguel_bruto * 0.32:,.2f}", f"R$ {imposto_pj_presumido:,.2f}", f"R$ {aluguel_bruto - imposto_pj_presumido:,.2f}"],
            "Holding (Lucro Real)": [f"R$ {aluguel_bruto:,.2f}", f"R$ {pj_contador + pj_taxas:,.2f}", f"R$ {aluguel_bruto * 0.15:,.2f}", f"R$ {imposto_pj_real:,.2f}", f"R$ {aluguel_bruto - imposto_pj_real:,.2f}"]
        })
        st.table(df_comp)

        # 3. CONCLUSÃO E BOTÃO WHATSAPP
        st.success(f"🧠 **Inteligência Artificial Patrimonial:** O Lucro Presumido é o campeão! Ganho de R$ {economia:,.2f}/mês sobre a PF.")
        
        msg = f"Olá, sou {nome_cliente}. Simulei na Holding Patrimônio e vi uma economia de R$ {economia:,.2f}. Quero falar com o Glauber!"
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("Falar com o Especialista Agora 📲", link_wa, type="primary")

        # Registro na Planilha (Opcional)
        try:
            df_novo = pd.DataFrame([{"Data": pd.Timestamp.now(), "Nome": nome_cliente, "Whats": whats_cliente, "Economia": economia}])
            conn.create(data=df_novo)
        except:
            pass
