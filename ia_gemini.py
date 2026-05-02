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
    """Fallback quando não encontra nas tabelas"""
    nome = nome_alimento.lower()

    if any(p in nome for p in ["pão", "torrada", "biscoito", "croissant"]):
        return {
            "kcal": 65,
            "proteina": 2.5,
            "carboidrato": 13,
            "gordura": 1.5,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["arroz", "macarrão", "macarrao", "espaguete"]):
        return {
            "kcal": 35,
            "proteina": 0.7,
            "carboidrato": 7,
            "gordura": 0.2,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["batata", "aipim", "mandioca", "inhame"]):
        return {
            "kcal": 75,
            "proteina": 1.2,
            "carboidrato": 18,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["frango", "galinha", "peito"]):
        return {
            "kcal": 165,
            "proteina": 31,
            "carboidrato": 0,
            "gordura": 3.5,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["carne", "bife", "patinho", "alcatra"]):
        return {
            "kcal": 180,
            "proteina": 30,
            "carboidrato": 0,
            "gordura": 7,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["peixe", "salmão", "atum", "sardinha"]):
        return {
            "kcal": 140,
            "proteina": 26,
            "carboidrato": 0,
            "gordura": 5,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["feijão", "lentilha", "ervilha"]):
        return {
            "kcal": 85,
            "proteina": 6,
            "carboidrato": 14,
            "gordura": 0.5,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["leite", "iogurte", "queijo", "ricota"]):
        return {
            "kcal": 60,
            "proteina": 4,
            "carboidrato": 5,
            "gordura": 3,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["banana", "maçã", "laranja"]):
        return {
            "kcal": 80,
            "proteina": 0.5,
            "carboidrato": 20,
            "gordura": 0.3,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["alface", "tomate", "couve", "brócolis"]):
        return {
            "kcal": 15,
            "proteina": 1,
            "carboidrato": 3,
            "gordura": 0.1,
            "fonte": "estimativa",
        }
    elif any(p in nome for p in ["ovo", "omelete"]):
        return {
            "kcal": 75,
            "proteina": 6,
            "carboidrato": 0.6,
            "gordura": 5,
            "fonte": "estimativa",
        }
    else:
        return {
            "kcal": 50,
            "proteina": 2,
            "carboidrato": 8,
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
