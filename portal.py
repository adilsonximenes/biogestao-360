"""
portal.py — BioGestão 360
===========================
Landing page / guia de uso do aplicativo.
Design clean, responsivo, com suporte a tema claro/escuro.
"""

import streamlit as st

_CSS = """
<style>
/* ========== VARIÁVEIS CSS QUE RESPONDEM AO TEMA ========== */
:root {
    --bg-card: var(--secondary-background-color);
    --border-card: var(--border-color);
    --text-primary: var(--text-color);
    --text-secondary: var(--text-color-dim);
    --accent: #f59e0b;
    --accent-light: #fbbf24;
    --accent-dark: #d97706;
    --badge-free: #22c55e;
    --badge-acesso: #3b82f6;
    --badge-prof: #f97316;
    --badge-oms1: #dc2626;
    --badge-oms2a: #ea580c;
    --badge-oms2b: #8b5cf6;
}

/* Cards principais */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1.8rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 20px rgba(0,0,0,0.08);
}

/* Cabeçalho do card */
.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1rem;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.6rem;
}
.card-header .step-num {
    background: var(--accent);
    color: white;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.2rem;
}
.card-header h3 {
    margin: 0;
    font-size: 1.4rem;
    font-weight: 600;
}

/* Badges (etiquetas) */
.badge {
    display: inline-block;
    border-radius: 30px;
    padding: 4px 12px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    margin-right: 8px;
    text-transform: uppercase;
}
.badge-free { background: var(--badge-free); color: white; }
.badge-acesso { background: var(--badge-acesso); color: white; }
.badge-prof { background: var(--badge-prof); color: white; }
.badge-oms1 { background: var(--badge-oms1); color: white; }
.badge-oms2a { background: var(--badge-oms2a); color: white; }
.badge-oms2b { background: var(--badge-oms2b); color: white; }

/* Setas animadas */
.arrow-right {
    display: inline-block;
    animation: bounceRight 0.9s infinite;
    font-size: 1.3rem;
    margin-left: 6px;
}
.arrow-down {
    display: inline-block;
    animation: bounceDown 0.9s infinite;
    font-size: 1.3rem;
    margin: 0 4px;
}
@keyframes bounceRight {
    0%,100% { transform: translateX(0); }
    50% { transform: translateX(6px); }
}
@keyframes bounceDown {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(6px); }
}

/* Caixas de destaque */
.highlight-box {
    background: var(--bg-card);
    border-left: 5px solid var(--accent);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin: 1rem 0;
    font-size: 0.9rem;
}
.simulate-code {
    background: var(--bg-card);
    font-family: monospace;
    border-radius: 12px;
    padding: 0.8rem;
    border: 1px solid var(--border-card);
    margin: 0.8rem 0;
}

/* Planos de apoio */
.plan-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.plan-card {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 20px;
    padding: 1rem;
    text-align: center;
    transition: 0.1s;
}
.plan-card:hover { border-color: var(--accent); }
.plan-price {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--accent);
}
.plan-name { font-weight: 700; margin: 0.5rem 0 0.2rem; }
.plan-desc { font-size: 0.7rem; opacity: 0.7; }

/* Rodapé */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-card);
    font-size: 0.75rem;
    color: var(--text-secondary);
}
</style>
"""

def tela_portal():
    st.markdown(_CSS, unsafe_allow_html=True)

    # === HERO ===
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <span style="font-size: 4rem;">🏋️</span>
        <h1 style="margin: 0.2rem 0 0; font-size: 2.5rem;">BioGestão 360</h1>
        <p style="font-size: 1.2rem; opacity: 0.85;">Avaliação física, planejamento alimentar e treino – tudo em um só lugar</p>
        <p><span class="badge badge-free">🟢 Gratuito</span> <span class="badge badge-acesso">🔐 Cadastro gratuito</span> <span class="badge badge-prof">🟡 Profissional</span></p>
        <p>⚡ Dados científicos | Zero-Footprint | Geração de laudos completos</p>
    </div>
    """, unsafe_allow_html=True)

    # === PASSO 1 – SIDEBAR ===
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="step-num">1</span>
            <h3>⚙️ Barra lateral – o ponto de partida</h3>
        </div>
        <p><strong>🔑 Preencha seus dados:</strong> peso, altura, idade, sexo, objetivo, nível de atividade física.</p>
        <div class="highlight-box">
            <span class="arrow-right">👉</span> <strong>Exemplo:</strong> 70kg · 170cm · 30 anos · Masculino · Perda de peso · Moderado (3-5x/sem)
        </div>
        <p>✅ Após preencher, o sistema calcula <strong>GET (gasto calórico total), TMB, IMC, % gordura estimada</strong> e projeções de perda/ganho de peso.</p>
        <p>📌 Na barra lateral você também escolhe: <strong>tipo de planejamento (Diário/Semanal)</strong> e a <strong>tabela nutricional</strong> (BioGestão 360 / TACO / IBGE).</p>
        <span class="arrow-down">👇</span> <em>Os resultados aparecem em tempo real no dashboard principal.</em>
    </div>
    """, unsafe_allow_html=True)

    # === PASSO 2 – IDENTIFICAÇÃO E RESTRIÇÕES ===
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="step-num">2</span>
            <h3>📋 Identificação da consulta (Seção 24)</h3>
        </div>
        <p>Cadastre os dados do <strong>paciente</strong> (nome, telefone, e-mail) e do <strong>profissional responsável</strong> (CREF/CRN).</p>
        <div class="highlight-box">
            <span class="arrow-right">⚠️</span> <strong>Campo Observações – Restrições alimentares</strong><br>
            Informe alergias ou intolerâncias, ex: <code>"alergia a camarão"</code>, <code>"intolerância à lactose"</code>, <code>"não pode glúten"</code>.<br>
            ✅ O sistema <strong>alertará automaticamente</strong> ao adicionar alimentos que contenham o ingrediente restrito.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === PASSO 3 – IMPORTADOR AUTOMÁTICO DE CARDÁPIO ===
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="step-num">3</span>
            <h3>📥 Importador Automático (Seção 24.1)</h3>
        </div>
        <p><span class="badge badge-acesso">🤖 IA</span> Cole seu cardápio em texto – o sistema identifica alimentos, quantidades e busca valores nutricionais na hierarquia <strong>TACO → IBGE → BioGestão 360 → Estimativa inteligente</strong>.</p>
        <div class="simulate-code">
            <strong>📋 Exemplo (diário):</strong><br>
            Café da manhã: 2 fatias de pão integral, 200ml de leite desnatado<br>
            Almoço: 150g de frango grelhado, 100g de arroz integral, 80g de feijão<br>
            Jantar: 100g de ovos mexidos, 30g de alface
        </div>
        <p>✔️ Após importar, você pode <strong>marcar/desmarcar itens</strong>, ver <strong>alertas da OMS (Grupos 1, 2A, 2B)</strong> e restrições alimentares, além de <strong>baixar CSV ou relatório HTML completo com gráficos</strong>.</p>
        <p><span class="arrow-right">💡</span> Modo semanal: planeje 7 dias. O sistema soma totais por dia e mostra a média diária.</p>
    </div>
    """, unsafe_allow_html=True)

    # === PASSO 4 – AVALIAÇÃO FÍSICA PROFISSIONAL ===
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="step-num">4</span>
            <h3>📏 Avaliação Física (Seção 25 – Jackson & Pollock)</h3>
        </div>
        <p><span class="badge badge-prof">🔬 PROFISSIONAL</span> Protocolo de dobras cutâneas (3 ou 7 dobras), circunferências, handgrip e banco de Wells.</p>
        <div class="highlight-box">
            <span class="arrow-right">📐</span> <strong>Exemplo de medições (adipômetro):</strong><br>
            Tríceps: 12,0 mm | Peitoral: 8,5 mm | Abdome: 20,2 mm | Coxa: 18,0 mm<br>
            → O sistema calcula % de gordura, massa magra, classificação (Atleta/Saudável/Obesidade) e risco à saúde.
        </div>
        <p>✔️ Gera <strong>laudo completo em HTML</strong> com gráficos de composição corporal, comparativo por idade e biotipo.</p>
        <p>⚠️ Recomendado para profissionais de Educação Física com CREF ativo. Mais preciso que a estimativa por IMC.</p>
    </div>
    """, unsafe_allow_html=True)

    # === PASSO 5 – MONTE SEU TREINO ===
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="step-num">5</span>
            <h3>🏋️ Monte Seu Treino (Seção 25.1 – Educação Física)</h3>
        </div>
        <p><strong>Ferramenta completa para prescrição de exercícios:</strong></p>
        <ul>
            <li><strong>Anamnese</strong> – condições de saúde, lesões, liberação médica, frequência cardíaca de repouso.</li>
            <li><strong>Modalidades</strong> – musculação, corrida, natação, triatlo, dança, lutas, esportes olímpicos, adaptado PCD.</li>
            <li><strong>Cálculo de calorias</strong> – baseado no MET (Compendium of Physical Activities).</li>
            <li><strong>Sugestão automática</strong> conforme nível, frequência e modalidade.</li>
            <li><strong>Montagem livre</strong> – 120+ exercícios, 15 métodos (superset, drop set, pirâmide, AMRAP, EMOM, circuito...).</li>
        </ul>
        <div class="highlight-box">
            <span class="arrow-right">🎯</span> <strong>Exemplo:</strong> Supino reto — 4×12 (séries convencionais) ou Agachamento — pirâmide crescente 12→10→8 reps com carga 40→50→60kg.
        </div>
        <p>✔️ Relatório HTML com todas as séries, alertas de contraindicações e zonas de frequência cardíaca.</p>
    </div>
    """, unsafe_allow_html=True)

    # === PASSO 6 – PLANO ALIMENTAR (busca manual) ===
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="step-num">6</span>
            <h3>🍏 Plano Alimentar manual (Seção 26)</h3>
        </div>
        <p>Escolha refeição, alimento (com suporte a marcas), quantidade e unidade (g/ml/un).</p>
        <div class="highlight-box">
            <span class="arrow-right">📌</span> <strong>Regra de ouro para precisão:</strong><br>
            Para alimentos em "unidades" (biscoito, ovo, pão, fruta), <strong>informe o peso real de UMA unidade</strong> no campo "Peso Real (g/ml)".<br>
            Ex: 1 biscoito maisena = 5g → informe Peso Real = 5g, Quantidade = 2 → total 10g.
        </div>
        <p>✔️ O sistema exibe macros, micronutrientes (açúcar, saturada, trans, fibra, sódio) e alertas de risco OMS em tempo real.</p>
    </div>
    """, unsafe_allow_html=True)

    # === PASSO 7 – ALERTAS OMS E RELATÓRIOS ===
    st.markdown("""
    <div class="card">
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
        <p>🖨️ <strong>Impressão:</strong> Use Ctrl+P ou a extensão GoFullPage para capturar toda a página com gráficos e tabelas.</p>
    </div>
    """, unsafe_allow_html=True)

    # === PASSO 8 – PRIVACIDADE E SEGURANÇA ===
    st.markdown("""
    <div class="card">
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

    # === PLANOS DE APOIO ===
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

    # === RODAPÉ ===
    st.markdown("""
    <div class="footer">
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