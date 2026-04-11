# 🏋️‍♂️ BioGestão 360 - Indústria 5.0

## 🤖 Tecnologia Humanizada para Avaliação Física

**BioGestão 360: Onde a precisão científica encontra o toque humano da Indústria 5.0**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biogestao-360.streamlit.app)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🌐 O que é Indústria 5.0 e como o BioGestão 360 se encaixa?

**Indústria 5.0** representa a evolução da automação para a **colaboração humano-máquina**. Diferente da Indústria 4.0 (focada em eficiência e automação), a 5.0 coloca o **ser humano no centro** da tecnologia.

### Os 3 pilares da Indústria 5.0 no BioGestão 360:

| Pilar | Como o BioGestão 360 aplica |
|-------|----------------------------|
| **🌍 Centrado no Humano** | A tecnologia auxilia, mas a decisão final é do profissional. O sistema NÃO substitui o avaliador - apenas organiza os dados. |
| **🌱 Sustentável** | 100% gratuito, código aberto, sem servidores externos. Zero carbono digital desnecessário. |
| **🔄 Resiliente** | Processamento 100% local. Mesmo sem internet, o sistema funciona (após carregar). |

### O que NÃO somos:

❌ Não somos um sistema que "diagnostica" automaticamente
❌ Não substituímos o profissional de Educação Física ou Nutrição
❌ Não tomamos decisões por você

### O que SOMOS:

✅ Uma ferramenta que potencializa o seu conhecimento profissional
✅ Um sistema que organiza dados para você interpretar
✅ Um parceiro tecnológico que respeita o seu julgamento clínico

> **"A máquina calcula, o profissional interpreta. O BioGestão 360 calcula para você interpretar melhor."**

---

## ⚠️ **AVISO IMPORTANTE**

> **SISTEMA EM DESENVOLVIMENTO BASEADO NA TABELA TACO - DADOS PODEM CONTER ERRO**
> 
> Este é um projeto **EXCLUSIVAMENTE EDUCACIONAL E ACADÊMICO**. Os cálculos e informações são baseados em fontes científicas, mas podem conter imprecisões. 
> **Sempre consulte um profissional de saúde antes de fazer mudanças significativas na sua alimentação.**

---

## 📋 **Sobre o Projeto**

O **BioGestão 360** é uma ferramenta web **gratuita e de código aberto para fins acadêmicos** que permite:

### 🆕 NOVAS FUNCIONALIDADES (Atualização 2026)

- ✅ **Separação Adipômetro vs Fita Métrica** - Agora fica claro: dobras cutâneas (mm) para % de gordura, circunferências (cm) para tamanho muscular
- ✅ **Sistema de 3 Medições com Média Automática** - Protocolo científico: 3 tentativas, média calculada automaticamente
- ✅ **Dobra Supra-espinal (SS) Incluída** - Para cálculo do somatotipo de Heath-Carter
- ✅ **Handgrip (Força)** - Avaliação de força de preensão palmar com classificação por nível
- ✅ **Banco de Wells (Flexibilidade)** - Avaliação de flexibilidade com classificação por nível
- ✅ **Laudo CSV Exclusivo** - Botão separado para baixar o laudo da avaliação física

### Funcionalidades já existentes

- ✅ **Análise de composição corporal** (percentual de gordura, massa magra, peso ideal)
- ✅ **Cálculo do gasto energético** (TMB e GET baseado em Harris-Benedict)
- ✅ **Planejamento alimentar** usando a Tabela TACO
- ✅ **Laudo técnico** com projeção de resultados em 30 dias
- ✅ **Modo de impressão econômica** para economizar tinta/papel

### 🎯 **Público-alvo**

- Profissionais de Educação Física
- Nutricionistas
- Estudantes de nutrição e educação física
- Pesquisadores da área de nutrição e metabolismo
- Desenvolvedores interessados em projetos de saúde tech

---

## 🔒 **Licenciamento e Uso**

### **Este NÃO é um software comercial!**

Este projeto está licenciado sob a **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**.

### **O que isso significa?**

| Permissão | Status |
|-----------|--------|
| ✅ Uso acadêmico e educacional | Permitido |
| ✅ Estudo e pesquisa | Permitido |
| ✅ Compartilhamento com atribuição | Permitido |
| ❌ **USO COMERCIAL** | **PROIBIDO** |
| ❌ Venda ou redistribuição paga | **PROIBIDO** |
| ❌ Modificação e distribuição modificada | **PROIBIDO** |

### **Para uso comercial, entre em contato com o desenvolvedor.**

---

## 🧠 **Metodologia Científica - Indústria 5.0**

### 3 MEDIÇÕES COM MÉDIA AUTOMÁTICA (Protocolo Científico)

O sistema implementa o protocolo padrão de avaliação física:
- 3 medições não consecutivas para cada dobra cutânea
- Média calculada automaticamente
- Diferença máxima entre medidas: 5%
- Caso exceda, o profissional deve realizar nova série

### Fórmulas utilizadas:

| Cálculo | Fórmula | Fonte |
|---------|---------|-------|
| **TMB (Homens)** | 66.47 + (13.75 × peso) + (5.0 × altura) - (6.75 × idade) | Harris-Benedict (1919) |
| **TMB (Mulheres)** | 655.1 + (9.56 × peso) + (1.85 × altura) - (4.67 × idade) | Harris-Benedict (1919) |
| **GET** | TMB × Fator de Atividade | WHO/FAO |
| **% Gordura (IMC)** | (1.20 × IMC) + (0.23 × idade) - (16.2 ou 5.4) | Deurenberg et al. |
| **% Gordura (Dobras)** | Jackson & Pollock + Siri | ACSM |
| **Densidade Corporal** | Protocolo Jackson & Pollock (3 ou 7 dobras) | Jackson AS, Pollock ML (1978) |
| **% Gordura por Densidade** | (4.95 / Densidade - 4.5) × 100 | Siri WE (1961) |
| **Peso Ideal** | IMC ideal (21.7/21.3) × altura² | Metropolitan Life Insurance |
| **Variação 30 dias** | Saldo calórico × 30 ÷ 7700 | Termodinâmica (7700 kcal/kg) |

### Dobras Cutâneas Disponíveis:

| # | Dobra | Localização | Protocolo |
|---|-------|-------------|-----------|
| 1 | Tríceps | Face posterior do braço | 3 ou 7 dobras |
| 2 | Bíceps | Face anterior do braço | 7 dobras |
| 3 | Peitoral | Metade axila-mamilo | 3 ou 7 dobras |
| 4 | Subescapular | 2cm abaixo da escápula | 7 dobras |
| 5 | Axilar Média | Linha axilar média | 7 dobras |
| 6 | Supra-ilíaca | Sobre a crista ilíaca | 3 ou 7 dobras |
| 7 | Supra-espinal | 5-7cm acima da espinha ilíaca | Somatotipo |
| 8 | Abdominal | 2cm à direita do umbigo | 3 ou 7 dobras |
| 9 | Coxa | Ponto médio inguinal-patela | 3 ou 7 dobras |
| 10 | Panturrilha | Maior perímetro da perna | 7 dobras |

### Circunferências (Fita Métrica):

| Medida | Localização | Unidade |
|--------|-------------|---------|
| Braço Contraído | Maior circunferência com contração | cm |
| Peitoral / Tórax | Altura dos mamilos, expiração normal | cm |
| Cintura | Ponto médio costela-crista ilíaca | cm |
| Quadril | Maior circunferência glútea | cm |
| Coxa | Terço proximal da coxa | cm |
| Panturrilha | Maior circunferência da perna | cm |

### Avaliações Complementares:

| Equipamento | O que avalia | Classificação (Homens) | Classificação (Mulheres) |
|-------------|--------------|------------------------|--------------------------|
| **Handgrip** | Força de preensão palmar | Fraco <35kg / Regular 35-45kg / Forte >45kg | Fraco <25kg / Regular 25-35kg / Forte >35kg |
| **Banco de Wells** | Flexibilidade | Abaixo <20cm / Média 20-30cm / Acima >30cm | Abaixo <25cm / Média 25-35cm / Acima >35cm |

### Classificação do Percentual de Gordura (ACSM):

| Classificação | Homens | Mulheres | Risco |
|---------------|--------|----------|-------|
| Gordura Essencial | 2-5% | 10-13% | Mínimo |
| Atleta | 6-13% | 14-20% | Muito baixo |
| Saudável | 14-17% | 21-24% | Baixo |
| Aceitável | 18-21% | 25-31% | Moderado |
| Obesidade | >22% | >32% | Alto |

### Biotipos Corporais (Heath-Carter):

| Biotipo | Característica | % Gordura típico | Recomendação |
|---------|----------------|------------------|--------------|
| **Endomorfo** | Tendência a acumular gordura | >25% (H) / >28% (M) | Déficit calórico + treino de força |
| **Mesomorfo** | Estrutura atlética natural | 10-18% (H) / 18-25% (M) | Treino equilibrado |
| **Ectomorfo** | Metabolismo acelerado | <10% (H) / <18% (M) | Superávit calórico + força |

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
```
2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Instale as dependências
```bash
pip install -r requirements.txt
```
4. Execute o aplicativo
```bash
streamlit run app.py
```
5. Acesse no navegador
```bash
http://localhost:8501
```
## 📁 Estrutura do Projeto
```bash
biogestao-360/
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências do projeto
├── alimentos.csv          # Base de dados TACO (alimentos)
├── acidos-graxos.csv      # Base de dados (ácidos graxos)
├── aminoacidos.csv        # Base de dados (aminoácidos)
├── README.md              # Este arquivo
└── .gitignore             # Arquivos ignorados pelo Git
```
## 🖨️ Funcionalidade de Impressão

O sistema possui um modo especial de impressão que:

✅ Economiza tinta (fundo branco, texto preto)
✅ Remove elementos desnecessários (sidebar, botões)
✅ Otimiza margens para papel
✅ Mantém todas as informações importantes

Como usar:

Clique em "Gerar Versão para Impressão" no menu lateral

Aguarde o recarregamento

Clique nos 3 pontinhos (⋮) do navegador

Selecione "Imprimir"

Configure "Margens: Mínimas"

## 📊 Base de Dados - Tabela TACO

Os dados alimentares são baseados na Tabela Brasileira de Composição de Alimentos (TACO) desenvolvida pela Universidade Estadual de Campinas (UNICAMP).

Fonte: NEPA - Núcleo de Estudos e Pesquisas em Alimentação

Instituição: UNICAMP

Ano da versão utilizada: 2011 (última versão completa disponível publicamente)

⚠️ Nota sobre os dados: A tabela TACO tem limitações e pode não refletir variações sazonais, regionais ou de preparo dos alimentos. Este projeto usa os dados "como estão" para fins educacionais.

## 🛡️ Privacidade e Segurança - Indústria 5.0
Zero-Footprint Total! 🔒
✅ Nenhum dado é enviado para servidores externos (Resiliência)
✅ Todo processamento é 100% local no seu navegador (Sustentabilidade)
✅ Não há banco de dados, login ou coleta de informações (Centrado no humano)
✅ Ao fechar a aba, todos os dados são permanentemente deletados
✅ Você pode usar sem preocupações com privacidade

"Seus dados são seus. O BioGestão 360 apenas organiza o que você já sabe."

## 📄 Licença
Este projeto está licenciado sob a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).

Permissão	Status
✅ Compartilhar (copiar e redistribuir)	Permitido com atribuição
✅ Uso acadêmico e educacional	Permitido
❌ Uso comercial	PROIBIDO
❌ Modificar ou criar derivados	PROIBIDO
Texto completo da licença: https://creativecommons.org/licenses/by-nc-nd/4.0/

## 👨‍💻 Desenvolvedor
Desenvolvido como ferramenta educacional para estudo de atividade física e consumo energético de alimentos.

Autor: ADILSON GONCALVES XIMENES

Finalidade: Exclusivamente acadêmica e educacional

Filosofia: Indústria 5.0 - Tecnologia a serviço do humano

Contato para uso comercial: Abrir uma Issue no GitHub

## ⭐ Reconhecimentos
UNICAMP - Tabela TACO

Harris & Benedict - Equação de metabolismo basal

Jackson & Pollock - Protocolo de dobras cutâneas

Siri WE - Fórmula de densidade para % de gordura

Deurenberg et al. - Fórmula de composição corporal por IMC

ACSM - Classificações de referência

Comunidade Streamlit - Framework incrível

## 📞 Contato
Issues: GitHub Issues

Para uso comercial: Abra uma Issue com o título "USO COMERCIAL"

## 🙏 Agradecimentos
Agradeço a todos que contribuírem academicamente para este projeto! Juntos podemos melhorar a ferramenta e ajudar mais profissionais a realizarem avaliações físicas de qualidade.

Feito com ❤️ para a comunidade acadêmica e desenvolvimento open-source educacional

*BioGestão 360 - Tecnologia humanizada para avaliação física* 🏋️‍♂️🤝💻
```bash

---

## 📋 Resumo do que foi adicionado/atualizado:

| Seção | O que mudou |
|-------|-------------|
| **Título principal** | Adicionado "Indústria 5.0" e subtítulo "Tecnologia Humanizada" |
| **Nova seção** | "O que é Indústria 5.0 e como o BioGestão 360 se encaixa?" com os 3 pilares |
| **Novas funcionalidades** | Lista destacada com todas as atualizações (3 medições, adipômetro vs fita, supra-espinal, handgrip, wells, laudo CSV) |
| **Metodologia científica** | Adicionadas tabelas completas de dobras, circunferências, handgrip, wells, classificação ACSM e biotipos |
| **Privacidade** | Relacionada aos 3 pilares da Indústria 5.0 |
| **Filosofia** | Frase de impacto: "A máquina calcula, o profissional interpreta" |
| **Rodapé** | Nova assinatura: "BioGestão 360 - Tecnologia humanizada para avaliação física" |
