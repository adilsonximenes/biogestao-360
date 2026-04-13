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
st.set_page_config(
    page_title="BioGestão 360 - Profissional", layout="wide", page_icon="🏋️"
)

# 2. INICIALIZAÇÕES
if "modo_impressao" not in st.session_state:
    st.session_state.modo_impressao = False
if "planejamento_tipo" not in st.session_state:
    st.session_state.planejamento_tipo = "Diário"
if "cardapio_semanal" not in st.session_state:
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    st.session_state.cardapio_semanal = {
        dia: {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]}
        for dia in dias_semana
    }
if "dia_atual" not in st.session_state:
    st.session_state.dia_atual = "Segunda"
if "cardapio" not in st.session_state:
    st.session_state.cardapio = {
        k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
    }


# 3. FUNÇÃO PARA GERAR QR CODE PIX
def gerar_qr_code_pix():
    pix_data = "00020126580014br.gov.bcb.pix0136f3e890da-fb72-4e8c-a0cd-d88177457a305204000053039865802BR5925ADILSON GONCALVES XIMENES6012BELFORD ROXO62180514AdilsonXimenes6304B1CB"
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(pix_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
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
        "grupo1": {
            "alimentos": [
                "salsicha",
                "presunto",
                "linguiça",
                "bacon",
                "salame",
                "mortadela",
                "nuggets",
                "peixe salgado",
            ],
            "mensagem": "⚠️ GRUPO 1: CANCERÍGENO PARA HUMANOS! Consumo diário de 50g aumenta em 18% o risco de câncer colorretal.",
        },
        "grupo2a": {
            "alimentos": [
                "carne bovina",
                "carne de porco",
                "carneiro",
                "cordeiro",
                "vitela",
            ],
            "mensagem": "⚠️ GRUPO 2A: PROVAVELMENTE CANCERÍGENO! Limite a 500g por semana.",
        },
        "grupo2b": {
            "alimentos": [
                "aspartame",
                "bebida adoçada",
                "refrigerante diet",
                "adoçante artificial",
            ],
            "mensagem": "⚠️ GRUPO 2B: POSSIVELMENTE CANCERÍGENO! Ingestão diária aceitável: 40mg/kg.",
        },
    }


ALIMENTOS_RISCO = carregar_alimentos_risco()


def verificar_risco_oms(nome_alimento):
    nome_lower = nome_alimento.lower()
    for item in ALIMENTOS_RISCO["grupo1"]["alimentos"]:
        if item in nome_lower:
            return ALIMENTOS_RISCO["grupo1"]["mensagem"]
    for item in ALIMENTOS_RISCO["grupo2a"]["alimentos"]:
        if item in nome_lower:
            return ALIMENTOS_RISCO["grupo2a"]["mensagem"]
    for item in ALIMENTOS_RISCO["grupo2b"]["alimentos"]:
        if item in nome_lower:
            return ALIMENTOS_RISCO["grupo2b"]["mensagem"]
    return None


# 6. FUNÇÃO PARA CALCULAR COMPOSIÇÃO CORPORAL
def calcular_composicao_corporal(peso, altura, idade, sexo):
    altura_m = altura / 100
    imc = peso / (altura_m**2)

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

    peso_ideal = imc_ideal * (altura_m**2)

    return {
        "percentual_gordura": round(percentual_gordura, 1),
        "massa_gordura": round(massa_gordura, 1),
        "massa_magra": round(massa_magra, 1),
        "peso_ideal": round(peso_ideal, 1),
        "imc": round(imc, 1),
    }


# 7. FUNÇÃO PARA CALCULAR TOTAIS (DIÁRIO OU SEMANAL)
def calcular_totais_cardapio(cardapio, planejamento_tipo, cardapio_semanal=None):
    if planejamento_tipo == "Diário":
        total_kcal = sum(item["Kcal"] for ref in cardapio.values() for item in ref)
        total_prot = sum(item["P"] for ref in cardapio.values() for item in ref)
        total_carb = sum(item["C"] for ref in cardapio.values() for item in ref)
        total_gord = sum(item["G"] for ref in cardapio.values() for item in ref)
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
                    total_kcal += item["Kcal"]
                    total_prot += item["P"]
                    total_carb += item["C"]
                    total_gord += item["G"]

    return {
        "total_kcal": total_kcal,
        "total_prot": total_prot,
        "total_carb": total_carb,
        "total_gord": total_gord,
        "media_diaria_kcal": total_kcal / dias if dias > 0 else 0,
        "dias": dias,
    }


# 8. FUNÇÕES DE LIMPEZA
def limpar_cardapio():
    if st.session_state.planejamento_tipo == "Diário":
        st.session_state.cardapio = {
            k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
        }
    else:
        st.session_state.cardapio_semanal[st.session_state.dia_atual] = {
            k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
        }
    st.success("✅ Cardápio limpo com sucesso!")
    st.rerun()


def remover_item_semanal(dia, refeicao, idx):
    st.session_state.cardapio_semanal[dia][refeicao].pop(idx)
    st.rerun()


def remover_item_diario(refeicao, idx):
    st.session_state.cardapio[refeicao].pop(idx)
    st.rerun()


def limpar_dia_semanal(dia):
    st.session_state.cardapio_semanal[dia] = {
        k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
    }
    st.success(f"✅ Cardápio de {dia} limpo!")
    st.rerun()


def limpar_semana_completa():
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    for dia in dias_semana:
        st.session_state.cardapio_semanal[dia] = {
            k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
        }
    st.success("✅ Semana inteira limpa!")
    st.rerun()


# 9. CSS PROFISSIONAL
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    .banner-profissional {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
        padding: 25px; border-radius: 20px; margin-bottom: 20px; text-align: center;
        position: relative; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .banner-profissional::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer { 100% { left: 100%; } }
    
    .icones-esportes { font-size: 40px; margin-bottom: 10px; letter-spacing: 15px; }
    .banner-profissional h1 { font-size: 45px; font-weight: 800; margin: 0;
        background: linear-gradient(135deg, #ffd700, #ff8c00, #ff4500);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .slogan { font-size: 16px; color: #94a3b8; margin-top: 8px; letter-spacing: 1px; }
    
    .perfil-gigante {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 20px; padding: 20px; margin: 15px 0; text-align: center;
        border: 2px solid #ffd700; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .perfil-gigante .titulo { font-size: 22px; font-weight: 800; color: #ffd700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; }
    .perfil-gigante .dados-container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }
    .perfil-gigante .dado-item { background: rgba(255,255,255,0.15); padding: 10px 20px; border-radius: 15px; min-width: 120px; }
    .perfil-gigante .dado-icon { font-size: 30px; margin-bottom: 5px; }
    .perfil-gigante .dado-valor { font-size: 28px; font-weight: 800; color: white; line-height: 1; }
    .perfil-gigante .dado-label { font-size: 12px; color: #94a3b8; margin-top: 5px; }
    
    .meta-gigante {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        border-radius: 20px; padding: 15px; margin-top: 10px; text-align: center;
        border: 2px solid #ffd700;
    }
    .meta-gigante .meta-titulo { font-size: 18px; font-weight: 600; color: rgba(255,255,255,0.9); margin-bottom: 10px; }
    .meta-gigante .meta-valor { font-size: 50px; font-weight: 900; color: white; line-height: 1; margin: 5px 0; }
    .meta-gigante .meta-mensagem { font-size: 16px; font-weight: 700; color: #ffd700; margin-top: 10px;
        background: rgba(0,0,0,0.3); display: inline-block; padding: 5px 20px; border-radius: 50px; }
    
    .card-com-explicacao {
        background: var(--bg-secondary); border-radius: 12px; padding: 12px; text-align: center;
        border: 1px solid var(--border-color); height: 100%;
    }
    .card-icon { font-size: 28px; margin-bottom: 5px; }
    .card-valor { font-size: 24px; font-weight: bold; }
    .card-titulo { font-size: 14px; font-weight: 600; margin: 5px 0; }
    .card-explicacao { font-size: 11px; color: var(--text-light); margin-top: 8px;
        padding-top: 8px; border-top: 1px solid var(--border-color); }
    
    .header-cafe { background: linear-gradient(90deg, #f59e0b, #fbbf24); color: white; padding: 15px;
        border-radius: 12px; margin-top: 20px; margin-bottom: 15px; font-size: 20px; font-weight: bold; }
    .header-almoco { background: linear-gradient(90deg, #ef4444, #f87171); color: white; padding: 15px;
        border-radius: 12px; margin-top: 20px; margin-bottom: 15px; font-size: 20px; font-weight: bold; }
    .header-lanches { background: linear-gradient(90deg, #10b981, #34d399); color: white; padding: 15px;
        border-radius: 12px; margin-top: 20px; margin-bottom: 15px; font-size: 20px; font-weight: bold; }
    .header-jantar { background: linear-gradient(90deg, #8b5cf6, #a78bfa); color: white; padding: 15px;
        border-radius: 12px; margin-top: 20px; margin-bottom: 15px; font-size: 20px; font-weight: bold; }
    
    .macro-tag-kcal { display: inline-block; background: #ef4444; color: white; padding: 5px 12px;
        border-radius: 20px; font-size: 13px; font-weight: bold; margin-right: 8px; }
    .macro-tag-proteina { display: inline-block; background: #3b82f6; color: white; padding: 5px 12px;
        border-radius: 20px; font-size: 13px; font-weight: bold; margin-right: 8px; }
    .macro-tag-carb { display: inline-block; background: #f59e0b; color: white; padding: 5px 12px;
        border-radius: 20px; font-size: 13px; font-weight: bold; margin-right: 8px; }
    .macro-tag-gordura { display: inline-block; background: #10b981; color: white; padding: 5px 12px;
        border-radius: 20px; font-size: 13px; font-weight: bold; margin-right: 8px; }
    
    .dia-btn-selected { background: linear-gradient(135deg, #f59e0b, #ef4444); color: white;
        border: 2px solid #ffd700; text-align: center; padding: 10px; border-radius: 10px; font-weight: bold; }
    
    .alerta-oms-grupo1 { background-color: #dc2626; color: white; padding: 12px; border-radius: 8px;
        margin: 10px 0; font-size: 13px; border-left: 5px solid #ffd700; }
    .alerta-oms-grupo2a { background-color: #f59e0b; color: white; padding: 12px; border-radius: 8px;
        margin: 10px 0; font-size: 13px; border-left: 5px solid #dc2626; }
    .alerta-oms-grupo2b { background-color: #8b5cf6; color: white; padding: 12px; border-radius: 8px;
        margin: 10px 0; font-size: 13px; border-left: 5px solid #f59e0b; }
    
    .aviso-cientifico { background: linear-gradient(135deg, #1e293b, #0f172a);
        border-left: 4px solid #f59e0b; padding: 10px 15px; border-radius: 8px;
        margin-bottom: 15px; font-size: 12px; color: #cbd5e1; }
    .privacidade-box { background-color: var(--bg-secondary); padding: 15px; border-radius: 10px;
        border-left: 5px solid #10b981; margin: 15px 0; font-size: 12px; }
    
    .resumo-laudo {
        background: linear-gradient(135deg, #1e293b, #0f172a) !important;
        border: 2px solid #ffd700 !important; border-radius: 15px !important;
        padding: 20px !important; margin: 15px 0 !important; color: #ffffff !important;
    }
    .resumo-laudo h4 { color: #ffd700 !important; margin-bottom: 15px !important; font-size: 18px !important; }
    .resumo-laudo p { color: #ffffff !important; margin: 10px 0 !important; font-size: 14px !important; line-height: 1.5 !important; }
    .resumo-laudo strong { color: #fbbf24 !important; }
    
/* CORREÇÃO - EQUIPAMENTO ADIPÔMETRO */
.equipamento-adipometro {
    background: linear-gradient(135deg, #1e3a5f, #0f172a);
    border-left: 5px solid #3b82f6;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 10px 0;
    color: #ffffff !important;
}

.equipamento-adipometro strong {
    color: #fbbf24 !important;
}

/* CORREÇÃO - EQUIPAMENTO FITA MÉTRICA */
.equipamento-fita {
    background: linear-gradient(135deg, #1e3a5f, #0f172a);
    border-left: 5px solid #10b981;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 10px 0;
    color: #ffffff !important;
}

.equipamento-fita strong {
    color: #fbbf24 !important;
}

/* CORREÇÃO - EQUIPAMENTO COMPLEMENTAR */
.equipamento-complementar {
    background: linear-gradient(135deg, #1e3a5f, #0f172a);
    border-left: 5px solid #f59e0b;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 10px 0;
    color: #ffffff !important;
}

.equipamento-complementar strong {
    color: #fbbf24 !important;
}
    
    /* IMPRESSAO - CORRIGIDA */
    @media print {
        .stSidebar, [data-testid="stSidebarContent"] {
            display: none !important;
        }
        
        * {
            color: black !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        body, .stApp, .main, .block-container, div, section, 
        p, h1, h2, h3, h4, h5, h6, span, li, .stMarkdown, .stMetric,
        .card-com-explicacao, .perfil-gigante, .meta-gigante,
        .header-cafe, .header-almoco, .header-lanches, .header-jantar,
        .resumo-laudo, .aviso-cientifico, .privacidade-box,
        .equipamento-adipometro, .equipamento-fita, .equipamento-complementar {
            color: black !important;
            background: white !important;
        }
        
        .banner-profissional h1 {
            background: none !important;
            -webkit-background-clip: unset !important;
            background-clip: unset !important;
            -webkit-text-fill-color: black !important;
            color: black !important;
            text-shadow: none !important;
        }
        
        table, .stDataFrame, .dataframe {
            border: 1px solid black !important;
            width: 100% !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
        
        th, td {
            border: 1px solid black !important;
            padding: 8px !important;
            color: black !important;
            background: white !important;
        }
        
        .js-plotly-plot .legend text,
        .plotly .legend text,
        .legend text,
        .g-legend text,
        .annotation-text {
            fill: black !important;
            color: black !important;
            font-weight: bold !important;
        }
        
        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text,
        .plotly .xtick text,
        .plotly .ytick text {
            fill: black !important;
            color: black !important;
        }
        
        .js-plotly-plot .bar,
        .plotly .bar {
            opacity: 1 !important;
        }
        
        .stMarkdown, .stMarkdown p, .stMarkdown div, 
        .card-com-explicacao, .card-com-explicacao *,
        .resumo-laudo, .resumo-laudo *,
        .aviso-cientifico, .aviso-cientifico *,
        .privacidade-box, .privacidade-box * {
            color: black !important;
            background: white !important;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

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

    objetivo = st.radio(
        "🎯 Seu objetivo principal:",
        ["Perda de peso", "Ganho de peso"],
        horizontal=True,
    )

    if objetivo == "Perda de peso":
        p_alvo = st.number_input(
            "🎯 Meta de Peso (kg)", 10.0, peso_at - 0.1, peso_at - 10
        )
        st.caption(f"Para perda de peso, a meta deve ser menor que {peso_at} kg")
    else:
        p_alvo = st.number_input(
            "🎯 Meta de Peso (kg)", peso_at + 0.1, 300.0, peso_at + 10
        )
        st.caption(f"Para ganho de peso, a meta deve ser maior que {peso_at} kg")

    opcoes_naf = {
        "Sedentário (Sem exercício)": 1.2,
        "Leve (1-3 dias/sem)": 1.375,
        "Moderado (3-5 dias/sem)": 1.55,
        "Intenso (6-7 dias/sem)": 1.725,
        "Atleta (Treino pesado 2x dia)": 1.9,
    }
    naf_label = st.selectbox(
        "🏃 Frequência de Atividade Física:", list(opcoes_naf.keys())
    )
    naf_val = opcoes_naf[naf_label]

    st.markdown("---")

    planejamento_tipo = st.radio(
        "📅 Tipo de Planejamento:", ["Diário", "Semanal"], horizontal=True
    )
    if planejamento_tipo != st.session_state.planejamento_tipo:
        st.session_state.planejamento_tipo = planejamento_tipo
        st.rerun()

    st.markdown("---")

    st.info(
        """
    🖨️ **IMPRESSÃO**
    
    1️⃣ Clique nos **3 pontinhos (⋮)** ao lado do botão Deploy
    2️⃣ Selecione **Imprimir**
    3️⃣ Mantenha as **margens padrão** do navegador
    4️⃣ Escolha **Salvar como PDF** 🌳
    """
    )

    st.caption(
        "💡 **Dica:** Para capturar a página inteira sem cortes, use a extensão GoFullPage no Chrome/Edge"
    )


# 11. CARGA DE DADOS
@st.cache_data
def load_db():
    df_a = (
        pd.read_csv("alimentos.csv")
        if os.path.exists("alimentos.csv")
        else pd.DataFrame()
    )
    return df_a, pd.DataFrame(), pd.DataFrame()


df_taco, df_graxos, df_amino = load_db()

# 12. HEADER
st.markdown(
    """
<div class='banner-profissional'>
    <div class='icones-esportes'>🏋️‍♂️ 🏊‍♂️ 🚴‍♂️ 🏃‍♂️ 🧘‍♀️</div>
    <h1>BioGestão 360</h1>
    <div class='slogan'>Evolua seu treino junto com os nutrientes que movem o seu corpo</div>
</div>
""",
    unsafe_allow_html=True,
)

# 13. DOAÇÕES E DICAS DE IMPRESSÃO
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
        st.caption(
            "Link: https://www.paypal.com/donate/?hosted_button_id=LQTE48R8SLWRG"
        )
    st.caption("Sua contribuição ajuda a manter o projeto gratuito!")

    st.markdown("---")
    st.markdown("### 🖨️ Dica de Impressão")
    st.info(
        """
    ⚠️ A impressão nativa (Ctrl+P) pode cortar gráficos e tabelas.
    
    ✅ **Para melhor resultado:**
    - Use a extensão **GoFullPage** (Chrome/Edge)
    - Ou ajuste margens para **5mm** cada lado no Ctrl+P
    """
    )
    st.caption("🌳 A natureza agradece o uso consciente do papel!")

# 14. POLÍTICA DE PRIVACIDADE
st.markdown(
    """
<div class='privacidade-box'>
    <b>🔒 POLÍTICA DE PRIVACIDADE (ZERO-FOOTPRINT):</b><br>
    ✅ Nenhum dado é enviado para servidores externos<br>
    ✅ Processamento 100% local no seu navegador<br>
    ✅ Ao fechar a aba, todas as informações são permanentemente deletadas
</div>
""",
    unsafe_allow_html=True,
)

# 15. AVISO CIENTÍFICO
st.markdown(
    """
<div class='aviso-cientifico'>
    <strong>📋 INFORMAÇÃO CIENTÍFICA:</strong> Baseado na Tabela TACO (UNICAMP) e equações Harris-Benedict.
    <strong>⚠️ SISTEMA EM DESENVOLVIMENTO - DADOS PODEM CONTER ERRO</strong>
</div>
""",
    unsafe_allow_html=True,
)

# 16. CÁLCULOS BIOMÉTRICOS
alt_m = alt_cm / 100
imc = peso_at / (alt_m**2)
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
st.markdown(
    f"""
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
""",
    unsafe_allow_html=True,
)

# 18. DASHBOARD
st.markdown("## ⚡ Metabolismo e Gasto Energético")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>⚡</div>
        <div class='card-valor'>{get_total:.0f} kcal</div>
        <div class='card-titulo'>Gasto Total (GET)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Total de calorias que seu corpo gasta por dia.<br>📊 <strong>Como usar:</strong> Para manter o peso, consuma esta quantidade.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>🔥</div>
        <div class='card-valor'>{tmb:.0f} kcal</div>
        <div class='card-titulo'>Metabolismo Basal (TMB)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Calorias queimadas em repouso total.<br>📊 <strong>Como usar:</strong> É o mínimo que seu corpo precisa para viver.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>📊</div>
        <div class='card-valor'>{composicao['imc']}</div>
        <div class='card-titulo'>Índice de Massa Corporal (IMC)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Relação entre peso e altura.<br>📊 <strong>Referência:</strong> 18.5-25 = Saudável | 25-30 = Sobrepeso | >30 = Obesidade</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>🎯</div>
        <div class='card-valor'>{composicao['peso_ideal']} kg</div>
        <div class='card-titulo'>Peso Ideal Estimado</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Peso considerado mais saudável para sua altura.<br>📊 <strong>Como usar:</strong> Meta de longo prazo baseada em estudos científicos.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# 19. COMPOSIÇÃO CORPORAL
st.markdown("---")
st.markdown("## 🧬 Composição Corporal")

col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown(
        f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>🎯</div>
        <div class='card-valor'>{composicao['percentual_gordura']}%</div>
        <div class='card-titulo'>Percentual de Gordura</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Porcentagem do seu corpo que é gordura.<br>📊 <strong>Referência:</strong> Homens: 10-25% | Mulheres: 18-32%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_g2:
    st.markdown(
        f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>⚖️</div>
        <div class='card-valor'>{composicao['massa_gordura']} kg</div>
        <div class='card-titulo'>Massa de Gordura</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Peso total da gordura no seu corpo.<br>📊 <strong>Como usar:</strong> Acompanhe a redução para perder peso saudável.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_g3:
    st.markdown(
        f"""
    <div class='card-com-explicacao'>
        <div class='card-icon'>💪</div>
        <div class='card-valor'>{composicao['massa_magra']} kg</div>
        <div class='card-titulo'>Massa Magra</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Músculos + ossos + órgãos.<br>📊 <strong>Como usar:</strong> Quanto maior, melhor para o metabolismo!</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================
# 19.5. AVALIAÇÃO FÍSICA PROFISSIONAL (VERSÃO CORRIGIDA)
# ============================================
st.markdown("---")
st.markdown("## 📏 Avaliação Física Profissional")
st.markdown("*Protocolo de Dobras Cutâneas - Jackson & Pollock (1980)*")

with st.expander("📋 Sobre esta avaliação (clique para expandir)"):
    st.markdown(
        """
    ### 🧪 Métodos de Avaliação
    
    | Método | Equipamento | O que avalia | Unidade |
    |--------|-------------|--------------|---------|
    | **Dobras Cutâneas** | Adipômetro (plicômetro) | Gordura subcutânea → % de gordura corporal | mm (milímetros) |
    | **Circunferências** | Fita métrica inelástica | Perímetros musculares e cintura | cm (centímetros) |
    | **Força** | Handgrip (dinamômetro) | Força de preensão palmar | kg/f |
    | **Flexibilidade** | Banco de Wells | Alongamento e flexibilidade | cm |
    
    ---
    
    ### ⚠️ **Importante:**
    
    Esta seção é **recomendada para profissionais de Educação Física, Nutrição e Saúde**.
    
    - ✅ Os resultados são **mais precisos** que a estimativa por IMC
    - ✅ Utiliza o **Protocolo de Jackson & Pollock** (referência científica)
    - ✅ Para cada dobra, realize **3 medições** e o sistema calcula automaticamente a média
    - ✅ Medidas sempre no **lado direito** do corpo (hemicorpo direito)
    - ⚠️ **Para resultado válido, as medidas devem ser feitas por um profissional qualificado**
    
    ---
    
    ### 🧬 Classificação do Percentual de Gordura e Riscos à Saúde
    
    | Classificação | Homens | Mulheres | Riscos à Saúde |
    |--------------|--------|----------|----------------|
    | **Gordura Essencial** | 2-5% | 10-13% | Mínimo necessário para sobrevivência |
    | **Atleta** | 6-13% | 14-20% | Baixo risco, alta performance |
    | **Saudável** | 14-17% | 21-24% | Risco muito baixo |
    | **Aceitável** | 18-21% | 25-31% | Risco moderado |
    | **Obesidade** | >22% | >32% | Alto risco cardiovascular, diabetes, hipertensão |
    
    ---
    
    ### 🏃 Biotipos Corporais (Heath-Carter)
    
    | Biotipo | Características | % Gordura típico | Recomendação |
    |---------|-----------------|------------------|--------------|
    | **Endomorfo** | Tendência a acumular gordura, corpo mais arredondado | Acima de 22% (H) / 28% (M) | Foco em déficit calórico + treino de força |
    | **Mesomorfo** | Estrutura atlética natural, facilidade para ganhar músculos | 10-18% (H) / 18-25% (M) | Treino equilibrado, fácil manutenção |
    | **Ectomorfo** | Metabolismo acelerado, dificuldade para ganhar peso | Abaixo de 10% (H) / 18% (M) | Foco em superávit calórico + treino de força |
    
    > **Fonte:** Organização Mundial da Saúde (OMS) e American College of Sports Medicine (ACSM)
    """
    )

usar_avaliacao = st.checkbox(
    "📊 Deseja realizar avaliação física completa?", value=False
)

if usar_avaliacao:
    # ========== FUNÇÃO PARA CRIAR 3 MEDIÇÕES ==========
    def criar_medicao_tripla(nome, valor_padrao=15.0, key_prefix=""):
        st.markdown(f"**{nome}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            m1 = st.number_input(
                f"Medição 1 (mm)",
                3.0,
                80.0,
                valor_padrao,
                step=0.5,
                key=f"{key_prefix}_{nome}_m1",
            )
        with col2:
            m2 = st.number_input(
                f"Medição 2 (mm)",
                3.0,
                80.0,
                valor_padrao,
                step=0.5,
                key=f"{key_prefix}_{nome}_m2",
            )
        with col3:
            m3 = st.number_input(
                f"Medição 3 (mm)",
                3.0,
                80.0,
                valor_padrao,
                step=0.5,
                key=f"{key_prefix}_{nome}_m3",
            )
        media = (m1 + m2 + m3) / 3
        st.caption(
            f"📊 **Média: {media:.1f} mm** (diferença máxima permitida entre medidas: 5%)"
        )
        return media

    st.markdown("---")

    # SEÇÃO 1: ADIPÔMETRO (Dobras Cutâneas)
    st.markdown("## 📏 SEÇÃO 1: DOBRAS CUTÂNEAS (ADIPÔMETRO)")
    st.markdown(
        """
    <div class='equipamento-adipometro'>
        <strong>🔵 ADIPÔMETRO (Plicômetro):</strong> Utilizado para medir a espessura da gordura subcutânea. 
        Estas medidas são usadas para calcular o <strong>percentual de gordura corporal</strong>.
        <br>Unidade: <strong>milímetros (mm)</strong>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.caption(
        "💡 **Instruções:** Para cada dobra, realize 3 medições. O sistema calculará automaticamente a média. Meça sempre no **lado direito** do corpo."
    )

    sexo_avaliacao = st.radio(
        "Sexo para avaliação:", ["Masculino", "Feminino"], horizontal=True
    )

    st.markdown("### 💪 Braços")
    triceps_media = criar_medicao_tripla("TRÍCEPS", 12.0, "adipometro")
    biceps_media = criar_medicao_tripla("BÍCEPS", 10.0, "adipometro")

    st.markdown("### 🏋️ Tronco")
    peitoral = criar_medicao_tripla("PEITORAL", 15.0, "adipometro")
    subescapular = criar_medicao_tripla("SUBESCAPULAR", 15.0, "adipometro")
    abdominal = criar_medicao_tripla("ABDOME", 20.0, "adipometro")

    st.markdown("### 📐 Quadril / Axila")
    axilar = criar_medicao_tripla("AXILAR MÉDIA", 12.0, "adipometro")
    suprailiaca = criar_medicao_tripla("SUPRA-ILÍACA", 18.0, "adipometro")

    st.markdown("### 🆕 Supra-espinal (SS)")
    st.caption(
        "Utilizada no cálculo do somatotipo de Heath-Carter. Localizada 5-7 cm acima da espinha ilíaca anterior."
    )
    supra_espinal = criar_medicao_tripla("SUPRA-ESPINAL", 14.0, "adipometro")

    st.markdown("### 🦵 Pernas")
    coxa_media = criar_medicao_tripla("COXA", 25.0, "adipometro")
    panturrilha_media = criar_medicao_tripla("PANTURRILHA", 15.0, "adipometro")

    # SEÇÃO 2: FITA MÉTRICA (Circunferências)
    st.markdown("---")
    st.markdown("## 📏 SEÇÃO 2: CIRCUNFERÊNCIAS (FITA MÉTRICA)")
    st.markdown(
        """
    <div class='equipamento-fita'>
        <strong>🟢 FITA MÉTRICA:</strong> Utilizada para medir perímetros musculares e circunferências corporais.
        Estas medidas avaliam o <strong>tamanho muscular</strong> e a distribuição da gordura.
        <br>Unidade: <strong>centímetros (cm)</strong>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_fita1, col_fita2 = st.columns(2)
    with col_fita1:
        st.markdown("**💪 Braço Contraído**")
        braco_d = st.number_input("Braço Direito (cm)", 20.0, 60.0, 32.0, step=0.5)
        braco_e = st.number_input("Braço Esquerdo (cm)", 20.0, 60.0, 31.5, step=0.5)
        braco_media_cm = (braco_d + braco_e) / 2
        st.caption(f"Média: {braco_media_cm:.1f} cm")

        st.markdown("**📏 Peitoral / Tórax**")
        st.caption("Medida na altura dos mamilos, em expiração normal.")
        peitoral_cm = st.number_input(
            "Circunferência Torácica (cm)", 60.0, 150.0, 95.0, step=0.5
        )

        st.markdown("**📐 Cintura**")
        cintura = st.number_input(
            "Circunferência da Cintura (cm)", 50.0, 150.0, 85.0, step=0.5
        )

    with col_fita2:
        st.markdown("**🦵 Coxa**")
        coxa_cm_d = st.number_input("Coxa Direita (cm)", 40.0, 80.0, 55.0, step=0.5)
        coxa_cm_e = st.number_input("Coxa Esquerda (cm)", 40.0, 80.0, 54.5, step=0.5)
        coxa_media_cm = (coxa_cm_d + coxa_cm_e) / 2
        st.caption(f"Média: {coxa_media_cm:.1f} cm")

        st.markdown("**🦵 Panturrilha**")
        panturrilha_cm_d = st.number_input(
            "Panturrilha Direita (cm)", 25.0, 50.0, 36.0, step=0.5
        )
        panturrilha_cm_e = st.number_input(
            "Panturrilha Esquerda (cm)", 25.0, 50.0, 35.5, step=0.5
        )
        panturrilha_media_cm = (panturrilha_cm_d + panturrilha_cm_e) / 2
        st.caption(f"Média: {panturrilha_media_cm:.1f} cm")

    st.markdown("**🫀 Relação Cintura-Quadril (RCQ)**")
    quadril = st.number_input(
        "Circunferência do Quadril (cm)", 60.0, 150.0, 95.0, step=0.5
    )
    if quadril > 0:
        rcq = cintura / quadril
        if sexo_avaliacao == "Masculino":
            risco_rcq = (
                "⚠️ Risco cardiovascular elevado"
                if rcq > 0.95
                else "✅ Risco cardiovascular normal"
            )
        else:
            risco_rcq = (
                "⚠️ Risco cardiovascular elevado"
                if rcq > 0.85
                else "✅ Risco cardiovascular normal"
            )
        st.caption(f"Relação Cintura-Quadril: **{rcq:.2f}** - {risco_rcq}")

    # SEÇÃO 3: AVALIAÇÕES COMPLEMENTARES
    st.markdown("---")
    st.markdown("## 💪 SEÇÃO 3: AVALIAÇÕES COMPLEMENTARES")
    st.markdown(
        """
    <div class='equipamento-complementar'>
        <strong>🟡 Handgrip e Banco de Wells:</strong> Estas avaliações NÃO entram no cálculo do percentual de gordura,
        mas são importantes para o perfil completo do avaliado.
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_comp1, col_comp2 = st.columns(2)
    with col_comp1:
        st.markdown("**🤝 Força de Preensão Palmar (Handgrip)**")
        st.caption(
            "Mede a força de preensão manual, indicador de força geral e saúde cardiovascular."
        )
        handgrip_d = st.number_input(
            "Handgrip Direito (kg/f)", 10.0, 80.0, 35.0, step=0.5
        )
        handgrip_e = st.number_input(
            "Handgrip Esquerdo (kg/f)", 10.0, 80.0, 32.0, step=0.5
        )
        handgrip_media = (handgrip_d + handgrip_e) / 2

        if sexo_avaliacao == "Masculino":
            if handgrip_media < 35:
                nivel_forca = "🔴 Fraco (abaixo da média)"
            elif handgrip_media < 45:
                nivel_forca = "🟡 Regular (na média)"
            else:
                nivel_forca = "🟢 Forte (acima da média)"
        else:
            if handgrip_media < 25:
                nivel_forca = "🔴 Fraco (abaixo da média)"
            elif handgrip_media < 35:
                nivel_forca = "🟡 Regular (na média)"
            else:
                nivel_forca = "🟢 Forte (acima da média)"
        st.caption(f"Média: {handgrip_media:.1f} kg/f - Nível: {nivel_forca}")

    with col_comp2:
        st.markdown("**🧘 Flexibilidade (Banco de Wells)**")
        st.caption("Mede a flexibilidade da região lombar e posterior da coxa.")
        wells = st.number_input("Banco de Wells (cm)", -20.0, 50.0, 25.0, step=0.5)

        if sexo_avaliacao == "Masculino":
            if wells < 20:
                nivel_flex = "🔴 Abaixo da média"
            elif wells < 30:
                nivel_flex = "🟡 Média"
            else:
                nivel_flex = "🟢 Acima da média"
        else:
            if wells < 25:
                nivel_flex = "🔴 Abaixo da média"
            elif wells < 35:
                nivel_flex = "🟡 Média"
            else:
                nivel_flex = "🟢 Acima da média"
        st.caption(f"Flexibilidade: {wells:.1f} cm - Nível: {nivel_flex}")

    # ========== CÁLCULOS JACKSON & POLLOCK ==========
    st.markdown("---")
    st.markdown("#### 🔬 Protocolo de Dobras (Jackson & Pollock)")

    if sexo_avaliacao == "Masculino":
        usar_7_dobras = (
            st.radio(
                "Escolha o protocolo:",
                [
                    "3 dobras (Tríceps, Peitoral, Abdome)",
                    "7 dobras (Completo - mais preciso)",
                ],
                horizontal=True,
            )
            == "7 dobras (Completo - mais preciso)"
        )

        if usar_7_dobras:
            soma_dobras = (
                triceps_media
                + peitoral
                + abdominal
                + subescapular
                + axilar
                + suprailiaca
                + coxa_media
            )
            st.caption(f"📊 Soma das 7 dobras: {soma_dobras:.1f} mm")
            densidade = (
                1.112
                - (0.00043499 * soma_dobras)
                + (0.00000055 * (soma_dobras**2))
                - (0.00028826 * idade)
            )
        else:
            soma_dobras = triceps_media + peitoral + abdominal
            st.caption(f"📊 Soma das 3 dobras: {soma_dobras:.1f} mm")
            densidade = (
                1.10938
                - (0.0008267 * soma_dobras)
                + (0.0000016 * (soma_dobras**2))
                - (0.0002574 * idade)
            )

    else:
        usar_7_dobras = (
            st.radio(
                "Escolha o protocolo:",
                [
                    "3 dobras (Tríceps, Supra-ilíaca, Coxa)",
                    "7 dobras (Completo - mais preciso)",
                ],
                horizontal=True,
            )
            == "7 dobras (Completo - mais preciso)"
        )

        if usar_7_dobras:
            soma_dobras = (
                triceps_media
                + suprailiaca
                + coxa_media
                + subescapular
                + peitoral
                + axilar
                + abdominal
            )
            st.caption(f"📊 Soma das 7 dobras: {soma_dobras:.1f} mm")
            densidade = (
                1.097
                - (0.00046971 * soma_dobras)
                + (0.00000056 * (soma_dobras**2))
                - (0.00012828 * idade)
            )
        else:
            soma_dobras = triceps_media + suprailiaca + coxa_media
            st.caption(f"📊 Soma das 3 dobras: {soma_dobras:.1f} mm")
            densidade = (
                1.0994921
                - (0.0009929 * soma_dobras)
                + (0.0000023 * (soma_dobras**2))
                - (0.0001392 * idade)
            )

    if densidade > 0:
        percentual_gordura_jp = ((4.95 / densidade) - 4.5) * 100
        percentual_gordura_jp = max(5, min(50, percentual_gordura_jp))
    else:
        percentual_gordura_jp = 0

    massa_gordura_jp = peso_at * (percentual_gordura_jp / 100)
    massa_magra_jp = peso_at - massa_gordura_jp

    # Classificações
    if sexo_avaliacao == "Masculino":
        if percentual_gordura_jp < 6:
            classif_gordura = "Gordura Essencial"
            grau_obesidade = "Muito abaixo do ideal"
            risco_saude = "Baixo (atletas de elite)"
        elif percentual_gordura_jp < 14:
            classif_gordura = "Atleta"
            grau_obesidade = "Abaixo do ideal (atleta)"
            risco_saude = "Muito baixo"
        elif percentual_gordura_jp < 18:
            classif_gordura = "Saudável"
            grau_obesidade = "Normal"
            risco_saude = "Baixo"
        elif percentual_gordura_jp < 25:
            classif_gordura = "Aceitável"
            grau_obesidade = "Sobrepeso"
            risco_saude = "Moderado"
        else:
            classif_gordura = "Elevado"
            grau_obesidade = "Obesidade"
            risco_saude = "Alto"
    else:
        if percentual_gordura_jp < 12:
            classif_gordura = "Gordura Essencial"
            grau_obesidade = "Muito abaixo do ideal"
            risco_saude = "Baixo (atletas de elite)"
        elif percentual_gordura_jp < 21:
            classif_gordura = "Atleta"
            grau_obesidade = "Abaixo do ideal (atleta)"
            risco_saude = "Muito baixo"
        elif percentual_gordura_jp < 25:
            classif_gordura = "Saudável"
            grau_obesidade = "Normal"
            risco_saude = "Baixo"
        elif percentual_gordura_jp < 32:
            classif_gordura = "Aceitável"
            grau_obesidade = "Sobrepeso"
            risco_saude = "Moderado"
        else:
            classif_gordura = "Elevado"
            grau_obesidade = "Obesidade"
            risco_saude = "Alto"

    # Biotipo
    if percentual_gordura_jp > 25:
        biotipo = "Endomorfo"
        cor_biotipo = "#ef4444"
        desc_biotipo = "Tendência a acumular gordura, corpo mais arredondado, dificuldade para definir os músculos."
        recomendacao_biotipo = "Foco em déficit calórico moderado, treino de força de alta intensidade e cardio regular."
    elif percentual_gordura_jp < 12 and massa_magra_jp > (peso_at * 0.4):
        biotipo = "Ectomorfo"
        cor_biotipo = "#3b82f6"
        desc_biotipo = "Metabolismo acelerado, dificuldade para ganhar peso e massa muscular, estrutura mais fina."
        recomendacao_biotipo = (
            "Foco em superávit calórico, treino de força com pouca frequência cardio."
        )
    else:
        biotipo = "Mesomorfo"
        cor_biotipo = "#10b981"
        desc_biotipo = "Estrutura atlética natural, facilidade para ganhar massa muscular e manter baixo percentual de gordura."
        recomendacao_biotipo = (
            "Treino equilibrado de força e cardio, facilidade para manutenção."
        )

    # Exibir resultados
    st.markdown("---")
    st.markdown("### 📊 Resultado da Avaliação Física (Jackson & Pollock)")

    col_jp1, col_jp2, col_jp3 = st.columns(3)

    with col_jp1:
        st.markdown(
            f"""
        <div class='card-com-explicacao'>
            <div class='card-icon'>🎯</div>
            <div class='card-valor'>{percentual_gordura_jp:.1f}%</div>
            <div class='card-titulo'>% Gordura (Adipômetro)</div>
            <div class='card-explicacao'>Classificação: {classif_gordura}<br>Risco: {risco_saude}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_jp2:
        st.markdown(
            f"""
        <div class='card-com-explicacao'>
            <div class='card-icon'>⚖️</div>
            <div class='card-valor'>{massa_gordura_jp:.1f} kg</div>
            <div class='card-titulo'>Massa de Gordura</div>
            <div class='card-explicacao'>{((massa_gordura_jp/peso_at)*100):.1f}% do peso total</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_jp3:
        st.markdown(
            f"""
        <div class='card-com-explicacao'>
            <div class='card-icon'>💪</div>
            <div class='card-valor'>{massa_magra_jp:.1f} kg</div>
            <div class='card-titulo'>Massa Magra</div>
            <div class='card-explicacao'>{((massa_magra_jp/peso_at)*100):.1f}% do peso total</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Gráfico de pizza
    st.markdown("---")
    st.markdown("#### 🥧 Composição Corporal")

    col_pizza, col_biotipo = st.columns(2)

    with col_pizza:
        composicao_corpo = pd.DataFrame(
            {
                "Componente": ["Massa Gorda", "Massa Magra"],
                "Valor": [percentual_gordura_jp, 100 - percentual_gordura_jp],
            }
        )
        fig_pizza = px.pie(
            composicao_corpo,
            values="Valor",
            names="Componente",
            title="Proporção do seu corpo",
            color="Componente",
            color_discrete_map={"Massa Gorda": "#ef4444", "Massa Magra": "#3b82f6"},
        )
        fig_pizza.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

    with col_biotipo:
        st.markdown(
            f"""
        <div class='card-com-explicacao' style='border-left: 5px solid {cor_biotipo};'>
            <div class='card-icon'>🧬</div>
            <div class='card-valor' style='color: {cor_biotipo};'>{biotipo}</div>
            <div class='card-titulo'>Biotipo Corporal</div>
            <div class='card-explicacao'>{desc_biotipo}<br><br>
            <strong>Recomendação:</strong> {recomendacao_biotipo}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Gráfico de barras comparativo
    st.markdown("---")
    st.markdown("#### 📊 Comparativo com Referências de Saúde")

    if sexo_avaliacao == "Masculino":
        referencia_saudavel = 17
        referencia_atleta = 12
        referencia_obesidade = 25
        referencia_essencial = 5
    else:
        referencia_saudavel = 24
        referencia_atleta = 20
        referencia_obesidade = 32
        referencia_essencial = 12

    df_comparacao = pd.DataFrame(
        {
            "Categoria": [
                "Seu % Gordura",
                "Gordura Essencial",
                "Atleta",
                "Saudável",
                "Obesidade",
            ],
            "Percentual": [
                percentual_gordura_jp,
                referencia_essencial,
                referencia_atleta,
                referencia_saudavel,
                referencia_obesidade,
            ],
        }
    )

    fig_comparacao = px.bar(
        df_comparacao,
        x="Categoria",
        y="Percentual",
        title="Comparação do seu percentual de gordura com referências",
        color="Categoria",
        color_discrete_map={
            "Seu % Gordura": "#3b82f6",
            "Gordura Essencial": "#8b5cf6",
            "Atleta": "#10b981",
            "Saudável": "#f59e0b",
            "Obesidade": "#ef4444",
        },
    )
    fig_comparacao.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        yaxis_title="Percentual de Gordura (%)",
    )
    st.plotly_chart(fig_comparacao, use_container_width=True)

    # Gráfico por idade
    st.markdown("---")
    st.markdown("#### 📈 Percentual de Gordura por Idade (Referência)")

    idades = list(range(20, 71, 5))
    if sexo_avaliacao == "Masculino":
        percentuais_referencia = [18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29]
    else:
        percentuais_referencia = [25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36]

    df_idade = pd.DataFrame(
        {
            "Idade": idades,
            "Referência": percentuais_referencia,
            "Seu Valor": [percentual_gordura_jp] * len(idades),
        }
    )

    fig_idade = px.line(
        df_idade,
        x="Idade",
        y="Referência",
        title="Percentual de Gordura por Idade (Referência ACSM)",
        labels={"value": "% Gordura", "Idade": "Idade (anos)"},
    )
    fig_idade.add_hline(
        y=percentual_gordura_jp,
        line_dash="dash",
        line_color="#3b82f6",
        annotation_text=f"Seu valor: {percentual_gordura_jp:.1f}%",
    )
    fig_idade.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=400
    )
    st.plotly_chart(fig_idade, use_container_width=True)

    # LAUDO DA AVALIAÇÃO FÍSICA
    st.markdown("---")
    st.markdown("## 🖨️ LAUDO DA AVALIAÇÃO FÍSICA")
    st.markdown(
        "*Este laudo pode ser impresso para arquivo pessoal ou para compartilhar com profissionais*"
    )

    if imc < 18.5:
        classificacao_imc_laudo = "Abaixo do peso"
    elif imc < 25:
        classificacao_imc_laudo = "Peso normal"
    elif imc < 30:
        classificacao_imc_laudo = "Sobrepeso"
    elif imc < 35:
        classificacao_imc_laudo = "Obesidade Grau I"
    elif imc < 40:
        classificacao_imc_laudo = "Obesidade Grau II"
    else:
        classificacao_imc_laudo = "Obesidade Grau III"

    st.markdown("### 📊 Dados do Avaliado")
    st.markdown(
        f"""
    | Medida | Valor |
    |--------|-------|
    | **Peso** | {peso_at:.1f} kg |
    | **Altura** | {alt_cm} cm |
    | **Idade** | {idade} anos |
    | **IMC** | {imc:.1f} ({classificacao_imc_laudo}) |
    """
    )

    st.markdown("### 📏 Resultados da Avaliação por Dobras Cutâneas (Adipômetro)")
    st.markdown(
        f"""
    | Medida | Valor |
    |--------|-------|
    | **Percentual de Gordura** | {percentual_gordura_jp:.1f}% |
    | **Classificação** | {classif_gordura} |
    | **Grau** | {grau_obesidade} |
    | **Risco à Saúde** | {risco_saude} |
    | **Massa de Gordura** | {massa_gordura_jp:.1f} kg |
    | **Massa Magra** | {massa_magra_jp:.1f} kg |
    """
    )

    st.markdown("### 📏 Resultados das Circunferências (Fita Métrica)")
    st.markdown(
        f"""
    | Medida | Valor |
    |--------|-------|
    | **Braço (média D+E)** | {braco_media_cm:.1f} cm |
    | **Peitoral / Tórax** | {peitoral_cm:.1f} cm |
    | **Coxa (média D+E)** | {coxa_media_cm:.1f} cm |
    | **Panturrilha (média D+E)** | {panturrilha_media_cm:.1f} cm |
    | **Cintura** | {cintura:.1f} cm |
    | **Quadril** | {quadril:.1f} cm |
    | **Relação Cintura-Quadril** | {rcq:.2f} - {risco_rcq} |
    """
    )

    st.markdown("### 💪 Resultados das Avaliações Complementares")
    st.markdown(
        f"""
    | Medida | Valor |
    |--------|-------|
    | **Handgrip (média D+E)** | {handgrip_media:.1f} kg/f - {nivel_forca} |
    | **Banco de Wells** | {wells:.1f} cm - {nivel_flex} |
    """
    )

    st.markdown("### 🧬 Biotipo Corporal")
    st.markdown(
        f"""
    | Medida | Valor |
    |--------|-------|
    | **Biotipo** | {biotipo} |
    | **Descrição** | {desc_biotipo} |
    | **Recomendação** | {recomendacao_biotipo} |
    """
    )

    st.markdown("### 📋 Protocolo Utilizado")
    st.markdown(
        f"""
    | Item | Informação |
    |------|-------------|
    | **Protocolo de Dobras** | Jackson & Pollock {'(7 dobras)' if usar_7_dobras else '(3 dobras)'} |
    | **Fórmula de Densidade** | Siri (1961) |
    | **Equipamentos** | Adipômetro, Fita Métrica, Handgrip, Banco de Wells |
    | **Referência** | ACSM - American College of Sports Medicine |
    """
    )

    # Botão para baixar Laudo da Avaliação Física em CSV
    st.markdown("---")
    st.markdown("#### 📥 Baixar Laudo da Avaliação Física")

    dados_laudo_avaliacao = {
        "Categoria": [
            "Data da Avaliação",
            "Sexo",
            "Idade",
            "Peso",
            "Altura",
            "IMC",
            "Protocolo Utilizado",
            "Soma das Dobras (mm)",
            "Densidade Corporal (g/cm³)",
            "% Gordura (Adipômetro)",
            "Classificação % Gordura",
            "Risco à Saúde",
            "Massa de Gordura (kg)",
            "Massa Magra (kg)",
            "Biotipo",
            "Circunferência do Braço (média cm)",
            "Circunferência do Peitoral (cm)",
            "Circunferência da Coxa (média cm)",
            "Circunferência da Panturrilha (média cm)",
            "Circunferência da Cintura (cm)",
            "Circunferência do Quadril (cm)",
            "Relação Cintura-Quadril (RCQ)",
            "Força Handgrip (média kg/f)",
            "Nível de Força",
            "Flexibilidade Banco de Wells (cm)",
            "Nível de Flexibilidade",
        ],
        "Valor": [
            pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
            sexo_avaliacao,
            idade,
            f"{peso_at} kg",
            f"{alt_cm} cm",
            f"{imc:.1f} ({classificacao_imc_laudo})",
            f"Jackson & Pollock - {'7 dobras' if usar_7_dobras else '3 dobras'}",
            f"{soma_dobras:.1f} mm",
            f"{densidade:.3f}",
            f"{percentual_gordura_jp:.1f}%",
            classif_gordura,
            risco_saude,
            f"{massa_gordura_jp:.1f} kg",
            f"{massa_magra_jp:.1f} kg",
            biotipo,
            f"{braco_media_cm:.1f} cm",
            f"{peitoral_cm:.1f} cm",
            f"{coxa_media_cm:.1f} cm",
            f"{panturrilha_media_cm:.1f} cm",
            f"{cintura:.1f} cm",
            f"{quadril:.1f} cm",
            f"{rcq:.2f} - {risco_rcq}",
            f"{handgrip_media:.1f} kg/f",
            nivel_forca,
            f"{wells:.1f} cm",
            nivel_flex,
        ],
    }

    df_laudo_avaliacao = pd.DataFrame(dados_laudo_avaliacao)
    csv_laudo_avaliacao = df_laudo_avaliacao.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        "📄 Baixar Laudo da Avaliação Física (CSV)",
        data=csv_laudo_avaliacao,
        file_name=f"laudo_avaliacao_fisica_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown(
        f"*Este laudo é uma estimativa baseada nas medidas inseridas. Para maior precisão, consulte um profissional de Educação Física ou Nutrição qualificado.*"
    )

else:
    st.info(
        "💡 **Dica:** Ative a opção acima para realizar uma avaliação física completa com dobras cutâneas (adipômetro), circunferências (fita métrica), handgrip e banco de wells."
    )

# ============================================
# 20. MONTAGEM DO PLANO ALIMENTAR
# ============================================
st.markdown("## 🍏 Montagem do Plano Alimentar")
st.info(
    "💡 **Dica de precisão:** Utilize 'Peso Real (g/ml)' com balança para maior exatidão!"
)

# ========== AVISO PARA SEGUIR RECEITA DA NUTRI ==========
st.markdown(
    """
<div class='aviso-cientifico' style='margin-bottom: 15px;'>
    <strong>📋 Para seguir sua receita da nutri:</strong>
    <br><br>
    1️⃣ Identifique os alimentos da sua receita na tabela TACO (busque pelo nome)
    <br>
    2️⃣ Adicione um a um nos campos abaixo com as quantidades prescritas
    <br>
    3️⃣ O sistema calcula automaticamente calorias e nutrientes com base em dados científicos (UNICAMP)
    <br>
    4️⃣ Use o resumo para impressão e acompanhamento
    <br><br>
    <strong>⚠️ Importante:</strong> Todos os alimentos possuem valores nutricionais baseados na Tabela TACO.
    Consulte seu nutricionista ou médico para ajustes personalizados.
</div>
""",
    unsafe_allow_html=True,
)
# ========== FIM DO AVISO ==========

if st.session_state.planejamento_tipo == "Semanal":
    st.markdown("### 📅 Selecione o dia")
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    cols = st.columns(7)
    for i, dia in enumerate(dias_semana):
        with cols[i]:
            if st.session_state.dia_atual == dia:
                st.markdown(
                    f"<div class='dia-btn-selected'>{dia} ✅</div>",
                    unsafe_allow_html=True,
                )
            else:
                if st.button(dia, key=f"dia_{dia}", use_container_width=True):
                    st.session_state.dia_atual = dia
                    st.rerun()
    st.markdown(
        f"<div style='text-align: center; margin: 15px 0;'><div style='background: linear-gradient(135deg, #f59e0b, #ef4444); color: white; padding: 10px 20px; border-radius: 50px; display: inline-block; font-weight: bold;'>📌 Editando: {st.session_state.dia_atual}</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

if not st.session_state.modo_impressao and not df_taco.empty:
    with st.container():
        col1, col2, col3, col4 = st.columns([1.5, 3, 1, 1])
        with col1:
            refeicao_sel = st.selectbox(
                "Refeição", ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
            )
        with col2:
            alimento_sel = st.selectbox(
                "Alimento", df_taco["Descrição dos alimentos"].unique()
            )
        with col3:
            qtd_unidade = st.number_input("Unidades", 0.0, 50.0, 1.0)
        with col4:
            peso_real = st.number_input("Peso Real (g/ml)", 0.0, 2000.0, 0.0)

    if st.button("➕ Adicionar ao Plano", use_container_width=True):
        item = df_taco[df_taco["Descrição dos alimentos"] == alimento_sel].iloc[0]
        is_liquido = any(
            x in alimento_sel.lower()
            for x in ["suco", "leite", "café", "bebida", "água", "chá"]
        )

        if peso_real > 0:
            peso_final = peso_real
            label_qtd = f"{peso_real}ml" if is_liquido else f"{peso_real}g"
        else:
            base_peso = 200 if is_liquido else 50
            peso_final = qtd_unidade * base_peso
            label_qtd = (
                f"{qtd_unidade} unid (~{peso_final}{'ml' if is_liquido else 'g'})"
            )

        fator_calc = peso_final / 100
        risco_oms = verificar_risco_oms(alimento_sel)

        novo_item = {
            "Ali": alimento_sel,
            "Qtd": label_qtd,
            "Kcal": round(item["Energia..kcal."] * fator_calc, 1),
            "P": round(item["Proteína..g."] * fator_calc, 1),
            "C": round(item["Carboidrato..g."] * fator_calc, 1),
            "G": round(item["Lipídeos..g."] * fator_calc, 1),
            "Risco": risco_oms,
        }

        if st.session_state.planejamento_tipo == "Diário":
            st.session_state.cardapio[refeicao_sel].append(novo_item)
        else:
            st.session_state.cardapio_semanal[st.session_state.dia_atual][
                refeicao_sel
            ].append(novo_item)
        st.rerun()

st.markdown("---")

# 21. EXIBIÇÃO DO PLANO
if st.session_state.planejamento_tipo == "Diário":
    st.markdown("### 📋 Seu Cardápio de Hoje")

    if st.session_state.cardapio["Café da Manhã"]:
        st.markdown(
            "<div class='header-cafe'>🌅 CAFÉ DA MANHÃ</div>", unsafe_allow_html=True
        )
        for idx, item in enumerate(st.session_state.cardapio["Café da Manhã"]):
            colA, colB, colC = st.columns([3, 4, 1])
            with colA:
                st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
            with colB:
                st.markdown(
                    f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>",
                    unsafe_allow_html=True,
                )
            with colC:
                if st.button("🗑️", key=f"del_cafe_{idx}"):
                    remover_item_diario("Café da Manhã", idx)
            if item.get("Risco"):
                st.markdown(
                    f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>",
                    unsafe_allow_html=True,
                )
            st.divider()

    if st.session_state.cardapio["Almoço"]:
        st.markdown(
            "<div class='header-almoco'>🍜 ALMOÇO</div>", unsafe_allow_html=True
        )
        for idx, item in enumerate(st.session_state.cardapio["Almoço"]):
            colA, colB, colC = st.columns([3, 4, 1])
            with colA:
                st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
            with colB:
                st.markdown(
                    f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>",
                    unsafe_allow_html=True,
                )
            with colC:
                if st.button("🗑️", key=f"del_almoco_{idx}"):
                    remover_item_diario("Almoço", idx)
            if item.get("Risco"):
                st.markdown(
                    f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>",
                    unsafe_allow_html=True,
                )
            st.divider()

    if st.session_state.cardapio["Lanches"]:
        st.markdown(
            "<div class='header-lanches'>🍎 LANCHES</div>", unsafe_allow_html=True
        )
        for idx, item in enumerate(st.session_state.cardapio["Lanches"]):
            colA, colB, colC = st.columns([3, 4, 1])
            with colA:
                st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
            with colB:
                st.markdown(
                    f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>",
                    unsafe_allow_html=True,
                )
            with colC:
                if st.button("🗑️", key=f"del_lanches_{idx}"):
                    remover_item_diario("Lanches", idx)
            if item.get("Risco"):
                st.markdown(
                    f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>",
                    unsafe_allow_html=True,
                )
            st.divider()

    if st.session_state.cardapio["Jantar"]:
        st.markdown(
            "<div class='header-jantar'>🌙 JANTAR</div>", unsafe_allow_html=True
        )
        for idx, item in enumerate(st.session_state.cardapio["Jantar"]):
            colA, colB, colC = st.columns([3, 4, 1])
            with colA:
                st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
            with colB:
                st.markdown(
                    f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>",
                    unsafe_allow_html=True,
                )
            with colC:
                if st.button("🗑️", key=f"del_jantar_{idx}"):
                    remover_item_diario("Jantar", idx)
            if item.get("Risco"):
                st.markdown(
                    f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>",
                    unsafe_allow_html=True,
                )
            st.divider()

else:
    st.markdown(f"### 📅 Planejamento Semanal - {st.session_state.dia_atual}")

    refeicoes = ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
    headers = {
        "Café da Manhã": "header-cafe",
        "Almoço": "header-almoco",
        "Lanches": "header-lanches",
        "Jantar": "header-jantar",
    }
    icons = {"Café da Manhã": "🌅", "Almoço": "🍜", "Lanches": "🍎", "Jantar": "🌙"}

    for refeicao in refeicoes:
        itens = st.session_state.cardapio_semanal.get(
            st.session_state.dia_atual, {}
        ).get(refeicao, [])
        if itens:
            st.markdown(
                f"<div class='{headers[refeicao]}'>{icons[refeicao]} {refeicao.upper()}</div>",
                unsafe_allow_html=True,
            )
            for idx, item in enumerate(itens):
                colA, colB, colC = st.columns([3, 4, 1])
                with colA:
                    st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
                with colB:
                    st.markdown(
                        f"<span class='macro-tag-kcal'>🔥 {item['Kcal']} kcal</span> <span class='macro-tag-proteina'>🥩 {item['P']}g</span> <span class='macro-tag-carb'>🍞 {item['C']}g</span> <span class='macro-tag-gordura'>🥑 {item['G']}g</span>",
                        unsafe_allow_html=True,
                    )
                with colC:
                    if st.button("🗑️", key=f"del_semanal_{refeicao}_{idx}"):
                        remover_item_semanal(st.session_state.dia_atual, refeicao, idx)
                if item.get("Risco"):
                    st.markdown(
                        f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>",
                        unsafe_allow_html=True,
                    )
                st.divider()

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button(
            f"🗑️ Limpar {st.session_state.dia_atual}", use_container_width=True
        ):
            limpar_dia_semanal(st.session_state.dia_atual)
    with col_btn2:
        if st.button("🗑️ Limpar Semana Inteira", use_container_width=True):
            limpar_semana_completa()

st.markdown("---")

# 22. CÁLCULO DOS TOTAIS
totais = calcular_totais_cardapio(
    st.session_state.cardapio,
    st.session_state.planejamento_tipo,
    st.session_state.cardapio_semanal,
)

total_kcal = totais["total_kcal"]
total_prot = totais["total_prot"]
total_carb = totais["total_carb"]
total_gord = totais["total_gord"]
media_diaria = totais["media_diaria_kcal"]

saldo_diario = get_total - media_diaria
variacao_semanal = abs((saldo_diario * 7) / 7700)
variacao_30dias = abs((saldo_diario * 30) / 7700)

# 23. GRÁFICOS
if total_kcal > 0:
    st.markdown("## 📊 Análise Nutricional")

    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        macros_data = pd.DataFrame(
            {
                "Macronutriente": ["Proteínas", "Carboidratos", "Gorduras"],
                "Calorias": [total_prot * 4, total_carb * 4, total_gord * 9],
            }
        )
        fig_pizza = px.pie(
            macros_data,
            values="Calorias",
            names="Macronutriente",
            title="Distribuição dos Macronutrientes",
            color_discrete_sequence=["#ef4444", "#3b82f6", "#f59e0b"],
        )
        fig_pizza.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

    with col_graf2:
        balanco_data = pd.DataFrame(
            {
                "Categoria": ["Gasto Total (GET)", "Consumo Médio", "Diferença"],
                "Valor (kcal)": [get_total, media_diaria, abs(saldo_diario)],
            }
        )
        fig_balanco = px.bar(
            balanco_data,
            x="Categoria",
            y="Valor (kcal)",
            title="Balanço Energético",
            color="Categoria",
            color_discrete_map={
                "Gasto Total (GET)": "#ef4444",
                "Consumo Médio": "#10b981",
                "Diferença": "#f59e0b",
            },
        )
        fig_balanco.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350
        )
        st.plotly_chart(fig_balanco, use_container_width=True)

    st.markdown(
        """
    <div style='background: var(--bg-secondary); border-radius: 10px; padding: 10px 15px; margin-top: 10px; font-size: 12px; display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;'>
        <span>🔥 <strong>kcal</strong> = Energia total do alimento</span>
        <span>🥩 <strong>Proteínas (g)</strong> = Essenciais para construção muscular</span>
        <span>🍞 <strong>Carboidratos (g)</strong> = Principal fonte de energia do corpo</span>
        <span>🥑 <strong>Gorduras (g)</strong> = Importantes para hormônios e vitaminas</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

# 24. LAUDO TÉCNICO COMPLETO
st.markdown("## 📋 LAUDO TÉCNICO DE VIABILIDADE ALIMENTAR")

if st.session_state.planejamento_tipo == "Diário":
    st.caption(
        f"📅 **Período analisado:** Hoje (1 dia) | Total de {total_kcal:.1f} kcal no dia"
    )
else:
    st.caption(
        f"📅 **Período analisado:** Semana completa (7 dias) | Total de {total_kcal:.1f} kcal na semana | Média diária: {media_diaria:.1f} kcal"
    )

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "🥗 Consumo Planejado",
        (
            f"{media_diaria:.1f} kcal"
            if st.session_state.planejamento_tipo == "Semanal"
            else f"{total_kcal:.1f} kcal"
        ),
    )
with col2:
    st.metric("⚡ Gasto Estimado (GET)", f"{get_total:.0f} kcal")
with col3:
    delta_texto = "Déficit" if saldo_diario > 0 else "Superávit"
    st.metric(
        "💪 Saldo Energético Diário", f"{abs(saldo_diario):.1f} kcal", delta_texto
    )

st.markdown("---")
st.markdown("#### 🍽️ MACRONUTRIENTES TOTAIS DO PLANO")

col_p, col_c, col_g = st.columns(3)

if st.session_state.planejamento_tipo == "Diário":
    with col_p:
        st.metric(
            "🥩 Proteínas",
            f"{total_prot:.1f} g",
            f"{((total_prot*4)/total_kcal*100 if total_kcal>0 else 0):.1f}% das calorias",
        )
    with col_c:
        st.metric(
            "🍞 Carboidratos",
            f"{total_carb:.1f} g",
            f"{((total_carb*4)/total_kcal*100 if total_kcal>0 else 0):.1f}% das calorias",
        )
    with col_g:
        st.metric(
            "🥑 Gorduras",
            f"{total_gord:.1f} g",
            f"{((total_gord*9)/total_kcal*100 if total_kcal>0 else 0):.1f}% das calorias",
        )
else:
    with col_p:
        st.metric(
            "🥩 Proteínas (semana)",
            f"{total_prot:.1f} g",
            f"Média: {total_prot/7:.1f}g/dia",
        )
    with col_c:
        st.metric(
            "🍞 Carboidratos (semana)",
            f"{total_carb:.1f} g",
            f"Média: {total_carb/7:.1f}g/dia",
        )
    with col_g:
        st.metric(
            "🥑 Gorduras (semana)",
            f"{total_gord:.1f} g",
            f"Média: {total_gord/7:.1f}g/dia",
        )

st.markdown("---")
st.markdown("#### 📊 ESTIMATIVA DE RESULTADOS")

col_result1, col_result2, col_result3 = st.columns(3)

with col_result1:
    if objetivo == "Perda de peso":
        if saldo_diario > 0:
            st.success(
                f"🎯 **Você está em DÉFICIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a menos por dia, seu corpo vai usar gordura como energia."
            )
        else:
            st.warning(
                f"⚠️ **Você está em SUPERÁVIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a mais por dia, seu corpo pode armazenar gordura."
            )
    else:
        if saldo_diario < 0:
            st.success(
                f"🎯 **Você está em SUPERÁVIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a mais por dia, ideal para ganho de massa muscular."
            )
        else:
            st.warning(
                f"⚠️ **Você está em DÉFICIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a menos por dia, pode prejudicar o ganho muscular."
            )

with col_result2:
    if st.session_state.planejamento_tipo == "Diário":
        st.info(
            f"📉 **Projeção em 7 dias:** {variacao_semanal:.2f} kg\n\n📉 **Projeção em 30 dias:** {variacao_30dias:.2f} kg"
        )
    else:
        st.info(
            f"📉 **Projeção semanal:** {variacao_semanal:.2f} kg\n\n📉 **Projeção em 30 dias:** {variacao_30dias:.2f} kg"
        )

with col_result3:
    if saldo_diario != 0:
        if objetivo == "Perda de peso" and saldo_diario > 0:
            semanas_meta = (
                abs(diferenca_meta) / (variacao_semanal) if variacao_semanal > 0 else 0
            )
            st.success(
                f"⏱️ **Tempo estimado para meta:** {max(1, int(semanas_meta))} semanas"
            )
        elif objetivo == "Ganho de peso" and saldo_diario < 0:
            semanas_meta = (
                abs(diferenca_meta) / (variacao_semanal) if variacao_semanal > 0 else 0
            )
            st.success(
                f"⏱️ **Tempo estimado para meta:** {max(1, int(semanas_meta))} semanas"
            )
        else:
            st.warning("⚡ **Ajuste seu consumo para atingir a meta!**")
    else:
        st.info("✅ **Manutenção!** Você está consumindo exatamente o que gasta.")

# 25. RESUMO COMPLETO PARA IMPRESSÃO
st.markdown("---")
st.markdown("## 🖨️ RESUMO COMPLETO PARA IMPRESSÃO")
st.markdown(
    "*Esta seção contém todos os alimentos selecionados para fácil impressão - sem botões de excluir*"
)

todos_alimentos = []
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

if st.session_state.planejamento_tipo == "Diário":
    for refeicao, itens in st.session_state.cardapio.items():
        for item in itens:
            todos_alimentos.append(
                {
                    "Dia": "Hoje",
                    "Refeição": refeicao,
                    "Alimento": item["Ali"],
                    "Quantidade": item["Qtd"],
                    "Kcal": item["Kcal"],
                    "Proteínas(g)": item["P"],
                    "Carboidratos(g)": item["C"],
                    "Gorduras(g)": item["G"],
                    "Alerta OMS": (
                        item.get("Risco", "")[:50] if item.get("Risco") else "-"
                    ),
                }
            )
else:
    for dia in dias_semana:
        for refeicao in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]:
            for item in st.session_state.cardapio_semanal.get(dia, {}).get(
                refeicao, []
            ):
                todos_alimentos.append(
                    {
                        "Dia": dia,
                        "Refeição": refeicao,
                        "Alimento": item["Ali"],
                        "Quantidade": item["Qtd"],
                        "Kcal": item["Kcal"],
                        "Proteínas(g)": item["P"],
                        "Carboidratos(g)": item["C"],
                        "Gorduras(g)": item["G"],
                        "Alerta OMS": (
                            item.get("Risco", "")[:50] if item.get("Risco") else "-"
                        ),
                    }
                )

if todos_alimentos:
    df_resumo = pd.DataFrame(todos_alimentos)
    st.dataframe(df_resumo, use_container_width=True, hide_index=True)
    csv = df_resumo.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        "📥 Baixar Resumo em CSV",
        data=csv,
        file_name="resumo_alimentar.csv",
        mime="text/csv",
    )
else:
    st.info(
        "ℹ️ Nenhum alimento adicionado ainda. Adicione alimentos para gerar o resumo."
    )

# 26. RESUMO DO LAUDO TÉCNICO
st.markdown("---")
st.markdown("## 📋 RESUMO DO LAUDO TÉCNICO")

if saldo_diario != 0:
    if objetivo == "Perda de peso" and saldo_diario > 0:
        semanas_meta = (
            abs(diferenca_meta) / (variacao_semanal) if variacao_semanal > 0 else 0
        )
        texto_tempo = f"{max(1, int(semanas_meta))} semanas"
    elif objetivo == "Ganho de peso" and saldo_diario < 0:
        semanas_meta = (
            abs(diferenca_meta) / (variacao_semanal) if variacao_semanal > 0 else 0
        )
        texto_tempo = f"{max(1, int(semanas_meta))} semanas"
    else:
        texto_tempo = "Ajuste necessário"
else:
    texto_tempo = "Manutenção"

st.markdown(
    f"""
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
""",
    unsafe_allow_html=True,
)

# 27. BOTÃO PARA BAIXAR LAUDO COMPLETO EM CSV
st.markdown("---")
st.markdown("### 📥 Exportar Dados Completos")

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

dados_laudo = {
    "Informação": [
        "Data do relatório",
        "Tipo de Planejamento",
        "Período analisado",
        "Objetivo",
        "Peso Atual (kg)",
        "Altura (cm)",
        "Idade (anos)",
        "Sexo",
        "Meta de Peso (kg)",
        "Frequência de Atividade Física",
        "Gasto Total (GET) - kcal/dia",
        "Metabolismo Basal (TMB) - kcal/dia",
        "IMC Atual",
        "Classificação IMC",
        "Peso Ideal Estimado (kg)",
        "Percentual de Gordura (%)",
        "Massa de Gordura (kg)",
        "Massa Magra (kg)",
        "Consumo Total do Período (kcal)",
        "Média Diária de Consumo (kcal)",
        "Saldo Energético Diário (kcal)",
        "Status do Saldo",
        "Projeção de Variação em 30 dias (kg)",
        "Tempo Estimado para Meta",
        "Macronutrientes - Proteínas (g)",
        "Macronutrientes - Carboidratos (g)",
        "Macronutrientes - Gorduras (g)",
    ],
    "Valor": [
        pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
        st.session_state.planejamento_tipo,
        (
            "Hoje (1 dia)"
            if st.session_state.planejamento_tipo == "Diário"
            else "Semana completa (7 dias)"
        ),
        objetivo,
        peso_at,
        alt_cm,
        idade,
        sexo,
        p_alvo,
        naf_label,
        get_total,
        tmb,
        composicao["imc"],
        classificacao_imc,
        composicao["peso_ideal"],
        composicao["percentual_gordura"],
        composicao["massa_gordura"],
        composicao["massa_magra"],
        total_kcal,
        media_diaria,
        abs(saldo_diario),
        "Déficit" if saldo_diario > 0 else "Superávit",
        variacao_30dias,
        texto_tempo,
        total_prot,
        total_carb,
        total_gord,
    ],
}

df_laudo = pd.DataFrame(dados_laudo)

col_down1, col_down2 = st.columns(2)

with col_down1:
    csv_laudo = df_laudo.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        "📊 Baixar Laudo Técnico Completo (CSV)",
        data=csv_laudo,
        file_name=f"laudo_biogestao_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col_down2:
    if todos_alimentos:
        st.download_button(
            "🍽️ Baixar Cardápio Detalhado (CSV)",
            data=df_resumo.to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"cardapio_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.caption(
    "Os arquivos CSV podem ser abertos no Excel, Google Sheets ou qualquer editor de planilhas"
)

# 28. INFORMAÇÃO OMS E DOCUMENTAÇÃO TÉCNICA
with st.expander("📋 Informações OMS e Documentação Técnica", expanded=False):
    st.markdown(
        """
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
    
    ---
    
    ### 📚 Documentação Técnica do BioGestão 360
    
    Conheça as fórmulas científicas utilizadas no app:
    
    | Cálculo | Fórmula | Fonte |
    |---------|---------|-------|
    | **TMB (Homens)** | 66.47 + (13.75 × peso) + (5.0 × altura) - (6.75 × idade) | Harris-Benedict (1919) |
    | **TMB (Mulheres)** | 655.1 + (9.56 × peso) + (1.85 × altura) - (4.67 × idade) | Harris-Benedict (1919) |
    | **% Gordura (IMC)** | (1.20 × IMC) + (0.23 × idade) - (16.2 ou 5.4) | Deurenberg et al. |
    | **% Gordura (Dobras)** | Protocolo Jackson & Pollock + Fórmula de Siri | ACSM |
    
    ### 📊 Sobre as Tabelas Nutricionais (TACO)
    
    O BioGestão 360 utiliza a **Tabela Brasileira de Composição de Alimentos** desenvolvida pela UNICAMP.
    
    | Arquivo | Conteúdo | Importância |
    |---------|----------|-------------|
    | **alimentos.csv** | Calorias, proteínas, carboidratos, gorduras | Base para cálculo nutricional diário |
    | **acidos-graxos.csv** | Perfil de ácidos graxos (saturados, insaturados, trans) | ⚠️ Gorduras saturadas em excesso aumentam colesterol. Gorduras insaturadas (ômega 3) são anti-inflamatórias |
    | **aminoacidos.csv** | Perfil de aminoácidos essenciais e não essenciais | ⚠️ Essenciais para construção muscular. Deficiência pode prejudicar ganho de massa magra |
    
    **Por que esses detalhes importam?**
    
    - **Ácidos graxos**: Consumir mais gorduras boas (peixes, azeite) e menos gorduras ruins (frituras, processados) ajuda no controle do colesterol e inflamação.
    - **Aminoácidos**: São os blocos de construção dos músculos. Quem quer **ganhar massa muscular** precisa de proteínas completas (que contêm todos os aminoácidos essenciais).
    
    > 🔗 Fonte oficial: [github.com/machine-learning-mocha/taco](https://github.com/machine-learning-mocha/taco)
    
    📄 [📥 Baixar Documentação Técnica Completa](https://raw.githubusercontent.com/adilsonximenes/biogestao-360/main/DOCUMENTO_TECNICO.md)
    
    🔗 [🌐 Ver no GitHub](https://github.com/adilsonximenes/biogestao-360/blob/main/DOCUMENTO_TECNICO.md)
    """
    )

# 29. BOTÃO DE LIMPAR
if st.session_state.planejamento_tipo == "Diário":
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        total_itens = sum(len(itens) for itens in st.session_state.cardapio.values())
        if total_itens > 0 and not st.session_state.modo_impressao:
            if st.button("🗑️ LIMPAR CARDÁPIO COMPLETO", use_container_width=True):
                limpar_cardapio()

# 30. SAIR DO MODO IMPRESSÃO
if st.session_state.modo_impressao:
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔙 Sair do Modo Impressão", use_container_width=True):
            st.session_state.modo_impressao = False
            st.rerun()

# 31. DICAS DE IMPRESSÃO (antes do rodapé)
with st.expander("🖨️ Dicas para melhor impressão", expanded=False):
    st.markdown(
        """
    ### ⚠️ Atenção
    A impressão nativa do navegador (Ctrl+P) pode cortar gráficos, tabelas e legendas.
    
    ### ✅ Soluções recomendadas
    
    **1. Extensão GoFullPage (Chrome/Edge) - Gratuita**
    - Capture a página inteira sem cortes
    - Salve como PDF com um clique
    """
    )

# 32. RODAPÉ
st.markdown(
    """
<div style='text-align: center; font-size: 11px; color: #666; padding: 15px;'>
    <b>BioGestão 360 v3.0</b> | Tabela TACO (UNICAMP) | Equações Harris-Benedict<br>
    <b>⚠️ SISTEMA EM DESENVOLVIMENTO - DADOS PODEM CONTER ERRO</b><br>
    📚 <a href='https://github.com/adilsonximenes/biogestao-360/blob/main/DOCUMENTO_TECNICO.md' target='_blank'>Documentação Técnica</a> | 
    💻 <a href='https://github.com/adilsonximenes/biogestao-360' target='_blank'>Código Fonte</a>
</div>
""",
    unsafe_allow_html=True,
)
