# DOCUMENTO TÉCNICO - BioGestão 360

**Versão:** 4.0 | **Data:** Maio/2026
**App:** https://biogestao-360.streamlit.app

---

## 1. METABOLISMO E GASTO ENERGETICO

### IMC

`IMC = Peso(kg) / Altura(m)²`

### TMB - Harris-Benedict

**Homens:** `66.47 + (13.75 x Peso) + (5.0 x Altura) - (6.75 x Idade)`

**Mulheres:** `655.1 + (9.56 x Peso) + (1.85 x Altura) - (4.67 x Idade)`

### TMB - Katch-McArdle (Massa Magra)

`TMB = 370 + (21.6 x Massa Magra em kg)`

### GET (Gasto Energético Total)

`GET = TMB x Fator Atividade`

**Fatores Atividade (NAF):**

- Sedentario = 1.2
- Leve (1-3x/semana) = 1.375
- Moderado (3-5x/semana) = 1.55
- Intenso (6-7x/semana) = 1.725
- Atleta (2x/dia) = 1.9

### Peso Ideal

`Peso Ideal = IMC Ideal x Altura(m)²`  
IMC Ideal: Homem=21.7 | Mulher=21.3

---

## 2. COMPOSIÇÃO CORPORAL (Estimativa por IMC)

### % Gordura - Deurenberg

**Homem:** `(1.20 x IMC) + (0.23 x Idade) - 16.2`

**Mulher:** `(1.20 x IMC) + (0.23 x Idade) - 5.4`

_Limites: min 5% | max 50%_

### Massas

`Massa Gordura = Peso x (%Gordura/100)`

`Massa Magra = Peso - Massa Gordura`

---

## 3. AVALIAÇÃO FISICA PROFISSIONAL

### Equipamentos

| Equipamento  | Avalia                | Unidade |
| ------------ | --------------------- | ------- |
| Adipometro   | Gordura subcutanea    | mm      |
| Fita Metrica | Perimetros musculares | cm      |
| Handgrip     | Forca preensao palmar | kg/f    |
| Banco Wells  | Flexibilidade         | cm      |

### Protocolo 3 Medicoes

- 3 medicoes nao consecutivas por dobra
- Media calculada automaticamente
- Diferenca maxima entre medidas: 5%

### Dobras Cutaneas (10 pontos)

| Dobra         | Localizacao                 | Protocolo     |
| ------------- | --------------------------- | ------------- |
| Triceps       | Face posterior braco        | 3 ou 7 dobras |
| Biceps        | Face anterior braco         | 7 dobras      |
| Peitoral      | Metade axila-mamilo         | 3 ou 7 dobras |
| Subescapular  | 2cm abaixo escapula         | 7 dobras      |
| Axilar Media  | Linha axilar media          | 7 dobras      |
| Supra-iliaca  | Sobre crista iliaca         | 3 ou 7 dobras |
| Supra-espinal | 5-7cm acima espinha iliaca  | Somatotipo    |
| Abdominal     | 2cm direita umbigo          | 3 ou 7 dobras |
| Coxa          | Ponto medio inguinal-patela | 3 ou 7 dobras |
| Panturrilha   | Maior perimetro perna       | 7 dobras      |

### Circunferencias (Fita Metrica)

| Medida          | Unidade |
| --------------- | ------- |
| Braco Contraido | cm      |
| Peitoral/Torax  | cm      |
| Cintura         | cm      |
| Quadril         | cm      |
| Coxa            | cm      |
| Panturrilha     | cm      |

### Jackson & Pollock - Densidade Corporal

**Homem 3 dobras:** `1.10938 - (0.0008267 x Soma) + (0.0000016 x Soma²) - (0.0002574 x Idade)`

**Homem 7 dobras:** `1.112 - (0.00043499 x Soma) + (0.00000055 x Soma²) - (0.00028826 x Idade)`

**Mulher 3 dobras:** `1.0994921 - (0.0009929 x Soma) + (0.0000023 x Soma²) - (0.0001392 x Idade)`

**Mulher 7 dobras:** `1.097 - (0.00046971 x Soma) + (0.00000056 x Soma²) - (0.00012828 x Idade)`

### % Gordura por Densidade - Siri

`%Gordura = (4.95 / Densidade - 4.5) x 100`

### Classificacao % Gordura (ACSM)

| Classificacao     | Homem  | Mulher | Risco       |
| ----------------- | ------ | ------ | ----------- |
| Gordura Essencial | 2-5%   | 10-13% | Minimo      |
| Atleta            | 6-13%  | 14-20% | Muito baixo |
| Saudavel          | 14-17% | 21-24% | Baixo       |
| Aceitavel         | 18-21% | 25-31% | Moderado    |
| Obesidade         | >22%   | >32%   | Alto        |

### Biotipos (Heath-Carter)

| Biotipo   | % Gordura tipico  | Recomendacao               |
| --------- | ----------------- | -------------------------- |
| Endomorfo | H>25% / M>28%     | Deficit calorico + forca   |
| Mesomorfo | H10-18% / M18-25% | Treino equilibrado         |
| Ectomorfo | H<10% / M<18%     | Superavit calorico + forca |

### Avaliacoes Complementares

**Handgrip (Forca)**

- Homem: Fraco <35 | Regular 35-45 | Forte >45 kg/f
- Mulher: Fraco <25 | Regular 25-35 | Forte >35 kg/f

**Banco Wells (Flexibilidade)**

- Homem: Abaixo <20 | Media 20-30 | Acima >30 cm
- Mulher: Abaixo <25 | Media 25-35 | Acima >35 cm

---

## 4. PLANEJAMENTO ALIMENTAR

### Calculo Calorias

`Calorias = (Energia/100g Tabela) x (Peso informado / 100)`

### Sistema Unidades Inteligente

| Tipo     | Unidade | Exemplos                        |
| -------- | ------- | ------------------------------- |
| Liquidos | ml      | Suco, leite, cafe, refrigerante |
| Solidos  | g       | Arroz, feijao, carne            |
| Unidades | un      | Ovos, biscoitos, frutas, paes   |

### Pesos por Unidade (Tabela calibrada)

| Alimento         | Peso por unidade |
| ---------------- | ---------------- |
| Biscoito maisena | 5g               |
| Pao frances      | 50g              |
| Maca             | 150g             |
| Banana           | 100g             |
| Laranja          | 120g             |
| Ovo galinha      | 50g              |
| Ovo codorna      | 9g               |
| Queijo fatia     | 20g              |

### Tratamento dados ausentes

Valores 'NA', '\*', 'Tr', '-' sao convertidos para 0 (zero)

---

## 5. LAUDO TECNICO

### Saldo Energetico

`Saldo = GET - Consumo Planejado`

Saldo positivo = Deficit (perda peso)  
Saldo negativo = Superavit (ganho peso)

### Distribuicao Macronutrientes

| Nutriente   | kcal/g |
| ----------- | ------ |
| Proteina    | 4      |
| Carboidrato | 4      |
| Gordura     | 9      |

### Projecao 30 dias

`Variacao(kg) = |Saldo diario| x 30 / 7700`

### Tempo estimado meta

`Semanas = |Peso atual - Meta| / Variacao semanal`

---

## 6. ALERTAS OMS (IARC)

| Grupo    | Classificacao             | Alimentos                  | Recomendacao    |
| -------- | ------------------------- | -------------------------- | --------------- |
| Grupo 1  | Cancerigeno humano        | Carnes processadas, alcool | Evitar          |
| Grupo 2A | Provavelmente cancerigeno | Carne vermelha             | Max 500g/semana |
| Grupo 2B | Possivelmente cancerigeno | Aspartame, bebidas >65°C   | Moderado        |

---

## 7. BASES DE DADOS

| Fonte              | Arquivo         | Conteudo                                |
| ------------------ | --------------- | --------------------------------------- |
| TACO/UNICAMP       | alimentos.csv   | Kcal, Proteinas, Carboidratos, Gorduras |
| IBGE POF 2008-2009 | tabela_ibge.csv | Alimentos in natura e regionais         |
| FAO/WHO            | -               | Fatores atividade fisica                |

---

## 8. REFERENCIAS CIENTIFICAS

| Calculo                 | Fonte             | Ano  |
| ----------------------- | ----------------- | ---- |
| TMB Harris-Benedict     | Harris & Benedict | 1919 |
| TMB Katch-McArdle       | Katch & McArdle   | 1975 |
| % Gordura por IMC       | Deurenberg et al. | 1991 |
| Protocolo Dobras        | Jackson & Pollock | 1978 |
| % Gordura por Densidade | Siri WE           | 1961 |
| GET x NAF               | WHO/FAO/UNU       | 1985 |

---

## 9. DEPENDÊNCIAS E BIBLIOTECAS UTILIZADAS

| Biblioteca      | Versão  | Finalidade                                    |
| --------------- | ------- | --------------------------------------------- |
| streamlit       | ≥1.35.0 | Framework web para interface do usuário       |
| pandas          | ≥2.0.0  | Manipulação e análise de dados                |
| plotly          | ≥5.24.0 | Gráficos interativos na tela                  |
| matplotlib      | ≥3.7.0  | Geração de gráficos estáticos para PDF        |
| qrcode          | ≥7.0.0  | Geração de QR Code PIX para doações           |
| pillow          | ≥10.0.0 | Manipulação de imagens                        |
| openpyxl        | ≥3.1.0  | Leitura de arquivos Excel (tabelas originais) |
| numpy           | ≥1.24.0 | Operações matemáticas e arrays                |
| psycopg2-binary | ≥2.9.0  | Conexão com banco PostgreSQL/Supabase         |
| pyotp           | ≥2.9.0  | Autenticação de dois fatores (2FA Admin)      |

### Instalação

```bash
pip install -r requirements.txt
pip install psycopg2-binary pyotp
```

---

**Documento gerado em:** Abril/2026  
**Status:** COMPLETO E CORRIGIDO
