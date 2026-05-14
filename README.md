# BioGestão 360

**Versão:** 4.2 (Maio/2026)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biogestao-360.streamlit.app)

---

## 💡 O que é o BioGestão 360?

O **BioGestão 360** é uma plataforma web **gratuita** de organização de
saúde, atividade física e alimentação — com dados nutricionais reais e
cálculos científicos validados.

> **"A tecnologia organiza, o profissional interpreta."**

---

## ✅ O que é GRATUITO para sempre (sem cadastro)

| Funcionalidade | Descrição |
|---|---|
| 📊 Bioimpedância por IMC | Estimativa de % gordura, massa magra, peso ideal |
| 🔥 Cálculo GET/TMB | Harris-Benedict e Katch-McArdle |
| 🍏 Montagem do Plano Alimentar | Bases TACO, IBGE e BioGestão 360 com seletor de tabela e marca |
| 📋 Laudo Técnico | Projeção de resultados em 30 dias |
| 📈 Gráficos e relatórios | Exportação CSV e modo impressão |
| ⚠️ Alertas OMS/IARC | Grupos 1, 2A e 2B com referências IARC |
| 🏋️ Monte Seu Treino | Anamnese, MET, sugestão automática, 120+ exercícios |

---

## 🔐 Funcionalidades exclusivas (cadastro gratuito — 2 dias de teste)

| Funcionalidade | Descrição |
|---|---|
| 📥 Importador Automático de Cardápio | Cole seu cardápio em texto — hierarquia TACO → IBGE → BioGestão 360 |
| 📏 Avaliação Física Profissional | Para profissionais de Ed. Física habilitados (CREF) |

---

## 💚 Colaboração Voluntária

| Plano | Inclui | Valor |
|---|---|---|
| ☕ Café | Importador 30 dias | R$ 5,00 |
| 🥗 Básico | Importador 1 ano | R$ 15,00 |
| 💪 Pro | Avaliação Física 30 dias | R$ 10,00 |
| 🏆 Combo Mensal | Importador + Avaliação 30 dias | R$ 12,00 |
| 🌟 Combo Anual | Importador + Avaliação 1 ano | R$ 25,00 |
| ♾️ Vitalício Importador | Importador para sempre | R$ 49,00 |
| 🏅 Combo Vitalício | Importador + Avaliação para sempre | R$ 79,00 |

📱 PIX: `f3e890da-fb72-4e8c-a0cd-d88177457a30` (ADILSON GONCALVES XIMENES)
💬 WhatsApp: (21) 97948-6731

---

## 🚀 Como executar localmente

```bash
# 1. Clonar o repositório
git clone https://github.com/adilsonximenes/biogestao-360.git
cd biogestao-360

# 2. Criar e ativar ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar secrets (NUNCA enviar ao GitHub)
mkdir .streamlit
# Criar .streamlit/secrets.toml com:
# SUPABASE_DB_URL = "postgresql://..."

# 5. Gerar tabelas nutricionais locais (necessário na 1ª execução)
python processar_tabelas.py

# 6. Executar
streamlit run app.py
```

> ⚠️ `processar_tabelas.py` lê `alimentos.csv` (TACO) e `tabela_ibge.csv` (IBGE)
> e gera `taco_limpa.csv` e `ibge_limpa.csv`. Execute uma vez após clonar.

---

## 📁 Estrutura do Projeto

```
biogestao-360/
├── app.py                    # Aplicação principal
├── auth.py                   # Autenticação e controle de acesso
├── database.py               # Banco de dados PostgreSQL (Supabase)
├── admin_panel.py            # Painel administrativo
├── admin_usuarios.py         # Gestão de usuários
├── ia_gemini.py              # Motor de busca nutricional (TACO→IBGE→BioGestão)
├── biogestao_helpers.py      # Helpers da seção 26 (seletor de marca, normalização)
├── treino_fisico.py          # Seção 25.1 — Monte Seu Treino
├── portal.py                 # Landing page / portal de apresentação
├── processar_tabelas.py      # Gera taco_limpa.csv e ibge_limpa.csv (rodar localmente)
├── requirements.txt          # Dependências Python
│
├── alimentos.csv             # TACO/UNICAMP (4ª Ed.) — fonte original (não subir ao Git via .gitignore não, manter)
├── tabela_ibge.csv           # IBGE POF 2008-2009 — fonte original
│   ↑ Os dois acima SÃO versionados — são as fontes brutas necessárias
│
├── taco_limpa.csv            # Gerado por processar_tabelas.py — NÃO versionar (.gitignore)
├── ibge_limpa.csv            # Gerado por processar_tabelas.py — NÃO versionar (.gitignore)
├── biogestao_foods.csv       # Base principal 25k+ — NÃO versionar (.gitignore)
│
├── DOCUMENTO_TECNICO.md      # Documentação técnica completa
├── README.md                 # Este arquivo
├── .gitignore                # Arquivos ignorados pelo Git
└── .streamlit/
    ├── config.toml           # Configurações do Streamlit
    └── secrets.toml          # Credenciais — NUNCA subir ao GitHub
```

---

## 📚 Bases de Dados Nutricionais

| Base | Arquivo | Cobertura | Papel no sistema |
|---|---|---|---|
| **BioGestão 360** | `biogestao_foods.csv` | 25.000+ produtos do mercado BR | Fonte principal — produtos industrializados com marca |
| **TACO/UNICAMP** | `alimentos.csv` | 613 alimentos in natura e preparações | Referência científica — prioridade 1 no importador |
| **IBGE/POF 2008-2009** | `tabela_ibge.csv` | 1.962 alimentos × 16 modos de preparo | Referência científica — prioridade 2 no importador |
| **IN 75/2020** | (interno) | Porções de referência Anvisa | Peso por unidade de alimentos |

### Hierarquia de busca (Seção 24.1 — Importador Automático)
```
1. TACO/UNICAMP    → alimentos in natura, preparações caseiras
2. IBGE/POF        → alimentos com forma de preparo (cozido, frito, grelhado...)
3. BioGestão 360   → produtos industrializados, marcas específicas
4. Estimativa      → fallback por categoria alimentar
```

### Atribuições e licenças
- **Open Food Facts:** https://br.openfoodfacts.org — Open Database License (ODbL)
- **TACO/UNICAMP:** https://www.fao.org/food-composition/tables-and-databases/detail/(brazil--2011)-tabela-brasileira-de-composi%C3%A7%C3%A3o-de-alimentos-(taco)/en
- **IBGE/POF:** https://www.fao.org/food-composition/tables-and-databases/detail/(brazil--2011)-tabelas-de-composi%C3%A7%C3%A3o-nutricional-dos-alimentos-consumidos-no-brasil/en

---

## 🧠 Metodologia Científica

| Cálculo | Fórmula | Referência |
|---|---|---|
| TMB Homem | 66.47 + (13.75×P) + (5.0×A) - (6.75×I) | Harris-Benedict (1919) |
| TMB Mulher | 655.1 + (9.56×P) + (1.85×A) - (4.67×I) | Harris-Benedict (1919) |
| TMB Katch-McArdle | 370 + (21.6 × Massa Magra) | Katch-McArdle (1975) |
| GET | TMB × Fator de Atividade | WHO/FAO/UNU (1985) |
| % Gordura IMC | (1.20×IMC) + (0.23×I) - (16.2 H / 5.4 M) | Deurenberg et al. (1991) |
| % Gordura Dobras | Jackson & Pollock 7 dobras + Siri | ACSM |
| Calorias treino | MET × peso(kg) × duração(h) | Ainsworth et al. (2011) |
| Porções | Medidas caseiras e tamanho de porção | IN 75/2020 (Anvisa) |

---

## 📦 Dependências

| Biblioteca | Versão | Finalidade |
|---|---|---|
| streamlit | ≥1.35.0 | Interface web |
| pandas | ≥2.0.0 | Manipulação de dados |
| plotly | ≥5.24.0 | Gráficos interativos |
| matplotlib | ≥3.7.0 | Gráficos estáticos |
| qrcode[pil] | ≥7.0.0 | QR Code PIX |
| pillow | ≥10.0.0 | Manipulação de imagens |
| openpyxl | ≥3.1.0 | Leitura de Excel |
| numpy | ≥1.24.0 | Operações matemáticas |
| psycopg2-binary | ≥2.9.0 | Conexão PostgreSQL/Supabase |
| pyotp | ≥2.9.0 | Autenticação 2FA |

---

## 🔒 Git e segurança

### O que NÃO é versionado (`.gitignore`)
- `.streamlit/secrets.toml` — credenciais do banco
- `biogestao_foods.csv` / `biogestao_foods_corrigido.csv` — base grande gerada
- `taco_limpa.csv` / `ibge_limpa.csv` — geradas pelo `processar_tabelas.py`
- `reset_admin.py`, `reimportar_supabase.py` — scripts de manutenção local

### O que É versionado
- `alimentos.csv` e `tabela_ibge.csv` — fontes brutas necessárias para o `processar_tabelas.py`
- Todo o código Python e arquivos de configuração

### Por que não versionar os CSVs gerados?
Qualquer pessoa que clonar o repo pode rodar `processar_tabelas.py` e gerar os arquivos localmente. Não faz sentido versionar arquivos grandes que mudam frequentemente e podem ser regenerados.

---

## 📄 Licença

**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 (CC BY-NC-ND 4.0)**

| Permissão | Status |
|---|---|
| ✅ Uso acadêmico e educacional | Permitido |
| ✅ Compartilhamento com atribuição | Permitido |
| ✅ Estudo e pesquisa | Permitido |
| ❌ Uso comercial | Proibido |
| ❌ Venda ou redistribuição paga | Proibido |
| ❌ Modificação e redistribuição | Proibido |

Texto completo: https://creativecommons.org/licenses/by-nc-nd/4.0/

---

## 👨‍💻 Desenvolvedor

| Item | Informação |
|---|---|
| Autor | Adilson Gonçalves Ximenes |
| Formação | Bacharel em Ed. Física (2005) + Técnico em Processamento de Dados (1996) |
| Telegram | t.me/biogestao360 |
| WhatsApp | (21) 97948-6731 |
| E-mail | adilson.ximenes@gmail.com |

---

## ⭐ Reconhecimentos

- **Open Food Facts** — Base colaborativa (ODbL) — https://br.openfoodfacts.org
- **UNICAMP/NEPA** — Tabela TACO (4ª Edição)
- **IBGE** — POF 2008-2009
- **Anvisa** — Instrução Normativa IN 75/2020
- **Harris & Benedict** (1919), **Katch & McArdle** (1975)
- **Jackson & Pollock** (1978), **Siri WE** (1961), **Deurenberg et al.** (1991)
- **Ainsworth et al.** (2011) — Compendium of Physical Activities
- **ACSM**, **IARC/OMS**, **Comunidade Streamlit**

---

**Feito com ❤️ para a comunidade de Educação Física e Nutrição**

*BioGestão 360 — Plataforma gratuita de organização de saúde, atividade física e alimentação.* 🏋️‍♂️🤝💻
