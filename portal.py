"""
portal.py — BioGestão 360
===========================
Landing page interativa com design moderno e atraente.
Apresenta todas as seções, mostra como usar e incentiva a navegação.
Estilo inspirado nas melhores práticas de UI/UX para 2025/2026.
"""

import streamlit as st

_CSS = """
<style>
/* ===== VARIÁVEIS CSS COM SUPORTE A DARK MODE ===== */
:root {
    --bg-primary: var(--background-color);
    --bg-secondary: var(--secondary-background-color);
    --card-bg: rgba(255, 255, 255, 0.05);
    --card-border: rgba(255, 255, 255, 0.1);
    --text-primary: var(--text-color);
    --text-secondary: var(--text-color-dim);
    --accent-primary: #f59e0b;
    --accent-secondary: #3b82f6;
    --accent-tertiary: #10b981;
    --accent-danger: #ef4444;
    --accent-warning: #f97316;
    --accent-info: #8b5cf6;
    --gradient-hero: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    --gradient-card: linear-gradient(135deg, rgba(30, 58, 95, 0.1) 0%, rgba(15, 23, 42, 0.1) 100%);
    --glass-effect: rgba(255, 255, 255, 0.03);
    --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.12);
    --shadow-lg: 0 16px 36px rgba(0, 0, 0, 0.15);
    --border-radius-sm: 12px;
    --border-radius-md: 20px;
    --border-radius-lg: 28px;
}

@media (prefers-color-scheme: dark) {
    :root {
        --card-bg: rgba(255, 255, 255, 0.03);
        --card-border: rgba(255, 255, 255, 0.05);
        --glass-effect: rgba(255, 255, 255, 0.02);
    }
}

/* ===== ESTILOS GLOBAIS ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.5;
}

/* ===== HERO SECTION ===== */
.hero-section {
    background: var(--gradient-hero);
    border-radius: var(--border-radius-lg);
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2.5rem;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,215,0,0.08) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.hero-icon {
    font-size: 4rem;
    margin-bottom: 0.5rem;
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffd700, #ff8c00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.5rem 0;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #cbd5e1;
    margin-bottom: 1rem;
}

.badge-container {
    margin: 1rem 0;
}

.badge {
    display: inline-block;
    border-radius: 30px;
    padding: 0.25rem 0.75rem;
    font-size: 0.7rem;
    font-weight: 600;
    margin: 0 0.25rem;
}
.badge-free { background: #22c55e; color: white; }
.badge-acesso { background: #3b82f6; color: white; }
.badge-prof { background: #f97316; color: white; }
.badge-oms1 { background: #dc2626; color: white; }
.badge-oms2a { background: #ea580c; color: white; }
.badge-oms2b { background: #8b5cf6; color: white; }

.hero-footer {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 1rem;
}

/* ===== CARDS PRINCIPAIS ===== */
.tour-card {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border: 1px solid var(--card-border);
    border-radius: var(--border-radius-md);
    margin-bottom: 1.8rem;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
}

.tour-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
    border-color: var(--accent-primary);
}

.card-header {
    background: var(--gradient-card);
    padding: 1rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    border-bottom: 1px solid var(--card-border);
}

.step-number {
    background: var(--accent-primary);
    color: white;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.3rem;
    box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.2);
}

.card-header h3 {
    margin: 0;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--accent-primary);
}

.card-body {
    padding: 1.5rem 1.8rem;
}

.card-body p {
    margin-bottom: 0.8rem;
}

.card-body ul, .card-body ol {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
}

.card-body li {
    margin-bottom: 0.3rem;
}

/* ===== CAIXAS DE DESTAQUE ===== */
.highlight-box {
    background: var(--glass-effect);
    border-left: 4px solid var(--accent-primary);
    border-radius: var(--border-radius-sm);
    padding: 1rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    backdrop-filter: blur(5px);
}

.highlight-box code {
    background: rgba(0,0,0,0.3);
    padding: 0.2rem 0.4rem;
    border-radius: 6px;
    font-family: monospace;
    color: #fbbf24;
}

/* ===== SIMULAÇÃO DE CARDÁPIO ===== */
.mock-cardapio {
    background: var(--glass-effect);
    border: 1px solid var(--card-border);
    border-radius: var(--border-radius-sm);
    padding: 1rem;
    font-family: monospace;
    margin: 1rem 0;
    backdrop-filter: blur(5px);
}

.mock-cardapio strong {
    color: var(--accent-primary);
}

/* ===== SETAS ANIMADAS ===== */
.arrow-right {
    display: inline-block;
    animation: bounceRight 0.9s infinite;
    font-size: 1.2rem;
    margin-right: 0.3rem;
}

.arrow-down {
    display: inline-block;
    animation: bounceDown 0.9s infinite;
    font-size: 1.2rem;
    margin-right: 0.3rem;
}

@keyframes bounceRight {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(5px); }
}

@keyframes bounceDown {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(5px); }
}

/* ===== PLANOS DE APOIO ===== */
.planos-section {
    margin: 2rem 0;
}

.planos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.plano-card {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border: 1px solid var(--card-border);
    border-radius: var(--border-radius-sm);
    padding: 1.2rem;
    text-align: center;
    transition: all 0.2s ease;
}

.plano-card:hover {
    border-color: var(--accent-primary);
    transform: scale(1.02);
    box-shadow: var(--shadow-sm);
}

.plano-nome {
    font-weight: 700;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
}

.plano-preco {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--accent-primary);
    margin-bottom: 0.3rem;
}

.plano-desc {
    font-size: 0.7rem;
    opacity: 0.8;
}

/* ===== RODAPÉ ===== */
.portal-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--card-border);
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.portal-footer a {
    color: var(--accent-primary);
    text-decoration: none;
}

.portal-footer a:hover {
    text-decoration: underline;
}

/* ===== RESPONSIVIDADE ===== */
@media (max-width: 768px) {
    .hero-title {
        font-size: 1.8rem;
    }
    .card-header h3 {
        font-size: 1.1rem;
    }
    .card-body {
        padding: 1rem;
    }
    .planos-grid {
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    }
}
</style>
"""

def tela_portal():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ===== HERO =====
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

    # ===== PASSO 1 – BARRA LATERAL =====
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <div class="step-number">1</div>
            <h3>⚙️ Barra lateral – o ponto de partida</h3>
        </div>
        <div class="card-body">
            <p><span class="arrow-right">👉</span> <strong>Preencha seus dados na barra lateral esquerda:</strong> peso, altura, idade, sexo, objetivo e nível de atividade física.</p>
            <div class="highlight-box">
                <span class="arrow-right">📌</span> <strong>Exemplo prático:</strong><br>
                Peso: 70kg · Altura: 170cm · Idade: 30 anos · Sexo: Masculino<br>
                Objetivo: Perda de peso · Atividade: Moderada (3-5x/semana)
            </div>
            <p>✅ Após preencher, o sistema calcula <strong>GET (gasto calórico total), TMB (metabolismo basal), IMC, percentual de gordura estimado</strong> e projeções de perda/ganho de peso.</p>
            <p>📌 Na barra lateral você também escolhe: <strong>tipo de planejamento (Diário/Semanal)</strong> e a <strong>tabela nutricional</strong> (BioGestão 360 / TACO / IBGE).</p>
            <span class="arrow-down">👇</span> <em>Os resultados aparecem em tempo real no dashboard principal.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== PASSO 2 – IDENTIFICAÇÃO E RESTRIÇÕES =====
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <div class="step-number">2</div>
            <h3>📋 Identificação da consulta (Seção 24)</h3>
        </div>
        <div class="card-body">
            <p>Cadastre os dados do <strong>paciente</strong> (nome, telefone, e-mail) e do <strong>profissional responsável</strong> (CREF/CRN).</p>
            <div class="highlight-box">
                <span class="arrow-right">⚠️</span> <strong>Campo Observações – Restrições alimentares</strong><br>
                Informe alergias ou intolerâncias, ex: <code>"alergia a camarão"</code>, <code>"intolerância à lactose"</code>, <code>"não pode glúten"</code>.<br>
                ✅ O sistema <strong>alertará automaticamente</strong> ao adicionar alimentos que contenham o ingrediente restrito.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== PASSO 3 – IMPORTADOR AUTOMÁTICO =====
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <div class="step-number">3</div>
            <h3>📥 Importador Automático (Seção 24.1)</h3>
        </div>
        <div class="card-body">
            <p><span class="badge badge-acesso">🤖 IA</span> Cole seu cardápio em texto – o sistema identifica alimentos, quantidades e busca valores nutricionais na hierarquia <strong>TACO → IBGE → BioGestão 360 → Estimativa inteligente</strong>.</p>
            <div class="mock-cardapio">
                <strong>📋 Exemplo (diário):</strong><br>
                Café da manhã: 2 fatias de pão integral, 200ml de leite desnatado<br>
                Almoço: 150g de frango grelhado, 100g de arroz integral, 80g de feijão<br>
                Jantar: 100g de ovos mexidos, 30g de alface
            </div>
            <p>✔️ Após importar, você pode <strong>marcar/desmarcar itens</strong>, ver <strong>alertas da OMS (Grupos 1, 2A, 2B)</strong> e restrições alimentares, além de <strong>baixar CSV ou relatório HTML completo com gráficos</strong>.</p>
            <p><span class="arrow-right">💡</span> Modo semanal: planeje 7 dias. O sistema soma totais por dia e mostra a média diária.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== PASSO 4 – AVALIAÇÃO FÍSICA =====
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <div class="step-number">4</div>
            <h3>📏 Avaliação Física (Seção 25 – Jackson & Pollock)</h3>
        </div>
        <div class="card-body">
            <p><span class="badge badge-prof">🔬 PROFISSIONAL</span> Protocolo de dobras cutâneas (3 ou 7 dobras), circunferências, handgrip e banco de Wells.</p>
            <div class="highlight-box">
                <span class="arrow-right">📐</span> <strong>Exemplo de medições (adipômetro):</strong><br>
                Tríceps: 12,0 mm | Peitoral: 8,5 mm | Abdome: 20,2 mm | Coxa: 18,0 mm<br>
                → O sistema calcula % de gordura, massa magra, classificação (Atleta/Saudável/Obesidade) e risco à saúde.
            </div>
            <p>✔️ Gera <strong>laudo completo em HTML</strong> com gráficos de composição corporal, comparativo por idade e biotipo.</p>
            <p>⚠️ Recomendado para profissionais de Educação Física com CREF ativo. Mais preciso que a estimativa por IMC.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== PASSO 5 – MONTE SEU TREINO =====
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <div class="step-number">5</div>
            <h3>🏋️ Monte Seu Treino (Seção 25.1)</h3>
        </div>
        <div class="card-body">
            <p><strong>Ferramenta completa para prescrição de exercícios:</strong></p>
            <ul>
                <li>Anamnese – condições de saúde, lesões, liberação médica, FC repouso.</li>
                <li>Modalidades – musculação, corrida, natação, triatlo, dança, lutas, esportes, adaptado PCD.</li>
                <li>Cálculo de calorias – baseado no MET (Compendium of Physical Activities).</li>
                <li>Sugestão automática conforme nível, frequência e modalidade.</li>
                <li>Montagem livre – 120+ exercícios, 15 métodos (superset, drop set, pirâmide, AMRAP, EMOM, circuito...).</li>
            </ul>
            <div class="highlight-box">
                <span class="arrow-right">🎯</span> <strong>Exemplo:</strong> Supino reto — 4×12 (séries convencionais) ou Agachamento — pirâmide crescente 12→10→8 reps com carga 40→50→60kg.
            </div>
            <p>✔️ Relatório HTML com todas as séries, alertas de contraindicações e zonas de frequência cardíaca.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== PASSO 6 – PLANO ALIMENTAR MANUAL =====
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <div class="step-number">6</div>
            <h3>🍏 Plano Alimentar manual (Seção 26)</h3>
        </div>
        <div class="card-body">
            <p>Escolha refeição, alimento (com suporte a marcas), quantidade e unidade (g/ml/un).</p>
            <div class="highlight-box">
                <span class="arrow-right">📌</span> <strong>Regra de ouro para precisão:</strong><br>
                Para alimentos em "unidades" (biscoito, ovo, pão, fruta), <strong>informe o peso real de UMA unidade</strong> no campo "Peso Real (g/ml)".<br>
                Ex: 1 biscoito maisena = 5g → informe Peso Real = 5g, Quantidade = 2 → total 10g.
            </div>
            <p>✔️ O sistema exibe macros, micronutrientes (açúcar, saturada, trans, fibra, sódio) e alertas de risco OMS em tempo real.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== PASSO 7 – ALERTAS OMS E RELATÓRIOS =====
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <div class="step-number">7</div>
            <h3>⚠️ Alertas científicos e geração de laudos</h3>
        </div>
        <div class="card-body">
            <p>O BioGestão 360 sinaliza automaticamente alimentos com classificação de risco pela <strong>IARC/OMS</strong>:</p>
            <p>
                <span class="badge badge-oms1">🔴 GRUPO 1</span> Cancerígeno confirmado (carnes processadas, álcool)<br>
                <span class="badge badge-oms2a">🟠 GRUPO 2A</span> Provavelmente cancerígeno (carne vermelha)<br>
                <span class="badge badge-oms2b">🟣 GRUPO 2B</span> Possivelmente cancerígeno (aspartame, bebidas >65°C)
            </p>
            <p>✔️ <strong>Exportação de laudos:</strong> todas as seções possuem botões para baixar em <strong>CSV</strong> (planilha) ou <strong>HTML/PDF</strong> (relatório completo com gráficos).</p>
            <div class="highlight-box">
                🖨️ <strong>Impressão:</strong> Use Ctrl+P ou a extensão <strong>GoFullPage</strong> (Chrome/Edge) para capturar toda a página com gráficos e tabelas.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== PASSO 8 – POLÍTICA DE PRIVACIDADE =====
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <div class="step-number">8</div>
            <h3>🔒 Política de privacidade e segurança</h3>
        </div>
        <div class="card-body">
            <p><strong>Zero‑Footprint:</strong> cálculos processados localmente no navegador. Ao fechar a aba, seus dados de saúde são permanentemente deletados.</p>
            <p><strong>Cadastro opcional:</strong> apenas nome de usuário, e‑mail e senha (hash SHA‑256) para controle de acesso às seções exclusivas (Importador, Avaliação Física).</p>
            <p><strong>Banco de dados:</strong> PostgreSQL no Supabase com SSL obrigatório.</p>
            <p><strong>Bases nutricionais:</strong> BioGestão 360 (Open Food Facts/ODbL) · TACO/UNICAMP 4ª Ed. · IBGE/POF 2008-2009.</p>
            <p><strong>Pagamentos via PIX ou PayPal</strong> – o app não armazena dados bancários.</p>
            <p><strong>Licença CC BY-NC-ND 4.0:</strong> uso educacional permitido com atribuição. Proibida comercialização ou obra derivada.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== PLANOS DE APOIO =====
    st.markdown("## 💚 Colaboração voluntária")
    st.markdown("O BioGestão 360 é gratuito e sempre será. Sua contribuição ajuda a manter o servidor e evoluir o app. Após 2 dias de teste, você pode continuar com qualquer valor.")

    st.markdown("""
    <div class="planos-grid">
        <div class="plano-card">
            <div class="plano-nome">☕ Café</div>
            <div class="plano-preco">R$ 5</div>
            <div class="plano-desc">Importador 30 dias</div>
        </div>
        <div class="plano-card">
            <div class="plano-nome">🥗 Básico</div>
            <div class="plano-preco">R$ 15</div>
            <div class="plano-desc">Importador 1 ano</div>
        </div>
        <div class="plano-card">
            <div class="plano-nome">💪 Pro</div>
            <div class="plano-preco">R$ 10</div>
            <div class="plano-desc">Avaliação Física 30 dias</div>
        </div>
        <div class="plano-card">
            <div class="plano-nome">🏆 Combo Mensal</div>
            <div class="plano-preco">R$ 12</div>
            <div class="plano-desc">Importador + Avaliação 30 dias</div>
        </div>
        <div class="plano-card">
            <div class="plano-nome">🌟 Combo Anual</div>
            <div class="plano-preco">R$ 25</div>
            <div class="plano-desc">Importador + Avaliação 1 ano</div>
        </div>
        <div class="plano-card">
            <div class="plano-nome">♾️ Vitalício</div>
            <div class="plano-preco">R$ 49</div>
            <div class="plano-desc">Importador para sempre</div>
        </div>
        <div class="plano-card">
            <div class="plano-nome">🏅 Combo Vitalício</div>
            <div class="plano-preco">R$ 79</div>
            <div class="plano-desc">Importador + Avaliação para sempre</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("📱 **PIX:** f3e890da-fb72-4e8c-a0cd-d88177457a30\n\nADILSON GONCALVES XIMENES")
    with col2:
        st.info("💬 **WhatsApp:** (21) 97948-6731\n\nEnvie o comprovante para ativação em até 72h")

    # ===== RODAPÉ =====
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
    st.set_page_config(page_title="BioGestão 360 – Guia de Uso", layout="wide")
    tela_portal()