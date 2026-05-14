"""
portal.py — BioGestão 360
===========================
Demonstração visual interativa do app.
Mostra na prática como usar cada seção, com componentes reais do Streamlit,
setas, círculos e simulações que funcionam tanto em modo claro quanto escuro.
"""

import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
# CSS adaptado para claro/escuro (usa variáveis do Streamlit)
# ══════════════════════════════════════════════════════════════════════════════
_CSS = """
<style>
/* Garante que os cards respeitem o tema */
.demo-card {
    background: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 16px;
    margin: 12px 0;
    transition: all 0.2s;
}
.demo-card:hover {
    box-shadow: 0 6px 14px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}
.arrow {
    display: inline-block;
    font-size: 1.8rem;
    animation: bounce 0.8s infinite;
    margin: 0 8px;
}
@keyframes bounce {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(8px); }
}
.highlight {
    background: linear-gradient(120deg, #fef9c3 0%, #fef9c3 40%, transparent 60%);
    font-weight: bold;
    padding: 0 4px;
    border-radius: 6px;
}
.step-badge {
    background: #f59e0b;
    color: white;
    border-radius: 40px;
    padding: 4px 12px;
    font-size: 0.8rem;
    font-weight: bold;
    display: inline-block;
    margin-right: 12px;
}
.mock-sidebar {
    background: var(--secondary-background-color);
    border-radius: 16px;
    padding: 12px;
    border: 1px solid var(--border-color);
}
.mock-input {
    background: var(--background-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 6px 0;
    font-family: monospace;
}
.icone-grande {
    font-size: 2.2rem;
    margin-right: 12px;
}
.separator {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: 24px 0;
}
code {
    background: var(--secondary-background-color);
    padding: 2px 6px;
    border-radius: 8px;
}
</style>
"""


def tela_portal():
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── TÍTULO PRINCIPAL ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align: center; margin-bottom: 32px;">
        <span style="font-size: 3rem;">🏋️</span>
        <h1 style="margin-bottom: 0;">BioGestão 360</h1>
        <p style="font-size: 1.1rem;">Guia visual interativo – aprenda usando a própria interface</p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 1. SIDEBAR MOCK (mostra exatamente onde preencher)
    # ══════════════════════════════════════════════════════════════════════════
    with st.expander("📌 1. PREENCHA A BARRA LATERAL →", expanded=True):
        st.markdown("""
        <div class="mock-sidebar">
            <span class="step-badge">🔑 ESSENCIAL</span> 
            <strong>Todos os cálculos começam aqui!</strong>
            <div style="margin-top: 12px;">
                <div class="mock-input">⚖️ Peso Atual (kg): <span style="color:#f59e0b;">70.0</span> <span class="arrow">⬅️</span> <em>digite seu peso</em></div>
                <div class="mock-input">📏 Altura (cm): <span style="color:#f59e0b;">170</span></div>
                <div class="mock-input">🎂 Idade (anos): <span style="color:#f59e0b;">30</span></div>
                <div class="mock-input">⚥ Sexo: <span style="color:#f59e0b;">Masculino / Feminino</span> <span class="arrow">⬅️</span> clique no botão</div>
                <div class="mock-input">🎯 Objetivo: <span style="color:#f59e0b;">Perda de peso / Ganho de peso</span></div>
                <div class="mock-input">📅 Planejamento: <span style="color:#f59e0b;">Diário / Semanal</span></div>
                <div class="mock-input">🥦 Tabela nutricional: <span style="color:#f59e0b;">BioGestão 360 / TACO / IBGE</span></div>
            </div>
            <p style="margin-top: 12px; font-size: 0.85rem;">✅ Após preencher, <strong>GET, TMB, IMC e % gordura</strong> aparecem automaticamente no dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 2. SEÇÃO 24 – DADOS DO PACIENTE E RESTRIÇÕES (simulação visual)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 📋 Identificação da Consulta")
        st.markdown("**Campos que você vai preencher:**")
        st.markdown("- Nome do paciente")
        st.markdown("- Telefone / E-mail")
        st.markdown("- Profissional (CREF/CRN)")
        st.markdown("- Clínica")
        st.markdown("- Datas de início e retorno")
    with col2:
        st.info(
            "⚠️ **Campo OBSERVAÇÕES – RESTRIÇÕES ALIMENTARES**\n\n"
            "Escreva aqui alergias ou intolerâncias. Exemplo:\n"
            "`alergia a camarão`, `não pode glúten`, `intolerância à lactose`.\n\n"
            "O sistema alertará automaticamente ao adicionar alimentos com esses ingredientes."
        )
        st.markdown(
            "<div class='demo-card'><span class='arrow'>👇</span> <strong>Exemplo real no cardápio:</strong> "
            "Se você adicionar 'pão francês' com restrição de glúten, aparecerá um alerta vermelho.</div>",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 3. SEÇÃO 24.1 – IMPORTADOR AUTOMÁTICO (demonstração com exemplo)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 📥 Importador Automático de Cardápio")
    st.markdown("Cole o cardápio em texto → o sistema identifica tudo e busca valores nutricionais.")

    # Exemplo interativo (apenas visual, mas com text_area real para copiar)
    with st.expander("📋 Clique para ver um exemplo prático", expanded=False):
        st.code(
            """Segunda:
Café da manhã: 2 fatias de pão integral, 200ml de leite desnatado
Almoço: 150g de frango grelhado, 100g de arroz integral, 80g de feijão
Jantar: 100g de ovos mexidos, 30g de alface""",
            language="text",
        )
        st.caption("⬆️ Copie esse exemplo, cole no campo de texto e clique em 'Importar Cardápio'.")
        st.markdown(
            "<div class='demo-card'>✅ <strong>Resultado:</strong> Você verá uma tabela editável, com colunas Kcal, Proteínas, Carboidratos, Gorduras, "
            "além de alertas OMS (Grupo 1,2A,2B) e restrições alimentares. Pode exportar CSV ou HTML com gráficos.</div>",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 4. SEÇÃO 25 – AVALIAÇÃO FÍSICA (simulação de medições)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 📏 Avaliação Física Profissional")
    st.markdown("Protocolo Jackson & Pollock (dobras cutâneas, circunferências, handgrip, wells)")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            """
            <div class="demo-card">
                <span class="icone-grande">📐</span>
                <strong>Exemplo de medições (adipômetro):</strong><br>
                Tríceps: 12,0 mm<br>
                Peitoral: 8,5 mm<br>
                Abdome: 20,2 mm<br>
                Coxa: 18,0 mm<br>
                <span class="arrow">➡️</span> O sistema calcula % de gordura, massa magra e classificação.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            """
            <div class="demo-card">
                <span class="icone-grande">💪</span>
                <strong>Circunferências e força:</strong><br>
                Cintura: 82 cm<br>
                Quadril: 96 cm → RCQ = 0,85<br>
                Handgrip: 42 kg/f → força normal<br>
                <span class="arrow">➡️</span> Laudo completo com gráficos de composição e comparação por idade.
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.info(
        "🔬 **Para profissionais de Educação Física:** exija CREF ativo. "
        "Os resultados são mais precisos que a bioimpedância de balança."
    )

    # ══════════════════════════════════════════════════════════════════════════
    # 5. SEÇÃO 25.1 – MONTE SEU TREINO (simulação de seleção)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 🏋️ Monte Seu Treino")
    st.markdown("Crie planos personalizados com anamnese, modalidade, MET e métodos avançados.")

    # Simula uma pequena parte da interface de treino (apenas visual)
    with st.expander("🎮 Veja como funciona (demonstração)", expanded=False):
        st.selectbox("Categoria:", ["🏋️ Academia / Musculação", "🏃 Cardiovascular", "🏊 Aquáticas"], key="demo_cat")
        st.selectbox("Atividade:", ["Musculação moderada (pesos livres)", "Corrida moderada (10 km/h)"], key="demo_act")
        st.number_input("Duração (minutos):", 30, key="demo_dur")
        st.metric("🔥 Calorias estimadas por sessão", "245 kcal", delta="baseado no MET")
        st.markdown(
            "<div class='demo-card'>✅ Após configurar, você pode escolher <strong>sugestão automática</strong> ou <strong>montagem livre</strong> "
            "com mais de 120 exercícios e 15 métodos (superset, drop set, pirâmide, AMRAP...). Relatório HTML completo.</div>",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 6. SEÇÃO 26 – PLANO ALIMENTAR (busca manual)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 🍏 Montagem do Plano Alimentar (busca manual)")
    st.markdown("Adicione alimentos um a um, com escolha de marca, quantidade e unidade.")

    # Simula os campos reais da seção 26
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Refeição:", ["Café da Manhã", "Almoço", "Lanches", "Jantar"], key="demo_ref")
        st.selectbox("Alimento:", ["Frango grelhado", "Arroz integral", "Feijão carioca"], key="demo_alim")
    with col2:
        st.number_input("Quantidade:", 1.0, key="demo_qtd")
        st.selectbox("Unidade:", ["g", "ml", "un"], key="demo_un")
    st.button("➕ Adicionar ao Plano (demonstração)", key="demo_add", disabled=True, help="Apenas exemplo – funcional no app real")
    st.markdown(
        "<div class='demo-card'><span class='arrow'>⚠️</span> <strong>Regra de ouro:</strong> Para 'unidades', informe o peso real de uma unidade (ex: 1 biscoito = 5g). "
        "Assim o cálculo fica preciso. O sistema alerta sobre alimentos OMS Grupo 1/2A/2B e restrições alimentares.</div>",
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # 7. ALERTAS OMS E RELATÓRIOS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### ⚠️ Alertas Científicos (IARC/OMS) e Relatórios")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="demo-card">
            <span class="icone-grande">🔴</span> <strong>Grupo 1 – Cancerígeno confirmado</strong><br>
            Carnes processadas, bebidas alcoólicas
        </div>
        <div class="demo-card">
            <span class="icone-grande">🟠</span> <strong>Grupo 2A – Provavelmente cancerígeno</strong><br>
            Carne vermelha (acima de 500g/semana)
        </div>
        <div class="demo-card">
            <span class="icone-grande">🟣</span> <strong>Grupo 2B – Possivelmente cancerígeno</strong><br>
            Aspartame, bebidas >65°C
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="demo-card">
            <span class="icone-grande">📄</span> <strong>Exportação de laudos</strong><br>
            • Cardápio importado → CSV / HTML com gráficos<br>
            • Avaliação física → laudo técnico completo<br>
            • Plano de treino → relatório com zonas de FC<br>
            • Plano alimentar → resumo em CSV
        </div>
        <div class="demo-card">
            <span class="icone-grande">🖨️</span> <strong>Impressão / PDF</strong><br>
            Use Ctrl+P ou extensão GoFullPage para capturar toda a página com gráficos.
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 8. POLÍTICA DE PRIVACIDADE (em formato resumido e atraente)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    with st.expander("🔒 Política de Privacidade e Segurança (clique para expandir)", expanded=False):
        st.markdown("""
        - **Zero-Footprint:** cálculos processados localmente. Ao fechar a aba, seus dados de saúde são deletados.
        - **Cadastro opcional:** apenas nome de usuário, e-mail e senha criptografada (hash SHA-256) para controle de acesso às seções exclusivas.
        - **Banco de dados:** PostgreSQL no Supabase com SSL obrigatório.
        - **Bases nutricionais:** BioGestão 360 (Open Food Facts/ODbL) · TACO/UNICAMP 4ª Ed. · IBGE/POF 2008-2009.
        - **Pagamentos via PIX ou PayPal** – o app não armazena dados bancários.
        - **Licença CC BY-NC-ND 4.0** – uso educacional permitido com atribuição. Proibida comercialização ou obra derivada.
        """)

    # ══════════════════════════════════════════════════════════════════════════
    # 9. PLANOS DE APOIO (mantido)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("## 💚 Colaboração voluntária")
    st.markdown("O BioGestão 360 é gratuito e sempre será. Sua ajuda mantém o servidor no ar.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📱 **PIX:** f3e890da-fb72-4e8c-a0cd-d88177457a30")
    with col2:
        st.info("💬 **WhatsApp:** (21) 97948-6731")
    with col3:
        st.info("📧 **E-mail:** adilson.ximenes@gmail.com")

    # Rodapé simples
    st.markdown(
        "<div style='text-align: center; margin-top: 32px; font-size: 0.8rem; opacity: 0.7;'>"
        "BioGestão 360 v5.0 – Use o menu à esquerda para navegar entre as seções reais do app.</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.set_page_config(page_title="BioGestão 360 – Guia Visual", layout="wide")
    tela_portal()