import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO VISUAL EXPERT (ALL BLACK) ---
st.set_page_config(page_title="Holding Patrimônio | Inteligência Tributária", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0c0c0c; color: #e0e0e0; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 10px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# Conexão com Planilha
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

# TÍTULO ATUALIZADO
st.title("🏛️ HOLDING PATRIMÔNIO")
st.subheader("Simulador Expert de Estrutura Patrimonial (2026)")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("👤 Identificação")
    nome_cliente = st.text_input("Nome do Investidor")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Renda Bruta")
    aluguel_bruto = st.number_input("Renda Mensal de Aluguéis (R$)", value=20000.0, step=1000.0)
    
    with st.expander("📝 Deduções Pessoa Física", expanded=True):
        taxa_adm = st.number_input("Taxa Imobiliária (Adm)", value=aluguel_bruto*0.1)
        iptu_dono = st.number_input("IPTU/Taxas (Pago pelo Dono)", value=500.0)
        saude_educ = st.number_input("Deduções Saúde/Educação", value=1500.0)

    botao_calcular = st.button("GERAR RAIO-X DETALHADO 🚀", type="primary")

# --- LÓGICA DE CÁLCULO EXPERT ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Por favor, preencha Nome e WhatsApp para gerar o relatório.")
    else:
        # Cálculos
        imposto_pf = ((aluguel_bruto - taxa_adm - iptu_dono - saude_educ) * 0.275) - 896
        imposto_pj_presumido = aluguel_bruto * 0.1133
        economia = imposto_pf - imposto_pj_presumido

        # LAYOUT DE MÉTRICAS (Igual à imagem 1000201857.png)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pessoa Física (Líquido)", f"R$ {aluguel_bruto - imposto_pf:,.2f}", f"- Imposto: R$ {imposto_pf:,.2f}", delta_color="inverse")
        with col2:
            st.metric("Holding Presumido (Líquido)", f"R$ {aluguel_bruto - imposto_pj_presumido:,.2f}", f"Economia: R$ {economia:,.2f}")

        # TABELA COMPARATIVA DETALHADA
        st.markdown("### 📋 Detalhamento Lado a Lado")
        dados_tabela = {
            "Etapa do Cálculo": ["(+) Receita Bruta", "(-) Despesas Operacionais", "(=) Base de Cálculo", "(-) IMPOSTO TOTAL", "(=) DINHEIRO NO BOLSO"],
            "Pessoa Física": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm + iptu_dono:,.2f}", f"R$ {aluguel_bruto - taxa_adm - iptu_dono:,.2f}", f"R$ {imposto_pf:,.2f}", f"R$ {aluguel_bruto - imposto_pf:,.2f}"],
            "Holding (Presumido)": [f"R$ {aluguel_bruto:,.2f}", "R$ 650.00 (Méd.)", f"R$ {aluguel_bruto * 0.32:,.2f}", f"R$ {imposto_pj_presumido:,.2f}", f"R$ {aluguel_bruto - imposto_pj_presumido:,.2f}"]
        }
        st.table(pd.DataFrame(dados_tabela))

        # CONCLUSÃO E BOTÃO WHATSAPP
        st.success(f"✅ Conclusão: A Holding é a melhor opção! Ganho de R$ {economia:,.2f}/mês.")
        
        msg = f"Olá, sou {nome_cliente}. Simulei na Holding Patrimônio e vi uma economia de R$ {economia:,.2f}. Quero falar com o Glauber!"
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("Falar com o Especialista Agora 📲", link_wa, type="primary")

        # Registro na Planilha
        try:
            df_novo = pd.DataFrame([{"Data": pd.Timestamp.now(), "Nome": nome_cliente, "Whats": whats_cliente, "Economia": economia}])
            conn.create(data=df_novo)
        except:
            pass
