# admin_panel.py
import streamlit as st
import secrets as secrets_lib
from database import (
    listar_usuarios,
    buscar_admin,
    verificar_senha_admin,
    alterar_senha_admin,
    deletar_usuario,
    ativar_desativar_usuario,
    contar_usuarios,
    atualizar_plano,
    gerar_codigo_acesso,
    configurar_2fa_admin,
    salvar_codigos_recuperacao,
    verificar_codigo_recuperacao,
)
import pyotp
import qrcode
import io
from PIL import Image


def tela_admin_dashboard():
    """Painel do Administrador"""
    st.sidebar.markdown("## 👑 Painel do Administrador")

    # Inicializar estados
    if "admin_autenticado" not in st.session_state:
        st.session_state.admin_autenticado = False
    if "admin_2fa_pendente" not in st.session_state:
        st.session_state.admin_2fa_pendente = False
    if "admin_senha_ok" not in st.session_state:
        st.session_state.admin_senha_ok = False

    # ─────────────────────────────────────────────
    # ETAPA 1 — FORMULÁRIO DE SENHA
    # ─────────────────────────────────────────────
    if not st.session_state.admin_autenticado and not st.session_state.admin_senha_ok:
        st.sidebar.markdown("### 🔐 Acesso restrito ao Administrador")

        # Exibir mensagem de sucesso de troca de senha se houver
        if st.session_state.get("msg_senha_alterada"):
            st.sidebar.success(st.session_state.msg_senha_alterada)
            del st.session_state.msg_senha_alterada

        with st.sidebar.form("admin_login_senha"):
            senha = st.text_input("🔒 Senha do Administrador", type="password")
            if st.form_submit_button("Continuar", use_container_width=True):
                if not senha:
                    st.sidebar.error("Digite a senha")
                elif verificar_senha_admin(senha):
                    admin_info = buscar_admin()
                    if admin_info and admin_info.get("google_2fa_secret"):
                        # Tem 2FA — guarda o secret e avança para etapa 2
                        st.session_state.admin_senha_ok = True
                        st.session_state.admin_2fa_secret_temp = admin_info[
                            "google_2fa_secret"
                        ]
                        st.session_state.admin_id_temp = admin_info["id"]
                        st.rerun()
                    else:
                        # Sem 2FA — acesso direto
                        st.session_state.admin_autenticado = True
                        st.session_state.admin_senha_ok = False
                        st.rerun()
                else:
                    st.sidebar.error("❌ Senha incorreta!")

        st.sidebar.caption(
            "⚠️ Esqueceu a senha? Execute `reset_admin.py` na pasta do projeto."
        )
        return

    # ─────────────────────────────────────────────
    # ETAPA 2 — VERIFICAÇÃO 2FA (só chega aqui se senha OK)
    # ─────────────────────────────────────────────
    if st.session_state.admin_senha_ok and not st.session_state.admin_autenticado:
        st.sidebar.markdown("### 📱 Verificação de Dois Fatores")
        st.sidebar.info("Senha verificada ✅ — Digite agora o código do autenticador.")

        with st.sidebar.form("admin_form_2fa"):
            codigo_2fa = st.text_input(
                "Código do Google Authenticator (6 dígitos)",
                max_chars=6,
                placeholder="000000",
            )
            usar_recuperacao = st.checkbox("Usar código de recuperação")
            if st.form_submit_button("Verificar", use_container_width=True):
                if not codigo_2fa:
                    st.sidebar.error("Digite o código")
                elif usar_recuperacao:
                    # Tenta código de recuperação
                    if verificar_codigo_recuperacao(
                        st.session_state.admin_id_temp, codigo_2fa
                    ):
                        st.session_state.admin_autenticado = True
                        st.session_state.admin_senha_ok = False
                        st.sidebar.success("✅ Acesso com código de recuperação!")
                        st.rerun()
                    else:
                        st.sidebar.error(
                            "❌ Código de recuperação inválido ou já usado!"
                        )
                else:
                    totp = pyotp.TOTP(st.session_state.admin_2fa_secret_temp)
                    if totp.verify(codigo_2fa):
                        st.session_state.admin_autenticado = True
                        st.session_state.admin_senha_ok = False
                        st.sidebar.success("✅ Acesso concedido!")
                        st.rerun()
                    else:
                        st.sidebar.error("❌ Código 2FA inválido! Verifique o app.")

        if st.sidebar.button("← Voltar", key="btn_voltar_2fa"):
            st.session_state.admin_senha_ok = False
            st.rerun()
        return

    # ─────────────────────────────────────────────
    # PAINEL AUTENTICADO
    # ─────────────────────────────────────────────
    admin = buscar_admin()
    if admin:
        st.sidebar.markdown(f"👑 Bem-vindo, **{admin['username']}**")

    st.sidebar.markdown("---")

    # ── ESTATÍSTICAS RÁPIDAS ──
    total_usuarios = contar_usuarios()
    usuarios = listar_usuarios()
    usuarios_ativos = sum(1 for u in usuarios if u.get("ativo", 1) == 1)

    st.sidebar.markdown(f"📊 **Total de apoiadores:** {total_usuarios}")
    st.sidebar.markdown(f"🟢 **Ativos:** {usuarios_ativos}")
    st.sidebar.markdown(f"🔴 **Inativos:** {total_usuarios - usuarios_ativos}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Gerenciar Usuários")

    for user in usuarios:
        if user["role"] == "admin":
            continue

        with st.sidebar.expander(f"📌 {user['username']}"):
            st.markdown(f"**ID:** {user['id']} | **Email:** {user['email']}")
            status = "🟢 Ativo" if user.get("ativo", 1) == 1 else "🔴 Inativo"
            st.markdown(f"**Status:** {status}")
            st.markdown(f"**Sessões máx:** {user.get('max_sessoes', 1)}")
            st.markdown("---")

            st.markdown("**📋 Importador de Cardápio:**")
            st.markdown(f"- Plano: `{user['plano_ia']}`")
            st.markdown(f"- Expira: `{user['acesso_ia_until'] or 'Não ativo'}`")

            st.markdown("**📏 Avaliação Física:**")
            st.markdown(f"- Plano: `{user['plano_avaliacao']}`")
            st.markdown(f"- Expira: `{user['acesso_avaliacao_until'] or 'Não ativo'}`")

            st.markdown("---")
            st.markdown("#### 📝 Alterar Plano")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📋 Importador**")
                plano_ia = st.selectbox(
                    "Plano",
                    ["2dias", "30dias", "1ano", "vitalicio"],
                    index=(
                        ["2dias", "30dias", "1ano", "vitalicio"].index(user["plano_ia"])
                        if user["plano_ia"] in ["2dias", "30dias", "1ano", "vitalicio"]
                        else 0
                    ),
                    key=f"ia_{user['id']}",
                )
                sessoes_ia = st.number_input(
                    "Sessões",
                    min_value=1,
                    max_value=3,
                    value=min(user.get("max_sessoes", 1), 3),
                    key=f"sessoes_ia_{user['id']}",
                )
                dias_ia = {"2dias": 2, "30dias": 30, "1ano": 365, "vitalicio": 36500}[
                    plano_ia
                ]
                if st.button("💾 Salvar", key=f"save_ia_{user['id']}"):
                    atualizar_plano(user["id"], "ia", plano_ia, dias_ia, sessoes_ia)
                    st.success(f"✅ Importador de {user['username']} atualizado!")
                    st.rerun()

            with col2:
                st.markdown("**📏 Avaliação**")
                plano_av = st.selectbox(
                    "Plano",
                    ["2dias", "30dias", "1ano", "vitalicio"],
                    index=(
                        ["2dias", "30dias", "1ano", "vitalicio"].index(
                            user["plano_avaliacao"]
                        )
                        if user["plano_avaliacao"]
                        in ["2dias", "30dias", "1ano", "vitalicio"]
                        else 0
                    ),
                    key=f"av_{user['id']}",
                )
                sessoes_av = st.number_input(
                    "Sessões",
                    min_value=1,
                    max_value=3,
                    value=min(user.get("max_sessoes", 1), 3),
                    key=f"sessoes_av_{user['id']}",
                )
                dias_av = {"2dias": 2, "30dias": 30, "1ano": 365, "vitalicio": 36500}[
                    plano_av
                ]
                if st.button("💾 Salvar", key=f"save_av_{user['id']}"):
                    atualizar_plano(
                        user["id"], "avaliacao", plano_av, dias_av, sessoes_av
                    )
                    st.success(f"✅ Avaliação de {user['username']} atualizada!")
                    st.rerun()

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                if user.get("ativo", 1) == 1:
                    if st.button("🔴 Desativar", key=f"deact_{user['id']}"):
                        ativar_desativar_usuario(user["id"], 0)
                        st.success(f"{user['username']} desativado!")
                        st.rerun()
                else:
                    if st.button("🟢 Ativar", key=f"act_{user['id']}"):
                        ativar_desativar_usuario(user["id"], 1)
                        st.success(f"{user['username']} ativado!")
                        st.rerun()
            with col_b:
                if st.button("🗑️ Deletar", key=f"del_{user['id']}"):
                    deletar_usuario(user["id"])
                    st.success(f"{user['username']} removido!")
                    st.rerun()

    # ── GERAR CÓDIGOS DE APOIO ──
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔑 Gerar Códigos de Apoio")
    st.sidebar.caption(
        "Gere códigos únicos para enviar ao apoiador após confirmação do PIX. "
        "Cada código é de uso único."
    )

    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.markdown("#### 📋 Código Importador")
        plano_ia = st.selectbox(
            "Plano", ["2dias", "30dias", "1ano", "vitalicio"], key="gen_ia"
        )
        sessoes_ia = st.number_input(
            "Sessões simultâneas",
            min_value=1,
            max_value=3,
            value=1,
            key="sessoes_gen_ia",
        )
        dias_ia = {"2dias": 2, "30dias": 30, "1ano": 365, "vitalicio": 36500}[plano_ia]
        if st.button("🎫 Gerar código", use_container_width=True, key="btn_gen_ia"):
            codigo = gerar_codigo_acesso("ia", plano_ia, dias_ia, sessoes_ia)
            st.success("Código gerado!")
            st.code(codigo, language="text")
            st.caption(
                f"Importador | {plano_ia} | {dias_ia} dias | {sessoes_ia} sessão(ões)"
            )

    with col2:
        st.markdown("#### 📏 Código Avaliação")
        plano_av = st.selectbox(
            "Plano", ["2dias", "30dias", "1ano", "vitalicio"], key="gen_av"
        )
        sessoes_av = st.number_input(
            "Sessões simultâneas",
            min_value=1,
            max_value=3,
            value=1,
            key="sessoes_gen_av",
        )
        dias_av = {"2dias": 2, "30dias": 30, "1ano": 365, "vitalicio": 36500}[plano_av]
        if st.button("🎫 Gerar código", use_container_width=True, key="btn_gen_av"):
            codigo = gerar_codigo_acesso("avaliacao", plano_av, dias_av, sessoes_av)
            st.success("Código gerado!")
            st.code(codigo, language="text")
            st.caption(
                f"Avaliação | {plano_av} | {dias_av} dias | {sessoes_av} sessão(ões)"
            )

    # ── CONFIGURAÇÕES DO ADMIN ──
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
                    alterar_senha_admin(nova_senha1)
                    # Guarda a mensagem no session_state para exibir após rerun
                    st.session_state.msg_senha_alterada = (
                        "✅ Senha alterada! Use a nova senha no próximo login."
                    )
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
            st.caption(
                "O código do Google Authenticator é exigido em todo login do painel."
            )
            if st.button(
                "🔄 Resetar 2FA", use_container_width=True, key="btn_reset_2fa"
            ):
                configurar_2fa_admin(None)
                st.success("2FA removido! Configure novamente quando quiser.")
                st.rerun()
        else:
            st.markdown("**Ativar autenticação de dois fatores:**")
            st.caption(
                "Após ativar, o código do Google Authenticator "
                "será obrigatório em cada login do painel."
            )
            if st.button(
                "🔐 Configurar 2FA", use_container_width=True, key="btn_config_2fa"
            ):
                secret = pyotp.random_base32()
                admin_atual = buscar_admin()

                # Gerar 8 códigos de recuperação únicos
                codigos_recuperacao = [
                    secrets_lib.token_hex(4).upper() for _ in range(8)
                ]
                salvar_codigos_recuperacao(admin_atual["id"], codigos_recuperacao)
                configurar_2fa_admin(secret)

                totp = pyotp.TOTP(secret)
                uri = totp.provisioning_uri(
                    name="BioGestão 360 - Admin", issuer_name="BioGestao360"
                )

                qr = qrcode.QRCode(version=1, box_size=5, border=2)
                qr.add_data(uri)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="PNG")
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
                # Exibir em grade 2 colunas
                cols = st.columns(2)
                for i, cod in enumerate(codigos_recuperacao):
                    cols[i % 2].code(cod, language="text")

                st.error(
                    "🚨 Se perder o celular E não tiver estes códigos, "
                    "a única recuperação é executar `reset_admin.py`."
                )

    # Botão sair
    st.sidebar.markdown("---")
    if st.sidebar.button(
        "🚪 Sair do Painel Admin", use_container_width=True, key="btn_sair_admin"
    ):
        st.session_state.admin_autenticado = False
        st.session_state.admin_senha_ok = False
        st.rerun()
