# ia_gemini.py - VERSÃO HÍBRIDA (IA extrai + Busca nas tabelas)
import json
import re
import pandas as pd
import unicodedata


def configurar_gemini(api_key):
    """Mantido para compatibilidade - retorna None pois IA externa foi removida"""
    return None


def normalizar_texto_busca(texto):
    """Normaliza texto para busca nas tabelas"""
    if not texto or not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode("ASCII")
    texto = re.sub(r"[^a-z0-9\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def tratar_valor(valor):
    """Trata valores numéricos"""
    if valor is None or pd.isna(valor):
        return 0.0
    if isinstance(valor, str):
        valor = valor.strip().upper()
        if valor in ["NA", "N/A", "*", "TR", "-", ""]:
            return 0.0
        valor = valor.replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            return 0.0
    return float(valor) if not pd.isna(valor) else 0.0


def buscar_na_tabela_taco(nome_alimento, df_taco):
    """Busca o alimento na tabela TACO"""
    if df_taco is None or df_taco.empty:
        return None

    nome_norm = normalizar_texto_busca(nome_alimento)
    if not nome_norm:
        return None

    for _, row in df_taco.iterrows():
        descricao = row.get("Descrição dos alimentos", "")
        if not descricao:
            continue
        desc_norm = normalizar_texto_busca(descricao)

        if nome_norm in desc_norm or desc_norm in nome_norm:
            kcal = tratar_valor(row.get("Energia..kcal.", 0))
            if kcal > 0:
                return {
                    "kcal": kcal,
                    "proteina": tratar_valor(row.get("Proteína..g.", 0)),
                    "carboidrato": tratar_valor(row.get("Carboidrato..g.", 0)),
                    "gordura": tratar_valor(row.get("Lipídeos..g.", 0)),
                    "fonte": "TACO",
                }
    return None


def buscar_na_tabela_ibge(nome_alimento, df_ibge):
    """Busca o alimento na tabela IBGE"""
    if df_ibge is None or df_ibge.empty:
        return None

    nome_norm = normalizar_texto_busca(nome_alimento)
    if not nome_norm:
        return None

    for _, row in df_ibge.iterrows():
        descricao = row.get("descricao_completa", "") or row.get("descricao", "")
        if not descricao:
            continue
        desc_norm = normalizar_texto_busca(descricao)

        if nome_norm in desc_norm or desc_norm in nome_norm:
            kcal = tratar_valor(row.get("energia_kcal", 0))
            if kcal > 0:
                return {
                    "kcal": kcal,
                    "proteina": tratar_valor(row.get("proteina_g", 0)),
                    "carboidrato": tratar_valor(row.get("carboidrato_g", 0)),
                    "gordura": tratar_valor(row.get("lipideos_g", 0)),
                    "fonte": "IBGE",
                }
    return None


def estimativa_inteligente(nome_alimento):
    """
    Fallback quando não encontra nas tabelas TACO/IBGE.
    Valores por 100g baseados em referências nutricionais brasileiras.
    Expandido para cobrir mais categorias e derivados.
    """
    nome = nome_alimento.lower()

    # ── Pães, torradas e biscoitos ──
    if any(p in nome for p in ["pão", "pao", "torrada", "croissant", "broa"]):
        return {
            "kcal": 65,
            "proteina": 2.5,
            "carboidrato": 13,
            "gordura": 1.5,
            "fonte": "estimativa",
        }
    if any(
        p in nome
        for p in ["biscoito", "bolacha", "cream cracker", "agua e sal", "wafer"]
    ):
        return {
            "kcal": 67,
            "proteina": 1.5,
            "carboidrato": 12,
            "gordura": 2.0,
            "fonte": "estimativa",
        }

    # ── Cereais, massas e tubérculos ──
    if any(p in nome for p in ["arroz", "risoto"]):
        return {
            "kcal": 36,
            "proteina": 0.7,
            "carboidrato": 7.9,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(
        p in nome
        for p in ["macarrão", "macarrao", "espaguete", "lasanha", "talharim", "penne"]
    ):
        return {
            "kcal": 35,
            "proteina": 0.7,
            "carboidrato": 7.0,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["aveia", "granola", "mingau"]):
        return {
            "kcal": 70,
            "proteina": 2.5,
            "carboidrato": 12,
            "gordura": 1.4,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["batata doce", "batata-doce"]):
        return {
            "kcal": 77,
            "proteina": 1.3,
            "carboidrato": 18,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["batata", "pure de batata"]):
        return {
            "kcal": 52,
            "proteina": 1.2,
            "carboidrato": 12,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["aipim", "mandioca", "macaxeira"]):
        return {
            "kcal": 71,
            "proteina": 0.7,
            "carboidrato": 17,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["inhame", "cará"]):
        return {
            "kcal": 59,
            "proteina": 1.2,
            "carboidrato": 14,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["cuscuz", "cuscuze"]):
        return {
            "kcal": 40,
            "proteina": 0.9,
            "carboidrato": 8.5,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["tapioca"]):
        return {
            "kcal": 55,
            "proteina": 0.2,
            "carboidrato": 13.5,
            "gordura": 0.1,
            "fonte": "estimativa",
        }

    # ── Carnes vermelhas (Grupo 2A OMS) ──
    if any(
        p in nome
        for p in ["carne moida", "carne moída", "patinho moido", "carne bovina"]
    ):
        return {
            "kcal": 160,
            "proteina": 22,
            "carboidrato": 0,
            "gordura": 8.0,
            "fonte": "estimativa",
        }
    if any(
        p in nome
        for p in [
            "bife",
            "alcatra",
            "picanha",
            "contrafile",
            "contrafilé",
            "file mignon",
            "filé mignon",
        ]
    ):
        return {
            "kcal": 180,
            "proteina": 26,
            "carboidrato": 0,
            "gordura": 8.5,
            "fonte": "estimativa",
        }
    if any(
        p in nome
        for p in [
            "carne",
            "patinho",
            "acem",
            "açém",
            "maminha",
            "fraldinha",
            "costela bovina",
        ]
    ):
        return {
            "kcal": 170,
            "proteina": 25,
            "carboidrato": 0,
            "gordura": 7.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["carneiro", "cordeiro", "cabrito"]):
        return {
            "kcal": 185,
            "proteina": 24,
            "carboidrato": 0,
            "gordura": 9.5,
            "fonte": "estimativa",
        }

    # ── Carnes de porco ──
    if any(
        p in nome
        for p in [
            "pernil",
            "lombo",
            "bisteca suina",
            "bisteca suína",
            "costela de porco",
        ]
    ):
        return {
            "kcal": 195,
            "proteina": 22,
            "carboidrato": 0,
            "gordura": 11,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["bacon"]):
        return {
            "kcal": 450,
            "proteina": 12,
            "carboidrato": 0,
            "gordura": 45,
            "fonte": "estimativa",
        }

    # ── Frango e aves ──
    if any(p in nome for p in ["frango", "galinha", "peito", "coxa", "sobrecoxa"]):
        return {
            "kcal": 165,
            "proteina": 31,
            "carboidrato": 0,
            "gordura": 3.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["peru", "chester"]):
        return {
            "kcal": 170,
            "proteina": 29,
            "carboidrato": 0,
            "gordura": 5.5,
            "fonte": "estimativa",
        }

    # ── Peixes e frutos do mar ──
    if any(p in nome for p in ["salmão", "salmao"]):
        return {
            "kcal": 175,
            "proteina": 25,
            "carboidrato": 0,
            "gordura": 8.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["atum"]):
        return {
            "kcal": 130,
            "proteina": 29,
            "carboidrato": 0,
            "gordura": 1.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["sardinha"]):
        return {
            "kcal": 150,
            "proteina": 24,
            "carboidrato": 0,
            "gordura": 6.0,
            "fonte": "estimativa",
        }
    if any(
        p in nome
        for p in ["peixe", "tilapia", "tilápia", "merluza", "robalo", "dourado"]
    ):
        return {
            "kcal": 110,
            "proteina": 22,
            "carboidrato": 0,
            "gordura": 2.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["camarao", "camarão"]):
        return {
            "kcal": 85,
            "proteina": 18,
            "carboidrato": 0.9,
            "gordura": 1.0,
            "fonte": "estimativa",
        }

    # ── Ovos ──
    if any(p in nome for p in ["ovo", "omelete", "ovos mexidos", "ovos cozidos"]):
        return {
            "kcal": 75,
            "proteina": 6.3,
            "carboidrato": 0.6,
            "gordura": 5.0,
            "fonte": "estimativa",
        }

    # ── Leguminosas ──
    if any(p in nome for p in ["feijão", "feijao"]):
        return {
            "kcal": 77,
            "proteina": 4.8,
            "carboidrato": 14,
            "gordura": 0.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["lentilha"]):
        return {
            "kcal": 93,
            "proteina": 6.3,
            "carboidrato": 16,
            "gordura": 0.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["ervilha"]):
        return {
            "kcal": 77,
            "proteina": 5.0,
            "carboidrato": 14,
            "gordura": 0.3,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["grao de bico", "grão de bico"]):
        return {
            "kcal": 120,
            "proteina": 7.0,
            "carboidrato": 20,
            "gordura": 2.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["soja"]):
        return {
            "kcal": 80,
            "proteina": 8.0,
            "carboidrato": 6.0,
            "gordura": 3.5,
            "fonte": "estimativa",
        }

    # ── Laticínios e derivados ──
    if any(
        p in nome for p in ["leite integral", "leite desnatado", "leite semidesnatado"]
    ):
        return {
            "kcal": 61,
            "proteina": 3.2,
            "carboidrato": 4.7,
            "gordura": 3.3,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["leite"]):
        return {
            "kcal": 55,
            "proteina": 3.0,
            "carboidrato": 4.5,
            "gordura": 2.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["iogurte desnatado", "iogurte natural desnatado"]):
        return {
            "kcal": 35,
            "proteina": 3.6,
            "carboidrato": 4.8,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["iogurte grego"]):
        return {
            "kcal": 97,
            "proteina": 9.0,
            "carboidrato": 6.0,
            "gordura": 3.8,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["iogurte"]):
        return {
            "kcal": 51,
            "proteina": 4.1,
            "carboidrato": 4.0,
            "gordura": 1.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["queijo minas", "queijo-minas"]):
        return {
            "kcal": 264,
            "proteina": 17,
            "carboidrato": 3.2,
            "gordura": 20,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["queijo cottage"]):
        return {
            "kcal": 98,
            "proteina": 11,
            "carboidrato": 3.4,
            "gordura": 4.3,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["queijo"]):
        return {
            "kcal": 280,
            "proteina": 18,
            "carboidrato": 2.5,
            "gordura": 22,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["requeijao", "requeijão"]):
        return {
            "kcal": 188,
            "proteina": 7.5,
            "carboidrato": 4.0,
            "gordura": 16,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["ricota"]):
        return {
            "kcal": 134,
            "proteina": 11,
            "carboidrato": 3.0,
            "gordura": 9.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["manteiga"]):
        return {
            "kcal": 726,
            "proteina": 0.5,
            "carboidrato": 0.1,
            "gordura": 81,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["creme de leite"]):
        return {
            "kcal": 300,
            "proteina": 2.5,
            "carboidrato": 3.5,
            "gordura": 30,
            "fonte": "estimativa",
        }

    # ── Frutas ──
    if any(p in nome for p in ["banana prata", "banana nanica", "banana da terra"]):
        return {
            "kcal": 89,
            "proteina": 1.1,
            "carboidrato": 23,
            "gordura": 0.3,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["banana"]):
        return {
            "kcal": 87,
            "proteina": 1.1,
            "carboidrato": 22,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["maçã", "maca"]):
        return {
            "kcal": 56,
            "proteina": 0.3,
            "carboidrato": 15,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["laranja"]):
        return {
            "kcal": 47,
            "proteina": 0.9,
            "carboidrato": 12,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["mamão", "mamao", "papaya"]):
        return {
            "kcal": 40,
            "proteina": 0.5,
            "carboidrato": 10,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["melancia"]):
        return {
            "kcal": 30,
            "proteina": 0.6,
            "carboidrato": 8.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["melão", "melao"]):
        return {
            "kcal": 29,
            "proteina": 0.7,
            "carboidrato": 7.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["abacaxi"]):
        return {
            "kcal": 50,
            "proteina": 0.5,
            "carboidrato": 13,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["manga"]):
        return {
            "kcal": 65,
            "proteina": 0.5,
            "carboidrato": 17,
            "gordura": 0.3,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["uva"]):
        return {
            "kcal": 69,
            "proteina": 0.6,
            "carboidrato": 18,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["morango"]):
        return {
            "kcal": 30,
            "proteina": 0.7,
            "carboidrato": 7.0,
            "gordura": 0.3,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["ameixa"]):
        return {
            "kcal": 46,
            "proteina": 0.7,
            "carboidrato": 11,
            "gordura": 0.3,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["pera"]):
        return {
            "kcal": 53,
            "proteina": 0.3,
            "carboidrato": 14,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["goiaba"]):
        return {
            "kcal": 54,
            "proteina": 2.6,
            "carboidrato": 10,
            "gordura": 1.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["abacate"]):
        return {
            "kcal": 160,
            "proteina": 2.0,
            "carboidrato": 6.0,
            "gordura": 15,
            "fonte": "estimativa",
        }

    # ── Hortaliças e verduras ──
    if any(p in nome for p in ["alface"]):
        return {
            "kcal": 11,
            "proteina": 1.3,
            "carboidrato": 2.0,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["tomate"]):
        return {
            "kcal": 15,
            "proteina": 1.1,
            "carboidrato": 3.1,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["couve", "couve-flor", "brocolis", "brócolis"]):
        return {
            "kcal": 25,
            "proteina": 2.1,
            "carboidrato": 4.4,
            "gordura": 0.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["cenoura"]):
        return {
            "kcal": 30,
            "proteina": 0.8,
            "carboidrato": 7.0,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["beterraba"]):
        return {
            "kcal": 29,
            "proteina": 1.0,
            "carboidrato": 6.5,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["chuchu"]):
        return {
            "kcal": 17,
            "proteina": 0.7,
            "carboidrato": 4.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["abobrinha", "abobrinha d'água"]):
        return {
            "kcal": 15,
            "proteina": 1.0,
            "carboidrato": 3.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["berinjela"]):
        return {
            "kcal": 24,
            "proteina": 0.9,
            "carboidrato": 5.5,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["pepino"]):
        return {
            "kcal": 10,
            "proteina": 0.7,
            "carboidrato": 2.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["pimentao", "pimentão"]):
        return {
            "kcal": 20,
            "proteina": 0.9,
            "carboidrato": 4.6,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["abobora", "abóbora"]):
        return {
            "kcal": 26,
            "proteina": 1.0,
            "carboidrato": 6.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["vagem"]):
        return {
            "kcal": 31,
            "proteina": 1.8,
            "carboidrato": 7.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["quiabo"]):
        return {
            "kcal": 23,
            "proteina": 1.5,
            "carboidrato": 5.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(
        p in nome
        for p in ["espinafre", "acelga", "rucula", "rúcula", "agriao", "agrião"]
    ):
        return {
            "kcal": 18,
            "proteina": 2.0,
            "carboidrato": 2.5,
            "gordura": 0.3,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["repolho"]):
        return {
            "kcal": 16,
            "proteina": 0.9,
            "carboidrato": 3.5,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["nabo"]):
        return {
            "kcal": 22,
            "proteina": 0.9,
            "carboidrato": 5.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["salada"]):
        return {
            "kcal": 14,
            "proteina": 0.8,
            "carboidrato": 3.0,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["legumes"]):
        return {
            "kcal": 30,
            "proteina": 1.5,
            "carboidrato": 6.0,
            "gordura": 0.2,
            "fonte": "estimativa",
        }

    # ── Oleaginosas ──
    if any(p in nome for p in ["castanha do para", "castanha do pará"]):
        return {
            "kcal": 656,
            "proteina": 14,
            "carboidrato": 12,
            "gordura": 64,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["castanha de caju"]):
        return {
            "kcal": 570,
            "proteina": 18,
            "carboidrato": 29,
            "gordura": 46,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["amendoim"]):
        return {
            "kcal": 544,
            "proteina": 25,
            "carboidrato": 20,
            "gordura": 44,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["nozes", "amendoa", "amêndoa"]):
        return {
            "kcal": 596,
            "proteina": 21,
            "carboidrato": 11,
            "gordura": 54,
            "fonte": "estimativa",
        }

    # ── Gorduras e óleos ──
    if any(p in nome for p in ["azeite", "oliva"]):
        return {
            "kcal": 884,
            "proteina": 0.0,
            "carboidrato": 0.0,
            "gordura": 100,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["oleo", "óleo"]):
        return {
            "kcal": 884,
            "proteina": 0.0,
            "carboidrato": 0.0,
            "gordura": 100,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["margarina"]):
        return {
            "kcal": 540,
            "proteina": 0.5,
            "carboidrato": 1.0,
            "gordura": 60,
            "fonte": "estimativa",
        }

    # ── Bebidas ──
    if any(
        p in nome
        for p in ["suco de laranja", "suco de uva", "suco de abacaxi", "suco natural"]
    ):
        return {
            "kcal": 42,
            "proteina": 0.6,
            "carboidrato": 10,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["cafe", "café"]):
        return {
            "kcal": 2,
            "proteina": 0.3,
            "carboidrato": 0.0,
            "gordura": 0.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["cha", "chá"]):
        return {
            "kcal": 1,
            "proteina": 0.0,
            "carboidrato": 0.2,
            "gordura": 0.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["vitamina de", "vitamina com"]):
        return {
            "kcal": 75,
            "proteina": 3.0,
            "carboidrato": 13,
            "gordura": 1.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["refrigerante"]):
        return {
            "kcal": 40,
            "proteina": 0.0,
            "carboidrato": 10,
            "gordura": 0.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["agua de coco", "água de coco"]):
        return {
            "kcal": 19,
            "proteina": 0.7,
            "carboidrato": 4.5,
            "gordura": 0.2,
            "fonte": "estimativa",
        }

    # ── Preparações e pratos ──
    if any(p in nome for p in ["sopa de legumes", "caldo de legumes"]):
        return {
            "kcal": 35,
            "proteina": 1.5,
            "carboidrato": 6.0,
            "gordura": 0.5,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["pure", "purê"]):
        return {
            "kcal": 72,
            "proteina": 1.5,
            "carboidrato": 15,
            "gordura": 1.0,
            "fonte": "estimativa",
        }
    if any(p in nome for p in ["refogado", "refogad"]):
        return {
            "kcal": 45,
            "proteina": 1.2,
            "carboidrato": 7.0,
            "gordura": 1.5,
            "fonte": "estimativa",
        }

    # ── Fallback genérico ──
    else:
        return {
            "kcal": 50,
            "proteina": 2.0,
            "carboidrato": 8.0,
            "gordura": 1.5,
            "fonte": "estimativa",
        }


def extrair_fator_quantidade(quantidade_texto):
    """Extrai fator multiplicador da quantidade (ex: 2 fatias → fator 2)"""
    if not quantidade_texto:
        return 1.0

    match = re.search(r"(\d+(?:[,.]?\d+)?)", quantidade_texto)
    if match:
        try:
            num = float(match.group(1).replace(",", "."))
            return max(0.1, min(10, num))
        except ValueError:
            pass

    texto = quantidade_texto.lower()
    if any(p in texto for p in ["meia", "metade"]):
        return 0.5
    elif any(p in texto for p in ["duas", "dois"]):
        return 2.0
    elif any(p in texto for p in ["três", "tres"]):
        return 3.0
    elif any(p in texto for p in ["quatro"]):
        return 4.0
    return 1.0


def analisar_receita_com_gemini(
    client, texto_receita, perfil=None, df_taco=None, df_ibge=None
):
    """Usa o Gemini para extrair alimentos e busca valores nas tabelas"""
    if not texto_receita or not client:
        return None

    prompt = f"""
    Extraia TODOS os alimentos deste cardápio. Retorne APENAS JSON.

    CARDÁPIO:
    {texto_receita}

    FORMATO EXATO:
    {{
        "alimentos": [
            {{
                "nome": "pão integral",
                "quantidade": "2 fatias",
                "refeicao": "Café da Manhã",
                "dia": "Segunda"
            }}
        ]
    }}

    REGRAS:
    1. Dias: Segunda, Terça, Quarta, Quinta, Sexta, Sábado, Domingo
    2. Refeições: "Café da Manhã", "Almoço", "Lanches", "Jantar"
    3. NÃO calcule calorias - apenas extraia nome, quantidade, refeicao, dia
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={"temperature": 0.1, "top_p": 0.95, "max_output_tokens": 8192},
        )

        texto_limpo = response.text.strip()
        texto_limpo = re.sub(r"```json\s*", "", texto_limpo)
        texto_limpo = re.sub(r"```\s*", "", texto_limpo)

        json_match = re.search(r"\{.*\}", texto_limpo, re.DOTALL)
        if json_match:
            texto_limpo = json_match.group(0)

        resultado = json.loads(texto_limpo)

        if "alimentos" not in resultado or not resultado["alimentos"]:
            return None

        dias_validos = [
            "Segunda",
            "Terça",
            "Quarta",
            "Quinta",
            "Sexta",
            "Sábado",
            "Domingo",
        ]
        refeicoes_validas = ["Café da Manhã", "Almoço", "Lanches", "Jantar"]

        for item in resultado["alimentos"]:
            if "dia" not in item or item["dia"] not in dias_validos:
                item["dia"] = "Segunda"
            if "refeicao" not in item or item["refeicao"] not in refeicoes_validas:
                item["refeicao"] = "Lanches"

            nome_alimento = item.get("nome", "")

            # Buscar valores nutricionais
            valores = None
            if df_taco is not None and not df_taco.empty:
                valores = buscar_na_tabela_taco(nome_alimento, df_taco)
            if valores is None and df_ibge is not None and not df_ibge.empty:
                valores = buscar_na_tabela_ibge(nome_alimento, df_ibge)
            if valores is None:
                valores = estimativa_inteligente(nome_alimento)

            quantidade_texto = item.get("quantidade", "1 porção")
            fator = extrair_fator_quantidade(quantidade_texto)

            item["kcal"] = round(valores["kcal"] * fator, 1)
            item["proteina"] = round(valores["proteina"] * fator, 1)
            item["carboidrato"] = round(valores["carboidrato"] * fator, 1)
            item["gordura"] = round(valores["gordura"] * fator, 1)

        return resultado

    except Exception as e:
        print(f"Erro: {e}")
        return None


def extrair_alimentos_manual(texto_receita):
    """Fallback de emergência"""
    return None
