import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="HOLDING PATRIMONIO | Inteligência Patrimonial", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0c0c0c; color: #e0e0e0; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 10px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 26px !important; }
    label { color: #d4af37 !important; font-weight: bold; }
    .stTable { background-color: #1a1a1a; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# URL da Planilha Fornecida
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1BuFZ7Rpt0aGk3lgEc4WY8rXeWYS5_Cf6_-tAqf59lCA/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

st.title("🏛️ HOLDING PATRIMONIO")
st.subheader("Simulador de Eficiência Tributária e Proteção Sucessória")

# --- BARRA LATERAL: CAPTURA DE DADOS DETALHADA ---
with st.sidebar:
    st.header("👤 Identificação")
    nome_cliente = st.text_input("Nome Completo")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Patrimônio e Renda")
    valor_patrimonio = st.number_input("Valor de Mercado total dos Imóveis (R$)", value=2000000.0, step=100000.0)
    aluguel_bruto = st.number_input("Receita Bruta Mensal de Aluguéis (R$)", value=20000.0)
    
    with st.expander("📝 Despesas Dedutíveis (Oportunidades)", expanded=True):
        st.caption("No Lucro Real, estas despesas reduzem drasticamente o seu imposto.")
        taxa_adm = st.number_input("Taxa de Imobiliária", value=aluguel_bruto*0.1)
        iptu_condo = st.number_input("IPTU e Condomínio (Dono)", value=1000.0)
        reformas = st.number_input("Reformas e Manutenção", value=500.0)
        seguranca = st.number_input("Segurança e Monitoramento", value=200.0)
        seguro_pat = st.number_input("Seguro Patrimonial", value=150.0)
        contabilidade = st.number_input("Contabilidade e Jurídico", value=800.0)
        viagens = st.number_input("Custos de Vistoria/Viagens", value=200.0)
        marketing = st.number_input("Propaganda e Anúncios", value=100.0)
        software = st.number_input("Sistemas/Software", value=100.0)
        tarifas = st.number_input("Tarifas Bancárias PJ", value=50.0)
        outras = st.number_input("Outras Operacionais", value=0.0)

    botao_calcular = st.button("GERAR ANÁLISE COMPLETA 🚀", type="primary")

# --- PROCESSAMENTO ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Preencha o Nome e WhatsApp para gerar o relatório.")
    else:
        # 1. CÁLCULO TRIBUTÁRIO
        imposto_pf = (max(0, aluguel_bruto - taxa_adm - iptu_condo) * 0.275) - 896
        imposto_presumido = aluguel_bruto * 0.1133
        
        depreciacao_mensal = (valor_patrimonio * 0.04) / 12
        soma_despesas = (taxa_adm + iptu_condo + reformas + seguranca + seguro_pat + 
                         contabilidade + viagens + marketing + software + tarifas + outras)
        imposto_real = max(0, (aluguel_bruto - soma_despesas - depreciacao_mensal)) * 0.34

        opcoes = {imposto_pf: "Pessoa Física", imposto_presumido: "Lucro Presumido", imposto_real: "Lucro Real (Expert)"}
        melhor_v_mensal = min(imposto_pf, imposto_presumido, imposto_real)
        melhor_opcao_txt = opcoes[melhor_v_mensal]
        economia_mes = imposto_pf - melhor_v_mensal
        economia_ano = economia_mes * 12

        # 2. CÁLCULO SUCESSÓRIO
        perda_inventario = valor_patrimonio * 0.18
        custo_holding = valor_patrimonio * 0.04
        economia_sucessoria = perda_inventario - custo_holding

        # --- SEÇÃO 1: RAIO-X TRIBUTÁRIO ---
        st.markdown("## 📋 1. Raio-X de Eficiência Mensal (Locação)")
        df_renda = pd.DataFrame({
            "Descrição": ["(+) Receita Bruta", "(-) Despesas Operacionais", "(-) Depreciação (Benefício)", "(-) IMPOSTO TOTAL", "(=) LÍQUIDO NO BOLSO"],
            "Pessoa Física": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_condo:,.2f}", "Não Aplicável", f"R$ {imposto_pf:,.2f}", f"R$ {aluguel_bruto-imposto_pf:,.2f}"],
            "Lucro Presumido": [f"R$ {aluguel_bruto:,.2f}", "Não Dedutível", "Não Aplicável", f"R$ {imposto_presumido:,.2f}", f"R$ {aluguel_bruto-imposto_presumido:,.2f}"],
            "Lucro Real (Expert)": [f"R$ {aluguel_bruto:,.2f}", f"R$ {soma_despesas:,.2f}", f"R$ {depreciacao_mensal:,.2f}", f"R$ {imposto_real:,.2f}", f"R$ {aluguel_bruto-imposto_real:,.2f}"]
        })
        st.table(df_renda)
        st.info(f"🎯 **Parecer Técnico Tributário:** Sua melhor opção é **{melhor_opcao_txt}**. Isso gera uma economia direta de **R$ {economia_mes:,.2f}/mês** comparado à Pessoa Física.")

        st.markdown("---")

        # --- SEÇÃO 2: PROTEÇÃO SUCESSÓRIA (DETALHAMENTO) ---
        st.markdown("## 🛡️ 2. Detalhamento de Proteção Sucessória (Lei 2026)")
        df_sucessorio = pd.DataFrame({
            "Ponto de Comparação": ["Custo Financeiro (Impostos/Custas)", "Disponibilidade dos Bens", "Velocidade do Processo", "Gestão do Patrimônio", "Impacto Familiar"],
            "Inventário Tradicional": [f"R$ {perda_inventario:,.2f} (~18%)", "Bens Bloqueados / Indisponíveis", "Lento (Anos de duração)", "Transtornos Operacionais", "Alto risco de conflitos"],
            "Holding Patrimonial": [f"R$ {custo_holding:,.2f} (~4%)", "Acesso Imediato / Uso livre", "Imediata (Sucessão planejada)", "Continuidade Fluida", "Harmonia e Regras Claras"]
        })
        st.table(df_sucessorio)
        st.success(f"⚖️ **Parecer Técnico Sucessório:** O Inventário causaria uma paralisia no seu legado e uma perda de **R$ {perda_inventario:,.2f}**. Com a Holding, você garante a continuidade do negócio e protege **R$ {economia_sucessoria:,.2f}** que ficariam presos em burocracia.")

        st.markdown("---")

        # --- SEÇÃO 3: PARECER CONSOLIDADO ---
        st.markdown("## 🏆 Parecer Técnico Consolidado")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Economia Tributária Anual", f"R$ {economia_ano:,.2f}", f"Base: {melhor_opcao_txt}")
        with c2:
            st.metric("Patrimônio Blindado", f"R$ {economia_sucessoria:,.2f}", "Economia Sucessória Estimada")
        
        st.write(f"**Conclusão:** Somando a eficiência mensal e a proteção sucessória, seu ganho real no primeiro ano de estruturação é de aproximadamente **R$ {economia_ano + economia_sucessoria:,.2f}**.")

        # --- OBSERVAÇÃO FINAL E CTA ---
        st.markdown("---")
        st.warning("""
        **⚠️ NOTA IMPORTANTE DE ADEQUAÇÃO TÉCNICA**
        
        Cada caso necessita de adequação personalizada. Esta simulação utiliza alíquotas médias e não considera particularidades como créditos tributários, benefícios fiscais vigentes ou especificidades do seu modelo de negócio. 
        
        Para uma análise precisa do impacto no seu caso específico e identificação de oportunidades de otimização, recomendamos um **diagnóstico tributário personalizado**. Os valores apresentados são estimativas baseadas em alíquotas médias setoriais e não constituem aconselhamento jurídico ou fiscal definitivo. 
        
        **Não deixe seu legado à mercê da burocracia. Consulte um especialista para validar seu projeto.**
        """)

        # BOTÃO WHATSAPP
        msg = (f"Olá Glauber, meu nome é {nome_cliente}. Realizei a simulação na HOLDING PATRIMONIO e vi que posso "
               f"economizar R$ {economia_ano:,.2f}/ano e evitar uma perda sucessória de R$ {perda_inventario:,.2f}. "
               f"Quero agendar meu diagnóstico personalizado!")
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("SOLICITAR MEU DIAGNÓSTICO PERSONALIZADO 📲", link_wa, type="primary", use_container_width=True)

        # Registro na Planilha Específica
        try:
            df_envio = pd.DataFrame([{
                "Data": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                "Nome": nome_cliente,
                "Whats": whats_cliente,
                "Patrimonio": valor_patrimonio,
                "Aluguel": aluguel_bruto,
                "Melhor_Opcao": melhor_opcao_txt,
                "Econ_Tributaria_Ano": round(economia_ano, 2),
                "Econ_Sucessoria": round(economia_sucessoria, 2)
            }])
            # Enviando para a planilha via URL
            conn.create(spreadsheet=URL_PLANILHA, data=df_envio)
            st.toast("Simulação registrada na sua planilha! 📊")
        except Exception as e:
            st.error(f"Erro ao salvar na planilha: {e}")
