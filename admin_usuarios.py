# admin_usuarios.py
# Página de gerenciamento de usuários — acesso exclusivo do admin
# Execute separadamente: streamlit run admin_usuarios.py --server.port 8502

import streamlit as st
import psycopg2
import hashlib
import pyotp
import qrcode
import io
import secrets as secrets_lib
from datetime import datetime, timedelta
from PIL import Image

# Importa as funções do database.py que já existem
from database import (
    get_connection,
    verificar_senha_admin,
    buscar_admin,
    configurar_2fa_admin,
    salvar_codigos_recuperacao,
    verificar_codigo_recuperacao,
    listar_usuarios,
    atualizar_plano,
    alterar_senha_usuario,
    ativar_desativar_usuario,
    deletar_usuario,
    gerar_codigo_acesso,
)

st.set_page_config(
    page_title="BioGestão 360 — Gestão de Usuários", page_icon="👑", layout="wide"
)

# ============================================
# INICIALIZAÇÃO DOS ESTADOS DE AUTENTICAÇÃO
# ============================================
if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False
if "admin_senha_ok" not in st.session_state:
    st.session_state.admin_senha_ok = False
if "admin_2fa_pendente" not in st.session_state:
    st.session_state.admin_2fa_pendente = False
if "admin_2fa_secret_temp" not in st.session_state:
    st.session_state.admin_2fa_secret_temp = None
if "admin_id_temp" not in st.session_state:
    st.session_state.admin_id_temp = None
if "msg_senha_alterada" not in st.session_state:
    st.session_state.msg_senha_alterada = None

# ============================================
# ETAPA 1 — FORMULÁRIO DE SENHA
# ============================================
if not st.session_state.admin_autenticado and not st.session_state.admin_senha_ok:
    st.title("👑 BioGestão 360 — Gestão de Usuários")
    st.markdown("### 🔐 Acesso restrito ao Administrador")

    # Exibir mensagem de sucesso de troca de senha se houver
    if st.session_state.msg_senha_alterada:
        st.success(st.session_state.msg_senha_alterada)
        st.session_state.msg_senha_alterada = None

    with st.form("admin_login_senha"):
        senha = st.text_input("🔒 Senha do Administrador", type="password")
        if st.form_submit_button("Continuar", use_container_width=True):
            if not senha:
                st.error("Digite a senha")
            elif verificar_senha_admin(senha):
                admin_info = buscar_admin()
                if admin_info and admin_info.get("google_2fa_secret"):
                    # Tem 2FA — guarda o secret e avança para etapa 2
                    st.session_state.admin_senha_ok = True
                    st.session_state.admin_2fa_secret_temp = admin_info["google_2fa_secret"]
                    st.session_state.admin_id_temp = admin_info["id"]
                    st.rerun()
                else:
                    # Sem 2FA — acesso direto
                    st.session_state.admin_autenticado = True
                    st.session_state.admin_senha_ok = False
                    st.rerun()
            else:
                st.error("❌ Senha incorreta!")

    st.caption("⚠️ Esqueceu a senha? Execute `reset_admin.py` na pasta do projeto.")
    st.stop()

# ============================================
# ETAPA 2 — VERIFICAÇÃO 2FA (só chega aqui se senha OK e 2FA configurado)
# ============================================
if st.session_state.admin_senha_ok and not st.session_state.admin_autenticado:
    st.title("👑 BioGestão 360 — Gestão de Usuários")
    st.markdown("### 📱 Verificação de Dois Fatores")
    st.info("Senha verificada ✅ — Digite agora o código do autenticador ou um código de recuperação.")

    with st.form("admin_form_2fa"):
        codigo_2fa = st.text_input(
            "Código do Google Authenticator (6 dígitos) ou código de recuperação",
            max_chars=20,
            placeholder="000000",
        )
        usar_recuperacao = st.checkbox("Usar código de recuperação")
        if st.form_submit_button("Verificar", use_container_width=True):
            if not codigo_2fa:
                st.error("Digite o código")
            elif usar_recuperacao:
                # Tenta código de recuperação
                if verificar_codigo_recuperacao(st.session_state.admin_id_temp, codigo_2fa):
                    st.session_state.admin_autenticado = True
                    st.session_state.admin_senha_ok = False
                    st.success("✅ Acesso com código de recuperação!")
                    st.rerun()
                else:
                    st.error("❌ Código de recuperação inválido ou já usado!")
            else:
                totp = pyotp.TOTP(st.session_state.admin_2fa_secret_temp)
                if totp.verify(codigo_2fa):
                    st.session_state.admin_autenticado = True
                    st.session_state.admin_senha_ok = False
                    st.success("✅ Acesso concedido!")
                    st.rerun()
                else:
                    st.error("❌ Código 2FA inválido! Verifique o app.")

    if st.button("← Voltar", key="btn_voltar_2fa"):
        st.session_state.admin_senha_ok = False
        st.rerun()
    st.stop()

# ============================================
# PAINEL AUTENTICADO (ADMIN)
# ============================================
st.title("👑 BioGestão 360 — Gestão de Usuários")

# Botão sair na sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Sair", use_container_width=True):
    st.session_state.admin_autenticado = False
    st.session_state.admin_senha_ok = False
    st.rerun()

# Exibir dados do admin logado
admin = buscar_admin()
if admin:
    st.sidebar.markdown(f"👑 **Admin:** {admin['username']}")
    if admin.get("google_2fa_secret"):
        st.sidebar.success("✅ 2FA ativo")
    else:
        st.sidebar.warning("⚠️ 2FA não configurado")

# Tabs principais (igual ao seu código original)
tab_usuarios, tab_codigos, tab_stats = st.tabs(
    ["👥 Usuários", "🔑 Gerar Códigos", "📊 Estatísticas"]
)

# ══════════════════════════════
# TAB 1 — USUÁRIOS
# ══════════════════════════════
with tab_usuarios:
    usuarios = listar_usuarios()
    comuns = [u for u in usuarios if u["role"] != "admin"]

    st.markdown(f"**Total de apoiadores:** {len(comuns)}")

    # Filtros (simplificados, mantendo seu estilo anterior)
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_nome = st.text_input("🔍 Buscar por nome/email", "")
    with col_f2:
        filtro_status = st.selectbox("Status", ["Todos", "Ativos", "Inativos"])
    with col_f3:
        filtro_plano = st.selectbox(
            "Plano IA", ["Todos", "2dias", "30dias", "1ano", "vitalicio"]
        )

    # Aplicar filtros
    filtrados = comuns
    if filtro_nome:
        fn = filtro_nome.lower()
        filtrados = [u for u in filtrados if fn in u["username"].lower() or fn in u["email"].lower()]
    if filtro_status == "Ativos":
        filtrados = [u for u in filtrados if u["ativo"] == 1]
    elif filtro_status == "Inativos":
        filtrados = [u for u in filtrados if u["ativo"] == 0]
    if filtro_plano != "Todos":
        filtrados = [u for u in filtrados if u["plano_ia"] == filtro_plano]

    st.markdown(f"**Exibindo:** {len(filtrados)} usuário(s)")
    st.markdown("---")

    for u in filtrados:
        status_icon = "🟢" if u["ativo"] == 1 else "🔴"
        with st.expander(
            f"{status_icon} **{u['username']}** | {u['email']} | "
            f"Importador: {u['plano_ia']} | Avaliação: {u['plano_avaliacao']}"
        ):
            col_info, col_acoes = st.columns([2, 3])

            with col_info:
                st.markdown(f"**ID:** {u['id']}")
                st.markdown(f"**Cadastro:** {u.get('created_at', '-')}")
                st.markdown(f"**Sessões máx:** {u['max_sessoes']}")
                st.markdown(
                    f"**Importador expira:** "
                    f"{u['acesso_ia_until'].strftime('%d/%m/%Y %H:%M') if u['acesso_ia_until'] else 'N/A'}"
                )
                st.markdown(
                    f"**Avaliação expira:** "
                    f"{u['acesso_avaliacao_until'].strftime('%d/%m/%Y %H:%M') if u['acesso_avaliacao_until'] else 'N/A'}"
                )

            with col_acoes:
                st.markdown("#### ✏️ Ações")
                tabs_acao = st.tabs(["📋 Plano", "🔐 Senha", "⚙️ Status"])

                # Aba Plano
                with tabs_acao[0]:
                    tipo_plano = st.selectbox(
                        "Tipo",
                        ["ia", "avaliacao", "combo"],
                        key=f"tipo_{u['id']}",
                        format_func=lambda x: {
                            "ia": "📋 Importador",
                            "avaliacao": "📏 Avaliação",
                            "combo": "🏆 Combo (ambos)",
                        }[x],
                    )
                    plano_sel = st.selectbox(
                        "Plano",
                        ["2dias", "30dias", "1ano", "vitalicio"],
                        key=f"plano_{u['id']}",
                    )
                    sessoes_sel = st.number_input(
                        "Sessões simultâneas",
                        min_value=1,
                        max_value=3,
                        value=u["max_sessoes"],
                        key=f"sess_{u['id']}",
                    )
                    dias_map = {"2dias": 2, "30dias": 30, "1ano": 365, "vitalicio": 36500}
                    if st.button("💾 Salvar plano", key=f"sv_{u['id']}", use_container_width=True):
                        if tipo_plano == "combo":
                            # Atualiza ambos os planos
                            atualizar_plano(u["id"], "ia", plano_sel, dias_map[plano_sel], sessoes_sel)
                            atualizar_plano(u["id"], "avaliacao", plano_sel, dias_map[plano_sel], sessoes_sel)
                        else:
                            atualizar_plano(u["id"], tipo_plano, plano_sel, dias_map[plano_sel], sessoes_sel)
                        st.success(f"✅ Plano de {u['username']} atualizado!")
                        st.rerun()

                # Aba Senha
                with tabs_acao[1]:
                    nova_s = st.text_input("Nova senha", type="password", key=f"ns_{u['id']}")
                    conf_s = st.text_input("Confirmar senha", type="password", key=f"cs_{u['id']}")
                    if st.button("🔐 Alterar senha", key=f"as_{u['id']}", use_container_width=True):
                        if not nova_s:
                            st.error("Digite a nova senha")
                        elif nova_s != conf_s:
                            st.error("Senhas não conferem")
                        elif len(nova_s) < 4:
                            st.error("Mínimo 4 caracteres")
                        else:
                            alterar_senha_usuario(u["id"], nova_s)
                            st.success(f"✅ Senha de {u['username']} alterada!")

                # Aba Status
                with tabs_acao[2]:
                    if u["ativo"] == 1:
                        if st.button("🔴 Desativar usuário", key=f"da_{u['id']}", use_container_width=True):
                            ativar_desativar_usuario(u["id"], 0)
                            st.success(f"{u['username']} desativado!")
                            st.rerun()
                    else:
                        if st.button("🟢 Ativar usuário", key=f"at_{u['id']}", use_container_width=True):
                            ativar_desativar_usuario(u["id"], 1)
                            st.success(f"{u['username']} ativado!")
                            st.rerun()

                    st.markdown("---")
                    if st.button("🗑️ Deletar usuário", key=f"del_{u['id']}", use_container_width=True, type="secondary"):
                        deletar_usuario(u["id"])
                        st.success(f"{u['username']} removido!")
                        st.rerun()

# ══════════════════════════════
# TAB 2 — GERAR CÓDIGOS
# ══════════════════════════════
with tab_codigos:
    st.markdown("### 🔑 Gerar Códigos de Ativação")
    st.info(
        "Gere um código após confirmar o PIX do apoiador. "
        "Cada código é único e de uso único. "
        "Envie pelo WhatsApp para o apoiador ativar no app."
    )

    col_c1, col_c2, col_c3 = st.columns(3)

    with col_c1:
        st.markdown("#### 📋 Importador")
        p_ia = st.selectbox("Plano", ["2dias", "30dias", "1ano", "vitalicio"], key="gen_p_ia")
        s_ia = st.number_input("Sessões", min_value=1, max_value=3, value=1, key="gen_s_ia")
        dias_ia = {"2dias": 2, "30dias": 30, "1ano": 365, "vitalicio": 36500}[p_ia]
        if st.button("🎫 Gerar código Importador", use_container_width=True, key="btn_gen_ia"):
            cod = gerar_codigo_acesso("ia", p_ia, dias_ia, s_ia)
            st.success("Código gerado!")
            st.code(cod, language="text")
            st.caption(f"Importador | {p_ia} | {dias_ia} dias | {s_ia} sessão(ões)")

    with col_c2:
        st.markdown("#### 📏 Avaliação Física")
        p_av = st.selectbox("Plano", ["2dias", "30dias", "1ano", "vitalicio"], key="gen_p_av")
        s_av = st.number_input("Sessões", min_value=1, max_value=3, value=1, key="gen_s_av")
        dias_av = {"2dias": 2, "30dias": 30, "1ano": 365, "vitalicio": 36500}[p_av]
        if st.button("🎫 Gerar código Avaliação", use_container_width=True, key="btn_gen_av"):
            cod = gerar_codigo_acesso("avaliacao", p_av, dias_av, s_av)
            st.success("Código gerado!")
            st.code(cod, language="text")
            st.caption(f"Avaliação | {p_av} | {dias_av} dias | {s_av} sessão(ões)")

    with col_c3:
        st.markdown("#### 🏆 Combo")
        p_co = st.selectbox("Plano", ["30dias", "1ano", "vitalicio"], key="gen_p_co")
        s_co = st.number_input("Sessões", min_value=1, max_value=3, value=1, key="gen_s_co")
        dias_co = {"30dias": 30, "1ano": 365, "vitalicio": 36500}[p_co]
        if st.button("🎫 Gerar código Combo", use_container_width=True, key="btn_gen_co"):
            cod_ia = gerar_codigo_acesso("ia", p_co, dias_co, s_co)
            cod_av = gerar_codigo_acesso("avaliacao", p_co, dias_co, s_co)
            st.success("Códigos Combo gerados!")
            st.markdown("**Código Importador:**")
            st.code(cod_ia, language="text")
            st.markdown("**Código Avaliação:**")
            st.code(cod_av, language="text")
            st.caption(f"Combo | {p_co} | {dias_co} dias | {s_co} sessão(ões)")

# ══════════════════════════════
# TAB 3 — ESTATÍSTICAS
# ══════════════════════════════
with tab_stats:
    st.markdown("### 📊 Estatísticas dos Apoiadores")

    usuarios = listar_usuarios()
    comuns = [u for u in usuarios if u["role"] != "admin"]

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Total apoiadores", len(comuns))
    with col_s2:
        ativos = sum(1 for u in comuns if u["ativo"] == 1)
        st.metric("Ativos", ativos)
    with col_s3:
        inativos = len(comuns) - ativos
        st.metric("Inativos", inativos)
    with col_s4:
        vitalicio = sum(1 for u in comuns if u["plano_ia"] == "vitalicio" or u["plano_avaliacao"] == "vitalicio")
        st.metric("Vitalícios", vitalicio)

    st.markdown("---")
    # Distribuição de planos
    planos_ia = {}
    for u in comuns:
        p = u["plano_ia"] or "sem plano"
        planos_ia[p] = planos_ia.get(p, 0) + 1

    st.markdown("#### 📋 Distribuição — Importador de Cardápio")
    for plano, qtd in sorted(planos_ia.items()):
        st.progress(qtd / max(len(comuns), 1), text=f"{plano}: {qtd} usuário(s)")

# ============================================
# CONFIGURAÇÕES DO ADMIN (2FA e senha) na sidebar
# ============================================
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Configurações do Admin")

# Alterar senha
with st.sidebar.expander("🔐 Alterar senha", expanded=False):
    with st.form("alterar_senha_admin"):
        senha_atual = st.text_input("Senha atual", type="password")
        nova_senha1 = st.text_input("Nova senha", type="password")
        nova_senha2 = st.text_input("Confirmar nova senha", type="password")

        if st.form_submit_button("Alterar senha"):
            if not senha_atual or not nova_senha1 or not nova_senha2:
                st.error("Preencha todos os campos")
            elif nova_senha1 != nova_senha2:
                st.error("Nova senha e confirmação não conferem")
            elif len(nova_senha1) < 6:
                st.error("A senha deve ter pelo menos 6 caracteres")
            elif verificar_senha_admin(senha_atual):
                from database import alterar_senha_admin as alterar_senha_admin_func
                alterar_senha_admin_func(nova_senha1)
                st.session_state.msg_senha_alterada = "✅ Senha alterada! Use a nova senha no próximo login."
                st.session_state.admin_autenticado = False
                st.session_state.admin_senha_ok = False
                st.rerun()
            else:
                st.error("❌ Senha atual incorreta")

# Configurar 2FA
with st.sidebar.expander("🔐 Configurar 2FA", expanded=False):
    admin_info = buscar_admin()
    if admin_info and admin_info.get("google_2fa_secret"):
        st.success("✅ 2FA configurado e ativo")
        st.caption("O código do Google Authenticator é exigido em todo login do painel.")
        if st.button("🔄 Resetar 2FA", use_container_width=True, key="btn_reset_2fa"):
            configurar_2fa_admin(None)
            # Remove também os códigos de recuperação
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM codigos_recuperacao_2fa WHERE admin_id = %s", (admin_info["id"],))
                conn.commit()
                cursor.close()
                conn.close()
            st.success("2FA removido! Configure novamente quando quiser.")
            st.rerun()
    else:
        st.markdown("**Ativar autenticação de dois fatores:**")
        st.caption("Após ativar, o código do Google Authenticator será obrigatório em cada login do painel.")
        if st.button("🔐 Configurar 2FA", use_container_width=True, key="btn_config_2fa"):
            secret = pyotp.random_base32()
            admin_atual = buscar_admin()

            # Gerar 8 códigos de recuperação únicos
            codigos_recuperacao = [secrets_lib.token_hex(4).upper() for _ in range(8)]
            salvar_codigos_recuperacao(admin_atual["id"], codigos_recuperacao)
            configurar_2fa_admin(secret)

            totp = pyotp.TOTP(secret)
            uri = totp.provisioning_uri(name="BioGestão 360 - Admin", issuer_name="BioGestao360")

            qr = qrcode.QRCode(version=1, box_size=5, border=2)
            qr.add_data(uri)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_bytes = io.BytesIO()
            img.save(img_bytes)
            img_bytes.seek(0)

            st.image(img_bytes, width=200)
            st.caption(f"**Chave secreta:** `{secret}`")
            st.caption("Escaneie com Google Authenticator ou Authy.")

            st.markdown("---")
            st.markdown("#### 🔑 Códigos de Recuperação")
            st.warning(
                "⚠️ **ANOTE AGORA!** Estes códigos aparecem apenas uma vez. "
                "Guarde em lugar seguro. Cada código só pode ser usado uma vez."
            )
            cols = st.columns(2)
            for i, cod in enumerate(codigos_recuperacao):
                cols[i % 2].code(cod, language="text")
            st.error(
                "🚨 Se perder o celular E não tiver estes códigos, "
                "a única recuperação é executar `reset_admin.py`."
            )