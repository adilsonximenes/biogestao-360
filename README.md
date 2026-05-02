# BioGestão 360

**Versão:** 4.0 (Maio/2026)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biogestao-360.streamlit.app)

---

## 💡 O que é o BioGestão 360?

O **BioGestão 360** é uma ferramenta web **gratuita** para organização
de dados de saúde, atividade física e alimentação — baseada em fontes
científicas reconhecidas (TACO/UNICAMP, IBGE, Harris-Benedict).

> **"A tecnologia organiza, o profissional interpreta."**

---

## ✅ O que é GRATUITO para sempre (sem cadastro)

| Funcionalidade                 | Descrição                                        |
| ------------------------------ | ------------------------------------------------ |
| 📊 Bioimpedância por IMC       | Estimativa de % gordura, massa magra, peso ideal |
| 🔥 Cálculo GET/TMB             | Harris-Benedict e Katch-McArdle                  |
| 🥗 Montagem do Plano Alimentar | Tabelas TACO e IBGE                              |
| 📋 Laudo Técnico               | Projeção de resultados em 30 dias                |
| 📈 Gráficos e relatórios       | Exportação CSV e modo impressão                  |
| ⚠️ Alertas OMS/IARC            | Classificação de alimentos por risco             |

---

## 🔐 Funcionalidades exclusivas (cadastro gratuito — 2 dias de teste)

| Funcionalidade                       | Descrição                                                        |
| ------------------------------------ | ---------------------------------------------------------------- |
| 📋 Importador Automático de Cardápio | Cole seu cardápio em texto e o sistema preenche automaticamente  |
| 📏 Avaliação Física Profissional     | Para profissionais de Ed. Física habilitados — adipômetro e fita |

> Após os 2 dias gratuitos, é possível continuar com colaboração voluntária.

---

## 💚 Colaboração Voluntária

O BioGestão 360 é gratuito e sempre será. A colaboração voluntária
ajuda a manter o servidor no ar e o projeto em evolução.

| Plano                   | Inclui                             | Valor    |
| ----------------------- | ---------------------------------- | -------- |
| ☕ Café                 | Importador 30 dias                 | R$ 5,00  |
| 🥗 Básico               | Importador 1 ano                   | R$ 15,00 |
| 💪 Pro                  | Avaliação Física 30 dias           | R$ 10,00 |
| 🏆 Combo Mensal         | Importador + Avaliação 30 dias     | R$ 12,00 |
| 🌟 Combo Anual          | Importador + Avaliação 1 ano       | R$ 25,00 |
| ♾️ Vitalício Importador | Importador para sempre             | R$ 49,00 |
| 🏅 Combo Vitalício      | Importador + Avaliação para sempre | R$ 79,00 |

📱 PIX: `f3e890da-fb72-4e8c-a0cd-d88177457a30` (ADILSON GONCALVES XIMENES)  
💬 WhatsApp: (21) 97948-6731 — envie o comprovante para ativação em até 72h

---

## ⚠️ O que NÃO somos

|     |                                                                        |
| --- | ---------------------------------------------------------------------- |
| ❌  | Não diagnosticamos automaticamente                                     |
| ❌  | Não substituímos nutricionista ou médico                               |
| ❌  | Não prescrevemos dietas ou tratamentos                                 |
| ❌  | A seção de Avaliação Física é exclusiva para profissionais habilitados |

---

## 🔒 Privacidade e Segurança

| Item              | Descrição                                                               |
| ----------------- | ----------------------------------------------------------------------- |
| 🧮 Cálculos       | Processados localmente no navegador                                     |
| 🗑️ Dados de saúde | Deletados ao fechar a aba                                               |
| 🔐 Cadastro       | Nome de usuário, e-mail e senha criptografada armazenados com segurança |
| 🏦 Banco de dados | PostgreSQL hospedado no Supabase com SSL obrigatório                    |
| 💳 Pagamentos     | Via PIX ou PayPal — nenhum dado bancário é armazenado no app            |
| 🛡️ Proteção       | SQL Injection bloqueado, senhas com hash SHA-256                        |

---

## 🧠 Metodologia Científica

| Cálculo                 | Fórmula                                                   | Fonte                    |
| ----------------------- | --------------------------------------------------------- | ------------------------ |
| IMC                     | Peso / Altura²                                            | OMS                      |
| TMB Homem               | 66.47 + (13.75×P) + (5.0×A) - (6.75×I)                    | Harris-Benedict (1919)   |
| TMB Mulher              | 655.1 + (9.56×P) + (1.85×A) - (4.67×I)                    | Harris-Benedict (1919)   |
| TMB Katch-McArdle       | 370 + (21.6 × Massa Magra)                                | Katch-McArdle (1975)     |
| GET                     | TMB × Fator de Atividade                                  | WHO/FAO                  |
| % Gordura IMC H         | (1.20×IMC) + (0.23×I) - 16.2                              | Deurenberg et al. (1991) |
| % Gordura IMC M         | (1.20×IMC) + (0.23×I) - 5.4                               | Deurenberg et al. (1991) |
| Densidade 7 dobras H    | 1.112 - (0.00043499×S) + (0.00000055×S²) - (0.00028826×I) | Jackson & Pollock (1978) |
| % Gordura por Densidade | (4.95 / Densidade - 4.5) × 100                            | Siri WE (1961)           |

### Fatores de Atividade Física (NAF)

| Nível      | Descrição            | Fator |
| ---------- | -------------------- | ----- |
| Sedentário | Sem exercício        | 1.2   |
| Leve       | 1-3 dias/semana      | 1.375 |
| Moderado   | 3-5 dias/semana      | 1.55  |
| Intenso    | 6-7 dias/semana      | 1.725 |
| Atleta     | Treino pesado 2x/dia | 1.9   |

---

## 🚀 Como executar localmente

```bash
# 1. Clonar o repositório
git clone https://github.com/adilsonximenes/biogestao-360.git
cd biogestao-360

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Configurar secrets (NUNCA enviar ao GitHub!)
mkdir .streamlit
# Criar .streamlit/secrets.toml com sua URL do Supabase

# 6. Executar
streamlit run app.py
```

---

## 📁 Estrutura do Projeto
```bash
biogestao-360/
├── app.py # Aplicação principal
├── auth.py # Autenticação e controle de acesso
├── database.py # Banco de dados PostgreSQL (Supabase)
├── admin_panel.py # Painel administrativo
├── ia_gemini.py # Importador de cardápio (modo local)
├── requirements.txt # Dependências Python
├── alimentos.csv # Tabela TACO/UNICAMP
├── tabela_ibge.csv # Tabela IBGE POF 2008-2009
├── acidos-graxos.csv # Perfil de ácidos graxos
├── aminoacidos.csv # Perfil de aminoácidos
├── Taco-4a-Edicao.xlsx # Tabela TACO original (referência)
├── tabelacompleta.xls # Tabela IBGE original (referência)
├── DOCUMENTO_TECNICO.md # Documentação técnica
├── README.md # Este arquivo
├── .gitignore # Arquivos ignorados pelo Git
└── .streamlit/
└── config.toml # Configurações do Streamlit
```
> ⚠️ O arquivo `.streamlit/secrets.toml` **nunca** é enviado ao GitHub.
> Contém credenciais do banco de dados.

---

## 📚 Bases de Dados

| Fonte                 | Arquivo           | Conteúdo                                |
| --------------------- | ----------------- | --------------------------------------- |
| TACO/UNICAMP (4ª Ed.) | `alimentos.csv`   | Kcal, Proteínas, Carboidratos, Gorduras |
| IBGE POF 2008-2009    | `tabela_ibge.csv` | Alimentos in natura e regionais         |
| FAO/WHO               | —                 | Fatores de atividade física             |

---

## 📦 Dependências

| Biblioteca      | Versão  | Finalidade                         |
| --------------- | ------- | ---------------------------------- |
| streamlit       | ≥1.35.0 | Interface web                      |
| pandas          | ≥2.0.0  | Manipulação de dados               |
| plotly          | ≥5.24.0 | Gráficos interativos               |
| matplotlib      | ≥3.7.0  | Gráficos estáticos                 |
| qrcode          | ≥7.0.0  | QR Code PIX                        |
| pillow          | ≥10.0.0 | Manipulação de imagens             |
| openpyxl        | ≥3.1.0  | Leitura de Excel                   |
| numpy           | ≥1.24.0 | Operações matemáticas              |
| psycopg2-binary | ≥2.9.0  | Conexão PostgreSQL/Supabase        |
| pyotp           | ≥2.9.0  | Autenticação de dois fatores (2FA) |

---

## 📄 Licença

**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 (CC BY-NC-ND 4.0)**

| Permissão                          | Status    |
| ---------------------------------- | --------- |
| ✅ Uso acadêmico e educacional     | Permitido |
| ✅ Compartilhamento com atribuição | Permitido |
| ✅ Estudo e pesquisa               | Permitido |
| ❌ Uso comercial                   | Proibido  |
| ❌ Venda ou redistribuição paga    | Proibido  |
| ❌ Modificação e distribuição      | Proibido  |

> A colaboração voluntária é uma contribuição ao desenvolvedor,
> não a compra ou venda do software.

Texto completo: https://creativecommons.org/licenses/by-nc-nd/4.0/

---

## 👨‍💻 Desenvolvedor

| Item     | Informação                                                   |
| -------- | ------------------------------------------------------------ |
| Autor    | Adilson Gonçalves Ximenes                                    |
| Formação | Ed. Física (2005) + Técnico em Processamento de Dados (1996) |
| Telegram | t.me/biogestao360                                            |
| WhatsApp | (21) 97948-6731                                              |
| E-mail   | adilson.ximenes@gmail.com                                    |

---

## ⭐ Reconhecimentos

- **UNICAMP/NEPA** — Tabela TACO
- **IBGE** — POF 2008-2009
- **FAO/WHO** — Fatores de atividade física
- **Harris & Benedict** (1919), **Katch & McArdle** (1975)
- **Jackson & Pollock** (1978), **Siri WE** (1961)
- **Deurenberg et al.** (1991), **ACSM**, **IARC/OMS**
- **Comunidade Streamlit**

---

**Feito com ❤️ para a comunidade de Educação Física e Nutrição**

_BioGestão 360 — Tecnologia humanizada para saúde e qualidade de vida_ 🏋️‍♂️🤝💻
