import streamlit as st
import pandas as pd
import os
import math
import plotly.express as px
import plotly.graph_objects as go
import qrcode
import io
import unicodedata
from PIL import Image
import base64
from datetime import datetime, timedelta

# ============================================
# 1. CONFIGURAÇÃO DE PÁGINA
# ============================================
st.set_page_config(
    page_title="BioGestão 360 - Profissional", layout="wide", page_icon="🏋️"
)

# ============================================
# 2. INICIALIZAÇÕES
# ============================================
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
if "fonte_dados" not in st.session_state:
    st.session_state.fonte_dados = "TACO (UNICAMP)"
if "metodo_get" not in st.session_state:
    st.session_state.metodo_get = "Harris-Benedict (Peso Total)"
if "sexo" not in st.session_state:
    st.session_state.sexo = None

# NOVAS INICIALIZAÇÕES - DADOS DO PACIENTE E PROFISSIONAL
if "dados_paciente" not in st.session_state:
    st.session_state.dados_paciente = {
        "nome": "",
        "data_nascimento": "",
        "telefone": "",
        "email": "",
    }
if "dados_profissional" not in st.session_state:
    st.session_state.dados_profissional = {
        "nome": "",
        "registro": "",
        "especialidade": "Nutrição",
    }
if "dados_consulta" not in st.session_state:
    st.session_state.dados_consulta = {
        "clinica": "",
        "data_inicio": datetime.now().strftime("%Y-%m-%d"),
        "data_retorno": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "observacoes": "",
    }


# ============================================
# NOVA FUNÇÃO PARA GERAR HTML DO LAUDO
# ============================================
def gerar_html_laudo():
    """Gera HTML para PDF com os dados atuais da tela"""
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Laudo BioGestão 360</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #f59e0b; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .section {{ margin-bottom: 25px; page-break-inside: avoid; }}
            .section h2 {{ background: #1e3a5f; color: white; padding: 10px; border-radius: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background: #f59e0b; color: white; }}
            .footer {{ text-align: center; margin-top: 40px; font-size: 10px; color: #999; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏋️ BioGestão 360 - Laudo Técnico</h1>
            <p>Gerado em {data_atual}</p>
        </div>
        
        <div class="section">
            <h2>📋 DADOS DA CONSULTA</h2>
            <p><strong>Paciente:</strong> {st.session_state.dados_paciente.get('nome', '-')}</p>
            <p><strong>Telefone:</strong> {st.session_state.dados_paciente.get('telefone', '-')}</p>
            <p><strong>Profissional:</strong> {st.session_state.dados_profissional.get('nome', '-')} | Registro: {st.session_state.dados_profissional.get('registro', '-')}</p>
            <p><strong>Clínica:</strong> {st.session_state.dados_consulta.get('clinica', '-')}</p>
            <p><strong>Data Início:</strong> {st.session_state.dados_consulta.get('data_inicio', '-')} | <strong>Retorno:</strong> {st.session_state.dados_consulta.get('data_retorno', '-')}</p>
        </div>
    """

    # Perfil (se disponível)
    if dados_validos:
        html += f"""
        <div class="section">
            <h2>⚡ PERFIL BIOLÓGICO</h2>
            <p><strong>Peso:</strong> {peso_at:.1f} kg | <strong>Altura:</strong> {alt_cm} cm | <strong>Idade:</strong> {idade} anos | <strong>Sexo:</strong> {sexo}</p>
            <p><strong>IMC:</strong> {composicao['imc']} | <strong>GET:</strong> {get_atual:.0f} kcal | <strong>TMB:</strong> {tmb_atual:.0f} kcal</p>
            <p><strong>Objetivo:</strong> {objetivo} | <strong>Meta:</strong> {p_alvo:.1f} kg</p>
        </div>
        """

    # Cardápio
    html += f"""
        <div class="section">
            <h2>🍽️ CARDÁPIO - {st.session_state.planejamento_tipo}</h2>
            <table>
                <thead><tr><th>Dia</th><th>Refeição</th><th>Alimento</th><th>Quantidade</th><th>Kcal</th><th>P</th><th>C</th><th>G</th></tr></thead>
                <tbody>
    """

    if st.session_state.planejamento_tipo == "Diário":
        for refeicao, itens in st.session_state.cardapio.items():
            for item in itens:
                html += f"<tr><td>Hoje</td><td>{refeicao}</td><td>{item['Ali']}</td><td>{item['Qtd']}</td><td>{item['Kcal']}</td><td>{item['P']}</td><td>{item['C']}</td><td>{item['G']}</td></tr>"
    else:
        for dia in [
            "Segunda",
            "Terça",
            "Quarta",
            "Quinta",
            "Sexta",
            "Sábado",
            "Domingo",
        ]:
            for refeicao in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]:
                for item in st.session_state.cardapio_semanal.get(dia, {}).get(
                    refeicao, []
                ):
                    html += f"<tr><td>{dia}</td><td>{refeicao}</td><td>{item['Ali']}</td><td>{item['Qtd']}</td><td>{item['Kcal']}</td><td>{item['P']}</td><td>{item['C']}</td><td>{item['G']}</td></tr>"

    html += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            BioGestão 360 | Este documento não substitui avaliação médica.
        </div>
    </body>
    </html>
    """

    return html


# ============================================
# 3. FUNÇÃO PARA GERAR QR CODE PIX
# ============================================
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


# ============================================
# 4. FUNÇÃO PARA GERAR BOTÃO PAYPAL
# ============================================
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


# ============================================
# 5. ALIMENTOS DE RISCO (Grupo OMS)
# ============================================
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


# ============================================
# 6. FUNÇÃO PARA CALCULAR COMPOSIÇÃO CORPORAL
# ============================================
def calcular_composicao_corporal(peso, altura, idade, sexo):
    if peso <= 0 or altura <= 0 or idade <= 0 or not sexo:
        return None
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


# ============================================
# 7. FUNÇÃO PARA CALCULAR TOTAIS
# ============================================
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


# ============================================
# 8. FUNÇÕES DE LIMPEZA
# ============================================
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


# ============================================
# 9. FUNÇÕES PARA TRATAR VALORES NUTRICIONAIS
# ============================================
def tratar_valor_nutricional(valor):
    if valor is None:
        return 0.0
    if pd.isna(valor):
        return 0.0
    if isinstance(valor, str):
        valor = valor.strip().upper()
        if valor in ["NA", "N/A", "*", "TR", "-", ""]:
            return 0.0
        valor = valor.replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            return 0.0
    if isinstance(valor, (int, float)):
        return float(valor) if not pd.isna(valor) else 0.0
    return 0.0


# ============================================
# 10. FUNÇÕES PARA CARREGAR TABELAS
# ============================================
@st.cache_data
def carregar_tabela_taco():
    try:
        if os.path.exists("alimentos.csv"):
            df = pd.read_csv("alimentos.csv", encoding="utf-8")
            return df
        else:
            st.warning(
                "Arquivo alimentos.csv não encontrado. Verifique se está na pasta correta."
            )
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar tabela TACO: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def carregar_tabela_ibge():
    try:
        if not os.path.exists("tabela_ibge.csv"):
            st.warning(
                "Arquivo tabela_ibge.csv não encontrado. Verifique se está na pasta correta."
            )
            return pd.DataFrame()

        cabecalho_linha = None
        with open("tabela_ibge.csv", "r", encoding="utf-8") as f:
            linhas = f.readlines()
            for i, linha in enumerate(linhas):
                if "CÓDIGO DO ALIMENTO" in linha and "DESCRIÇÃO DO ALIMENTO" in linha:
                    cabecalho_linha = i
                    break

        if cabecalho_linha is None:
            st.error("Não foi possível encontrar o cabeçalho da tabela IBGE.")
            return pd.DataFrame()

        df = pd.read_csv(
            "tabela_ibge.csv",
            encoding="utf-8",
            sep=";",
            skiprows=cabecalho_linha,
            on_bad_lines="skip",
        )
        df.columns = df.columns.str.strip()

        colunas_renomear = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if "código do alimento" in col_lower or "codigo do alimento" in col_lower:
                colunas_renomear[col] = "codigo"
            elif (
                "descrição do alimento" in col_lower
                or "descricao do alimento" in col_lower
            ):
                colunas_renomear[col] = "descricao"
            elif (
                "código da preparação" in col_lower
                or "codigo da preparacao" in col_lower
            ):
                colunas_renomear[col] = "codigo_preparacao"
            elif (
                "descrição da preparação" in col_lower
                or "descricao da preparacao" in col_lower
            ):
                colunas_renomear[col] = "preparacao"
            elif "energia (kcal)" in col_lower or "energia" in col_lower:
                colunas_renomear[col] = "energia_kcal"
            elif "proteína (g)" in col_lower or "proteina (g)" in col_lower:
                colunas_renomear[col] = "proteina_g"
            elif (
                "lipídeos totais (g)" in col_lower or "lipideos totais (g)" in col_lower
            ):
                colunas_renomear[col] = "lipideos_g"
            elif "carboidrato (g)" in col_lower:
                colunas_renomear[col] = "carboidrato_g"
            elif "fibra alimentar total (g)" in col_lower:
                colunas_renomear[col] = "fibra_g"

        df = df.rename(columns=colunas_renomear)

        if "descricao" in df.columns:
            if "preparacao" in df.columns:
                df["descricao_completa"] = (
                    df["descricao"].fillna("") + " - " + df["preparacao"].fillna("")
                )
            else:
                df["descricao_completa"] = df["descricao"]

        df = df.dropna(
            subset=(
                ["descricao_completa"]
                if "descricao_completa" in df.columns
                else ["descricao"]
            ),
            how="all",
        )
        return df
    except Exception as e:
        st.error(f"Erro ao carregar tabela do IBGE: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def carregar_acidosis_graxos():
    try:
        if os.path.exists("acidos-graxos.csv"):
            return pd.read_csv("acidos-graxos.csv", encoding="utf-8")
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data
def carregar_aminoacidos():
    try:
        if os.path.exists("aminoacidos.csv"):
            return pd.read_csv("aminoacidos.csv", encoding="utf-8")
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


# ============================================
# 11. FUNÇÃO PARA DETERMINAR PESO POR UNIDADE
# ============================================
def obter_peso_por_unidade(descricao_alimento):
    desc = descricao_alimento.lower() if descricao_alimento else ""
    pesos_por_unidade = {
        "biscoito": 5,
        "maisena": 4,
        "cream cracker": 5,
        "wafer": 6,
        "bolacha": 5,
        "cracker": 5,
        "sequilho": 5,
        "rosquinha": 6,
        "biscoito doce": 5,
        "biscoito salgado": 5,
        "pão francês": 50,
        "pão de forma": 25,
        "pão integral": 25,
        "torrada": 10,
        "croissant": 45,
        "brioche": 40,
        "pão de queijo": 30,
        "maçã": 150,
        "banana": 100,
        "laranja": 120,
        "pera": 130,
        "manga": 200,
        "melão": 300,
        "melancia": 400,
        "abacaxi": 500,
        "uva": 5,
        "morango": 12,
        "kiwi": 70,
        "ovo": 50,
        "omelete": 80,
        "ovo de codorna": 9,
        "queijo": 20,
        "muçarela": 20,
        "prato": 20,
        "minas": 30,
        "ricota": 25,
        "parmesão": 15,
        "presunto": 15,
        "mortadela": 15,
        "salame": 10,
        "hambúrguer": 80,
        "linguiça": 60,
        "salsicha": 50,
        "cenoura": 50,
        "beterraba": 60,
        "batata": 100,
        "tomate": 80,
        "cebola": 100,
        "pimentão": 100,
        "abobrinha": 150,
        "berinjela": 150,
        "chuchu": 150,
        "couve-flor": 200,
        "brócolis": 200,
    }
    for chave, peso in pesos_por_unidade.items():
        if chave in desc:
            return peso
    return 0


def obter_unidade_padrao(categoria, descricao_alimento):
    categoria_lower = categoria.lower() if categoria else ""
    descricao_lower = descricao_alimento.lower() if descricao_alimento else ""
    palavras_liquidas = [
        "suco",
        "leite",
        "café",
        "bebida",
        "água",
        "chá",
        "refrigerante",
        "cerveja",
        "vinho",
        "aguardente",
        "caldo",
        "achocolatado",
    ]
    palavras_unidade = ["ovo", "unidade", "codorna", "ovos", "biscoito", "pão", "fruta"]
    is_liquido = any(palavra in descricao_lower for palavra in palavras_liquidas)
    usa_unidade = any(palavra in descricao_lower for palavra in palavras_unidade)
    if usa_unidade:
        return "un", 1
    elif is_liquido:
        return "ml", 200
    else:
        return "g", 1


# ============================================
# 12. FUNÇÕES PARA OBTER VALORES NUTRICIONAIS
# ============================================
def obter_valor_nutricional_taco(item, fator_calc):
    kcal_raw = item.get("Energia..kcal.", 0)
    prot_raw = item.get("Proteína..g.", 0)
    carb_raw = item.get("Carboidrato..g.", 0)
    gord_raw = item.get("Lipídeos..g.", 0)
    return {
        "kcal": round(tratar_valor_nutricional(kcal_raw) * fator_calc, 1),
        "prot": round(tratar_valor_nutricional(prot_raw) * fator_calc, 1),
        "carb": round(tratar_valor_nutricional(carb_raw) * fator_calc, 1),
        "gord": round(tratar_valor_nutricional(gord_raw) * fator_calc, 1),
    }


def obter_valor_nutricional_ibge(item, fator_calc):
    kcal_raw = item.get("energia_kcal", 0)
    prot_raw = item.get("proteina_g", 0)
    carb_raw = item.get("carboidrato_g", 0)
    gord_raw = item.get("lipideos_g", 0)
    return {
        "kcal": round(tratar_valor_nutricional(kcal_raw) * fator_calc, 1),
        "prot": round(tratar_valor_nutricional(prot_raw) * fator_calc, 1),
        "carb": round(tratar_valor_nutricional(carb_raw) * fator_calc, 1),
        "gord": round(tratar_valor_nutricional(gord_raw) * fator_calc, 1),
    }


# ============================================
# 13. CSS PROFISSIONAL (MANTIDO IGUAL)
# ============================================
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
    
    .equipamento-adipometro {
        background: linear-gradient(135deg, #1e3a5f, #0f172a);
        border-left: 5px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 10px 0;
        color: #ffffff !important;
    }
    .equipamento-adipometro strong { color: #fbbf24 !important; }
    
    .equipamento-fita {
        background: linear-gradient(135deg, #1e3a5f, #0f172a);
        border-left: 5px solid #10b981;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 10px 0;
        color: #ffffff !important;
    }
    .equipamento-fita strong { color: #fbbf24 !important; }
    
    .equipamento-complementar {
        background: linear-gradient(135deg, #1e3a5f, #0f172a);
        border-left: 5px solid #f59e0b;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 10px 0;
        color: #ffffff !important;
    }
    .equipamento-complementar strong { color: #fbbf24 !important; }
    
    .seletor-fonte {
        background: linear-gradient(135deg, #1e3a5f, #0f172a);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #ffd700;
    }
    
    .metodo-selector {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
        border: 1px solid #ffd700;
    }
    .metodo-selector h4 {
        color: #ffd700 !important;
        margin-bottom: 10px;
    }
    
    .aviso-peso-real {
        background: linear-gradient(135deg, #fef3c7, #fffbeb);
        border-left: 8px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .aviso-peso-real h3 {
        color: #92400e !important;
        margin: 0 0 8px 0;
    }
    .aviso-peso-real p {
        color: #78350f !important;
        margin: 0;
        font-size: 15px;
    }
    .aviso-peso-real .grid-referencia {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin: 15px 0;
    }
    
    .aviso-peso-real .card-peso {
        background: #ffffff !important;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #fde68a;
    }
    .aviso-peso-real .card-peso strong {
        color: #d97706 !important;
    }
    .aviso-peso-real .card-peso br {
        display: block;
        margin: 4px 0;
    }
    .aviso-peso-real .card-peso span {
        color: #1e293b !important;
    }
    
    .aviso-peso-real .obs {
        margin-top: 12px;
        font-size: 13px;
        color: #92400e !important;
        background: #fffbeb;
        padding: 8px;
        border-radius: 6px;
        border: 1px solid #fde68a;
    }
    
    .instrucao-cientifica {
        background: linear-gradient(135deg, #e0f2fe, #f0f9ff);
        border-left: 5px solid #0284c7;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    .instrucao-cientifica h4 {
        color: #0369a1 !important;
        margin: 0 0 10px 0;
    }
    .instrucao-cientifica ol {
        margin: 0;
        padding-left: 20px;
        color: #0c4a6e !important;
    }
    .instrucao-cientifica p {
        margin-top: 10px;
        font-size: 13px;
        color: #0369a1 !important;
    }
    
    @media print {
        .stSidebar, [data-testid="stSidebarContent"] { display: none !important; }
        * { color: black !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
        body, .stApp, .main, .block-container, div, section, p, h1, h2, h3, h4, h5, h6, span, li, .stMarkdown, .stMetric,
        .card-com-explicacao, .perfil-gigante, .meta-gigante, .header-cafe, .header-almoco, .header-lanches, .header-jantar,
        .resumo-laudo, .aviso-cientifico, .privacidade-box, .equipamento-adipometro, .equipamento-fita, .equipamento-complementar,
        .aviso-peso-real, .instrucao-cientifica, .metodo-selector { color: black !important; background: white !important; }
        .banner-profissional h1 { background: none !important; -webkit-background-clip: unset !important; background-clip: unset !important;
            -webkit-text-fill-color: black !important; color: black !important; text-shadow: none !important; }
        table, .stDataFrame, .dataframe { border: 1px solid black !important; width: 100% !important; margin-left: 0 !important; margin-right: 0 !important; }
        th, td { border: 1px solid black !important; padding: 8px !important; color: black !important; background: white !important; }
        .js-plotly-plot .legend text, .plotly .legend text, .legend text, .g-legend text, .annotation-text { fill: black !important; color: black !important; font-weight: bold !important; }
        .js-plotly-plot .xtick text, .js-plotly-plot .ytick text, .plotly .xtick text, .plotly .ytick text { fill: black !important; color: black !important; }
        .js-plotly-plot .bar, .plotly .bar { opacity: 1 !important; }
        .stMarkdown, .stMarkdown p, .stMarkdown div, .card-com-explicacao, .card-com-explicacao *,
        .resumo-laudo, .resumo-laudo *, .aviso-cientifico, .aviso-cientifico *, .privacidade-box, .privacidade-box *,
        .aviso-peso-real, .aviso-peso-real *, .instrucao-cientifica, .instrucao-cientifica *, .metodo-selector, .metodo-selector * {
            color: black !important; background: white !important; }
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================
# 14. SIDEBAR (MANTIDA IGUAL)
# ============================================
with st.sidebar:
    st.markdown("### 👤 Perfil Biológico")
    st.markdown("---")

    peso_at = st.number_input(
        "📊 Peso Atual (kg)", 0.0, 300.0, 0.0, step=0.5, format="%.1f", key="peso_atual"
    )
    alt_cm = st.number_input("📏 Altura (cm)", 0, 250, 0, step=1, key="altura_cm")
    if alt_cm == 0:
        st.caption("💡 Exemplo: 165 cm = 1,65 m")

    idade = st.number_input("🎂 Idade (anos)", 0, 120, 0, step=1, key="idade_input")

    st.markdown("**⚥ Sexo Biológico**")
    col_sexo1, col_sexo2 = st.columns(2)
    with col_sexo1:
        if st.button("👨 Homem", key="btn_homem", use_container_width=True):
            st.session_state.sexo = "Masculino"
    with col_sexo2:
        if st.button("👩 Mulher", key="btn_mulher", use_container_width=True):
            st.session_state.sexo = "Feminino"

    sexo = st.session_state.sexo
    if sexo:
        st.caption(f"✅ Selecionado: {sexo}")
    else:
        st.caption("⬅️ Clique em um dos botões acima")

    st.markdown("---")
    st.markdown("### 🎯 Objetivos")

    objetivo = st.radio(
        "🎯 Seu objetivo principal:",
        ["Perda de peso", "Ganho de peso"],
        horizontal=True,
    )

    p_alvo = st.number_input(
        "🎯 Meta de Peso (kg)",
        0.0,
        300.0,
        0.0,
        step=0.5,
        format="%.1f",
        key="meta_peso",
    )
    if p_alvo > 0 and peso_at > 0:
        if objetivo == "Perda de peso" and p_alvo >= peso_at:
            st.warning(
                f"⚠️ Para perda de peso, a meta deve ser menor que {peso_at:.1f} kg"
            )
        elif objetivo == "Ganho de peso" and p_alvo <= peso_at:
            st.warning(
                f"⚠️ Para ganho de peso, a meta deve ser maior que {peso_at:.1f} kg"
            )

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
    st.markdown("### 📊 Fonte de Dados")

    fonte_dados = st.radio(
        "📚 Selecione a tabela nutricional:",
        ["TACO (UNICAMP)", "IBGE (POF 2008-2009)"],
        horizontal=False,
        index=0 if st.session_state.fonte_dados == "TACO (UNICAMP)" else 1,
    )

    st.session_state.fonte_dados = fonte_dados

    st.caption(
        """
    **TACO (UNICAMP):** Mais completa para alimentos industrializados.
    **IBGE (POF 2008-2009):** Mais alimentos in natura e preparações regionais.
    🔗 **Fontes:** TACO/UNICAMP | IBGE | FAO/WHO
    """
    )

    st.markdown("---")
    st.caption(
        "**📁 Arquivos de dados:** `alimentos.csv` (TACO) | `tabela_ibge.csv` (IBGE)"
    )
    st.caption("💡 Arquivos complementares: `acidos-graxos.csv`, `aminoacidos.csv`")

    st.markdown("---")
    planejamento_tipo = st.radio(
        "📅 Tipo de Planejamento:", ["Diário", "Semanal"], horizontal=True
    )
    if planejamento_tipo != st.session_state.planejamento_tipo:
        st.session_state.planejamento_tipo = planejamento_tipo

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
    st.caption("💡 **Dica:** Use a extensão GoFullPage para capturar a página inteira")


# ============================================
# 15. CARGA DE DADOS
# ============================================
@st.cache_data
def load_db():
    return carregar_tabela_taco(), carregar_tabela_ibge()


df_taco, df_ibge = load_db()

# ============================================
# 16. HEADER
# ============================================
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

# ============================================
# 17. DOAÇÕES E DICAS DE IMPRESSÃO
# ============================================
with st.expander("💚 Apoie este projeto - Colaboração voluntária", expanded=False):
    col_pix, col_paypal = st.columns(2)
    with col_pix:
        st.markdown("### 📱 PIX")
        st.image(gerar_qr_code_pix(), width=150)
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
    ✅ **Para melhor resultado:** Use a extensão **GoFullPage** (Chrome/Edge)
    """
    )
    st.caption("🌳 A natureza agradece o uso consciente do papel!")

# ============================================
# 18. POLÍTICA DE PRIVACIDADE
# ============================================
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

# ============================================
# 19. AVISO CIENTÍFICO
# ============================================
st.markdown(
    """
<div class='aviso-cientifico'>
    <strong>📋 INFORMAÇÃO CIENTÍFICA:</strong> Baseado na Tabela TACO (UNICAMP), Tabela IBGE (POF 2008-2009) e equações Harris-Benedict.
    <strong>⚠️ SISTEMA EM DESENVOLVIMENTO - DADOS PODEM CONTER ERRO</strong>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================
# 20. CÁLCULOS BIOMÉTRICOS
# ============================================
if peso_at > 0 and alt_cm > 0 and idade > 0 and sexo:
    alt_m = alt_cm / 100
    imc = peso_at / (alt_m**2)
    if sexo == "Masculino":
        tmb_harris = 66.47 + (13.75 * peso_at) + (5.0 * alt_cm) - (6.75 * idade)
    else:
        tmb_harris = 655.1 + (9.56 * peso_at) + (1.85 * alt_cm) - (4.67 * idade)
    get_harris = tmb_harris * naf_val
    composicao = calcular_composicao_corporal(peso_at, alt_cm, idade, sexo)

    if p_alvo > 0:
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
    else:
        texto_meta = "📝 Defina sua meta de peso acima"
        diferenca_meta = 0

    dados_validos = True
else:
    dados_validos = False
    composicao = None
    diferenca_meta = 0
    texto_meta = "📝 Preencha seus dados na barra lateral"

# ============================================
# 21. PERFIL GIGANTE (MANTIDO)
# ============================================
if dados_validos:
    st.markdown(
        f"""
    <div class='perfil-gigante'>
        <div class='titulo'>📋 SEU PERFIL</div>
        <div class='dados-container'>
            <div class='dado-item'><div class='dado-icon'>⚖️</div><div class='dado-valor'>{peso_at:.1f} kg</div><div class='dado-label'>Peso</div></div>
            <div class='dado-item'><div class='dado-icon'>📏</div><div class='dado-valor'>{alt_cm} cm</div><div class='dado-label'>Altura</div></div>
            <div class='dado-item'><div class='dado-icon'>🎂</div><div class='dado-valor'>{idade} anos</div><div class='dado-label'>Idade</div></div>
            <div class='dado-item'><div class='dado-icon'>⚥</div><div class='dado-valor'>{sexo}</div><div class='dado-label'>Sexo</div></div>
        </div>
        <div class='meta-gigante'>
            <div class='meta-titulo'>🎯 META DE PESO - {objetivo.upper()}</div>
            <div class='meta-valor'>{p_alvo:.1f} kg</div>
            <div class='meta-mensagem'>{texto_meta}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
    <div class='perfil-gigante'>
        <div class='titulo'>📋 SEU PERFIL</div>
        <div class='dados-container'>
            <div class='dado-item'><div class='dado-icon'>⚖️</div><div class='dado-valor'>-- kg</div><div class='dado-label'>Peso</div></div>
            <div class='dado-item'><div class='dado-icon'>📏</div><div class='dado-valor'>-- cm</div><div class='dado-label'>Altura</div></div>
            <div class='dado-item'><div class='dado-icon'>🎂</div><div class='dado-valor'>-- anos</div><div class='dado-label'>Idade</div></div>
            <div class='dado-item'><div class='dado-icon'>⚥</div><div class='dado-valor'>--</div><div class='dado-label'>Sexo</div></div>
        </div>
        <div class='meta-gigante'>
            <div class='meta-titulo'>🎯 META DE PESO</div>
            <div class='meta-valor'>-- kg</div>
            <div class='meta-mensagem'>📝 Preencha seus dados na barra lateral</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ============================================
# 22. DASHBOARD (MANTIDO)
# ============================================
st.markdown("## ⚡ Metabolismo e Gasto Energético")

if dados_validos:
    get_atual = get_harris
    tmb_atual = tmb_harris
    metodo_atual_nome = "Harris-Benedict (Peso Total)"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""<div class='card-com-explicacao'><div class='card-icon'>⚡</div>
        <div class='card-valor'>{get_atual:.0f} kcal</div><div class='card-titulo'>Gasto Total (GET)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Total de calorias que seu corpo gasta por dia.<br>📊 <strong>Como usar:</strong> Para manter o peso, consuma esta quantidade.</div></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""<div class='card-com-explicacao'><div class='card-icon'>🔥</div>
        <div class='card-valor'>{tmb_atual:.0f} kcal</div><div class='card-titulo'>Metabolismo Basal (TMB)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Calorias queimadas em repouso total.<br>📊 <strong>Como usar:</strong> É o mínimo que seu corpo precisa para viver.</div></div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""<div class='card-com-explicacao'><div class='card-icon'>📊</div>
        <div class='card-valor'>{composicao['imc']}</div><div class='card-titulo'>Índice de Massa Corporal (IMC)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Relação entre peso e altura.<br>📊 <strong>Referência:</strong> 18.5-25 = Saudável | 25-30 = Sobrepeso | >30 = Obesidade</div></div>""",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""<div class='card-com-explicacao'><div class='card-icon'>🎯</div>
        <div class='card-valor'>{composicao['peso_ideal']} kg</div><div class='card-titulo'>Peso Ideal Estimado</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Peso considerado mais saudável para sua altura.<br>📊 <strong>Como usar:</strong> Meta de longo prazo baseada em estudos científicos.</div></div>""",
            unsafe_allow_html=True,
        )
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            """<div class='card-com-explicacao'><div class='card-icon'>⚡</div>
        <div class='card-valor'>-- kcal</div><div class='card-titulo'>Gasto Total (GET)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Total de calorias que seu corpo gasta por dia.<br>📊 <strong>Como usar:</strong> Para manter o peso, consuma esta quantidade.</div></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """<div class='card-com-explicacao'><div class='card-icon'>🔥</div>
        <div class='card-valor'>-- kcal</div><div class='card-titulo'>Metabolismo Basal (TMB)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Calorias queimadas em repouso total.<br>📊 <strong>Como usar:</strong> É o mínimo que seu corpo precisa para viver.</div></div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """<div class='card-com-explicacao'><div class='card-icon'>📊</div>
        <div class='card-valor'>--</div><div class='card-titulo'>Índice de Massa Corporal (IMC)</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Relação entre peso e altura.<br>📊 <strong>Referência:</strong> 18.5-25 = Saudável | 25-30 = Sobrepeso | >30 = Obesidade</div></div>""",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """<div class='card-com-explicacao'><div class='card-icon'>🎯</div>
        <div class='card-valor'>-- kg</div><div class='card-titulo'>Peso Ideal Estimado</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Peso considerado mais saudável para sua altura.<br>📊 <strong>Como usar:</strong> Meta de longo prazo baseada em estudos científicos.</div></div>""",
            unsafe_allow_html=True,
        )

# ============================================
# 23. COMPOSIÇÃO CORPORAL (MANTIDO)
# ============================================
st.markdown("---")
st.markdown("## 🧬 Composição Corporal (Estimativa por IMC)")

if dados_validos:
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.markdown(
            f"""<div class='card-com-explicacao'><div class='card-icon'>🎯</div>
        <div class='card-valor'>{composicao['percentual_gordura']}%</div><div class='card-titulo'>Percentual de Gordura</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Porcentagem do seu corpo que é gordura.<br>📊 <strong>Referência:</strong> Homens: 10-25% | Mulheres: 18-32%</div></div>""",
            unsafe_allow_html=True,
        )
    with col_g2:
        st.markdown(
            f"""<div class='card-com-explicacao'><div class='card-icon'>⚖️</div>
        <div class='card-valor'>{composicao['massa_gordura']} kg</div><div class='card-titulo'>Massa de Gordura</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Peso total da gordura no seu corpo.<br>📊 <strong>Como usar:</strong> Acompanhe a redução para perder peso saudável.</div></div>""",
            unsafe_allow_html=True,
        )
    with col_g3:
        st.markdown(
            f"""<div class='card-com-explicacao'><div class='card-icon'>💪</div>
        <div class='card-valor'>{composicao['massa_magra']} kg</div><div class='card-titulo'>Massa Magra</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Músculos + ossos + órgãos.<br>📊 <strong>Como usar:</strong> Quanto maior, melhor para o metabolismo!</div></div>""",
            unsafe_allow_html=True,
        )
else:
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.markdown(
            """<div class='card-com-explicacao'><div class='card-icon'>🎯</div>
        <div class='card-valor'>--%</div><div class='card-titulo'>Percentual de Gordura</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Porcentagem do seu corpo que é gordura.<br>📊 <strong>Referência:</strong> Homens: 10-25% | Mulheres: 18-32%</div></div>""",
            unsafe_allow_html=True,
        )
    with col_g2:
        st.markdown(
            """<div class='card-com-explicacao'><div class='card-icon'>⚖️</div>
        <div class='card-valor'>-- kg</div><div class='card-titulo'>Massa de Gordura</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Peso total da gordura no seu corpo.<br>📊 <strong>Como usar:</strong> Acompanhe a redução para perder peso saudável.</div></div>""",
            unsafe_allow_html=True,
        )
    with col_g3:
        st.markdown(
            """<div class='card-com-explicacao'><div class='card-icon'>💪</div>
        <div class='card-valor'>-- kg</div><div class='card-titulo'>Massa Magra</div>
        <div class='card-explicacao'>💡 <strong>O que é?</strong> Músculos + ossos + órgãos.<br>📊 <strong>Como usar:</strong> Quanto maior, melhor para o metabolismo!</div></div>""",
            unsafe_allow_html=True,
        )

st.markdown("---")

# ============================================
# 24. NOVA SEÇÃO: DADOS DO PACIENTE E PROFISSIONAL
# ============================================
st.markdown("## 📋 IDENTIFICAÇÃO DA CONSULTA")

with st.expander("📝 Dados do Paciente e Profissional", expanded=True):
    col_pac1, col_pac2 = st.columns(2)

    with col_pac1:
        st.markdown("### 👤 Dados do Paciente")
        nome_paciente = st.text_input(
            "Nome completo do paciente",
            value=st.session_state.dados_paciente.get("nome", ""),
            key="nome_paciente_novo",
        )

        from datetime import date

        data_nascimento_default = None
        if st.session_state.dados_paciente.get("data_nascimento"):
            try:
                data_nascimento_default = datetime.strptime(
                    st.session_state.dados_paciente.get("data_nascimento"), "%Y-%m-%d"
                ).date()
            except:
                data_nascimento_default = date(1970, 1, 1)
        else:
            data_nascimento_default = date(1970, 1, 1)

        data_nascimento = st.date_input(
            "Data de nascimento",
            value=data_nascimento_default,
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            key="data_nascimento_novo",
        )

        if data_nascimento:
            hoje = date.today()
            idade_calculada = (
                hoje.year
                - data_nascimento.year
                - (
                    (hoje.month, hoje.day)
                    < (data_nascimento.month, data_nascimento.day)
                )
            )
            st.caption(f"📊 **Idade calculada: {idade_calculada} anos**")

        telefone_paciente = st.text_input(
            "Telefone para contato",
            value=st.session_state.dados_paciente.get("telefone", ""),
            key="telefone_paciente_novo",
        )
        email_paciente = st.text_input(
            "E-mail",
            value=st.session_state.dados_paciente.get("email", ""),
            key="email_paciente_novo",
        )

    with col_pac2:
        st.markdown("### 👨‍⚕️ Dados do Profissional Responsável")
        nome_profissional = st.text_input(
            "Nome do profissional (Nutricionista/Médico)",
            value=st.session_state.dados_profissional.get("nome", ""),
            key="nome_profissional_novo",
        )
        registro_profissional = st.text_input(
            "Nº de Registro (CRN/CRM)",
            value=st.session_state.dados_profissional.get("registro", ""),
            key="registro_profissional_novo",
        )
        especialidade = st.selectbox(
            "Especialidade",
            ["Nutrição", "Nutrição Esportiva", "Medicina", "Educação Física", "Outro"],
            index=[
                "Nutrição",
                "Nutrição Esportiva",
                "Medicina",
                "Educação Física",
                "Outro",
            ].index(
                st.session_state.dados_profissional.get("especialidade", "Nutrição")
            ),
            key="especialidade_novo",
        )

        st.markdown("### 🏢 Local da Consulta")
        nome_clinica = st.text_input(
            "Clínica/Consultório",
            value=st.session_state.dados_consulta.get("clinica", ""),
            key="nome_clinica_novo",
        )

    st.markdown("### 📅 Datas da Consulta")
    col_data1, col_data2 = st.columns(2)
    with col_data1:
        data_inicio = st.date_input(
            "Data de início do plano",
            value=(
                datetime.strptime(
                    st.session_state.dados_consulta.get(
                        "data_inicio", datetime.now().strftime("%Y-%m-%d")
                    ),
                    "%Y-%m-%d",
                )
                if st.session_state.dados_consulta.get("data_inicio")
                else datetime.now()
            ),
            key="data_inicio_novo",
        )
    with col_data2:
        data_retorno = st.date_input(
            "Data prevista para retorno",
            value=(
                datetime.strptime(
                    st.session_state.dados_consulta.get(
                        "data_retorno",
                        (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                    ),
                    "%Y-%m-%d",
                )
                if st.session_state.dados_consulta.get("data_retorno")
                else (datetime.now() + timedelta(days=30))
            ),
            key="data_retorno_novo",
        )

    observacoes = st.text_area(
        "Observações gerais (opcional)",
        value=st.session_state.dados_consulta.get("observacoes", ""),
        key="observacoes_consulta_novo",
        height=80,
    )

    # Salvar no session_state
    st.session_state.dados_paciente = {
        "nome": nome_paciente,
        "data_nascimento": (
            data_nascimento.strftime("%Y-%m-%d") if data_nascimento else ""
        ),
        "telefone": telefone_paciente,
        "email": email_paciente,
    }
    st.session_state.dados_profissional = {
        "nome": nome_profissional,
        "registro": registro_profissional,
        "especialidade": especialidade,
    }
    st.session_state.dados_consulta = {
        "clinica": nome_clinica,
        "data_inicio": data_inicio.strftime("%Y-%m-%d"),
        "data_retorno": data_retorno.strftime("%Y-%m-%d"),
        "observacoes": observacoes,
    }

st.markdown("---")

# ============================================
# 25. AVALIAÇÃO FÍSICA PROFISSIONAL (MANTIDA)
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
    
    ### 🫀 Pressão Arterial - Classificação (Ministério da Saúde 2024)
    
    | Classificação | Sistólica (mmHg) | Diastólica (mmHg) |
    |---------------|------------------|-------------------|
    | **Ótima** | < 120 | < 80 |
    | **Normal** | 120-129 | 80-84 |
    | **Pré-hipertensão** | 130-139 | 85-89 |
    | **Hipertensão Estágio 1** | 140-159 | 90-99 |
    | **Hipertensão Estágio 2** | 160-179 | 100-109 |
    | **Hipertensão Estágio 3** | ≥ 180 | ≥ 110 |
    
    > ⚠️ A partir de 130/85 mmHg já é considerado pré-hipertensão. Consulte um médico regularmente.
    
    ---
    
    ### 🧬 Sobre o Protocolo de Dobras (3 ou 7 dobras)
    
    | Protocolo | Dobras utilizadas | Precisão | Tempo de coleta |
    |-----------|-------------------|----------|-----------------|
    | **3 dobras** | Tríceps, Peitoral/Subescapular*, Abdome/Supra-ilíaca* | Boa (erro ~3-4%) | Rápido (~5 min) |
    | **7 dobras** | Todas as 7 dobras principais | Alta (erro ~2-3%) | Demorado (~15 min) |
    
    *Depende do sexo: Homens (Peitoral + Abdome) | Mulheres (Subescapular + Supra-ilíaca)
    
    **Recomendação:** Utilize 7 dobras para maior precisão clínica. 3 dobras é suficiente para triagem rápida.
    
    ---
    
    ### 📊 Sobre o GET por Katch-McArdle
    
    **Harris-Benedict (Método Padrão):**
    - Fórmula: TMB = 66.47 + (13.75 × peso) + (5.0 × altura) - (6.75 × idade)
    - Baseado no **PESO TOTAL** (gordura + massa magra)
    - Menos preciso para pessoas com alto % de gordura
    
    **Katch-McArdle (Método Alternativo):**
    - Fórmula: TMB = 370 + (21.6 × Massa Magra em kg)
    - Baseado apenas na **MASSA MAGRA** (músculos + ossos + órgãos)
    - **Mais preciso** porque a gordura não consome energia
    
    **Comparação:**
    | Método | Base | Quando usar |
    |--------|------|-------------|
    | Harris-Benedict | Peso total | Padrão, para todos |
    | Katch-McArdle | Massa magra | Para quem tem % de gordura elevado ou busca máxima precisão |
    
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
    
    ---
    
    ### 📊 Sobre as Tabelas Nutricionais
    
    O BioGestão 360 oferece duas opções de tabelas nutricionais:
    
    | Tabela | Fonte | Características |
    |--------|-------|-----------------|
    | **TACO (UNICAMP)** | Universidade Estadual de Campinas | Mais completa para alimentos industrializados e preparações comuns |
    | **IBGE (POF 2008-2009)** | Pesquisa de Orçamentos Familiares | Mais alimentos in natura e preparações regionais brasileiras |
    
    🔗 **Fontes oficiais:**
    - **TACO/UNICAMP:** https://www.tbca.net.br/
    - **IBGE - POF 2008-2009:** https://www.ibge.gov.br/estatisticas/sociais/populacao/9050-pesquisa-de-orcamentos-familiares.html
    - **FAO/WHO:** https://www.fao.org/
    
    > Este sistema é um **agregador de dados públicos** e não substitui a consulta a um profissional de saúde.
    
    ---
    
    ### 🥗 Recomendações práticas (OMS)
    
    - ✅ Prefira carnes brancas (frango, peixe)
    - ✅ Cozinhe em temperaturas mais baixas (vapor, cozido)
    - ✅ Evite frituras e churrascos em excesso
    - ✅ Aumente consumo de fibras (frutas, verduras, legumes)
    
    **Fonte:** Agência Internacional de Pesquisa sobre o Câncer (IARC/OMS)
    """
    )

usar_avaliacao = st.checkbox(
    "📊 Deseja realizar avaliação física completa?", value=False
)

if usar_avaliacao:
    if not dados_validos:
        st.warning(
            "⚠️ Preencha primeiro os dados do Perfil Biológico na barra lateral (Peso, Altura, Idade e Sexo)."
        )
    else:
        # ========== FUNÇÃO PARA CRIAR 3 MEDIÇÕES ==========
        def criar_medicao_tripla(nome, key_prefix=""):
            st.markdown(f"**{nome}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                m1 = st.number_input(
                    f"Medição 1 (mm)",
                    0.0,
                    80.0,
                    0.0,
                    step=0.5,
                    key=f"{key_prefix}_{nome}_m1",
                )
            with col2:
                m2 = st.number_input(
                    f"Medição 2 (mm)",
                    0.0,
                    80.0,
                    0.0,
                    step=0.5,
                    key=f"{key_prefix}_{nome}_m2",
                )
            with col3:
                m3 = st.number_input(
                    f"Medição 3 (mm)",
                    0.0,
                    80.0,
                    0.0,
                    step=0.5,
                    key=f"{key_prefix}_{nome}_m3",
                )
            media = (m1 + m2 + m3) / 3
            if media > 0:
                st.caption(f"📊 **Média: {media:.1f} mm**")
            return media

        st.markdown("---")

        # ========== DADOS DO AVALIADO ==========
        st.markdown("### 📋 Dados do Avaliado")
        col_nome, col_fc = st.columns(2)
        with col_nome:
            nome_avaliado = st.text_input(
                "📝 Nome do avaliado", placeholder="Ex: João Silva", key="nome_avaliado"
            )
        with col_fc:
            frequencia_cardiaca = st.number_input(
                "❤️ Frequência Cardíaca (pulsações/min)",
                0,
                200,
                0,
                step=1,
                key="freq_cardiaca",
            )

        st.markdown("### 🫀 Pressão Arterial")
        col_pas, col_pad = st.columns(2)
        with col_pas:
            pressao_sistolica = st.number_input(
                "Pressão Sistólica (máxima) - mmHg",
                0,
                250,
                0,
                step=1,
                key="pressao_sistolica",
            )
        with col_pad:
            pressao_diastolica = st.number_input(
                "Pressão Diastólica (mínima) - mmHg",
                0,
                150,
                0,
                step=1,
                key="pressao_diastolica",
            )

        # Classificação da Pressão
        if pressao_sistolica > 0 and pressao_diastolica > 0:
            if pressao_sistolica < 120 and pressao_diastolica < 80:
                classif_pressao = "🟢 Ótima"
            elif pressao_sistolica < 130 and pressao_diastolica < 85:
                classif_pressao = "🟡 Normal"
            elif pressao_sistolica < 140 and pressao_diastolica < 90:
                classif_pressao = "🟠 Pré-hipertensão"
            elif pressao_sistolica < 160 and pressao_diastolica < 100:
                classif_pressao = "🔴 Hipertensão Estágio 1"
            elif pressao_sistolica < 180 and pressao_diastolica < 110:
                classif_pressao = "🔴 Hipertensão Estágio 2"
            else:
                classif_pressao = "🔴 Hipertensão Estágio 3"
            st.caption(f"Classificação: {classif_pressao} (Ministério da Saúde 2024)")

        st.markdown("---")

        # SEÇÃO 1: ADIPÔMETRO
        st.markdown("## 📏 SEÇÃO 1: DOBRAS CUTÂNEAS (ADIPÔMETRO)")
        st.markdown(
            """<div class='equipamento-adipometro'><strong>🔵 ADIPÔMETRO (Plicômetro):</strong> Utilizado para medir a espessura da gordura subcutânea. 
        Estas medidas são usadas para calcular o <strong>percentual de gordura corporal</strong>.<br>Unidade: <strong>milímetros (mm)</strong></div>""",
            unsafe_allow_html=True,
        )
        st.caption(
            "💡 **Instruções:** Para cada dobra, realize 3 medições. O sistema calculará automaticamente a média. Meça sempre no **lado direito** do corpo."
        )

        sexo_avaliacao = st.radio(
            "Sexo para avaliação:",
            ["Masculino", "Feminino"],
            horizontal=True,
            key="sexo_avaliacao",
        )

        st.markdown("### 💪 Braços")
        triceps_media = criar_medicao_tripla("TRÍCEPS", "adipometro")
        biceps_media = criar_medicao_tripla("BÍCEPS", "adipometro")

        st.markdown("### 🏋️ Tronco")
        peitoral = criar_medicao_tripla("PEITORAL", "adipometro")
        subescapular = criar_medicao_tripla("SUBESCAPULAR", "adipometro")
        abdominal = criar_medicao_tripla("ABDOME", "adipometro")

        st.markdown("### 📐 Quadril / Axila")
        axilar = criar_medicao_tripla("AXILAR MÉDIA", "adipometro")
        suprailiaca = criar_medicao_tripla("SUPRA-ILÍACA", "adipometro")

        st.markdown("### 🆕 Supra-espinal (SS)")
        st.caption(
            "Utilizada no cálculo do somatotipo de Heath-Carter. Localizada 5-7 cm acima da espinha ilíaca anterior."
        )
        supra_espinal = criar_medicao_tripla("SUPRA-ESPINAL", "adipometro")

        st.markdown("### 🦵 Pernas")
        coxa_media = criar_medicao_tripla("COXA", "adipometro")
        panturrilha_media = criar_medicao_tripla("PANTURRILHA", "adipometro")

        # SEÇÃO 2: FITA MÉTRICA
        st.markdown("---")
        st.markdown("## 📏 SEÇÃO 2: CIRCUNFERÊNCIAS (FITA MÉTRICA)")
        st.markdown(
            """<div class='equipamento-fita'><strong>🟢 FITA MÉTRICA:</strong> Utilizada para medir perímetros musculares e circunferências corporais.
        Estas medidas avaliam o <strong>tamanho muscular</strong> e a distribuição da gordura.<br>Unidade: <strong>centímetros (cm)</strong></div>""",
            unsafe_allow_html=True,
        )

        col_fita1, col_fita2 = st.columns(2)
        with col_fita1:
            st.markdown("**💪 Braço Contraído**")
            braco_d = st.number_input(
                "Braço Direito (cm)", 0.0, 60.0, 0.0, step=0.5, key="braco_d"
            )
            braco_e = st.number_input(
                "Braço Esquerdo (cm)", 0.0, 60.0, 0.0, step=0.5, key="braco_e"
            )
            braco_media_cm = (
                (braco_d + braco_e) / 2 if braco_d > 0 or braco_e > 0 else 0
            )
            if braco_media_cm > 0:
                st.caption(f"Média: {braco_media_cm:.1f} cm")

            st.markdown("**📏 Peitoral / Tórax**")
            st.caption("Medida na altura dos mamilos, em expiração normal.")
            peitoral_cm = st.number_input(
                "Circunferência Torácica (cm)",
                0.0,
                150.0,
                0.0,
                step=0.5,
                key="peitoral_cm",
            )

            st.markdown("**📐 Cintura**")
            cintura = st.number_input(
                "Circunferência da Cintura (cm)",
                0.0,
                150.0,
                0.0,
                step=0.5,
                key="cintura",
            )

        with col_fita2:
            st.markdown("**🦵 Coxa**")
            coxa_cm_d = st.number_input(
                "Coxa Direita (cm)", 0.0, 80.0, 0.0, step=0.5, key="coxa_cm_d"
            )
            coxa_cm_e = st.number_input(
                "Coxa Esquerda (cm)", 0.0, 80.0, 0.0, step=0.5, key="coxa_cm_e"
            )
            coxa_media_cm = (
                (coxa_cm_d + coxa_cm_e) / 2 if coxa_cm_d > 0 or coxa_cm_e > 0 else 0
            )
            if coxa_media_cm > 0:
                st.caption(f"Média: {coxa_media_cm:.1f} cm")

            st.markdown("**🦵 Panturrilha**")
            panturrilha_cm_d = st.number_input(
                "Panturrilha Direita (cm)",
                0.0,
                50.0,
                0.0,
                step=0.5,
                key="panturrilha_cm_d",
            )
            panturrilha_cm_e = st.number_input(
                "Panturrilha Esquerda (cm)",
                0.0,
                50.0,
                0.0,
                step=0.5,
                key="panturrilha_cm_e",
            )
            panturrilha_media_cm = (
                (panturrilha_cm_d + panturrilha_cm_e) / 2
                if panturrilha_cm_d > 0 or panturrilha_cm_e > 0
                else 0
            )
            if panturrilha_media_cm > 0:
                st.caption(f"Média: {panturrilha_media_cm:.1f} cm")

        st.markdown("**🫀 Relação Cintura-Quadril (RCQ)**")
        quadril = st.number_input(
            "Circunferência do Quadril (cm)", 0.0, 150.0, 0.0, step=0.5, key="quadril"
        )

        # CORREÇÃO DO ERRO rcq - DEFINIR VARIÁVEIS MESMO SE NÃO HOUVER DADOS
        rcq = 0
        risco_rcq = "-"
        if quadril > 0 and cintura > 0:
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
            """<div class='equipamento-complementar'><strong>🟡 Handgrip e Banco de Wells:</strong> Estas avaliações NÃO entram no cálculo do percentual de gordura,
        mas são importantes para o perfil completo do avaliado.</div>""",
            unsafe_allow_html=True,
        )

        col_comp1, col_comp2 = st.columns(2)
        with col_comp1:
            st.markdown("**🤝 Força de Preensão Palmar (Handgrip)**")
            st.caption(
                "Mede a força de preensão manual, indicador de força geral e saúde cardiovascular."
            )
            handgrip_d = st.number_input(
                "Handgrip Direito (kg/f)", 0.0, 80.0, 0.0, step=0.5, key="handgrip_d"
            )
            handgrip_e = st.number_input(
                "Handgrip Esquerdo (kg/f)", 0.0, 80.0, 0.0, step=0.5, key="handgrip_e"
            )
            handgrip_media = (
                (handgrip_d + handgrip_e) / 2 if handgrip_d > 0 or handgrip_e > 0 else 0
            )
            if handgrip_media > 0:
                if sexo_avaliacao == "Masculino":
                    nivel_forca = (
                        "🔴 Fraco"
                        if handgrip_media < 35
                        else ("🟡 Regular" if handgrip_media < 45 else "🟢 Forte")
                    )
                else:
                    nivel_forca = (
                        "🔴 Fraco"
                        if handgrip_media < 25
                        else ("🟡 Regular" if handgrip_media < 35 else "🟢 Forte")
                    )
                st.caption(f"Média: {handgrip_media:.1f} kg/f - Nível: {nivel_forca}")

        with col_comp2:
            st.markdown("**🧘 Flexibilidade (Banco de Wells)**")
            st.caption("Mede a flexibilidade da região lombar e posterior da coxa.")
            wells = st.number_input(
                "Banco de Wells (cm)", -20.0, 50.0, 0.0, step=0.5, key="wells"
            )
            if wells != 0:
                if sexo_avaliacao == "Masculino":
                    nivel_flex = (
                        "🔴 Abaixo"
                        if wells < 20
                        else ("🟡 Média" if wells < 30 else "🟢 Acima")
                    )
                else:
                    nivel_flex = (
                        "🔴 Abaixo"
                        if wells < 25
                        else ("🟡 Média" if wells < 35 else "🟢 Acima")
                    )
                st.caption(f"Flexibilidade: {wells:.1f} cm - Nível: {nivel_flex}")

        # ========== CÁLCULOS JACKSON & POLLOCK ==========
        st.markdown("---")
        st.markdown("#### 🔬 Protocolo de Dobras (Jackson & Pollock)")

        tem_medidas = (
            triceps_media > 0 or peitoral > 0 or abdominal > 0 or coxa_media > 0
        )

        if tem_medidas:
            if sexo_avaliacao == "Masculino":
                usar_7_dobras = (
                    st.radio(
                        "Escolha o protocolo:",
                        [
                            "3 dobras (Tríceps, Peitoral, Abdome)",
                            "7 dobras (Completo - mais preciso)",
                        ],
                        horizontal=True,
                        key="protocolo_masc",
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
                    if soma_dobras > 0:
                        densidade = (
                            1.112
                            - (0.00043499 * soma_dobras)
                            + (0.00000055 * (soma_dobras**2))
                            - (0.00028826 * idade)
                        )
                    else:
                        densidade = 0
                else:
                    soma_dobras = triceps_media + peitoral + abdominal
                    st.caption(f"📊 Soma das 3 dobras: {soma_dobras:.1f} mm")
                    if soma_dobras > 0:
                        densidade = (
                            1.10938
                            - (0.0008267 * soma_dobras)
                            + (0.0000016 * (soma_dobras**2))
                            - (0.0002574 * idade)
                        )
                    else:
                        densidade = 0
            else:
                usar_7_dobras = (
                    st.radio(
                        "Escolha o protocolo:",
                        [
                            "3 dobras (Tríceps, Supra-ilíaca, Coxa)",
                            "7 dobras (Completo - mais preciso)",
                        ],
                        horizontal=True,
                        key="protocolo_fem",
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
                    if soma_dobras > 0:
                        densidade = (
                            1.097
                            - (0.00046971 * soma_dobras)
                            + (0.00000056 * (soma_dobras**2))
                            - (0.00012828 * idade)
                        )
                    else:
                        densidade = 0
                else:
                    soma_dobras = triceps_media + suprailiaca + coxa_media
                    st.caption(f"📊 Soma das 3 dobras: {soma_dobras:.1f} mm")
                    if soma_dobras > 0:
                        densidade = (
                            1.0994921
                            - (0.0009929 * soma_dobras)
                            + (0.0000023 * (soma_dobras**2))
                            - (0.0001392 * idade)
                        )
                    else:
                        densidade = 0

            if densidade > 0:
                percentual_gordura_jp = ((4.95 / densidade) - 4.5) * 100
                percentual_gordura_jp = max(5, min(50, percentual_gordura_jp))
            else:
                percentual_gordura_jp = 0

            if percentual_gordura_jp > 0:
                massa_gordura_jp = peso_at * (percentual_gordura_jp / 100)
                massa_magra_jp = peso_at - massa_gordura_jp

                # Classificações
                if sexo_avaliacao == "Masculino":
                    if percentual_gordura_jp < 6:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Gordura Essencial",
                            "Muito abaixo do ideal",
                            "Baixo (atletas de elite)",
                        )
                    elif percentual_gordura_jp < 14:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Atleta",
                            "Abaixo do ideal (atleta)",
                            "Muito baixo",
                        )
                    elif percentual_gordura_jp < 18:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Saudável",
                            "Normal",
                            "Baixo",
                        )
                    elif percentual_gordura_jp < 25:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Aceitável",
                            "Sobrepeso",
                            "Moderado",
                        )
                    else:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Elevado",
                            "Obesidade",
                            "Alto",
                        )
                else:
                    if percentual_gordura_jp < 12:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Gordura Essencial",
                            "Muito abaixo do ideal",
                            "Baixo (atletas de elite)",
                        )
                    elif percentual_gordura_jp < 21:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Atleta",
                            "Abaixo do ideal (atleta)",
                            "Muito baixo",
                        )
                    elif percentual_gordura_jp < 25:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Saudável",
                            "Normal",
                            "Baixo",
                        )
                    elif percentual_gordura_jp < 32:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Aceitável",
                            "Sobrepeso",
                            "Moderado",
                        )
                    else:
                        classif_gordura, grau_obesidade, risco_saude = (
                            "Elevado",
                            "Obesidade",
                            "Alto",
                        )

                # Biotipo
                if percentual_gordura_jp > 25:
                    biotipo, cor_biotipo = "Endomorfo", "#ef4444"
                    desc_biotipo = (
                        "Tendência a acumular gordura, corpo mais arredondado."
                    )
                    recomendacao_biotipo = "Foco em déficit calórico moderado + treino de força de alta intensidade."
                elif percentual_gordura_jp < 12 and massa_magra_jp > (peso_at * 0.4):
                    biotipo, cor_biotipo = "Ectomorfo", "#3b82f6"
                    desc_biotipo = "Metabolismo acelerado, dificuldade para ganhar peso e massa muscular."
                    recomendacao_biotipo = "Foco em superávit calórico + treino de força com pouca frequência cardio."
                else:
                    biotipo, cor_biotipo = "Mesomorfo", "#10b981"
                    desc_biotipo = "Estrutura atlética natural, facilidade para ganhar massa muscular."
                    recomendacao_biotipo = "Treino equilibrado de força e cardio, facilidade para manutenção."

                # ========== SELEÇÃO DO MÉTODO DE CÁLCULO DO GET ==========
                st.markdown("---")
                st.markdown("### 🧮 Configuração do Gasto Energético (GET)")
                st.markdown(
                    """<div class='metodo-selector'><h4>📊 Método de Cálculo do GET</h4>
                <p>Escolha qual método será utilizado para calcular seu Gasto Energético Total (GET).</p></div>""",
                    unsafe_allow_html=True,
                )

                col_metodo1, col_metodo2 = st.columns(2)

                with col_metodo1:
                    tmb_katch = 370 + (21.6 * massa_magra_jp)
                    get_katch = tmb_katch * naf_val
                    st.markdown(
                        f"""<div style='background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 12px; padding: 15px; border: 2px solid {"#ffd700" if st.session_state.metodo_get == "Katch-McArdle (Massa Magra)" else "#3b82f6"};'>
                    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'><span style='font-size: 24px;'>📊</span><h4 style='color: #3b82f6; margin: 0;'>Harris-Benedict</h4></div>
                    <p style='color: #94a3b8; font-size: 13px;'>Baseado no <strong>PESO TOTAL</strong> ({peso_at:.1f} kg)</p>
                    <div style='display: flex; justify-content: space-between;'><div><div style='font-size: 11px; color: #94a3b8;'>TMB</div><div style='font-size: 24px; font-weight: bold; color: white;'>{tmb_harris:.0f} kcal</div></div>
                    <div><div style='font-size: 11px; color: #94a3b8;'>GET</div><div style='font-size: 24px; font-weight: bold; color: white;'>{get_harris:.0f} kcal</div></div></div>
                    <p style='color: #94a3b8; font-size: 11px; margin-top: 12px;'>✅ Padrão utilizado em estudos desde 1919</p></div>""",
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        "✅ Usar Harris-Benedict",
                        key="btn_harris",
                        use_container_width=True,
                    ):
                        st.session_state.metodo_get = "Harris-Benedict (Peso Total)"
                        st.rerun()

                with col_metodo2:
                    st.markdown(
                        f"""<div style='background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 12px; padding: 15px; border: 2px solid {"#ffd700" if st.session_state.metodo_get == "Katch-McArdle (Massa Magra)" else "#10b981"};'>
                    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'><span style='font-size: 24px;'>🧬</span><h4 style='color: #10b981; margin: 0;'>Katch-McArdle</h4></div>
                    <p style='color: #94a3b8; font-size: 13px;'>Baseado na <strong>MASSA MAGRA</strong> ({massa_magra_jp:.1f} kg)</p>
                    <div style='display: flex; justify-content: space-between;'><div><div style='font-size: 11px; color: #94a3b8;'>TMB</div><div style='font-size: 24px; font-weight: bold; color: white;'>{tmb_katch:.0f} kcal</div>
                    <div style='font-size: 12px; color: #fbbf24;'>{tmb_katch - tmb_harris:+.0f} kcal</div></div>
                    <div><div style='font-size: 11px; color: #94a3b8;'>GET</div><div style='font-size: 24px; font-weight: bold; color: white;'>{get_katch:.0f} kcal</div>
                    <div style='font-size: 12px; color: #fbbf24;'>{get_katch - get_harris:+.0f} kcal</div></div></div>
                    <p style='color: #94a3b8; font-size: 11px; margin-top: 12px;'>💡 <strong>MAIS PRECISO!</strong> A gordura não consome energia</p></div>""",
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        "✅ Usar Katch-McArdle",
                        key="btn_katch",
                        use_container_width=True,
                    ):
                        st.session_state.metodo_get = "Katch-McArdle (Massa Magra)"
                        st.rerun()

                # Atualizar GET conforme método selecionado
                if st.session_state.metodo_get == "Katch-McArdle (Massa Magra)":
                    tmb_atual = tmb_katch
                    get_atual = get_katch
                    metodo_atual_nome = "Katch-McArdle (Massa Magra)"
                else:
                    tmb_atual = tmb_harris
                    get_atual = get_harris
                    metodo_atual_nome = "Harris-Benedict (Peso Total)"

                st.info(
                    f"🔬 **Método selecionado:** {metodo_atual_nome}\n\nEste método será utilizado para calcular seu Gasto Energético Total (GET) e TMB."
                )

                # Exibir resultados da avaliação
                st.markdown("---")
                st.markdown("### 📊 Resultado da Avaliação Física (Jackson & Pollock)")

                col_jp1, col_jp2, col_jp3 = st.columns(3)
                with col_jp1:
                    st.markdown(
                        f"""<div class='card-com-explicacao'><div class='card-icon'>🎯</div>
                    <div class='card-valor'>{percentual_gordura_jp:.1f}%</div><div class='card-titulo'>% Gordura (Adipômetro)</div>
                    <div class='card-explicacao'>Classificação: {classif_gordura}<br>Risco: {risco_saude}</div></div>""",
                        unsafe_allow_html=True,
                    )
                with col_jp2:
                    st.markdown(
                        f"""<div class='card-com-explicacao'><div class='card-icon'>⚖️</div>
                    <div class='card-valor'>{massa_gordura_jp:.1f} kg</div><div class='card-titulo'>Massa de Gordura</div>
                    <div class='card-explicacao'>{((massa_gordura_jp/peso_at)*100):.1f}% do peso total</div></div>""",
                        unsafe_allow_html=True,
                    )
                with col_jp3:
                    st.markdown(
                        f"""<div class='card-com-explicacao'><div class='card-icon'>💪</div>
                    <div class='card-valor'>{massa_magra_jp:.1f} kg</div><div class='card-titulo'>Massa Magra</div>
                    <div class='card-explicacao'>{((massa_magra_jp/peso_at)*100):.1f}% do peso total</div></div>""",
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
                            "Valor": [
                                percentual_gordura_jp,
                                100 - percentual_gordura_jp,
                            ],
                        }
                    )
                    fig_pizza = px.pie(
                        composicao_corpo,
                        values="Valor",
                        names="Componente",
                        title="Proporção do seu corpo",
                        color="Componente",
                        color_discrete_map={
                            "Massa Gorda": "#ef4444",
                            "Massa Magra": "#3b82f6",
                        },
                    )
                    fig_pizza.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        height=350,
                    )
                    st.plotly_chart(fig_pizza, use_container_width=True)
                with col_biotipo:
                    st.markdown(
                        f"""<div class='card-com-explicacao' style='border-left: 5px solid {cor_biotipo};'>
                    <div class='card-icon'>🧬</div><div class='card-valor' style='color: {cor_biotipo};'>{biotipo}</div>
                    <div class='card-titulo'>Biotipo Corporal</div><div class='card-explicacao'>{desc_biotipo}<br><br>
                    <strong>Recomendação:</strong> {recomendacao_biotipo}</div></div>""",
                        unsafe_allow_html=True,
                    )

                # Gráficos comparativos
                st.markdown("---")
                st.markdown("#### 📊 Comparativo com Referências de Saúde")
                referencia_saudavel = 17 if sexo_avaliacao == "Masculino" else 24
                referencia_atleta = 12 if sexo_avaliacao == "Masculino" else 20
                referencia_obesidade = 25 if sexo_avaliacao == "Masculino" else 32
                referencia_essencial = 5 if sexo_avaliacao == "Masculino" else 12

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
                )
                st.plotly_chart(fig_comparacao, use_container_width=True)

                # Gráfico por idade
                st.markdown("---")
                st.markdown("#### 📈 Percentual de Gordura por Idade (Referência)")
                idades = list(range(20, 71, 5))
                if sexo_avaliacao == "Masculino":
                    percentuais_referencia = [
                        18,
                        19,
                        20,
                        22,
                        23,
                        24,
                        25,
                        26,
                        27,
                        28,
                        29,
                    ]
                else:
                    percentuais_referencia = [
                        25,
                        26,
                        27,
                        29,
                        30,
                        31,
                        32,
                        33,
                        34,
                        35,
                        36,
                    ]
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
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=400,
                )
                st.plotly_chart(fig_idade, use_container_width=True)

                # ========== LAUDO DA AVALIAÇÃO FÍSICA COMPLETO ==========
                st.markdown("---")
                st.markdown("## 🖨️ LAUDO DA AVALIAÇÃO FÍSICA")
                st.markdown(
                    "*Este laudo pode ser impresso para arquivo pessoal ou para compartilhar com profissionais*"
                )

                # Classificação IMC para o laudo
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
                | **Nome** | {nome_avaliado if nome_avaliado else '-'} |
                | **Peso** | {peso_at:.1f} kg |
                | **Altura** | {alt_cm} cm |
                | **Idade** | {idade} anos |
                | **IMC** | {imc:.1f} ({classificacao_imc_laudo}) |
                | **Frequência Cardíaca** | {frequencia_cardiaca} bpm {f'({classif_pressao})' if frequencia_cardiaca > 0 else '-'} |
                | **Pressão Arterial** | {pressao_sistolica}/{pressao_diastolica} mmHg {f'({classif_pressao})' if pressao_sistolica > 0 and pressao_diastolica > 0 else '-'} |
                """
                )

                st.markdown(
                    "### 📏 Resultados da Avaliação por Dobras Cutâneas (Adipômetro)"
                )
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
                # CORREÇÃO: Usar rcq_valor seguro
                rcq_valor = f"{rcq:.2f}" if rcq > 0 else "-"
                risco_rcq_valor = risco_rcq if risco_rcq != "-" else "-"
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
                | **Relação Cintura-Quadril** | {rcq_valor} - {risco_rcq_valor} |
                """
                )

                st.markdown("### 💪 Resultados das Avaliações Complementares")
                st.markdown(
                    f"""
                | Medida | Valor |
                |--------|-------|
                | **Handgrip (média D+E)** | {handgrip_media:.1f} kg/f - {nivel_forca if handgrip_media > 0 else '-'} |
                | **Banco de Wells** | {wells:.1f} cm - {nivel_flex if wells != 0 else '-'} |
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

                st.markdown("### 📊 Método de Cálculo do GET Selecionado")
                st.markdown(
                    f"""
                | Item | Informação |
                |------|-------------|
                | **Método Utilizado** | {metodo_atual_nome} |
                | **TMB Calculada** | {tmb_atual:.0f} kcal/dia |
                | **GET Calculado** | {get_atual:.0f} kcal/dia |
                | **Fator de Atividade** | {naf_label} ({naf_val}) |
                
                **Sobre o método:** {'Baseado no PESO TOTAL (Harris-Benedict, 1919)' if 'Harris' in metodo_atual_nome else 'Baseado na MASSA MAGRA (Katch-McArdle) - MAIS PRECISO!'}
                """
                )

                # Botão para baixar Laudo da Avaliação Física em CSV e PDF
st.markdown("---")
st.markdown("#### 📥 Exportar Laudo da Avaliação Física")

col_avaliacao1, col_avaliacao2 = st.columns(2)

with col_avaliacao1:
    dados_laudo_avaliacao = {
        "Categoria": [
            "Data da Avaliação",
            "Nome do Avaliado",
            "Sexo",
            "Idade",
            "Peso",
            "Altura",
            "IMC",
            "Frequência Cardíaca",
            "Pressão Sistólica",
            "Pressão Diastólica",
            "Classificação Pressão",
            "Protocolo de Dobras",
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
            "Flexibilidade Banco de Wells (cm)",
            "Método GET Selecionado",
            "TMB Calculada (kcal/dia)",
            "GET Calculado (kcal/dia)",
            "Fator de Atividade Física",
        ],
        "Valor": [
            pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
            nome_avaliado if nome_avaliado else "-",
            sexo_avaliacao,
            idade,
            f"{peso_at:.1f} kg",
            f"{alt_cm} cm",
            f"{imc:.1f}",
            (f"{frequencia_cardiaca} bpm" if frequencia_cardiaca > 0 else "-"),
            f"{pressao_sistolica} mmHg" if pressao_sistolica > 0 else "-",
            f"{pressao_diastolica} mmHg" if pressao_diastolica > 0 else "-",
            classif_pressao if "classif_pressao" in locals() else "-",
            f"Jackson & Pollock - {'7 dobras' if usar_7_dobras else '3 dobras'}",
            f"{soma_dobras:.1f} mm" if soma_dobras > 0 else "-",
            f"{densidade:.3f}" if densidade > 0 else "-",
            f"{percentual_gordura_jp:.1f}%",
            classif_gordura,
            risco_saude,
            f"{massa_gordura_jp:.1f} kg",
            f"{massa_magra_jp:.1f} kg",
            biotipo,
            f"{braco_media_cm:.1f} cm" if braco_media_cm > 0 else "-",
            f"{peitoral_cm:.1f} cm" if peitoral_cm > 0 else "-",
            f"{coxa_media_cm:.1f} cm" if coxa_media_cm > 0 else "-",
            (f"{panturrilha_media_cm:.1f} cm" if panturrilha_media_cm > 0 else "-"),
            f"{cintura:.1f} cm" if cintura > 0 else "-",
            f"{quadril:.1f} cm" if quadril > 0 else "-",
            f"{rcq:.2f}" if rcq > 0 else "-",
            f"{handgrip_media:.1f} kg/f" if handgrip_media > 0 else "-",
            f"{wells:.1f} cm" if wells != 0 else "-",
            metodo_atual_nome,
            f"{tmb_atual:.0f} kcal/dia",
            f"{get_atual:.0f} kcal/dia",
            f"{naf_label} ({naf_val})",
        ],
    }
    df_laudo_avaliacao = pd.DataFrame(dados_laudo_avaliacao)
    csv_laudo_avaliacao = df_laudo_avaliacao.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        "📊 Baixar CSV",
        data=csv_laudo_avaliacao,
        file_name=f"laudo_avaliacao_fisica_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col_avaliacao2:
    # Coletar todas as medidas
    medidas_dobras = []
    if triceps_media > 0:
        medidas_dobras.append(f"Tríceps: {triceps_media:.1f} mm")
    if biceps_media > 0:
        medidas_dobras.append(f"Bíceps: {biceps_media:.1f} mm")
    if peitoral > 0:
        medidas_dobras.append(f"Peitoral: {peitoral:.1f} mm")
    if subescapular > 0:
        medidas_dobras.append(f"Subescapular: {subescapular:.1f} mm")
    if abdominal > 0:
        medidas_dobras.append(f"Abdome: {abdominal:.1f} mm")
    if axilar > 0:
        medidas_dobras.append(f"Axilar: {axilar:.1f} mm")
    if suprailiaca > 0:
        medidas_dobras.append(f"Supra-ilíaca: {suprailiaca:.1f} mm")
    if coxa_media > 0:
        medidas_dobras.append(f"Coxa: {coxa_media:.1f} mm")
    if panturrilha_media > 0:
        medidas_dobras.append(f"Panturrilha: {panturrilha_media:.1f} mm")

    medidas_circunferencias = []
    if braco_media_cm > 0:
        medidas_circunferencias.append(f"Braço: {braco_media_cm:.1f} cm")
    if peitoral_cm > 0:
        medidas_circunferencias.append(f"Peitoral: {peitoral_cm:.1f} cm")
    if cintura > 0:
        medidas_circunferencias.append(f"Cintura: {cintura:.1f} cm")
    if quadril > 0:
        medidas_circunferencias.append(f"Quadril: {quadril:.1f} cm")
    if coxa_media_cm > 0:
        medidas_circunferencias.append(f"Coxa: {coxa_media_cm:.1f} cm")
    if panturrilha_media_cm > 0:
        medidas_circunferencias.append(f"Panturrilha: {panturrilha_media_cm:.1f} cm")

    # Criar gráficos
    import matplotlib.pyplot as plt
    import io

    # Gráfico 1: Composição Corporal
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    sizes1 = [percentual_gordura_jp, 100 - percentual_gordura_jp]
    ax1.pie(
        sizes1,
        labels=["Massa Gorda", "Massa Magra"],
        colors=["#ef4444", "#3b82f6"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax1.set_title("Composição Corporal", fontsize=12, fontweight="bold")
    plt.tight_layout()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    buf1.seek(0)
    grafico_composicao_b64 = base64.b64encode(buf1.getvalue()).decode("utf-8")
    plt.close()

    # Gráfico 2: Comparativo
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    categorias = ["Seu %", "Essencial", "Atleta", "Saudável", "Obesidade"]
    valores = [
        percentual_gordura_jp,
        referencia_essencial,
        referencia_atleta,
        referencia_saudavel,
        referencia_obesidade,
    ]
    cores = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"]
    ax2.bar(categorias, valores, color=cores)
    ax2.axhline(y=percentual_gordura_jp, color="red", linestyle="--", linewidth=2)
    ax2.set_title("Comparação do % de Gordura", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Percentual (%)")
    plt.tight_layout()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    buf2.seek(0)
    grafico_comparativo_b64 = base64.b64encode(buf2.getvalue()).decode("utf-8")
    plt.close()

    # Gráfico 3: Por Idade
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    idades_grafico = list(range(20, 71, 5))
    if sexo_avaliacao == "Masculino":
        percentuais_referencia = [18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29]
    else:
        percentuais_referencia = [25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36]
    ax3.plot(
        idades_grafico,
        percentuais_referencia,
        "o-",
        color="#f59e0b",
        linewidth=2,
        markersize=6,
        label="Referência ACSM",
    )
    ax3.axhline(
        y=percentual_gordura_jp,
        color="#ef4444",
        linestyle="--",
        linewidth=2,
        label=f"Seu valor: {percentual_gordura_jp:.1f}%",
    )
    ax3.set_title("Percentual de Gordura por Idade", fontsize=12, fontweight="bold")
    ax3.set_xlabel("Idade (anos)")
    ax3.set_ylabel("Percentual (%)")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    buf3 = io.BytesIO()
    plt.savefig(buf3, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    buf3.seek(0)
    grafico_idade_b64 = base64.b64encode(buf3.getvalue()).decode("utf-8")
    plt.close()

    # Classificação IMC
    if imc < 18.5:
        classificacao_imc_texto = "Abaixo do peso"
    elif imc < 25:
        classificacao_imc_texto = "Peso normal"
    elif imc < 30:
        classificacao_imc_texto = "Sobrepeso"
    elif imc < 35:
        classificacao_imc_texto = "Obesidade Grau I"
    elif imc < 40:
        classificacao_imc_texto = "Obesidade Grau II"
    else:
        classificacao_imc_texto = "Obesidade Grau III"

    data_atual_avaliacao = datetime.now().strftime("%d/%m/%Y às %H:%M")

    # Construir HTML das medidas
    dobras_html = ""
    for medida in medidas_dobras:
        partes = medida.split(": ")
        dobras_html += f'<div class="card"><div class="card-title">{partes[0]}</div><div class="card-value">{partes[1]}</div></div>'

    circunferencias_html = ""
    for medida in medidas_circunferencias:
        partes = medida.split(": ")
        circunferencias_html += f'<div class="card"><div class="card-title">{partes[0]}</div><div class="card-value">{partes[1]}</div></div>'

    if not dobras_html:
        dobras_html = '<div class="card"><div class="card-value">Nenhuma medida registrada</div></div>'
    if not circunferencias_html:
        circunferencias_html = '<div class="card"><div class="card-value">Nenhuma medida registrada</div></div>'

    html_avaliacao = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Laudo Avaliação Física</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: white; color: #1e293b; padding: 15px; font-size: 11pt; }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        h1 {{ color: #f59e0b; font-size: 18pt; text-align: center; border-bottom: 2px solid #f59e0b; padding-bottom: 8px; margin-bottom: 15px; }}
        h2 {{ background: linear-gradient(135deg, #1e3a5f, #0f172a); color: white; padding: 6px 10px; margin: 15px 0 10px 0; font-size: 13pt; border-radius: 6px; }}
        h3 {{ color: #1e3a5f; margin: 12px 0 8px 0; border-left: 4px solid #f59e0b; padding-left: 10px; font-size: 11pt; }}
        .subheader {{ text-align: center; color: #64748b; font-size: 9pt; margin-bottom: 15px; }}
        .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin: 8px 0; }}
        .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 8px 0; }}
        .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 8px 0; }}
        .card {{ border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px; background: #f8fafc; }}
        .card-title {{ font-size: 8pt; color: #64748b; margin-bottom: 3px; }}
        .card-value {{ font-size: 12pt; font-weight: bold; color: #1e293b; }}
        .metric-card {{ text-align: center; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px; background: #f8fafc; }}
        .metric-icon {{ font-size: 20pt; }}
        .metric-value {{ font-size: 15pt; font-weight: bold; color: #f59e0b; }}
        .metric-label {{ font-size: 8pt; color: #64748b; }}
        .graficos-container {{ text-align: center; margin: 15px 0; }}
        .graficos-container img {{ max-width: 100%; height: auto; border: 1px solid #e2e8f0; border-radius: 8px; margin: 8px 0; }}
        .explicacao {{ background: #f0f9ff; border-left: 4px solid #0284c7; padding: 10px; margin: 10px 0; font-size: 9pt; color: #0369a1; }}
        .info-box {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 10px; margin: 10px 0; font-size: 9pt; color: #92400e; }}
        .footer {{ text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #e2e8f0; font-size: 8pt; color: #94a3b8; }}
        @media print {{
            body {{ padding: 0; margin: 0; }}
            h2 {{ background: #333 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .page-break {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏋️ BioGestão 360 - Laudo de Avaliação Física</h1>
        <div class="subheader">Gerado em {data_atual_avaliacao}</div>
        
        <!-- DADOS DO AVALIADO -->
        <h2>📋 DADOS DO AVALIADO</h2>
        <div class="grid-2">
            <div class="card"><div class="card-title">👤 Nome</div><div class="card-value">{nome_avaliado if nome_avaliado else '-'}</div></div>
            <div class="card"><div class="card-title">⚥ Sexo</div><div class="card-value">{sexo_avaliacao}</div></div>
            <div class="card"><div class="card-title">🎂 Idade</div><div class="card-value">{idade} anos</div></div>
            <div class="card"><div class="card-title">⚖️ Peso</div><div class="card-value">{peso_at:.1f} kg</div></div>
            <div class="card"><div class="card-title">📏 Altura</div><div class="card-value">{alt_cm} cm</div></div>
            <div class="card"><div class="card-title">📊 IMC</div><div class="card-value">{imc:.1f} ({classificacao_imc_texto})</div></div>
            <div class="card"><div class="card-title">❤️ FC</div><div class="card-value">{frequencia_cardiaca if frequencia_cardiaca > 0 else '-'} bpm</div></div>
            <div class="card"><div class="card-title">🫀 Pressão</div><div class="card-value">{pressao_sistolica if pressao_sistolica > 0 else '-'}/{pressao_diastolica if pressao_diastolica > 0 else '-'} mmHg</div></div>
        </div>
        
        <!-- RESULTADOS PRINCIPAIS -->
        <h2>📊 RESULTADOS DA AVALIAÇÃO</h2>
        <div class="grid-3">
            <div class="metric-card"><div class="metric-icon">🎯</div><div class="metric-value">{percentual_gordura_jp:.1f}%</div><div class="metric-label">% Gordura</div></div>
            <div class="metric-card"><div class="metric-icon">⚖️</div><div class="metric-value">{massa_gordura_jp:.1f} kg</div><div class="metric-label">Massa Gorda</div></div>
            <div class="metric-card"><div class="metric-icon">💪</div><div class="metric-value">{massa_magra_jp:.1f} kg</div><div class="metric-label">Massa Magra</div></div>
        </div>
        
        <div class="grid-3">
            <div class="card"><div class="card-title">🏷️ Classificação</div><div class="card-value">{classif_gordura}</div></div>
            <div class="card"><div class="card-title">⚠️ Grau</div><div class="card-value">{grau_obesidade}</div></div>
            <div class="card"><div class="card-title">🩺 Risco à Saúde</div><div class="card-value">{risco_saude}</div></div>
        </div>
        
        <div class="info-box">
            <strong>💡 Sobre o percentual de gordura:</strong> Valores entre 14-17% (homens) e 21-24% (mulheres) são considerados saudáveis. 
            Seu percentual está na faixa {classif_gordura.lower()}, o que indica {risco_saude.lower()} risco para doenças cardiovasculares e metabólicas.
        </div>
        
        <!-- CIRCUNFERÊNCIAS -->
        <h2>📏 CIRCUNFERÊNCIAS CORPORAIS</h2>
        <div class="grid-2">
            <div class="card"><div class="card-title">💪 Braço</div><div class="card-value">{braco_media_cm:.1f} cm</div></div>
            <div class="card"><div class="card-title">📏 Peitoral</div><div class="card-value">{peitoral_cm:.1f} cm</div></div>
            <div class="card"><div class="card-title">🦵 Coxa</div><div class="card-value">{coxa_media_cm:.1f} cm</div></div>
            <div class="card"><div class="card-title">🦵 Panturrilha</div><div class="card-value">{panturrilha_media_cm:.1f} cm</div></div>
            <div class="card"><div class="card-title">📐 Cintura</div><div class="card-value">{cintura:.1f} cm</div></div>
            <div class="card"><div class="card-title">📐 Quadril</div><div class="card-value">{quadril:.1f} cm</div></div>
            <div class="card"><div class="card-title">🫀 RCQ</div><div class="card-value">{rcq:.2f} - {risco_rcq if risco_rcq != '-' else '-'}</div></div>
        </div>
        
        <div class="info-box">
            <strong>💡 Sobre a Relação Cintura-Quadril (RCQ):</strong> 
            {f'Seu valor de {rcq:.2f} está acima do recomendado (0.95 para homens, 0.85 para mulheres), indicando maior risco cardiovascular.' if rcq > (0.95 if sexo_avaliacao == 'Masculino' else 0.85) else f'Seu valor de {rcq:.2f} está dentro do recomendado, indicando baixo risco cardiovascular.'}
        </div>
        
        <!-- AVALIAÇÕES COMPLEMENTARES -->
        <h2>💪 AVALIAÇÕES COMPLEMENTARES</h2>
        <div class="grid-2">
            <div class="card"><div class="card-title">🤝 Handgrip</div><div class="card-value">{handgrip_media:.1f} kg/f - {nivel_forca if handgrip_media > 0 else '-'}</div></div>
            <div class="card"><div class="card-title">🧘 Wells</div><div class="card-value">{wells:.1f} cm - {nivel_flex if wells != 0 else '-'}</div></div>
        </div>
        
        <div class="info-box">
            <strong>💡 Interpretação:</strong> 
            A força de preensão ({handgrip_media:.1f} kg/f) é um indicador de força geral e saúde cardiovascular. 
            A flexibilidade ({wells:.1f} cm) indica a mobilidade da região lombar e posterior da coxa.
        </div>
        
        <!-- BIOTIPO -->
        <h2>🧬 BIOTIPO CORPORAL</h2>
        <div class="grid-3">
            <div class="metric-card"><div class="metric-icon">🏃</div><div class="metric-value">{biotipo}</div><div class="metric-label">Biotipo</div></div>
            <div class="card"><div class="card-title">📝 Descrição</div><div class="card-value">{desc_biotipo}</div></div>
            <div class="card"><div class="card-title">💡 Recomendação</div><div class="card-value">{recomendacao_biotipo}</div></div>
        </div>
        
        <!-- PROTOCOLO E GET -->
        <h2>📋 PROTOCOLO UTILIZADO</h2>
        <div class="grid-2">
            <div class="card"><div class="card-title">🔬 Protocolo de Dobras</div><div class="card-value">Jackson & Pollock {'(7 dobras)' if usar_7_dobras else '(3 dobras)'}</div></div>
            <div class="card"><div class="card-title">📐 Fórmula de Densidade</div><div class="card-value">Siri (1961)</div></div>
            <div class="card"><div class="card-title">🧰 Equipamentos</div><div class="card-value">Adipômetro, Fita Métrica, Handgrip, Banco de Wells</div></div>
            <div class="card"><div class="card-title">📚 Referência</div><div class="card-value">ACSM - American College of Sports Medicine</div></div>
        </div>
        
        <h2>⚡ GASTO ENERGÉTICO (GET)</h2>
        <div class="grid-2">
            <div class="card"><div class="card-title">🧮 Método</div><div class="card-value">{metodo_atual_nome}</div></div>
            <div class="card"><div class="card-title">🏃 Atividade</div><div class="card-value">{naf_label} ({naf_val})</div></div>
            <div class="card"><div class="card-title">🔥 TMB</div><div class="card-value">{tmb_atual:.0f} kcal/dia</div></div>
            <div class="card"><div class="card-title">⚡ GET</div><div class="card-value">{get_atual:.0f} kcal/dia</div></div>
        </div>
        
        <div class="info-box">
            <strong>💡 Sobre seu metabolismo:</strong> Seu Gasto Energético Total (GET) é de {get_atual:.0f} kcal por dia. 
            Este é o total de calorias que seu corpo gasta considerando seu nível de atividade física. 
            Para perda de peso, consuma 300-500 kcal a menos; para ganho de massa muscular, consuma 300-500 kcal a mais.
        </div>
        
        <!-- MEDIDAS DETALHADAS -->
        <h2>📏 MEDIDAS DETALHADAS</h2>
        <h3>Dobras Cutâneas (mm)</h3>
        <div class="grid-3">{dobras_html}</div>
        
        <h3>Circunferências (cm)</h3>
        <div class="grid-3">{circunferencias_html}</div>
        
        <!-- GRÁFICOS -->
        <h2>📊 GRÁFICOS DA AVALIAÇÃO</h2>
        <div class="graficos-container">
            <img src="data:image/png;base64,{grafico_composicao_b64}" alt="Composição Corporal">
            <div class="explicacao">
                <strong>📌 Análise da Composição Corporal:</strong> Seu corpo é composto por {percentual_gordura_jp:.1f}% de gordura e {100-percentual_gordura_jp:.1f}% de massa magra. 
                A massa magra inclui músculos, ossos e órgãos. Quanto maior a massa magra, maior seu metabolismo basal.
            </div>
            
            <img src="data:image/png;base64,{grafico_comparativo_b64}" alt="Comparativo com Referências">
            <div class="explicacao">
                <strong>📌 Comparação com Referências:</strong> O gráfico acima compara seu percentual de gordura com as referências científicas.
                {f'Seu valor ({percentual_gordura_jp:.1f}%) está na faixa "{classif_gordura}"' if classif_gordura else ''}.
                A faixa saudável recomendada pelo ACSM é de 14-17% para homens e 21-24% para mulheres.
            </div>
            
            <img src="data:image/png;base64,{grafico_idade_b64}" alt="Percentual por Idade">
            <div class="explicacao">
                <strong>📌 Tendência por Idade:</strong> O percentual de gordura tende a aumentar naturalmente com o envelhecimento. 
                A linha laranja mostra a média esperada para a população brasileira segundo o ACSM.
                {f'Seu valor está abaixo da média para sua idade, o que é positivo!' if percentual_gordura_jp < percentuais_referencia[min(len(percentuais_referencia)-1, max(0, int((idade-20)/5)))] else 'Seu valor está acima da média para sua idade, indicando necessidade de atenção.'}
            </div>
        </div>
        
        <div class="footer">
            <strong>BioGestão 360</strong> | Jackson & Pollock (1980) | Siri (1961) | ACSM<br>
            🔒 Zero-Footprint | 📊 Estimativa | 👨‍⚕️ Consulte um profissional
        </div>
    </div>
</body>
</html>"""

    b64_avaliacao = base64.b64encode(html_avaliacao.encode()).decode()
    st.markdown(
        f"""
        <a href="data:text/html;base64,{b64_avaliacao}" download="laudo_avaliacao_fisica_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html" 
           style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 10px 20px; 
           text-decoration: none; border-radius: 8px; display: inline-block; width: 100%; text-align: center; 
           font-weight: bold; font-size: 14px;">
           📄 Baixar PDF
        </a>
    """,
        unsafe_allow_html=True,
    )
    st.caption("💡 Abra o arquivo HTML → Ctrl+P → Salvar como PDF")

st.markdown(
    "*Este laudo é uma estimativa baseada nas medidas inseridas. Para maior precisão, consulte um profissional de Educação Física ou Nutrição qualificado.*"
)

# ============================================
# 26. MONTAGEM DO PLANO ALIMENTAR (MANTIDO)
# ============================================
st.markdown("## 🍏 Montagem do Plano Alimentar")

st.markdown(
    """
<div class='aviso-peso-real'>
    <div style='display: flex; align-items: center; gap: 15px; flex-wrap: wrap;'>
        <span style='font-size: 40px;'>⚠️</span>
        <div style='flex: 1;'>
            <h3>📌 REGRA DE OURO PARA PRECISÃO!</h3>
            <p>Para alimentos em <strong>"unidades"</strong> (biscoitos, frutas, ovos, pães, etc.), 
            <strong>sempre informe o peso real de UMA unidade</strong> no campo <strong>"Peso Real (g/ml)"</strong>.</p>
        </div>
    </div>
    <hr>
    <div class='grid-referencia'>
        <div class='card-peso'><strong>🍪 Biscoito maisena</strong><br><span>1 unidade = 5g → informe 5g</span></div>
        <div class='card-peso'><strong>🍞 Pão francês</strong><br><span>1 unidade = 50g → informe 50g</span></div>
        <div class='card-peso'><strong>🍎 Maçã</strong><br><span>1 unidade = 150g → informe 150g</span></div>
        <div class='card-peso'><strong>🥚 Ovo</strong><br><span>1 unidade = 50g → informe 50g</span></div>
        <div class='card-peso'><strong>🍌 Banana</strong><br><span>1 unidade = 100g → informe 100g</span></div>
        <div class='card-peso'><strong>🍊 Laranja</strong><br><span>1 unidade = 120g → informe 120g</span></div>
    </div>
    <div class='obs'>💡 <strong>Não sabe o peso?</strong> Use a tabela de referência acima ou consulte a embalagem do produto.</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class='instrucao-cientifica'>
    <h4>📋 Para seguir sua receita da nutri:</h4>
    <ol>
        <li>🔍 Identifique os alimentos da sua receita na tabela <strong>{st.session_state.fonte_dados}</strong> (busque pelo nome)</li>
        <li>➕ Adicione um a um nos campos abaixo com as quantidades prescritas</li>
        <li>⚡ O sistema calcula automaticamente calorias e nutrientes com base em dados científicos</li>
        <li>📊 Use o resumo para impressão e acompanhamento</li>
    </ol>
    <p>⚠️ <strong>Atenção:</strong> Alguns alimentos podem ter dados incompletos (valores NA, *, Tr). Nesses casos, o sistema considera 0 (zero).</p>
    <p>🔗 <strong>Fontes científicas:</strong> TACO/UNICAMP | IBGE | FAO/WHO</p>
</div>
""",
    unsafe_allow_html=True,
)

# ========== SELECIONAR A TABELA CORRETA ==========
if st.session_state.fonte_dados == "TACO (UNICAMP)":
    df_atual = df_taco
    if not df_atual.empty and "Descrição dos alimentos" in df_atual.columns:
        campo_busca = "Descrição dos alimentos"
    else:
        campo_busca = None
else:
    df_atual = df_ibge
    if not df_atual.empty:
        if "descricao_completa" in df_atual.columns:
            campo_busca = "descricao_completa"
        elif "descricao" in df_atual.columns:
            campo_busca = "descricao"
        else:
            campo_busca = None
    else:
        campo_busca = None

if df_atual.empty or campo_busca is None:
    st.error(f"⚠️ Tabela {st.session_state.fonte_dados} não encontrada ou vazia.")
    st.stop()

lista_alimentos = df_atual[campo_busca].dropna().unique().tolist()
lista_alimentos.sort()

if not st.session_state.modo_impressao:
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1.5, 3, 1, 1, 1])
        with col1:
            refeicao_sel = st.selectbox(
                "Refeição", ["Café da Manhã", "Almoço", "Lanches", "Jantar"]
            )
        with col2:
            alimento_sel = st.selectbox("Alimento", lista_alimentos)
        with col3:
            qtd_unidade = st.number_input("Quantidade", 0.0, 50.0, 1.0, step=0.5)
        with col4:
            peso_real = st.number_input(
                "Peso Real (g/ml)",
                0.0,
                2000.0,
                0.0,
                step=1.0,
                help="Informe o peso de UMA unidade",
            )
        with col5:
            unidade_tipo = st.selectbox("Unidade", ["g", "ml", "un"])

    if st.button("➕ Adicionar ao Plano", use_container_width=True):
        item = df_atual[df_atual[campo_busca] == alimento_sel].iloc[0]

        if peso_real > 0:
            peso_final = peso_real * qtd_unidade
            label_qtd = f"{qtd_unidade:g} un ({peso_final:.0f} {'ml' if unidade_tipo == 'ml' else 'g'})"
        else:
            if unidade_tipo == "un":
                peso_por_unidade = obter_peso_por_unidade(alimento_sel)
                if peso_por_unidade > 0:
                    peso_final = peso_por_unidade * qtd_unidade
                    label_qtd = f"{qtd_unidade:g} un (~{peso_final:.0f} g)"
                else:
                    st.warning(
                        f"⚠️ Sem estimativa para '{alimento_sel}'. Informe o Peso Real!"
                    )
                    peso_final = 0
                    label_qtd = f"{qtd_unidade:g} un (peso não informado)"
            elif unidade_tipo == "ml":
                peso_final = 200 * qtd_unidade
                label_qtd = f"{qtd_unidade:g} un (~{peso_final:.0f} ml)"
            else:
                peso_final = qtd_unidade
                label_qtd = f"{qtd_unidade:g} g"

        fator_calc = peso_final / 100 if peso_final > 0 else 0
        risco_oms = verificar_risco_oms(alimento_sel)

        if st.session_state.fonte_dados == "TACO (UNICAMP)":
            valores = obter_valor_nutricional_taco(item, fator_calc)
        else:
            valores = obter_valor_nutricional_ibge(item, fator_calc)

        novo_item = {
            "Ali": alimento_sel,
            "Qtd": label_qtd,
            "Kcal": valores["kcal"],
            "P": valores["prot"],
            "C": valores["carb"],
            "G": valores["gord"],
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

# ============================================
# 27. EXIBIÇÃO DO PLANO
# ============================================
if st.session_state.planejamento_tipo == "Diário":
    st.markdown("### 📋 Seu Cardápio de Hoje")
    for refeicao in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]:
        itens = st.session_state.cardapio.get(refeicao, [])
        if itens:
            header_class = {
                "Café da Manhã": "header-cafe",
                "Almoço": "header-almoco",
                "Lanches": "header-lanches",
                "Jantar": "header-jantar",
            }[refeicao]
            st.markdown(
                f"<div class='{header_class}'>{refeicao.upper()}</div>",
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
                    if st.button("🗑️", key=f"del_{refeicao}_{idx}"):
                        remover_item_diario(refeicao, idx)
                if item.get("Risco"):
                    st.markdown(
                        f"<div class='alerta-oms-grupo1'>{item['Risco']}</div>",
                        unsafe_allow_html=True,
                    )
                st.divider()
else:
    # Título com o dia da semana
    st.markdown(f"### 📅 Planejamento Semanal: **{st.session_state.dia_atual}**")

    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    cols_dias = st.columns(7)

    for i, dia in enumerate(dias_semana):
        with cols_dias[i]:
            # Usar o próprio botão do Streamlit, sem CSS complicado
            # Apenas muda a cor de fundo quando selecionado via markdown
            if st.session_state.dia_atual == dia:
                # Botão com cor laranja (selecionado)
                st.markdown(
                    f"""
                <div style="
                    background: linear-gradient(135deg, #f59e0b, #ef4444);
                    border: 1px solid #ffd700;
                    color: white;
                    text-align: center;
                    padding: 8px 0;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 14px;
                ">
                    {dia}
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                # Botão normal (clicável)
                if st.button(dia, key=f"dia_{dia}", use_container_width=True):
                    st.session_state.dia_atual = dia
                    st.rerun()

    st.markdown("---")

    for refeicao in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]:
        itens = st.session_state.cardapio_semanal.get(
            st.session_state.dia_atual, {}
        ).get(refeicao, [])
        if itens:
            header_class = {
                "Café da Manhã": "header-cafe",
                "Almoço": "header-almoco",
                "Lanches": "header-lanches",
                "Jantar": "header-jantar",
            }[refeicao]
            st.markdown(
                f"<div class='{header_class}'>{refeicao.upper()}</div>",
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

# ============================================
# 28. CÁLCULO DOS TOTAIS (MANTIDO)
# ============================================
if dados_validos:
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
    saldo_diario = get_atual - media_diaria
    variacao_semanal = abs((saldo_diario * 7) / 7700) if saldo_diario != 0 else 0
    variacao_30dias = abs((saldo_diario * 30) / 7700) if saldo_diario != 0 else 0
else:
    total_kcal = 0
    total_prot = 0
    total_carb = 0
    total_gord = 0
    media_diaria = 0
    saldo_diario = 0
    variacao_semanal = 0
    variacao_30dias = 0

# ============================================
# 29. GRÁFICOS (MANTIDO)
# ============================================
if total_kcal > 0 and dados_validos:
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
                "Valor (kcal)": [get_atual, media_diaria, abs(saldo_diario)],
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
    st.markdown("---")

# ============================================
# 30. LAUDO TÉCNICO COMPLETO (MANTIDO)
# ============================================
st.markdown("## 📋 LAUDO TÉCNICO DE VIABILIDADE ALIMENTAR")

if dados_validos:
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
        st.metric("⚡ Gasto Estimado (GET)", f"{get_atual:.0f} kcal")
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
                    f"🎯 **DÉFICIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a menos por dia."
                )
            elif saldo_diario < 0:
                st.warning(
                    f"⚠️ **SUPERÁVIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a mais por dia."
                )
            else:
                st.info(
                    "✅ **Manutenção!** Você está consumindo exatamente o que gasta."
                )
        else:
            if saldo_diario < 0:
                st.success(
                    f"🎯 **SUPERÁVIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a mais por dia."
                )
            elif saldo_diario > 0:
                st.warning(
                    f"⚠️ **DÉFICIT calórico!**\n\nConsumindo {abs(saldo_diario):.1f} kcal a menos por dia."
                )
            else:
                st.info(
                    "✅ **Manutenção!** Você está consumindo exatamente o que gasta."
                )

    with col_result2:
        st.markdown(
            f"""
        📉 **Projeção em 7 dias:** {variacao_semanal:.2f} kg
        
        📉 **Projeção em 30 dias:** {variacao_30dias:.2f} kg
        
        ---
        ℹ️ **Sobre a projeção de 7 dias:**
        Esta é uma **estimativa teórica** baseada no déficit calórico médio.
        
        Variações diárias de peso são normais devido a:
        • 💧 Retenção hídrica (pode variar 1-2kg)
        • ⏰ Horário da pesagem
        • 🍽️ Conteúdo intestinal
        
        O resultado real pode diferir. O mais importante é a **consistência** e a **tendência de longo prazo**.
        """
        )

    with col_result3:
        if saldo_diario != 0 and p_alvo > 0 and diferenca_meta != 0:
            if objetivo == "Perda de peso" and saldo_diario > 0:
                semanas_meta = (
                    abs(diferenca_meta) / (variacao_30dias / 4.3)
                    if variacao_30dias > 0
                    else 0
                )
                if semanas_meta > 0:
                    st.success(
                        f"⏱️ **Tempo estimado:** {max(1, int(semanas_meta))} semanas"
                    )
                    st.caption("⏱️ Baseado na projeção de 30 dias")
                else:
                    st.info("📝 Adicione alimentos para calcular o tempo")
            elif objetivo == "Ganho de peso" and saldo_diario < 0:
                semanas_meta = (
                    abs(diferenca_meta) / (variacao_30dias / 4.3)
                    if variacao_30dias > 0
                    else 0
                )
                if semanas_meta > 0:
                    st.success(
                        f"⏱️ **Tempo estimado:** {max(1, int(semanas_meta))} semanas"
                    )
                    st.caption("⏱️ Baseado na projeção de 30 dias")
                else:
                    st.info("📝 Adicione alimentos para calcular o tempo")
            else:
                st.warning("⚡ **Ajuste seu consumo para atingir a meta!**")
        elif p_alvo == 0:
            st.info("📝 Defina sua meta de peso para ver o tempo estimado")
        elif saldo_diario == 0:
            st.info("✅ **Manutenção!** Você está consumindo exatamente o que gasta.")
        else:
            st.info("📝 Adicione alimentos ao cardápio para calcular o tempo estimado")

else:
    st.info("📝 Preencha seus dados na barra lateral para gerar o laudo técnico.")

# ============================================
# 31. RESUMO COMPLETO PARA IMPRESSÃO
# ============================================
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

# ============================================
# 32. EXPORTAÇÃO LAUDO TÉCNICO (CSV + PDF COM GRÁFICOS)
# ============================================
st.markdown("---")
st.markdown("### 📥 Exportar Laudo Técnico")

if dados_validos:
    # Classificação IMC para o laudo
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

    if saldo_diario > 0:
        status_saldo = "Déficit (perda de peso)"
    elif saldo_diario < 0:
        status_saldo = "Superávit (ganho de peso)"
    else:
        status_saldo = "Manutenção"

    if objetivo == "Perda de peso":
        if p_alvo > 0:
            if p_alvo < peso_at:
                mensagem_meta = f"Faltam {peso_at - p_alvo:.1f} kg para atingir sua meta de {p_alvo:.1f} kg"
            else:
                mensagem_meta = f"Meta de {p_alvo:.1f} kg está acima do peso atual. Ajuste para perda de peso."
        else:
            mensagem_meta = "Defina sua meta de peso para acompanhamento"
    else:
        if p_alvo > 0:
            if p_alvo > peso_at:
                mensagem_meta = f"Faltam {p_alvo - peso_at:.1f} kg para atingir sua meta de {p_alvo:.1f} kg"
            else:
                mensagem_meta = f"Meta de {p_alvo:.1f} kg está abaixo do peso atual. Ajuste para ganho de peso."
        else:
            mensagem_meta = "Defina sua meta de peso para acompanhamento"

    # Calcular percentuais baseados no total_kcal
    if total_kcal > 0 and not pd.isna(total_kcal) and total_kcal is not None:
        perc_prot = (total_prot * 4 / total_kcal) * 100 if total_prot > 0 else 0
        perc_carb = (total_carb * 4 / total_kcal) * 100 if total_carb > 0 else 0
        perc_gord = (total_gord * 9 / total_kcal) * 100 if total_gord > 0 else 0
    else:
        perc_prot = perc_carb = perc_gord = 0

    perc_prot = (
        0 if (pd.isna(perc_prot) or perc_prot is None or perc_prot < 0) else perc_prot
    )
    perc_carb = (
        0 if (pd.isna(perc_carb) or perc_carb is None or perc_carb < 0) else perc_carb
    )
    perc_gord = (
        0 if (pd.isna(perc_gord) or perc_gord is None or perc_gord < 0) else perc_gord
    )

    if saldo_diario != 0 and p_alvo > 0 and diferenca_meta != 0:
        if objetivo == "Perda de peso" and saldo_diario > 0:
            semanas_meta = (
                abs(diferenca_meta) / (variacao_30dias / 4.3)
                if variacao_30dias > 0
                else 0
            )
            if semanas_meta > 0:
                tempo_meta = f"{max(1, int(semanas_meta))} semanas"
            else:
                tempo_meta = "Adicione alimentos para calcular"
        elif objetivo == "Ganho de peso" and saldo_diario < 0:
            semanas_meta = (
                abs(diferenca_meta) / (variacao_30dias / 4.3)
                if variacao_30dias > 0
                else 0
            )
            if semanas_meta > 0:
                tempo_meta = f"{max(1, int(semanas_meta))} semanas"
            else:
                tempo_meta = "Adicione alimentos para calcular"
        else:
            tempo_meta = "Ajuste seu consumo para atingir a meta"
    elif p_alvo == 0:
        tempo_meta = "Defina sua meta de peso"
    elif saldo_diario == 0:
        tempo_meta = "Manutenção - consumo igual ao gasto"
    else:
        tempo_meta = "Adicione alimentos ao cardápio"

    # DADOS DA CONSULTA para incluir no CSV
    dados_consulta_csv = [
        {"Categoria": "📋 DADOS DA CONSULTA", "Valor": ""},
        {
            "Categoria": "Paciente",
            "Valor": st.session_state.dados_paciente.get("nome", "-"),
        },
        {
            "Categoria": "Telefone",
            "Valor": st.session_state.dados_paciente.get("telefone", "-"),
        },
        {
            "Categoria": "Profissional",
            "Valor": st.session_state.dados_profissional.get("nome", "-"),
        },
        {
            "Categoria": "Registro",
            "Valor": st.session_state.dados_profissional.get("registro", "-"),
        },
        {
            "Categoria": "Clínica",
            "Valor": st.session_state.dados_consulta.get("clinica", "-"),
        },
        {
            "Categoria": "Data Início",
            "Valor": st.session_state.dados_consulta.get("data_inicio", "-"),
        },
        {
            "Categoria": "Data Retorno",
            "Valor": st.session_state.dados_consulta.get("data_retorno", "-"),
        },
        {
            "Categoria": "Observações",
            "Valor": (
                st.session_state.dados_consulta.get("observacoes", "-")
                if st.session_state.dados_consulta.get("observacoes")
                else "-"
            ),
        },
        {"Categoria": "", "Valor": ""},
    ]

    dados_laudo = {
        "Categoria": [
            "📋 DATA DO RELATÓRIO",
            "📋 TIPO DE PLANEJAMENTO",
            "📋 PERÍODO ANALISADO",
            "",
            "👤 PERFIL DO AVALIADO",
            "Peso Atual (kg)",
            "Altura (cm)",
            "Idade (anos)",
            "Sexo",
            "Objetivo",
            "Meta de Peso (kg)",
            "Status da Meta",
            "Frequência de Atividade Física",
            "",
            "⚡ METABOLISMO E GASTO ENERGÉTICO",
            "Gasto Total (GET) - kcal/dia",
            "Metabolismo Basal (TMB) - kcal/dia",
            "Índice de Massa Corporal (IMC)",
            "Classificação IMC",
            "Peso Ideal Estimado (kg)",
            "Percentual de Gordura (Estimativa IMC)",
            "Massa de Gordura (kg)",
            "Massa Magra (kg)",
            "Método de Cálculo do GET",
            "",
            "🍽️ CONSUMO DO PERÍODO",
            "Consumo Total (kcal)",
            "Média Diária (kcal)",
            "Saldo Energético Diário (kcal)",
            "Status do Saldo",
            "",
            "🥩 MACRONUTRIENTES",
            "Proteínas (g)",
            "% Proteínas",
            "Carboidratos (g)",
            "% Carboidratos",
            "Gorduras (g)",
            "% Gorduras",
            "",
            "📊 PROJEÇÕES",
            "Projeção de Variação em 7 dias (kg)",
            "Projeção de Variação em 30 dias (kg)",
            "Tempo Estimado para Meta",
            "Mensagem do Saldo",
            "",
            "⚠️ AVISO CIENTÍFICO",
        ],
        "Valor": [
            pd.Timestamp.now().strftime("%d/%m/%Y %H:%M"),
            st.session_state.planejamento_tipo,
            (
                "Hoje (1 dia)"
                if st.session_state.planejamento_tipo == "Diário"
                else "Semana completa (7 dias)"
            ),
            "",
            "",
            f"{peso_at:.1f} kg",
            f"{alt_cm} cm",
            f"{idade} anos",
            sexo,
            objetivo,
            f"{p_alvo:.1f} kg" if p_alvo > 0 else "Não definida",
            mensagem_meta,
            naf_label,
            "",
            "",
            f"{get_atual:.0f} kcal",
            f"{tmb_atual:.0f} kcal",
            f"{composicao['imc']}",
            classificacao_imc,
            f"{composicao['peso_ideal']:.1f} kg",
            f"{composicao['percentual_gordura']:.1f}%",
            f"{composicao['massa_gordura']:.1f} kg",
            f"{composicao['massa_magra']:.1f} kg",
            metodo_atual_nome,
            "",
            "",
            f"{total_kcal:.1f} kcal",
            f"{media_diaria:.1f} kcal",
            f"{abs(saldo_diario):.1f} kcal",
            status_saldo,
            "",
            "",
            f"{total_prot:.1f} g",
            f"{perc_prot:.1f}%",
            f"{total_carb:.1f} g",
            f"{perc_carb:.1f}%",
            f"{total_gord:.1f} g",
            f"{perc_gord:.1f}%",
            "",
            "",
            f"{variacao_semanal:.2f} kg",
            f"{variacao_30dias:.2f} kg",
            tempo_meta,
            f"{'Déficit calórico' if saldo_diario > 0 else 'Superávit calórico' if saldo_diario < 0 else 'Manutenção'} - Consumindo {abs(saldo_diario):.1f} kcal {'a menos' if saldo_diario > 0 else 'a mais'} por dia",
            "",
            "⚠️ ATENÇÃO: Projeção de 7 dias é uma estimativa teórica. Variações diárias de peso são normais (retenção hídrica 1-2kg, horário da pesagem, conteúdo intestinal). O resultado real pode diferir. A consistência e a tendência de 30 dias são mais confiáveis.",
        ],
    }

    df_consulta = pd.DataFrame(dados_consulta_csv)
    df_laudo = pd.DataFrame(dados_laudo)
    df_final = pd.concat([df_consulta, df_laudo], ignore_index=True)

    # Adicionar separador e tipo de cardápio
    df_separador = pd.DataFrame([{"Categoria": "", "Valor": ""}])
    df_tipo_cardapio = pd.DataFrame(
        [
            {
                "Categoria": "📅 TIPO DE CARDÁPIO",
                "Valor": st.session_state.planejamento_tipo,
            }
        ]
    )
    df_separador2 = pd.DataFrame([{"Categoria": "", "Valor": ""}])
    df_separador3 = pd.DataFrame([{"Categoria": "🍽️ CARDÁPIO DETALHADO", "Valor": ""}])
    df_separador4 = pd.DataFrame([{"Categoria": "", "Valor": ""}])

    df_final = pd.concat(
        [
            df_final,
            df_separador,
            df_tipo_cardapio,
            df_separador2,
            df_separador3,
            df_separador4,
        ],
        ignore_index=True,
    )

    # CORREÇÃO: Coletar alimentos conforme o tipo de planejamento
    todos_alimentos_csv = []

    if st.session_state.planejamento_tipo == "Diário":
        # Estrutura para DIÁRIO
        for refeicao in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]:
            itens = st.session_state.cardapio.get(refeicao, [])
            if itens:
                todos_alimentos_csv.append(
                    {"Categoria": f"--- {refeicao.upper()} ---", "Valor": ""}
                )
                for item in itens:
                    todos_alimentos_csv.append(
                        {
                            "Categoria": f"  • {item['Ali']}",
                            "Valor": f"{item['Qtd']} | {item['Kcal']} kcal | P:{item['P']}g C:{item['C']}g G:{item['G']}g",
                        }
                    )
                todos_alimentos_csv.append({"Categoria": "", "Valor": ""})
    else:
        # Estrutura para SEMANAL
        for dia in [
            "Segunda",
            "Terça",
            "Quarta",
            "Quinta",
            "Sexta",
            "Sábado",
            "Domingo",
        ]:
            tem_itens_no_dia = False
            for refeicao in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]:
                itens = st.session_state.cardapio_semanal.get(dia, {}).get(refeicao, [])
                if itens:
                    if not tem_itens_no_dia:
                        todos_alimentos_csv.append(
                            {"Categoria": f"📆 {dia.upper()}", "Valor": ""}
                        )
                        tem_itens_no_dia = True
                    todos_alimentos_csv.append(
                        {"Categoria": f"    🍽️ {refeicao}", "Valor": ""}
                    )
                    for item in itens:
                        todos_alimentos_csv.append(
                            {
                                "Categoria": f"        • {item['Ali']}",
                                "Valor": f"{item['Qtd']} | {item['Kcal']} kcal | P:{item['P']}g C:{item['C']}g G:{item['G']}g",
                            }
                        )
            if tem_itens_no_dia:
                todos_alimentos_csv.append({"Categoria": "", "Valor": ""})

    if todos_alimentos_csv:
        df_alimentos = pd.DataFrame(todos_alimentos_csv)
        df_final = pd.concat([df_final, df_alimentos], ignore_index=True)
    else:
        df_final = pd.concat(
            [
                df_final,
                pd.DataFrame(
                    [
                        {
                            "Categoria": "ℹ️ NENHUM ALIMENTO ADICIONADO",
                            "Valor": "Adicione alimentos ao cardápio",
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

    csv_laudo = df_final.to_csv(index=False, encoding="utf-8-sig", sep=";")

    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.download_button(
            "📊 Baixar Laudo Técnico Completo (CSV)",
            data=csv_laudo,
            file_name=f"laudo_biogestao_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.caption(
            "📌 CSV organizado: Dados da Consulta | Perfil | Metabolismo | Consumo | Macronutrientes | Projeções | Tipo de Cardápio | Alimentos"
        )

    with col_exp2:
        # ============================================
        # GERAR HTML PARA PDF - COM QUEBRAS DE PÁGINA
        # ============================================

        import matplotlib.pyplot as plt
        import io

        # Valores seguros
        comp_gordura_val = (
            composicao["percentual_gordura"]
            if composicao and composicao["percentual_gordura"] > 0
            else 50
        )
        comp_magra_val = 100 - comp_gordura_val

        prot_cal = total_prot * 4 if total_prot > 0 else 0
        carb_cal = total_carb * 4 if total_carb > 0 else 0
        gord_cal = total_gord * 9 if total_gord > 0 else 0

        if prot_cal == 0 and carb_cal == 0 and gord_cal == 0:
            prot_cal, carb_cal, gord_cal = 100, 100, 100

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        axes[0].pie(
            [comp_gordura_val, comp_magra_val],
            labels=["Massa Gorda", "Massa Magra"],
            colors=["#ef4444", "#3b82f6"],
            autopct="%1.1f%%",
            startangle=90,
        )
        axes[0].set_title("Composição Corporal", fontsize=12, fontweight="bold")

        get_val = get_atual if get_atual > 0 else 2000
        consumo_val = media_diaria if media_diaria > 0 else 2000
        diferenca_val = abs(saldo_diario) if abs(saldo_diario) > 0 else 500

        bars = axes[1].bar(
            ["GET", "Consumo", "Diferença"],
            [get_val, consumo_val, diferenca_val],
            color=["#ef4444", "#10b981", "#f59e0b"],
        )
        axes[1].set_title(
            "Balanço Energético (kcal/dia)", fontsize=12, fontweight="bold"
        )
        axes[1].set_ylabel("kcal")
        for bar, val in zip(bars, [get_val, consumo_val, diferenca_val]):
            axes[1].text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 10,
                f"{val:.0f}",
                ha="center",
                fontsize=9,
            )

        axes[2].pie(
            [prot_cal, carb_cal, gord_cal],
            labels=["Proteínas", "Carboidratos", "Gorduras"],
            colors=["#ef4444", "#3b82f6", "#f59e0b"],
            autopct="%1.1f%%",
            startangle=90,
        )
        axes[2].set_title(
            "Distribuição dos Macronutrientes", fontsize=12, fontweight="bold"
        )

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=200, bbox_inches="tight", facecolor="white")
        buf.seek(0)
        graficos_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close()

        data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")

        if saldo_diario > 0:
            saldo_texto_pdf = "🎯 DÉFICIT calórico!"
            saldo_desc_pdf = f"Consumindo {abs(saldo_diario):.1f} kcal a menos por dia."
        elif saldo_diario < 0:
            saldo_texto_pdf = "🎯 SUPERÁVIT calórico!"
            saldo_desc_pdf = f"Consumindo {abs(saldo_diario):.1f} kcal a mais por dia."
        else:
            saldo_texto_pdf = "🎯 Manutenção!"
            saldo_desc_pdf = "Você está consumindo exatamente o que gasta."

        observacoes_texto = st.session_state.dados_consulta.get("observacoes", "")
        if not observacoes_texto:
            observacoes_texto = "Nenhuma observação registrada"

        # Construir tabela do cardápio
        tabela_cardapio_html = ""
        if st.session_state.planejamento_tipo == "Diário":
            for refeicao, itens in st.session_state.cardapio.items():
                for item in itens:
                    tabela_cardapio_html += f"<tr><td>Hoje</td><td>{refeicao}</td><td>{item['Ali']}</td><td>{item['Qtd']}</td><td>{item['Kcal']}</td><td>{item['P']}</td><td>{item['C']}</td><td>{item['G']}</td></tr>"
        else:
            for dia in [
                "Segunda",
                "Terça",
                "Quarta",
                "Quinta",
                "Sexta",
                "Sábado",
                "Domingo",
            ]:
                for refeicao in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]:
                    for item in st.session_state.cardapio_semanal.get(dia, {}).get(
                        refeicao, []
                    ):
                        tabela_cardapio_html += f"<tr><td>{dia}</td><td>{refeicao}</td><td>{item['Ali']}</td><td>{item['Qtd']}</td><td>{item['Kcal']}</td><td>{item['P']}</td><td>{item['C']}</td><td>{item['G']}</td></tr>"

        if not tabela_cardapio_html:
            tabela_cardapio_html = "<tr><td colspan='8' style='text-align: center'>Nenhum alimento adicionado ao cardápio</td></tr>"

        html_pdf = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Laudo BioGestão 360</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: white;
            color: #1e293b;
            padding: 15px;
            font-size: 11pt;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #f59e0b; font-size: 20pt; text-align: center; border-bottom: 2px solid #f59e0b; padding-bottom: 8px; }}
        h2 {{ background: linear-gradient(135deg, #1e3a5f, #0f172a); color: white; padding: 6px 10px; margin: 20px 0 12px 0; font-size: 14pt; border-radius: 6px; }}
        .subheader {{ text-align: center; color: #64748b; font-size: 9pt; margin-top: 5px; }}
        .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 10px 0; }}
        .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 10px 0; }}
        .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 10px 0; }}
        .card {{ border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; background: #f8fafc; }}
        .card-title {{ font-size: 9pt; color: #64748b; }}
        .card-value {{ font-size: 13pt; font-weight: bold; color: #1e293b; }}
        .metric-card {{ text-align: center; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; background: #f8fafc; }}
        .metric-icon {{ font-size: 22pt; }}
        .metric-value {{ font-size: 16pt; font-weight: bold; color: #f59e0b; }}
        .metric-label {{ font-size: 9pt; color: #64748b; }}
        .metric-desc {{ font-size: 7pt; color: #94a3b8; margin-top: 5px; }}
        .success-box {{ background: #dcfce7; border-left: 4px solid #10b981; padding: 10px; border-radius: 8px; margin: 12px 0; }}
        .warning-box {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 10px; border-radius: 8px; margin: 12px 0; font-size: 9pt; }}
        table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 8pt; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 5px 6px; text-align: left; }}
        th {{ background: #f59e0b; color: white; }}
        tr:nth-child(even) {{ background: #f8fafc; }}
        .graficos-container {{ text-align: center; margin: 15px 0; }}
        .graficos-container img {{ max-width: 100%; height: auto; border: 1px solid #e2e8f0; border-radius: 12px; }}
        .footer {{ text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #e2e8f0; font-size: 8pt; color: #94a3b8; }}
        .page-break {{ page-break-before: always; }}
        @media print {{
            body {{ padding: 0; margin: 0; }}
            h2 {{ background: #333 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            th {{ background: #666 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .page-break {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- PÁGINA 1: DADOS DA CONSULTA + PERFIL + METABOLISMO -->
        <h1>🏋️ BioGestão 360 - Laudo Técnico Completo</h1>
        <div class="subheader">Gerado em {data_atual}</div>
        
        <h2>📋 DADOS DA CONSULTA</h2>
        <div class="grid-2">
            <div class="card"><div class="card-title">👤 Paciente</div><div class="card-value">{st.session_state.dados_paciente.get('nome', '-')}</div></div>
            <div class="card"><div class="card-title">📞 Telefone</div><div class="card-value">{st.session_state.dados_paciente.get('telefone', '-')}</div></div>
            <div class="card"><div class="card-title">👨‍⚕️ Profissional</div><div class="card-value">{st.session_state.dados_profissional.get('nome', '-')}</div></div>
            <div class="card"><div class="card-title">📜 Registro</div><div class="card-value">{st.session_state.dados_profissional.get('registro', '-')}</div></div>
            <div class="card"><div class="card-title">🏥 Clínica</div><div class="card-value">{st.session_state.dados_consulta.get('clinica', '-')}</div></div>
            <div class="card"><div class="card-title">📅 Data Início</div><div class="card-value">{st.session_state.dados_consulta.get('data_inicio', '-')}</div></div>
            <div class="card"><div class="card-title">🔄 Data Retorno</div><div class="card-value">{st.session_state.dados_consulta.get('data_retorno', '-')}</div></div>
            <div class="card"><div class="card-title">📝 Observações</div><div class="card-value">{observacoes_texto}</div></div>
        </div>
        
        <h2>👤 PERFIL BIOLÓGICO</h2>
        <div class="grid-3">
            <div class="metric-card"><div class="metric-icon">⚖️</div><div class="metric-value">{peso_at:.1f} kg</div><div class="metric-label">Peso</div></div>
            <div class="metric-card"><div class="metric-icon">📏</div><div class="metric-value">{alt_cm} cm</div><div class="metric-label">Altura</div></div>
            <div class="metric-card"><div class="metric-icon">🎂</div><div class="metric-value">{idade} anos</div><div class="metric-label">Idade</div></div>
            <div class="metric-card"><div class="metric-icon">⚥</div><div class="metric-value">{sexo}</div><div class="metric-label">Sexo</div></div>
            <div class="metric-card"><div class="metric-icon">🎯</div><div class="metric-value">{objetivo}</div><div class="metric-label">Objetivo</div></div>
            <div class="metric-card"><div class="metric-icon">🏆</div><div class="metric-value">{p_alvo:.1f} kg</div><div class="metric-label">Meta de Peso</div></div>
        </div>
        
        <h2>⚡ Metabolismo e Gasto Energético</h2>
        <div class="grid-4">
            <div class="metric-card"><div class="metric-icon">⚡</div><div class="metric-value">{get_atual:.0f} kcal</div><div class="metric-label">Gasto Total (GET)</div><div class="metric-desc">Total de calorias que seu corpo gasta por dia.</div></div>
            <div class="metric-card"><div class="metric-icon">🔥</div><div class="metric-value">{tmb_atual:.0f} kcal</div><div class="metric-label">Metabolismo Basal (TMB)</div><div class="metric-desc">Calorias queimadas em repouso total.</div></div>
            <div class="metric-card"><div class="metric-icon">📊</div><div class="metric-value">{composicao['imc']}</div><div class="metric-label">Índice de Massa Corporal (IMC)</div><div class="metric-desc">{classificacao_imc}</div></div>
            <div class="metric-card"><div class="metric-icon">🎯</div><div class="metric-value">{composicao['peso_ideal']} kg</div><div class="metric-label">Peso Ideal Estimado</div></div>
        </div>
        
        <!-- QUEBRA DE PÁGINA: Composição Corporal começa na página 2 -->
        <div class="page-break"></div>
        
        <!-- PÁGINA 2: COMPOSIÇÃO CORPORAL + GRÁFICOS + ESTIMATIVA -->
        <h2>🧬 Composição Corporal</h2>
        <div class="grid-3">
            <div class="metric-card"><div class="metric-icon">🎯</div><div class="metric-value">{composicao['percentual_gordura']:.1f}%</div><div class="metric-label">Percentual de Gordura</div><div class="metric-desc">Homens: 10-25% | Mulheres: 18-32%</div></div>
            <div class="metric-card"><div class="metric-icon">⚖️</div><div class="metric-value">{composicao['massa_gordura']:.1f} kg</div><div class="metric-label">Massa de Gordura</div></div>
            <div class="metric-card"><div class="metric-icon">💪</div><div class="metric-value">{composicao['massa_magra']:.1f} kg</div><div class="metric-label">Massa Magra</div></div>
        </div>
        
        <div class="graficos-container">
            <img src="data:image/png;base64,{graficos_b64}" alt="Gráficos do Laudo">
        </div>
        
        <h2>📊 ESTIMATIVA DE RESULTADOS</h2>
        <div class="success-box">
            <strong>{saldo_texto_pdf}</strong><br>{saldo_desc_pdf}
        </div>
        <div class="grid-3">
            <div class="metric-card"><div class="metric-value">{variacao_semanal:.2f} kg</div><div class="metric-label">📉 Projeção em 7 dias</div></div>
            <div class="metric-card"><div class="metric-value">{variacao_30dias:.2f} kg</div><div class="metric-label">📉 Projeção em 30 dias</div></div>
            <div class="metric-card"><div class="metric-value">{tempo_meta}</div><div class="metric-label">⏱️ Tempo estimado</div></div>
        </div>
        <div class="warning-box">
            <strong>ℹ️ Sobre as projeções:</strong><br>
            Esta é uma <strong>estimativa teórica</strong> baseada no déficit/superávit calórico médio.<br><br>
            Variações diárias de peso são normais devido a:<br>
            • 💧 Retenção hídrica (pode variar 1-2kg)<br>
            • ⏰ Horário da pesagem<br>
            • 🍽️ Conteúdo intestinal<br><br>
            O resultado real pode diferir. O mais importante é a <strong>consistência</strong> e a <strong>tendência de longo prazo</strong>.
        </div>
        
        <!-- QUEBRA DE PÁGINA: Cardápio começa na página 3 -->
        <div class="page-break"></div>
        
        <!-- PÁGINA 3: CARDÁPIO -->
        <h2>🍽️ CARDÁPIO - {st.session_state.planejamento_tipo}</h2>
        <table>
            <thead>
                <tr><th>Dia</th><th>Refeição</th><th>Alimento</th><th>Quantidade</th><th>Kcal</th><th>P</th><th>C</th><th>G</th></tr>
            </thead>
            <tbody>{tabela_cardapio_html}</tbody>
        </table>
        
        <div class="footer">
            BioGestão 360 | Este documento foi gerado automaticamente e não substitui avaliação médica profissional.<br>
            Fonte: {st.session_state.fonte_dados} | Método GET: {metodo_atual_nome}
        </div>
    </div>
</body>
</html>"""

        b64_pdf = base64.b64encode(html_pdf.encode()).decode()
        st.markdown(
            f"""
            <a href="data:text/html;base64,{b64_pdf}" download="laudo_biogestao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html" 
               style="background: linear-gradient(135deg, #f59e0b, #ef4444); color: white; padding: 12px 20px; 
               text-decoration: none; border-radius: 8px; display: inline-block; width: 100%; text-align: center; 
               font-weight: bold; font-size: 16px;">
               📄 Baixar Laudo Completo com Gráficos (HTML/PDF)
            </a>
        """,
            unsafe_allow_html=True,
        )
        st.caption(
            "💡 Abra o arquivo HTML e pressione Ctrl+P (ou Cmd+P) para salvar como PDF"
        )
        st.caption(
            "📌 O PDF tem quebras de página: Página 1 (Dados+Perfil+Metabolismo) | Página 2 (Composição+Gráficos+Estimativa) | Página 3 (Cardápio)"
        )

else:
    st.info("📝 Preencha seus dados na barra lateral para gerar o laudo técnico.")

# ============================================
# 33. RESUMO DO LAUDO TÉCNICO (MANTIDO)
# ============================================
if dados_validos:
    st.markdown("---")
    st.markdown("## 📋 RESUMO DO LAUDO TÉCNICO")
    st.markdown(
        f"""
    <div class='resumo-laudo'>
        <h4>📊 Resumo da Análise</h4>
        <p><strong>📅 Período analisado:</strong> {'Hoje (1 dia)' if st.session_state.planejamento_tipo == "Diário" else 'Semana completa (7 dias)'}</p>
        <p><strong>🥗 Consumo total:</strong> {total_kcal:.1f} kcal</p>
        <p><strong>📊 Média diária:</strong> {media_diaria:.1f} kcal</p>
        <p><strong>⚡ Gasto diário (GET):</strong> {get_atual:.0f} kcal</p>
        <p><strong>💪 Saldo diário:</strong> {abs(saldo_diario):.1f} kcal <strong>{"Déficit" if saldo_diario > 0 else "Superávit"}</strong></p>
        <p><strong>📉 Projeção em 30 dias:</strong> {variacao_30dias:.2f} kg</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ============================================
# 34. INFORMAÇÃO OMS E DOCUMENTAÇÃO TÉCNICA (MANTIDO)
# ============================================
with st.expander("📋 Informações OMS e Documentação Técnica", expanded=False):
    st.markdown(
        """
    ### Classificação da OMS/IARC para alimentos:
    
    | Grupo | Classificação | Alimentos | Recomendação |
    |-------|--------------|-----------|--------------|
    | **Grupo 1** | **Cancerígeno para humanos** | Carnes processadas, Bebidas alcoólicas | Evitar ou reduzir |
    | **Grupo 2A** | **Provavelmente cancerígeno** | Carne vermelha | Limitar a 500g/semana |
    | **Grupo 2B** | **Possivelmente cancerígeno** | Aspartame, bebidas >65°C | Consumo moderado |
    
    ### 📚 Fórmulas Científicas:
    
    | Cálculo | Fórmula | Fonte |
    |---------|---------|-------|
    | **TMB (Homens)** | 66.47 + (13.75 × P) + (5.0 × A) - (6.75 × I) | Harris-Benedict (1919) |
    | **TMB (Mulheres)** | 655.1 + (9.56 × P) + (1.85 × A) - (4.67 × I) | Harris-Benedict (1919) |
    | **TMB Katch-McArdle** | 370 + (21.6 × Massa Magra) | Katch-McArdle (1975) |
    | **% Gordura (IMC)** | (1.20 × IMC) + (0.23 × I) - (16.2 ou 5.4) | Deurenberg et al. |
    | **% Gordura (Dobras)** | Protocolo Jackson & Pollock + Fórmula de Siri | ACSM |
    
    ### 📊 Sobre as Tabelas Nutricionais
    
    | Tabela | Fonte | Características |
    |--------|-------|-----------------|
    | **TACO (UNICAMP)** | Universidade Estadual de Campinas | Mais completa para alimentos industrializados |
    | **IBGE (POF 2008-2009)** | Pesquisa de Orçamentos Familiares | Mais alimentos in natura e preparações regionais |
    
    🔗 **Fontes oficiais:**
    - **TACO/UNICAMP:** https://www.tbca.net.br/
    - **IBGE - POF 2008-2009:** https://www.ibge.gov.br/estatisticas/sociais/populacao/9050-pesquisa-de-orcamentos-familiares.html
    - **FAO/WHO:** https://www.fao.org/
    
    ### 🥗 Recomendações práticas (OMS)
    
    - ✅ Prefira carnes brancas (frango, peixe)
    - ✅ Cozinhe em temperaturas mais baixas (vapor, cozido)
    - ✅ Evite frituras e churrascos em excesso
    - ✅ Aumente consumo de fibras (frutas, verduras, legumes)
    
    > Este sistema é um **agregador de dados públicos** e não substitui a consulta a um profissional de saúde.
    """
    )

# ============================================
# 35. BOTÃO DE LIMPAR (MANTIDO)
# ============================================
if st.session_state.planejamento_tipo == "Diário":
    total_itens = sum(len(itens) for itens in st.session_state.cardapio.values())
    if total_itens > 0 and not st.session_state.modo_impressao:
        if st.button("🗑️ LIMPAR CARDÁPIO COMPLETO", use_container_width=True):
            limpar_cardapio()

# ============================================
# 36. SAIR DO MODO IMPRESSÃO (MANTIDO)
# ============================================
if st.session_state.modo_impressao:
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔙 Sair do Modo Impressão", use_container_width=True):
            st.session_state.modo_impressao = False
            st.rerun()

# ============================================
# 37. RODAPÉ (MANTIDO)
# ============================================
st.markdown(
    f"""
<div style='text-align: center; font-size: 11px; color: #666; padding: 15px;'>
    <b>BioGestão 360 v3.2</b> | Fonte: {st.session_state.fonte_dados} | Método GET: {metodo_atual_nome if dados_validos else "Harris-Benedict"}<br>
    <b>⚠️ SISTEMA EM DESENVOLVIMENTO - DADOS PODEM CONTER ERRO</b><br>
    🔗 <b>Fontes científicas:</b> TACO/UNICAMP | IBGE (POF 2008-2009) | FAO/WHO<br>
    💻 <a href='https://github.com/adilsonximenes/biogestao-360' target='_blank'>Código Fonte</a>
</div>
""",
    unsafe_allow_html=True,
)
