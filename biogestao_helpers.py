"""
biogestao_helpers.py  —  BioGestão 360
=======================================
Módulo auxiliar para a seção 26 (Montagem do Plano Alimentar).

Resolve três problemas:
  1. Nomes com/sem acento — normaliza para busca sem tocar o dicionário do app.py
  2. Duplicados por marca — seletor de marca dinâmico na seção 26
  3. Peso por unidade — usa porcao_num do banco primeiro, dicionário como fallback

Import no app.py:
    from biogestao_helpers import (
        preparar_lista_alimentos,
        obter_marcas_disponiveis,
        obter_item_selecionado,
        obter_peso_unidade_item,
    )
"""

import unicodedata
import re
import pandas as pd


# ── Normalização ──────────────────────────────────────────────────────────────

def _norm(texto):
    """Normaliza texto: minúsculo, sem acento, sem espaço duplo."""
    if not texto or not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode("ASCII")
    return re.sub(r"\s+", " ", texto).strip()


# ── 1. Preparar lista de alimentos para o selectbox ──────────────────────────

def preparar_lista_alimentos(df_filtrado):
    """
    Retorna lista de nomes ÚNICOS ordenados para o selectbox de alimentos.
    
    Estratégia: agrupa por nome normalizado e usa o nome com a grafia
    mais completa (com acentos, preferindo letras maiúsculas no início).
    Isso elimina os 3.617 duplicados nome/acento do seletor.
    
    Retorna: list[str] — nomes únicos para exibir no selectbox.
    """
    if df_filtrado is None or df_filtrado.empty:
        return []

    df = df_filtrado[df_filtrado["nome"].notna()].copy()
    df["_norm"] = df["nome"].apply(_norm)

    # Para cada grupo de nomes normalizados iguais, escolher o melhor representante:
    # prefere o que tem mais letras maiúsculas corretas (acentuado) e é mais curto
    def melhor_nome(nomes):
        # Entre as variantes, prefer a que tem acentos (á, ã, ç, etc.)
        com_acento = [n for n in nomes if any(c in n for c in "áéíóúâêîôûãõàèìòùäëïöüçñ")]
        grupo = com_acento if com_acento else list(nomes)
        # Dentro do grupo, preferir o mais curto (evita nomes com marcas embutidas)
        return sorted(grupo, key=lambda x: (len(x), x))[0]

    representantes = (
        df.groupby("_norm")["nome"]
        .apply(lambda s: melhor_nome(s.tolist()))
        .reset_index(drop=True)
        .sort_values()
        .tolist()
    )

    return representantes


# ── 2. Obter marcas disponíveis para um alimento ─────────────────────────────

def obter_marcas_disponiveis(df_filtrado, nome_alimento):
    """
    Retorna lista de marcas disponíveis para um nome de alimento.
    
    Lógica:
      - Busca por nome normalizado (resolve acento/maiúscula)
      - Se só uma marca (ou nenhuma): retorna ["(padrão)"]
      - Se várias marcas: retorna ["(qualquer marca)"] + marcas ordenadas
      - Produtos sem marca entram como "(sem marca)"
    
    Returns: list[str]
    """
    if df_filtrado is None or df_filtrado.empty:
        return ["(padrão)"]

    nome_n = _norm(nome_alimento)
    df = df_filtrado.copy()
    df["_norm"] = df["nome"].apply(_norm)
    df_match = df[df["_norm"] == nome_n]

    if df_match.empty:
        # Fallback: busca parcial
        df_match = df[df["_norm"].str.contains(nome_n, na=False)]

    if df_match.empty:
        return ["(padrão)"]

    marcas = df_match["marca"].dropna().unique().tolist()
    marcas = sorted([m for m in marcas if str(m).strip()])

    tem_sem_marca = df_match["marca"].isna().any() or \
                    df_match["marca"].apply(lambda x: str(x).strip() == "").any()

    if not marcas and not tem_sem_marca:
        return ["(padrão)"]

    opcoes = []
    if len(marcas) > 1 or (marcas and tem_sem_marca):
        opcoes.append("(qualquer marca)")
    if tem_sem_marca and marcas:
        opcoes.append("(sem marca)")
    opcoes.extend(marcas)

    return opcoes if opcoes else ["(padrão)"]


# ── 3. Obter item selecionado do DataFrame ────────────────────────────────────

def obter_item_selecionado(df_filtrado, nome_alimento, marca_selecionada="(qualquer marca)"):
    """
    Retorna a linha (Series) do DataFrame que corresponde ao alimento e marca.
    
    Lógica de seleção:
      1. Filtra por nome normalizado
      2. Se marca específica: filtra por ela
      3. Se "(sem marca)": filtra onde marca é nula
      4. Se "(qualquer marca)" ou "(padrão)": pega o primeiro com melhor kcal
      5. Fallback: primeiro da lista
    
    Returns: pd.Series ou None
    """
    if df_filtrado is None or df_filtrado.empty:
        return None

    df = df_filtrado.copy()
    df["_norm"] = df["nome"].apply(_norm)
    nome_n = _norm(nome_alimento)

    # Filtrar por nome normalizado
    df_match = df[df["_norm"] == nome_n]

    if df_match.empty:
        # Fallback: busca o nome exato (caso o nome já seja exato)
        df_match = df[df["nome"] == nome_alimento]

    if df_match.empty:
        return None

    # Filtrar por marca
    if marca_selecionada not in ("(qualquer marca)", "(padrão)", ""):
        if marca_selecionada == "(sem marca)":
            df_filtrado_marca = df_match[df_match["marca"].isna() |
                                          (df_match["marca"].astype(str).str.strip() == "")]
        else:
            df_filtrado_marca = df_match[
                df_match["marca"].astype(str).str.strip() == marca_selecionada.strip()
            ]
        if not df_filtrado_marca.empty:
            df_match = df_filtrado_marca

    # Entre os candidatos, preferir o com mais campos preenchidos
    df_match = df_match.copy()
    df_match["_completude"] = (
        df_match[["kcal_100g", "proteina_g", "carboidrato_g", "gordura_g"]]
        .notna()
        .sum(axis=1)
    )
    df_match = df_match.sort_values("_completude", ascending=False)

    return df_match.iloc[0]


# ── 4. Obter peso por unidade ─────────────────────────────────────────────────

def obter_peso_unidade_item(item, nome_alimento=""):
    """
    Retorna o peso de UMA unidade do alimento em gramas.
    
    Hierarquia:
      1. porcao_num do banco (dado real do rótulo)
      2. porcao_uni deve ser 'g' (não ml)
      3. Fallback: dicionário TACO/N75 interno
      4. Fallback final: 0 (não foi possível determinar)
    
    Args:
      item: pd.Series — linha do DataFrame do alimento
      nome_alimento: str — nome para busca no dicionário fallback
    
    Returns: float — peso em gramas (0 se não encontrado)
    """
    # 1. Tentar porcao_num do banco
    try:
        porcao_num = float(item.get("porcao_num") or 0)
        porcao_uni = str(item.get("porcao_uni") or "g").strip().lower()
        if porcao_num > 0 and porcao_uni == "g":
            return porcao_num
        # Se for ml, não serve como peso em gramas para unidade sólida
        # mas se o alimento for líquido e selecionou "un", usa mesmo assim
        if porcao_num > 0:
            return porcao_num
    except (TypeError, ValueError):
        pass

    # 2. Fallback: dicionário interno (TACO/IN 75/2020)
    nome = (nome_alimento or str(item.get("nome", ""))).lower()
    nome_n = _norm(nome)

    # Tabela de pesos por unidade — normatizada para busca sem acento
    _PESOS = {
        # Pães
        "pao frances": 50, "pao de sal": 50, "pao de queijo": 30,
        "pao de forma": 25, "pao integral": 25, "pao de hamburguer": 50,
        "croissant": 45, "brioche": 40, "pao doce": 40, "panetone": 80,
        "pao de batata": 40, "pao de hot dog": 50, "pao sirio": 50,
        # Biscoitos
        "biscoito doce": 5, "biscoito recheado": 10, "biscoito salgado": 5,
        "cream cracker": 5, "agua e sal": 5, "wafer": 10, "maisena": 5,
        "bolacha": 5, "cracker": 5, "sequilho": 5, "rosquinha": 6,
        "torrada": 10, "biscoito polvilho": 5, "biscoito integral": 5,
        # Frutas
        "maca": 150, "banana": 100, "banana prata": 100, "banana nanica": 100,
        "banana da terra": 150, "laranja": 120, "pera": 130, "manga": 200,
        "melao": 300, "melancia": 400, "abacaxi": 500, "uva": 5,
        "morango": 12, "kiwi": 70, "ameixa": 30, "pessego": 80,
        "goiaba": 100, "caqui": 100, "abacate": 200, "mamao": 150,
        "figo": 40, "tangerina": 100, "mexerica": 100, "cereja": 5,
        # Ovos
        "ovo": 50, "ovo de galinha": 50, "ovo de codorna": 9, "omelete": 80,
        # Queijos
        "queijo minas": 30, "queijo branco": 30, "queijo prato": 20,
        "queijo mussarela": 20, "mussarela": 20, "mucArela": 20,
        "queijo coalho": 30, "queijo provolone": 20, "queijo parmesao": 15,
        "queijo ralado": 10, "ricota": 25, "queijo cottage": 25,
        "requeijao": 15, "queijo cremoso": 15,
        # Frios
        "presunto": 15, "apresuntado": 15, "mortadela": 15, "salame": 10,
        "peito de peru": 15, "hamburguer": 80, "linguica": 60, "salsicha": 50,
        "bacon": 10,
        # Hortaliças
        "cenoura": 50, "beterraba": 60, "batata": 100, "batata inglesa": 100,
        "batata doce": 100, "tomate": 80, "cebola": 100, "pimentao": 100,
        "abobrinha": 150, "berinjela": 150, "chuchu": 150, "couve-flor": 200,
        "brocolis": 200, "pepino": 100, "vagem": 50, "alface": 30,
        "rucula": 30, "espinafre": 30, "couve": 30, "repolho": 30,
        # Oleaginosas
        "castanha do para": 4, "castanha de caju": 3, "amendoa": 2,
        "nozes": 5, "avela": 3, "amendoim": 1,
        # Outros
        "chocolate": 25, "bombom": 25, "barra de cereal": 25,
        "sorvete": 60, "picole": 60, "bolo": 60,
        "mandioca": 100, "aipim": 100, "inhame": 100, "milho": 100,
    }

    # Busca exata primeiro
    if nome_n in _PESOS:
        return _PESOS[nome_n]

    # Busca parcial: chave contida no nome normalizado
    # ordena pelas chaves mais longas (mais específicas) primeiro
    for chave, peso in sorted(_PESOS.items(), key=lambda x: -len(x[0])):
        if chave in nome_n:
            return peso

    return 0


# ── 5. Resumo dos dados do item para exibição ─────────────────────────────────

def resumo_item(item, nome_alimento=""):
    """
    Retorna dict com informações de exibição do item selecionado.
    Útil para mostrar ao usuário antes de adicionar ao cardápio.
    """
    marca = item.get("marca")
    marca_str = str(marca).strip() if pd.notna(marca) and str(marca).strip() else "—"
    porcao_num = item.get("porcao_num")
    porcao_uni = item.get("porcao_uni") or "g"
    porcao_str = f"{porcao_num:.0f}{porcao_uni}" if pd.notna(porcao_num) and porcao_num else "—"

    return {
        "nome": item.get("nome", nome_alimento),
        "marca": marca_str,
        "porcao_referencia": porcao_str,
        "kcal_100g": item.get("kcal_100g"),
        "proteina_g": item.get("proteina_g"),
        "carboidrato_g": item.get("carboidrato_g"),
        "gordura_g": item.get("gordura_g"),
    }
