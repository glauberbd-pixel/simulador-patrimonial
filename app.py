import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="Holding Patrimônio | Inteligência Tributária", layout="wide")
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
st.subheader("Simulador de Inteligência Fiscal e Sucessória")

# --- ENTRADA DE DADOS UNIFICADA E SUGESTIVA ---
with st.sidebar:
    st.header("👤 Identificação")
    nome_cliente = st.text_input("Nome do Investidor")
    whats_cliente = st.text_input("WhatsApp (com DDD)")
    
    st.markdown("---")
    st.header("💰 Receita de Locação")
    aluguel_bruto = st.number_input("Receita Bruta Mensal (R$)", value=20000.0, step=1000.0)
    
    st.markdown("---")
    st.header("📑 Despesas Operacionais")
    st.caption("Preencha todos os custos que você tem com seus imóveis e gestão:")
    
    # Lista Única e Sugestiva
    taxa_adm = st.number_input("Comissão de Imobiliária/Adm", value=aluguel_bruto*0.1)
    iptu_cond = st.number_input("IPTU e Condomínio (Pagos pelo Proprietário)", value=1000.0)
    manutencao = st.number_input("Manutenções e Reformas nos Imóveis", value=500.0)
    contabilidade = st.number_input("Contabilidade e Jurídico", value=800.0)
    seguros_taxas = st.number_input("Seguros e Taxas Bancárias", value=200.0)
    
    # Depreciação (Sugerida para Lucro Real)
    valor_imoveis = st.number_input("Valor total dos Imóveis (para cálculo de Depreciação)", value=1000000.0)
    depreciacao_mensal = (valor_imoveis * 0.04) / 12 # 4% ao ano
    
    botao_calcular = st.button("GERAR RAIO-X DE ELISÃO FISCAL 🚀", type="primary")

# --- LÓGICA DE SEPARAÇÃO PARA RELATÓRIO ---
if botao_calcular:
    if not nome_cliente or not whats_cliente:
        st.error("Por favor, identifique-se para gerar o relatório.")
    else:
        # 1. CÁLCULO PESSOA FÍSICA (Carnê-Leão)
        # Deduções permitidas: Adm, IPTU, Condomínio e Manutenções essenciais
        base_pf = aluguel_bruto - taxa_adm - iptu_cond - manutencao
        if base_pf < 0: base_pf = 0
        imposto_pf = (base_pf * 0.275) - 896
        
        # 2. CÁLCULO LUCRO PRESUMIDO
        # Imposto fixo sobre a receita (aprox. 11.33% a 14.53% dependendo da cidade)
        imposto_presumido = aluguel_bruto * 0.1133
        
        # 3. CÁLCULO LUCRO REAL (Onde a elisão é maximizada)
        # Todas as despesas deduzem + Depreciação (despesa sem saída de caixa)
        total_despesas_real = taxa_adm + iptu_cond + manutencao + contabilidade + seguros_taxas + depreciacao_mensal
        lucro_liquido_real = aluguel_bruto - total_despesas_real
        if lucro_liquido_real < 0: lucro_liquido_real = 0
        imposto_real = lucro_liquido_real * 0.34 # IRPJ + CSLL

        # --- RELATÓRIO FINAL EM 4 COLUNAS ---
        st.markdown("### 📋 Comparativo Detalhado de Eficiência Tributária")
        
        dados_relatorio = {
            "Descrição / Etapa": [
                "1. (+) Receita Bruta Mensal",
                "2. (-) Despesas Operacionais",
                "3. (-) Depreciação (Benefício Fiscal)",
                "4. (=) Base de Cálculo do Imposto",
                "5. (X) Alíquota Efetiva Estimada",
                "6. (-) VALOR TOTAL DO IMPOSTO",
                "7. (=) DINHEIRO LÍQUIDO NO BOLSO"
            ],
            "Pessoa Física (CPF)": [
                f"R$ {aluguel_bruto:,.2f}",
                f"R$ {taxa_adm + iptu_cond + manutencao:,.2f}",
                "Não Aplicável",
                f"R$ {base_pf:,.2f}",
                "27,5% (Tabela)",
                f"R$ {imposto_pf:,.2f}",
                f"R$ {aluguel_bruto - imposto_pf:,.2f}"
            ],
            "Lucro Presumido": [
                f"R$ {aluguel_bruto:,.2f}",
                "Custos não abatem base",
                "Não Aplicável",
                f"R$ {aluguel_bruto * 0.32:,.2f} (Presunção)",
                "11.33% (Fixa)",
                f"R$ {imposto_presumido:,.2f}",
                f"R$ {aluguel_bruto - imposto_presumido:,.2f}"
            ],
            "Lucro Real (Expert)": [
                f"R$ {aluguel_bruto:,.2f}",
                f"R$ {taxa_adm + iptu_cond + manutencao + contabilidade + seguros_taxas:,.2f}",
                f"R$ {depreciacao_mensal:,.2f}",
                f"R$ {lucro_liquido_real:,.2f}",
                "34,0% s/ Lucro",
                f"R$ {imposto_real:,.2f}",
                f"R$ {aluguel_bruto - imposto_real:,.2f}"
            ]
        }
        
        st.table(pd.DataFrame(dados_relatorio))

        # --- MENSAGEM DE IMPACTO ---
        melhor_opcao = min(imposto_pf, imposto_presumido, imposto_real)
        economia_maxima = imposto_pf - melhor_opcao
        
        st.success(f"🎯 **Estratégia de Elisão:** Ao migrar para a estrutura de Holding, você economiza **R$ {economia_maxima:,.2f} todos os meses**.")

        # BOTÃO WHATSAPP
        msg = f"Olá Glauber, sou {nome_cliente}. Simulei na Holding Patrimônio e vi que posso economizar R$ {economia_maxima:,.2f} por mês. Quero iniciar minha transição fiscal!"
        link_wa = f"https://wa.me/5537991478808?text={msg.replace(' ', '%20')}"
        st.link_button("Maximizar minha Elisão Fiscal Agora 📲", link_wa, type="primary")

        # Salvar na planilha
        try:
            df_novo = pd.DataFrame([{"Data": pd.Timestamp.now(), "Nome": nome_cliente, "Economia": economia_maxima}])
            conn.create(data=df_novo)
        except: pass
