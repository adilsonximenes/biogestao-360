"""
processar_tabelas.py  —  BioGestão 360
=======================================
Gera taco_limpa.csv e ibge_limpa.csv a partir dos arquivos originais.

Execute UMA VEZ quando atualizar as tabelas originais:
    python processar_tabelas.py

Arquivos de entrada (mesma pasta):
    alimentos.csv        → tabela TACO (UNICAMP, 4ª ed.)
    tabela_ibge.csv      → tabela IBGE (POF 2008-2009)

Arquivos gerados:
    taco_limpa.csv       → TACO normalizada, pronta para uso
    ibge_limpa.csv       → IBGE normalizada, com chave de busca nome+preparação

O que o script faz em cada tabela:

TACO:
  - Remove vírgulas dos nomes ("Arroz, integral, cozido" → "arroz integral cozido")
  - Substitui TR (0.00001) por 0 (traço = presença mínima, insignificante)
  - Sódio permanece em mg/100g (consistente com IBGE)
  - Gera coluna 'nome_busca' normalizada para lookup rápido

IBGE:
  - Separador ; e decimal , tratados corretamente
  - Combina nome + preparação em 'nome_busca'
    Ex: "OVO DE GALINHA" + "FRITO(A)" → "ovo de galinha frito"
  - "NAO SE APLICA" → nome puro sem sufixo (preparo padrão)
  - Traço "-" → None em todos os campos numéricos
  - Mantém gordura saturada, gordura trans e açúcar total (extras vs TACO)
"""

import os, sys, re, unicodedata
import pandas as pd

ARQ_TACO      = "alimentos.csv"
ARQ_IBGE      = "tabela_ibge.csv"
ARQ_TACO_OUT  = "taco_limpa.csv"
ARQ_IBGE_OUT  = "ibge_limpa.csv"


# ── Funções auxiliares ────────────────────────────────────────────────────────

def normalizar(texto):
    """Normaliza para chave de busca: sem acento, minúsculo, sem vírgulas."""
    if not texto or not isinstance(texto, str):
        return ''
    t = texto.lower().strip()
    t = t.replace(',', ' ')
    t = unicodedata.normalize('NFKD', t)
    t = t.encode('ASCII', 'ignore').decode('ASCII')
    t = re.sub(r'[^a-z0-9\s]', '', t)
    return re.sub(r'\s+', ' ', t).strip()


def conv_float(valor):
    """String com vírgula decimal → float. '-' ou vazio → None."""
    if valor is None:
        return None
    s = str(valor).strip()
    if s in ('-', '', 'nan', 'None', 'NA'):
        return None
    try:
        return float(s.replace(',', '.'))
    except (ValueError, TypeError):
        return None


def tr_para_zero(valor):
    """TR = 0.00001 no CSV → substitui por 0.0 (traço = insignificante)."""
    v = conv_float(valor)
    if v is None:
        return None
    return 0.0 if abs(v - 0.00001) < 1e-8 else v


# Mapeamento: DESCRIÇÃO DA PREPARAÇÃO da IBGE → sufixo legível
MAPA_PREP = {
    'NAO SE APLICA':               '',
    'CRU(A)':                      'cru',
    'COZIDO(A)':                   'cozido',
    'FRITO(A)':                    'frito',
    'ASSADO(A)':                   'assado',
    'REFOGADO(A)':                 'refogado',
    'GRELHADO(A)/BRASA/CHURRASCO': 'grelhado',
    'ENSOPADO':                    'ensopado',
    'EMPANADO(A)/A MILANESA':      'empanado',
    'MOLHO VERMELHO':              'ao molho vermelho',
    'MOLHO BRANCO':                'ao molho branco',
    'AO VINAGRETE':                'ao vinagrete',
    'AO ALHO E OLEO':              'ao alho e oleo',
    'COM MANTEIGA/OLEO':           'com manteiga',
    'SOPA':                        'sopa',
    'MINGAU':                      'mingau',
}


# ── Processar TACO ─────────────────────────────────────────────────────────────

def processar_taco(entrada, saida):
    print(f"\n{'='*55}")
    print(f"  TACO: {entrada}")
    print(f"{'='*55}")

    if not os.path.exists(entrada):
        print(f"  ❌ Arquivo não encontrado: {entrada}")
        return

    df = pd.read_csv(entrada, encoding='utf-8', low_memory=False)
    print(f"  Linhas originais: {len(df):,}")

    registros = []
    sem_kcal = 0
    for _, row in df.iterrows():
        nome_orig = str(row.get('Descrição dos alimentos', '')).strip()
        if not nome_orig or nome_orig == 'nan':
            continue

        kcal = tr_para_zero(row.get('Energia..kcal.'))
        if not kcal:
            sem_kcal += 1
            continue

        registros.append({
            'nome':           nome_orig,
            'nome_busca':     normalizar(nome_orig),
            'categoria':      str(row.get('Categoria do alimento', '')).strip(),
            'kcal_100g':      kcal,
            'proteina_g':     tr_para_zero(row.get('Proteína..g.')),
            'carboidrato_g':  tr_para_zero(row.get('Carboidrato..g.')),
            'gordura_g':      tr_para_zero(row.get('Lipídeos..g.')),
            'fibra_g':        tr_para_zero(row.get('Fibra.Alimentar..g.')),
            'sodio_mg':       tr_para_zero(row.get('Sódio..mg.')),
            'colesterol_mg':  tr_para_zero(row.get('Colesterol..mg.')),
            'calcio_mg':      tr_para_zero(row.get('Cálcio..mg.')),
            'ferro_mg':       tr_para_zero(row.get('Ferro..mg.')),
            'fonte':          'TACO',
        })

    df_out = pd.DataFrame(registros)
    df_out.to_csv(saida, index=False, encoding='utf-8')
    print(f"  Descartados sem kcal: {sem_kcal}")
    print(f"  ✅ Salvo: {saida}  ({len(df_out)} linhas)")


# ── Processar IBGE ─────────────────────────────────────────────────────────────

def processar_ibge(entrada, saida):
    print(f"\n{'='*55}")
    print(f"  IBGE: {entrada}")
    print(f"{'='*55}")

    if not os.path.exists(entrada):
        print(f"  ❌ Arquivo não encontrado: {entrada}")
        return

    df = pd.read_csv(
        entrada,
        encoding='utf-8-sig', sep=';', skiprows=3,
        low_memory=False, decimal=',', on_bad_lines='skip'
    )
    df = df.dropna(axis=1, how='all')
    df.columns = [c.strip() for c in df.columns]
    print(f"  Linhas originais: {len(df):,}")

    registros = []
    sem_kcal = 0
    for _, row in df.iterrows():
        nome_orig = str(row.get('DESCRIÇÃO DO ALIMENTO', '')).strip()
        prep_orig = str(row.get('DESCRIÇÃO DA PREPARAÇÃO', '')).strip()
        if not nome_orig or nome_orig == 'nan':
            continue

        kcal = conv_float(row.get('ENERGIA (kcal)'))
        if not kcal:
            sem_kcal += 1
            continue

        # Chave de busca: nome normalizado + sufixo de preparação
        sufixo   = MAPA_PREP.get(prep_orig, normalizar(prep_orig))
        nome_n   = normalizar(nome_orig)
        chave    = f"{nome_n} {sufixo}".strip() if sufixo else nome_n

        registros.append({
            'nome':              nome_orig,
            'preparacao':        prep_orig,
            'nome_busca':        chave,
            'kcal_100g':         kcal,
            'proteina_g':        conv_float(row.get('PROTEÍNA (g)')),
            'carboidrato_g':     conv_float(row.get('CARBOIDRATO (g)')),
            'gordura_g':         conv_float(row.get('LIPÍDEOS TOTAIS (g)')),
            'fibra_g':           conv_float(row.get('FIBRA ALIMENTAR TOTAL (g)')),
            'sodio_mg':          conv_float(row.get('SÓDIO (mg)')),
            'gordura_saturada_g':conv_float(row.get('ÁCIDOS GRAXOS SATURADOS (g)')),
            'gordura_trans_g':   conv_float(row.get('ÁCIDOS GRAXOS TRANS TOTAL (g)')),
            'acucar_g':          conv_float(row.get('AÇÚCAR TOTAL (g)')),
            'colesterol_mg':     conv_float(row.get('COLESTEROL (mg)')),
            'fonte':             'IBGE',
        })

    df_out = pd.DataFrame(registros)
    df_out.to_csv(saida, index=False, encoding='utf-8')
    print(f"  Descartados sem kcal: {sem_kcal}")
    print(f"  Com gordura saturada: {df_out['gordura_saturada_g'].notna().sum()}")
    print(f"  Com gordura trans:    {df_out['gordura_trans_g'].notna().sum()}")
    print(f"  Com açúcar total:     {df_out['acucar_g'].notna().sum()}")
    print(f"  ✅ Salvo: {saida}  ({len(df_out)} linhas)")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("BioGestão 360 — Processamento das Tabelas Nutricionais")
    processar_taco(ARQ_TACO, ARQ_TACO_OUT)
    processar_ibge(ARQ_IBGE, ARQ_IBGE_OUT)
    print(f"\n{'='*55}")
    print("  CONCLUÍDO")
    print(f"{'='*55}")
    print(f"  Coloque taco_limpa.csv e ibge_limpa.csv")
    print(f"  na pasta raiz do projeto junto com app.py")
    print(f"{'='*55}")


if __name__ == '__main__':
    main()
