import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="Simulador Patrimonial Expert", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0c0c0c; color: #e0e0e0; }
    h1, h2, h3 { color: #ffffff !important; font-family: 'Helvetica', sans-serif; }
    .stNumberInput > label { color: #d4af37 !important; font-size: 16px; font-weight: bold; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 15px; border-radius: 8px; }
    div[data-testid="stMetricValue"] { color: #d4af37; font-size: 26px; }
    .css-16idsys p { font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Simulador Expert de Estrutura Patrimonial")
st.markdown("### Guia Detalhado de Deduções e Eficiência Tributária (2026)")

# --- BARRA LATERAL: INPUTS GUIADOS ---
with st.sidebar:
    st.header("1. Receitas")
    aluguel_bruto = st.number_input("Renda Bruta de Aluguéis (R$)", value=20000.0, step=500.0, help="Valor total recebido dos inquilinos antes de qualquer desconto.")

    st.markdown("---")
    st.header("2. Pessoa Física (Carnê-Leão)")
    with st.expander("📝 Livro Caixa (Abate Imposto)", expanded=True):
        st.info("Despesas essenciais para receber o aluguel.")
        pf_adm = st.number_input("Taxa de Adm. Imobiliária (R$)", value=2000.0, help="Valor pago à imobiliária (ex: 10%). Dedutível.")
        pf_iptu = st.number_input("IPTU/Condomínio (Pagos pelo Dono)", value=0.0, help="Apenas se o imóvel estiver vago ou se o contrato definir que é ônus do proprietário.")
        pf_manutencao = st.number_input("Manutenção Necessária", value=0.0, help="Reparos, pintura, encanamento pagos pelo dono para manter o imóvel alugável. Não inclui ampliações.")
    
    with st.expander("👨‍👩‍👧‍👦 Deduções Legais (Abate Base)", expanded=False):
        num_dependentes = st.number_input("Nº de Dependentes", value=2, step=1, help="Cônjuge, filhos até 21 anos (ou 24 se universitários).")
        pf_pensao = st.number_input("Pensão Alimentícia Judicial", value=0.0, help="Valor exato definido em sentença judicial.")
        pf_inss = st.number_input("INSS (Autônomo)", value=0.0, help="Contribuição previdenciária oficial paga via guia GPS.")
    
    with st.expander("💸 Outras Despesas (Saem do Bolso)", expanded=False):
        st.warning("Estas saem do caixa, mas NÃO abatem Carnê-Leão mensal.")
        pf_saude = st.number_input("Plano de Saúde/Educação (Média/Mês)", value=1500.0)

    st.markdown("---")
    st.header("3. Pessoa Jurídica (Holding)")
    with st.expander("🏢 Despesas Operacionais", expanded=True):
        pj_contador = st.number_input("Honorários Contábeis", value=600.0, help="Mensalidade do contador.")
        pj_banco = st.number_input("Tarifas Bancárias/Taxas", value=50.0)
        pj_manutencao = st.number_input("Manutenção Imóveis (PJ)", value=pf_manutencao)

    with st.expander("📈 Exclusivo Lucro Real", expanded=False):
        st.info("Aqui a mágica acontece: Despesas que reduzem o lucro tributável.")
        pj_depreciacao = st.number_input("Depreciação (Benefício Fiscal)", value=aluguel_bruto*0.04/12, help="Aprox. 4% a.a. sobre valor da construção. Reduz imposto sem gastar dinheiro.")
        pj_juros = st.number_input("Juros de Financiamento", value=0.0, help="Se houver dívida no imóvel, os juros abatem o imposto.")

    botao_calcular = st.button("CALCULAR RAIO-X DETALHADO 🚀", type="primary")

# --- MOTOR DE CÁLCULO ---
if botao_calcular:
    # --- CÁLCULO PF ---
    # 1. Base Legal (Livro Caixa)
    livro_caixa = pf_adm + pf_iptu + pf_manutencao
    renda_livro_caixa = max(aluguel_bruto - livro_caixa, 0)
    
    # 2. Base Tributável (Deduções Legais)
    deducao_dep = num_dependentes * 189.59
    base_irpf = max(renda_livro_caixa - deducao_dep - pf_pensao - pf_inss, 0)
    
    # 3. Imposto (Tabela 2025/2026)
    if base_irpf <= 2259.20: irpf = 0
    elif base_irpf <= 2826.65: irpf = (base_irpf * 0.075) - 169.44
    elif base_irpf <= 3751.05: irpf = (base_irpf * 0.15) - 381.44
    elif base_irpf <= 4664.68: irpf = (base_irpf * 0.225) - 662.77
    else: irpf = (base_irpf * 0.275) - 896.00
    
    # 4. Caixa Líquido PF (O que sobra pra gastar)
    # Receita - (Tudo que saiu do bolso, dedutível ou não)
    liquido_pf = aluguel_bruto - livro_caixa - pf_pensao - pf_inss - irpf - pf_saude

    # --- CÁLCULO PRESUMIDO ---
    # Base Fixa: 32% (Regra para Aluguel - IRPJ/CSLL)
    # Impostos Federais: ~11,33% sobre Receita Bruta
    impostos_presumido = aluguel_bruto * 0.1133
    despesas_pj_caixa = pj_contador + pj_banco + pj_manutencao # O que sai do banco
    liquido_presumido = aluguel_bruto - impostos_presumido - despesas_pj_caixa

    # --- CÁLCULO LUCRO REAL ---
    # PIS/COFINS (3,65% Cumulativo para Aluguel é o mais comum, ou 9,25% Non-Cumulativo. Vamos usar 3,65% sem crédito para ser conservador/padrão holding pura)
    pis_cofins = aluguel_bruto * 0.0365
    
    # Base IRPJ/CSLL = Receita - Todas Despesas - Depreciação
    despesas_dedutiveis_real = pj_contador + pj_banco + pj_manutencao + pj_juros + pj_depreciacao + pis_cofins
    lucro_fiscal = aluguel_bruto - despesas_dedutiveis_real
    
    if lucro_fiscal > 0:
        irpj_csll = lucro_fiscal * 0.34 # 15% IRPJ + 10% Adicional + 9% CSLL
    else:
        irpj_csll = 0
        
    imposto_total_real = pis_cofins + irpj_csll
    
    # Caixa Líquido Real (Receita - Despesas Reais - Impostos)
    # Depreciação NÃO sai do caixa, então não subtrai aqui
    liquido_real = aluguel_bruto - despesas_pj_caixa - pj_juros - imposto_total_real

    # --- DASHBOARD ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Pessoa Física (Líquido)", f"R$ {liquido_pf:,.2f}", delta=f"- Imposto: R$ {irpf:,.2f}", delta_color="inverse")
    c2.metric("Presumido (Líquido)", f"R$ {liquido_presumido:,.2f}", delta=f"- Imposto: R$ {impostos_presumido:,.2f}")
    c3.metric("Lucro Real (Líquido)", f"R$ {liquido_real:,.2f}", delta=f"- Imposto: R$ {imposto_total_real:,.2f}")
    
    st.markdown("---")
    st.subheader("📋 Detalhamento Lado a Lado (Checklist)")
    
    # Preparando dados para a tabela
    dados_tabela = {
        "Etapa do Cálculo": [
            "1. (+) Receita Bruta",
            "2. (-) Livro Caixa / Despesas Operacionais",
            "3. (-) Depreciação (Benefício sem desembolso)",
            "4. (=) Base de Cálculo do Imposto",
            "5. (-) IMPOSTO TOTAL (DARF)",
            "6. (-) Outras Despesas Pessoais (Saúde/Educ)",
            "7. (=) DINHEIRO LIMPO NO BOLSO"
        ],
        "Pessoa Física": [
            f"R$ {aluguel_bruto:,.2f}",
            f"R$ {livro_caixa:,.2f} (Adm/Manut)",
            "Não Aplicável",
            f"R$ {base_irpf:,.2f} (Após Dep./INSS)",
            f"R$ {irpf:,.2f}",
            f"R$ {pf_saude:,.2f}",
            f"**R$ {liquido_pf:,.2f}**"
        ],
        "Holding (Presumido)": [
            f"R$ {aluguel_bruto:,.2f}",
            f"R$ {despesas_pj_caixa:,.2f} (Contador/Taxas)",
            "Não Abate (Base Fixa)",
            f"R$ {(aluguel_bruto*0.32):,.2f} (32% fixo)",
            f"R$ {impostos_presumido:,.2f}",
            "Pago na PF (Distribuição)",
            f"**R$ {liquido_presumido:,.2f}**"
        ],
        "Holding (Lucro Real)": [
            f"R$ {aluguel_bruto:,.2f}",
            f"R$ {(despesas_pj_caixa + pj_juros):,.2f}",
            f"R$ {pj_depreciacao:,.2f} (Abatimento Extra)",
            f"R$ {max(lucro_fiscal, 0):,.2f}",
            f"R$ {imposto_total_real:,.2f}",
            "Pago na PF (Distribuição)",
            f"**R$ {liquido_real:,.2f}**"
        ]
    }
    
    df = pd.DataFrame(dados_tabela)
    st.table(df)
    
    # Análise Inteligente
    melhor = max(liquido_pf, liquido_presumido, liquido_real)
    st.markdown("### 🧠 Inteligência Artificial Patrimonial:")
    if melhor == liquido_pf:
        st.warning("⚠️ **Conclusão:** A Pessoa Física ainda é melhor devido às baixas despesas ou deduções altas.")
    elif melhor == liquido_presumido:
        st.success(f"✅ **Conclusão:** O **Lucro Presumido** é o campeão! Estrutura simples e eficiente. Ganho de **R$ {(liquido_presumido - liquido_pf):,.2f}/mês** sobre a PF.")
    else:
        st.success(f"💎 **Conclusão:** O **Lucro Real** é imbatível aqui! A depreciação/despesas anularam grande parte do imposto. Ganho de **R$ {(liquido_real - liquido_pf):,.2f}/mês**.")

else:
    st.info("👈 Preencha os detalhes na barra lateral. Passe o mouse sobre as (?) para dicas de preenchimento.")