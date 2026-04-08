import streamlit as st
import pandas as pd
import os
import math
import plotly.express as px
import plotly.graph_objects as go
import qrcode
import io
from PIL import Image

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="BioGestão 360 - Profissional", layout="wide", page_icon="🏋️")

# 2. INICIALIZAÇÕES
if 'modo_impressao' not in st.session_state:
    st.session_state.modo_impressao = False
if 'planejamento_tipo' not in st.session_state:
    st.session_state.planejamento_tipo = "Diário"
if 'cardapio_semanal' not in st.session_state:
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    st.session_state.cardapio_semanal = {dia: {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]} for dia in dias_semana}
if 'dia_atual' not in st.session_state:
    st.session_state.dia_atual = "Segunda"
if 'cardapio' not in st.session_state:
    st.session_state.cardapio = {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]}

# 3. FUNÇÃO PARA GERAR QR CODE PIX
def gerar_qr_code_pix():
    pix_data = "00020126580014br.gov.bcb.pix0136f3e890da-fb72-4e8c-a0cd-d88177457a305204000053039865802BR5925ADILSON GONCALVES XIMENES6012BELFORD ROXO62180514AdilsonXimenes6304B1CB"
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(pix_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

# 4. FUNÇÃO PARA GERAR BOTÃO PAYPAL
def get_paypal_html():
    return """
    <div id="donate-button-container" style="text-align: center; margin: 10px 0;">
        <div id="donate-button"></div>
        <script src="https://www.paypalobjects.com/donate/sdk/donate-sdk.js" charset="UTF-8"></script>
        <script>
        PayPal.Donation.Button({
            env:'production',
            hosted_button_id:'LQTE48R8SLWRG',
            image: {
                src:'https://www.paypalobjects.com/pt_BR/BR/i/btn/btn_donateCC_LG.gif',
                alt:'Faça doações com o botão do PayPal',
                title:'PayPal - The safer, easier way to pay online!'
            }
        }).render('#donate-button');
        </script>
    </div>
    """

# 5. ALIMENTOS DE RISCO (Grupo OMS)
def carregar_alimentos_risco():
    return {
        'grupo1': {
            'alimentos': ['salsicha', 'presunto', 'linguiça', 'bacon', 'salame', 'mortadela', 'nuggets', 'peixe salgado'],
            'mensagem': '⚠️ GRUPO 1: CANCERÍGENO PARA HUMANOS! Consumo diário de 50g aumenta em 18% o risco de câncer colorretal.'
        },
        'grupo2a': {
            'alimentos': ['carne bovina', 'carne de porco', 'carneiro', 'cordeiro', 'vitela'],
            'mensagem': '⚠️ GRUPO 2A: PROVAVELMENTE CANCERÍGENO! Limite a 500g por semana.'
        },
        'grupo2b': {
            'alimentos': ['aspartame', 'bebida adoçada', 'refrigerante diet', 'adoçante artificial'],
            'mensagem': '⚠️ GRUPO 2B: POSSIVELMENTE CANCERÍGENO! Ingestão diária aceitável: 40mg/kg.'
        }
    }

ALIMENTOS_RISCO = carregar_alimentos_risco()

def verificar_risco_oms(nome_alimento):
    nome_lower = nome_alimento.lower()
    for item in ALIMENTOS_RISCO['grupo1']['alimentos']:
        if item in nome_lower:
            return ALIMENTOS_RISCO['grupo1']['mensagem']
    for item in ALIMENTOS_RISCO['grupo2a']['alimentos']:
        if item in nome_lower:
            return ALIMENTOS_RISCO['grupo2a']['mensagem']
    for item in ALIMENTOS_RISCO['grupo2b']['alimentos']:
        if item in nome_lower:
            return ALIMENTOS_RISCO['grupo2b']['mensagem']
    return None

# 6. FUNÇÃO PARA CALCULAR COMPOSIÇÃO CORPORAL
def calcular_composicao_corporal(peso, altura, idade, sexo):
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    
    if sexo == "Masculino":
        percentual_gordura = (1.20 * imc) + (0.23 * idade) - 16.2
    else:
        percentual_gordura = (1.20 * imc) + (0.23 * idade) - 5.4
    
    percentual_gordura = max(5, min(50, percentual_gordura))
    massa_gordura = peso * (percentual_gordura / 100)
    massa_magra = peso - massa_gordura
    
    if sexo == "Masculino":
        imc_ideal = 21.7
    else:
        imc_ideal = 21.3
    
    peso_ideal = imc_ideal * (altura_m ** 2)
    
    return {
        'percentual_gordura': round(percentual_gordura, 1),
        'massa_gordura': round(massa_gordura, 1),
        'massa_magra': round(massa_magra, 1),
        'peso_ideal': round(peso_ideal, 1),
        'imc': round(imc, 1)
    }

# 7. FUNÇÃO PARA CALCULAR TOTAIS (DIÁRIO OU SEMANAL)
def calcular_totais_cardapio(cardapio, planejamento_tipo, cardapio_semanal=None):
    if planejamento_tipo == "Diário":
        total_kcal = sum(item['Kcal'] for ref in cardapio.values() for item in ref)
        total_prot = sum(item['P'] for ref in cardapio.values() for item in ref)
        total_carb = sum(item['C'] for ref in cardapio.values() for item in ref)
        total_gord = sum(item['G'] for ref in cardapio.values() for item in ref)
        dias = 1
    else:
        total_kcal = 0
        total_prot = 0
        total_carb = 0
        total_gord = 0
        dias = 7
        for dia in cardapio_semanal:
            for ref in cardapio_semanal[dia].values():
                for item in ref:
                    total_kcal += item['Kcal']
                    total_prot += item['P']
                    total_carb += item['C']
                    total_gord += item['G']
    
    return {
        'total_kcal': total_kcal,
        'total_prot': total_prot,
        'total_carb': total_carb,
        'total_gord': total_gord,
        'media_diaria_kcal': total_kcal / dias if dias > 0 else 0,
        'dias': dias
    }

# 8. FUNÇÕES DE LIMPEZA
def limpar_cardapio():
    if st.session_state.planejamento_tipo == "Diário":
        st.session_state.cardapio = {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]}
    else:
        st.session_state.cardapio_semanal[st.session_state.dia_atual] = {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]}
    st.success("✅ Cardápio limpo com sucesso!")
    st.rerun()

def remover_item_semanal(dia, refeicao, idx):
    st.session_state.cardapio_semanal[dia][refeicao].pop(idx)
    st.rerun()

def remover_item_diario(refeicao, idx):
    st.session_state.cardapio[refeicao].pop(idx)
    st.rerun()

def limpar_dia_semanal(dia):
    st.session_state.cardapio_semanal[dia] = {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]}
    st.success(f"✅ Cardápio de {dia} limpo!")
    st.rerun()

def limpar_semana_completa():
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    for dia in dias_semana:
        st.session_state.cardapio_semanal[dia] = {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]}
    st.success("✅ Semana inteira limpa!")
    st.rerun()

# 9. CSS PROFISSIONAL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    
    .banner-profissional {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .banner-profissional::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        100% { left: 100%; }
    }
    
    .icones-esportes {
        font-size: 40px;
        margin-bottom: 10px;
        letter-spacing: 15px;
    }
    
    .banner-profissional h1 {
        font-size: 45px;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #ffd700, #ff8c00, #ff4500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .slogan {
        font-size: 16px;
        color: #94a3b8;
        margin-top: 8px;
        letter-spacing: 1px;
    }
    
    .perfil-gigante {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        text-align: center;
        border: 2px solid #ffd700;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .perfil-gigante .titulo {
        font-size: 22px;
        font-weight: 800;
        color: #ffd700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }
    
    .perfil-gigante .dados-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    
    .perfil-gigante .dado-item {
        background: rgba(255,255,255,0.15);
        padding: 10px 20px;
        border-radius: 15px;
        min-width: 120px;
    }
    
    .perfil-gigante .dado-icon {
        font-size: 30px;
        margin-bottom: 5px;
    }
    
    .perfil-gigante .dado-valor {
        font-size: 28px;
        font-weight: 800;
        color: white;
        line-height: 1;
    }
    
    .perfil-gigante .dado-label {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 5px;
    }
    
    .meta-gigante {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        border-radius: 20px;
        padding: 15px;
        margin-top: 10px;
        text-align: center;
        border: 2px solid #ffd700;
    }
    
    .meta-gigante .meta-titulo {
        font-size: 18px;
        font-weight: 600;
        color: rgba(255,255,255,0.9);
        margin-bottom: 10px;
    }
    
    .meta-gigante .meta-valor {
        font-size: 50px;
        font-weight: 900;
        color: white;
        line-height: 1;
        margin: 5px 0;
    }
    
    .meta-gigante .meta-mensagem {
        font-size: 16px;
        font-weight: 700;
        color: #ffd700;
        margin-top: 10px;
        background: rgba(0,0,0,0.3);
        display: inline-block;
        padding: 5px 20px;
        border-radius: 50px;
    }
    
    .card-com-explicacao {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        border: 1px solid var(--border-color);
        height: 100%;
    }
    
    .card-icon {
        font-size: 28px;
        margin-bottom: 5px;
    }
    
    .card-valor {
        font-size: 24px;
        font-weight: bold;
    }
    
    .card-titulo {
        font-size: 14px;
        font-weight: 600;
        margin: 5px 0;
    }
    
    .card-explicacao {
        font-size: 11px;
        color: var(--text-light);
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid var(--border-color);
    }
    
    .header-cafe {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 15px;
        font-size: 20px;
        font-weight: bold;
    }
    
    .header-almoco {
        background: linear-gradient(90deg, #ef4444, #f87171);
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 15px;
        font-size: 20px;
        font-weight: bold;
    }
    
    .header-lanches {
        background: linear-gradient(90deg, #10b981, #34d399);
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 15px;
        font-size: 20px;
        font-weight: bold;
    }
    
    .header-jantar {
        background: linear-gradient(90deg, #8b5cf6, #a78bfa);
        color: white;
        padding: 15px;
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 15px;
        font-size: 20px;
        font-weight: bold;
    }
    
    .macro-tag-kcal {
        display: inline-block;
        background: #ef4444;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        margin-right: 8px;
    }
    
    .macro-tag-proteina {
        display: inline-block;
        background: #3b82f6;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        margin-right: 8px;
    }
    
    .macro-tag-carb {
        display: inline-block;
        background: #f59e0b;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        margin-right: 8px;
    }
    
    .macro-tag-gordura {
        display: inline-block;
        background: #10b981;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        margin-right: 8px;
    }
    
    .dia-btn-selected {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        color: white;
        border: 2px solid #ffd700;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
    }
    
    .alerta-oms-grupo1 {
        background-color: #dc2626;
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 13px;
        border-left: 5px solid #ffd700;
    }
    
    .alerta-oms-grupo2a {
        background-color: #f59e0b;
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 13px;
        border-left: 5px solid #dc2626;
    }
    
    .alerta-oms-grupo2b {
        background-color: #8b5cf6;
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 13px;
        border-left: 5px solid #f59e0b;
    }
    
    .aviso-cientifico {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-left: 4px solid #f59e0b;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-size: 12px;
        color: #cbd5e1;
    }
    
    .privacidade-box {
        background-color: var(--bg-secondary);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        margin: 15px 0;
        font-size: 12px;
    }
    
    /* RESUMO DO LAUDO - ALTO CONTRASTE */
.resumo-laudo {
    background: linear-gradient(135deg, #1e293b, #0f172a) !important;
    border: 2px solid #ffd700 !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    color: #ffffff !important;
}

.resumo-laudo h4 {
    color: #ffd700 !important;
    margin-bottom: 15px !important;
    font-size: 18px !important;
}

.resumo-laudo p {
    color: #ffffff !important;
    margin: 10px 0 !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
}

.resumo-laudo strong {
    color: #fbbf24 !important;
}

.resumo-laudo .destaque-perda {
    color: #fbbf24 !important;
    font-weight: bold;
}

.resumo-laudo .destaque-ganho {
    color: #f87171 !important;
    font-weight: bold;
}
    
    /* IMPRESSÃO - TODOS OS ELEMENTOS VISÍVEIS */
@media print {
    /* REMOVER APENAS ELEMENTOS INTERATIVOS E DESNECESSÁRIOS */
    .stSidebar, 
    .stButton, 
    .stExpander, 
    .stAlert, 
    .stDownloadButton, 
    .stRadio, 
    .stSelectbox, 
    .stNumberInput,
    .stCheckbox,
    .stTextInput,
    .stDateInput,
    .stSlider,
    button,
    [data-testid="stSidebarContent"],
    [data-testid="stToolbar"],
    .stAppHeader,
    .stAppFooter {
        display: none !important;
    }
    
    /* MANTER FUNDO BRANCO E TEXTO PRETO PARA ECONOMIA DE TINTA */
    body, .stApp, .main, .block-container, div, section {
        background: white !important;
        color: black !important;
    }
    
    /* FORÇAR CORES EM TEXTOS */
    p, h1, h2, h3, h4, h5, h6, span, li, div, .stMarkdown, .stMetric {
        color: black !important;
    }
    
    /* BANNER PROFISSIONAL - TORNA VISÍVEL */
    .banner-profissional {
        background: white !important;
        border: 2px solid #000 !important;
        box-shadow: none !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    .banner-profissional h1 {
        color: black !important;
        background: none !important;
        -webkit-text-fill-color: black !important;
    }
    
    .banner-profissional .slogan {
        color: black !important;
    }
    
    .icones-esportes {
        color: black !important;
    }
    
    /* PERFIL GIGANTE - VISÍVEL */
    .perfil-gigante {
        background: white !important;
        border: 2px solid #000 !important;
        box-shadow: none !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    .perfil-gigante .titulo {
        color: black !important;
    }
    
    .perfil-gigante .dado-item {
        background: #f0f0f0 !important;
        border: 1px solid #000 !important;
    }
    
    .perfil-gigante .dado-valor {
        color: black !important;
    }
    
    .perfil-gigante .dado-label {
        color: black !important;
    }
    
    /* META GIGANTE - VISÍVEL */
    .meta-gigante {
        background: white !important;
        border: 2px solid #000 !important;
        box-shadow: none !important;
    }
    
    .meta-gigante .meta-titulo {
        color: black !important;
    }
    
    .meta-gigante .meta-valor {
        color: black !important;
    }
    
    .meta-gigante .meta-mensagem {
        color: black !important;
        background: #f0f0f0 !important;
    }
    
    /* CARDS - VISÍVEIS */
    .card-com-explicacao {
        background: white !important;
        border: 1px solid #000 !important;
        box-shadow: none !important;
    }
    
    .card-icon {
        color: black !important;
    }
    
    .card-valor {
        color: black !important;
    }
    
    .card-titulo {
        color: black !important;
    }
    
    .card-explicacao {
        color: black !important;
        border-top: 1px solid #ccc !important;
    }
    
    /* CABEÇALHOS DAS REFEIÇÕES - VISÍVEIS EM PRETO E BRANCO */
    .header-cafe, .header-almoco, .header-lanches, .header-jantar {
        background: white !important;
        border: 2px solid #000 !important;
        color: black !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    /* MACROS TAGS - VISÍVEIS */
    .macro-tag-kcal, .macro-tag-proteina, .macro-tag-carb, .macro-tag-gordura {
        background: white !important;
        border: 1px solid #000 !important;
        color: black !important;
    }
    
    /* ALERTAS OMS - VISÍVEIS */
    .alerta-oms-grupo1, .alerta-oms-grupo2a, .alerta-oms-grupo2b {
        background: white !important;
        border: 2px solid #000 !important;
        color: black !important;
    }
    
    /* GRÁFICOS - MANTÉM CORES PARA MELHOR VISUALIZAÇÃO */
    .js-plotly-plot, .plotly, .svg-container {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    /* TABELAS - VISÍVEIS */
    table, .stDataFrame, .dataframe {
        border: 1px solid #000 !important;
        width: 100% !important;
    }
    
    th, td {
        border: 1px solid #000 !important;
        padding: 5px !important;
    }
    
    th {
        background: #f0f0f0 !important;
    }
    
    /* RESUMO LAUDO - VISÍVEL */
    .resumo-laudo {
        background: white !important;
        border: 2px solid #000 !important;
        box-shadow: none !important;
    }
    
    .resumo-laudo h4 {
        color: black !important;
    }
    
    .resumo-laudo p {
        color: black !important;
    }
    
    .resumo-laudo strong {
        color: black !important;
    }
    
    /* AVISO CIENTÍFICO - VISÍVEL */
    .aviso-cientifico {
        background: white !important;
        border: 1px solid #000 !important;
        color: black !important;
    }
    
    /* PRIVACIDADE - VISÍVEL */
    .privacidade-box {
        background: white !important;
        border: 1px solid #000 !important;
        color: black !important;
    }
    
    /* RODAPÉ - VISÍVEL */
    .rodape {
        border-top: 1px solid #000 !important;
        color: black !important;
    }
    
    /* CONTAINER PRINCIPAL */
    .main .block-container {
        padding: 0.5cm !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* EVITAR QUEBRAS DE PÁGINA EM ELEMENTOS IMPORTANTES */
    .perfil-gigante, .meta-gigante, .card-com-explicacao, 
    .header-cafe, .header-almoco, .header-lanches, .header-jantar,
    .resumo-laudo {
        page-break-inside: avoid;
        break-inside: avoid;
    }
}
</style>
""", unsafe_allow_html=True)

# 10. SIDEBAR
with st.sidebar:
    st.markdown("### 👤 Perfil Biológico")
    st.markdown("---")
    
    peso_at = st.number_input("📊 Peso Atual (kg)", 30.0, 250.0, 85.8)
    alt_cm = st.number_input("📏 Altura (cm)", 100, 230, 164)
    idade = st.number_input("🎂 Idade (anos)", 10, 110, 47)
    sexo = st.selectbox("⚥ Sexo Biológico", ["Masculino", "Feminino"])
    
    st.markdown("---")
    st.markdown("### 🎯 Objetivos")
    
    # Objetivo principal: Perda ou Ganho de peso
    objetivo = st.radio("🎯 Seu objetivo principal:", ["Perda de peso", "Ganho de peso"], horizontal=True)
    
    # Meta de peso (pode ser menor ou maior que o atual)
    if objetivo == "Perda de peso":
        p_alvo = st.number_input("🎯 Meta de Peso (kg)", 10.0, peso_at - 0.1, peso_at - 10)
        st.caption(f"Para perda de peso, a meta deve ser menor que {peso_at} kg")
    else:
        p_alvo = st.number_input("🎯 Meta de Peso (kg)", peso_at + 0.1, 300.0, peso_at + 10)
        st.caption(f"Para ganho de peso, a meta deve ser maior que {peso_at} kg")
    
    opcoes_naf = {
        "Sedentário (Sem exercício)": 1.2,
        "Leve (1-3 dias/sem)": 1.375,
        "Moderado (3-5 dias/sem)": 1.55,
        "Intenso (6-7 dias/sem)": 1.725,
        "Atleta (Treino pesado 2x dia)": 1.9
    }
    naf_label = st.selectbox("🏃 Frequência de Atividade Física:", list(opcoes_naf.keys()))
    naf_val = opcoes_naf[naf_label]
    
    st.markdown("---")
    
    planejamento_tipo = st.radio("📅 Tipo de Planejamento:", ["Diário", "Semanal"], horizontal=True)
    if planejamento_tipo != st.session_state.planejamento_tipo:
        st.session_state.planejamento_tipo = planejamento_tipo
        st.rerun()
    
    st.markdown("---")
    st.info("🖨️ **IMPRESSÃO:** Botão abaixo → 3 pontinhos (⋮) → Imprimir → Margens: Mínimas")
    
    if st.button("📄 Versão para Impressão", use_container_width=True):
        st.session_state.modo_impressao = True
        st.rerun()

# 11. CARGA DE DADOS
@st.cache_data
def load_db():
    df_a = pd.read_csv('alimentos.csv') if os.path.exists('alimentos.csv') else pd.DataFrame()
    return df_a, pd.DataFrame(), pd.DataFrame()

df_taco, df_graxos, df_amino = load_db()

# 12. HEADER
st.markdown("""
<div class='banner-profissional'>
    <div class='icones-esportes'>🏋️‍♂️ 🏊‍♂️ 🚴‍♂️ 🏃‍♂️ 🧘‍♀️</div>
    <h1>BioGestão 360</h1>
    <div class='slogan'>Evolua seu treino junto com os nutrientes que movem o seu corpo</div>
</div>
""", unsafe_allow_html=True)

# 13. DOAÇÕES
with st.expander("💚 Apoie este projeto - Colaboração voluntária", expanded=False):
    col_pix, col_paypal = st.columns(2)
    with col_pix:
        st.markdown("### 📱 PIX")
        qr_img = gerar_qr_code_pix()
        st.image(qr_img, width=150)
        st.markdown("**Chave PIX (Aleatória):**")
        st.code("f3e890da-fb72-4e8c-a0cd-d88177457a30", language="text")
        st.caption("ADILSON GONCALVES XIMENES")
    with col_paypal:
        st.markdown("### 💳 PayPal")
        st.components.v1.html(get_paypal_html(), height=100)
        st.caption("Link: https://www.paypal.com/donate/?hosted_button_id=LQTE48R8SLWRG")
    st.caption("Sua contribuição ajuda a manter o projeto gratuito!")

# 14. POLÍTICA DE PRIVACIDADE
st.markdown("""
<div class='privacidade-box'>
    <b>🔒 POLÍTICA DE PRIVACIDADE (ZERO-FOOTPRINT):</b><br>
    ✅ Nenhum dado é enviado para servidores externos<br>
    ✅ Processamento 100% local no seu navegador<br>
    ✅ Ao fechar a aba, todas as informações são permanentemente deletadas
</div>
""", unsafe_allow_html=True)

# 15. AVISO CIENTÍFICO
st.markdown("""
<div class='aviso-cientifico'>
    <strong>📋 INFORMAÇÃO CIENTÍFICA:</strong> Baseado na Tabela TACO (UNICAMP) e equações Harris-Benedict.
    <strong>⚠️ SISTEMA EM DESENVOLVIMENTO - DADOS PODEM CONTER ERRO</strong>
</div>
""", unsafe_allow_html=True)

# 16. CÁLCULOS BIOMÉTRICOS
alt_m = alt_cm / 100
imc = peso_at / (alt_m ** 2)
if sexo == "Masculino":
    tmb = 66.47 + (13.75 * peso_at) + (5.0 * alt_cm) - (6.75 * idade)
else:
    tmb = 655.1 + (9.56 * peso_at) + (1.85 * alt_cm) - (4.67 * idade)
get_total = tmb * naf_val

composicao = calcular_composicao_corporal(peso_at, alt_cm, idade, sexo)

diferenca_meta = p_alvo - peso_at
if objetivo == "Perda de peso":
    if diferenca_meta > 0:
        texto_meta = f"🏆 Você já está abaixo da sua meta! Faltam {abs(diferenca_meta):.1f} kg para manter."
    elif diferenca_meta < 0:
        texto_meta = f"🎯 Você precisa perder {abs(diferenca_meta):.1f} kg para atingir sua meta!"
    else:
        texto_meta = "🎉 Parabéns! Meta alcançada!"
else:
    if diferenca_meta > 0:
        texto_meta = f"🎯 Você precisa ganhar {abs(diferenca_meta):.1f} kg para atingir sua meta!"
    elif diferenca_meta < 0:
        texto_meta = f"🏆 Você já está acima da sua meta! Faltam {abs(diferenca_meta):.1f} kg para manter."
    else:
        texto_meta = "🎉 Parabéns! Meta alcançada!"

# 17. PERFIL GIGANTE
st.markdown(f"""
<div class='perfil-gigante'>
    <div class='titulo'>📋 SEU PERFIL</div>
    <div class='dados-container'>
        <div class='dado-item'><div class='dado-icon'>⚖️</div><div class='dado-valor'>{peso_at} kg</div><div class='dado-label'>Peso</div></div>
        <div class='dado-item'><div class='dado-icon'>📏</div><div class='dado-valor'>{alt_cm} cm</div><div class='dado-label'>Altura</div></div>
        <div class='dado-item'><div class='dado-icon'>🎂</div><div class='dado-valor'>{idade} anos</div><div class='dado-label'>Idade</div></div>
        <div class='dado-item'><div class='dado-icon'>⚥</div><div class='dado-valor'>{sexo}</div><div class='dado-label'>Sexo</div></div>
    </div>
    <div class='meta-gigante'>
        <div class='meta-titulo'>🎯 META DE PESO - {objetivo.upper()}</div>
        <div class='meta-valor'>{p_alvo} kg</div>
        <div class='meta-mensagem'>{texto_meta}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 18. DASHBOARD
st.markdown("## ⚡ Metabolismo e Gasto Energético")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>⚡</div>
        <div class='card-valor'>{get_total:.0f} kcal</div>
        <div class='card-titulo'>Gasto Total (GET)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Total de calorias que seu corpo gasta por dia.<br>📊 <strong>Como usar:</strong> Para manter o peso, consuma esta quantidade.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>🔥</div>
        <div class='card-valor'>{tmb:.0f} kcal</div>
        <div class='card-titulo'>Metabolismo Basal (TMB)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Calorias queimadas em repouso total.<br>📊 <strong>Como usar:</strong> É o mínimo que seu corpo precisa para viver.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>📊</div>
        <div class='card-valor'>{composicao['imc']}</div>
        <div class='card-titulo'>Índice de Massa Corporal (IMC)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Relação entre peso e altura.<br>📊 <strong>Referência:</strong> 18.5-25 = Saudável | 25-30 = Sobrepeso | >30 = Obesidade</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>🎯</div>
        <div class='card-valor'>{composicao['peso_ideal']} kg</div>
        <div class='card-titulo'>Peso Ideal Estimado</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Peso considerado mais saudável para sua altura.<br>📊 <strong>Como usar:</strong> Meta de longo prazo baseada em estudos científicos.</div>
    </div>
    """, unsafe_allow_html=True)

# 19. COMPOSIÇÃO CORPORAL
st.markdown("---")
st.markdown("## 🧬 Composição Corporal")

col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown(f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>🎯</div>
        <div class='card-valor'>{composicao['percentual_gordura']}%</div>
        <div class='card-titulo'>Percentual de Gordura</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Porcentagem do seu corpo que é gordura.<br>📊 <strong>Referência:</strong> Homens: 10-25% | Mulheres: 18-32%</div>
    </div>
    """, unsafe_allow_html=True)

with col_g2:
    st.markdown(f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>⚖️</div>
        <div class='card-valor'>{composicao['massa_gordura']} kg</div>
        <div class='card-titulo'>Massa de Gordura</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Peso total da gordura no seu corpo.<br>📊 <strong>Como usar:</strong> Acompanhe a redução para perder peso saudável.</div>
    </div>
    """, unsafe_allow_html=True)

with col_g3:
    st.markdown(f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>💪</div>
        <div class='card-valor'>{composicao['massa_magra']} kg</div>
        <div class='card-titulo'>Massa Magra</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Músculos + ossos + órgãos.<br>📊 <strong>Como usar:</strong> Quanto maior, melhor para o metabolismo!</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 20. MONTAGEM DO PLANO ALIMENTAR
st.markdown("## 🍏 Montagem do Plano Alimentar")
st.info("💡 **Dica de precisão:** Utilize 'Peso Real (g/ml)' com balança para maior exatidão! Alimentos diferentes possuem densidades diferentes - uma 'unidade' de pão pode variar muito de tamanho!")

if st.session_state.planejamento_tipo == "Semanal":
    st.markdown("### 📅 Selecione o dia")
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    cols = st.columns(7)
    for i, dia in enumerate(dias_semana):
        with cols[i]:
            if st.session_state.dia_atual == dia:
                st.markdown(f"<div class='dia-btn-selected'>{dia} ✅</div>", unsafe_allow_html=True)
            else:
                if st.button(dia, key=f"dia_{dia}", use_container_width=True):
                    st.session_state.dia_atual = dia
                    st.rerun()
    st.markdown(f"<div style='text-align: center; margin: 15px 0;'><div style='background: linear-gradient(135deg, #f59e0b, #ef4444); color: white; padding: 10px 20px; border-radius: 50px; display: inline-block; font-weight: bold;'>📌 Editando: {st.session_state.dia_atual}</div></div>", unsafe_allow_html=True)
    st.markdown("---")

if not st.session_state.modo_impressao and not df_taco.empty:
    with st.container():
        col1, col2, col3, col4 = st.columns([1.5, 3, 1, 1])
        with col1: 
            refeicao_sel = st.selectbox("Refeição", ["Café da Manhã", "Almoço", "Lanches", "Jantar"])
        with col2: 
            alimento_sel = st.selectbox("Alimento", df_taco['Descrição dos alimentos'].unique())
        with col3: 
            qtd_unidade = st.number_input("Unidades", 0.0, 50.0, 1.0)
        with col4: 
            peso_real = st.number_input("Peso Real (g/ml)", 0.0, 2000.0, 0.0)

    if st.button("➕ Adicionar ao Plano", use_container_width=True):
        item = df_taco[df_taco['Descrição dos alimentos'] == alimento_sel].iloc[0]
        is_liquido = any(x in alimento_sel.lower() for x in ["suco", "leite", "café", "bebida", "água", "chá"])
        
        if peso_real > 0:
            peso_final = peso_real
            label_qtd = f"{peso_real}ml" if is_liquido else f"{peso_real}g"
        else:
            base_peso = 200 if is_liquido else 50
            peso_final = qtd_unidade * base_peso
            label_qtd = f"{qtd_unidade} unid (~{peso_final}{'ml' if is_liquido else 'g'})"
        
        fator_calc = peso_final / 100
        risco_oms = verificar_risco_oms(alimento_sel)
        
        novo_item = {
            "Ali": alimento_sel, "Qtd": label_qtd,
            "Kcal": round(item['Energia..kcal.'] * fator_calc, 1),
            "P": round(item['Proteína..g.'] * fator_calc, 1),
            "C": round(item['Carboidrato..g.'] * fator_calc, 1),
            "G": round(item['Lipídeos..g.'] * fator_calc, 1),
            "Risco": risco_oms
        }
        
        if st.session_state.planejamento_tipo == "Diário":
            st.session_state.cardapio[refeicao_sel].append(novo_item)
        else:
            st.session_state.cardapio_semanal[st.session_state.dia_atual][refeicao_sel].append(novo_item)
        st.rerun()

st.markdown("---")

# 21. EXIBIÇÃO DO PLANO
if st.session_state.planejamento_tipo == "Diário":
    st.markdown("### 📋 Seu Cardápio de Hoje")
    
    # Café da Manhã
    if st.session_state.cardapio["Café da Manhã"]:
        st.markdown("<div class='header-cafe'>🌅 CAFÉ DA MANHÃ</div>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state.cardapio["Café da Manhã"]):
            colA, colB, colC = st.columns([3, 4, 1])
            with colA:
                st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
            with colB:
                st.markdown(f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>", unsafe_allow_html=True)
            with colC:
                if st.button("🗑️", key=f"del_cafe_{idx}"):
                    remover_item_diario("Café da Manhã", idx)
            if item.get('Risco'):
                st.markdown(f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>", unsafe_allow_html=True)
            st.divider()
    
    # Almoço
    if st.session_state.cardapio["Almoço"]:
        st.markdown("<div class='header-almoco'>🍜 ALMOÇO</div>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state.cardapio["Almoço"]):
            colA, colB, colC = st.columns([3, 4, 1])
            with colA:
                st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
            with colB:
                st.markdown(f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>", unsafe_allow_html=True)
            with colC:
                if st.button("🗑️", key=f"del_almoco_{idx}"):
                    remover_item_diario("Almoço", idx)
            if item.get('Risco'):
                st.markdown(f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>", unsafe_allow_html=True)
            st.divider()
    
    # Lanches
    if st.session_state.cardapio["Lanches"]:
        st.markdown("<div class='header-lanches'>🍎 LANCHES</div>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state.cardapio["Lanches"]):
            colA, colB, colC = st.columns([3, 4, 1])
            with colA:
                st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
            with colB:
                st.markdown(f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>", unsafe_allow_html=True)
            with colC:
                if st.button("🗑️", key=f"del_lanches_{idx}"):
                    remover_item_diario("Lanches", idx)
            if item.get('Risco'):
                st.markdown(f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>", unsafe_allow_html=True)
            st.divider()
    
    # Jantar
    if st.session_state.cardapio["Jantar"]:
        st.markdown("<div class='header-jantar'>🌙 JANTAR</div>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state.cardapio["Jantar"]):
            colA, colB, colC = st.columns([3, 4, 1])
            with colA:
                st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
            with colB:
                st.markdown(f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>", unsafe_allow_html=True)
            with colC:
                if st.button("🗑️", key=f"del_jantar_{idx}"):
                    remover_item_diario("Jantar", idx)
            if item.get('Risco'):
                st.markdown(f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>", unsafe_allow_html=True)
            st.divider()

else:
    # MODO SEMANAL
    st.markdown(f"### 📅 Planejamento Semanal - {st.session_state.dia_atual}")
    
    refeicoes = ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
    headers = {"Café da Manhã": "header-cafe", "Almoço": "header-almoco", "Lanches": "header-lanches", "Jantar": "header-jantar"}
    icons = {"Café da Manhã": "🌅", "Almoço": "🍜", "Lanches": "🍎", "Jantar": "🌙"}
    
    for refeicao in refeicoes:
        itens = st.session_state.cardapio_semanal.get(st.session_state.dia_atual, {}).get(refeicao, [])
        if itens:
            st.markdown(f"<div class='{headers[refeicao]}'>{icons[refeicao]} {refeicao.upper()}</div>", unsafe_allow_html=True)
            for idx, item in enumerate(itens):
                colA, colB, colC = st.columns([3, 4, 1])
                with colA:
                    st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
                with colB:
                    st.markdown(f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>", unsafe_allow_html=True)
                with colC:
                    if st.button("🗑️", key=f"del_semanal_{refeicao}_{idx}"):
                        remover_item_semanal(st.session_state.dia_atual, refeicao, idx)
                if item.get('Risco'):
                    st.markdown(f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>", unsafe_allow_html=True)
                st.divider()
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button(f"🗑️ Limpar {st.session_state.dia_atual}", use_container_width=True):
            limpar_dia_semanal(st.session_state.dia_atual)
    with col_btn2:
        if st.button("🗑️ Limpar Semana Inteira", use_container_width=True):
            limpar_semana_completa()

st.markdown("---")

# 22. CÁLCULO DOS TOTAIS (DIÁRIO OU SEMANAL)
totais = calcular_totais_cardapio(st.session_state.cardapio, st.session_state.planejamento_tipo, st.session_state.cardapio_semanal)

total_kcal = totais['total_kcal']
total_prot = totais['total_prot']
total_carb = totais['total_carb']
total_gord = totais['total_gord']
media_diaria = totais['media_diaria_kcal']
dias = totais['dias']

# Saldo energético baseado na MÉDIA DIÁRIA
saldo_diario = get_total - media_diaria
variacao_semanal = abs((saldo_diario * 7) / 7700)
variacao_30dias = abs((saldo_diario * 30) / 7700)

# 23. GRÁFICOS
if total_kcal > 0:
    st.markdown("## 📊 Análise Nutricional")
    
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        macros_data = pd.DataFrame({
            'Macronutriente': ['Proteínas', 'Carboidratos', 'Gorduras'],
            'Calorias': [total_prot * 4, total_carb * 4, total_gord * 9]
        })
        fig_pizza = px.pie(macros_data, values='Calorias', names='Macronutriente', 
                           title='Distribuição dos Macronutrientes',
                           color_discrete_sequence=['#ef4444', '#3b82f6', '#f59e0b'])
        fig_pizza.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col_graf2:
        balanco_data = pd.DataFrame({
            'Categoria': ['Gasto Total (GET)', 'Consumo Médio', 'Diferença'],
            'Valor (kcal)': [get_total, media_diaria, abs(saldo_diario)]
        })
        fig_balanco = px.bar(balanco_data, x='Categoria', y='Valor (kcal)', 
                              title='Balanço Energético',
                              color='Categoria',
                              color_discrete_map={'Gasto Total (GET)': '#ef4444', 'Consumo Médio': '#10b981', 'Diferença': '#f59e0b'})
        fig_balanco.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
        st.plotly_chart(fig_balanco, use_container_width=True)
    
    st.markdown("""
    <div style='background: var(--bg-secondary); border-radius: 10px; padding: 10px 15px; margin-top: 10px; font-size: 12px; display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;'>
        <span>🔥 <strong>kcal</strong> = Energia total do alimento</span>
        <span>🥩 <strong>Proteínas (g)</strong> = Essenciais para construção muscular</span>
        <span>🍞 <strong>Carboidratos (g)</strong> = Principal fonte de energia do corpo</span>
        <span>🥑 <strong>Gorduras (g)</strong> = Importantes para hormônios e vitaminas</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

# 24. LAUDO TÉCNICO COMPLETO
st.markdown("## 📋 LAUDO TÉCNICO DE VIABILIDADE ALIMENTAR")

# Explicação do período
if st.session_state.planejamento_tipo == "Diário":
    st.caption(f"📅 **Período analisado:** Hoje (1 dia) | Total de {total_kcal:.1f} kcal no dia")
else:
    st.caption(f"📅 **Período analisado:** Semana completa (7 dias) | Total de {total_kcal:.1f} kcal na semana | Média diária: {media_diaria:.1f} kcal")

col1, col2, col3 = st.columns(3)
with col1: 
    st.metric("🥗 Consumo Planejado", f"{media_diaria:.1f} kcal" if st.session_state.planejamento_tipo == "Semanal" else f"{total_kcal:.1f} kcal")
with col2: 
    st.metric("⚡ Gasto Estimado (GET)", f"{get_total:.0f} kcal")
with col3: 
    delta_texto = "Déficit" if saldo_diario > 0 else "Superávit"
    st.metric("💪 Saldo Energético Diário", f"{abs(saldo_diario):.1f} kcal", delta_texto)

st.markdown("---")
st.markdown("#### 🍽️ MACRONUTRIENTES TOTAIS DO PLANO")

col_p, col_c, col_g = st.columns(3)

if st.session_state.planejamento_tipo == "Diário":
    with col_p: 
        st.metric("🥩 Proteínas", f"{total_prot:.1f} g", f"{((total_prot*4)/total_kcal*100 if total_kcal>0 else 0):.1f}% das calorias")
    with col_c: 
        st.metric("🍞 Carboidratos", f"{total_carb:.1f} g", f"{((total_carb*4)/total_kcal*100 if total_kcal>0 else 0):.1f}% das calorias")
    with col_g: 
        st.metric("🥑 Gorduras", f"{total_gord:.1f} g", f"{((total_gord*9)/total_kcal*100 if total_kcal>0 else 0):.1f}% das calorias")
else:
    with col_p: 
        st.metric("🥩 Proteínas (semana)", f"{total_prot:.1f} g", f"Média: {total_prot/7:.1f}g/dia")
    with col_c: 
        st.metric("🍞 Carboidratos (semana)", f"{total_carb:.1f} g", f"Média: {total_carb/7:.1f}g/dia")
    with col_g: 
        st.metric("🥑 Gorduras (semana)", f"{total_gord:.1f} g", f"Média: {total_gord/7:.1f}g/dia")

st.markdown("---")
st.markdown("#### 📊 ESTIMATIVA DE RESULTADOS")

col_result1, col_result2, col_result3 = st.columns(3)

with col_result1:
    if objetivo == "Perda de peso":
        if saldo_diario > 0:
            st.success(f"🎯 **Você está em DÉFICIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a menos por dia, seu corpo vai usar gordura como energia.")
        else:
            st.warning(f"⚠️ **Você está em SUPERÁVIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a mais por dia, seu corpo pode armazenar gordura.")
    else:
        if saldo_diario < 0:
            st.success(f"🎯 **Você está em SUPERÁVIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a mais por dia, ideal para ganho de massa muscular.")
        else:
            st.warning(f"⚠️ **Você está em DÉFICIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a menos por dia, pode prejudicar o ganho muscular.")

with col_result2:
    if st.session_state.planejamento_tipo == "Diário":
        st.info(f"📉 **Projeção em 7 dias:** {variacao_semanal:.2f} kg\n\n📉 **Projeção em 30 dias:** {variacao_30dias:.2f} kg")
    else:
        st.info(f"📉 **Projeção semanal:** {variacao_semanal:.2f} kg\n\n📉 **Projeção em 30 dias:** {variacao_30dias:.2f} kg")

with col_result3:
    if saldo_diario != 0:
        if objetivo == "Perda de peso" and saldo_diario > 0:
            semanas_meta = abs(diferenca_meta) / (variacao_semanal) if variacao_semanal > 0 else 0
            st.success(f"⏱️ **Tempo estimado para meta:** {max(1, int(semanas_meta))} semanas")
        elif objetivo == "Ganho de peso" and saldo_diario < 0:
            semanas_meta = abs(diferenca_meta) / (variacao_semanal) if variacao_semanal > 0 else 0
            st.success(f"⏱️ **Tempo estimado para meta:** {max(1, int(semanas_meta))} semanas")
        else:
            st.warning("⚡ **Ajuste seu consumo para atingir a meta!**")
    else:
        st.info("✅ **Manutenção!** Você está consumindo exatamente o que gasta.")

# 25. RESUMO COMPLETO PARA IMPRESSÃO
st.markdown("---")
st.markdown("## 🖨️ RESUMO COMPLETO PARA IMPRESSÃO")
st.markdown("*Esta seção contém todos os alimentos selecionados para fácil impressão - sem botões de excluir*")

todos_alimentos = []
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

if st.session_state.planejamento_tipo == "Diário":
    for refeicao, itens in st.session_state.cardapio.items():
        for item in itens:
            todos_alimentos.append({
                "Dia": "Hoje", "Refeição": refeicao, "Alimento": item['Ali'],
                "Quantidade": item['Qtd'], "Kcal": item['Kcal'], "Proteínas(g)": item['P'],
                "Carboidratos(g)": item['C'], "Gorduras(g)": item['G'], 
                "Alerta OMS": item.get('Risco', '')[:50] if item.get('Risco') else '-'
            })
else:
    for dia in dias_semana:
        for refeicao in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]:
            for item in st.session_state.cardapio_semanal.get(dia, {}).get(refeicao, []):
                todos_alimentos.append({
                    "Dia": dia, "Refeição": refeicao, "Alimento": item['Ali'],
                    "Quantidade": item['Qtd'], "Kcal": item['Kcal'], "Proteínas(g)": item['P'],
                    "Carboidratos(g)": item['C'], "Gorduras(g)": item['G'],
                    "Alerta OMS": item.get('Risco', '')[:50] if item.get('Risco') else '-'
                })

if todos_alimentos:
    df_resumo = pd.DataFrame(todos_alimentos)
    st.dataframe(df_resumo, use_container_width=True, hide_index=True)
    csv = df_resumo.to_csv(index=False, encoding='utf-8-sig')
    st.download_button("📥 Baixar Resumo em CSV", data=csv, file_name="resumo_alimentar.csv", mime="text/csv")
else:
    st.info("ℹ️ Nenhum alimento adicionado ainda. Adicione alimentos para gerar o resumo.")

# 26. LAUDO FINAL RESUMIDO (para o resumo de impressão)
st.markdown("---")
st.markdown("## 📋 RESUMO DO LAUDO TÉCNICO")

# Calcular semanas para meta
if saldo_diario != 0:
    if objetivo == "Perda de peso" and saldo_diario > 0:
        semanas_meta = abs(diferenca_meta) / (variacao_semanal) if variacao_semanal > 0 else 0
        texto_tempo = f"{max(1, int(semanas_meta))} semanas"
    elif objetivo == "Ganho de peso" and saldo_diario < 0:
        semanas_meta = abs(diferenca_meta) / (variacao_semanal) if variacao_semanal > 0 else 0
        texto_tempo = f"{max(1, int(semanas_meta))} semanas"
    else:
        texto_tempo = "Ajuste necessário"
else:
    texto_tempo = "Manutenção"

st.markdown(f"""
<div class='resumo-laudo'>
    <h4>📊 Resumo da Análise</h4>
    <p><strong>📅 Período analisado:</strong> {'Hoje (1 dia)' if st.session_state.planejamento_tipo == "Diário" else 'Semana completa (7 dias)'}</p>
    <p><strong>🥗 Consumo total:</strong> {total_kcal:.1f} kcal</p>
    <p><strong>📊 Média diária:</strong> {media_diaria:.1f} kcal</p>
    <p><strong>⚡ Gasto diário (GET):</strong> {get_total:.0f} kcal</p>
    <p><strong>💪 Saldo diário:</strong> {abs(saldo_diario):.1f} kcal <strong style='color: {"#fbbf24" if saldo_diario > 0 else "#f87171"};'>{"Déficit" if saldo_diario > 0 else "Superávit"}</strong></p>
    <p><strong>📉 Projeção de variação em 30 dias:</strong> {variacao_30dias:.2f} kg</p>
    <p><strong>⏱️ Tempo estimado para meta:</strong> {texto_tempo}</p>
</div>
""", unsafe_allow_html=True)

# 26.5. BOTÃO PARA BAIXAR LAUDO COMPLETO EM CSV
st.markdown("---")
st.markdown("### 📥 Exportar Dados Completos")

# Classificação IMC
if imc < 18.5:
    classificacao_imc = "Abaixo do peso"
elif imc < 25:
    classificacao_imc = "Peso normal"
elif imc < 30:
    classificacao_imc = "Sobrepeso"
elif imc < 35:
    classificacao_imc = "Obesidade Grau I"
elif imc < 40:
    classificacao_imc = "Obesidade Grau II"
else:
    classificacao_imc = "Obesidade Grau III"

# Criar DataFrame com todas as informações do laudo
dados_laudo = {
    "Informação": [
        "📅 Data do relatório",
        "📋 Tipo de Planejamento",
        "📅 Período analisado",
        "🎯 Objetivo",
        "⚖️ Peso Atual (kg)",
        "📏 Altura (cm)",
        "🎂 Idade (anos)",
        "⚥ Sexo",
        "🎯 Meta de Peso (kg)",
        "🏃 Frequência de Atividade Física",
        "⚡ Gasto Total (GET) - kcal/dia",
        "🔥 Metabolismo Basal (TMB) - kcal/dia",
        "📊 IMC Atual",
        "📊 Classificação IMC",
        "🎯 Peso Ideal Estimado (kg)",
        "🎯 Percentual de Gordura (%)",
        "⚖️ Massa de Gordura (kg)",
        "💪 Massa Magra (kg)",
        "🥗 Consumo Total do Período (kcal)",
        "📊 Média Diária de Consumo (kcal)",
        "💪 Saldo Energético Diário (kcal)",
        "📊 Status do Saldo",
        "📉 Projeção de Variação em 30 dias (kg)",
        "⏱️ Tempo Estimado para Meta",
        "🥩 Macronutrientes - Proteínas (g)",
        "🍞 Macronutrientes - Carboidratos (g)",
        "🥑 Macronutrientes - Gorduras (g)",
        "🥩 % Calórico de Proteínas",
        "🍞 % Calórico de Carboidratos",
        "🥑 % Calórico de Gorduras"
    ],
    "Valor": [
        pd.Timestamp.now().strftime('%d/%m/%Y %H:%M'),
        st.session_state.planejamento_tipo,
        "Hoje (1 dia)" if st.session_state.planejamento_tipo == "Diário" else "Semana completa (7 dias)",
        objetivo,
        peso_at,
        alt_cm,
        idade,
        sexo,
        p_alvo,
        naf_label,
        get_total,
        tmb,
        composicao['imc'],
        classificacao_imc,
        composicao['peso_ideal'],
        composicao['percentual_gordura'],
        composicao['massa_gordura'],
        composicao['massa_magra'],
        total_kcal,
        media_diaria,
        abs(saldo_diario),
        "Déficit" if saldo_diario > 0 else "Superávit",
        variacao_30dias,
        texto_tempo,
        total_prot,
        total_carb,
        total_gord,
        f"{((total_prot*4)/total_kcal*100 if total_kcal>0 else 0):.1f}%",
        f"{((total_carb*4)/total_kcal*100 if total_kcal>0 else 0):.1f}%",
        f"{((total_gord*9)/total_kcal*100 if total_kcal>0 else 0):.1f}%"
    ]
}

df_laudo = pd.DataFrame(dados_laudo)

# Botões de download
col_down1, col_down2 = st.columns(2)

with col_down1:
    csv_laudo = df_laudo.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        "📊 Baixar Laudo Técnico Completo (CSV)", 
        data=csv_laudo, 
        file_name=f"laudo_biogestao_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv", 
        mime="text/csv",
        use_container_width=True
    )

with col_down2:
    if todos_alimentos:
        st.download_button(
            "🍽️ Baixar Cardápio Detalhado (CSV)", 
            data=df_resumo.to_csv(index=False, encoding='utf-8-sig'), 
            file_name=f"cardapio_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv", 
            mime="text/csv",
            use_container_width=True
        )

st.caption("Os arquivos CSV podem ser abertos no Excel, Google Sheets ou qualquer editor de planilhas")

# 27. INFORMAÇÃO OMS
with st.expander("📋 Informações OMS sobre Classificação de Alimentos"):
    st.markdown("""
    ### Classificação da OMS/IARC para alimentos:
    
    | Grupo | Classificação | Alimentos | Recomendação |
    |-------|--------------|-----------|--------------|
    | **Grupo 1** | **Cancerígeno para humanos** | Carnes processadas (salsicha, presunto, bacon, salame, mortadela), Bebidas alcoólicas, Peixe salgado chinês | Evitar ou reduzir drasticamente |
    | **Grupo 2A** | **Provavelmente cancerígeno** | Carne vermelha (bovina, suína, ovina, caprina) | Limitar a 500g cozida por semana |
    | **Grupo 2B** | **Possivelmente cancerígeno** | Aspartame, Bebidas muito quentes (>65°C) | Consumo moderado |
    
    **Recomendações práticas:**
    - ✅ Prefira carnes brancas (frango, peixe)
    - ✅ Cozinhe em temperaturas mais baixas (vapor, cozido)
    - ✅ Evite frituras e churrascos em excesso
    - ✅ Aumente consumo de fibras (frutas, verduras, legumes)
    
    **Fonte:** Agência Internacional de Pesquisa sobre o Câncer (IARC/OMS)
    """)

# continua com o resto do código...

# 28. BOTÃO DE LIMPAR (modo diário)
if st.session_state.planejamento_tipo == "Diário":
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        total_itens = sum(len(itens) for itens in st.session_state.cardapio.values())
        if total_itens > 0 and not st.session_state.modo_impressao:
            if st.button("🗑️ LIMPAR CARDÁPIO COMPLETO", use_container_width=True):
                limpar_cardapio()

# 29. SAIR DO MODO IMPRESSÃO
if st.session_state.modo_impressao:
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔙 Sair do Modo Impressão", use_container_width=True):
            st.session_state.modo_impressao = False
            st.rerun()

# 30. RODAPÉ
st.markdown("""
<div style='text-align: center; font-size: 11px; color: #666; padding: 15px;'>
    <b>BioGestão 360 v3.0</b> | Tabela TACO (UNICAMP) | Equações Harris-Benedict<br>
    <b>⚠️ SISTEMA EM DESENVOLVIMENTO - DADOS PODEM CONTER ERRO</b><br>
    Consulte sempre um nutricionista ou médico antes de fazer mudanças significativas na sua alimentação.
</div>
""", unsafe_allow_html=True)