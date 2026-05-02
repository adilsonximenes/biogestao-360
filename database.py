# database.py
import psycopg2
import psycopg2.extras
import hashlib
from datetime import datetime, timedelta
import secrets
import streamlit as st


def get_connection():
    """Cria conexão com o banco Supabase/PostgreSQL"""
    try:
        conn = psycopg2.connect(
            st.secrets["SUPABASE_DB_URL"], connect_timeout=10, sslmode="require"
        )
        return conn
    except Exception as e:
        st.error(f"❌ Erro de conexão com o banco: {e}")
        return None


def init_db():
    """Cria todas as tabelas no banco Supabase"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            plano_ia TEXT DEFAULT '2dias',
            plano_avaliacao TEXT DEFAULT '2dias',
            acesso_ia_until TIMESTAMP NULL,
            acesso_avaliacao_until TIMESTAMP NULL,
            max_sessoes INTEGER DEFAULT 1,
            ativo INTEGER DEFAULT 1,
            google_2fa_secret TEXT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de códigos de acesso
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS codigos_acesso (
            id SERIAL PRIMARY KEY,
            codigo TEXT UNIQUE NOT NULL,
            tipo TEXT CHECK(tipo IN ('ia', 'avaliacao')),
            plano TEXT NOT NULL,
            dias INTEGER NOT NULL,
            sessoes INTEGER DEFAULT 1,
            usado INTEGER DEFAULT 0,
            usuario_id INTEGER NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used_at TIMESTAMP NULL
        )
    """)

    # Tabela de sessões ativas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_ativas (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    # Tabela de códigos de recuperação 2FA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS codigos_recuperacao_2fa (
            id SERIAL PRIMARY KEY,
            admin_id INTEGER NOT NULL,
            codigo TEXT NOT NULL,
            usado INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Criar admin se não existir
    cursor.execute("SELECT id FROM usuarios WHERE username = 'admin'")
    if not cursor.fetchone():
        senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
        data_futura = datetime.now() + timedelta(days=36500)
        cursor.execute(
            """
            INSERT INTO usuarios (
                username, email, senha_hash, role,
                plano_ia, plano_avaliacao,
                acesso_ia_until, acesso_avaliacao_until,
                max_sessoes, google_2fa_secret
            )
            VALUES (%s, %s, %s, 'admin', 'vitalicio', 'vitalicio', %s, %s, 5, NULL)
        """,
            (
                "admin",
                "admin@biogestao.com",
                senha_hash,
                data_futura,
                data_futura,
            ),
        )
        print("✅ Admin criado: admin / admin123")

    conn.commit()
    cursor.close()
    conn.close()


def remover_todas_sessoes_usuario(usuario_id):
    """Remove todas as sessões de um usuário"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessoes_ativas WHERE usuario_id = %s", (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()


def verificar_credenciais(username, senha):
    """Verifica login do usuário"""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    cursor.execute(
        """
        SELECT id, username, email, role, plano_ia, plano_avaliacao,
               acesso_ia_until, acesso_avaliacao_until, max_sessoes, ativo
        FROM usuarios
        WHERE username = %s AND senha_hash = %s
    """,
        (username, senha_hash),
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and user[9] == 1:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[3],
            "plano_ia": user[4],
            "plano_avaliacao": user[5],
            "acesso_ia_until": user[6],
            "acesso_avaliacao_until": user[7],
            "max_sessoes": user[8],
        }
    return None


def cadastrar_usuario(username, email, senha):
    """Cadastra novo usuário com 2 dias grátis"""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    expira_2dias = datetime.now() + timedelta(days=2)
    try:
        cursor.execute(
            """
            INSERT INTO usuarios (
                username, email, senha_hash,
                plano_ia, plano_avaliacao,
                acesso_ia_until, acesso_avaliacao_until,
                max_sessoes
            )
            VALUES (%s, %s, %s, '2dias', '2dias', %s, %s, 1)
        """,
            (username, email, senha_hash, expira_2dias, expira_2dias),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        cursor.close()
        conn.close()
        return False


def usuario_tem_acesso_ia(usuario_id):
    """Verifica se usuário tem acesso ao Importador de Cardápio"""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    cursor.execute(
        "SELECT acesso_ia_until FROM usuarios WHERE id = %s AND ativo = 1",
        (usuario_id,),
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and result[0]:
        try:
            expira = result[0]
            if isinstance(expira, str):
                expira = datetime.strptime(expira, "%Y-%m-%d %H:%M:%S")
            return expira > datetime.now()
        except Exception:
            return False
    return False


def usuario_tem_acesso_avaliacao(usuario_id):
    """Verifica se usuário tem acesso à Avaliação Física"""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    cursor.execute(
        "SELECT acesso_avaliacao_until FROM usuarios WHERE id = %s AND ativo = 1",
        (usuario_id,),
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and result[0]:
        try:
            expira = result[0]
            if isinstance(expira, str):
                expira = datetime.strptime(expira, "%Y-%m-%d %H:%M:%S")
            return expira > datetime.now()
        except Exception:
            return False
    return False


def contar_sessoes_ativas(usuario_id):
    """Conta sessões ativas do usuário"""
    conn = get_connection()
    if not conn:
        return 0
    cursor = conn.cursor()
    limite = datetime.now() - timedelta(hours=24)
    cursor.execute("DELETE FROM sessoes_ativas WHERE ultimo_acesso < %s", (limite,))
    cursor.execute(
        "SELECT COUNT(*) FROM sessoes_ativas WHERE usuario_id = %s", (usuario_id,)
    )
    count = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return count


def registrar_sessao(usuario_id, session_token):
    """Registra uma nova sessão"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessoes_ativas (usuario_id, session_token) VALUES (%s, %s)",
        (usuario_id, session_token),
    )
    conn.commit()
    cursor.close()
    conn.close()


def remover_sessao(session_token):
    """Remove uma sessão específica"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM sessoes_ativas WHERE session_token = %s", (session_token,)
    )
    conn.commit()
    cursor.close()
    conn.close()


def listar_usuarios():
    """Lista todos os usuários para o admin"""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, email, role, plano_ia, plano_avaliacao,
               acesso_ia_until, acesso_avaliacao_until, max_sessoes, ativo
        FROM usuarios ORDER BY id
    """)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {
            "id": u[0],
            "username": u[1],
            "email": u[2],
            "role": u[3],
            "plano_ia": u[4],
            "plano_avaliacao": u[5],
            "acesso_ia_until": u[6],
            "acesso_avaliacao_until": u[7],
            "max_sessoes": u[8],
            "ativo": u[9],
        }
        for u in users
    ]


def atualizar_plano(usuario_id, tipo, plano, dias, sessoes=1):
    """Atualiza o plano de acesso do usuário"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    expira = datetime.now() + timedelta(days=dias)
    if tipo == "ia":
        cursor.execute(
            """
            UPDATE usuarios
            SET plano_ia = %s, acesso_ia_until = %s, max_sessoes = %s
            WHERE id = %s
        """,
            (plano, expira, sessoes, usuario_id),
        )
    else:
        cursor.execute(
            """
            UPDATE usuarios
            SET plano_avaliacao = %s, acesso_avaliacao_until = %s, max_sessoes = %s
            WHERE id = %s
        """,
            (plano, expira, sessoes, usuario_id),
        )
    conn.commit()
    cursor.close()
    conn.close()


def gerar_codigo_acesso(tipo, plano, dias, sessoes=1):
    """Gera um código único de acesso"""
    codigo = secrets.token_hex(8).upper()
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO codigos_acesso (codigo, tipo, plano, dias, sessoes)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (codigo, tipo, plano, dias, sessoes),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return codigo


def validar_codigo_acesso(codigo, usuario_id):
    """Valida e ativa um código de acesso"""
    conn = get_connection()
    if not conn:
        return False, "Erro de conexão com o banco"
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, tipo, plano, dias, sessoes, usado
        FROM codigos_acesso
        WHERE codigo = %s AND usado = 0
    """,
        (codigo.upper(),),
    )
    result = cursor.fetchone()
    if not result:
        cursor.close()
        conn.close()
        return False, "Código inválido ou já utilizado"

    codigo_id, tipo, plano, dias, sessoes, _ = result
    atualizar_plano(usuario_id, tipo, plano, dias, sessoes)

    cursor.execute(
        """
        UPDATE codigos_acesso
        SET usado = 1, usuario_id = %s, used_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """,
        (usuario_id, codigo_id),
    )
    conn.commit()
    cursor.close()
    conn.close()

    tipo_nome = "Importador de Cardápio" if tipo == "ia" else "Avaliação Física"
    return (
        True,
        f"✅ Código validado! Acesso {tipo_nome} ativado por {dias} dias "
        f"({sessoes} sessão(ões) simultânea(s)).",
    )


def deletar_usuario(user_id):
    """Remove um usuário exceto o admin"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s AND role != 'admin'", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()


def ativar_desativar_usuario(user_id, ativo):
    """Ativa ou desativa um usuário"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET ativo = %s WHERE id = %s AND role != 'admin'",
        (ativo, user_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def contar_usuarios():
    """Conta total de usuários comuns"""
    conn = get_connection()
    if not conn:
        return 0
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE role != 'admin'")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count


def verificar_senha_admin(senha):
    """Verifica a senha do admin"""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    cursor.execute(
        "SELECT id FROM usuarios WHERE role = 'admin' AND senha_hash = %s",
        (senha_hash,),
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None


def alterar_senha_admin(nova_senha):
    """Altera a senha do admin"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    nova_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
    cursor.execute(
        "UPDATE usuarios SET senha_hash = %s WHERE role = 'admin'", (nova_hash,)
    )
    conn.commit()
    cursor.close()
    conn.close()


def buscar_admin():
    """Retorna dados do admin"""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, google_2fa_secret FROM usuarios WHERE role = 'admin' LIMIT 1"
    )
    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    if admin:
        return {
            "id": admin[0],
            "username": admin[1],
            "google_2fa_secret": admin[2],
        }
    return None


def configurar_2fa_admin(secret):
    """Configura ou remove o 2FA do admin"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET google_2fa_secret = %s WHERE role = 'admin'", (secret,)
    )
    conn.commit()
    cursor.close()
    conn.close()


def salvar_codigos_recuperacao(admin_id, codigos):
    """Salva códigos de recuperação 2FA"""
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM codigos_recuperacao_2fa WHERE admin_id = %s", (admin_id,)
    )
    for codigo in codigos:
        cursor.execute(
            "INSERT INTO codigos_recuperacao_2fa (admin_id, codigo) VALUES (%s, %s)",
            (admin_id, codigo),
        )
    conn.commit()
    cursor.close()
    conn.close()


def verificar_codigo_recuperacao(admin_id, codigo_informado):
    """Verifica e consome um código de recuperação 2FA"""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id FROM codigos_recuperacao_2fa
        WHERE admin_id = %s AND codigo = %s AND usado = 0
    """,
        (admin_id, codigo_informado.upper().strip()),
    )
    result = cursor.fetchone()
    if result:
        cursor.execute(
            "UPDATE codigos_recuperacao_2fa SET usado = 1 WHERE id = %s", (result[0],)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    cursor.close()
    conn.close()
    return False


def buscar_usuario_por_id(usuario_id):
    """Busca usuário pelo ID"""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, username, email, role, plano_ia, plano_avaliacao,
               acesso_ia_until, acesso_avaliacao_until, max_sessoes, ativo
        FROM usuarios WHERE id = %s
    """,
        (usuario_id,),
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[3],
            "plano_ia": user[4],
            "plano_avaliacao": user[5],
            "acesso_ia_until": user[6],
            "acesso_avaliacao_until": user[7],
            "max_sessoes": user[8],
            "ativo": user[9],
        }
    return None


# Inicializar banco
init_db()
