# auth.py
import streamlit as st
from database import (
    verificar_credenciais,
    cadastrar_usuario,
    usuario_tem_acesso_ia,
    usuario_tem_acesso_avaliacao,
    validar_codigo_acesso,
    buscar_usuario_por_id,
    contar_sessoes_ativas,
    registrar_sessao,
    remover_sessao,
    remover_todas_sessoes_usuario,
    get_configuracao,
)
from datetime import datetime
import uuid


def tela_login():
    """Tela de login na barra lateral"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Acesso ao Sistema")

    # Se já estiver logado, mostrar informações
    if st.session_state.get("logado", False):
        st.sidebar.success(f"✅ Logado: {st.session_state['usuario_nome']}")

        # Mostrar status de acesso
        if st.session_state.get("tem_acesso_ia", False):
            st.sidebar.success("📋 Importador de Cardápio: Ativo")
        else:
            st.sidebar.error("📋 Importador de Cardápio: Expirado")

        if st.session_state.get("tem_acesso_avaliacao", False):
            st.sidebar.success("📏 Avaliação Física: Ativa")
        else:
            st.sidebar.error("📏 Avaliação Física: Expirada")

        # Botão para renovar acesso com código
        with st.sidebar.expander("💚 Ativar plano de apoio", expanded=False):
            st.markdown(
                "Após realizar o PIX, o administrador irá gerar "
                "um código de ativação e enviar para você pelo WhatsApp."
            )
            st.markdown("**Cole abaixo o código recebido:**")
            codigo = st.text_input(
                "Código de ativação", type="password", key="codigo_acesso"
            )
            st.caption(
                "O código ativa automaticamente o plano correto "
                "(Importador, Avaliação ou Combo) pelo período contratado."
            )
            if st.button(
                "✅ Ativar", use_container_width=True, key="btn_ativar_codigo"
            ):
                if codigo:
                    sucesso, msg = validar_codigo_acesso(
                        codigo.upper(), st.session_state["usuario_id"]
                    )
                    if sucesso:
                        st.sidebar.success(msg)
                        st.session_state["tem_acesso_ia"] = usuario_tem_acesso_ia(
                            st.session_state["usuario_id"]
                        )
                        st.session_state["tem_acesso_avaliacao"] = (
                            usuario_tem_acesso_avaliacao(st.session_state["usuario_id"])
                        )
                        st.rerun()
                    else:
                        st.sidebar.error(msg)
                else:
                    st.sidebar.warning("Cole o código antes de clicar em Ativar.")
            st.caption(
                "⚠️ Após o PIX, ativação em até 72h. "
                "Dúvidas: WhatsApp (21) 97948-6731"
            )

        # Botão sair
        if st.sidebar.button("🚪 Sair", use_container_width=True, key="btn_sair"):
            if "session_token" in st.session_state:
                remover_sessao(st.session_state["session_token"])
            for key in [
                "logado",
                "usuario_id",
                "usuario_nome",
                "usuario_role",
                "tem_acesso_ia",
                "tem_acesso_avaliacao",
                "session_token",
                "admin_autenticado",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        return True

    # Formulário de login
    with st.sidebar.form("login_form"):
        username = st.text_input("👤 Usuário")
        senha = st.text_input("🔒 Senha", type="password")
        submitted = st.form_submit_button("Entrar", use_container_width=True)

        if submitted:
            # Limpar espaços invisíveis — problema comum no celular
            username = username.strip().lower()
            senha = senha.strip()

            if not username or not senha:
                st.sidebar.error("Preencha usuário e senha")
                return False

            usuario = verificar_credenciais(username, senha)
            if usuario:
                if "session_token" in st.session_state:
                    remover_sessao(st.session_state["session_token"])
                    del st.session_state["session_token"]

                sessoes_ativas = contar_sessoes_ativas(usuario["id"])

                if sessoes_ativas >= usuario["max_sessoes"]:
                    remover_todas_sessoes_usuario(usuario["id"])
                    sessoes_ativas = 0

                session_token = str(uuid.uuid4())
                registrar_sessao(usuario["id"], session_token)

                st.session_state["logado"] = True
                st.session_state["usuario_id"] = usuario["id"]
                st.session_state["usuario_nome"] = usuario["username"]
                st.session_state["usuario_role"] = usuario["role"]
                st.session_state["session_token"] = session_token
                st.session_state["tem_acesso_ia"] = usuario_tem_acesso_ia(usuario["id"])
                st.session_state["tem_acesso_avaliacao"] = usuario_tem_acesso_avaliacao(
                    usuario["id"]
                )
                st.sidebar.success(f"✅ Logado como {username}")
                st.rerun()
            else:
                st.sidebar.error("Usuário ou senha inválidos")
                return False

    # ── Cadastro de novo usuário (2 dias grátis) ──
    # Só exibe se o admin não tiver bloqueado novos cadastros
    cadastro_aberto = get_configuracao("cadastro_aberto", "1") == "1"

    if cadastro_aberto:
        with st.sidebar.expander("🆕 Cadastre-se (2 dias grátis)", expanded=False):
            with st.form("cadastro_form"):
                novo_user = st.text_input("Usuário")
                novo_email = st.text_input("E-mail")
                nova_senha = st.text_input("Senha", type="password")
                confirm_senha = st.text_input("Confirmar senha", type="password")
                st.caption(
                    "🔓 Após o cadastro, você terá **2 dias grátis** para testar "
                    "o **Importador Automático de Cardápio** e a **Avaliação Física**!"
                )

                if st.form_submit_button("Cadastrar", use_container_width=True):
                    novo_user = novo_user.strip().lower()
                    novo_email = novo_email.strip().lower()
                    nova_senha = nova_senha.strip()
                    confirm_senha = confirm_senha.strip()

                    if not novo_user or not novo_email or not nova_senha:
                        st.sidebar.error("Preencha todos os campos")
                    elif " " in novo_user:
                        st.sidebar.error(
                            "❌ O nome de usuário não pode ter espaços. "
                            "Use underline: ex. joao_silva"
                        )
                    elif len(novo_user) < 3:
                        st.sidebar.error(
                            "❌ Nome de usuário deve ter pelo menos 3 caracteres"
                        )
                    elif not novo_user.replace("_", "").replace(".", "").isalnum():
                        st.sidebar.error(
                            "❌ Nome de usuário só pode ter letras, números, "
                            "ponto (.) ou underline (_)"
                        )
                    elif nova_senha != confirm_senha:
                        st.sidebar.error("❌ Senhas não conferem")
                    elif len(nova_senha) < 4:
                        st.sidebar.error("❌ Senha deve ter pelo menos 4 caracteres")
                    elif "@" not in novo_email or "." not in novo_email:
                        st.sidebar.error("❌ Informe um e-mail válido")
                    else:
                        if cadastrar_usuario(novo_user, novo_email, nova_senha):
                            st.sidebar.success(
                                "✅ Cadastro realizado! Faça login para começar."
                            )
                            st.sidebar.info(
                                f"💡 Usuário cadastrado como: **{novo_user}**\n\n"
                                "Seu acesso gratuito de 2 dias já está ativo!"
                            )
                        else:
                            st.sidebar.error("❌ Usuário ou e-mail já existe")
    else:
        st.sidebar.info(
            "🔒 Novos cadastros estão temporariamente suspensos.\n\n"
            "Entre em contato pelo WhatsApp **(21) 97948-6731** "
            "para solicitar acesso."
        )

    # Se não estiver logado, mostrar aviso
    if not st.session_state.get("logado", False):
        st.warning(
            "🔐 Faça login na barra lateral para acessar o "
            "Importador Automático de Cardápio e a Avaliação Física"
        )
        st.info(
            "💡 **Novo usuário?** Cadastre-se e ganhe **2 dias grátis** para testar!"
        )

    return False


def verificar_acesso_ia():
    """Verifica acesso ao Importador de Cardápio - retorna (bool, mensagem)"""
    if not st.session_state.get("logado", False):
        return False, "🔒 Faça login para usar o Importador Automático de Cardápio"
    if not st.session_state.get("tem_acesso_ia", False):
        return (
            False,
            "🔒 Seu acesso ao Importador de Cardápio expirou.\n\n"
            "📱 Envie o comprovante PIX no WhatsApp: **(21) 97948-6731**\n"
            "📚 Tutoriais e materiais no Telegram: **t.me/biogestao360**\n\n"
            "⏱️ Após envio, ativação em até 72 horas.",
        )
    return True, "Acesso liberado"


def verificar_acesso_avaliacao():
    """Verifica acesso à Avaliação Física - retorna (bool, mensagem)"""
    if not st.session_state.get("logado", False):
        return False, "🔒 Faça login para usar a Avaliação Física"
    if not st.session_state.get("tem_acesso_avaliacao", False):
        return (
            False,
            "🔒 Seu acesso à Avaliação Física expirou.\n\n"
            "📱 Envie o comprovante PIX no WhatsApp: **(21) 97948-6731**\n"
            "📚 Tutoriais e materiais no Telegram: **t.me/biogestao360**\n\n"
            "⏱️ Após envio, ativação em até 72 horas.",
        )
    return True, "Acesso liberado"
