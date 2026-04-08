# 🏋️‍♂️ BioGestão 360

**Sistema universal de análise de bioimpedância e planejamento alimentar baseado na metodologia TACO e protocolos científicos Harris-Benedict**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biogestao-360.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## ⚠️ **AVISO IMPORTANTE**

> **SISTEMA EM DESENVOLVIMENTO BASEADO NA TABELA TACO - DADOS PODEM CONTER ERRO**
> 
> Este é um projeto educacional e de estudo. Os cálculos e informações são baseados em fontes científicas, mas podem conter imprecisões. 
> **Sempre consulte um profissional de saúde antes de fazer mudanças significativas na sua alimentação.**

---

## 📋 **Sobre o Projeto**

O **BioGestão 360** é uma ferramenta web gratuita e open-source que permite:

- ✅ **Análise de composição corporal** (percentual de gordura, massa magra, peso ideal)
- ✅ **Cálculo do gasto energético** (TMB e GET baseado em Harris-Benedict)
- ✅ **Planejamento alimentar** usando a Tabela TACO (Tabela Brasileira de Composição de Alimentos)
- ✅ **Laudo técnico** com projeção de resultados em 30 dias
- ✅ **Interface adaptativa** que segue o tema do seu sistema operacional
- ✅ **Modo de impressão econômica** para economizar tinta/papel

### 🎯 **Público-alvo**

- Estudantes de nutrição e educação física
- Profissionais da saúde que buscam uma ferramenta de apoio
- Desenvolvedores interessados em projetos de saúde tech
- Pessoas que desejam entender melhor sua composição corporal

---

## 🧠 **Metodologia Científica**

### Fórmulas utilizadas:

| Cálculo | Fórmula | Fonte |
|---------|---------|-------|
| **TMB (Homens)** | 66.47 + (13.75 × peso) + (5.0 × altura) - (6.75 × idade) | Harris-Benedict (1919) |
| **TMB (Mulheres)** | 655.1 + (9.56 × peso) + (1.85 × altura) - (4.67 × idade) | Harris-Benedict (1919) |
| **GET** | TMB × Fator de Atividade | WHO/FAO |
| **% Gordura** | (1.20 × IMC) + (0.23 × idade) - (16.2 ou 5.4) | Deurenberg et al. |
| **Peso Ideal** | IMC ideal (21.7/21.3) × altura² | Metropolitan Life Insurance |
| **Variação 30 dias** | Saldo calórico × 30 ÷ 7700 | Termodinâmica (7700 kcal/kg) |

### Fatores de Atividade Física (NAF):

| Nível | Descrição | Fator |
|-------|-----------|-------|
| Sedentário | Sem exercício | 1.2 |
| Leve | 1-3 dias/semana | 1.375 |
| Moderado | 3-5 dias/semana | 1.55 |
| Intenso | 6-7 dias/semana | 1.725 |
| Atleta | Treino pesado 2x/dia | 1.9 |

---

## 🚀 **Como executar localmente**

### Pré-requisitos

- Python 3.10 ou superior
- Pip (gerenciador de pacotes)

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/biogestao-360.git
cd biogestao-360
