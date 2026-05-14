"""
portal.py — BioGestão 360
===========================
Landing page com tour guiado real (Driver.js).
Clique em "🎓 Iniciar Tour" e veja os cards sendo destacados.
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg-primary: var(--background-color);
    --bg-secondary: var(--secondary-background-color);
    --text-primary: var(--text-color);
    
    /* Accents */
    --accent-primary: #f59e0b;
    --accent-secondary: #3b82f6;
    --accent-tertiary: #10b981;
    --accent-danger: #ef4444;
    --accent-warning: #f97316;
    --accent-gradient: linear-gradient(135deg, #ffd700, #ff8c00);
    
    /* LIGHT MODE DEFAULTS */
    --text-secondary: #475569;
    --hero-bg: linear-gradient(145deg, #f0fdf4 0%, #e0f2fe 100%);
    --card-bg: rgba(255, 255, 255, 0.7);
    --card-border: rgba(0, 0, 0, 0.08);
    --glass-effect: rgba(255, 255, 255, 0.5);
    
    --header-bg: rgba(0, 0, 0, 0.03);
    --highlight-bg: rgba(0, 0, 0, 0.02);
    
    --shadow-sm: 0 4px 15px rgba(0, 0, 0, 0.03);
    --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.06);
    --shadow-hover: 0 20px 40px rgba(245, 158, 11, 0.15);
    
    --border-radius-sm: 12px;
    --border-radius-md: 20px;
}

@media (prefers-color-scheme: dark) {
    :root {
        /* DARK MODE OVERRIDES */
        --text-secondary: #cbd5e1;
        --hero-bg: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
        --card-bg: rgba(15, 23, 42, 0.4);
        --card-border: rgba(255, 255, 255, 0.05);
        --glass-effect: rgba(255, 255, 255, 0.03);
        
        --header-bg: rgba(0, 0, 0, 0.15);
        --highlight-bg: rgba(15, 23, 42, 0.3);
        
        --shadow-sm: 0 4px 15px rgba(0, 0, 0, 0.2);
        --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    font-family: 'Inter', sans-serif; 
    background: var(--bg-primary); 
    color: var(--text-primary); 
    line-height: 1.6;
}

h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
    letter-spacing: -0.02em;
}

/* HERO SECTION */
.hero-section {
    background: var(--hero-bg);
    border-radius: 24px;
    padding: 4rem 2rem;
    text-align: center;
    margin-bottom: 3rem;
    box-shadow: var(--shadow-md);
    position: relative;
    overflow: hidden;
    border: 1px solid var(--card-border);
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255, 215, 0, 0.15) 0%, transparent 60%);
    animation: pulseGlow 15s ease-in-out infinite alternate;
}

@keyframes pulseGlow {
    0% { transform: scale(1); opacity: 0.4; }
    100% { transform: scale(1.1); opacity: 0.8; }
}

.hero-icon {
    font-size: 4rem;
    margin-bottom: 0.5rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.1));
}

.hero-subtitle {
    font-size: 1.2rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
    font-weight: 400;
}

.badge-container {
    margin: 1.5rem 0;
}

.hero-footer {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 1.5rem;
    opacity: 0.8;
}

@media (max-width: 768px) {
    .hero-title { font-size: 2.2rem; }
}

.badge {
    display: inline-block;
    border-radius: 20px;
    padding: 0.35rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 0.5rem 0.3rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.badge-free { background: #22c55e; color: white; border: none; }
.badge-acesso { background: #3b82f6; color: white; border: none; }
.badge-prof { background: #f97316; color: white; border: none; }

/* CARDS */
.tour-card {
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--card-border);
    border-radius: var(--border-radius-md);
    margin-bottom: 2rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    overflow: hidden;
}

.tour-card:hover {
    transform: translateY(-6px) scale(1.01);
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-hover);
}

.card-header {
    background: var(--header-bg);
    padding: 1.2rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    border-bottom: 1px solid var(--card-border);
}

.step-number {
    background: var(--accent-gradient);
    color: white;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.3rem;
    box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
}

.card-header h3 {
    margin: 0;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text-primary);
}

.card-body {
    padding: 1.5rem;
    color: var(--text-secondary);
}

.card-body strong {
    color: var(--text-primary);
}

.highlight-box, .mock-cardapio {
    background: var(--highlight-bg);
    border-left: 4px solid var(--accent-primary);
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.95rem;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
}

.mock-cardapio {
    border-left: none;
    border-top: 4px solid var(--accent-secondary);
    border-radius: 0 0 12px 12px;
    font-family: 'JetBrains Mono', monospace;
}

/* PLANOS */
.planos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.2rem;
    margin: 2rem 0;
}

.plano-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--border-radius-md);
    padding: 1.5rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.plano-card:hover { 
    border-color: var(--accent-secondary); 
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(14, 165, 233, 0.15);
}

.plano-preco { 
    font-size: 1.8rem; 
    font-weight: 800; 
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.5rem 0;
}

/* FOOTER & MISC */
.portal-footer {
    text-align: center;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--card-border);
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.portal-footer a { color: var(--accent-secondary); text-decoration: none; transition: color 0.2s; }
.portal-footer a:hover { color: var(--accent-primary); }

.arrow-right {
    display: inline-block;
    animation: floatRight 1.5s ease-in-out infinite;
    margin-right: 0.5rem;
}

@keyframes floatRight {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(6px); }
}

.flow-card {
    min-width: 200px;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
}
.flow-card:hover {
    border-color: var(--accent-primary);
    background: rgba(16, 185, 129, 0.05);
}
.flow-card h4 {
    color: var(--accent-primary);
    margin-bottom: 0.5rem;
}
.footer-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.footer-card h4 {
    font-size: 1.2rem;
    color: var(--accent-secondary);
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--card-border);
    padding-bottom: 0.5rem;
}
</style>
"""

def tela_portal():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ========== HERO ==========
    st.markdown("""
    <div class="hero-section">
        <div class="hero-icon">🏋️</div>
        <div class="hero-title">BioGestão 360</div>
        <div class="hero-subtitle">Avaliação física, planejamento alimentar e treino – tudo em um só lugar</div>
        <div class="badge-container">
            <span class="badge badge-free">🟢 Gratuito</span>
            <span class="badge badge-acesso">🔐 Cadastro gratuito</span>
            <span class="badge badge-prof">🟡 Profissional</span>
        </div>
        <div class="hero-footer">⚡ Dados científicos | Zero-Footprint | Laudos completos</div>
    </div>
    """, unsafe_allow_html=True)

    # ========== CARDS ==========
    st.markdown("""
    <div class="tour-card" id="step1">
        <div class="card-header">
            <div class="step-number">1</div>
            <h3>⚙️ Barra lateral – o ponto de partida</h3>
        </div>
        <div class="card-body">
            <p><span class='arrow-right'>👉</span> <strong>Preencha seus dados na barra lateral esquerda:</strong> peso, altura, idade, sexo, objetivo e nível de atividade física.</p>
            <div class='highlight-box'><span class='arrow-right'>📌</span> <strong>Exemplo prático:</strong><br>Peso: 70kg · Altura: 170cm · Idade: 30 anos · Sexo: Masculino<br>Objetivo: Perda de peso · Atividade: Moderada (3-5x/semana)</div>
            <p>✅ Após preencher, o sistema calcula <strong>GET, TMB, IMC, % gordura</strong> e projeções de perda/ganho de peso.</p>
            <p>📌 Na barra lateral você também escolhe: <strong>tipo de planejamento (Diário/Semanal)</strong> e a <strong>tabela nutricional</strong> (BioGestão 360 / TACO / IBGE).</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tour-card" id="step2">
        <div class="card-header">
            <div class="step-number">2</div>
            <h3>📋 Identificação da consulta (Seção 24)</h3>
        </div>
        <div class="card-body">
            <p>Cadastre os dados do <strong>paciente</strong> (nome, telefone, e-mail) e do <strong>profissional responsável</strong> (CREF/CRN).</p>
            <div class='highlight-box'><span class='arrow-right'>⚠️</span> <strong>Campo Observações – Restrições alimentares</strong><br>Informe alergias ou intolerâncias, ex: <code>"alergia a camarão"</code>, <code>"intolerância à lactose"</code>.<br>✅ O sistema <strong>alertará automaticamente</strong> ao adicionar alimentos com esses ingredientes.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tour-card" id="step3">
        <div class="card-header">
            <div class="step-number">3</div>
            <h3>📥 Importador Automático (Seção 24.1)</h3>
        </div>
        <div class="card-body">
            <p><span class='badge badge-acesso'>🤖 IA</span> Cole seu cardápio em texto – o sistema identifica alimentos, quantidades e busca valores nutricionais na hierarquia <strong>TACO → IBGE → BioGestão 360 → Estimativa inteligente</strong>.</p>
            <div class='mock-cardapio'><strong>📋 Exemplo (diário):</strong><br>Café da manhã: 2 fatias de pão integral, 200ml de leite desnatado<br>Almoço: 150g de frango grelhado, 100g de arroz integral, 80g de feijão<br>Jantar: 100g de ovos mexidos, 30g de alface</div>
            <p>✔️ Após importar, você pode <strong>marcar/desmarcar itens</strong>, ver <strong>alertas da OMS</strong> e restrições, além de <strong>baixar CSV ou relatório HTML completo</strong>.</p>
            <p><span class='arrow-right'>💡</span> Modo semanal: planeje 7 dias. O sistema soma totais por dia e mostra a média diária.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tour-card" id="step4">
        <div class="card-header">
            <div class="step-number">4</div>
            <h3>📏 Avaliação Física (Seção 25 – Jackson & Pollock)</h3>
        </div>
        <div class="card-body">
            <p><span class='badge badge-prof'>🔬 PROFISSIONAL</span> Protocolo de dobras cutâneas (3 ou 7 dobras), circunferências, handgrip e banco de Wells.</p>
            <div class='highlight-box'><span class='arrow-right'>📐</span> <strong>Exemplo de medições (adipômetro):</strong><br>Tríceps: 12,0 mm | Peitoral: 8,5 mm | Abdome: 20,2 mm | Coxa: 18,0 mm<br>→ O sistema calcula % de gordura, massa magra, classificação (Atleta/Saudável/Obesidade) e risco à saúde.</div>
            <p>✔️ Gera <strong>laudo completo em HTML</strong> com gráficos de composição corporal, comparativo por idade e biotipo.</p>
            <p>⚠️ Recomendado para profissionais de Educação Física com CREF ativo.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tour-card" id="step5">
        <div class="card-header">
            <div class="step-number">5</div>
            <h3>🏋️ Monte Seu Treino (Seção 25.1)</h3>
        </div>
        <div class="card-body">
            <p><strong>Ferramenta completa para prescrição de exercícios:</strong></p>
            <ul><li>Anamnese – condições de saúde, lesões, liberação médica, FC repouso.</li><li>Modalidades – musculação, corrida, natação, triatlo, dança, lutas, esportes, adaptado PCD.</li><li>Cálculo de calorias – baseado no MET.</li><li>Sugestão automática conforme nível, frequência e modalidade.</li><li>Montagem livre – 120+ exercícios, 15 métodos (superset, drop set, pirâmide, AMRAP...).</li></ul>
            <div class='highlight-box'><span class='arrow-right'>🎯</span> <strong>Exemplo:</strong> Supino reto — 4×12 (séries convencionais) ou Agachamento — pirâmide crescente 12→10→8 reps com carga 40→50→60kg.</div>
            <p>✔️ Relatório HTML com todas as séries, alertas de contraindicações e zonas de frequência cardíaca.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tour-card" id="step6">
        <div class="card-header">
            <div class="step-number">6</div>
            <h3>🍏 Plano Alimentar manual (Seção 26)</h3>
        </div>
        <div class="card-body">
            <p>Escolha refeição, alimento (com suporte a marcas), quantidade e unidade (g/ml/un).</p>
            <div class='highlight-box'><span class='arrow-right'>📌</span> <strong>Regra de ouro para precisão:</strong><br>Para alimentos em "unidades" (biscoito, ovo, pão, fruta), <strong>informe o peso real de UMA unidade</strong> no campo "Peso Real (g/ml)".<br>Ex: 1 biscoito maisena = 5g → informe Peso Real = 5g, Quantidade = 2 → total 10g.</div>
            <p>✔️ O sistema exibe macros, micronutrientes e alertas de risco OMS em tempo real.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tour-card" id="step7">
        <div class="card-header">
            <div class="step-number">7</div>
            <h3>⚠️ Alertas científicos e geração de laudos</h3>
        </div>
        <div class="card-body">
            <p>O BioGestão 360 sinaliza automaticamente alimentos com classificação de risco pela <strong>IARC/OMS</strong>:</p>
            <p><span class='badge' style='background:#dc2626;color:white;'>🔴 GRUPO 1</span> Cancerígeno confirmado (carnes processadas, álcool)<br>
            <span class='badge' style='background:#ea580c;color:white;'>🟠 GRUPO 2A</span> Provavelmente cancerígeno (carne vermelha)<br>
            <span class='badge' style='background:#8b5cf6;color:white;'>🟣 GRUPO 2B</span> Possivelmente cancerígeno (aspartame, bebidas >65°C)</p>
            <p>✔️ <strong>Exportação de laudos:</strong> todas as seções possuem botões para baixar em <strong>CSV</strong> ou <strong>HTML/PDF</strong>.</p>
            <div class='highlight-box'>🖨️ <strong>Impressão:</strong> Use Ctrl+P ou a extensão <strong>GoFullPage</strong> para capturar toda a página com gráficos e tabelas.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tour-card" id="step8">
        <div class="card-header">
            <div class="step-number">8</div>
            <h3>🔒 Política de privacidade e segurança</h3>
        </div>
        <div class="card-body">
            <p><strong>Zero‑Footprint:</strong> cálculos processados localmente no navegador. Ao fechar a aba, seus dados de saúde são permanentemente deletados.</p>
            <p><strong>Cadastro opcional:</strong> apenas nome de usuário, e‑mail e senha (hash SHA‑256).</p>
            <p><strong>Banco de dados:</strong> PostgreSQL no Supabase com SSL obrigatório.</p>
            <p><strong>Bases nutricionais:</strong> BioGestão 360 (Open Food Facts/ODbL) · TACO/UNICAMP · IBGE/POF.</p>
            <p><strong>Pagamentos via PIX ou PayPal</strong> – o app não armazena dados bancários.</p>
            <p><strong>Licença CC BY-NC-ND 4.0:</strong> uso educacional permitido com atribuição. Proibida comercialização ou obra derivada.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ========== PLANOS DE APOIO ==========
    st.markdown("## 💚 Colaboração voluntária")
    st.markdown("O BioGestão 360 é gratuito e sempre será. Sua contribuição ajuda a manter o servidor e evoluir o app. Após 2 dias de teste, você pode continuar com qualquer valor.")

    st.markdown("""
    <div class="planos-grid">
        <div class="plano-card"><div class="plano-nome">☕ Café</div><div class="plano-preco">R$ 5</div><div class="plano-desc">Importador 30 dias</div></div>
        <div class="plano-card"><div class="plano-nome">🥗 Básico</div><div class="plano-preco">R$ 15</div><div class="plano-desc">Importador 1 ano</div></div>
        <div class="plano-card"><div class="plano-nome">💪 Pro</div><div class="plano-preco">R$ 10</div><div class="plano-desc">Avaliação Física 30 dias</div></div>
        <div class="plano-card"><div class="plano-nome">🏆 Combo Mensal</div><div class="plano-preco">R$ 12</div><div class="plano-desc">Importador + Avaliação 30 dias</div></div>
        <div class="plano-card"><div class="plano-nome">🌟 Combo Anual</div><div class="plano-preco">R$ 25</div><div class="plano-desc">Importador + Avaliação 1 ano</div></div>
        <div class="plano-card"><div class="plano-nome">♾️ Vitalício</div><div class="plano-preco">R$ 49</div><div class="plano-desc">Importador para sempre</div></div>
        <div class="plano-card"><div class="plano-nome">🏅 Combo Vitalício</div><div class="plano-preco">R$ 79</div><div class="plano-desc">Importador + Avaliação para sempre</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("📱 **PIX:** f3e890da-fb72-4e8c-a0cd-d88177457a30\n\nADILSON GONCALVES XIMENES")
    with col2:
        st.info("💬 **WhatsApp:** (21) 97948-6731\n\nEnvie o comprovante para ativação em até 72h")

    st.markdown("""
    <div class="portal-footer">
        BioGestão 360 v5.0 – Desenvolvido por Adilson Gonçalves Ximenes<br>
        Bacharel em Educação Física (2005) | Técnico em Processamento de Dados (1996)<br>
        🔗 Bases: Open Food Facts (ODbL) · TACO/UNICAMP · IBGE/POF · OMS/IARC · IN 75/2020<br>
        <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank">📄 Licença CC BY-NC-ND 4.0</a> · 
        <a href="https://t.me/biogestao360" target="_blank">📱 Telegram</a> · 
        <a href="mailto:adilson.ximenes@gmail.com">✉️ E-mail</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title="BioGestão 360 – Guia com Tour", layout="wide")
    tela_portal()