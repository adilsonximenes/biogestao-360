"""
portal.py — BioGestão 360
===========================
Página de apresentação / landing page do app.

Como usar no app.py (multi-page Streamlit):
    Salvar como:  pages/portal.py
    Streamlit cria automaticamente o link na sidebar.

Ou chamar diretamente em qualquer seção:
    from portal import tela_portal
    tela_portal()
"""

import streamlit as st


# ── CSS ──────────────────────────────────────────────────────────────────────
_CSS = """
<style>
.hero {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 60%, #1a1a2e 100%);
    border-radius: 16px; padding: 48px 32px; color: white;
    text-align: center; margin-bottom: 32px;
}
.hero h1 { font-size: 2.6em; margin: 0 0 8px; }
.hero p  { font-size: 1.15em; opacity: 0.85; margin: 4px 0; }
.hero small { opacity: 0.6; font-size: 0.9em; }

.secao-card {
    border: 1px solid #e0e7ff; border-radius: 12px;
    padding: 22px 24px; margin-bottom: 16px;
    background: #f8faff; transition: box-shadow .2s;
}
.secao-card:hover { box-shadow: 0 4px 18px rgba(15,52,96,.10); }
.secao-card h3 { color: #0f3460; margin: 0 0 6px; font-size: 1.1em; }
.secao-card p  { color: #444; margin: 0; font-size: 0.95em; line-height: 1.6; }

.badge {
    display: inline-block; border-radius: 20px;
    padding: 2px 10px; font-size: 11px; font-weight: bold;
    margin-left: 8px; vertical-align: middle;
}
.badge-free   { background: #d4edda; color: #155724; }
.badge-acesso { background: #cce5ff; color: #004085; }
.badge-prof   { background: #fff3cd; color: #856404; }

.aviso {
    background: #fff8e1; border-left: 4px solid #ffc107;
    padding: 14px 18px; border-radius: 8px;
    margin: 20px 0; font-size: 14px; color: #555;
}
.planos-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px; margin: 20px 0;
}
.plano-card {
    border: 1px solid #ddd; border-radius: 10px;
    padding: 16px; background: white; text-align: center;
}
.plano-card .preco {
    font-size: 1.6em; font-weight: bold; color: #0f3460;
}
.plano-card .nome { font-weight: bold; margin-bottom: 4px; }
.plano-card .desc { font-size: 12px; color: #777; }
.rodape-portal {
    text-align: center; color: #888; font-size: 12px;
    margin-top: 48px; padding-top: 20px;
    border-top: 1px solid #eee;
}
</style>
"""


def tela_portal():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── HERO ─────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="hero">
    <h1>🏋️ BioGestão 360</h1>
    <p>Plataforma gratuita de organização de saúde,<br>
       atividade física e alimentação</p>
    <p><em>"A tecnologia organiza, o profissional interpreta."</em></p>
    <small>Versão 4.2 — Maio/2026</small>
</div>
""", unsafe_allow_html=True)

    # ── SOBRE ─────────────────────────────────────────────────────────────────
    st.markdown("## 💡 O que é o BioGestão 360?")
    st.markdown("""
O **BioGestão 360** é uma plataforma web desenvolvida por um **Bacharel em Educação Física**
para apoiar profissionais de saúde, estudantes e o público geral no monitoramento de
composição corporal, planejamento alimentar e atividade física.

Todos os cálculos são baseados em **equações científicas validadas** e os dados nutricionais
vêm de **três bases de referência**:

| Base | Cobertura | Uso no app |
|---|---|---|
| 🥦 **BioGestão 360** | 25.000+ produtos do mercado BR (Open Food Facts) | Produtos industrializados com marca |
| 🌿 **TACO/UNICAMP** | 613 alimentos in natura e preparações (4ª Ed.) | Frutas, verduras, preparações caseiras |
| 📊 **IBGE/POF 2008-2009** | 1.962 alimentos com 16 formas de preparo | Ovos fritos, grelhados, cozidos, etc. |
""")

    # ── SEÇÕES ───────────────────────────────────────────────────────────────
    st.markdown("## 🗂️ O que tem em cada seção")

    secoes = [
        ("free",   "📊 Bioimpedância por IMC",
         "Estima % de gordura corporal, massa magra, peso ideal e classificação IMC. "
         "Baseado em Deurenberg et al. (1991). Sem necessidade de cadastro."),
        ("free",   "🔥 Metabolismo e GET",
         "Calcula o Gasto Energético Total (GET) e Metabolismo Basal (TMB) pelos métodos "
         "Harris-Benedict (peso total) e Katch-McArdle (massa magra). "
         "Mostra projeção de perda/ganho de peso em 30 dias."),        
        ("free",   "📋 Laudo Técnico",
         "Gera laudo completo em HTML com dados do paciente, profissional, composição corporal, "
         "saldo calórico, projeções e alertas nutricionais. Exportável para impressão ou PDF."),    
        ("acesso", "📥 Seção 24.1 — Importador Automático de Cardápio",
         "Cole seu cardápio em texto e o sistema identifica os alimentos, busca os valores "
         "nutricionais automaticamente na hierarquia TACO → IBGE → BioGestão 360 → estimativa. "
         "Exporta CSV e HTML com gráficos."),
         ("prof",   "📏 Seção 25 — Avaliação Física Profissional",
         "Protocolo de dobras cutâneas Jackson & Pollock (7 dobras), circunferências, "
         "handgrip e banco de Wells. Requer acesso profissional. Exporta laudo técnico completo "
         "com classificação por gênero/idade segundo ACSM."),
         ("free",   "🏋️ Seção 25.1 — Monte Seu Treino",
         "Planejamento de atividade física com anamnese, seleção de modalidade (musculação, "
         "corrida, natação, triathlon, dança, adaptado PCD), cálculo de calorias pelo MET, "
         "sugestão automática de treino e montagem livre com 120+ exercícios e 14 métodos. "
         "Exporta relatório HTML completo."),        
        ("free",   "🍏 Seção 26 — Montagem do Plano Alimentar",
         "Monte seu plano alimentar buscando alimentos nas tabelas TACO, IBGE ou BioGestão 360. "
         "Seletor de tabela na sidebar. Seletor de marca para produtos industrializados. "
         "Alertas automáticos OMS/IARC e restrições alimentares."),
    ]

    rotulos = {
        "free":   ("🟢 Gratuito", "badge-free"),
        "acesso": ("🔵 Cadastro gratuito", "badge-acesso"),
        "prof":   ("🟡 Profissional", "badge-prof"),
    }

    for tipo, nome, desc in secoes:
        rotulo, cls = rotulos[tipo]
        st.markdown(f"""
<div class="secao-card">
    <h3>{nome} <span class="badge {cls}">{rotulo}</span></h3>
    <p>{desc}</p>
</div>
""", unsafe_allow_html=True)

    # ── PLANOS ────────────────────────────────────────────────────────────────
    st.markdown("## 💚 Colaboração Voluntária")
    st.markdown("""
O BioGestão 360 é **gratuito e sempre será**. A colaboração voluntária ajuda a manter
o servidor no ar e o projeto em evolução. Após os 2 dias gratuitos de teste, você pode
continuar com uma contribuição voluntária de qualquer valor.
""")

    st.markdown("""
<div class="planos-grid">
    <div class="plano-card">
        <div class="nome">☕ Café</div>
        <div class="preco">R$ 5</div>
        <div class="desc">Importador 30 dias</div>
    </div>
    <div class="plano-card">
        <div class="nome">🥗 Básico</div>
        <div class="preco">R$ 15</div>
        <div class="desc">Importador 1 ano</div>
    </div>
    <div class="plano-card">
        <div class="nome">💪 Pro</div>
        <div class="preco">R$ 10</div>
        <div class="desc">Avaliação Física 30 dias</div>
    </div>
    <div class="plano-card">
        <div class="nome">🏆 Combo Mensal</div>
        <div class="preco">R$ 12</div>
        <div class="desc">Importador + Avaliação 30 dias</div>
    </div>
    <div class="plano-card">
        <div class="nome">🌟 Combo Anual</div>
        <div class="preco">R$ 25</div>
        <div class="desc">Importador + Avaliação 1 ano</div>
    </div>
    <div class="plano-card">
        <div class="nome">♾️ Vitalício</div>
        <div class="preco">R$ 49</div>
        <div class="desc">Importador para sempre</div>
    </div>
    <div class="plano-card">
        <div class="nome">🏅 Combo Vitalício</div>
        <div class="preco">R$ 79</div>
        <div class="desc">Importador + Avaliação para sempre</div>
    </div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("📱 **PIX:** f3e890da-fb72-4e8c-a0cd-d88177457a30\n\nADILSON GONCALVES XIMENES")
    with col2:
        st.info("💬 **WhatsApp:** (21) 97948-6731\n\nEnvie o comprovante para ativação em até 72h")

    # ── AVISOS LEGAIS ─────────────────────────────────────────────────────────
    st.markdown("## ⚠️ Avisos Importantes")
    st.markdown("""
<div class="aviso">
<strong>Este sistema não diagnostica, não prescreve e não substitui profissionais de saúde.</strong><br><br>
❌ Não somos um consultório médico ou nutricional.<br>
❌ A seção de Avaliação Física é exclusiva para profissionais de Educação Física habilitados (CREF ativo).<br>
❌ A seção Monte Seu Treino é uma ferramenta educacional — não substitui prescrição presencial.<br>
✅ Todo profissional de Educação Física deve ter <strong>CREF ativo</strong> e <strong>SBV (Suporte Básico de Vida)</strong>.<br>
✅ Para atividades aquáticas: exija também o <strong>Curso de Socorrismo Aquático</strong>.
</div>
""", unsafe_allow_html=True)

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.link_button(
            "🔍 Consultar profissional no CREF-RJ",
            "https://cref-rj.implanta.net.br/servicosOnline/Publico/ConsultaInscritos/"
        )
    with col_l2:
        st.link_button(
            "🚨 Fazer denúncia ao CREF-RJ",
            "https://cref-rj.implanta.net.br/servicosOnline/Publico/Denuncias/"
        )
    st.caption("Para outros estados, acesse o site do CREF da sua região.")

    # ── TECNOLOGIA ────────────────────────────────────────────────────────────
    st.markdown("## 🔒 Privacidade e Segurança")
    st.markdown("""
| Item | Descrição |
|---|---|
| 🧮 Cálculos | Processados localmente no navegador |
| 🗑️ Dados de saúde | Deletados ao fechar a aba |
| 🔐 Cadastro | Nome de usuário, e-mail e senha criptografada (hash SHA-256) |
| 🏦 Banco de dados | PostgreSQL no Supabase com SSL obrigatório |
| 💳 Pagamentos | Via PIX ou PayPal — o app não armazena dados bancários |
| 🛡️ Proteção | SQL Injection bloqueado |
""")

    # ── METODOLOGIA ───────────────────────────────────────────────────────────
    st.markdown("## 🧠 Metodologia Científica")
    st.markdown("""
| Cálculo | Fórmula | Referência |
|---|---|---|
| TMB Homem | 66.47 + (13.75×P) + (5.0×A) - (6.75×I) | Harris-Benedict (1919) |
| TMB Mulher | 655.1 + (9.56×P) + (1.85×A) - (4.67×I) | Harris-Benedict (1919) |
| TMB Katch-McArdle | 370 + (21.6 × Massa Magra) | Katch-McArdle (1975) |
| GET | TMB × Fator de Atividade | WHO/FAO/UNU (1985) |
| % Gordura (IMC) | (1.20×IMC) + (0.23×I) - (16.2 H / 5.4 M) | Deurenberg et al. (1991) |
| % Gordura (Dobras) | Jackson & Pollock 7 dobras + Siri (1961) | ACSM |
| Calorias treino | MET × peso(kg) × duração(h) | Ainsworth et al. (2011) |
| Porções referência | Medidas caseiras e tamanho de porção | IN 75/2020 (Anvisa) |
""")

    # ── CONTATO ───────────────────────────────────────────────────────────────
    st.markdown("## 📱 Contato e Suporte")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button("📱 Telegram", "https://t.me/biogestao360")
    with col2:
        st.link_button("💬 WhatsApp", "https://wa.me/5521979486731")
    with col3:
        st.link_button("📧 E-mail", "mailto:adilson.ximenes@gmail.com")

    # ── RODAPÉ ────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="rodape-portal">
    <strong>BioGestão 360 v4.2</strong> — Desenvolvido por Adilson Gonçalves Ximenes<br>
    Bacharel em Educação Física (2005) | Técnico em Processamento de Dados (1996)<br><br>
    🔗 Bases de dados: BioGestão 360 (Open Food Facts/ODbL) |
    TACO/UNICAMP (4ª Ed.) | IBGE/POF 2008-2009 | OMS/IARC | IN 75/2020<br><br>
    📄 Licença: CC BY-NC-ND 4.0 — uso educacional permitido com atribuição.
    Proibida comercialização ou obra derivada.<br>
    <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank">
    Texto completo da licença</a>
</div>
""", unsafe_allow_html=True)


# ── Executar como página standalone ──────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(
        page_title="BioGestão 360 — Portal",
        page_icon="🏋️",
        layout="wide",
    )
    tela_portal()
