import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="Holding Patrimônio | Inteligência Sucessória", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0c0c0c; color: #e0e0e0; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 10px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 26px !important; }
    .stTable { background-color: #1a1a1a; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

st.title("🏛️ HOLDING PATRIMÔNIO")
st.subheader("Simulador de Inteligência Fiscal e Sucessória (Lei 2026)")

# --- ENTRADA DE DADOS UNIFICADA ---
with st.sidebar:
    st.header("👤 Identificação")
    nome_cliente = st.text_input("Nome do Investidor")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Patrimônio e Renda")
    valor_patrimonio = st.number_input("Valor Total do Patrimônio (R$)", value=2000000.0, step=100000.0)
    aluguel_bruto = st.number_input("Receita de Aluguéis Mensal (R$)", value=20000.0, step=1000.0)
    
    st.markdown("---")
    st.header("📑 Despesas Operacionais Sugeridas")
    st.caption("Custos que reduzem sua base de imposto:")
    taxa_adm = st.number_input("Adm. Imobiliária (10%)", value=aluguel_bruto*0.1)
    iptu_cond = st.number_input("IPTU e Condomínio (Anual/12)", value=1000.0)
    manutencao = st.number_input("Manutenção e Reformas", value=500.0)
    contabilidade = st.number_input("Contabilidade e Jurídico", value=800.0)
    
    # Cálculo automático de Depreciação
    depreciacao_mensal = (valor_patrimonio * 0.04) / 12
    
    botao_calcular = st.button("GERAR RAIO-X COMPLETO 🚀", type="primary")

# --- PROCESSAMENTO DOS RELATÓRIOS ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Por favor, preencha os dados de identificação.")
    else:
        # 1. CÁLCULO DE RENDA MENSAL (4 Colunas)
        base_pf = aluguel_bruto - taxa_adm - iptu_cond - manutencao
        imposto_pf = (max(0, base_pf) * 0.275) - 896
        imposto_presumido = aluguel_bruto * 0.1133
        
        total_despesas_real = taxa_adm + iptu_cond + manutencao + contabilidade + depreciacao_mensal
        imposto_real = max(0, (aluguel_bruto - total_despesas_real)) * 0.34

        # 2. CÁLCULO SUCESSÓRIO (Inventário x Holding)
        # Custos Médios 2026: ITCMD Progressivo (est. 6%), Advogado (10%), Custas (2%)
        custo_itcmd = valor_patrimonio * 0.06
        custo_advogado = valor_patrimonio * 0.10
        custo_inventario_total = custo_itcmd + custo_advogado + (valor_patrimonio * 0.02)
        
        custo_holding_sucessao = valor_patrimonio * 0.03 # Custo de estruturação e gatilhos sucessórios

        # --- EXIBIÇÃO RELATÓRIO 1: EFICIÊNCIA DE RENDA ---
        st.markdown("## 📋 1. Eficiência Tributária Mensal")
        dados_renda = {
            "Etapa do Cálculo": ["Receita Bruta", "Despesas Operacionais", "Depreciação (Isenção)", "Imposto Total", "Líquido Final"],
            "Pessoa Física": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_cond:,.2f}", "Não permite", f"R$ {imposto_pf:,.2f}", f"R$ {aluguel_bruto-imposto_pf:,.2f}"],
            "Lucro Presumido": [f"R$ {aluguel_bruto:,.2f}", "Não abate", "Não permite", f"R$ {imposto_presumido:,.2f}", f"R$ {aluguel_bruto-imposto_presumido:,.2f}"],
            "Lucro Real (Expert)": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_cond+contabilidade:,.2f}", f"R$ {depreciacao_mensal:,.2f}", f"R$ {imposto_real:,.2f}", f"R$ {aluguel_bruto-imposto_real:,.2f}"]
        }
        st.table(pd.DataFrame(dados_renda))

        st.markdown("---")

        # --- EXIBIÇÃO RELATÓRIO 2: CUSTO SUCESSÓRIO (INVENTÁRIO) ---
        st.markdown("## ⚰️ 2. Proteção de Herança: Inventário x Holding")
        st.warning("⚠️ Com a Lei de 2026, o ITCMD progressivo pode consumir até 20% do patrimônio no inventário.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Perda no Inventário", f"R$ {custo_inventario_total:,.2f}", "Custas + Imposto + Advogado", delta_color="inverse")
        with col2:
            st.metric("Custo na Holding", f"R$ {custo_holding_sucessao:,.2f}", f"Economia de R$ {custo_inventario_total - custo_holding_sucessao:,.2f}")

        st.markdown("### Detalhamento da Perda Patrimonial")
        dados_sucessao = {
            "Custos Previstos": ["ITCMD (Imposto de Causa Mortis)", "Honorários Advocatícios (Litigioso/Judicial)", "Custas Processuais e Cartórios", "Total de Perda Patrimonial"],
            "Cenário: Inventário": [f"R$ {custo_itcmd:,.2f} (Progressivo)", f"R$ {custo_advogado:,.2f} (10%)", f"R$ {valor_patrimonio*0.02:,.2f}", f"R$ {custo_inventario_total:,.2f}"],
            "Cenário: Holding": ["Pago na Doação de Cotas", "Consultoria Prévia", "Taxas de Junta Comercial", f"R$ {custo_holding_sucessao:,.2f}"]
        }
        st.table(pd.DataFrame(dados_sucessao))

        # CONCLUSÃO FINAL
        st.success(f"🎯 **Resumo Estratégico:** Além de ganhar R$ {imposto_pf - min(imposto_presumido, imposto_real):,.2f} a mais por mês, você evita que sua família perca R$ {custo_inventario_total - custo_holding_sucessao:,.2f} em um futuro inventário.")

        # BOTÃO WHATSAPP
        msg = f"Olá Glauber, sou {nome_cliente}. Fiz a simulação completa. Vi que posso economizar no mensal e evitar uma perda de R$ {custo_inventario_total:,.2f} no inventário. Quero proteger meu patrimônio!"
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("Blindar meu Patrimônio Agora 📲", link_wa, type="primary")

        # Salvar na planilha
        try:
            df_novo = pd.DataFrame([{"Data": pd.Timestamp.now(), "Nome": nome_cliente, "Economia_Mensal": imposto_pf - imposto_presumido, "Risco_Inventario": custo_inventario_total}])
            conn.create(data=df_novo)
        except: pass
