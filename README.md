# 🏋️‍♂️ BioGestão 360

**Sistema universal de análise de bioimpedância e planejamento alimentar baseado na metodologia TACO e protocolos científicos Harris-Benedict**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biogestao-360.streamlit.app)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## ⚠️ **AVISO IMPORTANTE**

> **SISTEMA EM DESENVOLVIMENTO BASEADO NA TABELA TACO - DADOS PODEM CONTER ERRO**
> 
> Este é um projeto **EXCLUSIVAMENTE EDUCACIONAL E ACADÊMICO**. Os cálculos e informações são baseados em fontes científicas, mas podem conter imprecisões. 
> **Sempre consulte um profissional de saúde antes de fazer mudanças significativas na sua alimentação.**

---

## 📋 **Sobre o Projeto**

O **BioGestão 360** é uma ferramenta web **gratuita e de código aberto para fins acadêmicos** que permite:

- ✅ **Análise de composição corporal** (percentual de gordura, massa magra, peso ideal)
- ✅ **Cálculo do gasto energético** (TMB e GET baseado em Harris-Benedict)
- ✅ **Planejamento alimentar** usando a Tabela TACO (Tabela Brasileira de Composição de Alimentos)
- ✅ **Laudo técnico** com projeção de resultados em 30 dias
- ✅ **Interface adaptativa** que segue o tema do seu sistema operacional
- ✅ **Modo de impressão econômica** para economizar tinta/papel

### 🎯 **Público-alvo**

- Estudantes de nutrição e educação física
- Profissionais da saúde que buscam uma ferramenta de apoio educacional
- Desenvolvedores interessados em projetos de saúde tech
- Pesquisadores da área de nutrição e metabolismo

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

## 🤝 Como Contribuir (Academicamente)
Este é um projeto acadêmico e toda contribuição educacional é bem-vinda!

Você pode ajudar de várias formas:
🐛 Reportar bugs → Abra uma Issue

💡 Sugerir melhorias → Abra uma Issue

📚 Melhorar documentação → Corrija erros ou adicione exemplos

🔬 Validar dados científicos → Compare com outras fontes

🧪 Testar em diferentes cenários → Compartilhe os resultados

⚠️ Importante sobre contribuições:
Todas as contribuições devem ser para fins acadêmicos

Não serão aceitas contribuições para uso comercial

Ao contribuir, você concorda com a licença CC BY-NC-ND 4.0

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
Este projeto está licenciado sob a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).

Resumo da licença:
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

Contato para uso comercial: Abrir uma Issue no GitHub

## ⭐ Reconhecimentos
UNICAMP - Tabela TACO

Harris & Benedict - Equação de metabolismo basal

Deurenberg et al. - Fórmula de composição corporal

Comunidade Streamlit - Framework incrível

## 📞 Contato
Issues: GitHub Issues

Para uso comercial: Abra uma Issue com o título "USO COMERCIAL"

## 🙏 Agradecimentos
Agradeço a todos que contribuírem academicamente para este projeto! Juntos podemos melhorar a ferramenta e ajudar mais pessoas a entenderem sua saúde metabólica.

Feito com ❤️ para a comunidade acadêmica e desenvolvimento open-source educacional
```bash

---

## 📜 **Arquivo LICENSE (crie um arquivo `LICENSE` no repositório)**

```markdown
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International

Creative Commons Corporation ("Creative Commons") não é uma sociedade de advogados e não presta serviços jurídicos ou aconselhamento. A distribuição desta licença não cria uma relação advogado-cliente ou qualquer outra relação. A Creative Commons disponibiliza as suas licenças e informações relacionadas "no estado em que se encontram". A Creative Commons não oferece garantias em relação às suas licenças, aos materiais licenciados nos seus termos, ou a qualquer informação relacionada. A Creative Commons exime-se de toda a responsabilidade por danos resultantes da sua utilização na máxima medida possível.

### Uso da Licença Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International

Este trabalho está licenciado sob a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International. Para visualizar uma cópia desta licença, visite http://creativecommons.org/licenses/by-nc-nd/4.0/ ou envie uma carta para Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

### Você tem permissão para:

- **Compartilhar** — copiar e redistribuir o material em qualquer suporte ou formato

### Sob as seguintes condições:

- **Atribuição** — Você deve dar o crédito apropriado, prover um link para a licença e indicar se mudanças foram feitas. Você deve fazê-lo em qualquer circunstância razoável, mas de nenhuma maneira que sugira que o licenciante apoia você ou o seu uso.

- **NãoComercial** — Você não pode usar o material para fins comerciais.

- **SemDerivações** — Se você remixar, transformar ou criar a partir do material, você não pode distribuir o material modificado.

- **Sem restrições adicionais** — Você não pode aplicar termos jurídicos ou medidas de caráter tecnológico que restrinjam legalmente outros de fazerem algo que a licença permita.

### Avisos:

Não é necessário cumprir com os termos da licença em relação aos elementos do material que estejam no domínio público ou cuja utilização seja permitida por uma exceção ou limite aplicável.

Não são dadas quaisquer garantias. A licença pode não lhe dar todas as autorizações necessárias para o uso pretendido. Por exemplo, outros direitos, tais como direitos de imagem, de privacidade ou direitos morais, podem limitar o uso do material.
```
