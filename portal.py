"""
portal.py — BioGestão 360
===========================
Landing page interativa com o visual do app.
Apresenta todas as seções, mostra como usar e incentiva a navegação.
Cores e estilos inspirados no app.py – suporta tema claro/escuro.
"""

import streamlit as st

_CSS = """
<style>
/* ===== VARIÁVEIS CSS (RESPEITA TEMA DO STREAMLIT) ===== */
:root {
    --bg-grad-start: var(--background-color);
    --bg-grad-end: var(--secondary-background-color);
    --card-bg: var(--secondary-background-color);
    --border-color: var(--border-color);
    --text-main: var(--text-color);
    --text-dim: var(--text-color-dim);
    --accent-laranja: #f59e0b;
    --accent-laranja-escuro: #d97706;
    --accent-azul: #1e3a5f;
    --accent-azul-claro: #3b82f6;
    --accent-ouro: #ffd700;
    --accent-ouro-claro: #fef08a;
    --accent-vermelho: #ef4444;
    --accent-verde: #10b981;
    --accent-roxo: #8b5cf6;
}
@media (prefers-color-scheme: dark) {
    :root {
        --card-bg: #1e293b;
        --border-color: #334155;
    }
}
@media (prefers-color-scheme: light) {
    :root {
        --card-bg: #ffffff;
        --border-color: #e2e8f0;
    }
}

/* ===== ELEMENTOS GLOBAIS ===== */
body {
    background: var(--bg-grad-start);
    color: var(--text-main);
}
h1, h2, h3 {
    font-weight: 600;
}
.stApp {
    background: var(--bg-grad-start);
}

/* ===== CARDS PRINCIPAIS (ESTILO PERFIL GIGANTE / AVISO PESO REAL) ===== */
.tour-card {
    background: linear-gradient(135deg, var(--accent-azul), #0f172a);
    border-radius: 20px;
    border: 1px solid var(--accent-ouro);
    padding: 1.2rem 1.8rem;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    transition: transform 0.2s;
}
.tour-card:hover {
    transform: translateY(-4px);
}
.tour-card .card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1rem;
    border-bottom: 2px solid var(--accent-ouro);
    padding-bottom: 0.6rem;
}
.tour-card .step-num {
    background: var(--accent-laranja);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.3rem;
}
.tour-card h3 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent-ouro);
}
.tour-card p, .tour-card li {
    color: #f1f5f9;
}
.tour-card code {
    background: rgba(255,255,255,0.2);
    padding: 2px 6px;
    border-radius: 8px;
    color: #fbbf24;
}
.highlight-box {
    background: rgba(0,0,0,0.3);
    border-left: 5px solid var(--accent-laranja);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin: 1rem 0;
    font-size: 0.9rem;
}
.badge {
    display: inline-block;
    border-radius: 30px;
    padding: 4px 12px;
    font-size: 0.7rem;
    font-weight: 700;
    margin-right: 8px;
}
.badge-free { background: #22c55e; color: white; }
.badge-acesso { background: #3b82f6; color: white; }
.badge-prof { background: #f97316; color: white; }
.badge-oms1 { background: #dc2626; color: white; }
.badge-oms2a { background: #ea580c; color: white; }
.badge-oms2b { background: #8b5cf6; color: white; }

/* Caixa de exemplo de cardápio */
.mock-cardapio {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1rem;
    font-family: monospace;
    margin: 1rem 0;
}
.arrow {
    display: inline-block;
    animation: bounce 0.9s infinite;
    font-size: 1.2rem;
    margin: 0 4px;
}
@keyframes bounce {
    0%,100% { transform: translateX(0); }
    50% { transform: translateX(6px); }
}
@keyframes bounceY {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(6px); }
}
.arrow-down {
    display: inline-block;
    animation: bounceY 0.9s infinite;
    font-size: 1.2rem;
    margin-left: 6px;
}

/* Grid de planos */
.plan-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.plan-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    transition: 0.15s;
}
.plan-card:hover {
    border-color: var(--accent-laranja);
    transform: scale(1.02);
}
.plan-price {
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--accent-laranja);
}
.plan-name { font-weight: 700; margin: 0.5rem 0 0.2rem; }
.plan-desc { font-size: 0.7rem; opacity: 0.8; }

/* Rodapé */
.portal-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.75rem;
    color: var(--text-dim);
}
</style>
"""

def tela_portal():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── HERO (gradiente azul com dourado, igual ao banner do app) ──
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
                border-radius: 24px; padding: 3rem 2rem; text-align: center; margin-bottom: 2.5rem;
                box-shadow: 0 12px 25px rgba(0,0,0,0.3);">
        <div style="font-size: 4rem; margin-bottom: 0.5rem;">🏋️</div>
        <h1 style="margin: 0; font-size: 2.6rem; background: linear-gradient(135deg, #ffd700, #ff8c00);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">BioGestão 360</h1>
        <p style="font-size: 1.2rem; color: #cbd5e1;">Avaliação física, planejamento alimentar e treino – tudo em um só lugar</p>
        <div style="margin-top: 0.8rem;">
            <span class="badge badge-free">🟢 Gratuito</span>
            <span class="badge badge-acesso">🔐 Cadastro gratuito</span>
            <span class="badge badge-prof">🟡 Profissional</span>
        </div>
        <p style="font-size: 0.9rem; margin-top: 1rem; color: #94a3b8;">⚡ Dados científicos | Zero-Footprint | Laudos completos</p>
    </div>
    """, unsafe_allow_html=True)

    # PASSO 1 – SIDEBAR (estilo perfil-gigante)
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <span class="step-num">1</span>
            <h3>⚙️ Barra lateral – o ponto de partida</h3>
        </div>
        <p><strong>🔑 Preencha seus dados:</strong> peso, altura, idade, sexo, objetivo, nível de atividade física.</p>
        <div class="highlight-box">
            <span class="arrow">👉</span> <strong>Exemplo:</strong> 70kg · 170cm · 30 anos · Masculino · Perda de peso · Moderado (3-5x/sem)
        </div>
        <p>✅ Após preencher, o sistema calcula <strong>GET (gasto calórico total), TMB, IMC, % gordura estimada</strong> e projeções de perda/ganho de peso.</p>
        <p>📌 Na barra lateral você também escolhe: <strong>tipo de planejamento (Diário/Semanal)</strong> e a <strong>tabela nutricional</strong> (BioGestão 360 / TACO / IBGE).</p>
        <span class="arrow-down">👇</span> <em>Os resultados aparecem em tempo real no dashboard principal.</em>
    </div>
    """, unsafe_allow_html=True)

    # PASSO 2 – IDENTIFICAÇÃO E RESTRIÇÕES
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <span class="step-num">2</span>
            <h3>📋 Identificação da consulta (Seção 24)</h3>
        </div>
        <p>Cadastre os dados do <strong>paciente</strong> (nome, telefone, e-mail) e do <strong>profissional responsável</strong> (CREF/CRN).</p>
        <div class="highlight-box">
            <span class="arrow">⚠️</span> <strong>Campo Observações – Restrições alimentares</strong><br>
            Informe alergias ou intolerâncias, ex: <code>"alergia a camarão"</code>, <code>"intolerância à lactose"</code>, <code>"não pode glúten"</code>.<br>
            ✅ O sistema <strong>alertará automaticamente</strong> ao adicionar alimentos que contenham o ingrediente restrito.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # PASSO 3 – IMPORTADOR AUTOMÁTICO
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <span class="step-num">3</span>
            <h3>📥 Importador Automático (Seção 24.1)</h3>
        </div>
        <p><span class="badge badge-acesso">🤖 IA</span> Cole seu cardápio em texto – o sistema identifica alimentos, quantidades e busca valores nutricionais na hierarquia <strong>TACO → IBGE → BioGestão 360 → Estimativa inteligente</strong>.</p>
        <div class="mock-cardapio">
            <strong>📋 Exemplo (diário):</strong><br>
            Café da manhã: 2 fatias de pão integral, 200ml de leite desnatado<br>
            Almoço: 150g de frango grelhado, 100g de arroz integral, 80g de feijão<br>
            Jantar: 100g de ovos mexidos, 30g de alface
        </div>
        <p>✔️ Após importar, você pode <strong>marcar/desmarcar itens</strong>, ver <strong>alertas da OMS (Grupos 1, 2A, 2B)</strong> e restrições alimentares, além de <strong>baixar CSV ou relatório HTML completo com gráficos</strong>.</p>
        <p><span class="arrow">💡</span> Modo semanal: planeje 7 dias. O sistema soma totais por dia e mostra a média diária.</p>
    </div>
    """, unsafe_allow_html=True)

    # PASSO 4 – AVALIAÇÃO FÍSICA PROFISSIONAL
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <span class="step-num">4</span>
            <h3>📏 Avaliação Física (Seção 25 – Jackson & Pollock)</h3>
        </div>
        <p><span class="badge badge-prof">🔬 PROFISSIONAL</span> Protocolo de dobras cutâneas (3 ou 7 dobras), circunferências, handgrip e banco de Wells.</p>
        <div class="highlight-box">
            <span class="arrow">📐</span> <strong>Exemplo de medições (adipômetro):</strong><br>
            Tríceps: 12,0 mm | Peitoral: 8,5 mm | Abdome: 20,2 mm | Coxa: 18,0 mm<br>
            → O sistema calcula % de gordura, massa magra, classificação (Atleta/Saudável/Obesidade) e risco à saúde.
        </div>
        <p>✔️ Gera <strong>laudo completo em HTML</strong> com gráficos de composição corporal, comparativo por idade e biotipo.</p>
        <p>⚠️ Recomendado para profissionais de Educação Física com CREF ativo. Mais preciso que a estimativa por IMC.</p>
    </div>
    """, unsafe_allow_html=True)

    # PASSO 5 – MONTE SEU TREINO
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <span class="step-num">5</span>
            <h3>🏋️ Monte Seu Treino (Seção 25.1)</h3>
        </div>
        <p><strong>Ferramenta completa para prescrição de exercícios:</strong></p>
        <ul>
            <li>Anamnese – condições de saúde, lesões, liberação médica, FC repouso.</li>
            <li>Modalidades – musculação, corrida, natação, triatlo, dança, lutas, esportes, adaptado PCD.</li>
            <li>Cálculo de calorias – baseado no MET (Compendium of Physical Activities).</li>
            <li>Sugestão automática conforme nível, frequência e modalidade.</li>
            <li>Montagem livre – 120+ exercícios, 15 métodos (superset, drop set, pirâmide, AMRAP, EMOM, circuito...).</li>
        </ul>
        <div class="highlight-box">
            <span class="arrow">🎯</span> <strong>Exemplo:</strong> Supino reto — 4×12 (séries convencionais) ou Agachamento — pirâmide crescente 12→10→8 reps com carga 40→50→60kg.
        </div>
        <p>✔️ Relatório HTML com todas as séries, alertas de contraindicações e zonas de frequência cardíaca.</p>
    </div>
    """, unsafe_allow_html=True)

    # PASSO 6 – PLANO ALIMENTAR MANUAL
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <span class="step-num">6</span>
            <h3>🍏 Plano Alimentar manual (Seção 26)</h3>
        </div>
        <p>Escolha refeição, alimento (com suporte a marcas), quantidade e unidade (g/ml/un).</p>
        <div class="highlight-box">
            <span class="arrow">📌</span> <strong>Regra de ouro para precisão:</strong><br>
            Para alimentos em "unidades" (biscoito, ovo, pão, fruta), <strong>informe o peso real de UMA unidade</strong> no campo "Peso Real (g/ml)".<br>
            Ex: 1 biscoito maisena = 5g → informe Peso Real = 5g, Quantidade = 2 → total 10g.
        </div>
        <p>✔️ O sistema exibe macros, micronutrientes (açúcar, saturada, trans, fibra, sódio) e alertas de risco OMS em tempo real.</p>
    </div>
    """, unsafe_allow_html=True)

    # PASSO 7 – ALERTAS OMS E RELATÓRIOS
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <span class="step-num">7</span>
            <h3>⚠️ Alertas científicos e geração de laudos</h3>
        </div>
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
    """, unsafe_allow_html=True)

    # PASSO 8 – PRIVACIDADE E SEGURANÇA
    st.markdown("""
    <div class="tour-card">
        <div class="card-header">
            <span class="step-num">8</span>
            <h3>🔒 Política de privacidade e segurança</h3>
        </div>
        <p><strong>Zero‑Footprint:</strong> cálculos processados localmente no navegador. Ao fechar a aba, seus dados de saúde são permanentemente deletados.</p>
        <p><strong>Cadastro opcional:</strong> apenas nome de usuário, e‑mail e senha (hash SHA‑256) para controle de acesso às seções exclusivas (Importador, Avaliação Física).</p>
        <p><strong>Banco de dados:</strong> PostgreSQL no Supabase com SSL obrigatório.</p>
        <p><strong>Bases nutricionais:</strong> BioGestão 360 (Open Food Facts/ODbL) · TACO/UNICAMP 4ª Ed. · IBGE/POF 2008-2009.</p>
        <p><strong>Pagamentos via PIX ou PayPal</strong> – o app não armazena dados bancários.</p>
        <p><strong>Licença CC BY-NC-ND 4.0:</strong> uso educacional permitido com atribuição. Proibida comercialização ou obra derivada.</p>
    </div>
    """, unsafe_allow_html=True)

    # PLANOS DE APOIO
    st.markdown("## 💚 Colaboração voluntária")
    st.markdown("O BioGestão 360 é gratuito e sempre será. Sua contribuição ajuda a manter o servidor e evoluir o app. Após 2 dias de teste, você pode continuar com qualquer valor.")

    st.markdown("""
    <div class="plan-grid">
        <div class="plan-card"><div class="plan-name">☕ Café</div><div class="plan-price">R$ 5</div><div class="plan-desc">Importador 30 dias</div></div>
        <div class="plan-card"><div class="plan-name">🥗 Básico</div><div class="plan-price">R$ 15</div><div class="plan-desc">Importador 1 ano</div></div>
        <div class="plan-card"><div class="plan-name">💪 Pro</div><div class="plan-price">R$ 10</div><div class="plan-desc">Avaliação Física 30 dias</div></div>
        <div class="plan-card"><div class="plan-name">🏆 Combo Mensal</div><div class="plan-price">R$ 12</div><div class="plan-desc">Importador + Avaliação 30 dias</div></div>
        <div class="plan-card"><div class="plan-name">🌟 Combo Anual</div><div class="plan-price">R$ 25</div><div class="plan-desc">Importador + Avaliação 1 ano</div></div>
        <div class="plan-card"><div class="plan-name">♾️ Vitalício</div><div class="plan-price">R$ 49</div><div class="plan-desc">Importador para sempre</div></div>
        <div class="plan-card"><div class="plan-name">🏅 Combo Vitalício</div><div class="plan-price">R$ 79</div><div class="plan-desc">Importador + Avaliação para sempre</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("📱 **PIX:** f3e890da-fb72-4e8c-a0cd-d88177457a30\n\nADILSON GONCALVES XIMENES")
    with col2:
        st.info("💬 **WhatsApp:** (21) 97948-6731\n\nEnvie o comprovante para ativação em até 72h")

    # RODAPÉ
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