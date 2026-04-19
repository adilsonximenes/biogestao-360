# 📋 DOCUMENTO TÉCNICO - BioGestão 360

## Metodologia de Cálculos Científicos

**Versão:** 3.2  
**Data:** Abril/2026  
**App:** https://biogestao-360.streamlit.app  
**Repositório:** https://github.com/adilsonximenes/biogestao-360

---

## 1. METABOLISMO E GASTO ENERGÉTICO

### 1.1 Índice de Massa Corporal (IMC)

**Fórmula:**

IMC = Peso (kg) / (Altura (m))²

**Exemplo com dados padrão:**
- Peso = 85.8 kg
- Altura = 164 cm = 1.64 m
- IMC = 85.8 / (1.64 × 1.64) = 85.8 / 2.6896 = 31.9

**Classificação OMS:**
| IMC | Classificação |
|-----|---------------|
| < 18.5 | Abaixo do peso |
| 18.5 - 24.9 | Peso normal |
| 25.0 - 29.9 | Sobrepeso |
| 30.0 - 34.9 | Obesidade Grau I |
| 35.0 - 39.9 | Obesidade Grau II |
| ≥ 40 | Obesidade Grau III |

---

### 1.2 Taxa Metabólica Basal (TMB) - Métodos

#### Método 1: Harris-Benedict (Padrão - baseado no PESO TOTAL)

**Fórmula para HOMENS:**

TMB = 66.47 + (13.75 × Peso) + (5.0 × Altura) - (6.75 × Idade)

**Exemplo (Homem, 85.8kg, 164cm, 47 anos):**

TMB = 66.47 + (13.75 × 85.8) + (5.0 × 164) - (6.75 × 47)
TMB = 66.47 + 1.179,75 + 820 - 317.25
TMB = 1.749 kcal/dia

**Fórmula para MULHERES:**

TMB = 655.1 + (9.56 × Peso) + (1.85 × Altura) - (4.67 × Idade)

#### Método 2: Katch-McArdle (Alternativo - baseado na MASSA MAGRA)

**Fórmula (universal para ambos os sexos):**

TMB = 370 + (21.6 × Massa Magra em kg)

**Exemplo (com Massa Magra de 72.6 kg):**

TMB = 370 + (21.6 × 72.6) = 370 + 1.568,16 = 1.938 kcal/dia

**Comparação dos métodos:**
| Método | Base | Fórmula | Quando usar |
|--------|------|---------|-------------|
| Harris-Benedict | Peso total (gordura + músculos) | TMB = 66.47 + (13.75×P) + (5.0×A) - (6.75×I) | Padrão, para todos |
| Katch-McArdle | Apenas Massa Magra | TMB = 370 + (21.6 × MM) | Mais preciso para alto % de gordura |

> 💡 **Por que Katch-McArdle é mais preciso?** A gordura corporal é metabolicamente inativa (não consome energia). Ao usar apenas a Massa Magra, eliminamos o erro causado pelo excesso de gordura.

---

### 1.3 Gasto Energético Total (GET)

**Fórmula:**

GET = TMB × Fator de Atividade Física (NAF)

**Fatores de Atividade Física (NAF) - Fonte FAO/WHO:**
| Nível | Descrição | Fator |
|-------|-----------|-------|
| Sedentário | Sem exercício | 1.2 |
| Leve | 1-3 dias/semana | 1.375 |
| Moderado | 3-5 dias/semana | 1.55 |
| Intenso | 6-7 dias/semana | 1.725 |
| Atleta | Treino pesado 2x/dia | 1.9 |

**Exemplo (NAF Moderado = 1.55, TMB = 1.749):**

GET = 1.749 × 1.55 = 2.711 kcal/dia

---

### 1.4 Peso Ideal Estimado

**Fórmula:**

Peso Ideal = IMC Ideal × (Altura em metros)²

**IMC Ideal de referência (Metropolitan Life Insurance):**
- Homens = 21.7
- Mulheres = 21.3

**Exemplo (Homem, 1.64m):**

Peso Ideal = 21.7 × (1.64 × 1.64) = 21.7 × 2.6896 = 58.4 kg

---

## 2. COMPOSIÇÃO CORPORAL (Estimada por IMC)

### 2.1 Percentual de Gordura - Fórmula de Deurenberg

**Fórmula para HOMENS:**

% Gordura = (1.20 × IMC) + (0.23 × Idade) - 16.2

**Exemplo (IMC = 31.9, Idade = 47):**

% Gordura = (1.20 × 31.9) + (0.23 × 47) - 16.2
% Gordura = 38.28 + 10.81 - 16.2 = 32.9%

**Fórmula para MULHERES:**

% Gordura = (1.20 × IMC) + (0.23 × Idade) - 5.4

**Limites aplicados:**
- Mínimo = 5%
- Máximo = 50%

---

### 2.2 Massa de Gordura e Massa Magra

**Fórmulas:**

Massa de Gordura = Peso × (% Gordura / 100)
Massa Magra = Peso - Massa de Gordura

**Exemplo:**

Massa de Gordura = 85.8 × (32.9 / 100) = 28.2 kg
Massa Magra = 85.8 - 28.2 = 57.6 kg

---

## 3. AVALIAÇÃO FÍSICA PROFISSIONAL

### 3.1 Equipamentos e Finalidades

| Equipamento | O que avalia | Unidade |
|-------------|--------------|---------|
| **Adipômetro (Plicômetro)** | Gordura subcutânea → % de gordura corporal | mm (milímetros) |
| **Fita Métrica** | Perímetros musculares e circunferências | cm (centímetros) |
| **Handgrip (Dinamômetro)** | Força de preensão palmar | kg/f |
| **Banco de Wells** | Flexibilidade | cm |

---

### 3.2 Protocolo de Medição (3 tentativas)

Para cada dobra cutânea, devem ser realizadas **3 medições não consecutivas**:
- Aguardar 2 segundos para leitura do adipômetro
- Diferença máxima entre medidas = 5%
- Caso exceda, realizar nova série de medições
- Utilizar a **média das 3 medições** nos cálculos
- Todas as medidas devem ser realizadas no **hemicorpo direito** (lado direito do corpo)

---

### 3.3 Dobras Cutâneas Padronizadas (Adipômetro)

| # | Dobra | Localização | Protocolo |
|---|-------|-------------|-----------|
| 1 | **Tríceps (TR)** | Face posterior do braço | 3 ou 7 dobras |
| 2 | **Bíceps (BI)** | Face anterior do braço | 7 dobras |
| 3 | **Peitoral (TX)** | Metade da distância axila-mamilo | 3 ou 7 dobras |
| 4 | **Subescapular (SB)** | 2cm abaixo do ângulo inferior da escápula | 7 dobras |
| 5 | **Axilar Média (AM)** | Intersecção linha axilar média com apêndice xifóide | 7 dobras |
| 6 | **Supra-ilíaca (SI)** | Sobre a crista ilíaca, linha axilar média | 3 ou 7 dobras |
| 7 | **Supra-espinal (SS)** | 5-7cm acima da espinha ilíaca anterior | Somatotipo |
| 8 | **Abdominal (AB)** | 2cm à direita da cicatriz umbilical | 3 ou 7 dobras |
| 9 | **Coxa (CX)** | Ponto médio entre inguinal e patela | 3 ou 7 dobras |
| 10 | **Panturrilha (PN)** | Maior perímetro da perna | 7 dobras |

---

### 3.4 Circunferências Padronizadas (Fita Métrica)

| Medida | Localização | Unidade |
|--------|-------------|---------|
| **Braço Contraído** | Maior circunferência do braço com contração | cm |
| **Peitoral / Tórax** | Altura dos mamilos, em expiração normal | cm |
| **Cintura** | Ponto médio entre costela e crista ilíaca | cm |
| **Quadril** | Maior circunferência glútea | cm |
| **Coxa** | Terço proximal da coxa | cm |
| **Panturrilha** | Maior circunferência da perna | cm |

---

### 3.5 Protocolo Jackson & Pollock (Dobras Cutâneas)

**Protocolos disponíveis:**

| Sexo | Protocolo | Dobras utilizadas |
|------|-----------|-------------------|
| **Masculino** | 3 dobras | Tríceps, Peitoral, Abdome |
| **Masculino** | 7 dobras | Tríceps, Peitoral, Abdome, Subescapular, Axilar, Supra-ilíaca, Coxa |
| **Feminino** | 3 dobras | Tríceps, Supra-ilíaca, Coxa |
| **Feminino** | 7 dobras | Tríceps, Supra-ilíaca, Coxa, Subescapular, Peitoral, Axilar, Abdome |

---

### 3.6 Cálculo da Densidade Corporal

#### Fórmula para HOMENS (3 dobras):

Densidade = 1.10938 - (0.0008267 × Soma) + (0.0000016 × Soma²) - (0.0002574 × Idade)

#### Fórmula para HOMENS (7 dobras):

Densidade = 1.112 - (0.00043499 × Soma) + (0.00000055 × Soma²) - (0.00028826 × Idade)

#### Fórmula para MULHERES (3 dobras):

Densidade = 1.0994921 - (0.0009929 × Soma) + (0.0000023 × Soma²) - (0.0001392 × Idade)

#### Fórmula para MULHERES (7 dobras):

Densidade = 1.097 - (0.00046971 × Soma) + (0.00000056 × Soma²) - (0.00012828 × Idade)

**Exemplo (Homem, 7 dobras, Soma = 116.5 mm, Idade = 47):**

Densidade = 1.112 - (0.00043499 × 116.5) + (0.00000055 × 13.572,25) - (0.00028826 × 47)
Densidade = 1.112 - 0.05068 + 0.00746 - 0.01355
Densidade = 1.055 g/cm³

---

### 3.7 Percentual de Gordura por Densidade (Fórmula de Siri)

**Fórmula:**

% Gordura = (4.95 / Densidade - 4.5) × 100

**Exemplo (Densidade = 1.055 g/cm³):**

% Gordura = (4.95 / 1.055 - 4.5) × 100
% Gordura = (4.69 - 4.5) × 100 = 19.0%

---

### 3.8 Massas a partir da Avaliação Física

**Fórmulas:**
Massa de Gordura = Peso × (% Gordura / 100)
Massa Magra = Peso - Massa de Gordura

---

### 3.9 Classificação do Percentual de Gordura (ACSM)

| Classificação | Homens | Mulheres | Risco |
|---------------|--------|----------|-------|
| **Gordura Essencial** | 2-5% | 10-13% | Mínimo |
| **Atleta** | 6-13% | 14-20% | Muito baixo |
| **Saudável** | 14-17% | 21-24% | Baixo |
| **Aceitável** | 18-21% | 25-31% | Moderado |
| **Obesidade** | >22% | >32% | Alto |

---

### 3.10 Biotipo Corporal (Heath-Carter adaptado)

| Biotipo | Característica | % Gordura típico | Recomendação |
|---------|----------------|------------------|--------------|
| **Endomorfo** | Tendência a acumular gordura | >25% (H) / >28% (M) | Déficit calórico + treino de força |
| **Mesomorfo** | Estrutura atlética natural | 10-18% (H) / 18-25% (M) | Treino equilibrado |
| **Ectomorfo** | Metabolismo acelerado | <10% (H) / <18% (M) | Superávit calórico + força |

---

### 3.11 Avaliações Complementares

#### Handgrip (Força de Preensão Palmar)

| Sexo | Fraco | Regular | Forte |
|------|-------|---------|-------|
| **Masculino** | <35 kg | 35-45 kg | >45 kg |
| **Feminino** | <25 kg | 25-35 kg | >35 kg |

#### Banco de Wells (Flexibilidade)

| Sexo | Abaixo da média | Média | Acima da média |
|------|-----------------|-------|----------------|
| **Masculino** | <20 cm | 20-30 cm | >30 cm |
| **Feminino** | <25 cm | 25-35 cm | >35 cm |

---

## 4. PLANEJAMENTO ALIMENTAR

### 4.1 Cálculo de Calorias por Alimento

**Fórmula:**

Calorias do alimento = (Energia por 100g da Tabela Nutricional) × (Peso informado / 100)

**Exemplo (Arroz integral cozido, 50g):**

Tabela TACO: Arroz integral cozido = 124 kcal/100g
Calorias = 124 × (50 / 100) = 62 kcal

---

### 4.2 Cálculo de Macronutrientes

**Fórmula (para cada nutriente):**

Nutriente = (Valor na Tabela por 100g) × (Peso informado / 100)

**Exemplo (Proteínas do arroz integral cozido, 50g):**

Tabela TACO: Proteínas = 2.6g/100g
Proteínas = 2.6 × (50 / 100) = 1.3g

---

### 4.3 Totais do Cardápio

**Diário:**

Total kcal = Soma(Calorias de todos os alimentos do dia)
Total Proteínas = Soma(Proteínas de todos os alimentos do dia)
Total Carboidratos = Soma(Carboidratos de todos os alimentos do dia)
Total Gorduras = Soma(Gorduras de todos os alimentos do dia)

**Semanal:**

Total kcal = Soma(Calorias de todos os alimentos da semana)
Média diária = Total kcal / 7

---

### 4.4 Sistema de Unidades Inteligente

#### Classificação por categoria e palavras-chave:

| Tipo | Unidade | Exemplos |
|------|---------|----------|
| **Líquidos** | ml | Leite, suco, café, refrigerante, cerveja, vinho |
| **Sólidos** | g | Arroz, feijão, carne, frango, canjica, farinha |
| **Unidades** | un | Ovos, codorna, biscoitos, frutas, pães |

#### Tabela de Pesos Reais por Unidade (calibrada):

| Alimento | Peso por unidade |
|----------|------------------|
| Biscoito maisena | 5g |
| Pão francês | 50g |
| Maçã | 150g |
| Banana | 100g |
| Laranja | 120g |
| Ovo de galinha | 50g |
| Ovo de codorna | 9g |
| Queijo (fatia) | 20g |

#### Combinação de Unidades com Peso Real:

- Se **Peso Real > 0**: `Peso Final = Peso Real × Quantidade`
- Se **Peso Real = 0** (não informado): usar estimativa da tabela acima

**Exemplos:**
- 2 unidades de suco com 250ml cada = 500ml total
- 3 unidades de ovo com 50g cada = 150g total

---

### 4.5 Tratamento de Dados Ausentes nas Tabelas

**Problema identificado:**
As tabelas TACO e IBGE contêm valores "NA", "*", "Tr", "-" para alguns alimentos.

**Solução implementada:**
```python
def tratar_valor_nutricional(valor):
    if valor is None or pd.isna(valor):
        return 0.0
    if isinstance(valor, str):
        valor = valor.strip().upper()
        if valor in ['NA', 'N/A', '*', 'TR', '-', '']:
            return 0.0
        valor = valor.replace(',', '.')
        try:
            return float(valor)
        except ValueError:
            return 0.0
    return float(valor) if not pd.isna(valor) else 0.0
```
Impacto:

. Alimentos com dados completos: calculados normalmente

. Alimentos com dados ausentes: contribuem com 0 (zero) para os totais

. O sistema NÃO quebra (sem NaN ou erros)

5. LAUDO TÉCNICO DE VIABILIDADE ALIMENTAR
5.1 Consumo Planejado

Consumo Planejado = Total de calorias do cardápio (diário) ou Média diária (semanal)
5.2 Saldo Energético
Fórmula:

Saldo Energético = GET - Consumo Planejado
Interpretação:

Saldo positivo (Déficit) = Consumo menor que o gasto → Perda de peso

Saldo negativo (Superávit) = Consumo maior que o gasto → Ganho de peso

Exemplo:

text
GET = 2.099 kcal
Consumo = 1.200 kcal
Saldo = 2.099 - 1.200 = 899 kcal (Déficit)

5.3 Distribuição dos Macronutrientes
Calorias por grama:

Proteínas = 4 kcal/g

Carboidratos = 4 kcal/g

Gorduras = 9 kcal/g

Percentual calórico:

% Proteínas = (Proteínas × 4 / Total kcal) × 100
% Carboidratos = (Carboidratos × 4 / Total kcal) × 100
% Gorduras = (Gorduras × 9 / Total kcal) × 100

Exemplo:

Proteínas = 31.3g, Carboidratos = 106g, Gorduras = 16.6g, Total kcal = 706.8
% Proteínas = (31.3 × 4 / 706.8) × 100 = 17.7%
% Carboidratos = (106 × 4 / 706.8) × 100 = 60.0%
% Gorduras = (16.6 × 9 / 706.8) × 100 = 21.1%
Referência OMS recomendada:

Proteínas = 10-35%

Carboidratos = 45-65%

Gorduras = 20-35%

5.4 Projeção de Resultados
Base termodinâmica:

1 kg de gordura corporal ≈ 7.700 kcal
Projeção de variação de peso:

Variação em 30 dias = |Saldo diário| × 30 / 7.700
Exemplo:

Saldo diário = 899 kcal (Déficit)
Variação em 30 dias = 899 × 30 / 7.700 = 3.50 kg de perda
5.5 Tempo Estimado para Meta

Fórmula:

Semanas para meta = |Peso atual - Meta| / (Variação semanal)

Exemplo:

Peso atual = 85.8 kg
Meta = 75.8 kg
Diferença = 10.0 kg
Variação semanal = 0.5 kg
Semanas = 10.0 / 0.5 = 20 semanas

6. ALERTAS OMS (Alimentos de Risco)
Classificação IARC/OMS:

Grupo	Classificação	Alimentos	Recomendação
Grupo 1	Cancerígeno para humanos	Carnes processadas (salsicha, presunto, bacon, salame, mortadela), Bebidas alcoólicas	Evitar ou reduzir drasticamente
Grupo 2A	Provavelmente cancerígeno	Carne vermelha (bovina, suína, ovina, caprina)	Limitar a 500g por semana
Grupo 2B	Possivelmente cancerígeno	Aspartame, bebidas muito quentes (>65°C)	Consumo moderado

7. BASES DE DADOS UTILIZADAS

7.1 Tabela TACO (UNICAMP) - Principal
Item	Informação
Fonte	NEPA - Núcleo de Estudos e Pesquisas em Alimentação
Instituição	Universidade Estadual de Campinas (UNICAMP)
Versão	4ª Edição (2011) - última versão completa disponível publicamente
Site oficial	https://www.tbca.net.br/
Arquivo no projeto	alimentos.csv
Dados	Calorias (kcal), Proteínas (g), Carboidratos (g), Gorduras (g)

7.2 Tabela IBGE (POF 2008-2009) - Alternativa
Item	Informação
Fonte	Pesquisa de Orçamentos Familiares (POF)
Instituição	Instituto Brasileiro de Geografia e Estatística (IBGE)
Ano	2008-2009
Link oficial	https://www.ibge.gov.br/estatisticas/sociais/populacao/9050-pesquisa-de-orcamentos-familiares.html
Arquivo no projeto	tabela_ibge.csv
Dados	Alimentos in natura e preparações regionais brasileiras

7.3 FAO/WHO
Item	Informação
Organização	Food and Agriculture Organization / World Health Organization
Link	https://www.fao.org/
Utilização	Fatores de atividade física e referências nutricionais

7.4 Arquivos do Sistema
Arquivo	Conteúdo	Utilização
app.py	Aplicação principal Streamlit	Execução do sistema
requirements.txt	Dependências do projeto	Instalação de pacotes
alimentos.csv	Dados nutricionais TACO	Principal - usado nos cálculos
tabela_ibge.csv	Tabela IBGE POF 2008-2009	Alternativa - selecionável pelo usuário
acidos-graxos.csv	Perfil de ácidos graxos	Complementar (futuro)
aminoacidos.csv	Perfil de aminoácidos	Complementar (futuro)
README.md	Documentação do projeto	-
.gitignore	Arquivos ignorados pelo Git	-

8. REFERÊNCIAS CIENTÍFICAS
Cálculo	Fórmula	Fonte	Ano
TMB (Homens)	66.47 + (13.75 × P) + (5.0 × A) - (6.75 × I)	Harris-Benedict	1919
TMB (Mulheres)	655.1 + (9.56 × P) + (1.85 × A) - (4.67 × I)	Harris-Benedict	1919
TMB (Katch-McArdle)	370 + (21.6 × Massa Magra)	Katch-McArdle	1975
GET	TMB × Fator Atividade	WHO/FAO/UNU	1985
% Gordura (IMC)	(1.20 × IMC) + (0.23 × I) - (16.2 ou 5.4)	Deurenberg et al.	1991
Densidade Corporal	Protocolo Jackson & Pollock	Jackson AS, Pollock ML	1978
% Gordura por Densidade	(4.95 / Densidade - 4.5) × 100	Siri WE	1961
Classificação % Gordura	Tabela ACSM	American College of Sports Medicine	-
Classificação IMC	Tabela OMS	World Health Organization	-

9. DECLARAÇÃO DE TRANSPARÊNCIA
O BioGestão 360 é um software de código aberto e 100% gratuito. Todos os cálculos são realizados localmente no navegador do usuário, sem envio de dados para servidores externos.

Filosofia: Indústria 5.0
Pilar	Aplicação
🌍 Centrado no Humano	A tecnologia auxilia, mas a decisão final é do profissional
🌱 Sustentável	100% gratuito, código aberto, sem servidores externos
🔄 Resiliente	Processamento 100% local, funciona offline
"A máquina calcula, o profissional interpreta. O BioGestão 360 calcula para você interpretar melhor."

Links úteis:

🔗 Código fonte: https://github.com/adilsonximenes/biogestao-360

🌐 App online: https://biogestao-360.streamlit.app

📚 Tabela TACO: https://www.tbca.net.br/

📊 IBGE - POF: https://www.ibge.gov.br/estatisticas/sociais/populacao/9050-pesquisa-de-orcamentos-familiares.html

🌍 FAO/WHO: https://www.fao.org/

Documento gerado em: Abril/2026
Versão: 3.2
Status: ✅ COMPLETO E CORRIGIDO
