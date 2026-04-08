import streamlit as st
import pandas as pd
import os
import math

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="BioGestão 360", layout="wide")

# 2. INICIALIZAÇÕES
if 'modo_impressao' not in st.session_state:
    st.session_state.modo_impressao = False

# 3. FUNÇÃO PARA CALCULAR COMPOSIÇÃO CORPORAL
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

# 4. FUNÇÃO PARA LIMPAR O CARDÁPIO
def limpar_cardapio():
    st.session_state.cardapio = {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]}
    st.success("✅ Cardápio limpo com sucesso!")
    st.rerun()

# 5. CSS MELHORADO - PERFIL SUPER DESTACADO
st.markdown("""
<style>
    /* ESTILOS GERAIS */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* PERFIL SUPER DESTACADO */
    .perfil-super-destacado {
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #1e3a5f 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 25px 0;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border: 2px solid #ffd700;
    }
    
    .perfil-super-destacado .perfil-titulo {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        letter-spacing: 2px;
        color: #ffd700;
        text-transform: uppercase;
    }
    
    .perfil-super-destacado .perfil-dados {
        display: flex;
        justify-content: center;
        gap: 30px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    
    .perfil-super-destacado .perfil-item {
        background: rgba(255,255,255,0.15);
        padding: 12px 20px;
        border-radius: 50px;
        font-size: 18px;
        font-weight: bold;
    }
    
    .perfil-super-destacado .meta-destacada {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        padding: 15px 25px;
        border-radius: 60px;
        margin-top: 15px;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        border: 2px solid #ffd700;
    }
    
    .perfil-super-destacado .meta-destacada .meta-label {
        font-size: 16px;
        letter-spacing: 1px;
        opacity: 0.9;
    }
    
    .perfil-super-destacado .meta-destacada .meta-valor {
        font-size: 42px;
        font-weight: bold;
        margin: 5px 0;
        line-height: 1;
    }
    
    .perfil-super-destacado .meta-destacada .meta-sub {
        font-size: 14px;
        opacity: 0.8;
    }
    
    .perfil-super-destacado .imc-info {
        margin-top: 15px;
        font-size: 16px;
        background: rgba(0,0,0,0.3);
        padding: 8px 15px;
        border-radius: 30px;
        display: inline-block;
    }
    
    /* CARDS */
    .card-ticket {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid var(--border-color);
        margin: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .card-composicao {
        background-color: var(--secondary-background-color);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid var(--border-color);
        margin: 5px;
    }
    
    .card-composicao h4 {
        margin-bottom: 10px;
        font-size: 16px;
        color: var(--text-color);
    }
    
    .card-composicao .valor {
        font-size: 24px;
        font-weight: bold;
        color: var(--text-color);
    }
    
    /* AVISOS */
    .aviso-critico {
        background-color: #dc2626;
        color: white;
        padding: 20px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* BANNER */
    .banner-ef {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #1e3a5f, #3b82f6);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .banner-ef h1 {
        color: white;
        margin: 0;
        font-size: 40px;
    }
    
    /* INSTRUÇÃO E PRIVACIDADE */
    .instrucao-impressao {
        background-color: #dbeafe;
        border-left: 5px solid #3b82f6;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        color: #1e3a8a !important;
    }
    
    .privacidade-box {
        background-color: #f3f4f6;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #6b7280;
        margin: 15px 0;
        color: #374151 !important;
    }
    
    /* REFEIÇÕES */
    .header-ref {
        background-color: #3b82f6;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 15px;
        font-size: 20px;
        font-weight: bold;
    }
    
    .macro-tag {
        display: inline-block;
        padding: 5px 10px;
        margin: 5px;
        border-radius: 6px;
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        font-size: 14px;
    }
    
    .alerta-oms {
        background-color: #dc2626;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        display: inline-block;
        margin-top: 5px;
    }
    
    /* IMPRESSÃO */
    @media print {
        section[data-testid="stSidebar"],
        .stButton,
        header,
        footer,
        .aviso-critico,
        .instrucao-impressao,
        .privacidade-box,
        .stExpander,
        button {
            display: none !important;
        }
        
        * {
            background-color: white !important;
            color: black !important;
            border-color: #ccc !important;
            box-shadow: none !important;
        }
        
        .perfil-super-destacado {
            background: white !important;
            border: 2px solid #000 !important;
            box-shadow: none !important;
        }
        
        .perfil-super-destacado .perfil-titulo {
            color: #000 !important;
        }
        
        .perfil-super-destacado .meta-destacada {
            background: white !important;
            border: 2px solid #000 !important;
            box-shadow: none !important;
        }
        
        .main .block-container {
            padding: 0.5cm !important;
            margin: 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 6. SIDEBAR
with st.sidebar:
    st.markdown("### 👤 Perfil Biológico")
    st.markdown("---")
    
    peso_at = st.number_input("📊 Peso Atual (kg)", 30.0, 250.0, 85.8)
    alt_cm = st.number_input("📏 Altura (cm)", 100, 230, 164)
    idade = st.number_input("🎂 Idade", 10, 110, 47)
    sexo = st.selectbox("⚥ Sexo Biológico", ["Masculino", "Feminino"])
    
    st.markdown("---")
    st.markdown("### 🎯 Objetivos")
    
    p_alvo = st.number_input("🎯 Meta de Peso (kg)", 10.0, 250.0, 75.0)
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
    
    st.info("🖨️ **IMPRESSÃO ECONÔMICA:**\n\nClique no botão abaixo → Após recarregar, clique nos **3 pontinhos (⋮)** → **Imprimir** → **Margens: Mínimas**")
    
    if st.button("📄 Gerar Versão para Impressão", use_container_width=True):
        st.session_state.modo_impressao = True
        st.rerun()

# 7. CARGA DE DADOS
@st.cache_data
def load_db():
    df_a = pd.read_csv('alimentos.csv') if os.path.exists('alimentos.csv') else pd.DataFrame()
    df_g = pd.read_csv('acidos-graxos.csv') if os.path.exists('acidos-graxos.csv') else pd.DataFrame()
    df_m = pd.read_csv('aminoacidos.csv') if os.path.exists('aminoacidos.csv') else pd.DataFrame()
    
    def r_oms(n):
        n = str(n).lower()
        if any(x in n for x in ['salsicha', 'bacon', 'presunto', 'salame', 'linguiça', 'mortadela', 'nuggets']): 
            return 'ALERTA OMS: PROCESSADO G1 (CANCERÍGENO)'
        return None
    
    if not df_a.empty: 
        df_a['Risco_OMS'] = df_a['Descrição dos alimentos'].apply(r_oms)
    return df_a, df_g, df_m

df_taco, df_graxos, df_amino = load_db()

# 8. HEADER
if st.session_state.modo_impressao:
    st.markdown("""
    <div class='aviso-critico' style='background-color: #10b981;'>
        ✅ MODO IMPRESSÃO ATIVADO - Visualização otimizada para economia de tinta/papel
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='aviso-critico'>
        ⚠️ SISTEMA EM DESENVOLVIMENTO BASEADO NA TABELA TACO - DADOS PODEM CONTER ERRO
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='banner-ef'><h1>🏋️‍♂️ BioGestão 360</h1></div>", unsafe_allow_html=True)

if not st.session_state.modo_impressao:
    st.markdown("""
    <div class='instrucao-impressao'>
        <b>🖨️ PROCEDIMENTO DE IMPRESSÃO (PDF):</b><br>
        1️⃣ Clique em <b>"Gerar Versão para Impressão"</b> no menu lateral<br>
        2️⃣ Aguarde o recarregamento da página<br>
        3️⃣ Clique nos <b>3 pontinhos (⋮)</b> no canto superior direito do navegador<br>
        4️⃣ Selecione <b>Imprimir</b><br>
        5️⃣ Configure <b>Margens: Mínimas</b> e <b>Salvar como PDF</b>
    </div>
    <div class='privacidade-box'>
        <b>🔒 POLÍTICA DE PRIVACIDADE (ZERO-FOOTPRINT):</b><br>
        ✅ Nenhum dado é enviado para servidores externos<br>
        ✅ Processamento 100% local no seu navegador<br>
        ✅ Ao fechar a aba, todas as informações são permanentemente deletadas
    </div>
    """, unsafe_allow_html=True)

# 9. CÁLCULOS BIOMÉTRICOS
alt_m = alt_cm / 100
imc = peso_at / (alt_m ** 2)
if sexo == "Masculino":
    tmb = 66.47 + (13.75 * peso_at) + (5.0 * alt_cm) - (6.75 * idade)
else:
    tmb = 655.1 + (9.56 * peso_at) + (1.85 * alt_cm) - (4.67 * idade)
get_total = tmb * naf_val

# 10. COMPOSIÇÃO CORPORAL
composicao = calcular_composicao_corporal(peso_at, alt_cm, idade, sexo)

# 11. PERFIL SUPER DESTACADO
# Calcular diferença para a meta
diferenca_meta = p_alvo - peso_at
if diferenca_meta > 0:
    texto_meta = f"Faltam {abs(diferenca_meta):.1f} kg para atingir sua meta!"
    cor_meta = "#f59e0b"
elif diferenca_meta < 0:
    texto_meta = f"Você está {abs(diferenca_meta):.1f} kg acima da sua meta"
    cor_meta = "#ef4444"
else:
    texto_meta = "Parabéns! Você atingiu sua meta!"
    cor_meta = "#10b981"

# Classificação do IMC
if imc < 18.5:
    classificacao_imc = "Abaixo do peso"
    cor_imc = "#3b82f6"
elif imc < 25:
    classificacao_imc = "Peso normal"
    cor_imc = "#10b981"
elif imc < 30:
    classificacao_imc = "Sobrepeso"
    cor_imc = "#f59e0b"
elif imc < 35:
    classificacao_imc = "Obesidade Grau I"
    cor_imc = "#ef4444"
elif imc < 40:
    classificacao_imc = "Obesidade Grau II"
    cor_imc = "#dc2626"
else:
    classificacao_imc = "Obesidade Grau III"
    cor_imc = "#991b1b"

st.markdown(f"""
<div class='perfil-super-destacado'>
    <div class='perfil-titulo'>
        📋 PERFIL BIOLÓGICO
    </div>
    <div class='perfil-dados'>
        <div class='perfil-item'>⚖️ {peso_at} kg</div>
        <div class='perfil-item'>📏 {alt_cm} cm</div>
        <div class='perfil-item'>🎂 {idade} anos</div>
        <div class='perfil-item'>⚥ {sexo}</div>
    </div>
    <div class='meta-destacada'>
        <div class='meta-label'>🎯 META DE PESO</div>
        <div class='meta-valor'>{p_alvo} kg</div>
        <div class='meta-sub'>{texto_meta}</div>
    </div>
    <div class='imc-info'>
        📊 IMC: {imc:.1f} - <span style='color: {cor_imc}; font-weight: bold;'>{classificacao_imc}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 12. DASHBOARD
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("⚡ GET Diário", f"{get_total:.0f} kcal", help="Gasto Energético Total diário")
with col2:
    st.metric("🔥 TMB Basal", f"{tmb:.0f} kcal", help="Taxa Metabólica Basal")
with col3:
    st.metric("📊 IMC", f"{imc:.1f}", help="Índice de Massa Corporal")

st.markdown("---")
st.markdown("## 🧬 Análise de Composição Corporal")

col_g1, col_g2, col_g3, col_g4 = st.columns(4)

with col_g1:
    st.metric("🎯 Percentual de Gordura", f"{composicao['percentual_gordura']}%")
with col_g2:
    st.metric("⚖️ Massa de Gordura", f"{composicao['massa_gordura']} kg")
with col_g3:
    st.metric("💪 Massa Magra", f"{composicao['massa_magra']} kg")
with col_g4:
    st.metric("🏆 Peso Ideal", f"{composicao['peso_ideal']} kg")

with st.expander("📖 Entenda sua composição corporal"):
    st.markdown("""
    - **Percentual de Gordura**: 
        - *Homens saudáveis*: entre 10% e 25%
        - *Mulheres saudáveis*: entre 18% e 32%
    - **Massa Magra**: Músculos, ossos e órgãos (quanto maior, melhor para o metabolismo)
    - **Peso Ideal**: Estimativa baseada no IMC ideal (21.7 para homens, 21.3 para mulheres)
    """)

st.markdown("---")

# 13. MONTAGEM DO PLANO
st.markdown("## 🍏 MONTAGEM DO PLANO ALIMENTAR")

if not st.session_state.modo_impressao:
    st.info("💡 **Dica:** Priorize usar 'Peso Real (g/ml)' com balança para maior precisão.")

if 'cardapio' not in st.session_state: 
    st.session_state.cardapio = {k: [] for k in ["Café da Manhã", "Almoço", "Lanches", "Jantar"]}

if not st.session_state.modo_impressao and not df_taco.empty:
    with st.container():
        col1, col2, col3, col4 = st.columns([1.5, 3, 1, 1])
        with col1: 
            refeicao_sel = st.selectbox("Refeição", list(st.session_state.cardapio.keys()))
        with col2: 
            alimento_sel = st.selectbox("Selecionar Alimento", df_taco['Descrição dos alimentos'].unique())
        with col3: 
            qtd_unidade = st.number_input("Qtd Unid/Copo", 0.0, 50.0, 1.0)
        with col4: 
            peso_real = st.number_input("Peso Real (g/ml)", 0.0, 2000.0, 0.0)

    if st.button("➕ ADICIONAR AO PLANO", use_container_width=True):
        item = df_taco[df_taco['Descrição dos alimentos'] == alimento_sel].iloc[0]
        is_liquido = any(x in alimento_sel.lower() for x in ["suco", "leite", "café", "bebida", "água", "chá"])
        
        if peso_real > 0:
            peso_final = peso_real
            label_qtd = f"{peso_real}ml" if is_liquido else f"{peso_real}g"
        else:
            base_peso = 200 if is_liquido else 50
            peso_final = qtd_unidade * base_peso
            label_qtd = f"{qtd_unidade} Unid (~{peso_final}{'ml' if is_liquido else 'g'})"
        
        fator_calc = peso_final / 100
        st.session_state.cardapio[refeicao_sel].append({
            "Ali": alimento_sel,
            "Qtd": label_qtd,
            "Kcal": round(item['Energia..kcal.'] * fator_calc, 1),
            "P": round(item['Proteína..g.'] * fator_calc, 1),
            "C": round(item['Carboidrato..g.'] * fator_calc, 1),
            "G": round(item['Lipídeos..g.'] * fator_calc, 1),
            "Risco": item.get('Risco_OMS')
        })
        st.rerun()

# 14. EXIBIÇÃO DAS REFEIÇÕES
for refeicao, itens in st.session_state.cardapio.items():
    if itens:
        st.markdown(f"<div class='header-ref'>{refeicao}</div>", unsafe_allow_html=True)
        for idx, item in enumerate(itens):
            with st.container():
                colA, colB, colC = st.columns([4, 7, 1])
                
                with colA:
                    st.markdown(f"**{item['Ali']}**  \n*{item['Qtd']}*")
                
                with colB:
                    cols_macro = st.columns(4)
                    with cols_macro[0]:
                        st.markdown(f"🔥 {item['Kcal']} kcal")
                    with cols_macro[1]:
                        st.markdown(f"🥩 {item['P']}g")
                    with cols_macro[2]:
                        st.markdown(f"🍞 {item['C']}g")
                    with cols_macro[3]:
                        st.markdown(f"🥑 {item['G']}g")
                    
                    if item.get('Risco') and str(item['Risco']) != 'nan':
                        st.markdown(f"<span class='alerta-oms'>{item['Risco']}</span>", unsafe_allow_html=True)
                
                with colC:
                    if not st.session_state.modo_impressao:
                        if st.button("🗑️", key=f"del_{refeicao}_{idx}"):
                            itens.pop(idx)
                            st.rerun()
                
                st.divider()

# 15. LAUDO TÉCNICO FINAL
st.markdown("---")
st.markdown("## 📋 LAUDO TÉCNICO DE VIABILIDADE ALIMENTAR")

# Calcular totais
total_kcal = sum(item['Kcal'] for ref in st.session_state.cardapio.values() for item in ref)
total_prot = sum(item['P'] for ref in st.session_state.cardapio.values() for item in ref)
total_carb = sum(item['C'] for ref in st.session_state.cardapio.values() for item in ref)
total_gord = sum(item['G'] for ref in st.session_state.cardapio.values() for item in ref)

deficit_superavit = get_total - total_kcal
variacao_peso = abs((deficit_superavit * 30) / 7700)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🥗 Consumo Planejado", f"{total_kcal:.1f} kcal")
with col2:
    st.metric("⚡ Gasto Estimado (GET)", f"{get_total:.0f} kcal")
with col3:
    st.metric("💪 Saldo Energético", f"{deficit_superavit:.1f} kcal", 
             "Déficit" if deficit_superavit > 0 else "Superávit")

st.markdown("---")
st.markdown("#### 🍽️ MACRONUTRIENTES TOTAIS DO PLANO")

col_p, col_c, col_g = st.columns(3)
with col_p:
    st.metric("🥩 Proteínas", f"{total_prot:.1f} g")
with col_c:
    st.metric("🍞 Carboidratos", f"{total_carb:.1f} g")
with col_g:
    st.metric("🥑 Gorduras", f"{total_gord:.1f} g")

st.markdown("---")
st.markdown("#### 📊 ESTIMATIVA BIOESTATÍSTICA (PERÍODO DE 30 DIAS)")

col_meta, col_variacao = st.columns(2)
with col_meta:
    st.info(f"🎯 Meta estabelecida: {p_alvo} kg")
with col_variacao:
    if deficit_superavit > 0:
        st.warning(f"⚠️ Projeção de perda de peso: {variacao_peso:.2f} kg em 30 dias\n\n*Déficit diário de {deficit_superavit:.1f} kcal*")
    else:
        st.info(f"📈 Projeção de ganho de peso: {variacao_peso:.2f} kg em 30 dias\n\n*Superávit diário de {abs(deficit_superavit):.1f} kcal*")

with st.expander("🔍 Detalhes da análise bioestatística"):
    st.markdown(f"""
    **Valores calculados:**
    - TMB: {tmb:.0f} kcal/dia
    - GET: {get_total:.0f} kcal/dia
    - Consumo: {total_kcal:.1f} kcal/dia
    - Saldo: {deficit_superavit:.1f} kcal/dia
    - Variação estimada (30 dias): {variacao_peso:.2f} kg
    """)

with st.expander("💡 Recomendações nutricionais"):
    if total_kcal > 0:
        pct_prot = (total_prot * 4 / total_kcal) * 100
        pct_carb = (total_carb * 4 / total_kcal) * 100
        pct_gord = (total_gord * 9 / total_kcal) * 100
        
        st.markdown(f"""
        **Distribuição atual:**
        - Proteínas: {pct_prot:.1f}% das calorias
        - Carboidratos: {pct_carb:.1f}% das calorias  
        - Gorduras: {pct_gord:.1f}% das calorias
        
        **Referência OMS para adultos saudáveis:**
        - Proteínas: 10-35% das calorias totais
        - Carboidratos: 45-65% das calorias totais
        - Gorduras: 20-35% das calorias totais
        """)

# 16. BOTÃO DE LIMPAR
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    total_itens = sum(len(itens) for itens in st.session_state.cardapio.values())
    if total_itens > 0 and not st.session_state.modo_impressao:
        if st.button("🗑️ LIMPAR CARDÁPIO", use_container_width=True):
            limpar_cardapio()

# 17. SAIR DO MODO IMPRESSÃO
if st.session_state.modo_impressao:
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔙 Sair do Modo Impressão", use_container_width=True):
            st.session_state.modo_impressao = False
            st.rerun()

# 18. RODAPÉ
st.markdown("""
---
<div style='text-align: center; font-size: 12px; color: #666;'>
    <b>BioGestão 360 v2.0</b> - Baseado na Tabela TACO (Universidade de Campinas)<br>
    Desenvolvido para fins educacionais e de monitoramento nutricional.
</div>
""", unsafe_allow_html=True)