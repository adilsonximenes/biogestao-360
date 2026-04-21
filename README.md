# BioGestão 360 - Indústria 5.0

**Versão:** 3.2 (Abril/2026)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biogestao-360.streamlit.app)

---

## 🤖 O que é Indústria 5.0?

**Indústria 5.0** representa a evolução da automação para a **colaboração humano-máquina**. Diferente da Indústria 4.0 (focada em eficiência e automação), a 5.0 coloca o **ser humano no centro** da tecnologia.

### Os 3 pilares da Indústria 5.0 no BioGestão 360:

| Pilar | Como o BioGestão 360 aplica |
|-------|----------------------------|
| **Centrado no Humano** | A tecnologia auxilia, mas a decisão final é do profissional. O sistema NÃO substitui o avaliador |
| **Sustentável** | 100% gratuito, código aberto, sem servidores externos |
| **Resiliente** | Processamento 100% local. Mesmo sem internet, o sistema funciona |

---

## ⚠️ O que NÃO somos

| Item | Explicação |
|------|-------------|
| ❌ | Não somos um sistema que "diagnostica" automaticamente |
| ❌ | Não substituímos o profissional de Educação Física ou Nutrição |
| ❌ | Não tomamos decisões por você |

## ✅ O que SOMOS

| Item | Explicação |
|------|-------------|
| ✅ | Uma ferramenta que potencializa o seu conhecimento profissional |
| ✅ | Um sistema que organiza dados para você interpretar |
| ✅ | Um parceiro tecnológico que respeita o seu julgamento clínico |

> **"A máquina calcula, o profissional interpreta. O BioGestão 360 calcula para você interpretar melhor."**

---

## ⚠️ AVISO IMPORTANTE

> **SISTEMA EM DESENVOLVIMENTO - DADOS PODEM CONTER ERRO**
>
> Este é um projeto **EXCLUSIVAMENTE EDUCACIONAL E ACADÊMICO**. Os cálculos e informações são baseados em fontes científicas, mas podem conter imprecisões.
>
> **Sempre consulte um profissional de saúde antes de fazer mudanças significativas na sua alimentação.**

---

## 📋 Sobre o Projeto

O **BioGestão 360** é uma ferramenta web **gratuita e de código aberto para fins acadêmicos** que permite:

### 🆕 NOVAS FUNCIONALIDADES (Atualização 2026)

| Funcionalidade | Descrição |
|----------------|-----------|
| Separação Adipômetro vs Fita Métrica | Dobras cutâneas (mm) para % de gordura / Circunferências (cm) para tamanho muscular |
| Sistema de 3 Medições com Média Automática | Protocolo científico: 3 tentativas, média calculada automaticamente |
| Dobra Supra-espinal (SS) | Para cálculo do somatotipo de Heath-Carter |
| Handgrip (Força) | Avaliação de força de preensão palmar com classificação |
| Banco de Wells (Flexibilidade) | Avaliação de flexibilidade com classificação |
| Laudo CSV Exclusivo | Botão separado para baixar o laudo da avaliação física |
| Sistema de Unidades Inteligente | Classifica automaticamente alimentos como líquidos (ml), sólidos (g) ou unidades (un) |
| Combinação Unidades × Peso Real | Permite informar 2 unidades de 250ml cada = 500ml total |
| Seleção de Tabela Nutricional | Escolha entre TACO (UNICAMP) ou IBGE (POF 2008-2009) |
| Método Katch-McArdle | GET baseado em MASSA MAGRA (mais preciso que Harris-Benedict) |

### ✅ Funcionalidades já existentes

| Funcionalidade | Descrição |
|----------------|-----------|
| Análise de composição corporal | Percentual de gordura, massa magra, peso ideal |
| Cálculo do gasto energético | TMB e GET (Harris-Benedict ou Katch-McArdle) |
| Planejamento alimentar | Usando Tabela TACO ou IBGE (Diário ou Semanal) |
| Laudo técnico | Com projeção de resultados em 30 dias |
| Modo de impressão econômica | Para economizar tinta/papel |

---

## 🔒 Licenciamento e Uso

### Este NÃO é um software comercial!

Este projeto está licenciado sob a **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**.

### O que isso significa?

| Permissão | Status |
|-----------|--------|
| ✅ Uso acadêmico e educacional | Permitido |
| ✅ Estudo e pesquisa | Permitido |
| ✅ Compartilhamento com atribuição | Permitido |
| ❌ **USO COMERCIAL** | **PROIBIDO** |
| ❌ Venda ou redistribuição paga | **PROIBIDO** |
| ❌ Modificação e distribuição modificada | **PROIBIDO** |

**Para uso comercial, entre em contato com o desenvolvedor.**

---

## 🧠 Metodologia Científica

### Fórmulas utilizadas:

| Cálculo | Fórmula | Fonte |
|---------|---------|-------|
| IMC | Peso / Altura² | OMS |
| TMB (Homem) | 66.47 + (13.75×P) + (5.0×A) - (6.75×I) | Harris-Benedict (1919) |
| TMB (Mulher) | 655.1 + (9.56×P) + (1.85×A) - (4.67×I) | Harris-Benedict (1919) |
| TMB Katch-McArdle | 370 + (21.6 × Massa Magra) | Katch-McArdle (1975) |
| GET | TMB × Fator de Atividade | WHO/FAO |
| % Gordura (IMC - H) | (1.20×IMC) + (0.23×I) - 16.2 | Deurenberg et al. (1991) |
| % Gordura (IMC - M) | (1.20×IMC) + (0.23×I) - 5.4 | Deurenberg et al. (1991) |
| Densidade (H 7 dobras) | 1.112 - (0.00043499×S) + (0.00000055×S²) - (0.00028826×I) | Jackson & Pollock (1978) |
| % Gordura por Densidade | (4.95 / Densidade - 4.5) × 100 | Siri WE (1961) |
| Peso Ideal | IMC ideal (21.7/21.3) × altura² | Metropolitan Life Insurance |
| Variação 30 dias | Saldo calórico × 30 ÷ 7700 | Termodinâmica |

### Fatores de Atividade Física (NAF):

| Nível | Descrição | Fator |
|-------|-----------|-------|
| Sedentário | Sem exercício | 1.2 |
| Leve | 1-3 dias/semana | 1.375 |
| Moderado | 3-5 dias/semana | 1.55 |
| Intenso | 6-7 dias/semana | 1.725 |
| Atleta | Treino pesado 2x/dia | 1.9 |

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
| Endomorfo | Tendência a acumular gordura | >25% (H) / >28% (M) | Déficit calórico + treino de força |
| Mesomorfo | Estrutura atlética natural | 10-18% (H) / 18-25% (M) | Treino equilibrado |
| Ectomorfo | Metabolismo acelerado | <10% (H) / <18% (M) | Superávit calórico + força |

### Handgrip (Força de Preensão Palmar):

| Sexo | Fraco | Regular | Forte |
|------|-------|---------|-------|
| Masculino | <35 kg | 35-45 kg | >45 kg |
| Feminino | <25 kg | 25-35 kg | >35 kg |

### Banco de Wells (Flexibilidade):

| Sexo | Abaixo da média | Média | Acima da média |
|------|-----------------|-------|----------------|
| Masculino | <20 cm | 20-30 cm | >30 cm |
| Feminino | <25 cm | 25-35 cm | >35 cm |

---

## 🚀 Como executar localmente

### Pré-requisitos

- Python 3.10 ou superior
- Pip (gerenciador de pacotes)

### Passo a passo

```bash
git clone https://github.com/adilsonximenes/biogestao-360.git
cd biogestao-360
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Estrutura do Projeto

```
biogestao-360/
├── app.py
├── requirements.txt
├── alimentos.csv
├── tabela_ibge.csv
├── acidos-graxos.csv
├── aminoacidos.csv
├── Taco-4a-Edicao.xlsx
├── tabelacompleta.xls
├── DOCUMENTO_TECNICO.md
├── README.md
└── .gitignore
```

> 💡 Os arquivos `.xlsx` e `.xls` são mantidos como referência original. O sistema utiliza os arquivos `.csv` convertidos.

---

## 🖨️ Funcionalidade de Impressão

O sistema possui um modo especial de impressão que:

| Benefício | Descrição |
|-----------|-----------|
| ✅ Economiza tinta | Fundo branco, texto preto |
| ✅ Remove elementos desnecessários | Sidebar e botões são ocultados |
| ✅ Otimiza margens | Configurado para papel |
| ✅ Mantém informações importantes | Todos os dados do cardápio e laudo |

### Como usar:

1. Clique em "Gerar Versão para Impressão" no menu lateral
2. Aguarde o recarregamento
3. Clique nos 3 pontinhos (⋮) do navegador
4. Selecione "Imprimir"
5. Configure "Margens: Mínimas"
6. Salve como PDF

---

## 📚 Bases de Dados Utilizadas

### Tabela TACO (UNICAMP) - Principal

| Item | Informação |
|------|-------------|
| Fonte | NEPA - Núcleo de Estudos e Pesquisas em Alimentação |
| Instituição | Universidade Estadual de Campinas (UNICAMP) |
| Ano da versão | 2011 (4ª Edição - última versão completa disponível publicamente) |
| Site oficial | https://www.tbca.net.br/ |
| Arquivo no projeto | `alimentos.csv` |
| Dados | Calorias (kcal), Proteínas (g), Carboidratos (g), Gorduras (g) |

### Tabela IBGE (POF 2008-2009) - Alternativa

| Item | Informação |
|------|-------------|
| Fonte | Pesquisa de Orçamentos Familiares (POF) |
| Instituição | Instituto Brasileiro de Geografia e Estatística (IBGE) |
| Ano | 2008-2009 |
| Link oficial | https://www.ibge.gov.br/estatisticas/sociais/populacao/9050-pesquisa-de-orcamentos-familiares.html |
| Arquivo no projeto | `tabela_ibge.csv` |
| Dados | Alimentos in natura e preparações regionais brasileiras |

### FAO/WHO

| Item | Informação |
|------|-------------|
| Organização | Food and Agriculture Organization / World Health Organization |
| Link | https://www.fao.org/ |
| Utilização | Fatores de atividade física e referências nutricionais |

### Arquivos Complementares

| Arquivo | Conteúdo | Status |
|---------|----------|--------|
| `acidos-graxos.csv` | Perfil de ácidos graxos | Disponível para futuras implementações |
| `aminoacidos.csv` | Perfil de aminoácidos | Disponível para futuras implementações |
| `Taco-4a-Edicao.xlsx` | Tabela TACO original | Referência (não usado diretamente) |
| `tabelacompleta.xls` | Tabela IBGE original | Referência (não usado diretamente) |

---

## ⚠️ Limitações da Tabela TACO

Alguns alimentos possuem dados incompletos (valores "NA" ou "traço"). Exemplo: "Leite, de vaca, integral" não tem calorias informadas.

### Como o sistema trata:

- Valores ausentes são convertidos para 0 (zero)
- O cálculo não quebra e continua funcionando
- O usuário é informado sobre a limitação no app

### Recomendação para dados incompletos:

- Consulte fontes complementares (USDA FoodData Central, rótulos nutricionais)
- Utilize o bom senso profissional para ajustes

---

## 🛡️ Privacidade e Segurança - Indústria 5.0

**Zero-Footprint Total!** 🔒

| Benefício | Descrição |
|-----------|-----------|
| ✅ | Nenhum dado é enviado para servidores externos (Resiliência) |
| ✅ | Todo processamento é 100% local no seu navegador (Sustentabilidade) |
| ✅ | Não há banco de dados, login ou coleta de informações (Centrado no humano) |
| ✅ | Ao fechar a aba, todos os dados são permanentemente deletados |
| ✅ | Você pode usar sem preocupações com privacidade |

> **"Seus dados são seus. O BioGestão 360 apenas organiza o que você já sabe."**

---

## 📄 Licença

Este projeto está licenciado sob a **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**.

| Permissão | Status |
|-----------|--------|
| ✅ Compartilhar (copiar e redistribuir) | Permitido com atribuição |
| ✅ Uso acadêmico e educacional | Permitido |
| ❌ Uso comercial | PROIBIDO |
| ❌ Modificar ou criar derivados | PROIBIDO |

Texto completo da licença: https://creativecommons.org/licenses/by-nc-nd/4.0/

---

## 👨‍💻 Desenvolvedor

Desenvolvido como ferramenta educacional para estudo de atividade física e consumo energético de alimentos.

| Item | Informação |
|------|-------------|
| Autor | ADILSON GONCALVES XIMENES |
| Finalidade | Exclusivamente acadêmica e educacional |
| Filosofia | Indústria 5.0 - Tecnologia a serviço do humano |
| Contato para uso comercial | Abrir uma Issue no GitHub |

---

## ⭐ Reconhecimentos

- **UNICAMP / NEPA** - Tabela Brasileira de Composição de Alimentos (TACO)
- **IBGE** - Pesquisa de Orçamentos Familiares (POF 2008-2009)
- **FAO/WHO** - Fatores de Atividade Física e referências nutricionais
- **Harris & Benedict** - Equação de metabolismo basal (1919)
- **Katch & McArdle** - Equação de metabolismo basal por massa magra (1975)
- **Jackson & Pollock** - Protocolo de dobras cutâneas (1978)
- **Siri WE** - Fórmula de densidade para percentual de gordura (1961)
- **Deurenberg et al.** - Fórmula de composição corporal por IMC (1991)
- **ACSM** - American College of Sports Medicine (classificações de referência)
- **IARC/OMS** - Classificação de alimentos cancerígenos
- **Comunidade Streamlit** - Framework para aplicações web
- **Machine Learning Mocha** - Organização do repositório TACO

---

## 📞 Contato

| Tipo | Como |
|------|------|
| Issues | GitHub Issues |
| Uso comercial | Abra uma Issue com o título "USO COMERCIAL" |

---

## 🌐 Language

Currently available in Portuguese (Brazil) only.

If you need an English version, feel free to:

- Fork the repository
- Translate the interface
- Submit a pull request

The code is open source for educational purposes.

---

## 🙏 Agradecimentos

Agradeço a todos que contribuírem academicamente para este projeto! Juntos podemos melhorar a ferramenta e ajudar mais profissionais a realizarem avaliações físicas de qualidade.

---

**Feito com ❤️ para a comunidade acadêmica e desenvolvimento open-source educacional**

*BioGestão 360 - Tecnologia humanizada para avaliação física* 🏋️‍♂️🤝💻
