# DOCUMENTO TÉCNICO — BioGestão 360

**Versão:** 4.2 | **Data:** Maio/2026
**App:** https://biogestao-360.streamlit.app

---

## 1. METABOLISMO E GASTO ENERGÉTICO

### IMC

`IMC = Peso(kg) / Altura(m)²`

### TMB — Harris-Benedict

**Homens:** `66.47 + (13.75 × Peso) + (5.0 × Altura) - (6.75 × Idade)`

**Mulheres:** `655.1 + (9.56 × Peso) + (1.85 × Altura) - (4.67 × Idade)`

### TMB — Katch-McArdle (Massa Magra)

`TMB = 370 + (21.6 × Massa Magra em kg)`

### GET (Gasto Energético Total)

`GET = TMB × Fator de Atividade`

**Fatores de Atividade (NAF):**

| Nível      | Descrição            | Fator |
| ---------- | -------------------- | ----- |
| Sedentário | Sem exercício        | 1.2   |
| Leve       | 1-3x/semana          | 1.375 |
| Moderado   | 3-5x/semana          | 1.55  |
| Intenso    | 6-7x/semana          | 1.725 |
| Atleta     | 2x/dia               | 1.9   |

### Peso Ideal

`Peso Ideal = IMC Ideal × Altura(m)²`

IMC Ideal: Homem = 21.7 | Mulher = 21.3

---

## 2. COMPOSIÇÃO CORPORAL (Estimativa por IMC)

### % Gordura — Deurenberg et al. (1991)

**Homem:** `(1.20 × IMC) + (0.23 × Idade) - 16.2`

**Mulher:** `(1.20 × IMC) + (0.23 × Idade) - 5.4`

_Limites aplicados: mín 5% | máx 50%_

### Massas

`Massa Gordura = Peso × (%Gordura / 100)`

`Massa Magra = Peso - Massa Gordura`

---

## 3. AVALIAÇÃO FÍSICA PROFISSIONAL

> Seção exclusiva para profissionais de Educação Física habilitados (CREF ativo).

### Equipamentos

| Equipamento  | Avalia                 | Unidade |
| ------------ | ---------------------- | ------- |
| Adipômetro   | Gordura subcutânea     | mm      |
| Fita Métrica | Perímetros musculares  | cm      |
| Handgrip     | Força preensão palmar  | kg/f    |
| Banco Wells  | Flexibilidade          | cm      |

### Protocolo de 3 Medições

- 3 medições não consecutivas por dobra
- Média calculada automaticamente
- Diferença máxima aceita entre medidas: 5%

### Dobras Cutâneas (10 pontos)

| Dobra         | Localização                  | Protocolo     |
| ------------- | ---------------------------- | ------------- |
| Tríceps       | Face posterior do braço      | 3 ou 7 dobras |
| Bíceps        | Face anterior do braço       | 7 dobras      |
| Peitoral      | Metade axila-mamilo          | 3 ou 7 dobras |
| Subescapular  | 2cm abaixo da escápula       | 7 dobras      |
| Axilar Média  | Linha axilar média           | 7 dobras      |
| Supra-ilíaca  | Sobre a crista ilíaca        | 3 ou 7 dobras |
| Supra-espinal | 5-7cm acima espinha ilíaca   | Somatotipo    |
| Abdominal     | 2cm à direita do umbigo      | 3 ou 7 dobras |
| Coxa          | Ponto médio inguinal-patela  | 3 ou 7 dobras |
| Panturrilha   | Maior perímetro da perna     | 7 dobras      |

### Circunferências (Fita Métrica)

| Medida          | Unidade |
| --------------- | ------- |
| Braço Contraído | cm      |
| Peitoral/Tórax  | cm      |
| Cintura         | cm      |
| Quadril         | cm      |
| Coxa            | cm      |
| Panturrilha     | cm      |

### Jackson & Pollock — Densidade Corporal

**Homem 3 dobras:** `1.10938 - (0.0008267 × Soma) + (0.0000016 × Soma²) - (0.0002574 × Idade)`

**Homem 7 dobras:** `1.112 - (0.00043499 × Soma) + (0.00000055 × Soma²) - (0.00028826 × Idade)`

**Mulher 3 dobras:** `1.0994921 - (0.0009929 × Soma) + (0.0000023 × Soma²) - (0.0001392 × Idade)`

**Mulher 7 dobras:** `1.097 - (0.00046971 × Soma) + (0.00000056 × Soma²) - (0.00012828 × Idade)`

### % Gordura por Densidade — Siri (1961)

`%Gordura = (4.95 / Densidade - 4.5) × 100`

### Classificação % Gordura (ACSM)

| Classificação     | Homem  | Mulher | Risco       |
| ----------------- | ------ | ------ | ----------- |
| Gordura Essencial | 2-5%   | 10-13% | Mínimo      |
| Atleta            | 6-13%  | 14-20% | Muito baixo |
| Saudável          | 14-17% | 21-24% | Baixo       |
| Aceitável         | 18-21% | 25-31% | Moderado    |
| Obesidade         | >22%   | >32%   | Alto        |

### Biotipos (Heath-Carter)

| Biotipo   | % Gordura típico  | Recomendação               |
| --------- | ----------------- | -------------------------- |
| Endomorfo | H>25% / M>28%     | Déficit calórico + força   |
| Mesomorfo | H10-18% / M18-25% | Treino equilibrado         |
| Ectomorfo | H<10% / M<18%     | Superávit calórico + força |

### Avaliações Complementares

**Handgrip (Força)**

| Classificação | Homem       | Mulher      |
| ------------- | ----------- | ----------- |
| Fraco         | < 35 kg/f   | < 25 kg/f   |
| Regular       | 35-45 kg/f  | 25-35 kg/f  |
| Forte         | > 45 kg/f   | > 35 kg/f   |

**Banco Wells (Flexibilidade)**

| Classificação | Homem   | Mulher  |
| ------------- | ------- | ------- |
| Abaixo        | < 20 cm | < 25 cm |
| Média         | 20-30cm | 25-35cm |
| Acima         | > 30 cm | > 35 cm |

---

## 4. PLANEJAMENTO ALIMENTAR (Seção 26)

> A seção 26 é **independente** da seção 24.1 (Importador de Cardápio).
> Cada uma opera com sua própria lógica de busca.

### Seletor de Fonte (Sidebar)

O usuário escolhe a tabela de referência na barra lateral. A escolha
afeta quais alimentos aparecem no seletor da seção 26.

| Opção | Base | Ideal para |
|---|---|---|
| 🥦 BioGestão 360 | Open Food Facts — 25k+ produtos | Produtos industrializados com marca |
| 🌿 TACO/UNICAMP | 613 alimentos (4ª Ed.) | In natura, preparações caseiras |
| 📊 IBGE/POF | 1.962 alimentos × 16 preparos | Ovos fritos/cozidos/grelhados, pratos típicos |

### Seletor de Marca

Quando há mais de uma marca disponível para o produto selecionado,
o sistema exibe automaticamente um seletor de marca. Se o usuário
não escolher, usa o produto com mais campos nutricionais preenchidos.

### Cálculo de Calorias

`Calorias = (Energia por 100g da base) × (Peso final / 100)`

### Sistema de Unidades Inteligente (IN 75/2020)

| Tipo      | Unidade sugerida | Peso pré-preenchido        |
| --------- | ---------------- | -------------------------- |
| Líquidos  | ml               | 200ml (porção padrão N75)  |
| Unitários | un               | Peso via porcao_num do banco ou dicionário N75 |
| Sólidos   | g                | —                          |

### Hierarquia de Cálculo de Peso (4 níveis)

| Nível | Situação | Ação |
| ----- | -------- | ---- |
| 1 | `peso_real > 0` | Usa o peso informado × quantidade |
| 2 | `un` + porcao_num no banco | Usa porcao_num do produto |
| 3 | `un` + sem porcao_num | Consulta dicionário interno + N75 |
| 4 | `un` + nenhuma referência | Bloqueia e orienta o usuário |

---

## 5. IMPORTADOR AUTOMÁTICO DE CARDÁPIO (Seção 24.1)

> Requer cadastro (2 dias gratuitos ou colaboração voluntária).

### Hierarquia de Busca

```
1. TACO/UNICAMP     → alimentos in natura e preparações caseiras
2. IBGE/POF         → alimentos com forma de preparo (cozido, frito, grelhado...)
3. BioGestão 360    → produtos industrializados e com marca
4. estimativa_inteligente → fallback por categoria alimentar
```

### Fluxo de Processamento

1. Usuário cola o cardápio em texto
2. Sistema extrai alimentos, quantidades, refeições e dias
3. Para cada alimento: percorre a hierarquia TACO → IBGE → BioGestão → estimativa
4. Calcula fator pela quantidade informada (g, ml, un, fatias, etc.)
5. Exibe tabela editável com coluna **Fonte** (TACO / IBGE / BioGestão / estimativa)
6. Alertas OMS/IARC e restrições alimentares aplicados automaticamente

### Coluna Fonte — o que cada valor significa

| Fonte | Significado |
|---|---|
| TACO | Valor da Tabela TACO/UNICAMP (4ª Ed.) — alta confiabilidade científica |
| IBGE | Valor da tabela IBGE/POF 2008-2009 — inclui forma de preparo |
| BioGestão | Valor do produto real no mercado brasileiro (Open Food Facts) |
| estimativa | Valor estimado por categoria — menos preciso, use como referência |

### Normalização de Texto

- Conversão para minúsculas
- Hífen → espaço (`castanhas-do-pará` → `castanhas do para`)
- Remoção de acentos via NFKD
- Vírgulas nos nomes TACO removidas (`Arroz, integral, cozido` → `arroz integral cozido`)

---

## 6. MONTE SEU TREINO (Seção 25.1)

> Seção gratuita. Ferramenta educacional — não substitui prescrição profissional.

### Cálculo de Calorias pelo MET

`kcal = MET × peso(kg) × duração(horas)`

Fonte: Ainsworth BE et al. Compendium of Physical Activities. Med Sci Sports Exerc. 2011.

### Exigências Profissionais (informativas)

| Profissional | Registro | Exigências adicionais |
|---|---|---|
| Educação Física | CREF ativo | SBV (Suporte Básico de Vida) obrigatório |
| Natação / Hidroginástica | CREF ativo | SBV + Curso de Socorrismo Aquático |
| Reabilitação | CREFITO ativo | Conforme especialidade |

**SBV (Suporte Básico de Vida / BLS):** capacita para RCP
(ressuscitação cardiopulmonar) e uso do DEA (desfibrilador).
Exigido pelo CREF para atuação em qualquer área da Educação Física.

---

## 7. ALERTAS OMS — CLASSIFICAÇÃO IARC

| Grupo    | Classificação             | Alimentos no sistema                                              | Recomendação    |
| -------- | ------------------------- | ----------------------------------------------------------------- | --------------- |
| Grupo 1  | Cancerígeno humano        | Salsicha, linguiça, bacon, presunto, salame, mortadela, nuggets   | Evitar          |
| Grupo 2A | Provavelmente cancerígeno | Carne bovina, suína, cordeiro, bife, carne moída                  | Máx 500g/semana |
| Grupo 2B | Possivelmente cancerígeno | Aspartame (diet/zero), acrilamida (biscoito, torrada), beb. >65°C | Moderado        |

Referências: IARC Monographs Vol. 114 (2015) e Vol. 116 (2016).

---

## 8. BASES DE DADOS

| Base | Arquivo | Cobertura | Papel |
| --- | --- | --- | --- |
| BioGestão 360 | `biogestao_foods.csv` | 25k+ produtos reais BR | Fonte principal — industrializados |
| TACO/UNICAMP 4ª Ed. | `alimentos.csv` | 613 alimentos | Prioridade 1 no importador |
| IBGE POF 2008-2009 | `tabela_ibge.csv` | 1.962 × 16 preparos | Prioridade 2 no importador |
| IN 75/2020 | (interno) | Porções Anvisa | Peso por unidade — nível 3 |

### Arquivos gerados (não versionados no Git)

| Arquivo | Gerado por | Conteúdo |
|---|---|---|
| `taco_limpa.csv` | `processar_tabelas.py` | TACO normalizada + aliases de busca |
| `ibge_limpa.csv` | `processar_tabelas.py` | IBGE normalizada com coluna nome_busca |
| `biogestao_foods_corrigido.csv` | `reimportar_supabase.py` | BioGestão com sódio corrigido |

### Atribuições

- **Open Food Facts:** https://br.openfoodfacts.org — ODbL
- **TACO/UNICAMP:** https://www.fao.org/food-composition/tables-and-databases/detail/(brazil--2011)-tabela-brasileira-de-composi%C3%A7%C3%A3o-de-alimentos-(taco)/en
- **IBGE/POF:** https://www.fao.org/food-composition/tables-and-databases/detail/(brazil--2011)-tabelas-de-composi%C3%A7%C3%A3o-nutricional-dos-alimentos-consumidos-no-brasil/en

---

## 9. IN 75/2020 — PORÇÕES DE REFERÊNCIA (buscar_porcao_n75)

| Categoria | Porção | Medida caseira |
| --- | --- | --- |
| Torradas | 30g | Unidades |
| Biscoito salgado / cream cracker | 30g | Unidades |
| Biscoito doce / recheado | 30g | Unidades |
| Pão embalado fatiado | 50g | Unidades ou fatias |
| Leite fluido (qualquer tipo) | 200ml | Copos |
| Iogurte / leite fermentado | 200ml | Copos |
| Queijo cottage / ricota / minas | 50g | Colheres ou fatias |
| Outros queijos | 30g | Colheres ou fatias |
| Ovo | — | Unidades (variável) |
| Hambúrguer | 80g | Unidades |
| Manteiga / margarina | 10g | Colheres de sopa |
| Refrigerante / chá / bebida | 200ml | Xícaras ou copos |
| Açúcar | 5g | Colheres de chá |

---

## 10. REFERÊNCIAS CIENTÍFICAS

| Cálculo | Referência | Ano |
| --- | --- | --- |
| TMB Harris-Benedict | Harris & Benedict | 1919 |
| TMB Katch-McArdle | Katch & McArdle | 1975 |
| % Gordura por IMC | Deurenberg et al. | 1991 |
| Protocolo Dobras | Jackson & Pollock | 1978 |
| % Gordura por Densidade | Siri WE | 1961 |
| GET × NAF | WHO/FAO/UNU | 1985 |
| Porções de referência | IN 75/2020 (Anvisa) | 2020 |
| Classificação de risco | IARC Vol. 114/116 | 2015/2016 |
| MET — Calorias treino | Ainsworth et al. | 2011 |

---

## 11. DEPENDÊNCIAS E BIBLIOTECAS

| Biblioteca | Versão | Finalidade |
| --- | --- | --- |
| streamlit | ≥1.35.0 | Framework web |
| pandas | ≥2.0.0 | Manipulação de dados |
| plotly | ≥5.24.0 | Gráficos interativos |
| matplotlib | ≥3.7.0 | Gráficos estáticos para exportação |
| qrcode[pil] | ≥7.0.0 | QR Code PIX |
| pillow | ≥10.0.0 | Manipulação de imagens |
| openpyxl | ≥3.1.0 | Leitura de Excel |
| numpy | ≥1.24.0 | Operações matemáticas |
| psycopg2-binary | ≥2.9.0 | Conexão PostgreSQL/Supabase |
| pyotp | ≥2.9.0 | Autenticação 2FA Admin |

---

**Documento atualizado em:** Maio/2026
**Versão:** 4.2 — Hierarquia TACO → IBGE → BioGestão 360 | Seção 25.1 Monte Seu Treino
