import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="Holding Patrimônio | Inteligência Fiscal", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0c0c0c; color: #e0e0e0; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 10px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 24px !important; }
    .stTable { background-color: #1a1a1a; border-radius: 10px; }
    label { color: #d4af37 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

st.title("🏛️ HOLDING PATRIMÔNIO")
st.subheader("Simulador de Elisão Fiscal e Planejamento Sucessório (2026)")

# --- ENTRADA DE DADOS UNIFICADA E SUGESTIVA ---
with st.sidebar:
    st.header("👤 Identificação")
    nome_cliente = st.text_input("Nome do Investidor")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Valor de Mercado do Patrimônio")
    st.caption("Valor total dos imóveis para fins de inventário e depreciação.")
    valor_patrimonio = st.number_input("Patrimônio Total (R$)", value=2000000.0, step=100000.0)
    aluguel_bruto = st.number_input("Receita Mensal de Aluguéis (R$)", value=20000.0, step=1000.0)
    
    st.markdown("---")
    st.header("📑 Checklist de Despesas (Deduções)")
    st.info("Lance abaixo tudo o que você gasta. O sistema separará o que pode ser usado em cada regime legal.")
    
    # 1. Gestão e Impostos
    taxa_adm = st.number_input("Taxa de Imobiliária/Administração", value=aluguel_bruto*0.1, help="Dedutível em todos os regimes.")
    iptu_cond = st.number_input("IPTU e Condomínio (Pagos por você)", value=1000.0, help="Custos fixos do imóvel.")
    
    # 2. Manutenção e Preservação (Sugestivo)
    st.caption("🛠️ Preservação do Ativo")
    manutencao = st.number_input("Reformas, Pinturas e Reparos", value=500.0, help="Essencial para o Lucro Real.")
    seguro_imovel = st.number_input("Seguro Incêndio/Patrimonial", value=150.0, help="Proteção do ativo.")
    
    # 3. Operação e Consultoria (Maximizando Elisão)
    st.caption("⚖️ Gestão Jurídica e Contábil")
    contabilidade = st.number_input("Honorários Contábeis e Jurídicos", value=650.0, help="Custo de conformidade.")
    tarifas_banc = st.number_input("Tarifas Bancárias e Boletos", value=50.0)
    viagens_vistoria = st.number_input("Combustível/Viagens para Vistorias", value=200.0, help="Gastos necessários para gerir os imóveis.")
    
    botao_calcular = st.button("GERAR RAIO-X COMPLETO 🚀", type="primary")

# --- LÓGICA DE PROCESSAMENTO ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Por favor, preencha o Nome e WhatsApp para continuar.")
    else:
        # A. CÁLCULO DE RENDA (4 COLUNAS)
        # Pessoa Física: Apenas Adm, IPTU e Condomínio abatem legalmente no Carnê-Leão.
        base_pf = aluguel_bruto - taxa_adm - iptu_cond
        imposto_pf = (max(0, base_pf) * 0.275) - 896
        
        # Lucro Presumido: Imposto sobre a receita bruta.
        imposto_presumido = aluguel_bruto * 0.1133
        
        # Lucro Real: Todas as despesas + Depreciação (4% a.a.)
        depreciacao_mensal = (valor_patrimonio * 0.04) / 12
        total_despesas_real = taxa_adm + iptu_cond + manutencao + seguro_imovel + contabilidade + tarifas_banc + viagens_vistoria + depreciacao_mensal
        imposto_real = max(0, (aluguel_bruto - total_despesas_real)) * 0.34

        # B. CÁLCULO SUCESSÓRIO 2026
        # ITCMD Progressivo (Média 6%), Advogado (10%), Custas (2%)
        perda_inventario = valor_patrimonio * 0.18 
        custo_holding = valor_patrimonio * 0.04

        # --- EXIBIÇÃO RELATÓRIO 1: EFICIÊNCIA DE RENDA ---
        st.markdown("## 📋 1. Raio-X de Eficiência Tributária Mensal")
        st.write(f"Comparativo detalhado para a renda de **R$ {aluguel_bruto:,.2f}**")
        
        df_renda = pd.DataFrame({
            "Descrição": ["(+) Receita Bruta", "(-) Despesas Adm/IPTU", "(-) Manutenção/Gestão/Seguros", "(-) Depreciação (Benefício)", "(-) IMPOSTO TOTAL", "(=) LÍQUIDO NO BOLSO"],
            "Pessoa Física": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_cond:,.2f}", "Não Dedutível", "Não Aplicável", f"R$ {imposto_pf:,.2f}", f"R$ {aluguel_bruto-imposto_pf:,.2f}"],
            "Lucro Presumido": [f"R$ {aluguel_bruto:,.2f}", "Não Abate", "Não Abate", "Não Aplicável", f"R$ {imposto_presumido:,.2f}", f"R$ {aluguel_bruto-imposto_presumido:,.2f}"],
            "Lucro Real (Expert)": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_cond:,.2f}", f"R$ {manutencao+seguro_imovel+contabilidade+tarifas_banc+viagens_vistoria:,.2f}", f"R$ {depreciacao_mensal:,.2f}", f"R$ {imposto_real:,.2f}", f"R$ {aluguel_bruto-imposto_real:,.2f}"]
        })
        st.table(df_renda)

        # --- EXIBIÇÃO RELATÓRIO 2: INVENTÁRIO X SUCESSÃO ---
        st.markdown("---")
        st.markdown("## 🛡️ 2. Proteção Sucessória (Lei 2026)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Perda Estimada em Inventário", f"R$ {perda_inventario:,.2f}", "ITCMD Progressivo + Advogado", delta_color="inverse")
        with col2:
            st.metric("Custo de Estruturação Holding", f"R$ {custo_holding:,.2f}", f"Economia: R$ {perda_inventario - custo_holding:,.2f}")

        # CONCLUSÃO FINAL
        economia_mes = imposto_pf - min(imposto_presumido, imposto_real)
        st.success(f"🎯 **Parecer Técnico:** Sua elisão fiscal mensal é de **R$ {economia_mes:,.2f}**. Além disso, a Holding evita uma perda de **R$ {perda_inventario:,.2f}** para sua família.")

        # BOTÃO WHATSAPP
        msg = f"Olá Glauber, sou {nome_cliente}. Simulei na Holding Patrimônio e quero maximizar minha elisão de R$ {economia_mes:,.2f}/mês e proteger meus R$ {valor_patrimonio:,.2f} em imóveis!"
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("Maximizar meu Patrimônio Agora 📲", link_wa, type="primary")

        # Salvar na planilha
        try:
            df_novo = pd.DataFrame([{"Data": pd.Timestamp.now(), "Nome": nome_cliente, "WhatsApp": whats_cliente, "Economia": economia_mes}])
            conn.create(data=df_novo)
        except: pass
