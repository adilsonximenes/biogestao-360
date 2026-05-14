"""
portal.py — BioGestão 360
===========================
Página de instrução / landing page interativa.
Agora com guia visual completo: sidebar, importador de cardápio,
avaliação física, montagem de treino, plano alimentar, alertas OMS,
política de privacidade e muito mais.
"""

import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
# CSS PERSONALIZADO PARA ELEMENTOS VISUAIS (setas, círculos, cards, animações)
# ══════════════════════════════════════════════════════════════════════════════
_CSS = """
<style>
/* Fonte e reset */
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
* { font-family: 'Inter', sans-serif; }

/* Hero aprimorado */
.hero {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 60%, #1a1a2e 100%);
    border-radius: 24px; padding: 48px 32px; color: white;
    text-align: center; margin-bottom: 32px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}
.hero h1 { font-size: 2.8em; margin: 0 0 8px; background: linear-gradient(135deg, #ffd700, #ff8c00);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero p  { font-size: 1.2em; opacity: 0.9; margin: 8px 0; }
.hero small { opacity: 0.7; }

/* Card de passo a passo */
.tour-step {
    background: #f8fafc; border-radius: 20px;
    border: 1px solid #e2e8f0; margin-bottom: 28px;
    overflow: hidden; transition: all 0.2s;
}
.tour-step:hover { box-shadow: 0 8px 25px rgba(0,0,0,0.08); transform: translateY(-2px); }
.tour-header {
    background: #0f3460; color: white; padding: 14px 20px;
    font-size: 1.3rem; font-weight: 600;
    display: flex; align-items: center; gap: 12px;
}
.tour-header .step-num {
    background: #ffd700; color: #0f3460;
    width: 36px; height: 36px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 1.2rem;
}
.tour-body { padding: 20px 24px; }
.tour-body p { margin-bottom: 12px; line-height: 1.5; }
.seta {
    display: inline-block; font-size: 1.6rem; margin: 0 5px;
    animation: bounce 1s infinite;
}
@keyframes bounce { 0%,100%{transform:translateY(0);} 50%{transform:translateY(8px);} }

/* Badges e destaques */
.badge-highlight {
    background: #fef9c3; color: #854d0e; border-radius: 30px;
    padding: 4px 12px; font-size: 0.75rem; font-weight: 600;
    display: inline-block; margin-right: 8px;
}
.badge-pro { background: #dcfce7; color: #166534; }
.badge-ia { background: #e0f2fe; color: #0369a1; }
.badge-oms1 { background: #fee2e2; color: #b91c1c; }
.badge-oms2a { background: #ffedd5; color: #9a3412; }

/* Simulação de cardápio minimalista */
.sim-cardapio {
    background: white; border-radius: 12px; border: 1px solid #e2e8f0;
    padding: 12px; font-family: monospace; font-size: 0.8rem;
    margin: 15px 0; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.sim-cardapio .refeicao { font-weight: bold; color: #0f3460; margin-top: 8px; }
.sim-cardapio .item { margin-left: 12px; }

/* Grid de planos */
.planos-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px; margin: 20px 0;
}
.plano-card {
    border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px;
    background: white; text-align: center; transition: all 0.2s;
}
.plano-card:hover { border-color: #f59e0b; transform: scale(1.02); }
.plano-card .preco { font-size: 1.7em; font-weight: 800; color: #0f3460; }
.plano-card .nome { font-weight: 700; margin-bottom: 6px; }
.plano-card .desc { font-size: 12px; color: #64748b; }

/* Caixas de exemplo interativo (não funcional, apenas visual) */
.demo-box {
    background: #f1f5f9; border-radius: 12px; padding: 12px;
    border-left: 5px solid #f59e0b; margin: 12px 0;
    font-size: 0.85rem;
}
.demo-box code { background: #e2e8f0; padding: 2px 6px; border-radius: 6px; }
.arrow-pointer {
    position: relative;
    display: inline-block;
    animation: pointer-shake 0.8s infinite;
}
@keyframes pointer-shake {
    0% { transform: translateX(0); }
    25% { transform: translateX(5px); }
    75% { transform: translateX(-5px); }
    100% { transform: translateX(0); }
}

.rodape-portal {
    text-align: center; color: #64748b; font-size: 12px;
    margin-top: 48px; padding-top: 20px;
    border-top: 1px solid #e2e8f0;
}
</style>
"""

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL DA PÁGINA
# ══════════════════════════════════════════════════════════════════════════════
def tela_portal():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── HERO ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <h1>🏋️ BioGestão 360</h1>
        <p><strong>Plataforma completa de avaliação física, planejamento alimentar e treino</strong></p>
        <p>✅ 100% gratuita · ✅ Dados científicos · ✅ Zero-Footprint</p>
        <small>Versão 5.0 — Guia de uso interativo</small>
    </div>
    """, unsafe_allow_html=True)

    # ── INTRODUÇÃO RÁPIDA ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#eef2ff; border-radius:20px; padding:20px; margin:20px 0; text-align:center;">
        <span style="font-size:2rem;">👋</span>
        <h3>Bem‑vindo ao BioGestão 360!</h3>
        <p>Este guia mostra <strong>exatamente como usar cada recurso</strong> — da sidebar ao laudo técnico.<br>
        Siga os passos abaixo e descubra tudo o que você pode fazer.</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PASSO A PASSO VISUAL (TOUR)
    # ══════════════════════════════════════════════════════════════════════════

    # 1. SIDEBAR – PERFIL BIOLÓGICO
    with st.container():
        st.markdown("""
        <div class="tour-step">
            <div class="tour-header">
                <span class="step-num">1</span>
                <span>⚙️ Barra Lateral — Onde tudo começa</span>
            </div>
            <div class="tour-body">
                <p><span class="badge-highlight">🔑 PRIMEIRO PASSO</span> Preencha seus dados <strong>na barra lateral esquerda</strong>:
                <strong>Peso, Altura, Idade, Sexo, Objetivo e Atividade Física</strong>.</p>
                <div class="demo-box">
                    <span class="arrow-pointer">👉</span> <strong>Exemplo:</strong> Peso 70kg · Altura 170cm · Idade 30 anos · Masculino · Objetivo "Perda de peso"
                </div>
                <p>✅ Após preencher, todas as seções do app serão atualizadas com <strong>GET (gasto calórico), TMB, IMC, % gordura estimada</strong> e projeções de resultado.</p>
                <p><span class="badge-highlight">📌 DICA</span> Escolha o <strong>tipo de planejamento</strong> (Diário ou Semanal) e a <strong>tabela nutricional</strong> (BioGestão 360 / TACO / IBGE) também na sidebar.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. SEÇÃO 24 – DADOS DO PACIENTE E PROFISSIONAL + RESTRIÇÕES
    st.markdown("""
    <div class="tour-step">
        <div class="tour-header">
            <span class="step-num">2</span>
            <span>📋 Identificação da Consulta (Seção 24)</span>
        </div>
        <div class="tour-body">
            <p><span class="badge-highlight">📝 IMPORTANTE</span> Cadastre nome, telefone, e‑mail do paciente e dados do profissional (CREF/CRN).</p>
            <p><strong>⚡ Campo "Observações":</strong> informe aqui <strong>restrições alimentares, alergias ou intolerâncias</strong>.<br>
            Exemplo: <code>"alergia a camarão"</code> ou <code>"intolerância a lactose"</code> ou <code>"não pode glúten"</code>.</p>
            <div class="demo-box">
                ✅ O sistema <strong>alertará automaticamente</strong> ao adicionar alimentos que contenham o ingrediente restrito.<br>
                <span class="arrow-pointer">👇</span> O alerta aparecerá no cardápio e na tabela do importador.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. SEÇÃO 24.1 – IMPORTADOR AUTOMÁTICO DE CARDÁPIO
    st.markdown("""
    <div class="tour-step">
        <div class="tour-header">
            <span class="step-num">3</span>
            <span>📥 Importador Automático (Seção 24.1)</span>
        </div>
        <div class="tour-body">
            <p><span class="badge-highlight badge-ia">🤖 INTELIGENTE</span> Cole seu cardápio em texto puro — o sistema identifica alimentos, quantidades e busca valores nutricionais na hierarquia <strong>TACO → IBGE → BioGestão 360 → Estimativa</strong>.</p>
            <div class="sim-cardapio">
                <strong>📋 Exemplo de cardápio (diário):</strong>
                <div class="refeicao">Café da manhã:</div>
                <div class="item">• 2 fatias de pão integral · 200ml de leite desnatado</div>
                <div class="refeicao">Almoço:</div>
                <div class="item">• 100g de arroz integral · 80g de feijão · 150g de frango grelhado</div>
                <div class="refeicao">Jantar:</div>
                <div class="item">• 100g de ovos mexidos · 30g de alface</div>
            </div>
            <p>✔️ Após importar, você pode <strong>marcar/desmarcar itens</strong>, ver <strong>alertas da OMS (Grupos 1,2A,2B)</strong> e restrições alimentares, além de <strong>baixar CSV ou relatório HTML completo com gráficos</strong>.</p>
            <p><span class="badge-highlight">💡 DICA</span> Use o modo <strong>semanal</strong> para planejar 7 dias. O sistema soma totais por dia e mostra a média diária.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. SEÇÃO 25 – AVALIAÇÃO FÍSICA PROFISSIONAL
    st.markdown("""
    <div class="tour-step">
        <div class="tour-header">
            <span class="step-num">4</span>
            <span>📏 Avaliação Física (Seção 25 – Jackson & Pollock)</span>
        </div>
        <div class="tour-body">
            <p><span class="badge-highlight badge-pro">🔬 PROFISSIONAL</span> Protocolo de dobras cutâneas (3 ou 7 dobras), circunferências, handgrip e banco de Wells.</p>
            <div class="demo-box">
                <strong>📐 Exemplo de medições (adipômetro):</strong><br>
                Tríceps: 12,0mm | Peitoral: 8,5mm | Abdome: 20,2mm | Coxa: 18,0mm<br>
                <span class="arrow-pointer">➡️</span> O sistema calcula % de gordura, massa magra, classificação (Atleta/Saudável/Obesidade) e risco à saúde.
            </div>
            <p>✔️ Gera <strong>laudo completo em HTML</strong> com gráficos de composição corporal, comparativo por idade e biotipo.</p>
            <p><span class="badge-highlight">⚠️ ATENÇÃO</span> Esta seção é recomendada para profissionais de Educação Física com CREF ativo. Os resultados são mais precisos que a estimativa por IMC.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. SEÇÃO 25.1 – MONTE SEU TREINO (NOVO)
    st.markdown("""
    <div class="tour-step">
        <div class="tour-header">
            <span class="step-num">5</span>
            <span>🏋️ Monte Seu Treino (Seção 25.1 – Educação Física)</span>
        </div>
        <div class="tour-body">
            <p><span class="badge-highlight">🎯 FERRAMENTA COMPLETA</span> Crie planos de treino personalizados com:</p>
            <ul>
                <li><strong>Anamnese</strong> – condições de saúde, lesões, liberação médica, frequência cardíaca de repouso.</li>
                <li><strong>Seleção de modalidade</strong> – musculação, corrida, natação, triatlo, dança, lutas, esportes olímpicos, adaptado PCD.</li>
                <li><strong>Cálculo de calorias</strong> – baseado no MET (Compendium of Physical Activities).</li>
                <li><strong>Sugestão automática de treino</strong> – conforme nível, frequência e atividade escolhida.</li>
                <li><strong>Montagem livre</strong> – escolha grupos musculares, exercícios (120+), método de treino (15 métodos: superset, drop set, pirâmide, AMRAP…).</li>
            </ul>
            <p>✔️ Gera <strong>relatório HTML</strong> com todo o plano, alertas de contraindicações (com base nas lesões/condições) e zonas de frequência cardíaca.</p>
            <div class="demo-box">
                <span class="arrow-pointer">🎯</span> <strong>Exemplo de método:</strong> "Supino reto — 4×12 | intervalo 60s" (séries convencionais) ou "Agachamento — 3 séries piramidal: 12→10→8 reps com carga 40→50→60kg".
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. SEÇÃO 26 – MONTAGEM DO PLANO ALIMENTAR
    st.markdown("""
    <div class="tour-step">
        <div class="tour-header">
            <span class="step-num">6</span>
            <span>🍏 Plano Alimentar (Seção 26)</span>
        </div>
        <div class="tour-body">
            <p><span class="badge-highlight">🔍 BUSCA MANUAL</span> Escolha refeição, alimento (com suporte a marcas), quantidade e unidade (g/ml/un).</p>
            <p>✔️ O sistema exibe <strong>macros, micronutrientes (açúcar, saturada, trans, fibra, sódio)</strong> e alertas de risco OMS em tempo real.</p>
            <p><span class="badge-highlight">📌 REGRA DE OURO</span> Para alimentos em "unidades" (ex: biscoito, ovo, pão), informe o <strong>peso real de UMA unidade</strong> no campo "Peso Real (g/ml)" – assim o cálculo fica preciso.</p>
            <div class="demo-box">
                <span class="arrow-pointer">🍪</span> Exemplo: 1 biscoito maisena = 5g → informe Peso Real = 5g, Quantidade = 2 → total 10g.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 7. ALERTAS OMS / IARC E RELATÓRIOS
    st.markdown("""
    <div class="tour-step">
        <div class="tour-header">
            <span class="step-num">7</span>
            <span>⚠️ Alertas Científicos (OMS/IARC) e Relatórios</span>
        </div>
        <div class="tour-body">
            <p>O BioGestão 360 sinaliza automaticamente alimentos com classificação de risco pela <strong>Agência Internacional de Pesquisa sobre o Câncer (IARC/OMS)</strong>:</p>
            <ul>
                <li><span class="badge-highlight badge-oms1">🔴 GRUPO 1 – Cancerígeno confirmado</span> (carnes processadas, álcool)</li>
                <li><span class="badge-highlight badge-oms2a">🟠 GRUPO 2A – Provavelmente cancerígeno</span> (carne vermelha)</li>
                <li><span class="badge-highlight">🟣 GRUPO 2B – Possivelmente cancerígeno</span> (aspartame, bebidas >65°C)</li>
            </ul>
            <p>✔️ Todos os laudos (importador de cardápio, avaliação física, treino, plano alimentar) podem ser <strong>exportados em HTML/PDF ou CSV</strong> – botões disponíveis em cada seção.</p>
            <p><span class="badge-highlight">🖨️ IMPRESSÃO</span> Use Ctrl+P ou extensão GoFullPage para capturar a página inteira com gráficos.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 8. POLÍTICA DE PRIVACIDADE DESTACADA
    st.markdown("""
    <div class="tour-step">
        <div class="tour-header">
            <span class="step-num">8</span>
            <span>🔒 Política de Privacidade e Segurança</span>
        </div>
        <div class="tour-body">
            <p>📌 <strong>Zero‑Footprint:</strong> Todos os cálculos são processados <strong>localmente no seu navegador</strong>. Ao fechar a aba, seus dados de saúde são permanentemente deletados.</p>
            <p>🔐 <strong>Cadastro opcional:</strong> apenas nome de usuário, e‑mail e senha (hash SHA‑256) para controle de acesso às seções exclusivas (Importador, Avaliação Física).</p>
            <p>🏦 <strong>Banco de dados:</strong> PostgreSQL no Supabase com SSL obrigatório.</p>
            <p>🥦 <strong>Bases nutricionais:</strong> BioGestão 360 (Open Food Facts/ODbL) · TACO/UNICAMP 4ª Ed. · IBGE/POF 2008-2009.</p>
            <p>💳 <strong>Pagamentos:</strong> via PIX ou PayPal – o app não armazena dados bancários.</p>
            <p>📋 <strong>Licença CC BY-NC-ND 4.0:</strong> uso educacional permitido com atribuição. Proibida comercialização ou obra derivada.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PLANOS DE APOIO (mesmo estilo original)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## 💚 Apoie o projeto (colaboração voluntária)")
    st.markdown("""
    O BioGestão 360 é gratuito e sempre será. Sua contribuição ajuda a manter o servidor e evoluir o app.
    Após 2 dias de teste, você pode continuar com qualquer valor.
    """)
    st.markdown("""
    <div class="planos-grid">
        <div class="plano-card"><div class="nome">☕ Café</div><div class="preco">R$ 5</div><div class="desc">Importador 30 dias</div></div>
        <div class="plano-card"><div class="nome">🥗 Básico</div><div class="preco">R$ 15</div><div class="desc">Importador 1 ano</div></div>
        <div class="plano-card"><div class="nome">💪 Pro</div><div class="preco">R$ 10</div><div class="desc">Avaliação Física 30 dias</div></div>
        <div class="plano-card"><div class="nome">🏆 Combo Mensal</div><div class="preco">R$ 12</div><div class="desc">Importador + Avaliação 30 dias</div></div>
        <div class="plano-card"><div class="nome">🌟 Combo Anual</div><div class="preco">R$ 25</div><div class="desc">Importador + Avaliação 1 ano</div></div>
        <div class="plano-card"><div class="nome">♾️ Vitalício</div><div class="preco">R$ 49</div><div class="desc">Importador para sempre</div></div>
        <div class="plano-card"><div class="nome">🏅 Combo Vitalício</div><div class="preco">R$ 79</div><div class="desc">Importador + Avaliação para sempre</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("📱 **PIX:** f3e890da-fb72-4e8c-a0cd-d88177457a30\n\nADILSON GONCALVES XIMENES")
    with col2:
        st.info("💬 **WhatsApp:** (21) 97948-6731\n\nEnvie o comprovante para ativação em até 72h")

    # ══════════════════════════════════════════════════════════════════════════
    # RODAPÉ COM ATRIBUIÇÕES E CONTATOS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="rodape-portal">
        <strong>BioGestão 360 v5.0</strong> — Desenvolvido por Adilson Gonçalves Ximenes<br>
        Bacharel em Educação Física (2005) | Técnico em Processamento de Dados (1996)<br><br>
        🔗 Bases: BioGestão 360 (Open Food Facts/ODbL) · TACO/UNICAMP · IBGE/POF · OMS/IARC · IN 75/2020<br>
        📄 Licença CC BY-NC-ND 4.0 — uso educacional permitido com atribuição. Proibida comercialização ou obra derivada.<br>
        <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank">🔗 Texto completo da licença</a>
        &nbsp;|&nbsp;
        <a href="https://t.me/biogestao360" target="_blank">📱 Telegram</a>
        &nbsp;|&nbsp;
        <a href="https://wa.me/5521979486731" target="_blank">💬 WhatsApp</a>
        &nbsp;|&nbsp;
        <a href="mailto:adilson.ximenes@gmail.com">📧 E-mail</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(
        page_title="BioGestão 360 — Portal de Ajuda",
        page_icon="🏋️",
        layout="wide",
    )
    tela_portal()