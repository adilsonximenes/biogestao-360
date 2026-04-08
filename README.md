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
```
2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. **Instale as dependências**
```bash
pip install -r requirements.txt
```
4. **Execute o aplicativo**
 ```bash
streamlit run app.py
```
5. **Acesse no navegador**
```bash
http://localhost:8501
```
## 📁 Estrutura do Projeto
````bash
biogestao-360/
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências do projeto
├── alimentos.csv          # Base de dados TACO (alimentos)
├── acidos-graxos.csv      # Base de dados (ácidos graxos)
├── aminoacidos.csv        # Base de dados (aminoácidos)
├── README.md              # Este arquivo
└── .gitignore             # Arquivos ignorados pelo Git
````

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

## 🤝 Como Contribuir
Este é um projeto open-source e toda contribuição é bem-vinda!

Você pode ajudar de várias formas:
Reportar bugs → Abra uma Issue

Sugerir melhorias → Abra uma Issue

Enviar código → Faça um Fork e abra um Pull Request

Melhorar documentação → Corrija erros ou adicione exemplos

Compartilhar → Divulgue o projeto para quem possa se beneficiar

Diretrizes para Pull Requests:
Fork o projeto

Crie uma branch para sua feature (git checkout -b feature/nova-feature)

Commit suas mudanças (git commit -m 'Adiciona nova feature')

Push para a branch (git push origin feature/nova-feature)

Abra um Pull Request

## 📊 Base de Dados - Tabela TACO
Os dados alimentares são baseados na Tabela Brasileira de Composição de Alimentos (TACO) desenvolvida pela Universidade Estadual de Campinas (UNICAMP).

Fonte: NEPA - Núcleo de Estudos e Pesquisas em Alimentação

Instituição: UNICAMP

Ano da versão utilizada: 2011 (última versão completa disponível publicamente)

⚠️ Nota sobre os dados: A tabela TACO tem limitações e pode não refletir variações sazonais, regionais ou de preparo dos alimentos. Este projeto usa os dados "como estão" para fins educacionais.

## 🛡️ Privacidade e Segurança
Zero-Footprint Total! 🔒

✅ Nenhum dado é enviado para servidores externos

✅ Todo processamento é 100% local no seu navegador

✅ Não há banco de dados, login ou coleta de informações

✅ Ao fechar a aba, todos os dados são permanentemente deletados

✅ Você pode usar sem preocupações com privacidade

## 📄 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

Resumo da licença MIT:

✅ Uso comercial permitido

✅ Modificação permitida

✅ Distribuição permitida

✅ Uso privado permitido

❌ Sem garantias

❌ Requer atribuição

## 👨‍💻 Desenvolvedor
Desenvolvido como ferramenta educacional para estudo de atividade física e consumo energético de alimentos.

## ⭐ Reconhecimentos
UNICAMP - Tabela TACO

Harris & Benedict - Equação de metabolismo basal

Deurenberg et al. - Fórmula de composição corporal

Comunidade Streamlit - Framework incrível

## 📞 Contato
Issues: GitHub Issues

Discord: [Link para servidor (se tiver)]

## 🙏 Agradecimentos
Agradeço a todos que contribuírem para este projeto! Juntos podemos melhorar a ferramenta e ajudar mais pessoas a entenderem sua saúde metabólica.

Feito com ❤️ para a comunidade de saúde e desenvolvimento open-source


## 📄 **Também crie o arquivo `.gitignore`**

Para não subir arquivos desnecessários, crie um arquivo `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```
