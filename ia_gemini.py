# ia_gemini.py — BioGestão 360  v4.0
# =====================================================================
# Hierarquia de busca para a seção 24.1 (importador automático):
#   1. TACO       → alimentos in natura, preparações caseiras (597 itens)
#   2. IBGE       → alimentos + 16 formas de preparo (1.962 itens)
#   3. BioGestão  → produtos industrializados brasileiros (25.176 itens)
#   4. Estimativa → fallback genérico por categoria
#
# Para a seção 26 (montagem manual), o usuário escolhe a fonte
# na sidebar — o app.py usa a df correspondente.
#
# Correções desta versão:
#   - Sódio: banco já em g/100g → _sodio_g_para_mg só multiplica por 1000
#   - Fallback CSV: gordura_saturada_g e gordura_trans_g incluídos
#   - Penalidade para produtos compostos na busca BioGestão
#   - estimativa_inteligente: valores corrigidos (TACO/IBGE)
#   - buscar_na_taco / buscar_na_ibge: lookup por nome_busca normalizado
# =====================================================================

import re, os
import pandas as pd
import unicodedata
from collections import defaultdict

# ── Cache global ──────────────────────────────────────────────────────────────
_BIO_INDEX_CACHE  = None   # índice invertido da BioGestão
_TACO_INDEX       = None   # dict nome_busca → row (TACO)
_IBGE_INDEX       = None   # dict nome_busca → row (IBGE)


def configurar_gemini(api_key):
    return None   # mantido para compatibilidade


# ══════════════════════════════════════════════════════════════════════════════
# CARREGAMENTO DAS TRÊS BASES
# ══════════════════════════════════════════════════════════════════════════════

def carregar_biogestao_foods():
    """Carrega BioGestão 360 do Supabase ou CSV local."""
    try:
        import streamlit as st
        import psycopg2
        conn = psycopg2.connect(
            st.secrets["SUPABASE_DB_URL"], connect_timeout=10, sslmode="require"
        )
        query = """
            SELECT nome, marca, porcao_g_ml, porcao_num, porcao_uni,
                   kcal_100g, proteina_g, carboidrato_g, gordura_g,
                   acucar_g, gordura_saturada_g, gordura_trans_g,
                   fibra_g, sodio_g, fonte
            FROM biogestao_foods ORDER BY nome
        """
        df = pd.read_sql(query, conn)
        conn.close()
        for col in ["kcal_100g","proteina_g","carboidrato_g","gordura_g",
                    "fibra_g","sodio_g","acucar_g","gordura_saturada_g",
                    "gordura_trans_g","porcao_num"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        print(f"BioGestão 360: {len(df):,} produtos do Supabase")
        return df
    except Exception as e:
        print(f"Supabase indisponível ({e}), tentando CSV local...")

    caminho = "biogestao_foods.csv"
    if not os.path.exists(caminho):
        print("CSV local não encontrado")
        return None
    try:
        df = pd.read_csv(caminho, encoding="utf-8", low_memory=False)
        for col in ["kcal_100g","proteina_g","carboidrato_g","gordura_g",
                    "fibra_g","sodio_g","acucar_g","gordura_saturada_g",
                    "gordura_trans_g","porcao_num"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        print(f"BioGestão 360: {len(df):,} produtos do CSV local")
        return df
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return None


@staticmethod if False else lambda f: f  # decorator dummy para legibilidade
def _carregar_csv_tabela(caminho, nome_tabela):
    """Carrega taco_limpa.csv ou ibge_limpa.csv."""
    if not os.path.exists(caminho):
        print(f"{nome_tabela}: arquivo não encontrado ({caminho})")
        return None
    try:
        df = pd.read_csv(caminho, encoding="utf-8", low_memory=False)
        for col in ["kcal_100g","proteina_g","carboidrato_g","gordura_g",
                    "fibra_g","sodio_mg","gordura_saturada_g","gordura_trans_g","acucar_g"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        print(f"{nome_tabela}: {len(df):,} alimentos carregados")
        return df
    except Exception as e:
        print(f"Erro ao carregar {nome_tabela}: {e}")
        return None


def carregar_taco():
    return _carregar_csv_tabela("taco_limpa.csv", "TACO")


def carregar_ibge():
    return _carregar_csv_tabela("ibge_limpa.csv", "IBGE")


# ══════════════════════════════════════════════════════════════════════════════
# NORMALIZAÇÃO
# ══════════════════════════════════════════════════════════════════════════════

def normalizar_texto_busca(texto):
    """Normaliza para busca: minúsculo, sem acento, sem vírgulas."""
    if not texto or not isinstance(texto, str):
        return ""
    t = texto.lower().replace(",", " ").replace("-", " ")
    t = unicodedata.normalize("NFKD", t)
    t = t.encode("ASCII", "ignore").decode("ASCII")
    t = re.sub(r"[^a-z0-9\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


# ══════════════════════════════════════════════════════════════════════════════
# TRATAMENTO DE VALORES
# ══════════════════════════════════════════════════════════════════════════════

def tratar_valor(valor, nullable=False):
    _vazios = ["NA","N/A","*","TR","-","","N","ND","NR"]
    if valor is None:
        return None if nullable else 0.0
    try:
        if pd.isna(valor):
            return None if nullable else 0.0
    except (TypeError, ValueError):
        pass
    if isinstance(valor, str):
        v = valor.strip().upper()
        if v in _vazios:
            return None if nullable else 0.0
        v = v.replace(",", ".")
        try:
            return float(v)
        except ValueError:
            return None if nullable else 0.0
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None if nullable else 0.0


def _sodio_g_para_mg(valor):
    """Banco BioGestão: sodio_g em g/100g → converte para mg."""
    v = tratar_valor(valor, nullable=True)
    if v is None:
        return None
    return round(v * 1000, 1)


def _sodio_mg_direto(valor):
    """TACO e IBGE: sódio já em mg/100g → usa direto."""
    v = tratar_valor(valor, nullable=True)
    if v is None:
        return None
    return round(float(v), 1)


def _resultado_base(dados, sodio_mg, fonte):
    """Monta o dict de retorno padrão."""
    return {
        "kcal":             tratar_valor(dados.get("kcal_100g", 0)),
        "proteina":         tratar_valor(dados.get("proteina_g", 0)),
        "carboidrato":      tratar_valor(dados.get("carboidrato_g", 0)),
        "gordura":          tratar_valor(dados.get("gordura_g", 0)),
        "acucar":           tratar_valor(dados.get("acucar_g"), nullable=True),
        "gordura_saturada": tratar_valor(dados.get("gordura_saturada_g"), nullable=True),
        "gordura_trans":    tratar_valor(dados.get("gordura_trans_g"), nullable=True),
        "fibra":            tratar_valor(dados.get("fibra_g"), nullable=True),
        "sodio_mg":         sodio_mg,
        "porcao_num":       100.0,
        "porcao_uni":       "g",
        "fonte":            fonte,
    }


# ══════════════════════════════════════════════════════════════════════════════
# BUSCA NA TACO
# ══════════════════════════════════════════════════════════════════════════════

def _build_taco_index(df_taco):
    """Constrói dict nome_busca → row para lookup O(1)."""
    idx = {}
    for _, row in df_taco.iterrows():
        chave = str(row.get("nome_busca", "")).strip()
        if chave:
            idx[chave] = row
    return idx


def buscar_na_taco(nome_alimento, df_taco=None):
    """
    Busca na TACO pelo campo nome_busca (já normalizado no CSV).
    Tenta: exata → parcial mais longa.
    """
    global _TACO_INDEX
    if df_taco is None or df_taco.empty:
        return None

    if _TACO_INDEX is None:
        _TACO_INDEX = _build_taco_index(df_taco)

    nome_n = normalizar_texto_busca(nome_alimento)
    if not nome_n:
        return None

    # 1. Busca exata
    if nome_n in _TACO_INDEX:
        row = _TACO_INDEX[nome_n]
        return _resultado_base(row, _sodio_mg_direto(row.get("sodio_mg")), "TACO")

    # 2. Busca parcial: chave mais longa contida no nome buscado
    melhor = None
    for chave, row in _TACO_INDEX.items():
        if chave in nome_n:
            if melhor is None or len(chave) > len(melhor[0]):
                melhor = (chave, row)

    if melhor:
        row = melhor[1]
        kcal = tratar_valor(row.get("kcal_100g", 0))
        if kcal > 0:
            return _resultado_base(row, _sodio_mg_direto(row.get("sodio_mg")), "TACO")

    return None


# ══════════════════════════════════════════════════════════════════════════════
# BUSCA NA IBGE
# ══════════════════════════════════════════════════════════════════════════════

def _build_ibge_index(df_ibge):
    """Constrói dict nome_busca → row."""
    idx = {}
    for _, row in df_ibge.iterrows():
        chave = str(row.get("nome_busca", "")).strip()
        if chave:
            idx[chave] = row
    return idx


def buscar_na_ibge(nome_alimento, df_ibge=None):
    """
    Busca na IBGE pelo campo nome_busca (nome + preparação já combinados).
    Ex: 'ovo de galinha frito' → encontra direto.
    """
    global _IBGE_INDEX
    if df_ibge is None or df_ibge.empty:
        return None

    if _IBGE_INDEX is None:
        _IBGE_INDEX = _build_ibge_index(df_ibge)

    nome_n = normalizar_texto_busca(nome_alimento)
    if not nome_n:
        return None

    # 1. Exata
    if nome_n in _IBGE_INDEX:
        row = _IBGE_INDEX[nome_n]
        return _resultado_base(row, _sodio_mg_direto(row.get("sodio_mg")), "IBGE")

    # 2. Parcial mais longa
    melhor = None
    for chave, row in _IBGE_INDEX.items():
        if chave in nome_n:
            if melhor is None or len(chave) > len(melhor[0]):
                melhor = (chave, row)

    if melhor:
        row = melhor[1]
        kcal = tratar_valor(row.get("kcal_100g", 0))
        if kcal > 0:
            return _resultado_base(row, _sodio_mg_direto(row.get("sodio_mg")), "IBGE")

    return None


# ══════════════════════════════════════════════════════════════════════════════
# ÍNDICE INVERTIDO — BIOGESTÃO
# ══════════════════════════════════════════════════════════════════════════════

def _build_index(df_bio):
    index = defaultdict(list)
    for idx, row in df_bio.iterrows():
        nome = str(row.get("nome", ""))
        if not nome:
            continue
        palavras = set(normalizar_texto_busca(nome).split())
        for p in palavras:
            if len(p) >= 3:
                index[p].append(idx)
    return index


# Palavras de produtos compostos — penalizar no score
_PALAVRAS_COMPOSTAS = {
    "chips","frita","frito","empanado","empanada","snack","salgadinho",
    "nugget","croquete","bolinho","lasanha","marmita","prato","refeicao",
    "mistura","preparo","molho","caldo","sopa","instant",
}
_PALAVRAS_CALORICAS = {
    "oleo","azeite","manteiga","bacon","castanha","nozes","amendoim",
    "chocolate","biscoito","torrada","granola","aveia","pasta",
}
_PALAVRAS_CARB = {
    "pao","arroz","macarrao","batata","mandioca","cuscuz","tapioca",
    "aveia","granola","cereal","biscoito","torrada","bolo",
}


def buscar_na_biogestao(nome_alimento, df_bio):
    """Busca na base BioGestão 360 usando índice invertido."""
    global _BIO_INDEX_CACHE
    if df_bio is None or df_bio.empty:
        return None

    nome_norm = normalizar_texto_busca(nome_alimento)
    if not nome_norm:
        return None

    if _BIO_INDEX_CACHE is None:
        _BIO_INDEX_CACHE = _build_index(df_bio)

    estimativa    = estimativa_inteligente(nome_alimento)
    kcal_estimada = estimativa.get("kcal", 50)

    palavras_busca = set(nome_norm.split())
    indices = set()
    for p in palavras_busca:
        if p in _BIO_INDEX_CACHE:
            indices.update(_BIO_INDEX_CACHE[p])

    if not indices:
        return None

    candidatos = []
    for idx in indices:
        row       = df_bio.iloc[idx]
        nome_prod = str(row.get("nome", ""))
        if not nome_prod:
            continue
        desc_norm    = normalizar_texto_busca(nome_prod)
        palavras_desc = set(desc_norm.split())
        intersecao   = palavras_busca.intersection(palavras_desc)
        if not intersecao:
            continue

        score = len(intersecao) / max(1, len(palavras_busca))
        if palavras_busca.issubset(palavras_desc): score += 2.0
        if nome_norm in desc_norm:                 score += 3.0
        if desc_norm.startswith(nome_norm):        score += 1.0
        if nome_norm == desc_norm:                 score += 5.0

        porcao_uni = row.get("porcao_uni")
        if porcao_uni in ("g", "ml"):
            score += 0.5

        extras = palavras_desc - palavras_busca
        if len(extras) > 3:
            score -= 0.15 * (len(extras) - 3)
        for p in extras:
            if p in _PALAVRAS_COMPOSTAS and p not in palavras_busca:
                score -= 1.5

        candidatos.append((score, row))

    if not candidatos:
        return None

    candidatos.sort(key=lambda x: x[0], reverse=True)

    def _kcal_ok(nome_b, k):
        if k <= 700: return True
        return any(p in nome_b.lower() for p in _PALAVRAS_CALORICAS)

    def _carb_ok(nome_b, c):
        if c is None: return True
        if any(p in nome_b.lower() for p in _PALAVRAS_CARB): return True
        return c <= 50

    def _kcal_prox(kp, kr):
        if kr <= 0: return True
        return (kr * 0.35) <= kp <= (kr * 2.8)

    for score, row in candidatos:
        kcal_c = tratar_valor(row.get("kcal_100g", 0))
        carb_c = tratar_valor(row.get("carboidrato_g", 0), nullable=True)
        if kcal_c <= 0:                                  continue
        if not _kcal_ok(nome_alimento, kcal_c):          continue
        if not _carb_ok(nome_alimento, carb_c):          continue
        if not _kcal_prox(kcal_c, kcal_estimada):       continue

        return {
            "kcal":             kcal_c,
            "proteina":         tratar_valor(row.get("proteina_g", 0)),
            "carboidrato":      tratar_valor(row.get("carboidrato_g", 0)),
            "gordura":          tratar_valor(row.get("gordura_g", 0)),
            "acucar":           tratar_valor(row.get("acucar_g"), nullable=True),
            "gordura_saturada": tratar_valor(row.get("gordura_saturada_g"), nullable=True),
            "gordura_trans":    tratar_valor(row.get("gordura_trans_g"), nullable=True),
            "fibra":            tratar_valor(row.get("fibra_g"), nullable=True),
            "sodio_mg":         _sodio_g_para_mg(row.get("sodio_g")),
            "porcao_num":       tratar_valor(row.get("porcao_num", 0)),
            "porcao_uni":       row.get("porcao_uni") or "g",
            "fonte":            "BioGestao",
        }

    return None


# ══════════════════════════════════════════════════════════════════════════════
# BUSCA SQL DIRETA (fallback Supabase)
# ══════════════════════════════════════════════════════════════════════════════

def buscar_na_biogestao_sql(nome_alimento):
    try:
        import psycopg2, streamlit as _st
        nome_n = normalizar_texto_busca(nome_alimento)
        if not nome_n: return None
        db_url = _st.secrets.get("SUPABASE_DB_URL", "")
        if not db_url: return None
        conn = psycopg2.connect(db_url, connect_timeout=5, sslmode="require")
        cur  = conn.cursor()
        cur.execute("""
            SELECT kcal_100g, proteina_g, carboidrato_g, gordura_g,
                   acucar_g, gordura_saturada_g, gordura_trans_g,
                   fibra_g, sodio_g, porcao_num, porcao_uni
            FROM biogestao_foods
            WHERE lower(nome) LIKE %s
            ORDER BY length(nome) LIMIT 3
        """, (f"%{nome_n}%",))
        rows = cur.fetchall()
        cur.close(); conn.close()
        if not rows: return None
        r = rows[0]
        kcal = tratar_valor(r[0])
        if kcal <= 0: return None
        return {
            "kcal": kcal, "proteina": tratar_valor(r[1]),
            "carboidrato": tratar_valor(r[2]), "gordura": tratar_valor(r[3]),
            "acucar": tratar_valor(r[4], nullable=True),
            "gordura_saturada": tratar_valor(r[5], nullable=True),
            "gordura_trans": tratar_valor(r[6], nullable=True),
            "fibra": tratar_valor(r[7], nullable=True),
            "sodio_mg": _sodio_g_para_mg(r[8]),
            "porcao_num": tratar_valor(r[9]),
            "porcao_uni": r[10] or "g",
            "fonte": "BioGestao",
        }
    except Exception as e:
        print(f"buscar_na_biogestao_sql erro: {e}")
        return None


# ══════════════════════════════════════════════════════════════════════════════
# ESTIMATIVA INTELIGENTE (fallback final)
# Valores TACO/IBGE por 100g cozido/pronto
# ══════════════════════════════════════════════════════════════════════════════

def estimativa_inteligente(nome_alimento):
    n = nome_alimento.lower()

    if "clara" in n and ("ovo" in n or "egg" in n):
        return {"kcal":48,  "proteina":10.8,"carboidrato":0.7, "gordura":0.0, "fonte":"estimativa"}
    if any(p in n for p in ["ovo","omelete","mexido","cozido","estrelado","frito"]) \
       and not any(p in n for p in ["chocolate","amendoim","biscoito","macarrao","massa"]):
        return {"kcal":155, "proteina":12.6,"carboidrato":0.6, "gordura":10.6,"fonte":"estimativa"}
    if any(p in n for p in ["frango","galinha","chester"]):
        if any(p in n for p in ["empanado","frito","nugget"]):
            return {"kcal":246,"proteina":18.0,"carboidrato":15.0,"gordura":13.0,"fonte":"estimativa"}
        if any(p in n for p in ["sobrecoxa","coxa"]):
            return {"kcal":185,"proteina":24.0,"carboidrato":0.0,"gordura":9.5,"fonte":"estimativa"}
        return {"kcal":159,"proteina":32.0,"carboidrato":0.0,"gordura":3.6,"fonte":"estimativa"}
    if "tilapia" in n or "tilápia" in n:
        return {"kcal":128,"proteina":26.2,"carboidrato":0.0,"gordura":2.7,"fonte":"estimativa"}
    if "salmao" in n or "salmão" in n:
        return {"kcal":208,"proteina":20.0,"carboidrato":0.0,"gordura":13.5,"fonte":"estimativa"}
    if "atum" in n:
        return {"kcal":119,"proteina":25.5,"carboidrato":0.0,"gordura":1.7,"fonte":"estimativa"}
    if any(p in n for p in ["peixe","pescada","file"]):
        return {"kcal":110,"proteina":22.0,"carboidrato":0.0,"gordura":2.5,"fonte":"estimativa"}
    if any(p in n for p in ["carne","bife","alcatra","picanha","patinho","hamburguer"]):
        return {"kcal":219,"proteina":26.0,"carboidrato":0.0,"gordura":12.5,"fonte":"estimativa"}
    if "arroz" in n:
        if "integral" in n:
            return {"kcal":124,"proteina":2.6,"carboidrato":25.8,"gordura":1.0,"fonte":"estimativa"}
        return {"kcal":128,"proteina":2.5,"carboidrato":28.1,"gordura":0.2,"fonte":"estimativa"}
    if any(p in n for p in ["macarrao","macarrão","espaguete","lasanha","penne"]):
        return {"kcal":131,"proteina":4.5,"carboidrato":26.0,"gordura":0.5,"fonte":"estimativa"}
    if "aveia" in n:
        return {"kcal":394,"proteina":13.9,"carboidrato":67.0,"gordura":8.5,"fonte":"estimativa"}
    if "batata doce" in n or "batata-doce" in n:
        return {"kcal":77, "proteina":1.4,"carboidrato":18.4,"gordura":0.1,"fonte":"estimativa"}
    if "batata" in n:
        if any(p in n for p in ["frita","chips","palha"]):
            return {"kcal":520,"proteina":5.0,"carboidrato":52.0,"gordura":32.0,"fonte":"estimativa"}
        return {"kcal":82, "proteina":1.9,"carboidrato":18.5,"gordura":0.1,"fonte":"estimativa"}
    if any(p in n for p in ["feijao","feijão","lentilha"]):
        return {"kcal":77, "proteina":4.8,"carboidrato":14.0,"gordura":0.5,"fonte":"estimativa"}
    if "banana" in n:
        return {"kcal":89, "proteina":1.1,"carboidrato":23.0,"gordura":0.3,"fonte":"estimativa"}
    if "maca" in n:
        return {"kcal":56, "proteina":0.3,"carboidrato":15.0,"gordura":0.2,"fonte":"estimativa"}
    if "laranja" in n:
        return {"kcal":46, "proteina":0.9,"carboidrato":11.0,"gordura":0.1,"fonte":"estimativa"}
    if any(p in n for p in ["leite integral","leite desnatado","leite semi"]):
        return {"kcal":61, "proteina":3.2,"carboidrato":4.7,"gordura":3.3,"fonte":"estimativa"}
    if "leite" in n:
        return {"kcal":55, "proteina":3.0,"carboidrato":4.5,"gordura":2.5,"fonte":"estimativa"}
    if any(p in n for p in ["iogurte","yogurt"]):
        return {"kcal":57, "proteina":5.0,"carboidrato":7.0,"gordura":0.5,"fonte":"estimativa"}
    if "queijo" in n:
        return {"kcal":280,"proteina":18.0,"carboidrato":2.5,"gordura":22.0,"fonte":"estimativa"}
    if any(p in n for p in ["pao","pão","torrada","croissant"]):
        return {"kcal":265,"proteina":8.0,"carboidrato":50.0,"gordura":3.5,"fonte":"estimativa"}
    if any(p in n for p in ["castanha","nozes","amendoim","amendoa"]):
        return {"kcal":620,"proteina":18.0,"carboidrato":20.0,"gordura":50.0,"fonte":"estimativa"}
    if any(p in n for p in ["azeite","oleo"]):
        return {"kcal":884,"proteina":0.0,"carboidrato":0.0,"gordura":100.0,"fonte":"estimativa"}
    if "manteiga" in n:
        return {"kcal":717,"proteina":0.9,"carboidrato":0.1,"gordura":81.0,"fonte":"estimativa"}
    if any(p in n for p in ["brocolis","couve","espinafre","alface","abobrinha",
                              "cenoura","tomate","vagem","aspargo","legume"]):
        return {"kcal":30, "proteina":2.5,"carboidrato":5.0,"gordura":0.3,"fonte":"estimativa"}
    if any(p in n for p in ["cafe","café"]):
        return {"kcal":2,  "proteina":0.3,"carboidrato":0.0,"gordura":0.0,"fonte":"estimativa"}
    if "refrigerante" in n:
        return {"kcal":40, "proteina":0.0,"carboidrato":10.0,"gordura":0.0,"fonte":"estimativa"}
    if "suco" in n:
        return {"kcal":42, "proteina":0.6,"carboidrato":10.0,"gordura":0.1,"fonte":"estimativa"}
    if any(p in n for p in ["whey","albumina","proteina em po"]):
        return {"kcal":370,"proteina":80.0,"carboidrato":5.0,"gordura":4.0,"fonte":"estimativa"}

    return {"kcal":50,"proteina":2.0,"carboidrato":8.0,"gordura":1.5,"fonte":"estimativa"}


# ══════════════════════════════════════════════════════════════════════════════
# EXTRAÇÃO DE FATOR
# ══════════════════════════════════════════════════════════════════════════════

def extrair_fator_quantidade(quantidade_texto):
    if not quantidade_texto: return 1.0
    m = re.search(r"(\d+(?:[,.]?\d+)?)", quantidade_texto)
    if m:
        try:
            return max(0.1, min(10, float(m.group(1).replace(",", "."))))
        except ValueError:
            pass
    t = quantidade_texto.lower()
    if any(p in t for p in ["meia","metade"]): return 0.5
    if any(p in t for p in ["duas","dois"]):   return 2.0
    if any(p in t for p in ["tres","três"]):   return 3.0
    if "quatro" in t:                          return 4.0
    return 1.0


# ══════════════════════════════════════════════════════════════════════════════
# PORÇÃO N75
# ══════════════════════════════════════════════════════════════════════════════

def buscar_porcao_n75(nome_alimento, df_n75=None):
    TABELA_N75 = [
        (["torrada"],                                    30,  "Unidades"),
        (["biscoito salgado","cream cracker","grissine"],30,  "Unidades"),
        (["pao de forma","pao integral","pao fatiado"],  50,  "Unidades ou fatias"),
        (["pao frances","pao de queijo"],                50,  "Unidades"),
        (["aveia em flocos","aveia"],                    30,  "Colheres de sopa"),
        (["leite fluido","leite integral","leite desnatado"],200,"Copos"),
        (["iogurte","leite fermentado"],                200,  "Copos"),
        (["queijo ralado"],                              10,  "Colheres de sopa"),
        (["queijo cottage","ricota","queijo minas"],     50,  "Fatias"),
        (["ovo"],                                       None, "Unidades (peso variável)"),
        (["hamburguer"],                                 80,  "Unidades"),
        (["manteiga","margarina"],                       10,  "Colheres de sopa"),
        (["acucar"],                                      5,  "Colheres de chá"),
        (["refrigerante","cha gelado"],                 200,  "Copos"),
    ]
    nome_n = normalizar_texto_busca(nome_alimento)
    for palavras, porcao, medida in TABELA_N75:
        for chave in palavras:
            if normalizar_texto_busca(chave) in nome_n:
                return {"porcao_g_ml": porcao, "medida": medida, "encontrado": True}
    return {"porcao_g_ml": None, "medida": "porcao", "encontrado": False}


# ══════════════════════════════════════════════════════════════════════════════
# SCORE DE MATCH (compatibilidade)
# ══════════════════════════════════════════════════════════════════════════════

def calcular_score_match(palavras_busca, palavras_desc, nome_busca_norm, desc_norm):
    pb = set(palavras_busca); pd_ = set(palavras_desc)
    inter = pb.intersection(pd_)
    if not inter: return 0
    score = len(inter) / max(1, len(pb))
    if pb.issubset(pd_):                    score += 2.0
    if nome_busca_norm in desc_norm:        score += 3.0
    if desc_norm.startswith(nome_busca_norm): score += 1.0
    if nome_busca_norm == desc_norm:        score += 5.0
    extras = len(pd_) - len(inter)
    if extras > 3: score -= 0.1 * (extras - 3)
    return score


# Stubs de compatibilidade
def analisar_receita_com_gemini(client, texto_receita, perfil=None,
                                 df_taco=None, df_ibge=None, df_bio=None):
    return None

def extrair_alimentos_manual(texto_receita): return None
def buscar_na_tabela_taco(nome_alimento, df_taco): return None
def buscar_na_tabela_ibge(nome_alimento, df_ibge): return None
