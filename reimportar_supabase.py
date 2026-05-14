"""
reimportar_supabase.py  —  BioGestão 360  v2.0
================================================
Usa TRUNCATE + importa CSV corrigido direto no banco via psycopg2.
Estrutura confirmada do banco:
  nome, marca, porcao_g_ml(real), kcal_100g, proteina_g, carboidrato_g,
  gordura_g, acucar_g, gordura_saturada_g, gordura_trans_g,
  fibra_g, sodio_g, fonte, porcao_num, porcao_uni
  (id e criado_em são automáticos)

COMO USAR:
  pip install psycopg2-binary
  python reimportar_supabase.py
"""

import os, sys, math
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

ARQUIVO_CSV = "biogestao_foods_corrigido.csv"
TABELA      = "biogestao_foods"
LOTE        = 500


def carregar_url_banco():
    url = os.environ.get("SUPABASE_DB_URL", "").strip()
    if url:
        return url
    base = os.path.dirname(os.path.abspath(__file__))
    for pasta in [base, os.path.join(base,".."), os.path.join(base,"..","..") ]:
        secrets = os.path.join(pasta, ".streamlit", "secrets.toml")
        if os.path.exists(secrets):
            with open(secrets, encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if linha.upper().startswith("SUPABASE_DB_URL"):
                        partes = linha.split("=", 1)
                        if len(partes) == 2:
                            return partes[1].strip().strip('"').strip("'")
    print("ERRO: SUPABASE_DB_URL nao encontrada em secrets.toml")
    sys.exit(1)


def nulo(v):
    if v is None:
        return None
    try:
        if math.isnan(float(v)):
            return None
        return v
    except (TypeError, ValueError):
        s = str(v).strip()
        return None if s in ("", "nan", "NaN", "None") else v


def linha_para_tupla(row):
    # Ordem exata do INSERT abaixo
    # porcao_g_ml recebe porcao_num (banco espera REAL, nao texto)
    return (
        nulo(row.get("nome")),
        nulo(row.get("marca")),
        nulo(row.get("porcao_num")),          # -> porcao_g_ml (real)
        nulo(row.get("kcal_100g")),
        nulo(row.get("proteina_g")),
        nulo(row.get("carboidrato_g")),
        nulo(row.get("gordura_g")),
        nulo(row.get("acucar_g")),
        nulo(row.get("gordura_saturada_g")),
        nulo(row.get("gordura_trans_g")),
        nulo(row.get("fibra_g")),
        nulo(row.get("sodio_g")),
        nulo(row.get("fonte")) or "Open Food Facts",
        nulo(row.get("porcao_num")),          # -> porcao_num
        nulo(row.get("porcao_uni")),          # -> porcao_uni
    )


SQL_INSERT = """
    INSERT INTO biogestao_foods (
        nome, marca, porcao_g_ml,
        kcal_100g, proteina_g, carboidrato_g,
        gordura_g, acucar_g, gordura_saturada_g, gordura_trans_g,
        fibra_g, sodio_g, fonte,
        porcao_num, porcao_uni
    ) VALUES %s
"""


def progresso(atual, total, larg=40):
    pct = atual / total if total else 0
    b   = int(larg * pct)
    bar = chr(9608)*b + chr(9617)*(larg-b)
    return f"[{bar}] {pct*100:5.1f}%  {atual:>6,}/{total:,}"


def main():
    inicio = datetime.now()
    print("="*60)
    print("  BioGestao 360 - Reimportacao Supabase  v2.0")
    print("="*60)

    # --- Carregar CSV ---
    if not os.path.exists(ARQUIVO_CSV):
        print(f"\nERRO: {ARQUIVO_CSV} nao encontrado")
        sys.exit(1)

    print(f"\nCarregando {ARQUIVO_CSV}...")
    df = pd.read_csv(ARQUIVO_CSV, encoding="utf-8", low_memory=False)
    df = df[df["nome"].notna() & df["kcal_100g"].notna()].reset_index(drop=True)
    total = len(df)
    print(f"  {total:,} produtos validos")

    sodio_max = pd.to_numeric(df["sodio_g"], errors="coerce").max()
    g_ct  = (df["porcao_uni"] == "g").sum()
    ml_ct = (df["porcao_uni"] == "ml").sum()
    print(f"  porcao_uni: g={g_ct:,}  ml={ml_ct:,}")
    print(f"  sodio max: {sodio_max:.4f} g = {sodio_max*1000:.0f} mg/100g")

    # --- Conectar ---
    url = carregar_url_banco()
    print(f"\nConectando ao Supabase...")
    try:
        conn = psycopg2.connect(url, connect_timeout=30, sslmode="require")
        conn.autocommit = False
        cur  = conn.cursor()
        print("  Conexao OK")
    except Exception as e:
        print(f"ERRO na conexao: {e}")
        sys.exit(1)

    try:
        # --- TRUNCATE ---
        print(f"\nLimpando tabela (TRUNCATE RESTART IDENTITY)...")
        cur.execute(f"TRUNCATE TABLE {TABELA} RESTART IDENTITY;")
        conn.commit()
        print("  Limpo OK")

        # --- Importar ---
        print(f"\nImportando {total:,} produtos em lotes de {LOTE}...\n")
        n_lotes   = math.ceil(total / LOTE)
        inseridos = 0
        erros     = 0

        for i in range(n_lotes):
            bloco = df.iloc[i*LOTE : (i+1)*LOTE]
            dados = [linha_para_tupla(row) for _, row in bloco.iterrows()]
            dados = [d for d in dados if d[0] is not None and d[3] is not None]
            if not dados:
                continue
            try:
                execute_values(cur, SQL_INSERT, dados, page_size=LOTE)
                conn.commit()
                inseridos += len(dados)
            except Exception as e:
                conn.rollback()
                erros += len(dados)
                print(f"\n  AVISO lote {i+1}: {e}")
                # fallback linha a linha
                for tupla in dados:
                    try:
                        cur.execute(
                            """INSERT INTO biogestao_foods
                            (nome,marca,porcao_g_ml,kcal_100g,proteina_g,
                             carboidrato_g,gordura_g,acucar_g,gordura_saturada_g,
                             gordura_trans_g,fibra_g,sodio_g,fonte,porcao_num,porcao_uni)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            tupla)
                        conn.commit()
                        inseridos += 1
                        erros -= 1
                    except Exception:
                        conn.rollback()

            print(f"\r  {progresso(inseridos, total)}", end="", flush=True)

        print()

        # --- Verificacao ---
        print("\nVerificando resultado...\n")

        cur.execute(f"SELECT COUNT(*) FROM {TABELA};")
        count_final = cur.fetchone()[0]

        cur.execute(f"""
            SELECT porcao_uni, COUNT(*)
            FROM {TABELA} GROUP BY porcao_uni ORDER BY 1;
        """)
        dist_uni = cur.fetchall()

        cur.execute(f"""
            SELECT MAX(sodio_g), ROUND(AVG(sodio_g)::numeric, 5)
            FROM {TABELA} WHERE sodio_g IS NOT NULL;
        """)
        s_max, s_avg = cur.fetchone()

        cur.execute(f"""
            SELECT nome, ROUND(sodio_g::numeric,4)
            FROM {TABELA}
            WHERE nome ILIKE '%frango grelhado%'
              AND sodio_g IS NOT NULL
            LIMIT 3;
        """)
        frango = cur.fetchall()

        print("="*60)
        print("  RESULTADO")
        print("="*60)
        print(f"  Inseridos : {count_final:,}  |  Erros: {erros}")
        print()
        print("  porcao_uni no banco:")
        for uni, cnt in dist_uni:
            print(f"    {str(uni or 'NULL'):<6} -> {cnt:>6,}")
        print()
        print(f"  sodio max : {s_max:.4f} g = {float(s_max)*1000:.1f} mg/100g")
        print(f"  sodio med : {s_avg} g = {float(s_avg)*1000:.1f} mg/100g")
        print()
        if frango:
            print("  Verificacao frango grelhado:")
            for nome, sod in frango:
                print(f"    {nome[:50]}: sodio={sod}g = {float(sod)*1000:.1f}mg/100g")
            print("    Esperado: ~29.6 mg  (antes era 74.000 mg - bug corrigido)")

    except Exception as e:
        conn.rollback()
        print(f"\nERRO critico: {e}")
        raise
    finally:
        cur.close()
        conn.close()

    seg = int((datetime.now()-inicio).total_seconds())
    print(f"\n  Tempo: {seg//60}m {seg%60}s")
    print("="*60)
    print("  CONCLUIDO! Reinicie o app para usar a nova tabela.")
    print("="*60)


if __name__ == "__main__":
    main()
