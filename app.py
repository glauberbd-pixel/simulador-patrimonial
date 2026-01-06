import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="HOLDING PATRIMONIO | Inteligência Patrimonial", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0c0c0c; color: #e0e0e0; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 10px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 24px !important; }
    label { color: #d4af37 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

st.title("🏛️ HOLDING PATRIMONIO")
st.subheader("Simulador de Eficiência Tributária e Proteção Sucessória")

# --- BARRA LATERAL: CAPTURA DE DADOS COMPLETA ---
with st.sidebar:
    st.header("👤 Seus Dados")
    nome_cliente = st.text_input("Nome Completo")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Patrimônio e Renda")
    valor_patrimonio = st.number_input("Valor de Mercado dos Imóveis (R$)", value=2000000.0, step=100000.0)
    aluguel_bruto = st.number_input("Renda Mensal de Aluguéis (R$)", value=20000.0)
    
    with st.expander("📝 Detalhamento de Despesas", expanded=True):
        taxa_adm = st.number_input("Taxa Imobiliária", value=aluguel_bruto*0.1)
        iptu_dono = st.number_input("IPTU e Condomínio (Dono)", value=1000.0)
        manutencao = st.number_input("Reformas e Manutenção", value=500.0)
        seguranca = st.number_input("Segurança e Monitoramento", value=200.0)
        seguro_imovel = st.number_input("Seguro Patrimonial", value=150.0)
        contabilidade = st.number_input("Contabilidade e Jurídico", value=800.0)
        viagens_vistoria = st.number_input("Custos de Vistoria/Viagens", value=200.0)

    botao_calcular = st.button("GERAR RAIO-X COMPLETO 🚀", type="primary")

# --- PROCESSAMENTO ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Preencha o Nome e WhatsApp para gerar o relatório.")
    else:
        # 1. CÁLCULO TRIBUTÁRIO MENSAL
        # Pessoa Física
        imposto_pf = (max(0, aluguel_bruto - taxa_adm - iptu_dono) * 0.275) - 896
        
        # Lucro Presumido
        imposto_presumido = aluguel_bruto * 0.1133
        
        # Lucro Real (Com benefício de Depreciação 4% a.a.)
        depreciacao_mensal = (valor_patrimonio * 0.04) / 12
        total_despesas = (taxa_adm + iptu_dono + manutencao + seguranca + 
                          seguro_imovel + contabilidade + viagens_vistoria + depreciacao_mensal)
        imposto_real = max(0, (aluguel_bruto - total_despesas)) * 0.34

        # Decisão da Melhor Opção
        opcoes = {imposto_pf: "Pessoa Física", imposto_presumido: "Lucro Presumido", imposto_real: "Lucro Real (Expert)"}
        melhor_valor = min(imposto_pf, imposto_presumido, imposto_real)
        melhor_opcao_txt = opcoes[melhor_valor]
        economia_mes = imposto_pf - melhor_valor

        # 2. CÁLCULO SUCESSÓRIO (LEI 2026)
        perda_inventario = valor_patrimonio * 0.18  # ITCMD Progressivo + Advogado + Custas
        custo_holding = valor_patrimonio * 0.04     # Estruturação e Planejamento
        economia_sucessoria = perda_inventario - custo_holding

        # --- RELATÓRIO 1: EFICIÊNCIA TRIBUTÁRIA ---
        st.markdown("## 📋 1. Raio-X de Eficiência Mensal (Locação)")
        df_renda = pd.DataFrame({
            "Descrição": ["(+) Receita Bruta", "(-) Despesas Adm/IPTU", "(-) Operacional/Seguros", "(-) Depreciação (Benefício)", "(-) IMPOSTO TOTAL", "(=) LÍQUIDO NO BOLSO"],
            "Pessoa Física": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_dono:,.2f}", "Não Dedutível", "Não Aplicável", f"R$ {imposto_pf:,.2f}", f"R$ {aluguel_bruto-imposto_pf:,.2f}"],
            "Lucro Presumido": [f"R$ {aluguel_bruto:,.2f}", "Não Abate", "Não Abate", "Não Aplicável", f"R$ {imposto_presumido:,.2f}", f"R$ {aluguel_bruto-imposto_presumido:,.2f}"],
            "Lucro Real (Expert)": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_dono:,.2f}", f"R$ {total_despesas-taxa_adm-iptu_dono-depreciacao_mensal:,.2f}", f"R$ {depreciacao_mensal:,.2f}", f"R$ {imposto_real:,.2f}", f"R$ {aluguel_bruto-imposto_real:,.2f}"]
        })
        st.table(df_renda)

        # --- RELATÓRIO 2: PROTEÇÃO SUCESSÓRIA ---
        st.markdown("## 🛡️ 2. Proteção Sucessória (Lei 2026)")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Perda Estimada em Inventário", f"R$ {perda_inventario:,.2f}", "ITCMD Progressivo + Advogado", delta_color="inverse")
        with c2:
            st.metric("Custo de Estruturação Holding", f"R$ {custo_holding:,.2f}", f"Economia: R$ {economia_sucessoria:,.2f}")

        st.info(f"🎯 **Parecer Técnico:** Sua melhor opção tributária é **{melhor_opcao_txt}** (R$ {melhor_valor:,.2f}). Isso gera uma economia de **R$ {economia_mes:,.2f}/mês** comparado à Pessoa Física.")

        # --- SALVAR NA PLANILHA GOOGLE ---
        try:
            dados_planilha = {
                "Data": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                "Nome": nome_cliente,
                "Whats": whats_cliente,
                "PF_Imposto": round(imposto_pf, 2),
                "LP_Imposto": round(imposto_presumido, 2),
                "LR_Imposto": round(imposto_real, 2),
                "Melhor_Opcao": melhor_opcao_txt,
                "Economia_Mes": round(economia_mes, 2),
                "Custo_Inventario": round(perda_inventario, 2),
                "Custo_Holding": round(custo_holding, 2),
                "Economia_Sucessoria": round(economia_sucessoria, 2)
            }
            df_envio = pd.DataFrame([dados_planilha])
            conn.create(data=df_envio)
            st.toast("Simulação registrada na base de dados! 📊")
        except:
            pass

        # BOTÃO WHATSAPP
        st.markdown("---")
        msg = f"Olá, meu nome é {nome_cliente}. Fiz a simulação na HOLDING PATRIMONIO e vi que posso economizar R$ {economia_mes:,.2f}/mês e evitar uma perda de R$ {perda_inventario:,.2f} no inventário. Quero blindar meu legado!"
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("Falar com um Especialista Agora 📲", link_wa, type="primary")
