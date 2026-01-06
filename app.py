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
st.subheader("Simulador de Elisão Fiscal e Planejamento Sucessório (Lei 2026)")

# --- ENTRADA DE DADOS: CHECKLIST DE ELISÃO MÁXIMA ---
with st.sidebar:
    st.header("👤 Identificação")
    nome_cliente = st.text_input("Nome do Investidor")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Patrimônio e Renda")
    valor_patrimonio = st.number_input("Valor de Mercado dos Imóveis (R$)", value=2000000.0, step=100000.0)
    aluguel_bruto = st.number_input("Receita Bruta Mensal de Aluguéis (R$)", value=20000.0, step=1000.0)
    
    st.markdown("---")
    st.header("📑 Checklist de Despesas (Deduções Sugeridas)")
    st.info("Sugira estes lançamentos para o sistema calcular o abatimento máximo de imposto:")
    
    # Bloco 1: Gestão Direta
    taxa_adm = st.number_input("Taxa de Imobiliária / Administração", value=aluguel_bruto*0.1)
    iptu_cond = st.number_input("IPTU e Condomínio (Pagos pelo Proprietário)", value=1000.0)
    
    # Bloco 2: Manutenção e Conservação (Maximizando Lucro Real)
    st.caption("🛠️ Preservação e Operação")
    manutencao = st.number_input("Reformas, Reparos e Pintura", value=500.0)
    limpeza_jardim = st.number_input("Limpeza, Jardinagem e Conservação", value=300.0)
    seguranca = st.number_input("Segurança e Monitoramento", value=200.0)
    seguro_imovel = st.number_input("Seguro Patrimonial / Incêndio", value=150.0)
    
    # Bloco 3: Gestão Executiva
    st.caption("⚖️ Apoio Administrativo e Jurídico")
    contabilidade = st.number_input("Honorários Contábeis e Jurídicos", value=800.0)
    tarifas_banc = st.number_input("Tarifas Bancárias e Manutenção de Conta", value=50.0)
    viagens_vistoria = st.number_input("Combustível e Despesas de Vistoria", value=200.0)
    
    botao_calcular = st.button("GERAR DIAGNÓSTICO PATRIMONIAL 🚀", type="primary")

# --- PROCESSAMENTO DOS RELATÓRIOS ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Por favor, preencha o Nome e WhatsApp para gerar o diagnóstico.")
    else:
        # A. CÁLCULO DE RENDA MENSAL
        base_pf = aluguel_bruto - taxa_adm - iptu_cond
        imposto_pf = (max(0, base_pf) * 0.275) - 896
        
        imposto_presumido = aluguel_bruto * 0.1133
        
        depreciacao_mensal = (valor_patrimonio * 0.04) / 12
        total_despesas_real = (taxa_adm + iptu_cond + manutencao + limpeza_jardim + 
                               seguranca + seguro_imovel + contabilidade + 
                               tarifas_banc + viagens_vistoria + depreciacao_mensal)
        imposto_real = max(0, (aluguel_bruto - total_despesas_real)) * 0.34

        # B. CÁLCULO SUCESSÓRIO (LEI 2026 - ITCMD PROGRESSIVO)
        itcmd = valor_patrimonio * 0.08 # Alíquota teto progressiva 2026
        advogado = valor_patrimonio * 0.08 # Tabela OAB Inventário Judicial
        custas_cartorio = valor_patrimonio * 0.02
        perda_inventario = itcmd + advogado + custas_cartorio
        
        custo_holding_total = valor_patrimonio * 0.04 # Estimativa de estruturação

        # --- RELATÓRIO 1: EFICIÊNCIA TRIBUTÁRIA ---
        st.markdown("## 📋 1. Raio-X de Eficiência Mensal (Locação)")
        df_renda = pd.DataFrame({
            "Etapa do Cálculo": ["(+) Receita Bruta", "(-) Despesas Adm/IPTU", "(-) Manutenção/Gestão/Seguros", "(-) Depreciação (Benefício)", "(-) IMPOSTO TOTAL", "(=) DINHEIRO NO BOLSO"],
            "Pessoa Física": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_cond:,.2f}", "Não Dedutível", "Não Aplicável", f"R$ {imposto_pf:,.2f}", f"R$ {aluguel_bruto-imposto_pf:,.2f}"],
            "Lucro Presumido": [f"R$ {aluguel_bruto:,.2f}", "Não Abate", "Não Abate", "Não Aplicável", f"R$ {imposto_presumido:,.2f}", f"R$ {aluguel_bruto-imposto_presumido:,.2f}"],
            "Lucro Real (Expert)": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_cond:,.2f}", f"R$ {total_despesas_real-taxa_adm-iptu_cond-depreciacao_mensal:,.2f}", f"R$ {depreciacao_mensal:,.2f}", f"R$ {imposto_real:,.2f}", f"R$ {aluguel_bruto-imposto_real:,.2f}"]
        })
        st.table(df_renda)

        st.markdown("---")

        # --- RELATÓRIO 2: PROTEÇÃO SUCESSÓRIA DETALHADA ---
        st.markdown("## 🛡️ 2. Diagnóstico Sucessório (Inventário x Holding)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Perda no Inventário", f"R$ {perda_inventario:,.2f}", "Imposto + Advogado + Custas", delta_color="inverse")
        with col2:
            st.metric("Custo na Holding", f"R$ {custo_holding_total:,.2f}", f"Economia de R$ {perda_inventario - custo_holding_total:,.2f}")

        st.markdown("### Descritivo do Custo Sucessório")
        df_sucessao = pd.DataFrame({
            "Item de Custo": ["1. ITCMD (Imposto Progressivo 2026)", "2. Honorários Advocatícios (Mín. OAB)", "3. Custas Judiciais e Cartórios", "4. Tempo Estimado de Processo", "TOTAL DA DESPESA"],
            "Cenário: Inventário": [f"R$ {itcmd:,.2f}", f"R$ {advogado:,.2f}", f"R$ {custas_cartorio:,.2f}", "12 a 36 meses", f"R$ {perda_inventario:,.2f}"],
            "Cenário: Holding": ["Isento na Sucessão (Pré-pago)", f"R$ {valor_patrimonio*0.01:,.2f} (Consultoria)", f"R$ {valor_patrimonio*0.005:,.2f}", "Imediato (Gatilho)", f"R$ {custo_holding_total:,.2f}"]
        })
        st.table(df_sucessao)

        # CONCLUSÃO
        economia_mes = imposto_pf - min(imposto_presumido, imposto_real)
        st.success(f"🎯 **Resumo Estratégico:** Além de salvar **R$ {economia_mes:,.2f}/mês**, você evita uma perda de **R$ {perda_inventario:,.2f}** para sua família.")

        # BOTÃO WHATSAPP
        msg = f"Olá Glauber, sou {nome_cliente}. Vi que posso salvar R$ {economia_mes:,.2f}/mês e evitar a perda de R$ {perda_inventario:,.2f} no meu patrimônio de R$ {valor_patrimonio:,.2f}. Quero blindar meu legado!"
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("Blindar meu Legado Agora 📲", link_wa, type="primary")

        # Registro na Planilha
        try:
            df_novo = pd.DataFrame([{"Data": pd.Timestamp.now(), "Nome": nome_cliente, "Whats": whats_cliente, "Economia_Mes": economia_mes, "Risco_Inventario": perda_inventario}])
            conn.create(data=df_novo)
        except: pass
