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
    .report-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

st.title("🏛️ HOLDING PATRIMONIO")
st.subheader("Simulador de Eficiência Tributária e Proteção Sucessória")

# --- BARRA LATERAL: CAPTURA DE DADOS EXTREMAMENTE DETALHADA ---
with st.sidebar:
    st.header("👤 Identificação")
    nome_cliente = st.text_input("Nome Completo")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Patrimônio e Renda")
    valor_patrimonio = st.number_input("Valor de Mercado total dos Imóveis (R$)", value=2000000.0, step=100000.0)
    aluguel_bruto = st.number_input("Receita Bruta Mensal de Aluguéis (R$)", value=20000.0)
    
    with st.expander("📝 Despesas Dedutíveis (Eduque seu Cliente)", expanded=True):
        st.caption("No Lucro Real, absolutamente todas as despesas abaixo reduzem o imposto a pagar. Na Pessoa Física, quase nada disso é aproveitado.")
        taxa_adm = st.number_input("Taxa de Imobiliária (Adm)", value=aluguel_bruto*0.1)
        iptu_condo = st.number_input("IPTU e Condomínio (Dono)", value=1000.0)
        reformas = st.number_input("Reformas e Manutenção Média", value=500.0)
        seguranca = st.number_input("Segurança e Monitoramento", value=200.0)
        seguro_patrimonial = st.number_input("Seguro Incêndio/Patrimonial", value=150.0)
        contabilidade_juridico = st.number_input("Contabilidade e Assessoria", value=800.0)
        viagens_vistoria = st.number_input("Custos de Vistoria/Viagens", value=200.0)
        anuncios = st.number_input("Propaganda e Anúncios", value=100.0)
        software_gestao = st.number_input("Software e Sistemas", value=100.0)
        taxas_bancarias = st.number_input("Taxas de Conta Jurídica", value=50.0)
        outras_despesas = st.number_input("Outras Despesas Operacionais", value=0.0)

    botao_calcular = st.button("GERAR ANÁLISE COMPLETA 🚀", type="primary")

# --- PROCESSAMENTO ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Preencha o Nome e WhatsApp para gerar o relatório.")
    else:
        # 1. CÁLCULO TRIBUTÁRIO MENSAL
        # Pessoa Física (Base simplificada)
        imposto_pf = (max(0, aluguel_bruto - taxa_adm - iptu_condo) * 0.275) - 896
        
        # Lucro Presumido
        imposto_presumido = aluguel_bruto * 0.1133
        
        # Lucro Real (Com benefício de Depreciação 4% a.a. sobre o valor das edificações)
        # Estimamos edificação como 60% do valor total para fins de simulação
        depreciacao_mensal = ((valor_patrimonio * 0.6) * 0.04) / 12
        soma_despesas_op = (taxa_adm + iptu_condo + reformas + seguranca + seguro_patrimonial + 
                            contabilidade_juridico + viagens_vistoria + anuncios + 
                            software_gestao + taxas_bancarias + outras_despesas)
        
        total_deducoes_real = soma_despesas_op + depreciacao_mensal
        imposto_real = max(0, (aluguel_bruto - total_deducoes_real)) * 0.34

        # Decisões
        opcoes = {imposto_pf: "Pessoa Física", imposto_presumido: "Lucro Presumido", imposto_real: "Lucro Real (Expert)"}
        melhor_valor_mensal = min(imposto_pf, imposto_presumido, imposto_real)
        melhor_opcao_txt = opcoes[melhor_valor_mensal]
        economia_mensal = imposto_pf - melhor_valor_mensal
        economia_anual_tributaria = economia_mensal * 12

        # 2. CÁLCULO SUCESSÓRIO (LEI 2026)
        itcmd_estimado = valor_patrimonio * 0.08  # Teto progressivo previsto
        advogados_estimado = valor_patrimonio * 0.07 # Média 6% a 8%
        custas_cartorio = valor_patrimonio * 0.03 # Taxas judiciais e cartórios
        total_inventario = itcmd_estimado + advogados_estimado + custas_cartorio
        
        custo_holding_estimado = valor_patrimonio * 0.04 
        economia_sucessoria_total = total_inventario - custo_holding_estimado

        # --- EXIBIÇÃO: RAIO-X TRIBUTÁRIO ---
        st.markdown("## 📋 1. Raio-X de Eficiência Mensal (Locação)")
        df_renda = pd.DataFrame({
            "Descrição": ["(+) Receita Bruta", "(-) Despesas Operacionais", "(-) Depreciação (Benefício Fiscal)", "(-) IMPOSTO TOTAL", "(=) LÍQUIDO NO BOLSO"],
            "Pessoa Física": [f"R$ {aluguel_bruto:,.2f}", f"R$ {taxa_adm+iptu_condo:,.2f}", "Não Dedutível", f"R$ {imposto_pf:,.2f}", f"R$ {aluguel_bruto-imposto_pf:,.2f}"],
            "Lucro Presumido": [f"R$ {aluguel_bruto:,.2f}", "Não Abate", "Não Aplicável", f"R$ {imposto_presumido:,.2f}", f"R$ {aluguel_bruto-imposto_presumido:,.2f}"],
            "Lucro Real (Expert)": [f"R$ {aluguel_bruto:,.2f}", f"R$ {soma_despesas_op:,.2f}", f"R$ {depreciacao_mensal:,.2f}", f"R$ {imposto_real:,.2f}", f"R$ {aluguel_bruto-imposto_real:,.2f}"]
        })
        st.table(df_renda)
        
        st.info(f"🎯 **Parecer Técnico Mensal:** Sua melhor opção hoje é o **{melhor_opcao_txt}**. Ao migrar da Pessoa Física para esta estrutura, você recupera **R$ {economia_mensal:,.2f}** todos os meses que atualmente são entregues ao fisco sem necessidade.")

        st.markdown("---")

        # --- EXIBIÇÃO: PROTEÇÃO SUCESSÓRIA ---
        st.markdown("## 🛡️ 2. Detalhamento de Proteção Sucessória (Lei 2026)")
        
        col_inv, col_hold = st.columns(2)
        with col_inv:
            st.markdown("### Cenário: Inventário Tradicional")
            st.write(f"❌ **ITCMD (Progressivo):** R$ {itcmd_estimado:,.2f}")
            st.write(f"❌ **Honorários Advocatícios:** R$ {advogados_estimado:,.2f}")
            st.write(f"❌ **Custas e Taxas:** R$ {custas_cartorio:,.2f}")
            st.metric("PERDA TOTAL ESTIMADA", f"R$ {total_inventario:,.2f}", delta_color="inverse")
        
        with col_hold:
            st.markdown("### Cenário: Estrutura de Holding")
            st.write(f"✅ **Planejamento Sucessório**")
            st.write(f"✅ **Doação com Reserva de Usufruto**")
            st.write(f"✅ **Gatilhos de Sucessão Imediata**")
            st.metric("INVESTIMENTO ESTIMADO", f"R$ {custo_holding_estimado:,.2f}", f"Economia: R$ {economia_sucessoria_total:,.2f}")

        st.success(f"⚖️ **Parecer Técnico Sucessório:** Sem uma estrutura de Holding, seus herdeiros enfrentarão uma dilapidação de **{ (total_inventario/valor_patrimonio)*100:.1f}%** do seu patrimônio total. A Holding elimina a necessidade de inventário, mantém o controle em suas mãos e garante a sucessão imediata.")

        st.markdown("---")

        # --- CONCLUSÃO GERAL ---
        st.markdown("## 🏆 Parecer Técnico Consolidado")
        
        res_tributario, res_sucessorio = st.columns(2)
        with res_tributario:
            st.subheader("💰 Impacto Financeiro Anual")
            st.metric("Economia Tributária Anual", f"R$ {economia_anual_tributaria:,.2f}")
            st.caption(f"Baseado na melhor opção: {melhor_opcao_txt}")

        with res_sucessorio:
            st.subheader("🛡️ Proteção de Legado")
            st.metric("Patrimônio Blindado", f"R$ {economia_sucessoria_total:,.2f}")
            st.caption("Valor que deixa de ser gasto com burocracia e impostos de morte.")

        # --- OBSERVAÇÃO FINAL E CTA ---
        st.markdown("---")
        st.error(f"""
        **⚠️ NOTA IMPORTANTE DE ADEQUAÇÃO TÉCNICA** Esta simulação utiliza alíquotas médias e não considera particularidades como créditos tributários acumulados, benefícios fiscais estaduais ou a complexidade específica da sua árvore genealógica.  
        
        **Importante:** Os valores acima são estimativas educacionais baseadas na legislação atual e projeções para 2026. Para transformar essa simulação em economia real e segurança jurídica, é indispensável um **Diagnóstico Jurídico-Tributário Personalizado**. Cada patrimônio é único e exige uma arquitetura própria para garantir a máxima proteção.
        """)

        # BOTÃO WHATSAPP COM CTA MELHORADO
        msg = (f"Olá Glauber, meu nome é {nome_cliente}. Analisei meu Raio-X na HOLDING PATRIMONIO e vi que posso "
               f"economizar R$ {economia_anual_tributaria:,.2f} por ano e proteger R$ {economia_sucessoria_total:,.2f} do inventário. "
               f"Quero agendar meu diagnóstico personalizado!")
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        
        st.link_button("AGENDAR MEU DIAGNÓSTICO PERSONALIZADO 📲", link_wa, type="primary", use_container_width=True)

        # Registro no GSheets
        try:
            dados_planilha = {
                "Data": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
                "Nome": nome_cliente,
                "Whats": whats_cliente,
                "Patrimonio": valor_patrimonio,
                "Econ_Anual": round(economia_anual_tributaria, 2),
                "Econ_Sucess": round(economia_sucessoria_total, 2)
            }
            conn.create(data=pd.DataFrame([dados_planilha]))
            st.toast("Simulação salva com sucesso!")
        except:
            pass
