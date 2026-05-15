"""
portal.py — BioGestão 360 v4.2
================================
Landing page interativa com guia visual passo a passo.
"""

import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
# CSS COMPLETO
# ══════════════════════════════════════════════════════════════════════════════
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── VARIÁVEIS: MODO CLARO (padrão) ── */
:root {
  --azul:       #0f3460;
  --azul2:      #16213e;
  --azul3:      #1a1a2e;
  --ouro:       #e69500;
  --verde:      #16a34a;
  --vermelho:   #ef4444;
  --roxo:       #8b5cf6;
  --cinza:      #64748b;
  --ouro-bg:    rgba(230,149,0,.15);
  --ouro-border:rgba(230,149,0,.4);

  /* Cards e superfícies — modo claro */
  --card-bg:    #ffffff;
  --card-borda: #e2e8f0;
  --field-bg:   #f1f5f9;
  --field-txt:  #475569;
  --body-txt:   #1e293b;
  --txt-sec:    #475569;
  --sep-color:  #e2e8f0;
  --nota-bg:    #fefce8;
  --nota-txt:   #854d0e;
  --nota-borda: #e69500;
  --priv-bg:    #0f172a;
  --priv-txt:   #e2e8f0;
  --step-h3:    #0f3460;
  --step-p:     #374151;
  --treino-bg:  #f0fdf4;
  --treino-brd: #86efac;
  --treino-txt: #166534;
  --treino-ex:  #374151;
  --oms1-bg:    #fef2f2;
  --oms2a-bg:   #fffbeb;
  --oms2b-bg:   #f5f3ff;
  --oms-ttl:    #1e293b;
  --oms-ex:     #475569;
  --sc-success-bg:  #dcfce7;
  --sc-success-brd: #86efac;
  --sc-success-txt: #166534;
  --sc-warn-bg:     #fef3c7;
  --sc-warn-brd:    #fcd34d;
  --sc-warn-txt:    #92400e;
  --sc-td-brd:  #e2e8f0;
  --sc-td-txt:  #334155;
  --sc-tr-alt:  #f8faff;
  --licenca-bg: #fafafa;
  --plano-bg:   #ffffff;
  --plano-brd:  #e2e8f0;
  --plano-txt:  #64748b;
}

/* ── VARIÁVEIS: MODO ESCURO ── */
@media (prefers-color-scheme: dark) {
  :root {
    --ouro:       #f5a623;
    --verde:      #22c55e;
    --ouro-bg:    rgba(245,166,35,.18);
    --ouro-border:rgba(245,166,35,.5);

    --card-bg:    #1e293b;
    --card-borda: #334155;
    --field-bg:   #0f172a;
    --field-txt:  #94a3b8;
    --body-txt:   #e2e8f0;
    --txt-sec:    #94a3b8;
    --sep-color:  #334155;
    --nota-bg:    #1c1200;
    --nota-txt:   #fbbf24;
    --nota-borda: #f5a623;
    --priv-bg:    #0a0f1e;
    --priv-txt:   #e2e8f0;
    --step-h3:    #93c5fd;
    --step-p:     #94a3b8;
    --treino-bg:  #052e16;
    --treino-brd: #166534;
    --treino-txt: #86efac;
    --treino-ex:  #cbd5e1;
    --oms1-bg:    #2d0a0a;
    --oms2a-bg:   #2d1800;
    --oms2b-bg:   #1a0a2e;
    --oms-ttl:    #e2e8f0;
    --oms-ex:     #94a3b8;
    --sc-success-bg:  #052e16;
    --sc-success-brd: #166534;
    --sc-success-txt: #86efac;
    --sc-warn-bg:     #2d1800;
    --sc-warn-brd:    #92400e;
    --sc-warn-txt:    #fbbf24;
    --sc-td-brd:  #334155;
    --sc-td-txt:  #cbd5e1;
    --sc-tr-alt:  #1e293b;
    --licenca-bg: #0f172a;
    --plano-bg:   #1e293b;
    --plano-brd:  #334155;
    --plano-txt:  #94a3b8;
  }
}

* { font-family: 'Sora', sans-serif; box-sizing: border-box; }

/* ── HERO — sempre escuro (contexto próprio) ── */
.hero {
  background: linear-gradient(135deg, #0f3460 0%, #16213e 55%, #1a1a2e 100%);
  border-radius: 20px; padding: 56px 32px 48px; color: white;
  text-align: center; margin-bottom: 48px; position: relative; overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 70% 20%, rgba(245,166,35,.12) 0%, transparent 60%),
              radial-gradient(ellipse at 20% 80%, rgba(34,197,94,.08) 0%, transparent 50%);
  pointer-events: none;
}
.hero h1 { font-size: 3em; font-weight: 800; margin: 0 0 10px; letter-spacing: -1px; }
.hero .sub { font-size: 1.2em; opacity: .85; margin: 6px 0; }
.hero .tag {
  display: inline-block; background: var(--ouro-bg); border: 1px solid var(--ouro-border);
  color: var(--ouro); border-radius: 30px; padding: 6px 18px; font-size: 13px; margin-top: 18px;
}
.hero-badges { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 24px; }
.hero-badge {
  background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.2);
  border-radius: 30px; padding: 8px 16px; font-size: 13px; color: white;
}

/* ── STEP CARDS ── */
.step-wrap { display: flex; gap: 16px; align-items: flex-start; margin-bottom: 32px; flex-wrap: wrap; }
.step-num {
  background: linear-gradient(135deg, var(--azul), var(--azul2));
  color: var(--ouro); font-size: 1.6em; font-weight: 800;
  border-radius: 50%; width: 54px; height: 54px; min-width: 54px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 16px rgba(15,52,96,.4);
}
.step-body { flex: 1; min-width: 220px; }
.step-body h3 { color: var(--step-h3); margin: 0 0 6px; font-size: 1.05em; font-weight: 700; }
.step-body p  { color: var(--step-p); margin: 0; font-size: .92em; line-height: 1.6; }

/* ── SETA ANIMADA ── */
.arrow-down {
  text-align: center; font-size: 28px; color: var(--ouro);
  animation: bounce 1.4s infinite; margin: 8px 0;
}
@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(8px)} }

/* ── MOCKUP SIDEBAR — sempre escuro (é simulação do app) ── */
.sidebar-mock {
  background: #1e293b; border-radius: 14px; padding: 20px;
  color: white; font-size: 13px; max-width: 320px;
  box-shadow: 0 8px 32px rgba(0,0,0,.35); border: 1px solid rgba(255,255,255,.08);
}
.sidebar-mock .sb-title { color: var(--ouro); font-weight: 700; font-size: 14px; margin-bottom: 12px; }
.sidebar-mock .sb-field {
  background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.15);
  border-radius: 8px; padding: 8px 12px; margin-bottom: 8px;
  color: #cbd5e1; font-size: 12px;
}
.sidebar-mock .sb-btn {
  background: var(--azul); color: white; border-radius: 8px;
  padding: 8px 14px; font-size: 12px; display: inline-block;
  margin: 4px 4px 4px 0; font-weight: 600;
}
.sidebar-mock .sb-btn.sel { background: #16a34a; }
.sidebar-mock .sb-sep { border-top: 1px solid rgba(255,255,255,.1); margin: 12px 0; }
.sidebar-mock .sb-caption { color: #64748b; font-size: 11px; margin-top: 4px; }

/* ── POINTER ── */
.pointer {
  display: inline-block; background: var(--ouro); color: #000;
  border-radius: 6px; padding: 4px 10px; font-size: 12px; font-weight: 700;
  position: relative; margin-left: 12px;
}
.pointer::before {
  content: '◀'; position: absolute; left: -14px; top: 50%;
  transform: translateY(-50%); color: var(--ouro); font-size: 14px;
}

/* ── SCREEN MOCK — responde ao tema ── */
.screen-mock {
  background: var(--card-bg); border-radius: 14px; padding: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,.15); border: 2px solid var(--card-borda);
  font-size: 13px; color: var(--body-txt);
}
.screen-mock .sc-header {
  background: linear-gradient(90deg, var(--azul), var(--azul2));
  color: white; border-radius: 8px; padding: 10px 14px;
  font-weight: 700; margin-bottom: 14px; font-size: 14px;
}
.screen-mock .sc-row { display: flex; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }
.screen-mock .sc-field {
  flex: 1; min-width: 100px; background: var(--field-bg);
  border: 1px solid var(--card-borda); border-radius: 8px;
  padding: 8px 10px; font-size: 12px; color: var(--field-txt);
}
.screen-mock .sc-btn {
  background: var(--azul); color: white; border-radius: 8px;
  padding: 8px 14px; font-size: 12px; font-weight: 600;
  display: inline-block; margin-top: 8px;
}
.screen-mock .sc-success {
  background: var(--sc-success-bg); border: 1px solid var(--sc-success-brd);
  border-radius: 8px; padding: 8px 12px; color: var(--sc-success-txt);
  font-size: 12px; margin-top: 8px;
}
.screen-mock .sc-warn {
  background: var(--sc-warn-bg); border: 1px solid var(--sc-warn-brd);
  border-radius: 8px; padding: 8px 12px; color: var(--sc-warn-txt);
  font-size: 12px; margin-top: 8px;
}
/* OMS — sempre colorido independente do tema */
.screen-mock .sc-oms1  { background: #dc2626; color: white; border-radius: 8px; padding: 8px 12px; font-size: 11px; margin-top: 6px; }
.screen-mock .sc-oms2a { background: #d97706; color: white; border-radius: 8px; padding: 8px 12px; font-size: 11px; margin-top: 6px; }
.screen-mock .sc-oms2b { background: #7c3aed; color: white; border-radius: 8px; padding: 8px 12px; font-size: 11px; margin-top: 6px; }
.screen-mock .sc-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.screen-mock .sc-table th { background: var(--azul); color: white; padding: 6px 8px; text-align: left; }
.screen-mock .sc-table td { padding: 5px 8px; border-bottom: 1px solid var(--sc-td-brd); color: var(--sc-td-txt); }
.screen-mock .sc-table tr:nth-child(even) td { background: var(--sc-tr-alt); }

/* ── METRICS ── */
.metrics-row { display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0; }
.metric-box {
  background: linear-gradient(135deg, var(--azul), var(--azul2));
  color: white; border-radius: 10px; padding: 12px 16px; flex: 1; min-width: 90px; text-align: center;
}
.metric-box .mv { font-size: 1.3em; font-weight: 800; color: var(--ouro); }
.metric-box .ml { font-size: 10px; opacity: .8; margin-top: 2px; }

/* ── TREINO BLOCK ── */
.treino-block {
  background: var(--treino-bg); border: 1px solid var(--treino-brd);
  border-radius: 10px; padding: 14px; margin-top: 10px; font-size: 12px;
}
.treino-block .tb-title { color: var(--treino-txt); font-weight: 700; margin-bottom: 8px; font-size: 13px; }
.treino-block .tb-ex    { color: var(--treino-ex); padding: 3px 0; }
.treino-block .tb-ex.riscado { text-decoration: line-through; color: #ef4444; opacity: .7; }
.treino-block .tb-warn  { color: #ef4444; font-size: 11px; font-weight: 600; }

/* ── LAUDO MOCK — sempre escuro (contexto próprio) ── */
.laudo-mock {
  background: linear-gradient(135deg, #0f3460, #16213e);
  border-radius: 14px; padding: 20px; color: white; font-size: 12px;
  box-shadow: 0 8px 32px rgba(15,52,96,.5);
}
.laudo-mock .lm-title { color: var(--ouro); font-weight: 800; font-size: 16px; margin-bottom: 14px; }
.laudo-mock .lm-row   { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 8px; }
.laudo-mock .lm-card  { background: rgba(255,255,255,.1); border-radius: 8px; padding: 10px 14px; flex: 1; min-width: 110px; text-align: center; }
.laudo-mock .lm-val   { font-size: 1.4em; font-weight: 800; color: var(--ouro); }
.laudo-mock .lm-lbl   { font-size: 10px; opacity: .75; margin-top: 2px; }
.laudo-mock .lm-btn   { background: var(--ouro); color: #000; border-radius: 8px; padding: 10px 20px; font-weight: 700; text-align: center; margin-top: 14px; display: inline-block; font-size: 13px; }

/* ── SECTION BADGE ── */
.sec-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--azul); color: white; border-radius: 30px;
  padding: 8px 18px; font-size: 13px; font-weight: 700; margin-bottom: 18px;
}
.sec-badge .sb-num {
  background: var(--ouro); color: #000; border-radius: 50%;
  width: 24px; height: 24px; display: flex; align-items: center;
  justify-content: center; font-weight: 800; font-size: 13px;
}

/* ── PRIVACIDADE ── */
.priv-box {
  background: var(--priv-bg); color: var(--priv-txt); border-radius: 14px;
  padding: 28px; border: 1px solid var(--ouro-border);
}
.priv-box h3   { color: var(--ouro); font-size: 1.1em; margin-bottom: 16px; }
.priv-item     { display: flex; gap: 12px; margin-bottom: 12px; align-items: flex-start; }
.priv-icon     { font-size: 1.2em; min-width: 24px; }
.priv-text     { font-size: 13px; line-height: 1.6; color: var(--priv-txt); }

/* ── OMS CARDS — cores fixas (semântico) + fundo adaptável ── */
.oms-grid { display: flex; gap: 12px; flex-wrap: wrap; margin: 12px 0; }
.oms-card { flex: 1; min-width: 200px; border-radius: 12px; padding: 16px; }
.oms-card.g1  { background: var(--oms1-bg);  border: 2px solid #ef4444; }
.oms-card.g2a { background: var(--oms2a-bg); border: 2px solid #f59e0b; }
.oms-card.g2b { background: var(--oms2b-bg); border: 2px solid #8b5cf6; }
.oms-card .oc-badge { display: inline-block; border-radius: 20px; padding: 4px 12px; font-size: 11px; font-weight: 800; margin-bottom: 8px; }
.oms-card.g1  .oc-badge { background: #ef4444; color: white; }
.oms-card.g2a .oc-badge { background: #f59e0b; color: white; }
.oms-card.g2b .oc-badge { background: #8b5cf6; color: white; }
.oms-card .oc-title { font-weight: 700; color: var(--oms-ttl); margin-bottom: 6px; font-size: 13px; }
.oms-card .oc-ex    { color: var(--oms-ex); font-size: 12px; line-height: 1.5; }

/* ── RODAPÉ — sempre escuro ── */
.rodape-final {
  background: linear-gradient(135deg, #0f3460, #1a1a2e);
  border-radius: 14px; padding: 32px; color: white; text-align: center; margin-top: 48px;
}
.rodape-final h3 { color: var(--ouro); font-size: 1.2em; margin-bottom: 16px; }
.rodape-final p  { color: #94a3b8; font-size: 13px; line-height: 1.7; }

/* ── SEPARADOR ── */
.sep { border: none; border-top: 2px solid var(--sep-color); margin: 40px 0; }

/* ── NOTA LATERAL ── */
.nota {
  background: var(--nota-bg); border-left: 4px solid var(--nota-borda);
  border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 12px 0;
  font-size: 13px; color: var(--nota-txt);
}

/* ── LICENÇA ── */
.licenca {
  background: var(--licenca-bg); border: 1px solid var(--card-borda); border-radius: 10px;
  padding: 16px 20px; font-size: 12px; color: var(--txt-sec); line-height: 1.8;
  padding: 16px 20px; font-size: 12px; color: #475569; line-height: 1.8;
}

/* ── RESPONSIVO ── */
@media (max-width: 700px) {
  .hero h1 { font-size: 2em; }
  .step-wrap { flex-direction: column; }
  .metrics-row, .oms-grid, .lm-row, .sc-row { flex-direction: column; }
}
</style>
"""

# ══════════════════════════════════════════════════════════════════════════════
# PORTAL PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
def tela_portal():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── HERO ─────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="hero">
  <div class="hero-badges">
    <span class="hero-badge">🏋️ Educação Física</span>
    <span class="hero-badge">🥗 Nutrição</span>
    <span class="hero-badge">📊 Dados Científicos</span>
    <span class="hero-badge">💻 Python / Streamlit</span>
  </div>
  <h1>🏋️ BioGestão 360</h1>
  <p class="sub">Plataforma gratuita de saúde, atividade física e alimentação</p>
  <p class="sub"><em>"A tecnologia organiza, o profissional interpreta."</em></p>
  <span class="tag">✅ 100% Gratuito · Científico · Feito por Ed. Física</span>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PASSO 0 — SIDEBAR
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("## 🚀 Como usar — Guia Passo a Passo")
    st.markdown("""
<div class="nota">
  💡 <strong>Antes de tudo:</strong> a sidebar (barra lateral esquerda) é onde você 
  configura tudo. No celular, toque no <strong>≡</strong> no canto superior esquerdo para abrir.
  No computador ela já aparece visível.
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
<div class="step-wrap">
  <div class="step-num">0</div>
  <div class="step-body">
    <h3>⬅️ Abra a Sidebar primeiro!</h3>
    <p>A sidebar é o painel de controle do app. 
    Ela fica à esquerda — se não aparecer, clique na seta 
    <strong>◀ ▶</strong> ou no ícone <strong>≡</strong> no topo.</p>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="step-wrap" style="margin-top:16px">
  <div class="step-num">1</div>
  <div class="step-body">
    <h3>👤 Preencha seu Perfil Biológico</h3>
    <p>Peso, altura, idade e sexo são necessários para calcular 
    IMC, % gordura, TMB e GET automaticamente.</p>
  </div>
</div>
""", unsafe_allow_html=True)

        # ── Login e Cadastro ──────────────────────────────────────────────────
        st.markdown("""
<div class="step-wrap" style="margin-top:16px">
  <div class="step-num">🔐</div>
  <div class="step-body">
    <h3>Login — Acesso ao sistema</h3>
    <p>Role a sidebar para baixo. Informe seu 
    <strong>usuário</strong> e <strong>senha</strong>, 
    responda a conta de somar anti-bot e clique em 
    <strong>Entrar</strong>.</p>
  </div>
</div>
<div class="step-wrap" style="margin-top:12px">
  <div class="step-num">🆕</div>
  <div class="step-body">
    <h3>Cadastro — 2 dias grátis</h3>
    <p>Clique em <strong>🆕 Cadastre-se (2 dias grátis)</strong>. 
    Preencha: <strong>usuário</strong>, <strong>e-mail</strong>, 
    <strong>senha</strong>, <strong>confirmar senha</strong> — 
    responda a conta de somar e clique em 
    <strong>Cadastrar</strong>. Acesso ativado imediatamente.</p>
  </div>
</div>
<div class="step-wrap" style="margin-top:12px">
  <div class="step-num">🤖</div>
  <div class="step-body">
    <h3>Verificação anti-bot</h3>
    <p>Uma conta simples aparece em ambos os formulários — 
    ex: <em>"Quanto é 7 + 3?"</em>. 
    Digite o número correto. Isso protege o sistema contra 
    bots automatizados.</p>
  </div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="sidebar-mock">
  <div class="sb-title">👤 Perfil Biológico</div>
  <div class="sb-field">📊 Peso Atual (kg) &nbsp;&nbsp;&nbsp; <strong style="color:#f5a623">85.0</strong></div>
  <div class="sb-field">📏 Altura (cm) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong style="color:#f5a623">164</strong></div>
  <div class="sb-field">🎂 Idade (anos) &nbsp;&nbsp;&nbsp;&nbsp; <strong style="color:#f5a623">47</strong></div>
  <div style="font-size:12px;color:#94a3b8;margin-bottom:6px">⚥ Sexo Biológico</div>
  <div>
    <span class="sb-btn sel">👨 Homem ✅</span>
    <span class="sb-btn">👩 Mulher</span>
  </div>
  <div class="sb-sep"></div>
  <div class="sb-title">🎯 Objetivos</div>
  <div class="sb-field">🎯 Objetivo: <strong style="color:#22c55e">Perda de peso</strong></div>
  <div class="sb-field">🎯 Meta: <strong style="color:#f5a623">65.0 kg</strong></div>
  <div class="sb-field">🏃 Atividade: <strong style="color:#f5a623">Moderado (3-5 dias/sem)</strong></div>
  <div class="sb-sep"></div>
  <div class="sb-title">📅 Tipo de Planejamento</div>
  <div>
    <span class="sb-btn">Diário</span>
    <span class="sb-btn sel">Semanal ✅</span>
  </div>
  <div class="sb-sep"></div>
  <div class="sb-title">📊 Fonte Nutricional</div>
  <div>
    <span class="sb-btn sel">🥦 BioGestão ✅</span>
  </div>
  <div class="sb-caption">25 mil+ produtos reais do mercado BR</div>
  <div class="sb-sep"></div>
  <div class="sb-btn" style="width:100%;text-align:center;background:#1e40af">🏋️ Como funciona cada seção</div>
  <div class="sb-sep"></div>
  <div class="sb-title">🔐 Acesso ao Sistema</div>
  <div class="sb-field">👤 Usuário &nbsp; <strong style="color:#f5a623">joao_silva</strong></div>
  <div class="sb-field">🔒 Senha &nbsp;&nbsp;&nbsp; <strong style="color:#f5a623">••••••••</strong></div>
  <div style="background:rgba(245,166,35,.12);border:1px solid rgba(245,166,35,.35);border-radius:8px;padding:8px;margin:6px 0;font-size:11px">
    <div style="color:#f5a623;font-weight:700;margin-bottom:4px">🤖 Anti-bot: Quanto é <strong style="color:white">7 + 3</strong>?</div>
    <div class="sb-field">Resposta: <strong style="color:#22c55e">10 ✅</strong></div>
  </div>
  <div class="sb-btn" style="width:100%;text-align:center;margin-bottom:6px">Entrar</div>
  <div class="sb-btn" style="background:#166534;width:100%;text-align:center">🆕 Cadastre-se (2 dias grátis)</div>
  <div class="sb-sep"></div>
  <div style="font-size:10px;color:#94a3b8;text-align:center">
    Cadastro: usuário · e-mail · senha · confirmar senha<br>
    + verificação anti-bot → clique em <strong style="color:#22c55e">Cadastrar</strong>
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO 24 — DADOS DO PACIENTE
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-badge">
  <span class="sb-num">24</span>
  📋 Identificação da Consulta — Dados do Paciente e Profissional
  <span style="background:#d4edda;color:#155724;border-radius:20px;padding:3px 10px;font-size:11px;margin-left:8px">🟢 Gratuito</span>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
<div class="step-wrap">
  <div class="step-num">2</div>
  <div class="step-body">
    <h3>🩺 Preencha os dados da consulta</h3>
    <p>Nome do paciente, data de nascimento, profissional responsável, 
    clínica e datas de início/retorno. Essas informações aparecem 
    no laudo HTML exportado.</p>
  </div>
</div>

<div class="step-wrap" style="margin-top:16px">
  <div class="step-num">3</div>
  <div class="step-body">
    <h3>⚠️ Restrições alimentares — campo poderoso</h3>
    <p>No campo <strong>"Observações"</strong> escreva restrições como: 
    <em>"alergia a glúten"</em>, <em>"intolerância à lactose"</em>, 
    <em>"alergia a amendoim"</em>. O sistema alerta automaticamente 
    sempre que o alimento restrito aparecer no cardápio.</p>
  </div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="screen-mock">
  <div class="sc-header">📋 Seção 24 — Identificação da Consulta</div>
  <div class="sc-row">
    <div class="sc-field">👤 Nome do paciente<br><strong>Adilson G. Ximenes</strong></div>
    <div class="sc-field">📅 Data nasc.<br><strong>15/03/1978</strong></div>
  </div>
  <div class="sc-row">
    <div class="sc-field">👨‍⚕️ Profissional<br><strong>Dr. João Silva</strong></div>
    <div class="sc-field">🏥 Clínica<br><strong>NutriSaúde</strong></div>
  </div>
  <div class="sc-field" style="margin-top:8px">
    📝 Observações / Restrições alimentares:<br>
    <strong style="color:#ef4444">Intolerância à lactose, alergia a amendoim</strong>
  </div>
  <div class="sc-warn" style="margin-top:10px">
    ⚠️ <strong>Alerta automático ativo:</strong> O sistema vai destacar 
    automaticamente alimentos com lactose e amendoim em todo o cardápio.
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO 24.1 — IMPORTADOR
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-badge">
  <span class="sb-num">24.1</span>
  📥 Importador Automático de Cardápio
  <span style="background:#cce5ff;color:#004085;border-radius:20px;padding:3px 10px;font-size:11px;margin-left:8px">🔵 Cadastro gratuito</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="step-wrap">
  <div class="step-num">4</div>
  <div class="step-body">
    <h3>📋 Cole seu cardápio em texto</h3>
    <p>Escreva o cardápio no formato abaixo, clique em 
    <strong>📥 Importar Cardápio</strong> e o sistema identifica 
    automaticamente cada alimento, busca os valores nutricionais 
    nas bases TACO → IBGE → BioGestão 360 e preenche a tabela inteira.</p>
  </div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
<div class="screen-mock">
  <div class="sc-header">📥 Importador Automático</div>
  <div style="background:#f8faff;border:1px dashed #94a3b8;border-radius:8px;padding:12px;font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;line-height:1.7">
    Segunda:<br>
    Café da manhã: 150g ovo de galinha mexido,<br>
    &nbsp;&nbsp;1 pão francês, 250ml café infusão sem açúcar<br>
    Almoço: 200g arroz branco cozido, 100g feijão<br>
    &nbsp;&nbsp;carioca cozido, 250g frango grelhado,<br>
    &nbsp;&nbsp;100g brócolis cozido<br>
    Jantar: 250g filé de tilápia grelhado,<br>
    &nbsp;&nbsp;100g cenoura cozida
  </div>
  <div class="sc-btn" style="margin-top:10px">📥 Importar Cardápio</div>
  <div class="sc-success">✅ 7 alimentos importados — valores da TACO e IBGE aplicados</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="screen-mock">
  <div class="sc-header">📊 Resultado da Importação</div>
  <table class="sc-table">
    <tr><th>Alimento</th><th>Qtd</th><th>kcal</th><th>Fonte</th><th>Alerta</th></tr>
    <tr><td>Ovo mexido</td><td>150g</td><td>219</td>
        <td><span style="background:#d4edda;color:#155724;border-radius:4px;padding:1px 6px;font-size:10px">TACO</span></td>
        <td>—</td></tr>
    <tr><td>Pão francês</td><td>1 un</td><td>150</td>
        <td><span style="background:#d4edda;color:#155724;border-radius:4px;padding:1px 6px;font-size:10px">TACO</span></td>
        <td>—</td></tr>
    <tr><td>Frango grelhado</td><td>250g</td><td>397</td>
        <td><span style="background:#cce5ff;color:#004085;border-radius:4px;padding:1px 6px;font-size:10px">Bio</span></td>
        <td>—</td></tr>
    <tr><td>Arroz cozido</td><td>200g</td><td>256</td>
        <td><span style="background:#d4edda;color:#155724;border-radius:4px;padding:1px 6px;font-size:10px">TACO</span></td>
        <td>—</td></tr>
    <tr><td>Presunto cozido</td><td>40g</td><td>90</td>
        <td><span style="background:#cce5ff;color:#004085;border-radius:4px;padding:1px 6px;font-size:10px">IBGE</span></td>
        <td><span style="background:#ef4444;color:white;border-radius:4px;padding:1px 6px;font-size:10px">🔴 G1</span></td></tr>
  </table>
  <div class="sc-oms1" style="margin-top:10px">
    🔴 <strong>GRUPO 1 OMS:</strong> Presunto cozido é carne processada — 
    cancerígeno confirmado (IARC). Recomendação: evitar ou reduzir.
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO 25 — AVALIAÇÃO FÍSICA
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-badge">
  <span class="sb-num">25</span>
  📏 Avaliação Física Profissional
  <span style="background:#fff3cd;color:#856404;border-radius:20px;padding:3px 10px;font-size:11px;margin-left:8px">🟡 Profissional CREF</span>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
<div class="step-wrap">
  <div class="step-num">5</div>
  <div class="step-body">
    <h3>📐 Insira as dobras cutâneas</h3>
    <p>Protocolo <strong>Jackson & Pollock 7 dobras</strong>. 
    Insira cada medida em mm (3 medições por dobra — o app calcula a média). 
    Também aceita circunferências, handgrip e banco de Wells.</p>
  </div>
</div>
<div class="nota" style="margin-top:16px">
  ⚠️ <strong>Exclusivo para profissionais</strong> com CREF ativo. 
  O laudo gerado tem validade técnica e pode ser assinado pelo profissional responsável.
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="screen-mock">
  <div class="sc-header">📏 Dobras Cutâneas — Jackson & Pollock 7</div>
  <div style="font-size:11px;color:#475569;margin-bottom:8px">
    3 medições por dobra • média calculada automaticamente
  </div>
  <div class="sc-row">
    <div class="sc-field">Peitoral<br><strong>18 mm</strong></div>
    <div class="sc-field">Axilar<br><strong>20 mm</strong></div>
    <div class="sc-field">Tríceps<br><strong>22 mm</strong></div>
    <div class="sc-field">Subescap.<br><strong>25 mm</strong></div>
  </div>
  <div class="sc-row">
    <div class="sc-field">Abdominal<br><strong>32 mm</strong></div>
    <div class="sc-field">Supra-ilíaca<br><strong>28 mm</strong></div>
    <div class="sc-field">Coxa<br><strong>24 mm</strong></div>
  </div>
  <div class="metrics-row" style="margin-top:10px">
    <div class="metric-box"><div class="mv">25.7%</div><div class="ml">% Gordura</div></div>
    <div class="metric-box"><div class="mv">63.2kg</div><div class="ml">Massa Magra</div></div>
    <div class="metric-box"><div class="mv">21.8kg</div><div class="ml">Massa Gorda</div></div>
  </div>
  <div class="sc-success" style="margin-top:8px">
    Classificação ACSM (Masc. 46-55 anos): <strong>Aceitável</strong>
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO 25.1 — MONTE SEU TREINO
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-badge">
  <span class="sb-num">25.1</span>
  🏋️ Monte Seu Treino — 49 Planos Automáticos
  <span style="background:#d4edda;color:#155724;border-radius:20px;padding:3px 10px;font-size:11px;margin-left:8px">🟢 Gratuito</span>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
<div class="step-wrap">
  <div class="step-num">6</div>
  <div class="step-body">
    <h3>🩺 Preencha a Anamnese Física</h3>
    <p>Nível (iniciante → atleta), frequência semanal, objetivo, 
    <strong>condições de saúde</strong> e lesões. O sistema usa 
    essas informações para filtrar exercícios contraindicados.</p>
  </div>
</div>
<div class="step-wrap" style="margin-top:16px">
  <div class="step-num">7</div>
  <div class="step-body">
    <h3>⚡ Plano automático + exercícios riscados</h3>
    <p>O sistema gera o plano ideal para seu perfil. 
    Se você tem <strong>lombalgia crônica</strong>, 
    o agachamento com barra aparece riscado automaticamente 
    com o motivo clínico explicado.</p>
  </div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="screen-mock">
  <div class="sc-header">🏋️ Sugestão Automática — Triathlon Avançado 6x</div>
  <div class="treino-block">
    <div class="tb-title">Natação + Corrida (Seg)</div>
    <div class="tb-ex">🏊 Natação: 400m aquec. → 6×100m crawl → 200m recupero</div>
    <div class="tb-ex">🏃 Corrida (transição): 15-20 min ritmo de prova</div>
  </div>
  <div class="treino-block" style="margin-top:8px">
    <div class="tb-title">🦴 Musculação Funcional (Ter) — Condição: Lombalgia</div>
    <div class="tb-ex">Remada curvada — 4×10</div>
    <div class="tb-ex">Supino — 3×10</div>
    <div class="tb-ex riscado">Agachamento livre — 4×8</div>
    <div class="tb-warn">⛔ Contraindicado — Lombalgia crônica: evitar carga axial na coluna</div>
    <div class="tb-ex riscado">Levantamento terra — 4×5</div>
    <div class="tb-warn">⛔ Contraindicado — Lombalgia crônica</div>
    <div class="tb-ex">Prancha + Rotação de tronco — 3×45s ✅</div>
    <div class="tb-ex">Dead bug (core estabilizador) — 3×12 ✅</div>
  </div>
  <div class="sc-success" style="margin-top:8px">
    🔥 Calorias queimadas: <strong>892 kcal/sessão</strong> | 
    <strong>5.352 kcal/semana</strong>
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SEÇÃO 26 — MONTAGEM DO PLANO ALIMENTAR
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("""
<div class="sec-badge">
  <span class="sb-num">26</span>
  🍏 Montagem do Plano Alimentar
  <span style="background:#d4edda;color:#155724;border-radius:20px;padding:3px 10px;font-size:11px;margin-left:8px">🟢 Gratuito</span>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
<div class="step-wrap">
  <div class="step-num">8</div>
  <div class="step-body">
    <h3>🔍 Busque o alimento e escolha a tabela</h3>
    <p>Selecione a fonte na sidebar: <strong>BioGestão 360</strong> 
    (25 mil produtos), <strong>TACO/UNICAMP</strong> (in natura) 
    ou <strong>IBGE/POF</strong> (com formas de preparo). 
    Para cada alimento o sistema sugere marca e porção.</p>
  </div>
</div>
<div class="step-wrap" style="margin-top:16px">
  <div class="step-num">9</div>
  <div class="step-body">
    <h3>➕ Adicione e visualize o balanço</h3>
    <p>Escolha refeição, quantidade e unidade (g, ml ou unidades). 
    O sistema calcula automaticamente kcal, proteínas, carboidratos, 
    gorduras, sódio e alertas OMS/IARC.</p>
  </div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="screen-mock">
  <div class="sc-header">🍏 Seção 26 — Adicionar Alimento</div>
  <div class="sc-row">
    <div class="sc-field">🍽️ Refeição<br><strong>Almoço</strong></div>
    <div class="sc-field">🔍 Alimento<br><strong>Frango grelhado</strong></div>
  </div>
  <div class="sc-row">
    <div class="sc-field">🏷️ Marca<br><strong>(qualquer marca)</strong></div>
  </div>
  <div class="sc-row">
    <div class="sc-field">Quantidade<br><strong>250</strong></div>
    <div class="sc-field">Unidade<br><strong>g</strong></div>
  </div>
  <div class="sc-btn">➕ Adicionar ao Plano</div>
  <div style="margin-top:12px;font-size:12px;font-weight:600;color:var(--txt-sec)">
    🔥 Resultado adicionado:
  </div>
  <div class="sc-success" style="margin-top:6px">
    <strong style="color:var(--body-txt)">Frango grelhado</strong> 
    <span style="color:var(--txt-sec)">· 250g</span><br>
    🔥 <strong>397 kcal</strong> &nbsp;
    🥩 <strong>80g prot</strong> &nbsp;
    🍞 <strong>0g carb</strong> &nbsp;
    🥑 <strong>9g gord</strong><br>
    🧂 Sódio: <strong>74mg</strong> &nbsp; 
    Fonte: <span style="background:var(--azul);color:white;border-radius:4px;padding:1px 6px;font-size:10px">BioGestão</span>
  </div>
  <div class="metrics-row" style="margin-top:10px">
    <div class="metric-box"><div class="mv">1.847</div><div class="ml">kcal hoje</div></div>
    <div class="metric-box"><div class="mv">+1.151</div><div class="ml">déficit vs GET</div></div>
    <div class="metric-box"><div class="mv">32%</div><div class="ml">proteínas</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # LAUDOS HTML
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("## 📄 Laudos HTML — O que é gerado")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
<div class="laudo-mock">
  <div class="lm-title">🏋️ BioGestão 360 — Laudo Nutricional</div>
  <div style="color:#94a3b8;font-size:11px;margin-bottom:12px">
    Dr. João Silva · CRN 12345 · NutriSaúde · 14/05/2026
  </div>
  <div class="lm-row">
    <div class="lm-card"><div class="lm-val">31.6</div><div class="lm-lbl">IMC</div></div>
    <div class="lm-card"><div class="lm-val">25.7%</div><div class="lm-lbl">% Gordura</div></div>
    <div class="lm-card"><div class="lm-val">63.2kg</div><div class="lm-lbl">Massa Magra</div></div>
    <div class="lm-card"><div class="lm-val">2.998</div><div class="lm-lbl">GET kcal</div></div>
  </div>
  <div style="background:rgba(34,197,94,.15);border:1px solid rgba(34,197,94,.4);border-radius:8px;padding:10px;margin-top:10px;font-size:12px">
    📉 Projeção 30 dias: <strong style="color:#22c55e">-3.9 kg</strong> de gordura<br>
    ⏱️ Tempo estimado meta: <strong style="color:#f5a623">16 semanas</strong>
  </div>
  <div class="lm-btn">⬇️ Baixar Laudo HTML</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="step-wrap" style="margin-bottom:20px">
  <div class="step-num">💡</div>
  <div class="step-body">
    <h3>Como baixar e imprimir</h3>
    <p>Clique no botão de <strong>exportar HTML ou CSV</strong> na seção desejada. 
    Para imprimir: abra o arquivo HTML no navegador → 
    <strong>Ctrl+P</strong> → Salvar como PDF.</p>
  </div>
</div>
<div class="nota">
  💡 <strong>Dica:</strong> Use a extensão 
  <strong>GoFullPage</strong> no Chrome para capturar a página inteira 
  do app em uma imagem ou PDF sem precisar exportar.
</div>
<div class="nota" style="background:#eff6ff;border-color:#3b82f6;color:#1e40af;margin-top:12px">
  🖨️ <strong>Imprimir o app:</strong> Clique nos 3 pontinhos ⋮ no topo direito 
  → <strong>Imprimir</strong> → Salvar como PDF.
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ALERTAS OMS/IARC
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("## ⚠️ Alertas OMS/IARC — Como funciona")

    st.markdown("""
<div class="nota">
  O sistema verifica automaticamente <strong>todos</strong> os alimentos adicionados 
  ao cardápio e sinaliza os que têm classificação de risco pela 
  <strong>Agência Internacional de Pesquisa em Câncer (IARC/OMS)</strong>.
</div>
<div class="oms-grid">
  <div class="oms-card g1">
    <span class="oc-badge">🔴 GRUPO 1</span>
    <div class="oc-title">Cancerígeno confirmado</div>
    <div class="oc-ex">
      <strong>Exemplos:</strong> salsicha, bacon, presunto, salame, mortadela, 
      linguiça, nuggets, embutidos em geral, bebidas alcoólicas.<br><br>
      <strong>Recomendação:</strong> Evitar ou reduzir ao máximo.
      50g/dia aumenta 18% o risco de câncer colorretal (IARC, 2015).
    </div>
  </div>
  <div class="oms-card g2a">
    <span class="oc-badge">🟠 GRUPO 2A</span>
    <div class="oc-title">Provavelmente cancerígeno</div>
    <div class="oc-ex">
      <strong>Exemplos:</strong> carne bovina, suína, cordeiro, bife grelhado, 
      carne moída.<br><br>
      <strong>Recomendação:</strong> Limitar a <strong>500g/semana</strong> 
      (carne vermelha total). Preferir métodos de preparo mais suaves.
    </div>
  </div>
  <div class="oms-card g2b">
    <span class="oc-badge">🟣 GRUPO 2B</span>
    <div class="oc-title">Possivelmente cancerígeno</div>
    <div class="oc-ex">
      <strong>Exemplos:</strong> aspartame (adoçante diet/zero), 
      acrilamida (biscoitos, torradas queimadas), 
      bebidas muito quentes (>65°C).<br><br>
      <strong>Recomendação:</strong> Consumo moderado e consciente.
    </div>
  </div>
</div>
<div class="nota" style="margin-top:12px">
  ✅ <strong>Importante:</strong> O alerta é baseado na 
  <strong>composição e processamento</strong> do alimento — não apenas no nome. 
  "Patê de frango" dispara Grupo 1 porque é processado, 
  mas "frango grelhado" não dispara. 
  "Café com leite" <strong>não</strong> dispara alerta (falso positivo corrigido).
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # POLÍTICA DE PRIVACIDADE
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("## 🔒 Política de Privacidade — Leia com Atenção")

    st.markdown("""
<div class="priv-box">
  <h3>🔒 POLÍTICA DE PRIVACIDADE — BioGestão 360</h3>
  <div class="priv-item">
    <span class="priv-icon">🧮</span>
    <span class="priv-text"><strong style="color:#f5a623">Cálculos locais:</strong> 
    Todos os cálculos de IMC, TMB, GET, % gordura e composição corporal são processados 
    diretamente no seu navegador. Nenhum dado de saúde é enviado a servidores.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">🗑️</span>
    <span class="priv-text"><strong style="color:#f5a623">Dados temporários:</strong> 
    Ao fechar a aba do navegador, todos os seus dados de saúde são 
    <strong>permanentemente deletados</strong>. O app não guarda histórico de consultas.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">🔐</span>
    <span class="priv-text"><strong style="color:#f5a623">Cadastro opcional:</strong> 
    O cadastro só é necessário para o Importador Automático e a Avaliação Física. 
    Armazenamos apenas: nome de usuário, e-mail e senha criptografada (hash SHA-256). 
    <strong>Nunca</strong> armazenamos dados de saúde do paciente.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">🏦</span>
    <span class="priv-text"><strong style="color:#f5a623">Banco de dados:</strong> 
    PostgreSQL hospedado no Supabase com SSL obrigatório e criptografia em repouso. 
    SQL Injection bloqueado em todas as queries.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">💳</span>
    <span class="priv-text"><strong style="color:#f5a623">Pagamentos:</strong> 
    Realizados exclusivamente via PIX ou PayPal. O app não armazena 
    nenhum dado bancário ou de cartão.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">🥦</span>
    <span class="priv-text"><strong style="color:#f5a623">Bases nutricionais:</strong> 
    Open Food Facts (ODbL) · TACO/UNICAMP (4ª Ed.) · IBGE/POF 2008-2009 · 
    IN 75/2020 (Anvisa). Dados públicos com atribuição obrigatória.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">📋</span>
    <span class="priv-text"><strong style="color:#f5a623">Seus direitos:</strong> 
    Solicite exclusão completa da sua conta a qualquer momento pelo 
    WhatsApp <strong>(21) 97948-6731</strong>. Resposta em até 72h.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">📄</span>
    <span class="priv-text"><strong style="color:#f5a623">Licença CC BY-NC-ND 4.0:</strong> 
    Este software é protegido por direitos autorais. Uso educacional permitido com atribuição. 
    É <strong>terminantemente proibida</strong> a comercialização ou criação de obras derivadas 
    para distribuição ou venda.</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # COLABORAÇÃO
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("## 💚 Colaboração Voluntária")
    st.markdown("""
O BioGestão 360 é **gratuito e sempre será**. 
A colaboração voluntária ajuda a manter o servidor e o projeto em evolução.
""")

    st.markdown("""
<style>
.planos-3d {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(148px, 1fr));
  gap: 16px; margin: 20px 0;
}
.card-3d {
  background: var(--plano-bg);
  border: 1px solid var(--plano-brd);
  border-radius: 14px;
  padding: 20px 12px 16px;
  text-align: center;
  position: relative;
  /* Efeito 3D: borda inferior + sombra lateral */
  box-shadow:
    0 6px 0 0 var(--plano-brd),
    0 8px 20px rgba(0,0,0,.10);
  transition: transform .18s ease, box-shadow .18s ease;
  cursor: default;
}
.card-3d:hover {
  transform: translateY(-5px);
  box-shadow:
    0 11px 0 0 var(--plano-brd),
    0 16px 32px rgba(15,52,96,.18);
}
.card-3d.ouro {
  border-color: var(--ouro);
  box-shadow:
    0 6px 0 0 var(--ouro),
    0 8px 20px rgba(230,149,0,.20);
}
.card-3d.ouro:hover {
  box-shadow:
    0 11px 0 0 var(--ouro),
    0 16px 32px rgba(230,149,0,.28);
}
.card-3d .c-emoji { font-size: 2em; margin-bottom: 8px; display: block; }
.card-3d .c-nome  { font-weight: 700; font-size: 13px; color: var(--body-txt); margin-bottom: 6px; }
.card-3d .c-preco {
  font-size: 1.7em; font-weight: 800;
  color: var(--azul); line-height: 1;
}
.card-3d.ouro .c-preco { color: var(--ouro); }
.card-3d .c-desc  { font-size: 11px; color: var(--txt-sec); margin-top: 6px; line-height: 1.4; }
.card-3d .c-tag {
  position: absolute; top: -10px; left: 50%; transform: translateX(-50%);
  background: var(--ouro); color: #000; font-size: 10px; font-weight: 800;
  border-radius: 20px; padding: 2px 10px; white-space: nowrap;
}
</style>
<div class="planos-3d">
  <div class="card-3d">
    <span class="c-emoji">☕</span>
    <div class="c-nome">Café</div>
    <div class="c-preco">R$ 5</div>
    <div class="c-desc">Importador<br>30 dias</div>
  </div>
  <div class="card-3d">
    <span class="c-emoji">🥗</span>
    <div class="c-nome">Básico</div>
    <div class="c-preco">R$ 15</div>
    <div class="c-desc">Importador<br>1 ano</div>
  </div>
  <div class="card-3d">
    <span class="c-emoji">💪</span>
    <div class="c-nome">Pro</div>
    <div class="c-preco">R$ 10</div>
    <div class="c-desc">Avaliação Física<br>30 dias</div>
  </div>
  <div class="card-3d">
    <span class="c-emoji">🏆</span>
    <div class="c-nome">Combo Mensal</div>
    <div class="c-preco">R$ 12</div>
    <div class="c-desc">Importador + Avaliação<br>30 dias</div>
  </div>
  <div class="card-3d">
    <span class="c-emoji">🌟</span>
    <div class="c-nome">Combo Anual</div>
    <div class="c-preco">R$ 25</div>
    <div class="c-desc">Importador + Avaliação<br>1 ano</div>
  </div>
  <div class="card-3d ouro">
    <span class="c-tag">⭐ Popular</span>
    <span class="c-emoji">♾️</span>
    <div class="c-nome">Vitalício</div>
    <div class="c-preco">R$ 49</div>
    <div class="c-desc">Importador<br>para sempre</div>
  </div>
  <div class="card-3d ouro">
    <span class="c-tag">🏆 Melhor valor</span>
    <span class="c-emoji">🏅</span>
    <div class="c-nome">Combo Vitalício</div>
    <div class="c-preco">R$ 79</div>
    <div class="c-desc">Importador + Avaliação<br>para sempre</div>
  </div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("📱 **PIX:** f3e890da-fb72-4e8c-a0cd-d88177457a30\n\n**ADILSON GONCALVES XIMENES**")
    with col2:
        st.info("💬 **WhatsApp:** (21) 97948-6731\n\nEnvie o comprovante — ativação em até 72h")

    # ══════════════════════════════════════════════════════════════════════════
    # AVISOS LEGAIS + LINKS CREF
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
    st.markdown("## ⚠️ Avisos de Segurança e Responsabilidade")

    st.markdown("""
<div class="priv-box" style="border-color:rgba(239,68,68,.4)">
  <h3 style="color:#ef4444">⚠️ Este sistema NÃO substitui profissionais de saúde</h3>
  <div class="priv-item">
    <span class="priv-icon">❌</span>
    <span class="priv-text">Não diagnosticamos doenças, não prescrevemos dietas nem tratamentos médicos.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">❌</span>
    <span class="priv-text">A seção de Avaliação Física é exclusiva para 
    <strong style="color:#f5a623">Bacharéis em Educação Física com CREF ativo</strong>.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">✅</span>
    <span class="priv-text">Todo profissional de Educação Física deve ter 
    <strong style="color:#f5a623">CREF ativo</strong> + 
    <strong style="color:#f5a623">SBV (Suporte Básico de Vida / BLS)</strong> — 
    certificação obrigatória que capacita para RCP e uso do DEA.</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">🏊</span>
    <span class="priv-text">Para atividades aquáticas: exija também o 
    <strong style="color:#f5a623">Curso de Primeiros Socorros e Salvamento Aquático</strong> 
    (exigido pelo CREF para supervisão em piscinas).</span>
  </div>
  <div class="priv-item">
    <span class="priv-icon">🚨</span>
    <span class="priv-text"><strong style="color:#ef4444">Pare imediatamente</strong> 
    se sentir: dor no peito · falta de ar intensa · tontura · 
    batimentos irregulares · visão turva.</span>
  </div>
</div>
""", unsafe_allow_html=True)

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.link_button("🔍 Consultar profissional no CREF-RJ",
                       "https://cref-rj.implanta.net.br/servicosOnline/Publico/ConsultaInscritos/")
    with col_l2:
        st.link_button("🚨 Denúncia ao CREF-RJ",
                       "https://cref-rj.implanta.net.br/servicosOnline/Publico/Denuncias/")
    st.caption("Para outros estados acesse o site do CREF da sua região.")

    # ══════════════════════════════════════════════════════════════════════════
    # RODAPÉ
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
<div class="rodape-final">
  <h3>🏋️ BioGestão 360 v4.2</h3>
  <p>
    Desenvolvido por <strong style="color:#f5a623">Adilson Gonçalves Ximenes</strong><br>
    Bacharel em Educação Física (2005) · Técnico em Processamento de Dados (1996)
  </p>
  <p>
    🔗 <strong>Bases de dados:</strong> BioGestão 360 (Open Food Facts/ODbL) · 
    TACO/UNICAMP (4ª Ed.) · IBGE/POF 2008-2009 · OMS/IARC · IN 75/2020 (Anvisa)<br>
    📐 <strong>Metodologia:</strong> Harris-Benedict (1919) · Katch-McArdle (1975) · 
    Deurenberg et al. (1991) · Jackson & Pollock (1978) · Siri (1961) · 
    Ainsworth et al. (2011) · ACSM · NSCA
  </p>
  <p>
    📄 <strong>Licença:</strong> CC BY-NC-ND 4.0 — uso educacional permitido com atribuição · 
    <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" 
       target="_blank" style="color:#f5a623">Texto completo</a>
  </p>
  <p style="margin-top:16px">
    📱 <a href="https://t.me/biogestao360" target="_blank" style="color:#f5a623">t.me/biogestao360</a> &nbsp;·&nbsp;
    💬 <a href="https://wa.me/5521979486731" target="_blank" style="color:#f5a623">(21) 97948-6731</a> &nbsp;·&nbsp;
    📧 <a href="mailto:adilson.ximenes@gmail.com" style="color:#f5a623">adilson.ximenes@gmail.com</a>
  </p>
</div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(
        page_title="BioGestão 360 — Guia Completo",
        page_icon="🏋️",
        layout="wide",
    )
    tela_portal()
