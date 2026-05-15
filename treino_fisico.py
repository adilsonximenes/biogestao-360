# -*- coding: utf-8 -*-
"""
treino_fisico.py — BioGestão 360
=================================
Seção 25.1 — Monte Seu Treino (Educação Física)

Chamada no app.py:
    from treino_fisico import tela_treino_fisico
    tela_treino_fisico(peso_kg=peso_at, dados_paciente=st.session_state.get("dados_paciente", {}))
"""

import streamlit as st
from datetime import datetime
import base64
import unicodedata
import re

# ══════════════════════════════════════════════════════════════════════════════
# TABELA MET — Metabolic Equivalent of Task
# Fonte: Compendium of Physical Activities (Ainsworth et al., 2011)
# ══════════════════════════════════════════════════════════════════════════════
TABELA_MET = {
    "🏋️ Academia / Musculação": {
        "Musculação leve (iniciante, máquinas)":          3.0,
        "Musculação moderada (pesos livres)":             5.0,
        "Musculação intensa (alta carga)":                6.0,
        "Funcional / CircuitTraining":                    8.0,
        "CrossFit (WOD moderado)":                        9.0,
        "Aula coletiva — Spinning / Bike indoor":         7.0,
        "Aula coletiva — Step":                           6.5,
        "Aula coletiva — Body Combat / Body Pump":        7.5,
        "Calistenia (peso corporal)":                     5.0,
        "Treinamento em suspensão (TRX)":                 5.5,
    },
    "🏃 Cardiovascular": {
        "Caminhada leve (4 km/h)":                        2.8,
        "Caminhada moderada (5 km/h)":                    3.8,
        "Caminhada rápida (6 km/h)":                      5.0,
        "Corrida leve (8 km/h)":                          8.0,
        "Corrida moderada (10 km/h)":                    10.0,
        "Corrida intensa (12 km/h)":                     11.5,
        "Corrida muito intensa (> 14 km/h)":             13.5,
        "Ciclismo lazer (< 16 km/h)":                     4.0,
        "Ciclismo moderado (16–22 km/h)":                 8.0,
        "Ciclismo intenso / Estrada (> 22 km/h)":        12.0,
        "Mountain Bike (trilha)":                        10.0,
        "Triathlon — treino combinado (natação+bike+corrida)": 9.5,
        "Triathlon — prova / simulado":                  12.0,
        "Remo ergômetro (moderado)":                      7.0,
        "Elíptico (moderado)":                            5.0,
    },
    "🏊 Aquáticas": {
        "Natação — Crawl (moderado)":                     5.8,
        "Natação — Crawl (intenso)":                      9.8,
        "Natação — Costas (moderado)":                    4.8,
        "Natação — Costas (intenso)":                     8.0,
        "Natação — Peito (moderado)":                     5.3,
        "Natação — Peito (intenso)":                     10.3,
        "Natação — Borboleta (intenso)":                 13.8,
        "Natação — Medley (todos os nados alternados)":  10.0,
        "Hidroginástica (moderada)":                      4.0,
        "Hidroginástica intensa":                         6.0,
        "Polo aquático":                                  8.0,
    },
    "💃 Dança": {
        "Zumba / Dança aeróbica":                         5.5,
        "Ballet / Dança clássica":                        4.8,
        "Forró / Samba / Pagode":                         4.5,
        "Dança urbana / Street dance":                    6.0,
        "Dança de salão":                                 3.5,
    },
    "🧘 Mente e Corpo": {
        "Yoga (Hatha / básico)":                          2.5,
        "Yoga (Vinyasa / dinâmico)":                      4.0,
        "Pilates (solo)":                                 3.0,
        "Pilates (aparelhos)":                            3.5,
        "Alongamento / Mobilidade":                       2.3,
        "Tai Chi / Chi Kung":                             2.5,
        "Meditação em movimento":                         2.0,
    },
    "♿ Adaptado (PCD / Restrições)": {
        "Musculação MMSS — cadeirante":                   3.5,
        "Basquete em cadeira de rodas":                   6.5,
        "Natação adaptada":                               4.5,
        "Handbike (ciclismo com braços)":                 5.0,
        "Fisioterapia ativa":                             2.5,
        "Caminhada assistida / pós-cirúrgico":            2.0,
        "Yoga adaptado":                                  2.0,
    },
    "🥋 Lutas": {
        "Judô (treino técnico)":                          7.0,
        "Judô (randori / luta)":                         10.0,
        "Jiu-Jitsu (técnica)":                            5.5,
        "Jiu-Jitsu (rolagem / luta)":                     9.0,
        "Boxe (sombra, corda, técnica)":                  6.0,
        "Boxe (saco pesado, luta)":                       9.5,
        "Muay Thai / Kickboxing (técnica)":               8.0,
        "Muay Thai / Kickboxing (luta)":                 11.0,
        "Taekwondo (poomsae/técnica)":                    5.0,
        "Taekwondo (kyorugi/luta)":                       9.0,
        "Lutas em geral (treino moderado)":               7.0,
        "Lutas em geral (treino intenso)":               10.0,
    },
    "💪 Esportes de Força": {
        "Powerlifting - treino técnico (leve)":           5.0,
        "Powerlifting - treino moderado":                 6.0,
        "Powerlifting - treino intenso / competição":     7.0,
        "Strongman - treino geral":                       8.0,
        "Strongman - treino competitivo (eventos)":      10.0,
        "Halterofilismo Olímpico - técnica":              5.5,
        "Halterofilismo Olímpico - treino intenso":       8.5,
        "CrossFit - WOD competitivo / Games":            12.0,
        "Kettlebell Lifting (snatch / clean & press)":    8.5,
        "Calistenia Avançada (planche, front lever)":     6.0,
        "Cabo de Guerra (Tug of War)":                    6.5,
        "Atletismo de Força (arremesso, lançamento)":     5.5,
        "Arm Wrestling (braço de ferro)":                 5.0,
    },
    "⚽ Esportes Olímpicos": {
        "Basquetebol (jogo recreativo)":                  6.5,
        "Basquetebol (jogo competitivo)":                 8.0,
        "Voleibol (jogo recreativo)":                     4.0,
        "Voleibol (jogo competitivo)":                    6.0,
        "Futsal / Futebol Society":                       8.0,
        "Futebol de Campo (recreativo)":                  7.0,
        "Futebol de Campo (competitivo)":                 9.5,
        "Handebol":                                       8.0,
        "Tênis (simples)":                                6.5,
        "Tênis (duplas)":                                 5.0,
        "Ginástica Artística (treino geral)":             5.0,
        "Hipismo (trote/galope)":                         4.5,
        "Hipismo (saltos)":                               6.0,
        "Rugby":                                          8.5,
        "Beach Tennis":                                   5.5,
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# REFERÊNCIAS DAS MODALIDADES
# ══════════════════════════════════════════════════════════════════════════════
REFERENCIAS_MODALIDADE = {
    "🏋️ Academia / Musculação": (
        "Treinamento com pesos (resistência) usando máquinas, halteres ou barras. "
        "Desenvolve força, hipertrofia e resistência muscular. Adequado para todos os níveis "
        "com orientação profissional habilitada (CREF)."
    ),
    "🏃 Cardiovascular": (
        "Atividades que elevam a frequência cardíaca de forma sustentada: corrida, caminhada, "
        "ciclismo e triathlon. O triathlon combina natação, ciclismo e corrida em sequência — "
        "exige preparo específico e acompanhamento profissional. MET calculado pelo treino combinado."
    ),
    "🏊 Aquáticas": (
        "Natação e hidroginástica. Os quatro nados são: Crawl (mais rápido), Costas, Peito e Borboleta (mais exigente). "
        "O Medley alterna todos os quatro nados numa mesma série. Hidroginástica é indicada para "
        "gestantes, idosos, condromalacia e pós-operatório."
    ),
    "💃 Dança": (
        "Modalidades que combinam atividade física com expressão artística e social. "
        "Excelente para coordenação motora, bem-estar e convívio social. Baixo risco de lesão "
        "quando praticadas com orientação."
    ),
    "🧘 Mente e Corpo": (
        "Práticas que integram movimento, respiração e atenção. Yoga, Pilates e Tai Chi "
        "melhoram flexibilidade, equilíbrio, postura e qualidade de vida. Indicadas para "
        "diversas condições de saúde especiais."
    ),
    "♿ Adaptado (PCD / Restrições)": (
        "Modalidades adaptadas para pessoas com deficiência física, mobilidade reduzida ou "
        "restrições médicas. Sempre requer avaliação individualizada por profissional habilitado "
        "e, quando necessário, laudo médico."
    ),
    "🥋 Lutas": (
        "Modalidades de luta e artes marciais que combinam técnica, força e condicionamento. "
        "Ótimo para coordenação motora, autoconfiança e condicionamento cardiovascular. "
        "Exige supervisão adequada para evitar lesões."
    ),
    "💪 Esportes de Força": (
        "Categoria que engloba Powerlifting (agachamento, supino e terra), Strongman (Farmer's Walk, Log Press, Sled Push/Pull, virada de pneus, battle ropes, levantamento de pedras), Halterofilismo Olímpico (arranco e arremesso), CrossFit competitivo, Kettlebell e calistenia avançada. Podem ser adaptados com halteres, kettlebells e sacos de areia."
    ),
    "⚽ Esportes Olímpicos": (
        "Esportes coletivos e individuais de alto rendimento ou lazer. Desenvolvem coordenação, "
        "agilidade, resistência e trabalho em equipe. Necessitam de profissional habilitado e "
        "avaliação médica prévia."
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# CONDIÇÕES DE SAÚDE
# ══════════════════════════════════════════════════════════════════════════════
CONDICOES_SAUDE = [
    "Nenhuma",
    "Condromalacia patelar",
    "Endometriose",
    "Gestante",
    "Pós-operatório (< 6 meses)",
    "Deficiência física / PCD",
    "Cardiopatia",
    "Osteoporose",
    "Artrite / Artrose",
    "Diabetes tipo 2",
    "Lombalgia crônica",
    "Hipertensão arterial",
    "Obesidade grau III",
    "Outro",
]

RESTRICOES = {
    "Condromalacia patelar": (
        ["Natação", "Ciclismo", "Hidroginástica", "Musculação MMSS"],
        ["Corrida", "Agachamento profundo", "Saltos", "Step", "Leg press carga alta"],
        "⚠️ Evitar impacto e flexão profunda do joelho. Fortalecer VMO (vasto medial oblíquo) sem carga axial."
    ),
    "Endometriose": (
        ["Yoga", "Pilates", "Caminhada", "Natação", "Hidroginástica"],
        ["Alta intensidade no período menstrual", "Abdominais hipopressivos"],
        "⚠️ Preferir baixo impacto. Intensidade moderada fora do período. Respeitar os sinais do corpo."
    ),
    "Gestante": (
        ["Hidroginástica", "Yoga pré-natal", "Caminhada leve", "Pilates pré-natal"],
        ["Impacto", "Abdominal", "Decúbito dorsal após 1º trimestre", "Levantamento pesado", "Esportes de contato"],
        "🚨 OBRIGATÓRIO: acompanhamento médico e liberação obstétrica por escrito a cada trimestre."
    ),
    "Pós-operatório (< 6 meses)": (
        ["Fisioterapia ativa", "Caminhada assistida", "Alongamento suave"],
        ["Treino de força sem liberação", "Impacto", "Esforço intenso"],
        "🚨 Necessita laudo médico por escrito. Progressão individualizada com fisioterapeuta."
    ),
    "Deficiência física / PCD": (
        ["Musculação MMSS adaptada", "Basquete em cadeira de rodas", "Natação adaptada", "Handbike"],
        [],
        "ℹ️ Avaliação individualizada obrigatória. Adaptar exercícios ao tipo e grau de deficiência."
    ),
    "Cardiopatia": (
        ["Caminhada leve (com monitoramento FC)", "Yoga", "Alongamento"],
        ["Qualquer treino sem ECG de esforço e laudo cardiológico", "Alta intensidade", "Isometria prolongada"],
        "🚨 OBRIGATÓRIO: laudo cardiológico, teste ergométrico e monitoramento da FC durante o treino."
    ),
    "Osteoporose": (
        ["Musculação leve", "Caminhada", "Yoga", "Tai Chi"],
        ["Impacto intenso", "Flexão vertebral forçada", "Saltos", "Risco de queda"],
        "⚠️ Exercícios de resistência fortalecem ossos. Priorizar prevenção de quedas e equilíbrio."
    ),
    "Artrite / Artrose": (
        ["Hidroginástica", "Natação", "Ciclismo", "Yoga", "Pilates"],
        ["Impacto nas articulações acometidas", "Carga excessiva"],
        "⚠️ Movimentos suaves, amplitude progressiva. Evitar impacto nas articulações afetadas."
    ),
    "Diabetes tipo 2": (
        ["Caminhada", "Musculação moderada", "Ciclismo", "Natação"],
        [],
        "ℹ️ Monitorar glicemia antes, durante e após o treino. Carregar fonte de açúcar de rápida absorção."
    ),
    "Lombalgia crônica": (
        ["Natação", "Hidroginástica", "Pilates", "Yoga"],
        ["Levantamento terra com carga alta", "Agachamento com barra", "Abdominais tradicionais (flexão de tronco)"],
        "⚠️ Core estabilizador é prioridade. Evitar carga axial excessiva na coluna lombar."
    ),
    "Hipertensão arterial": (
        ["Caminhada", "Natação", "Ciclismo moderado", "Yoga"],
        ["Isometria prolongada", "Manobra de Valsalva", "Alta intensidade sem monitoramento de PA"],
        "ℹ️ PA deve estar controlada. Aeróbico moderado é o mais indicado. Monitorar PA antes do treino."
    ),
    "Obesidade grau III": (
        ["Hidroginástica", "Natação", "Ciclismo", "Caminhada em piscina", "Musculação leve"],
        ["Corrida de impacto", "Saltos", "Alta intensidade sem avaliação prévia"],
        "⚠️ Iniciar com baixo impacto para proteger articulações. Progressão gradual e supervisionada."
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# RESTRIÇÕES PARA LESÕES (NOVO)
# ══════════════════════════════════════════════════════════════════════════════
RESTRICOES_LESOES = {
    "Lesão de LCA (Ligamento Cruzado Anterior)": (
        ["Cadeira extensora (ângulo 90°-45°)", "Cadeira flexora", "Ciclismo (selim alto)", "Natação (crawl com prancha)", "Prancha", "Hidroginástica"],
        ["Agachamento profundo", "Leg press com carga alta", "Saltos", "Corrida em subida", "Avanço (lunge) com rotação", "Movimentos de torção"],
        "⚠️ Reconstrução do LCA requer protocolo específico de reabilitação. Fortalecimento de isquiotibiais é crucial. Evitar estresse de rotação e impacto."
    ),
    "Lesão de LCP (Ligamento Cruzado Posterior)": (
        ["Cadeira extensora (sem carga)", "Ciclismo", "Natação", "Prancha"],
        ["Agachamento profundo", "Leg press com amplitude máxima", "Cadeira flexora com sobrecarga", "Saltos"],
        "⚠️ Evitar movimentos que forcem a tíbia para trás. Priorizar cadeia cinética aberta com orientação."
    ),
    "Lesão de Menisco": (
        ["Cadeira extensora (sem carga no pico)", "Ciclismo (selim alto)", "Natação (avaliar nado peito)", "Hidroginástica"],
        ["Agachamento profundo", "Leg press com amplitude máxima", "Corrida em terreno irregular", "Movimentos de torção", "Avanço"],
        "⚠️ Priorizar exercícios em cadeia cinética fechada com controle. Evitar rotação e estresse compressivo."
    ),
    "Lesão do Manguito Rotador": (
        ["Elevação lateral (até 90°, sem carga)", "Rotação externa com elástico", "Remada baixa (cotovelo junto)", "Puxada frontal (pegada aberta)"],
        ["Supino reto com barra", "Desenvolvimento por trás da cabeça", "Crucifixo", "Paralela", "Remada alta"],
        "⚠️ Fortalecer o manguito rotador e escapuloumerais. Evitar movimentos acima de 90° com carga."
    ),
    "Síndrome do Impacto do Ombro": (
        ["Rotação externa com elástico", "Remada baixa", "Puxada frontal", "Alongamento de peitoral"],
        ["Supino reto", "Desenvolvimento", "Elevação lateral acima de 90°", "Paralela", "Remada alta"],
        "⚠️ Evitar movimentos que comprimem o subacromial. Trabalhar estabilização escapular."
    ),
    "Tendinite Patelar (Joelho de Saltador)": (
        ["Cadeira extensora (ângulo 90°-45°)", "Ciclismo (selim alto)", "Natação", "Hidroginástica"],
        ["Saltos", "Agachamento profundo", "Leg press com amplitude total", "Corrida em declive"],
        "⚠️ Fortalecer VMO e cadeia posterior. Evitar impacto direto e sobrecarga do tendão patelar."
    ),
    "Bursite Trocanteriana": (
        ["Ciclismo (selim baixo)", "Hidroginástica", "Alongamento de ITB", "Fortalecimento de glúteo médio"],
        ["Avanço (lunge)", "Agachamento profundo", "Corrida em superfície inclinada", "Exercícios de abdução com carga"],
        "⚠️ Evitar atrito no trocanter. Fortalecer glúteo médio e alongar ITB e piriforme."
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# BANCO DE EXERCÍCIOS PARA MONTAGEM LIVRE
# ══════════════════════════════════════════════════════════════════════════════
BANCO_EXERCICIOS = {
    "Peito": [
        "Supino reto (barra)", "Supino inclinado (barra)", "Supino declinado (barra)",
        "Supino reto (halteres)", "Supino inclinado (halteres)", "Supino declinado (halteres)",
        "Crucifixo reto (halteres)", "Crucifixo inclinado (halteres)",
        "Crucifixo (crossover / cabos)", "Peck deck / Voador",
        "Flexão de braço (push-up)", "Flexão inclinada", "Flexão declinada",
        "Flexão diamante", "Dips em paralela (peito)",
    ],
    "Costas": [
        "Puxada frontal (barra larga)", "Puxada frontal (barra fechada)",
        "Puxada ao peito (barra neutra)", "Puxada por trás (barra larga)",
        "Remada curvada (barra)", "Remada curvada (halteres)",
        "Remada unilateral (halter)", "Remada cavalinho (máquina)",
        "Remada baixa (cabos)", "Remada alta (cabos)",
        "Pullover (halter)", "Pullover (cabo)", "Barra fixa (pull-up)",
        "Chin-up (pegada supinada)", "Superman (extensão lombar no chão)",
        "Mesa romana (extensão lombar)", "Stiff (posterior de coxa e lombar)",
    ],
    "Ombros": [
        "Desenvolvimento (barra) — em pé", "Desenvolvimento (barra) — sentado",
        "Desenvolvimento (halteres) — sentado", "Desenvolvimento militar (barra)",
        "Elevação lateral (halteres)", "Elevação lateral (cabos)",
        "Elevação frontal (halteres)", "Elevação frontal (barra)",
        "Encolhimento de ombros — trapézio (barra)", "Encolhimento (halteres)",
        "Remada alta (barra)", "Remada alta (cabos)",
        "Rotação externa (cabo)", "Rotação interna (cabo)",
        "Face pull (cabo com corda)",
    ],
    "Bíceps": [
        "Rosca direta (barra W)", "Rosca direta (barra reta)",
        "Rosca direta (halteres) — alternada", "Rosca direta (halteres) — simultânea",
        "Rosca concentrada (halter)", "Rosca martelo (halteres)",
        "Rosca inclinada (halteres)", "Rosca Scott (máquina / barra)",
        "Rosca cabo baixo", "Rosca 21 (parcial inferior + superior + completa)",
    ],
    "Tríceps": [
        "Tríceps pulley (corda)", "Tríceps pulley (barra V)",
        "Tríceps testa (barra W)", "Tríceps testa (halteres)",
        "Tríceps francês (barra)", "Tríceps francês (halter)",
        "Tríceps coice (halter)", "Dips em paralela (tríceps)",
        "Tríceps banco (bench dip)", "Tríceps cabo (unilateral)",
        "Push-down (cabo reto)", "Extensão testa (cabo)",
    ],
    "Quadríceps": [
        "Agachamento livre (barra)", "Agachamento frontal (barra)",
        "Agachamento Smith (máquina)", "Agachamento goblet (halter/kettle)",
        "Leg press 45°", "Leg press horizontal",
        "Cadeira extensora (máquina)", "Avanço (lunge) com barra",
        "Avanço (lunge) com halteres", "Avanço búlgaro (split squat)",
        "Hack squat (máquina)", "Passada lateral",
        "Step-up (caixote)", "Pistol squat (agachamento unilateral)",
    ],
    "Posterior de Coxa / Glúteos": [
        "Stiff (barra)", "Stiff (halteres)", "Stiff unilateral",
        "Levantamento terra (barra)", "Levantamento terra sumô",
        "Cadeira flexora (máquina)", "Mesa flexora (máquina)",
        "Curl deitado (halter unilateral)", "Hip thrust (barra / halter)",
        "Ponte glúteo (no chão)", "Agachamento sumô (halter)",
        "Abdução de quadril (cabo / máquina)", "Coice de glúteo (cabo)",
        "Good morning (barra)", "Romanian Deadlift (RDL)",
    ],
    "Panturrilha": [
        "Panturrilha em pé (máquina Smith)", "Panturrilha sentado (máquina)",
        "Panturrilha no leg press", "Panturrilha com halter (unilateral)",
        "Panturrilha no degrau (peso corporal)", "Panturrilha em pé (halteres)",
    ],
    "Core / Abdome": [
        "Prancha frontal (plank)", "Prancha lateral",
        "Abdominal crunch (chão)", "Abdominal remador (bicicleta)",
        "Abdominal supra (chão)", "Elevação de pernas (suspenso / chão)",
        "Rollout (roda abdominal)", "Ab crunch (máquina)",
        "Russian twist (halter / disco)", "Dead bug",
        "Hollow hold", "V-up", "Pallof press (cabo)",
        "Hiperextensão lombar (banco)", "Prancha com alcance",
    ],
    "Antebraço / Punho": [
        "Rosca punho pronada (barra)", "Rosca punho supinada (barra)",
        "Rosca punho (halteres)", "Farmer's carry (carga pesada andando)",
        "Plate pinch (pinçar disco)", "Squeeze de esponja / ball",
    ],
}

METODOS_TREINO = {
    "Séries convencionais": {
        "descricao": "Número fixo de séries e repetições. Ex: 3×12 (3 séries de 12 repetições).",
        "tipo": "fixo",
        "exemplo_series": 3,
        "exemplo_reps": "12",
        "permite_carga_progressiva": False
    },
    "Pirâmide crescente": {
        "descricao": "Aumenta a carga a cada série e diminui as repetições. Ex: 12→10→8 com carga 40→50→60kg.",
        "tipo": "progressivo",
        "series_padrao": 3,
        "reps_por_serie": ["12", "10", "8"],
        "carga_por_serie": ["40kg", "50kg", "60kg"],
        "permite_carga_progressiva": True
    },
    "Pirâmide decrescente": {
        "descricao": "Diminui a carga a cada série e aumenta as repetições. Ex: 8→10→12 com carga 60→50→40kg.",
        "tipo": "progressivo",
        "series_padrao": 3,
        "reps_por_serie": ["8", "10", "12"],
        "carga_por_serie": ["60kg", "50kg", "40kg"],
        "permite_carga_progressiva": True
    },
    "Drop set": {
        "descricao": "Ao falhar, reduz a carga imediatamente e continua sem descanso. Máxima intensidade.",
        "tipo": "drop",
        "series_padrao": 1,
        "drops_por_serie": 3,
        "reps_iniciais": "até a falha",
        "reducao_carga": "20-30% a cada drop",
        "permite_carga_progressiva": True
    },
    "Super set": {
        "descricao": "Dois exercícios em sequência sem descanso — mesmo grupo muscular (intensidade) ou antagonistas (volume).",
        "tipo": "superset",
        "series_padrao": 3,
        "reps_por_exercicio": "10-12",
        "descanso_entre_supersets": "60-90s",
        "permite_carga_progressiva": False
    },
    "Tri set": {
        "descricao": "Três exercícios em sequência sem descanso para o mesmo grupo muscular.",
        "tipo": "triset",
        "series_padrao": 3,
        "reps_por_exercicio": "10-12",
        "descanso_entre_trisets": "90-120s",
        "permite_carga_progressiva": False
    },
    "Giant set": {
        "descricao": "Quatro ou mais exercícios em sequência sem descanso.",
        "tipo": "giantset",
        "series_padrao": 3,
        "reps_por_exercicio": "8-12",
        "descanso_entre_giantsets": "90-120s",
        "permite_carga_progressiva": False
    },
    "Rest-pause": {
        "descricao": "Uma série até a falha, 10–20s de descanso, continua com mais repetições.",
        "tipo": "restpause",
        "series_padrao": 1,
        "pausas_por_serie": 2,
        "reps_primeiro_set": "até a falha",
        "reps_pos_pausa": "2-5",
        "permite_carga_progressiva": True
    },
    "Negativa acentuada": {
        "descricao": "Fase excêntrica lenta (4–6 segundos). Maior dano muscular e ganho de força.",
        "tipo": "negativa",
        "series_padrao": 3,
        "reps_padrao": "6-8",
        "tempo_excentrico": "4-6 segundos",
        "permite_carga_progressiva": True
    },
    "Isometria": {
        "descricao": "Contração sem movimento. Ex: segurar 3 segundos no ponto de maior tensão.",
        "tipo": "isometrico",
        "series_padrao": 3,
        "tempo_segundos": "15-30s",
        "permite_carga_progressiva": False
    },
    "Pré-exaustão": {
        "descricao": "Isolar o músculo principal antes do exercício composto. Ex: crucifixo antes do supino.",
        "tipo": "pre_exaustao",
        "series_padrao": 3,
        "reps_isolador": "12-15",
        "reps_composto": "8-10",
        "permite_carga_progressiva": False
    },
    "Cluster set": {
        "descricao": "Série com micro-pausas de 10–15s entre grupos de repetições para manter a qualidade.",
        "tipo": "cluster",
        "series_padrao": 3,
        "clusters_por_serie": 3,
        "reps_por_cluster": "2-4",
        "pausa_entre_clusters": "10-15s",
        "permite_carga_progressiva": True
    },
    "AMRAP": {
        "descricao": "As Many Reps As Possible — máximo de repetições com boa forma em um tempo definido.",
        "tipo": "amrap",
        "tempo_minutos": 10,
        "permite_carga_progressiva": False
    },
    "EMOM": {
        "descricao": "Every Minute On the Minute — executa X repetições no início de cada minuto.",
        "tipo": "emom",
        "duracao_minutos": 10,
        "reps_por_minuto": "5-10",
        "permite_carga_progressiva": False
    },
    "Circuito": {
        "descricao": "Série de exercícios realizados em sequência com descanso apenas ao final da rodada.",
        "tipo": "circuito",
        "series_padrao": 3,
        "exercicios_por_circuito": "6-8",
        "reps_por_exercicio": "10-15",
        "descanso_entre_rodadas": "60-90s",
        "permite_carga_progressiva": False
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# SUGESTÕES AUTOMÁTICAS (REFATORADO COM MAIS OPÇÕES)
# ══════════════════════════════════════════════════════════════════════════════
SUGESTOES_TREINO = {
    # Academia / Musculação
    ("🏋️ Academia / Musculação", "Iniciante", "3x"): {
        "nome": "Full Body A/B — Iniciante 3x",
        "descricao": "Alternância entre Treino A e B em dias não consecutivos. 3 séries × 12 repetições. Intervalo de 60–90s entre séries.",
        "dias": {
            "Treino A (Seg / Qua / Sex)": [
                "Agachamento livre — 3×12",
                "Supino reto (halteres) — 3×12",
                "Remada curvada (barra) — 3×12",
                "Desenvolvimento (halteres) — 3×12",
                "Rosca direta (barra) — 3×12",
                "Tríceps pulley (corda) — 3×12",
                "Prancha frontal — 3×30s",
            ],
            "Treino B (Ter / Qui / Sáb)": [
                "Leg press 45° — 3×12",
                "Crucifixo (halteres) — 3×12",
                "Puxada frontal — 3×12",
                "Elevação lateral — 3×15",
                "Rosca martelo — 3×12",
                "Tríceps testa (barra W) — 3×12",
                "Abdominal crunch — 3×20",
            ],
        }
    },
    ("🏋️ Academia / Musculação", "Intermediário", "4-5x"): {
        "nome": "Upper / Lower — Intermediário (Força + Hipertrofia)",
        "descricao": "Periodização ondulada: dias de força (baixas reps, alta carga) e hipertrofia. 4–5 séries. Intervalo 90–120s (força) / 60–90s (hipertrofia).",
        "dias": {
            "Upper Força (Seg)": [
                "Supino reto — 5×5 (carga alta)",
                "Remada curvada — 5×5",
                "Desenvolvimento militar — 4×6",
                "Rosca direta — 3×8",
                "Tríceps francês — 3×8",
            ],
            "Lower Força (Ter)": [
                "Agachamento livre — 5×5 (carga alta)",
                "Levantamento terra — 4×4",
                "Avanço búlgaro — 3×8 cada",
                "Panturrilha em pé — 4×12",
            ],
            "Upper Hipertrofia (Qui)": [
                "Supino inclinado (halteres) — 4×12",
                "Puxada (barra neutra) — 4×10",
                "Face pull — 4×15",
                "Rosca 21 — 3×21",
                "Tríceps corda (drop set) — 3×12+falha",
            ],
            "Lower Hipertrofia (Sex)": [
                "Leg press — 4×15",
                "Cadeira extensora — 4×15",
                "Cadeira flexora — 4×15",
                "Hip thrust — 4×12",
                "Panturrilha sentado — 5×20",
            ],
        }
    },
    ("🏋️ Academia / Musculação", "Avançado", "6-7x"): {
        "nome": "PPL — Push / Pull / Legs (Avançado 6x)",
        "descricao": "Push/Pull/Legs duas vezes por semana. Alta intensidade, técnicas avançadas (drop set, super set, rest-pause). 4–5 séries. Intervalo 90–120s.",
        "dias": {
            "Push A — Peito / Ombro / Tríceps (Seg)": [
                "Supino reto — 4×6 (força)",
                "Supino inclinado (halteres) — 4×10",
                "Crucifixo (crossover) — 3×12",
                "Desenvolvimento militar — 4×8",
                "Elevação lateral (super set c/ frontal) — 4×15+15",
                "Tríceps corda — 3×12 + drop set",
                "Tríceps francês — 3×10",
            ],
            "Pull A — Costas / Bíceps (Ter)": [
                "Levantamento terra — 4×4 (força)",
                "Barra fixa (pull-up) — 4×máx",
                "Remada curvada (barra) — 4×8",
                "Puxada (barra neutra) — 4×10",
                "Remada baixa (cabos) — 3×12",
                "Rosca direta (barra) — 4×10",
                "Rosca concentrada — 3×12",
            ],
            "Legs A — Quadríceps (Qua)": [
                "Agachamento livre — 5×5 (força)",
                "Leg press 45° — 4×12",
                "Hack squat — 3×12",
                "Cadeira extensora — 4×15 + drop set",
                "Avanço búlgaro — 3×10 cada",
                "Panturrilha em pé — 5×15",
            ],
            "Push B (Qui)": [
                "Supino inclinado (barra) — 4×8",
                "Peck deck — 4×12",
                "Dips (peito) — 4×máx",
                "Desenvolvimento (halteres) — 4×10",
                "Elevação lateral (rest-pause) — 3×15",
                "Tríceps testa — 4×10",
            ],
            "Pull B (Sex)": [
                "Remada cavalinho — 4×10",
                "Pullover (halter) — 4×12",
                "Chin-up (pegada supinada) — 4×máx",
                "Remada unilateral — 4×10",
                "Rosca martelo (super set c/ concentrada) — 3×12+10",
                "Rosca 21 — 3×21",
            ],
            "Legs B — Posterior / Glúteos (Sáb)": [
                "Romanian Deadlift (RDL) — 4×8",
                "Stiff (halteres) — 4×10",
                "Hip thrust (barra) — 4×10",
                "Cadeira flexora — 4×15 + drop set",
                "Agachamento sumô — 3×12",
                "Panturrilha sentado — 5×20",
            ],
        }
    },
    
    # Cardiovascular
    ("🏃 Cardiovascular", "Iniciante", "3x"): {
        "nome": "Corrida Iniciante — Método Jeff Galloway (Run/Walk)",
        "descricao": "Progressão segura em 8 semanas. Intercala corrida e caminhada para evitar lesões e construir base aeróbica.",
        "dias": {
            "Semana 1–2": ["Caminhar 5 min → Correr 1 min + Caminhar 2 min (repetir 6x) → Caminhar 5 min"],
            "Semana 3–4": ["Caminhar 5 min → Correr 2 min + Caminhar 2 min (repetir 6x) → Caminhar 5 min"],
            "Semana 5–6": ["Caminhar 5 min → Correr 5 min + Caminhar 2 min (repetir 4x) → Caminhar 5 min"],
            "Semana 7–8": ["Caminhar 5 min → Correr 10 min + Caminhar 2 min (repetir 2x) → Caminhar 5 min"],
        }
    },
    ("🏃 Cardiovascular", "Intermediário", "4-5x"): {
        "nome": "Corrida Intermediário — Volume Base 4x",
        "descricao": "4 sessões com treino longo, intervalado, regenerativo e fartlek.",
        "dias": {
            "Treino Longo (Dom)": ["Corrida contínua 50-60 min em ritmo leve"],
            "Intervalado (Ter)":  ["6 × 400m em ritmo forte | descanso 60s"],
            "Regenerativo (Qui)": ["Corrida leve 25-30 min | pace bem confortável"],
            "Fartlek (Sáb)":     ["35 min: alterna 3 min forte + 2 min leve"],
        }
    },
    ("🏃 Cardiovascular", "Avançado", "4-5x"): {
        "nome": "Corrida Avançado — Treino Periodizado",
        "descricao": "Periodização com treino de limiar, VO2max e longo. Para corredores experientes.",
        "dias": {
            "Longo (Dom)":        ["70-90 min em pace fácil (Z2) — base aeróbica"],
            "Limiar (Ter)":       ["3 × 15 min no limiar anaeróbico | 3 min descanso"],
            "VO2max (Qui)":       ["5 × 1000m em pace 5km | descanso 2 min"],
            "Recuperação (Sáb)": ["30 min leve + 6 × 100m aceleração"],
        }
    },
    
    # Triatlo - Específico
    ("🏃 Cardiovascular", "Triathlon — treino combinado (natação+bike+corrida)", "Avançado", "4-5x"): {
        "nome": "Triatlo Avançado — Preparação Olímpico",
        "descricao": "Treino específico para triatlo com natação, ciclismo e corrida. Inclui tiros, rodagem e transições.",
        "dias": {
            "Segunda — Natação + Corrida": [
                "Natação: 300m aquecimento → 6×100m crawl (descanso 30s) → 200m recupero",
                "Corrida: 5km em ritmo de prova (transição)"
            ],
            "Terça — Musculação Funcional": [
                "Peso morto (RDL) — 4×8",
                "Agachamento frontal — 4×6",
                "Remada curvada — 4×10",
                "Prancha — 4×45s",
                "Exercícios de mobilidade para triatlo"
            ],
            "Quarta — Bike Longa": [
                "Aquecimento 15 min → 90 min de pedal em zona 2 (60-70% FCM) → 15 min desaquecimento"
            ],
            "Quinta — Natação + Transição": [
                "Natação contínua: 2000m crawl em ritmo moderado",
                "Transição para corrida: 20 min trote leve"
            ],
            "Sexta — Corrida com Tiros": [
                "Aquecimento 15 min → 8×400m em ritmo 5km (descanso 60s) → 15 min desaquecimento"
            ],
            "Sábado — Bike + Corrida (Brick)": [
                "Bike: 60 min em zona 3 → Transição direta → Corrida: 30 min em ritmo de prova"
            ],
            "Domingo — Descanso Ativo": ["Alongamento, Yoga ou 30 min caminhada leve"]
        }
    },
    
    # Lutas - Jiu-Jitsu
    ("🥋 Lutas", "Jiu-Jitsu (rolagem / luta)", "Intermediário", "4-5x"): {
        "nome": "Jiu-Jitsu Intermediário — Performance",
        "descricao": "Treino específico para Jiu-Jitsu com ênfase em condicionamento, força de pegada e explosão.",
        "dias": {
            "Segunda — Técnica + Rolagem": ["Aquecimento específico BJJ → Técnica (40 min) → Rolagem (30 min) → Alongamento"],
            "Terça — Força e Condicionamento": [
                "Puxada frontal (pegada supinada) — 4×8",
                "Remada cavalinho — 4×10",
                "Rosca direta (pegada grossa) — 4×12",
                "Prancha com peso — 4×45s",
                "Farmer's walk — 4×20m"
            ],
            "Quarta — Técnica + Rolagem": ["Aquecimento → Posicionamento/Passagem (40 min) → Rolagem específica (30 min)"],
            "Quinta — Condicionamento Metabólico": [
                "Circuito HIIT: 8 exercícios (burpees, kettlebell swing, corda naval)",
                "30s trabalho / 15s descanso — 6 rodadas"
            ],
            "Sexta — Técnica + Resistência": ["Aquecimento → Técnica avançada (50 min) → Rolagem longa (40 min)"],
            "Sábado — Recuperação Ativa": ["Natação 1000m ou alongamento dinâmico"]
        }
    },
    
    # Esportes - Basquete
    ("⚽ Esportes Olímpicos", "Basquetebol (jogo competitivo)", "Intermediário", "4-5x"): {
        "nome": "Basquete Intermediário — Agilidade e Arremesso",
        "descricao": "Treino específico para basquete com fundamentos, agilidade, saltos e condicionamento.",
        "dias": {
            "Segunda — Fundamentos + Arremesso": [
                "Aquecimento com bola (10 min)",
                "Arremessos (100 tentativas)",
                "Bandejas (50 cada lado)",
                "Manejo de bola"
            ],
            "Terça — Agilidade e Saltos": [
                "Escada de agilidade (15 min)",
                "Saltos verticais (4×10)",
                "Pliometria (hopping, bounding)",
                "Defesa lateral (sideshuffle)"
            ],
            "Quarta — Força": [
                "Agachamento — 4×6",
                "Levantamento terra — 4×5",
                "Supino reto — 4×8",
                "Prancha lateral — 4×30s"
            ],
            "Quinta — Jogo Tático": ["Aquecimento → Exercícios táticos → Jogo reduzido (5x5, 20 min)"],
            "Sexta — Condicionamento": ["Idas e vindas (suicides) → Corrida contínua 30 min"],
            "Sábado — Descanso ou Alongamento": []
        }
    },
# Inserir ANTES da linha 735 (antes do fechamento } do dicionário)

    # ══════════════════════════════════════════════════════════════════════════
    # ACADEMIA — níveis faltantes
    # ══════════════════════════════════════════════════════════════════════════
    ("🏋️ Academia / Musculação", "Iniciante", "4-5x"): {
        "nome": "Upper / Lower Split — Iniciante 4x",
        "descricao": "2 dias MMSS + 2 dias MMII. 3 séries × 12 reps. Intervalo 60s. Aprende o movimento antes de aumentar carga.",
        "dias": {
            "Upper A — Seg": ["Supino reto halteres 3×12","Remada curvada 3×12","Desenvolvimento halteres 3×12","Puxada frontal 3×12","Rosca direta 3×12","Tríceps pulley 3×12"],
            "Lower A — Ter": ["Agachamento livre 3×12","Leg press 3×12","Cadeira extensora 3×15","Panturrilha em pé 4×15","Prancha 3×30s"],
            "Upper B — Qui": ["Supino inclinado 3×12","Remada unilateral 3×12","Elevação lateral 3×15","Barra fixa assistida 3×8","Rosca martelo 3×12","Dips assistido 3×10"],
            "Lower B — Sex": ["Stiff halteres 3×12","Cadeira flexora 3×12","Hip thrust 3×12","Avanço 3×10 cada","Panturrilha sentado 4×15"],
        }
    },
    ("🏋️ Academia / Musculação", "Intermediário", "3x"): {
        "nome": "Full Body Intermediário — Força 3x",
        "descricao": "3 sessões full body com ênfase em força. 4 séries. Periodização simples: semana de força / semana de volume.",
        "dias": {
            "Treino A — Seg": ["Agachamento 4×5 (força)","Supino reto 4×5","Remada curvada 4×5","Desenvolvimento 3×8","Rosca+Tríceps superset 3×10"],
            "Treino B — Qua": ["Levantamento terra 4×4","Supino inclinado 4×8","Puxada frontal 4×8","Elevação lateral 3×15","Panturrilha 4×15"],
            "Treino C — Sex": ["Leg press 4×10","Crucifixo 4×12","Remada cavalinho 4×10","Rosca+Tríceps superset 4×12","Prancha 3×45s"],
        }
    },
    ("🏋️ Academia / Musculação", "Intermediário", "6-7x"): {
        "nome": "PPL Intermediário — Push/Pull/Legs",
        "descricao": "6 treinos semanais. Duas vezes por semana cada grupo. Intensidade moderada-alta.",
        "dias": {
            "Push A — Seg": ["Supino reto 4×8","Supino inclinado 4×10","Desenvolvimento 4×10","Elevação lateral 4×15","Tríceps corda 3×12"],
            "Pull A — Ter": ["Remada curvada 4×8","Puxada frontal 4×10","Remada unilateral 3×12","Rosca direta 4×10"],
            "Legs A — Qua": ["Agachamento 4×8","Leg press 4×12","Extensora 3×15","Stiff 4×10","Panturrilha 5×15"],
            "Push B — Qui": ["Supino inclinado halteres 4×10","Peck deck 3×12","Desenvolvimento halteres 3×12","Triceps testa 3×10"],
            "Pull B — Sex": ["Pullover 4×12","Barra fixa 4×máx","Remada cavalinho 4×10","Rosca martelo 3×12"],
            "Legs B — Sáb": ["Stiff 4×8","Flexora 4×12","Hip thrust 4×10","Sumô 3×12","Panturrilha sentado 5×20"],
        }
    },
    ("🏋️ Academia / Musculação", "Avançado", "4-5x"): {
        "nome": "Upper/Lower Avançado — Força + Hipertrofia",
        "descricao": "Periodização ondulada avançada. 5×5 nos dias de força, 4×10-12 nos dias de hipertrofia.",
        "dias": {
            "Upper Força — Seg": ["Supino reto 5×5","Remada curvada 5×5","Desenvolvimento militar 4×6","Rosca 3×8","Tríceps francês 3×8"],
            "Lower Força — Ter": ["Agachamento 5×5","Levantamento terra 4×4","Avanço búlgaro 3×8 cada","Panturrilha 5×12"],
            "Upper Hipertrofia — Qui": ["Supino inclinado 4×10","Puxada neutra 4×10","Face pull 4×15","Rosca 21 3 séries","Tríceps corda drop set 3 séries"],
            "Lower Hipertrofia — Sex": ["Leg press 4×15","Extensora 4×15+drop","Flexora 4×15","Hip thrust 4×12","Panturrilha sentado 5×20"],
        }
    },
    ("🏋️ Academia / Musculação", "Atleta", "4-5x"): {
        "nome": "Força Atleta — Powerlifting Adaptado",
        "descricao": "Foco em força máxima. Periodização por blocos. Exercícios base com variações.",
        "dias": {
            "Agachamento (Seg)": ["Agachamento 5×3 (85-90% 1RM)","Leg press pausa 4×6","Extensora 3×10","Stiff 4×6"],
            "Supino (Ter)": ["Supino reto 5×3 (85-90%)","Supino pausa 4×5","Crucifixo 3×12","Tríceps corda 4×10","Face pull 4×15"],
            "Terra (Qui)": ["Levantamento terra 5×2 (90%+)","RDL 4×6","Remada curvada 4×6","Puxada 4×8"],
            "Volume (Sex)": ["Agachamento 4×8 (70%)","Supino 4×8 (70%)","Acessórios: panturrilha, core, ombro"],
        }
    },
    ("🏋️ Academia / Musculação", "Atleta", "6-7x"): {
        "nome": "Atleta — PPL de Alta Performance",
        "descricao": "PPL 6x com periodização avançada. Drop sets, rest-pause e técnicas de intensificação.",
        "dias": {
            "Push A — Força (Seg)": ["Supino 5×3","Desenvolvimento militar 4×5","Crucifixo 4×10","Tríceps francês 4×8"],
            "Pull A — Força (Ter)": ["Terra 4×3","Barra fixa lastro 4×5","Remada curvada 4×6","Rosca 4×8"],
            "Legs A — Foco Quad (Qua)": ["Agachamento 5×4","Front squat 4×5","Leg press 4×10+drop","Extensora 4×15"],
            "Push B — Volume (Qui)": ["Supino inclinado 5×8","Peck deck 4×12","Desenvolvimento 4×10","Superset tríceps 4 séries"],
            "Pull B — Volume (Sex)": ["Pullover 4×12","Puxada neutra 4×10","Remada cavalinho 4×10","Superset rosca 4 séries"],
            "Legs B — Foco Post (Sáb)": ["RDL 5×6","Hip thrust 4×10","Flexora drop set 4 séries","Panturrilha 6×15"],
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CARDIOVASCULAR — todos os níveis e atividades específicas
    # ══════════════════════════════════════════════════════════════════════════
    ("🏃 Cardiovascular", "Iniciante", "4-5x"): {
        "nome": "Caminhada Progressiva — Iniciante 4x",
        "descricao": "Progressão de caminhada para corrida em 8 semanas. 4 sessões semanais.",
        "dias": {
            "Sessão 1 (Seg)": ["Caminhada 30 min em ritmo confortável — Zona 2 (60-70% FCM)"],
            "Sessão 2 (Ter)": ["Caminhada 20 min + 4×2 min corrida leve com 3 min caminhada"],
            "Sessão 3 (Qui)": ["Caminhada 35 min levemente mais rápido"],
            "Sessão 4 (Sex)": ["Caminhada/corrida 30 min alternando conforme condicionamento"],
        }
    },
    ("🏃 Cardiovascular", "Intermediário", "3x"): {
        "nome": "Corrida Intermediário — Base Aeróbica 3x",
        "descricao": "Construção de base aeróbica sólida. Longo semanal + intervalado + regenerativo.",
        "dias": {
            "Longo (Dom)": ["Corrida 40-50 min em ritmo leve — Zona 2 (60-70% FCM)"],
            "Intervalado (Qua)": ["Aquecimento 10 min → 5×800m em Zona 4 (80-90% FCM) c/ 90s descanso → volta 10 min"],
            "Regenerativo (Sex)": ["Trote 25-30 min muito leve — Zona 1 (abaixo de 65% FCM)"],
        }
    },
    ("🏃 Cardiovascular", "Avançado", "6-7x"): {
        "nome": "Corrida Avançado — Alto Volume 6x",
        "descricao": "Preparação para meia maratona ou maratona. Periodização 3:1 (3 semanas carga, 1 recuperação).",
        "dias": {
            "Longo (Dom)": ["90-120 min em Zona 2 — base aeróbica"],
            "Tempo (Seg)": ["40 min em limiar anaeróbico (Zona 3-4) — pace confortavelmente difícil"],
            "Intervalado (Ter)": ["8×800m em Zona 5 (pace 5km) | descanso 90s"],
            "Regenerativo (Qua)": ["30 min muito leve ou descanso"],
            "Fartlek (Qui)": ["45 min: alterna 2 min forte / 1 min leve"],
            "Strides (Sex)": ["20 min leve + 8×100m aceleração progressiva"],
        }
    },
    ("🏃 Cardiovascular", "Atleta", "6-7x"): {
        "nome": "Corrida Atleta — Competição",
        "descricao": "Estrutura de atleta competitivo. Requer acompanhamento de treinador. Volume 80-120km/semana.",
        "dias": {
            "Longo (Dom)": ["120-150 min em Zona 2"],
            "Qualidade A (Ter)": ["10-12×1000m em pace 10km | descanso 90s"],
            "Qualidade B (Qui)": ["3×20 min no limiar | descanso 3 min"],
            "Volume (Seg/Qua/Sex)": ["30-60 min regenerativo ou moderado (Zona 1-2)"],
        }
    },

    # Triathlon — todos os níveis (atividade específica com 4 chaves)
    ("🏃 Cardiovascular", "Triathlon — treino combinado (natação+bike+corrida)", "Iniciante", "3x"): {
        "nome": "Triathlon Iniciante — Fundamentos das 3 Modalidades",
        "descricao": "Aprende as 3 modalidades e as transições. Distâncias curtas (Sprint ou Super Sprint).",
        "dias": {
            "Natação (Seg)": ["300-400m contínuo crawl | técnica e respiração bilateral | foco na eficiência"],
            "Bike (Qua)": ["30-40 min ciclismo lazer em zona 2 | pedalada técnica e posição","Musculação: Agachamento 3×12 | Leg press 3×12 | Prancha 3×30s"],
            "Corrida (Sex)": ["Corrida/caminhada alternada 25 min | Jeff Galloway adaptado","Após: 10 min natação ou mobilidade"],
        }
    },
    ("🏃 Cardiovascular", "Triathlon — treino combinado (natação+bike+corrida)", "Intermediário", "4-5x"): {
        "nome": "Triathlon Intermediário — Olímpico ou Sprint",
        "descricao": "Preparação para triathlon olímpico (1.5km nado + 40km bike + 10km corrida). Inclui brick e musculação de suporte.",
        "dias": {
            "Natação + Corrida (Seg)": [
                "Natação: 400m aquec. → 6×100m crawl (30s desc.) → 200m recupero",
                "Corrida (transição): 15-20 min em ritmo de prova",
            ],
            "Musculação Funcional (Ter)": [
                "Agachamento 4×8 | RDL (peso morto romeno) 4×8",
                "Remada curvada 4×10 | Supino 3×10",
                "Prancha + Rotação de tronco 3×45s",
                "⚡ Fortalecimento previne lesões no triathlon",
            ],
            "Bike Moderada (Qua)": [
                "60-75 min em Zona 2-3 (65-80% FCM)",
                "Últimos 15 min: aumentar cadência (90-100 rpm)",
            ],
            "Natação Técnica (Qui)": [
                "2000m: drills de braçada + séries de velocidade",
                "Crawl, costas e viradas de parede",
            ],
            "BRICK — Bike + Corrida (Sáb)": [
                "Bike: 45-60 min em Zona 3 → Transição direta",
                "Corrida: 20-25 min em ritmo de prova",
                "⚡ Brick treina o corpo para a transição T2",
            ],
        }
    },
    ("🏃 Cardiovascular", "Triathlon — treino combinado (natação+bike+corrida)", "Avançado", "6-7x"): {
        "nome": "Triathlon Avançado — Meio Ironman / Ironman",
        "descricao": "Volume alto com periodização. Treinos duplos. Para atletas experientes com base sólida.",
        "dias": {
            "Longa Natação + Corrida (Seg)": [
                "Natação: 3000m com séries por zona de FC",
                "Corrida: 30 min em Zona 2",
            ],
            "Musculação (Ter)": [
                "Levantamento terra 4×5 | Agachamento 4×6",
                "Remada 4×8 | Core avançado (dead bug, pallof press)",
                "⚡ Força de base reduz lesão em alto volume",
            ],
            "Bike Longa (Qua)": ["2-3h em Zona 2-3 | últimos 20 min em Zona 4 (Sweetspot)"],
            "Natação Velocidade (Qui)": ["10×200m em Zona 4-5 | descanso 30s | total ~3000m"],
            "Corrida Qualidade (Sex)": ["3×15 min no limiar | descanso 3 min | total ~50 min"],
            "BRICK Longo (Sáb)": [
                "Bike: 90-120 min Zona 3 → Transição",
                "Corrida: 30-40 min em ritmo de prova",
            ],
            "Recuperação (Dom)": ["Natação técnica 1500m ou alongamento/yoga 45 min"],
        }
    },
    ("🏃 Cardiovascular", "Triathlon — treino combinado (natação+bike+corrida)", "Atleta", "6-7x"): {
        "nome": "Triathlon Atleta — Alto Desempenho",
        "descricao": "Periodização de atleta competitivo de triathlon. Necessita treinador especializado.",
        "dias": {
            "Natação AM + Corrida PM (Seg)": ["AM: 4000m técnica e velocidade | PM: 45 min corrida Zona 2"],
            "Força + Bike (Ter)": ["Força olímpica 60 min | Bike 90 min Zona 2"],
            "Natação AM + Bike PM (Qua)": ["AM: 3000m velocidade | PM: 2h bike Zona 3-4"],
            "Corrida (Qui)": ["70 min: 4×10 min no limiar com 3 min descanso"],
            "BRICK Longo (Sex)": ["Bike 120 min Zona 3 → Corrida 45 min ritmo de prova"],
            "Sessão Longa (Sáb)": ["Natação 4000m OU Bike 3-4h OU Corrida 25-30km"],
            "Recuperação (Dom)": ["Natação técnica leve ou descanso completo"],
        }
    },

    # Ciclismo específico
    ("🏃 Cardiovascular", "Ciclismo moderado (16–22 km/h)", "Iniciante", "3x"): {
        "nome": "Ciclismo Iniciante — Base e Técnica",
        "descricao": "Construção de base aeróbica no ciclismo. Cadência técnica e posição no bike.",
        "dias": {
            "Bike Leve (Seg)": ["45 min Zona 2 (60-70% FCM) | cadência 80-90 rpm | terreno plano"],
            "Musculação Suporte (Qua)": ["Agachamento 3×12 | Leg press 3×12 | Extensora 3×15 | Stiff 3×12 | Core 3 séries"],
            "Bike Moderado (Sex)": ["60 min Zona 2-3 | incluir pequenas subidas | foco na respiração"],
        }
    },
    ("🏃 Cardiovascular", "Ciclismo moderado (16–22 km/h)", "Intermediário", "4-5x"): {
        "nome": "Ciclismo Intermediário — Volume e Intensidade",
        "descricao": "Progressão de volume e introdução de treinos de qualidade (intervalados e sweetspot).",
        "dias": {
            "Endurance (Seg)": ["90 min Zona 2 | cadência 85-95 rpm"],
            "Intervalado (Ter)": ["Aquec. 15 min → 5×4 min em Zona 4 (85-90% FCM) desc. 4 min → Resfr. 15 min"],
            "Musculação (Qua)": ["Agachamento 4×8 | Terra 4×6 | Afundo 3×10 | Core avançado"],
            "Sweetspot (Qui)": ["30 min Zona 2 → 2×20 min em Zona 3-4 (Sweetspot) → 15 min Zona 1"],
            "Bike Longa (Sáb/Dom)": ["2-3h em Zona 2 com intensificações nos últimos 20 min"],
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # AQUÁTICAS — todos os níveis
    # ══════════════════════════════════════════════════════════════════════════
    ("🏊 Aquáticas", "Iniciante", "4-5x"): {
        "nome": "Natação Iniciante — Progressão 4x",
        "descricao": "Adaptação ao meio aquático e técnica de crawl. Inclui musculação de suporte.",
        "dias": {
            "Natação Técnica (Seg)": ["Pernada com prancha 4×25m | Braçada c/ pull buoy 4×25m | Crawl 4×50m"],
            "Musculação (Ter)": ["Puxada frontal 3×12 | Remada unilateral 3×12 | Desenvolvimento 3×12 | Rotação externa ombro 3×15"],
            "Natação Volume (Qui)": ["6×50m crawl c/ 30s desc. | 4×25m costas | 200m livre"],
            "Hidroginástica (Sex)": ["45 min de hidroginástica moderada — baixo impacto"],
        }
    },
    ("🏊 Aquáticas", "Intermediário", "3x"): {
        "nome": "Natação Intermediário — Técnica e Volume",
        "descricao": "Aprimoramento técnico com volume progressivo. Foco em crawl e costas.",
        "dias": {
            "Técnico (Seg)": ["400m aquec. | Drills 4×50m | 6×100m crawl c/ 20s desc. | 200m costas"],
            "Velocidade (Qua)": ["300m aquec. | 8×50m sprint (30s desc.) | 4×100m moderado c/ 15s | 200m resfr."],
            "Longo (Sex)": ["400m aquec. | 1500m contínuo em ritmo moderado | 200m peito resfr."],
        }
    },
    ("🏊 Aquáticas", "Intermediário", "4-5x"): {
        "nome": "Natação Intermediário — Todos os Nados",
        "descricao": "Trabalha os 4 nados com séries específicas por técnica e velocidade.",
        "dias": {
            "Crawl + Costas (Seg)": ["500m aquec. | 8×100m crawl c/ 15s | 4×50m costas | 200m resfr."],
            "Musculação Ombro (Ter)": ["Rotação externa 4×15 | Elevation lateral 4×15 | Remada 4×12 | Puxada 4×10"],
            "Peito + Borboleta (Qua)": ["400m aquec. | 6×50m peito c/ 30s | 4×25m borboleta c/ 45s | 300m livre"],
            "Velocidade (Qui)": ["12×50m alternando nados | 30s desc. | foco em viragem e saída"],
            "Longo / Medley (Sáb)": ["3000m contínuo ou séries longas de medley"],
        }
    },
    ("🏊 Aquáticas", "Avançado", "4-5x"): {
        "nome": "Natação Avançado — Desempenho",
        "descricao": "Treino de alto desempenho com séries de VO2, velocidade e resistência específica.",
        "dias": {
            "Crawl Intenso (Seg)": ["600m aquec. | 10×100m Zona 4 c/ 15s | 400m resfr. | total 2400m"],
            "Técnica Mista (Ter)": ["Costas 4×100 | Peito 4×100 | Borboleta 4×50 | Drills 4×25"],
            "Musculação (Qua)": ["Levantamento terra 4×5 | Remada curvada 4×8 | Puxada 4×8 | Core 4 séries"],
            "Velocidade (Qui)": ["15×50m sprint alternando nados | 20s desc. | saída em bloco"],
            "Longo (Sáb)": ["4000m crawl em pace aeróbico + 500m técnica"],
        }
    },
    ("🏊 Aquáticas", "Atleta", "6-7x"): {
        "nome": "Natação Atleta — Competição",
        "descricao": "Volume de atleta competitivo. 4000-6000m/sessão. Necessita treinador.",
        "dias": {
            "Volume Longo (Seg)": ["5000m variando nados e intensidades"],
            "Velocidade (Ter)": ["20×100m Zona 4-5 c/ 20s desc. | saída com bloco"],
            "Técnica + Força (Qua)": ["3000m técnica | Musculação específica natação"],
            "Medley Intenso (Qui)": ["Séries de medley 4×400m c/ 60s desc."],
            "Sprint (Sex)": ["30×50m sprint c/ 30s desc. — potência máxima"],
            "Longa (Sáb)": ["6000m contínuo ou com séries longas"],
            "Recuperação (Dom)": ["1500m técnica muito leve"],
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # DANÇA — todos os níveis
    # ══════════════════════════════════════════════════════════════════════════
    ("💃 Dança", "Iniciante", "3x"): {
        "nome": "Dança Iniciante — Ritmo e Coordenação",
        "descricao": "Fundamentos de ritmo, postura e coordenação motora. Qualquer estilo de dança.",
        "dias": {
            "Aula 1": ["Aquecimento rítmico 10 min","Passos básicos do estilo escolhido 30 min","Alongamento final 10 min"],
            "Aula 2": ["Revisão 15 min","Sequência nova 25 min","Prática livre 10 min"],
            "Aula 3": ["Integração de sequências 20 min","Ensaio coreografia simples 20 min","Resfriamento 10 min"],
        }
    },
    ("💃 Dança", "Iniciante", "4-5x"): {
        "nome": "Dança Iniciante Intensivo",
        "descricao": "Progressão mais rápida. Inclui condicionamento físico complementar.",
        "dias": {
            "Técnica (Seg/Qui)": ["Aquec. 15 min | Técnica do estilo 40 min | Resfr. 10 min"],
            "Coreografia (Ter/Sex)": ["Ensaio de sequência 60 min"],
            "Condicionamento (Qua)": ["Cardio 20 min + Core 20 min + Alongamento 20 min"],
        }
    },
    ("💃 Dança", "Intermediário", "3x"): {
        "nome": "Dança Intermediário — Técnica e Expressão",
        "descricao": "Aprimoramento técnico, musicalidade e resistência para dançarinos.",
        "dias": {
            "Técnica (Seg)": ["Aquec. específico 15 min | Técnica avançada 40 min | Resfr. 10 min"],
            "Coreografia (Qua)": ["Ensaio de repertório 60 min com feedback técnico"],
            "Condicionamento (Sex)": ["Funcional para dança: core, equilíbrio, pliometria 60 min"],
        }
    },
    ("💃 Dança", "Intermediário", "4-5x"): {
        "nome": "Dança Intermediário — Performance",
        "descricao": "Foco em performance, resistência e qualidade técnica.",
        "dias": {
            "Técnica A (Seg/Qua)": ["Aquec. 15 min | Técnica específica 40 min | Resfr. 10 min"],
            "Coreografia (Ter/Qui)": ["Ensaio de repertório 60 min"],
            "Condicionamento (Sex)": ["Funcional para dança 60 min — core, equilíbrio, pliometria"],
        }
    },
    ("💃 Dança", "Avançado", "4-5x"): {
        "nome": "Dança Avançado — Profissional",
        "descricao": "Treino de bailarino profissional ou dançarino competitivo.",
        "dias": {
            "Barra + Centro (Diário)": ["Aquec. 20 min | Técnica avançada 50 min | Resfr. 15 min"],
            "Coreografia (Ter/Sex)": ["Ensaio completo de coreografia competitiva 90 min"],
            "Cross-training (Qua)": ["Pilates 60 min ou Yoga avançado — manutenção e prevenção de lesões"],
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # MENTE E CORPO — todos os níveis
    # ══════════════════════════════════════════════════════════════════════════
    ("🧘 Mente e Corpo", "Iniciante", "3x"): {
        "nome": "Yoga / Pilates Iniciante — Fundamentos",
        "descricao": "Respiração, consciência corporal e mobilidade. Sem exigência de flexibilidade prévia.",
        "dias": {
            "Sessão 1 — Base": ["Respiração diafragmática 5 min","Posturas em pé 20 min","Posturas no chão 20 min","Savasana 5 min"],
            "Sessão 2 — Core": ["Prancha 3×30s","Dead bug 3×10","Bird dog 3×10","Alongamento global 20 min"],
            "Sessão 3 — Mobilidade": ["Mobilização articular 10 min","Alongamento progressivo 40 min"],
        }
    },
    ("🧘 Mente e Corpo", "Iniciante", "4-5x"): {
        "nome": "Yoga / Pilates Iniciante — Prática Frequente",
        "descricao": "4 sessões semanais para desenvolvimento rápido de flexibilidade e força de core.",
        "dias": {
            "Força (Seg/Qui)": ["Pilates solo 60 min — foco em powerhouse (core profundo)"],
            "Flexibilidade (Ter)": ["Yoga Hatha 60 min — posturas sustentadas"],
            "Mobilidade (Qua/Sex)": ["Mobilização articular + alongamento progressivo 45 min"],
        }
    },
    ("🧘 Mente e Corpo", "Intermediário", "3x"): {
        "nome": "Yoga / Pilates Intermediário — Força e Flexibilidade",
        "descricao": "Equilíbrio entre força, flexibilidade e controle. Para praticantes com base.",
        "dias": {
            "Força (Seg)": ["Pilates aparelhos ou sequência avançada de core 60 min"],
            "Flexibilidade (Qua)": ["Yoga restaurativo ou Yin Yoga 60 min"],
            "Equilíbrio (Sex)": ["Posturas de equilíbrio, inversões assistidas e pranayama"],
        }
    },
    ("🧘 Mente e Corpo", "Intermediário", "4-5x"): {
        "nome": "Yoga / Pilates Intermediário — Desenvolvimento Completo",
        "descricao": "4-5 sessões com foco em diferentes aspectos do treinamento mente-corpo.",
        "dias": {
            "Força Core (Seg)": ["Pilates mat avançado ou aparelhos 60 min"],
            "Yoga Dinâmico (Ter)": ["Vinyasa ou Power Yoga 60 min"],
            "Yin / Restaurativo (Qua)": ["Yoga restaurativo ou Yin 60 min"],
            "Mobilidade (Qui)": ["Mobilização articular + pranayama 45 min"],
            "Integração (Sex/Sáb)": ["Sequência completa combinando força, flex. e respiração"],
        }
    },
    ("🧘 Mente e Corpo", "Avançado", "4-5x"): {
        "nome": "Yoga / Pilates Avançado — Performance",
        "descricao": "Prática avançada com inversões, posturas complexas e breathing técnico.",
        "dias": {
            "Força Avançada (Seg/Qui)": ["Ashtanga ou Pilates nível avançado 90 min"],
            "Yin Profundo (Ter)": ["Yin Yoga 75 min — posturas sustentadas 5-10 min"],
            "Meditação + Pranayama (Qua)": ["Técnicas respiratórias avançadas + meditação guiada 45 min"],
            "Integração (Sex)": ["Sequência completa com inversões e transições fluidas 90 min"],
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # LUTAS — vários níveis e modalidades
    # ══════════════════════════════════════════════════════════════════════════
    ("🥋 Lutas", "Jiu-Jitsu (rolagem / luta)", "Iniciante", "3x"): {
        "nome": "Jiu-Jitsu Iniciante — Técnica e Posicionamento",
        "descricao": "Fundamentos do BJJ: posições de guarda, passagem, finalização básica.",
        "dias": {
            "Técnica (Seg)": ["Aquecimento específico BJJ 15 min","Técnica nova (2 posições) 40 min","Rolagem posicional leve 20 min","Alongamento 10 min"],
            "Condicionamento (Qua)": ["Exercícios físicos específicos: puxadas, quedas técnicas, bridging","Circuito 3 rodadas: sprawl + grappling dummy + escada de agilidade"],
            "Técnica + Rolagem (Sex)": ["Revisão técnica 30 min","Rolagem com parceiros de nível similar 30 min","Análise de posições"],
        }
    },
    ("🥋 Lutas", "Judô / Jiu-Jitsu", "Intermediário", "4-5x"): {
        "nome": "Judô/BJJ Intermediário — Condicionamento e Técnica",
        "descricao": "Treino específico para artes marciais de agarre. Força de pegada, explosão e resistência.",
        "dias": {
            "Técnica (Seg/Qua/Sex)": ["Aquec. BJJ/Judô 15 min | Técnica 40 min | Randori/Rolagem 30 min"],
            "Força e Pegada (Ter)": ["Puxada supinada 4×8","Remada cavalinho 4×10","Rosca grossa 4×12","Farmer's carry 4×20m","Prancha com peso 4×45s"],
            "Condicionamento (Qui)": ["HIIT específico: 8 ex. × 30s trabalho / 15s desc. — 6 rodadas","Burpees, kettlebell, corda naval, sprawl"],
        }
    },
    ("🥋 Lutas", "Boxe / Muay Thai / Kickboxing", "Iniciante", "3x"): {
        "nome": "Boxe/Muay Thai Iniciante — Técnica de Base",
        "descricao": "Guarda, jab, direto, giro de quadril e defesas básicas. Condicionamento aeróbico.",
        "dias": {
            "Técnica (Seg)": ["Sombra 3×3 min | Mitts com parceiro 3×2 min | Saco pesado 3×3 min","Aquecimento e resfriamento 15 min"],
            "Condicionamento (Qua)": ["Corda 3×3 min","Saco pesado 5×3 min (intensidade leve-moderada)","Core: ab wheel + twists + prancha"],
            "Técnica + Sparring Leve (Sex)": ["Revisão de combos | Sparring técnico controlado 3×2 min"],
        }
    },
    ("🥋 Lutas", "Boxe / Muay Thai / Kickboxing", "Intermediário", "4-5x"): {
        "nome": "Boxe/Muay Thai Intermediário — Combos e Condicionamento",
        "descricao": "Desenvolvimento de combos, defesas e condicionamento específico para luta.",
        "dias": {
            "Técnica (Seg/Qua/Sex)": ["Sombra 5×3 min | Mitts 4×3 min | Saco 4×3 min | Sparring 3×3 min"],
            "Força Funcional (Ter)": ["Supino 4×8 | Desenvolvimento 4×8 | Remada 4×10 | Core pesado"],
            "Resistência (Qui)": ["Corda 10×1 min c/ 30s desc. | Sprint 8×100m | HIIT 3 rodadas"],
        }
    },
    ("🥋 Lutas", "Taekwondo / Karatê / Artes Marciais em pé", "Iniciante", "3x"): {
        "nome": "Artes Marciais em Pé — Iniciante",
        "descricao": "Postura básica, chutes e socos fundamentais. Flexibilidade e equilíbrio.",
        "dias": {
            "Técnica (Seg)": ["Aquec. 15 min | Postura + Deslocamentos 20 min | Chutes básicos 25 min | Alongamento 15 min"],
            "Condicionamento (Qua)": ["Corda 3×3 min | Pliometria (saltos) 20 min | Core 20 min"],
            "Técnica + Kata (Sex)": ["Revisão técnica 30 min | Kata ou sequência básica 30 min"],
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ESPORTES — modalidades coletivas e individuais
    # ══════════════════════════════════════════════════════════════════════════
    ("⚽ Esportes Olímpicos", "Futebol de Campo (recreativo)", "Iniciante", "3x"): {
        "nome": "Futebol Recreativo — Condicionamento Base",
        "descricao": "Condicionamento para jogar futebol recreativo sem lesões.",
        "dias": {
            "Condicionamento (Seg)": ["Corrida 20 min Zona 2","Agachamento 3×12 | Stiff 3×12 | Agilidade (cones) 15 min"],
            "Técnica (Qua)": ["Fundamentos: passe, domínio, chute 45 min | Pequeno jogo 15 min"],
            "Jogo + Física (Sex)": ["Aquec. 15 min | Partida 60 min | Resfr. e alongamento 15 min"],
        }
    },
    ("⚽ Esportes Olímpicos", "Futsal / Futebol Society", "Intermediário", "4-5x"): {
        "nome": "Futsal / Society Intermediário — Performance",
        "descricao": "Treino específico de futsal com técnica, tática e condicionamento de alta intensidade.",
        "dias": {
            "Técnica (Seg/Qui)": ["Aquec. 15 min | Fundamentos técnicos 40 min | Jogo reduzido 20 min"],
            "Força (Ter)": ["Agachamento 4×8 | Leg press 4×10 | Stiff 4×8 | Saltos 4×10"],
            "HIIT Específico (Qua)": ["10×30m sprint c/ 30s desc. | Circuito agilidade 20 min"],
            "Jogo (Sex)": ["Partida completa com análise tática"],
        }
    },
    ("⚽ Esportes Olímpicos", "Voleibol (jogo recreativo)", "Iniciante", "3x"): {
        "nome": "Vôlei Recreativo — Fundamentos",
        "descricao": "Saque, manchete, toque e bloqueio. Condicionamento para quadra.",
        "dias": {
            "Técnica (Seg)": ["Manchete 20 min | Toque 20 min | Saque 15 min | Jogo 20 min"],
            "Condicionamento (Qua)": ["Saltos 4×10 | Lateralidade (sliding) 20 min | Core 20 min"],
            "Jogo (Sex)": ["Partida 60 min com feedback técnico"],
        }
    },
    ("⚽ Esportes Olímpicos", "Tênis (simples)", "Intermediário", "4-5x"): {
        "nome": "Tênis Intermediário — Técnica e Condicionamento",
        "descricao": "Desenvolvimento de golpes, movimentação em quadra e resistência.",
        "dias": {
            "Técnica (Seg/Qui)": ["Aquec. 15 min | Treino de golpes 45 min | Jogo 30 min"],
            "Força (Ter)": ["Rotação de tronco 4×15 | Supino 4×10 | Remada 4×10 | Agachamento 4×10"],
            "Condicionamento (Qua)": ["Sprints laterais 10×30m | Footwork 20 min | HIIT 15 min"],
            "Jogo Competitivo (Sex)": ["Pelada ou set de treino 90 min"],
        }
    },
    # Powerlifting Iniciante
    ("💪 Esportes de Força", "Powerlifting - treino técnico (leve)", "Iniciante", "3x"): {
        "nome": "Powerlifting Iniciante - Técnica dos 3 Movimentos",
        "descricao": "Aprendizado técnico do agachamento, supino e levantamento terra. Foco na forma correta antes de aumentar carga. Progressão linear: +2,5kg por sessão nos exercícios principais.",
        "dias": {
            "Dia A - Agachamento + Supino (Seg)": [
                "Agachamento livre (começar com barra vazia -> carga leve) - 5x5",
                "ATENCAO: descer ate 90 graus ou abaixo, joelhos alinhados com os pes",
                "Supino reto (barra) - 5x5",
                "ATENCAO: cotovelos a 45-75 graus do corpo, arco lombar natural",
                "Barra fixa (pull-up) - 3xmax (mobilidade complementar)",
                "Prancha frontal - 3x45s",
            ],
            "Dia B - Terra + Supino (Qui)": [
                "Levantamento terra (convencional) - 5x3",
                "ATENCAO: barra sobre o medio-pe, costas neutras, quadril acima dos joelhos",
                "Supino reto - 5x5 (carga maior que Dia A)",
                "Agachamento frontal (front squat) - 3x5 (mobilidade e tecnica)",
                "Face pull - 4x15 (saude do ombro)",
                "Abdominal hollow hold - 3x30s",
            ],
            "Dia C - Volume (Sex)": [
                "Agachamento pausa 3s no fundo - 4x3",
                "Supino com pausa 1s no peito - 4x3",
                "Romanian Deadlift (RDL) - 4x8 (60% da carga do terra)",
                "Rosca + Triceps superset - 3x12",
            ],
        }
    },
    # Powerlifting Intermediario
    ("💪 Esportes de Força", "Powerlifting - treino moderado", "Intermediario", "4-5x"): {
        "nome": "Powerlifting Intermediario - Forca Linear Avancada",
        "descricao": "Programa 4 dias Upper/Lower enfase nos 3 levantamentos. Periodizacao simples: semana pesada (90%) -> leve (75%) -> moderada (82,5%).",
        "dias": {
            "Dia 1 - Agachamento (Seg)": [
                "Agachamento - 4x4 (80-85% 1RM)",
                "Agachamento pausa - 3x3 (70%)",
                "Leg press - 3x10",
                "Cadeira extensora - 3x12",
                "Panturrilha em pe - 4x15",
            ],
            "Dia 2 - Supino (Ter)": [
                "Supino reto - 4x4 (80-85% 1RM)",
                "Supino com pausa - 3x3 (70%)",
                "Supino inclinado halteres - 3x10",
                "Triceps corda - 4x12",
                "Face pull - 4x15",
                "Rosca direta - 3x12",
            ],
            "Dia 3 - Terra + Posterior (Qui)": [
                "Levantamento terra - 4x3 (80-87% 1RM)",
                "RDL Romanian Deadlift - 3x5 (65%)",
                "Remada curvada barra - 4x8",
                "Good morning - 3x10",
                "Extensao lombar - 3x15",
            ],
            "Dia 4 - Overhead + Upper (Sex)": [
                "Press militar overhead press - 4x6",
                "Remada cavalinho - 4x8",
                "Barra fixa lastro - 4x5",
                "Peck deck - 3x15",
                "Triceps frances - 3x12",
            ],
        }
    },
    # Powerlifting Avancado
    ("💪 Esportes de Força", "Powerlifting - treino intenso / competição", "Avançado", "4-5x"): {
        "nome": "Powerlifting Avancado - Periodizacao por Blocos",
        "descricao": "Blocos de acumulacao, intensificacao e realizacao. Pico de carga nas semanas 8-10 para competicao ou teste de 1RM.",
        "dias": {
            "Agachamento (Seg)": [
                "Agachamento - 5x2-3 (85-92% 1RM)",
                "Agachamento sumo variacao - 3x5",
                "Pausa agachamento - 3x3 (75%)",
                "Leg press - 4x8 + drop set final",
                "Dead bug com peso - 3x10",
            ],
            "Supino (Ter)": [
                "Supino reto - 5x2-3 (85-92% 1RM)",
                "Supino pegada fechada - 4x5 (forca de triceps)",
                "Supino pausa 2s - 3x3 (75%)",
                "Peck deck Crucifixo - 4x12",
                "Triceps corda drop set - 4 series",
                "Face pull + rotacao externa - 4x15",
            ],
            "Terra (Qui)": [
                "Levantamento terra - 5x1-2 (87-95% 1RM)",
                "Terra com deficit pe em step 5cm - 3x3 (70%)",
                "Terra sumo - 3x5 (60%)",
                "Good morning - 4x8",
                "Remada curvada pesada - 4x5",
            ],
            "Overhead + Acessorio (Sex)": [
                "Press militar - 5x3 (progressao semanal)",
                "Barra fixa lastro pesado - 5x3",
                "Triceps testa pesado - 4x6",
                "Rosca direta barra - 4x8",
                "Farmers carry - 4x20m (trabalho de pegada)",
            ],
        }
    },
    # Strongman Iniciante
    ("💪 Esportes de Força", "Strongman - treino geral", "Iniciante", "3x"): {
        "nome": "Strongman Iniciante - Fundamentos dos Eventos",
        "descricao": "Introducao aos movimentos do Strongman adaptados para academia. Usa halteres, kettlebells e sacos de areia para simular os eventos. Foco em tecnica correta e progressao gradual.",
        "dias": {
            "Dia 1 - Terra + Farmers Walk (Seg)": [
                "Levantamento terra - 4x5 (aprender posicao correta)",
                "Base do Strongman - cadeia posterior completa",
                "Farmers Walk com halteres pesados - 4x20m",
                "Simula o Farmers Carry - fortalece pegada, ombros e core",
                "Agachamento goblet kettlebell - 3x10",
                "Prancha com peso - 3x30s",
                "Farmers carry unilateral (valise) - 3x15m cada lado",
            ],
            "Dia 2 - Press + Empurrar e Puxar (Qua)": [
                "Log Press adaptado (barra hexagonal ou halteres pesados) - 4x5",
                "Substitui o Log Press - desenvolvimento de forca overhead",
                "Sled Push adaptado (agachamento com banda elastica) - 4x30s",
                "Sled Pull (puxar saco de areia) - 4x15m",
                "Battle ropes (corda grossa) - 6x30s ondas e chicote",
                "Farmers carry + press final - 3 series combinadas",
            ],
            "Dia 3 - Pedras + Pneu (Sex)": [
                "Simulacao levantamento de pedra: abracar medicine ball pesada - 4x5",
                "Posicao: agachar, abracar, levantar com quadril - tecnica Atlas Stone",
                "Virada de pneu adaptada (terra + empurre) - 4x5",
                "Loaded carry com saco de areia - 4x20m",
                "Isometria de pegada: Farmers hold - 3x60s",
                "Russian twist pesado + wood chop - 3x12",
            ],
        }
    },
    # Strongman Intermediario
    ("💪 Esportes de Força", "Strongman - treino geral", "Intermediario", "4-5x"): {
        "nome": "Strongman Intermediario - Condicionamento de Forca",
        "descricao": "4 sessoes com progressao de carga e eventos mais complexos. Combina forca maxima, explosao e resistencia de forca.",
        "dias": {
            "Forca Base (Seg)": [
                "Levantamento terra - 5x3 (trabalho pesado)",
                "Agachamento frontal - 4x5 (posicao de clean)",
                "Press militar estrito - 4x5",
                "Farmers Walk pesado - 5x20m (carga desafiadora)",
            ],
            "Eventos Carrying (Ter)": [
                "Yoke Walk adaptado (barra nas costas + carga extra) - 4x15m",
                "Simula o Yoke Carry do Strongman",
                "Sled Push (trenó ou substituicao) - 5x20m",
                "Battle ropes - 8x30s trabalho / 30s descanso",
                "Loaded carry de saco de areia - 4x20m",
            ],
            "Press + Overhead (Qui)": [
                "Log Press pesado (barra + presas) - 5x3",
                "Push press - 4x5 (impulso de quadril)",
                "Remada pesada - 4x6",
                "Barra fixa lastro - 4x5",
            ],
            "Eventos Mistos (Sex)": [
                "Atlas stones adaptado - 6 levantamentos maximos",
                "Tyre flip adaptado - 5 viradas + sprint 10m",
                "Puxada de corda rope pull - 3xmax",
                "Farmers Walk final - 3x30m (resistencia de forca)",
                "Pallof press pesado (core antirotacao) - 4x12",
            ],
        }
    },
    # Strongman Avancado
    ("💪 Esportes de Força", "Strongman - treino competitivo (eventos)", "Avançado", "6-7x"): {
        "nome": "Strongman Avancado - Preparacao para Competicao",
        "descricao": "6 sessoes semanais simulando eventos de competicao: Farmers Walk, Log Press, Sled, Yoke, Atlas Stones e terra.",
        "dias": {
            "Terra + Yoke (Seg)": [
                "Levantamento terra - maximas do ciclo",
                "Terra com deficit 5cm - 4x3",
                "Yoke Walk - 4x15m carga crescente",
                "Isometria de pegada - 3x90s",
            ],
            "Log Press + Supino (Ter)": [
                "Log Press - trabalho principal 5x3 ou onda 5-4-3-2-1",
                "Supino reto - 4x5 (suporte ao press)",
                "Push press - 4x3",
                "Triceps pesado - 4x6",
            ],
            "Carrying Events (Qua)": [
                "Farmers Walk - 6x20m progressao de carga",
                "Sled Push + Sled Pull - 5 rodadas carga maxima",
                "Loaded carry medley: 20m Farmers + 20m Yoke + 20m saco",
            ],
            "Pedras + Agachamento (Qui)": [
                "Atlas Stones - 5 levantamentos para plataforma",
                "Agachamento pesado - 4x3 (95% 1RM)",
                "Agachamento sumo base larga - 3x5",
            ],
            "Eventos Resistencia (Sex)": [
                "Battle ropes - 10x30s maxima intensidade",
                "Tyre flip - serie maxima em 90s",
                "Rope pull pesado - 3xmax",
                "Farmers hold grip - 3xmax",
            ],
            "Recuperacao Ativa (Sab)": [
                "Tecnica de levantamento (30-40% das cargas)",
                "Mobilidade de quadril, ombros e coluna toracica",
                "Alongamento especifico para atleta de forca - 40 min",
            ],
        }
    },
    # Halterofilismo Olimpico Iniciante
    ("💪 Esportes de Força", "Halterofilismo Olímpico - técnica", "Iniciante", "3x"): {
        "nome": "Halterofilismo Olimpico Iniciante - Aprendizagem Tecnica",
        "descricao": "Os movimentos olimpicos sao os mais tecnicos do esporte. Iniciante deve passar semanas com barra vazia antes de adicionar carga. Recomendado acompanhamento presencial de tecnico especializado.",
        "dias": {
            "Arranco - Snatch (Seg)": [
                "TECNICA: barra vazia - snatch grip (pegada larga)",
                "Overhead squat - 5x5 (mobilidade indispensavel)",
                "Snatch pull - 4x5 (puxada do chao)",
                "Hang power snatch - 4x3 (da altura dos joelhos)",
                "Power snatch - 4x3 (entrada parcial)",
                "Snatch balance - 3x5 (velocidade sob a barra)",
            ],
            "Arremesso - Clean and Jerk (Qua)": [
                "TECNICA: barra vazia - clean grip (pegada ombros)",
                "Front squat - 5x5 (posicao de recebimento)",
                "Hang power clean - 4x3",
                "Power clean - 4x3",
                "Push press - 4x5 (fase do jerk)",
                "Split jerk - 4x3 (posicao dividida)",
            ],
            "Combinado + Forca (Sex)": [
                "Power snatch + overhead squat - 4x(2+2)",
                "Power clean + front squat + push jerk - 4x(1+2+2)",
                "Agachamento costas - 4x5 (60% do total estimado)",
                "Stiff leg deadlift - 3x8",
                "Core: dead bug + hollow hold - 3 series de cada",
            ],
        }
    },
    # Kettlebell Iniciante
    ("💪 Esportes de Força", "Kettlebell Lifting (snatch / clean & press)", "Iniciante", "3x"): {
        "nome": "Kettlebell Iniciante - Swing, Clean e Press",
        "descricao": "O kettlebell e versatil e eficiente. Treino de forca, potencia e condicionamento em um unico implemento. Iniciante aprende swing, clean e press antes do snatch.",
        "dias": {
            "Forca + Swing (Seg)": [
                "Turkish Get-Up TGU - 5x1 cada lado (tecnica fundamental)",
                "Kettlebell swing bilateral - 5x10",
                "Goblet squat - 4x10",
                "Kettlebell clean unilateral - 4x5 cada",
                "Prancha com kettlebell renegade row - 3x8",
            ],
            "Press + Condicionamento (Qua)": [
                "Kettlebell press estrito - 4x8 cada braco",
                "Swing unilateral - 4x10 cada",
                "Clean + press combinado - 4x5 cada",
                "Farmers carry com kettlebell - 4x20m",
                "Windmill - 3x5 cada (mobilidade e forca obliquia)",
            ],
            "Potencia + Snatch (Sex)": [
                "Kettlebell snatch - 5x5 cada (aprender tecnica)",
                "ATENCAO: snatch e o mais tecnico do kettlebell - cuidado com o punho",
                "Swing duplo two-hand swing pesado - 5x8",
                "Clean + squat + press complexo - 4x3 cada",
                "Battle ropes finalizador - 4x20s",
            ],
        }
    },
    # Calistenia Avancada
    ("💪 Esportes de Força", "Calistenia Avançada (planche, front lever)", "Intermediario", "4-5x"): {
        "nome": "Calistenia Avancada - Progressao Planche e Front Lever",
        "descricao": "Progressao para planche, front lever e muscle-up. Requer base solida: pelo menos 10 pull-ups e 20 dips antes de comecar.",
        "dias": {
            "Planche (Seg)": [
                "Planche lean - 5x5s (inclinacao progressiva)",
                "Tuck planche hold - 5x10s",
                "Advanced tuck -> straddle planche progressao",
                "Pseudo planche push-ups - 5x8",
                "Pike push-ups para ombros - 4x10",
            ],
            "Front Lever + Pull (Ter)": [
                "Tuck front lever hold - 5x10s",
                "Advanced tuck -> straddle front lever progressao",
                "Front lever pull - 5x3",
                "Barra fixa pronada - 5x8 (lastro quando possivel)",
                "L-sit hold - 5x15s",
            ],
            "Muscle-up + Forca (Qui)": [
                "Muscle-up trabalho tecnico - 5x3",
                "Ring muscle-up progressao - 4x3",
                "Dips nas argolas rings - 4x8",
                "Handstand hold parada de mao - 5x20s",
                "Handstand push-up progressao",
            ],
            "Forca Complementar (Sex)": [
                "Pistol squat agachamento unilateral - 4x5 cada",
                "Dragon flag progressao - 4x5",
                "Barra fixa supinada pesada - 5x5",
                "Circuito tecnico: planche + front lever combinado",
            ],
        }
    },

}

# ══════════════════════════════════════════════════════════════════════════════
# AVISO DE SEGURANÇA (ATUALIZADO COM INFORMAÇÕES DE FREQUÊNCIA CARDÍACA)
# ══════════════════════════════════════════════════════════════════════════════
AVISO_SEGURANCA = """
**⚠️ IMPORTANTE — Leia antes de iniciar qualquer atividade física**

Este aplicativo é uma **ferramenta educacional e de apoio ao planejamento**. Ele **não substitui** a avaliação presencial de um profissional habilitado nem prescrição médica.

**Antes de iniciar:**
- Consulte um **médico** para avaliação clínica, especialmente se tiver doenças crônicas, cardiovasculares ou musculoesqueléticas.
- Exija do seu profissional o **CREF ativo** (Conselho Regional de Educação Física). Todo profissional de Educação Física deve apresentar o registro.
- Todo profissional de Educação Física que atua com pessoas deve ter o **SBV — Suporte Básico de Vida** (também chamado de BLS — Basic Life Support). Esse curso capacita para RCP e uso do DEA.
- Para atividades aquáticas supervisionadas: o profissional deve possuir adicionalmente o **Curso de Primeiros Socorros e Salvamento Aquático**.
- **Bacharel em Educação Física com CREF ativo** é o profissional habilitado para prescrever exercícios. Para reabilitação: **Fisioterapeuta com CREFITO ativo**.

**📈 Frequência Cardíaca e Zonas de Treino**
A frequência cardíaca (FC) é um excelente marcador da intensidade do exercício.
- **FC Máxima estimada (FCM):** `220 - IDADE` (fórmula geral). Para indivíduos mais treinados, a fórmula de Karvonen é mais precisa.
- **Zonas de Treino (Baseadas na % da FCM):**
    - **Zona 1 (Muito Leve - 50-60%):** Aquecimento e recuperação ativa.
    - **Zona 2 (Leve - 60-70%):** Queima de gordura, base aeróbica. Ideal para iniciantes.
    - **Zona 3 (Moderada - 70-80%):** Melhora cardiovascular. É a zona do "diálogo entrecortado".
    - **Zona 4 (Intensa - 80-90%):** Aumenta o limiar anaeróbico. Melhora performance.
    - **Zona 5 (Máxima - 90-100%):** Esforço máximo, para sprints e treinos curtos.
- **Monitoramento:** Utilize um frequencímetro de peito (mais preciso) ou de pulso. Durante o exercício, a meta é manter a FC na zona de treino escolhida.

**Sinais de alerta — PARE o treino imediatamente se sentir:**
- Dor no peito, falta de ar intensa ou tontura
- Dor aguda em qualquer articulação
- Batimentos cardíacos irregulares
- Visão turva ou desmaio iminente
- FC acima do limite seguro prescrito

**Progressão segura:**
- Inicie sempre com intensidade baixa e progrida gradualmente (máximo 10% de volume/semana).
- Respeite os dias de descanso — a recuperação é parte do treino.
- Hidrate-se antes, durante e após o exercício.
- Realize aquecimento (5–10 min) e resfriamento (5 min) em toda sessão.

*BioGestão 360 — para uso por profissionais habilitados e público autocapacitado sob orientação médica.*
"""

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO PARA RENDERIZAR CONFIGURAÇÕES DO MÉTODO DE TREINO
# ══════════════════════════════════════════════════════════════════════════════
def renderizar_configuracoes_metodo(metodo_key, prefixo="global"):
    """Renderiza os campos específicos para cada método de treino"""
    metodo = METODOS_TREINO[metodo_key]
    config = {}
    
    if metodo["tipo"] == "fixo":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de séries:", min_value=1, max_value=10, value=3, key=f"{prefixo}_series")
        with col2:
            config["reps"] = st.text_input("Repetições por série:", value="12", key=f"{prefixo}_reps", placeholder="Ex: 12 / 10-12")
        config["tipo"] = "fixo"
    
    elif metodo["tipo"] == "progressivo":
        num_series = metodo.get("series_padrao", 3)
        config["series"] = st.number_input("Número de séries:", min_value=1, max_value=6, value=num_series, key=f"{prefixo}_series")
        config["reps_por_serie"] = []
        config["carga_por_serie"] = []
        
        st.markdown("**Configuração por série:**")
        for i in range(config["series"]):
            col1, col2 = st.columns(2)
            with col1:
                reps_default = metodo["reps_por_serie"][i] if i < len(metodo["reps_por_serie"]) else "10"
                reps = st.text_input(f"Série {i+1} - Repetições:", value=reps_default, key=f"{prefixo}_reps_{i}")
                config["reps_por_serie"].append(reps)
            with col2:
                carga_default = metodo["carga_por_serie"][i] if i < len(metodo["carga_por_serie"]) else "Carga a definir"
                carga = st.text_input(f"Série {i+1} - Carga:", value=carga_default, key=f"{prefixo}_carga_{i}", 
                                      placeholder="Ex: 40kg / 50% RM")
                config["carga_por_serie"].append(carga)
        config["tipo"] = "progressivo"
    
    elif metodo["tipo"] == "drop":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de séries:", min_value=1, max_value=5, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["drops_por_serie"] = st.number_input("Drops por série:", min_value=1, max_value=5, value=metodo["drops_por_serie"], key=f"{prefixo}_drops")
        
        config["reps_iniciais"] = st.text_input("Repetições iniciais:", value=metodo["reps_iniciais"], key=f"{prefixo}_reps_ini")
        config["reducao_carga"] = st.text_input("Redução de carga por drop:", value=metodo["reducao_carga"], key=f"{prefixo}_reducao")
        config["tipo"] = "drop"
    
    elif metodo["tipo"] == "superset":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de supersets:", min_value=1, max_value=6, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["reps_por_exercicio"] = st.text_input("Repetições por exercício:", value=metodo["reps_por_exercicio"], key=f"{prefixo}_reps")
        config["descanso"] = st.text_input("Descanso entre supersets:", value=metodo["descanso_entre_supersets"], key=f"{prefixo}_descanso")
        config["tipo"] = "superset"
    
    elif metodo["tipo"] == "triset":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de trisets:", min_value=1, max_value=5, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["reps_por_exercicio"] = st.text_input("Repetições por exercício:", value=metodo["reps_por_exercicio"], key=f"{prefixo}_reps")
        config["descanso"] = st.text_input("Descanso entre trisets:", value=metodo["descanso_entre_trisets"], key=f"{prefixo}_descanso")
        config["tipo"] = "triset"
    
    elif metodo["tipo"] == "giantset":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de giantsets:", min_value=1, max_value=4, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["reps_por_exercicio"] = st.text_input("Repetições por exercício:", value=metodo["reps_por_exercicio"], key=f"{prefixo}_reps")
        config["descanso"] = st.text_input("Descanso entre giantsets:", value=metodo["descanso_entre_giantsets"], key=f"{prefixo}_descanso")
        config["tipo"] = "giantset"
    
    elif metodo["tipo"] == "restpause":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de séries:", min_value=1, max_value=4, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["pausas_por_serie"] = st.number_input("Pausas por série:", min_value=1, max_value=4, value=metodo["pausas_por_serie"], key=f"{prefixo}_pausas")
        config["reps_primeiro_set"] = st.text_input("Repetições no primeiro set:", value=metodo["reps_primeiro_set"], key=f"{prefixo}_reps_ini")
        config["reps_pos_pausa"] = st.text_input("Repetições após cada pausa:", value=metodo["reps_pos_pausa"], key=f"{prefixo}_reps_pausa")
        config["tipo"] = "restpause"
    
    elif metodo["tipo"] == "negativa":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de séries:", min_value=1, max_value=6, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["reps"] = st.text_input("Repetições:", value=metodo["reps_padrao"], key=f"{prefixo}_reps")
        config["tempo_excentrico"] = st.text_input("Tempo da fase excêntrica:", value=metodo["tempo_excentrico"], key=f"{prefixo}_tempo")
        config["tipo"] = "negativa"
    
    elif metodo["tipo"] == "isometrico":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de séries:", min_value=1, max_value=6, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["tempo"] = st.text_input("Tempo de contração:", value=metodo["tempo_segundos"], key=f"{prefixo}_tempo")
        config["tipo"] = "isometrico"
    
    elif metodo["tipo"] == "pre_exaustao":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de séries:", min_value=1, max_value=5, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["reps_isolador"] = st.text_input("Repetições (exercício isolador):", value=metodo["reps_isolador"], key=f"{prefixo}_reps_iso")
        config["reps_composto"] = st.text_input("Repetições (exercício composto):", value=metodo["reps_composto"], key=f"{prefixo}_reps_comp")
        config["tipo"] = "pre_exaustao"
    
    elif metodo["tipo"] == "cluster":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de séries:", min_value=1, max_value=5, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["clusters_por_serie"] = st.number_input("Clusters por série:", min_value=2, max_value=6, value=metodo["clusters_por_serie"], key=f"{prefixo}_clusters")
        config["reps_por_cluster"] = st.text_input("Repetições por cluster:", value=metodo["reps_por_cluster"], key=f"{prefixo}_reps_cluster")
        config["pausa_entre_clusters"] = st.text_input("Pausa entre clusters:", value=metodo["pausa_entre_clusters"], key=f"{prefixo}_pausa")
        config["tipo"] = "cluster"
    
    elif metodo["tipo"] == "amrap":
        config["tempo"] = st.number_input("Duração (minutos):", min_value=3, max_value=30, value=metodo["tempo_minutos"], key=f"{prefixo}_tempo")
        config["tipo"] = "amrap"
    
    elif metodo["tipo"] == "emom":
        col1, col2 = st.columns(2)
        with col1:
            config["duracao"] = st.number_input("Duração (minutos):", min_value=5, max_value=30, value=metodo["duracao_minutos"], key=f"{prefixo}_duracao")
        with col2:
            config["reps_por_minuto"] = st.text_input("Repetições por minuto:", value=metodo["reps_por_minuto"], key=f"{prefixo}_reps")
        config["tipo"] = "emom"
    
    elif metodo["tipo"] == "circuito":
        col1, col2 = st.columns(2)
        with col1:
            config["series"] = st.number_input("Número de rodadas:", min_value=1, max_value=6, value=metodo["series_padrao"], key=f"{prefixo}_series")
        with col2:
            config["reps_por_exercicio"] = st.text_input("Repetições por exercício:", value=metodo["reps_por_exercicio"], key=f"{prefixo}_reps")
        config["exercicios_por_circuito"] = st.number_input("Número de exercícios por circuito:", min_value=4, max_value=12, value=8, key=f"{prefixo}_num_ex")
        config["descanso"] = st.text_input("Descanso entre rodadas:", value=metodo["descanso_entre_rodadas"], key=f"{prefixo}_descanso")
        config["tipo"] = "circuito"
    
    return config


def formatar_exercicio_para_exibicao(nome_exercicio, config_metodo, series, reps, intervalo, carga_adicional=""):
    """Formata a linha do exercício baseado no método de treino"""
    metodo_tipo = config_metodo.get("tipo", "fixo")
    
    if metodo_tipo == "fixo":
        return f"{nome_exercicio} — {series}×{reps} | intervalo: {intervalo}"
    
    elif metodo_tipo == "progressivo":
        reps_str = " → ".join(config_metodo.get("reps_por_serie", []))
        carga_str = " → ".join(config_metodo.get("carga_por_serie", []))
        return f"{nome_exercicio} — {series} séries | reps: {reps_str} | carga: {carga_str} | intervalo: {intervalo}"
    
    elif metodo_tipo == "drop":
        return f"{nome_exercicio} — {series} série(s) com {config_metodo.get('drops_por_serie', 3)} drops | reps: {config_metodo.get('reps_iniciais', 'falha')} | redução: {config_metodo.get('reducao_carga', '20-30%')}"
    
    elif metodo_tipo == "superset":
        return f"{nome_exercicio} (em superset com próximo) — {series}×{reps} | descanso: {config_metodo.get('descanso', intervalo)}"
    
    elif metodo_tipo == "triset":
        return f"{nome_exercicio} (em triset com próximos 2) — {series}×{reps} | descanso: {config_metodo.get('descanso', intervalo)}"
    
    elif metodo_tipo == "giantset":
        return f"{nome_exercicio} (em giantset) — {series}×{reps} | descanso: {config_metodo.get('descanso', intervalo)}"
    
    elif metodo_tipo == "restpause":
        return f"{nome_exercicio} — {series} série(s) | {config_metodo.get('pausas_por_serie', 2)} pausas | primeiro set: {config_metodo.get('reps_primeiro_set', 'falha')} | após pausa: {config_metodo.get('reps_pos_pausa', '2-5')} reps"
    
    elif metodo_tipo == "negativa":
        return f"{nome_exercicio} — {series}×{reps} | fase excêntrica: {config_metodo.get('tempo_excentrico', '4-6s')} | intervalo: {intervalo}"
    
    elif metodo_tipo == "isometrico":
        return f"{nome_exercicio} — {series}×{config_metodo.get('tempo', '15-30s')} de contração isométrica | intervalo: {intervalo}"
    
    elif metodo_tipo == "pre_exaustao":
        return f"{nome_exercicio} — {series} séries | isolador: {config_metodo.get('reps_isolador', '12-15')} reps | composto: {config_metodo.get('reps_composto', '8-10')} reps"
    
    elif metodo_tipo == "cluster":
        return f"{nome_exercicio} — {series} séries | {config_metodo.get('clusters_por_serie', 3)} clusters de {config_metodo.get('reps_por_cluster', '2-4')} reps | pausa: {config_metodo.get('pausa_entre_clusters', '10-15s')}"
    
    elif metodo_tipo == "amrap":
        return f"{nome_exercicio} — AMRAP por {config_metodo.get('tempo', 10)} minutos"
    
    elif metodo_tipo == "emom":
        return f"{nome_exercicio} — EMOM por {config_metodo.get('duracao', 10)} min | {config_metodo.get('reps_por_minuto', '5-10')} reps/min"
    
    elif metodo_tipo == "circuito":
        return f"{nome_exercicio} (circuito com {config_metodo.get('exercicios_por_circuito', 8)} exercícios) — {series} rodadas | {reps} reps/exercício | descanso: {config_metodo.get('descanso', '60-90s')}"
    
    else:
        return f"{nome_exercicio} — {series}×{reps} | intervalo: {intervalo}"

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO AUXILIAR PARA NORMALIZAR TEXTO
# ══════════════════════════════════════════════════════════════════════════════
def normalizar_texto(texto):
    """Remove acentos e caracteres especiais para comparação"""
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO AUXILIAR PARA BUSCAR SUGESTÃO INTELIGENTE
# ══════════════════════════════════════════════════════════════════════════════
def buscar_sugestao_inteligente(categoria, atividade, nivel, frequencia):
    """
    Busca a sugestão mais adequada respeitando:
    1. Atividade específica + nível + frequência exata
    2. Atividade específica + nível + frequência próxima
    3. Categoria + nível + frequência exata (sem cair p/ outra categoria!)
    4. Categoria + nível diferente (mais próximo, nunca muda de categoria)
    """
    freq_map   = {"1-2x": "3x", "3x": "3x", "4-5x": "4-5x", "6-7x": "6-7x"}
    freq_chave = freq_map.get(frequencia, "3x")

    _niveis_ord = ["Atleta", "Avançado", "Intermediário", "Iniciante"]
    _freqs_ord  = ["6-7x", "4-5x", "3x"]
    idx_nivel   = _niveis_ord.index(nivel) if nivel in _niveis_ord else 3

    # 1. Atividade específica — nível exato — frequência exata
    s = SUGESTOES_TREINO.get((categoria, atividade, nivel, freq_chave))
    if s: return s

    # 2. Atividade específica — nível exato — outra frequência
    for f in _freqs_ord:
        s = SUGESTOES_TREINO.get((categoria, atividade, nivel, f))
        if s: return s

    # 3. Atividade específica — nível mais próximo
    for n in _niveis_ord[idx_nivel:]:
        for f in _freqs_ord:
            s = SUGESTOES_TREINO.get((categoria, atividade, n, f))
            if s: return s

    # 4. Categoria genérica — nível exato — frequência exata
    s = SUGESTOES_TREINO.get((categoria, nivel, freq_chave))
    if s: return s

    # 5. Categoria genérica — nível exato — outra frequência
    for f in _freqs_ord:
        s = SUGESTOES_TREINO.get((categoria, nivel, f))
        if s: return s

    # 6. Categoria genérica — nível mais próximo (NUNCA muda de categoria)
    for n in _niveis_ord[idx_nivel:]:
        for f in _freqs_ord:
            s = SUGESTOES_TREINO.get((categoria, n, f))
            if s: return s

    # 7. Nenhuma sugestão encontrada — retorna None (seção 5.5 entra em ação)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO AUXILIAR PARA APLICAR FILTROS DE RESTRIÇÃO
# ══════════════════════════════════════════════════════════════════════════════
def aplicar_filtro_restricoes(exercicios, termos_proibidos):
    """Marca exercícios como contraindicados baseado nos termos proibidos"""
    if not termos_proibidos:
        return exercicios
    
    exercicios_filtrados = []
    for ex in exercicios:
        ex_norm = normalizar_texto(ex)
        proibido = False
        motivo = None
        
        for termo, cond, obs in termos_proibidos:
            if termo in ex_norm:
                proibido = True
                motivo = f"{cond} — {obs}"
                break
        
        exercicios_filtrados.append({
            "texto": ex,
            "proibido": proibido,
            "motivo": motivo
        })
    
    return exercicios_filtrados


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO AUXILIAR PARA COLETAR TERMOS CONTRAINDICADOS
# ══════════════════════════════════════════════════════════════════════════════
def coletar_termos_proibidos(condicoes, lesoes):
    """Coleta todos os termos contraindicados das condições e lesões"""
    termos_proibidos = []
    
    # Processa condições de saúde
    for cond in condicoes:
        if cond in RESTRICOES:
            _, contraindicados, obs = RESTRICOES[cond]
            for c in contraindicados:
                termo_norm = normalizar_texto(c)
                termos_proibidos.append((termo_norm, cond, obs))
    
    # Processa lesões
    for lesao in lesoes:
        if lesao in RESTRICOES_LESOES:
            _, contraindicados, obs = RESTRICOES_LESOES[lesao]
            for c in contraindicados:
                termo_norm = normalizar_texto(c)
                termos_proibidos.append((termo_norm, lesao, obs))
    
    return termos_proibidos


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
def tela_treino_fisico(peso_kg=0.0, dados_paciente=None):
    if dados_paciente is None:
        dados_paciente = {}

    st.markdown("---")
    st.markdown("## 🏋️ Monte Seu Treino")

    # ── AVISO DE SEGURANÇA ───────────────────────────────────────────────────
    with st.expander("⚠️ Avisos de Segurança e Orientações Importantes — LEIA ANTES DE COMEÇAR", expanded=False):
        st.markdown(AVISO_SEGURANCA)
        col_links1, col_links2 = st.columns(2)
        with col_links1:
            st.link_button(
                "🔍 Consultar profissional no CREF-RJ",
                "https://cref-rj.implanta.net.br/servicosOnline/Publico/ConsultaInscritos/"
            )
        with col_links2:
            st.link_button(
                "🚨 Fazer denúncia ao CREF-RJ",
                "https://cref-rj.implanta.net.br/servicosOnline/Publico/Denuncias/"
            )
        st.caption("Links válidos para o CREF-RJ. Para outros estados, acesse o site do CREF do seu estado.")
        
        # Exemplo de cálculo de FC baseado na idade
        idade_exemplo = st.number_input("Digite sua idade para ver exemplo de zonas de FC:", min_value=15, max_value=100, value=30, key="fc_idade_exemplo")
        fcm = 220 - idade_exemplo
        st.info(f"💡 **Para {idade_exemplo} anos:** Frequência Cardíaca Máxima = **{fcm} bpm**\n\n"
                f"- Zona Leve (60-70%): **{fcm*0.6:.0f} - {fcm*0.7:.0f} bpm**\n"
                f"- Zona Moderada (70-80%): **{fcm*0.7:.0f} - {fcm*0.8:.0f} bpm**\n"
                f"- Zona Intensa (80-90%): **{fcm*0.8:.0f} - {fcm*0.9:.0f} bpm**")

    # ── 5.1 ANAMNESE ─────────────────────────────────────────────────────────
    with st.expander("📋 5.1 — Anamnese Física", expanded=True):

        # Dados do aluno/paciente
        st.markdown("**👤 Dados do Aluno / Paciente**")
        nome_pac = dados_paciente.get("nome", "")
        col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
        with col_p1:
            nome_aluno = st.text_input("Nome completo:", value=nome_pac, key="treino_nome_aluno")
        with col_p2:
            idade_aluno = st.number_input("Idade:", min_value=5, max_value=110, value=25, step=1, key="treino_idade_aluno")
        with col_p3:
            sexo_aluno = st.selectbox("Sexo biológico:", ["Masculino", "Feminino"], key="treino_sexo_aluno")
        
        # NOVO: Frequência Cardíaca de Repouso
        st.markdown("**❤️ Frequência Cardíaca**")
        col_fc1, col_fc2 = st.columns(2)
        with col_fc1:
            fc_repouso = st.number_input("Frequência Cardíaca em Repouso (bpm):",
                                         min_value=40, max_value=150, value=70, step=1,
                                         key="treino_fc_repouso",
                                         help="Meça ao acordar, ainda deitado, antes de levantar. Valor normal: 60-100 bpm.")
        with col_fc2:
            if idade_aluno > 0:
                fcm_estimada = 220 - idade_aluno
                st.metric("FC Máxima Estimada", f"{fcm_estimada} bpm", 
                         help="Fórmula: 220 - idade. Para indivíduos treinados, use a fórmula de Karvonen.")

        st.markdown("---")
        st.markdown("**🏅 Dados do Profissional / Local**")
        col_i1, col_i2, col_i3 = st.columns([2, 1.2, 2])
        with col_i1:
            nome_instrutor = st.text_input("Nome do instrutor / professor:", key="treino_instrutor",
                                           placeholder="Nome completo (opcional)")
        with col_i2:
            cref = st.text_input("CREF (opcional):", key="treino_cref",
                                 placeholder="Ex: 012345-G/SP")
        with col_i3:
            local_treino = st.text_input("Academia / Clube / Praça:", key="treino_local",
                                         placeholder="Nome do local de prática")

        st.markdown("---")
        st.markdown("**🎯 Perfil de Treino**")
        col1, col2 = st.columns(2)
        with col1:
            nivel = st.selectbox("Nível de condicionamento:",
                ["Iniciante", "Intermediário", "Avançado", "Atleta"], key="treino_nivel")
            frequencia = st.selectbox("Frequência semanal:",
                ["1-2x", "3x", "4-5x", "6-7x"], key="treino_freq")
            objetivo = st.selectbox("Objetivo principal:",
                ["Perda de gordura", "Ganho de massa muscular",
                 "Condicionamento físico", "Saúde geral / Qualidade de vida",
                 "Reabilitação / Retorno ao esporte"], key="treino_obj")
        with col2:
            condicoes = st.multiselect("Condições de saúde:",
                CONDICOES_SAUDE, default=["Nenhuma"], key="treino_condicoes")
            liberacao = st.radio("Liberação médica:",
                ["Sim", "Não", "Em andamento"], horizontal=True, key="treino_liberacao")
            exames = st.radio("Exames cardíacos em dia:",
                ["Sim", "Não"], horizontal=True, key="treino_exames")

        # Campo de lesões com sugestões
        st.markdown("**🩺 Lesões atuais ou histórico relevante**")
        lesoes_selecionadas = st.multiselect(
            "Selecione lesões existentes:",
            list(RESTRICOES_LESOES.keys()) + ["Outra lesão (especifique abaixo)"],
            key="treino_lesoes_select"
        )
        
        lesoes_outra = ""
        if "Outra lesão (especifique abaixo)" in lesoes_selecionadas:
            lesoes_outra = st.text_input("Especifique a lesão:",
                                        placeholder="Ex: Fratura de rádio distal, Tendinite de Aquiles...",
                                        key="treino_lesoes_outra")
            # Remove o marcador "Outra lesão" e adiciona o texto específico
            lesoes_lista = [l for l in lesoes_selecionadas if l != "Outra lesão (especifique abaixo)"]
            if lesoes_outra:
                lesoes_lista.append(lesoes_outra)
        else:
            lesoes_lista = lesoes_selecionadas.copy()

    # ── Alertas de condições e lesões (UNIFICADOS) ───────────────────────────
    condicoes_ativas = [c for c in condicoes if c != "Nenhuma"]
    lesoes_ativas = lesoes_lista
    
    # Exibe alertas para condições de saúde
    if condicoes_ativas:
        for cond in condicoes_ativas:
            if cond in RESTRICOES:
                indicado, contraindicado, obs = RESTRICOES[cond]
                st.warning(f"**{cond}** — {obs}")
                c1, c2 = st.columns(2)
                if indicado:
                    c1.success("✅ **Indicado:** " + " | ".join(indicado))
                if contraindicado:
                    c2.error("❌ **Contraindicado:** " + " | ".join(contraindicado))
    
    # Exibe alertas para lesões
    if lesoes_ativas:
        for lesao in lesoes_ativas:
            # Procura primeiro no dicionário de lesões
            if lesao in RESTRICOES_LESOES:
                indicado, contraindicado, obs = RESTRICOES_LESOES[lesao]
                st.warning(f"**{lesao}** — {obs}")
                c1, c2 = st.columns(2)
                if indicado:
                    c1.success("✅ **Indicado:** " + " | ".join(indicado))
                if contraindicado:
                    c2.error("❌ **Contraindicado:** " + " | ".join(contraindicado))
            # Se não encontrou mas tem "lesão" no texto, busca aproximada
            else:
                # Tenta encontrar chave similar
                encontrado = False
                for key in RESTRICOES_LESOES.keys():
                    if normalizar_texto(lesao) in normalizar_texto(key):
                        indicado, contraindicado, obs = RESTRICOES_LESOES[key]
                        st.warning(f"**{lesao}** (similar a {key}) — {obs}")
                        c1, c2 = st.columns(2)
                        if indicado:
                            c1.success("✅ **Indicado:** " + " | ".join(indicado))
                        if contraindicado:
                            c2.error("❌ **Contraindicado:** " + " | ".join(contraindicado))
                        encontrado = True
                        break
                if not encontrado:
                    st.info(f"**{lesao}** — ℹ️ Informe esta condição ao profissional de Educação Física para adaptações necessárias.")

    # Alertas críticos
    if "Cardiopatia" in condicoes_ativas or "Pós-operatório (< 6 meses)" in condicoes_ativas:
        st.error("🚨 **ATENÇÃO:** Esta condição requer laudo médico por escrito antes de iniciar qualquer atividade física.")
    
    if fc_repouso > 100:
        st.warning("⚠️ **Frequência cardíaca de repouso elevada (>100 bpm).** Consulte um médico antes de iniciar atividades físicas.")
    elif fc_repouso < 60 and nivel != "Atleta":
        st.info("ℹ️ **Frequência cardíaca de repouso baixa (<60 bpm).** Pode ser indicativo de bom condicionamento, mas informe-se com um médico se houver sintomas.")

    # ── 5.2 MODALIDADE ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🏊 5.2 — Modalidade e Atividade")

    categoria = st.selectbox("Categoria:", list(TABELA_MET.keys()), key="treino_categoria")

    # Referência da modalidade
    if categoria in REFERENCIAS_MODALIDADE:
        st.info(f"ℹ️ {REFERENCIAS_MODALIDADE[categoria]}")

    atividade = st.selectbox("Atividade:", list(TABELA_MET[categoria].keys()), key="treino_atividade")
    met_val   = TABELA_MET[categoria][atividade]
    st.caption(f"MET desta atividade: **{met_val}** — Compendium of Physical Activities (Ainsworth et al., 2011)")

    # ── 5.3 CÁLCULO MET ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔥 5.3 — Estimativa de Calorias Queimadas")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        peso_treino = st.number_input("⚖️ Peso (kg):",
            min_value=10.0, max_value=300.0,
            value=float(peso_kg) if peso_kg and peso_kg > 0 else 70.0,
            step=0.5, key="treino_peso")
    with col_b:
        duracao_min = st.number_input("⏱️ Duração (minutos):",
            min_value=5, max_value=300, value=60, step=5, key="treino_duracao")
    with col_c:
        sessoes_semana = st.number_input("📅 Sessões/semana:",
            min_value=1, max_value=7, value=3, step=1, key="treino_sessoes")

    duracao_h   = duracao_min / 60
    kcal_sessao = round(met_val * peso_treino * duracao_h, 1)
    kcal_semana = round(kcal_sessao * sessoes_semana, 1)
    kcal_mes    = round(kcal_semana * 4.33, 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 kcal / sessão", f"{kcal_sessao:.0f} kcal")
    col2.metric("📅 kcal / semana", f"{kcal_semana:.0f} kcal")
    col3.metric("📆 kcal / mês",    f"{kcal_mes:.0f} kcal")
    st.caption(f"Fórmula MET: {met_val} × {peso_treino}kg × {duracao_h:.2f}h = {kcal_sessao} kcal/sessão")

    # ── 5.4 SUGESTÃO AUTOMÁTICA (INTELIGENTE) ─────────────────────────────────
    st.markdown("---")
    st.markdown("### 📋 5.4 — Sugestão de Treino Automática")

    # Coleta termos proibidos para filtro
    termos_proibidos = coletar_termos_proibidos(condicoes_ativas, lesoes_ativas)
    
    # Busca sugestão inteligente
    sugestao = buscar_sugestao_inteligente(categoria, atividade, nivel, frequencia)

    if sugestao:
        st.success(f"**{sugestao['nome']}**")
        st.write(sugestao["descricao"])

        for dia_t, exs in sugestao["dias"].items():
            with st.expander(f"📅 {dia_t}"):
                if not exs:
                    st.write("Descanso ativo ou livre")
                else:
                    for ex in exs:
                        # Aplica filtro de restrições
                        ex_norm = normalizar_texto(ex)
                        proibido = False
                        motivo = None
                        
                        for termo, cond, obs in termos_proibidos:
                            if termo in ex_norm:
                                proibido = True
                                motivo = f"{cond} — {obs}"
                                break
                        
                        if proibido:
                            st.markdown(
                                f"~~• {ex}~~ &nbsp; ⚠️ *Contraindicado: {motivo}*",
                                unsafe_allow_html=True
                            )
                        else:
                            st.write(f"• {ex}")
    else:
        st.info(f"Sugestão automática não disponível para **{categoria} / {atividade} / {nivel} / {frequencia}**. Use a seção 5.5 abaixo para montar seu treino.")

    # ── 5.5 MONTAGEM LIVRE DE TREINO (REFATORADO COM MÉTODOS) ────────────────────
    st.markdown("---")
    st.markdown("### 🛠️ 5.5 — Monte Seu Próprio Treino (Musculação)")
    st.caption("Escolha os grupos musculares, exercícios e método. Configurações dinâmicas para cada tipo de treino.")

    # Inicializa session state para os dias de treino
    if "treino_personalizado_dias" not in st.session_state:
        st.session_state.treino_personalizado_dias = []

    # Botões para gerenciar dias
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("➕ Adicionar Dia de Treino", key="add_dia_btn"):
            novo_num = len(st.session_state.treino_personalizado_dias) + 1
            st.session_state.treino_personalizado_dias.append({
                "nome": f"Dia {novo_num}",
                "exercicios": [],
                "metodo": "Séries convencionais",
                "config_metodo": {}
            })
    with col_btn2:
        if st.button("📋 Duplicar Último Dia", key="duplicate_dia_btn") and st.session_state.treino_personalizado_dias:
            ultimo_dia = st.session_state.treino_personalizado_dias[-1].copy()
            ultimo_dia["nome"] = f"{ultimo_dia['nome']} (cópia)"
            st.session_state.treino_personalizado_dias.append(ultimo_dia)
    with col_btn3:
        if st.button("🗑️ Remover Último Dia", key="remove_dia_btn") and st.session_state.treino_personalizado_dias:
            st.session_state.treino_personalizado_dias.pop()

    # Configurações globais vs específicas
    col_global, _ = st.columns([1, 2])
    with col_global:
        usar_config_global = st.checkbox("Usar mesma configuração para todos os dias", value=True, key="usar_config_global")

    # Método global (se aplicável)
    metodo_global = "Séries convencionais"
    config_global = {}

    if usar_config_global:
        metodo_global = st.selectbox(
            "Método de treino (para todos os dias):",
            list(METODOS_TREINO.keys()),
            key="treino_metodo_global"
        )
        st.caption(f"📖 **{metodo_global}:** {METODOS_TREINO[metodo_global]['descricao']}")
        
        # Renderiza configurações específicas do método global
        with st.expander("⚙️ Configurações do método de treino", expanded=True):
            config_global = renderizar_configuracoes_metodo(metodo_global, "global")

    # Loop para cada dia de treino
    for i, dia in enumerate(st.session_state.treino_personalizado_dias):
        with st.expander(f"📅 {dia['nome']}", expanded=(i == len(st.session_state.treino_personalizado_dias)-1)):
            # Editar nome do dia
            novo_nome = st.text_input("Nome do dia:", value=dia['nome'], key=f"nome_dia_{i}")
            st.session_state.treino_personalizado_dias[i]['nome'] = novo_nome
            
            # Seleção de método (se não usar global)
            if not usar_config_global:
                metodo_dia = st.selectbox(
                    "Método de treino para este dia:",
                    list(METODOS_TREINO.keys()),
                    index=list(METODOS_TREINO.keys()).index(dia.get("metodo", "Séries convencionais")),
                    key=f"metodo_dia_{i}"
                )
                st.caption(f"📖 {METODOS_TREINO[metodo_dia]['descricao']}")
                st.session_state.treino_personalizado_dias[i]['metodo'] = metodo_dia
                
                with st.expander("⚙️ Configurações do método", expanded=True):
                    config_dia = renderizar_configuracoes_metodo(metodo_dia, f"dia_{i}")
                    st.session_state.treino_personalizado_dias[i]['config_metodo'] = config_dia
            else:
                metodo_dia = metodo_global
                config_dia = config_global
                st.session_state.treino_personalizado_dias[i]['metodo'] = metodo_dia
                st.session_state.treino_personalizado_dias[i]['config_metodo'] = config_dia
                st.info(f"📖 Usando método global: **{metodo_dia}**")
            
            # Selecionar grupos musculares para este dia
            grupos_dia = st.multiselect(
                "Grupos musculares desta sessão:",
                list(BANCO_EXERCICIOS.keys()),
                key=f"grupos_dia_{i}"
            )
            
            # Para cada grupo selecionado, mostrar exercícios
            exercicios_dia = []
            for grupo in grupos_dia:
                st.markdown(f"**{grupo}**")
                
                # Filtra exercícios contraindicados
                opcoes_exercicios = []
                for ex in BANCO_EXERCICIOS[grupo]:
                    ex_norm = normalizar_texto(ex)
                    proibido = False
                    motivo = None
                    
                    for termo, cond, obs in termos_proibidos:
                        if termo in ex_norm:
                            proibido = True
                            motivo = f"({cond})"
                            break
                    
                    if proibido:
                        opcoes_exercicios.append(f"❌ {ex} {motivo}")
                    else:
                        opcoes_exercicios.append(f"✅ {ex}")
                
                exs_sel = st.multiselect(
                    f"Exercícios para {grupo}:",
                    opcoes_exercicios,
                    key=f"exs_dia_{i}_{grupo}"
                )
                
                # Limpa os marcadores ✅ e ❌ para armazenar apenas o nome do exercício
                for ex in exs_sel:
                    ex_limpo = ex.replace("✅ ", "").replace("❌ ", "")
                    if " (" in ex_limpo:
                        ex_limpo = ex_limpo.split(" (")[0]
                    exercicios_dia.append(ex_limpo)
            
            # Intervalo entre séries/exercícios
            intervalo = st.text_input("Intervalo de descanso:", value="60s", key=f"intervalo_dia_{i}",
                                    help="Tempo de descanso entre séries ou entre exercícios (quando aplicável)")
            
            # Armazena os exercícios com suas configurações
            st.session_state.treino_personalizado_dias[i]["exercicios"] = [
                {
                    "nome": ex,
                    "metodo": metodo_dia,
                    "config_metodo": config_dia,
                    "intervalo": intervalo
                }
                for ex in exercicios_dia
            ]
            
            # Exibe prévia formatada dos exercícios do dia
            if st.session_state.treino_personalizado_dias[i]["exercicios"]:
                st.markdown("**📋 Prévia do treino formatada:**")
                for ex in st.session_state.treino_personalizado_dias[i]["exercicios"]:
                    linha_formatada = formatar_exercicio_para_exibicao(
                        ex["nome"],
                        ex["config_metodo"],
                        ex["config_metodo"].get("series", 3),
                        ex["config_metodo"].get("reps", "12"),
                        ex["intervalo"]
                    )
                    st.markdown(f"• {linha_formatada}")
                
                # Botão para remover todos exercícios do dia
                if st.button(f"🗑️ Limpar todos exercícios do {dia['nome']}", key=f"limpar_dia_{i}"):
                    st.session_state.treino_personalizado_dias[i]["exercicios"] = []
                    st.rerun()

    # ── 5.6 BALANÇO ENERGÉTICO ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### ⚖️ 5.6 — Balanço Energético Integrado")

    get_atual = st.session_state.get("get_calculado", 0)
    if get_atual > 0:
        get_com_treino = round(get_atual + kcal_semana / 7)
        col1, col2, col3 = st.columns(3)
        col1.metric("GET sem treino",  f"{get_atual:.0f} kcal/dia")
        col2.metric("Gasto c/ treino", f"+{kcal_semana/7:.0f} kcal/dia")
        col3.metric("GET total",       f"{get_com_treino:.0f} kcal/dia",
                    delta=f"+{kcal_semana/7:.0f} kcal")
        st.caption("Média diária do gasto extra das sessões de atividade física somada ao GET de repouso.")
    else:
        st.info("ℹ️ Preencha o perfil biológico na sidebar para ver o balanço energético completo.")

    # ── RELATÓRIO ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📄 Gerar Relatório de Treino")

    if st.button("📄 Gerar Relatório HTML", key="btn_relatorio_treino", use_container_width=True):
        # 1. Constrói dicionário de treino mantendo TODOS os dados dos exercícios
        treino_para_relatorio = {}
        if "treino_personalizado_dias" in st.session_state and st.session_state.treino_personalizado_dias:
            for dia in st.session_state.treino_personalizado_dias:
                nome_dia = dia.get("nome", "Dia sem nome")
                exercicios = dia.get("exercicios", [])
                # Inclui apenas se houver exercícios
                if exercicios:
                    treino_para_relatorio[nome_dia] = exercicios

        # 2. Define valores padrão para os parâmetros do método (evita unknown-name)
        if usar_config_global:
            metodo_final = metodo_global
            config_final = config_global
            series_final = config_global.get("series", 3)
            reps_final = config_global.get("reps", "12")
            intervalo_final = "60s"
        else:
            if st.session_state.treino_personalizado_dias:
                primeiro_dia = st.session_state.treino_personalizado_dias[0]
                metodo_final = primeiro_dia.get("metodo", "Séries convencionais")
                config_final = primeiro_dia.get("config_metodo", {})
                series_final = config_final.get("series", 3)
                reps_final = config_final.get("reps", "12")
                # Busca intervalo do primeiro exercício do primeiro dia, se houver
                exercicios_primeiro = primeiro_dia.get("exercicios", [])
                if exercicios_primeiro and isinstance(exercicios_primeiro[0], dict):
                    intervalo_final = exercicios_primeiro[0].get("intervalo", "60s")
                else:
                    intervalo_final = "60s"
            else:
                metodo_final = "Séries convencionais"
                config_final = {}
                series_final = 3
                reps_final = "12"
                intervalo_final = "60s"

        # 3. Gera o HTML do relatório
        html = _gerar_relatorio_html(
            nome_aluno=nome_aluno,
            idade_aluno=idade_aluno,
            sexo_aluno=sexo_aluno,
            nome_instrutor=nome_instrutor,
            cref=cref,
            local_treino=local_treino,
            nivel=nivel,
            frequencia=frequencia,
            objetivo=objetivo,
            condicoes=condicoes_ativas,
            liberacao=liberacao,
            exames=exames,
            lesoes=lesoes_ativas,
            lesoes_outra=lesoes_outra,
            fc_repouso=fc_repouso,
            fcm_estimada=220 - idade_aluno if idade_aluno > 0 else 0,
            categoria=categoria,
            atividade=atividade,
            met_val=met_val,
            peso_treino=peso_treino,
            duracao_min=duracao_min,
            sessoes_semana=sessoes_semana,
            kcal_sessao=kcal_sessao,
            kcal_semana=kcal_semana,
            kcal_mes=kcal_mes,
            sugestao=sugestao,
            treino_montado=treino_para_relatorio,
            metodo_sel=metodo_final,
            num_series=series_final,
            num_reps=reps_final,
            intervalo=intervalo_final,
            get_atual=get_atual,
        )

        # 4. Disponibiliza download
        nome_arq = f"treino_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        b64 = base64.b64encode(html.encode("utf-8")).decode()
        st.markdown(
            f'<a href="data:text/html;base64,{b64}" download="{nome_arq}">⬇️ Baixar {nome_arq}</a>',
            unsafe_allow_html=True
        )
        st.success("✅ Relatório gerado!")


# ══════════════════════════════════════════════════════════════════════════════
# GERADOR HTML (ATUALIZADO COM FREQUÊNCIA CARDÍACA)
# ══════════════════════════════════════════════════════════════════════════════
def _gerar_relatorio_html(**kw):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    sugestao = kw.get("sugestao")
    treino_montado_dict = kw.get("treino_montado", {})
    condicoes = kw.get("condicoes", [])
    lesoes = kw.get("lesoes", [])
    lesoes_outra = kw.get("lesoes_outra", "")
    get_atual = kw.get("get_atual", 0)
    fc_repouso = kw.get("fc_repouso", 0)
    fcm_estimada = kw.get("fcm_estimada", 0)
    
    # Coleta termos proibidos (igual à interface)
    termos_proibidos = []
    for cond in condicoes:
        if cond in RESTRICOES:
            _, contraindicados, obs = RESTRICOES[cond]
            for c in contraindicados:
                termo_norm = normalizar_texto(c)
                termos_proibidos.append((termo_norm, cond, obs))
    for lesao in lesoes:
        if lesao in RESTRICOES_LESOES:
            _, contraindicados, obs = RESTRICOES_LESOES[lesao]
            for c in contraindicados:
                termo_norm = normalizar_texto(c)
                termos_proibidos.append((termo_norm, lesao, obs))
    
    # Junta condições e lesões para exibição
    todas_condicoes = condicoes.copy()
    if lesoes:
        todas_condicoes.extend(lesoes)
    if lesoes_outra:
        todas_condicoes.append(lesoes_outra)
    cond_html = ", ".join(todas_condicoes) if todas_condicoes else "Nenhuma"

    # Sugestão automática (já funcionando)
    sug_html = ""
    if sugestao:
        sug_html = f"<h3>{sugestao['nome']}</h3><p><em>{sugestao['descricao']}</em></p>"
        for dia, exs in sugestao["dias"].items():
            sug_html += f"<h4 style='color:#0f3460'>{dia}</h4><ul>"
            for ex in exs:
                ex_norm = normalizar_texto(ex)
                proibido = False
                motivo = ""
                for termo, cond, obs in termos_proibidos:
                    if termo in ex_norm:
                        proibido = True
                        motivo = f"{cond} — {obs}"
                        break
                if proibido:
                    sug_html += f"<li><del>{ex}</del> ⚠️ <em>Contraindicado: {motivo}</em></li>"
                else:
                    sug_html += f"<li>{ex}</li>"
            sug_html += "</ul>"

    # Treino personalizado com formatação detalhada (CORRIGIDO)
    montado_html = ""
    if treino_montado_dict:
        montado_html = f"""
        <h3>Treino Personalizado</h3>
        <p><strong>Método padrão:</strong> {kw.get('metodo_sel', 'Séries convencionais')}</p>
        <p><strong>Séries padrão:</strong> {kw.get('num_series', '3')} &nbsp;|&nbsp;
           <strong>Repetições padrão:</strong> {kw.get('num_reps', '12')} &nbsp;|&nbsp;
           <strong>Intervalo padrão:</strong> {kw.get('intervalo', '60s')}</p>
        <p><em>{METODOS_TREINO.get(kw.get('metodo_sel', 'Séries convencionais'), {}).get('descricao', '')}</em></p>
        """
        for dia, exs_data in treino_montado_dict.items():
            montado_html += f"<h4 style='color:#0f3460'>{dia}</h4><ul>"
            if exs_data and isinstance(exs_data, list):
                for ex in exs_data:
                    if isinstance(ex, dict):
                        nome = ex.get("nome", "")
                        intervalo = ex.get("intervalo", kw.get('intervalo', '60s'))
                        config_usuario = ex.get("config_metodo", {})
                        metodo = ex.get("metodo", kw.get('metodo_sel', 'Séries convencionais'))
                        
                        # Obtém definição do método
                        metodo_def = METODOS_TREINO.get(metodo, {})
                        if not metodo_def:
                            metodo_def = METODOS_TREINO.get("Séries convencionais", {})
                        
                        # Cria config baseada no método, sobrescrevendo com dados do usuário se existirem
                        config = {}
                        if metodo_def.get("tipo") == "progressivo":
                            config = {
                                "tipo": "progressivo",
                                "series": config_usuario.get("series") or metodo_def.get("series_padrao", 3),
                                "reps_por_serie": config_usuario.get("reps_por_serie") or metodo_def.get("reps_por_serie", []),
                                "carga_por_serie": config_usuario.get("carga_por_serie") or metodo_def.get("carga_por_serie", [])
                            }
                        elif metodo_def.get("tipo") == "drop":
                            config = {
                                "tipo": "drop",
                                "series": config_usuario.get("series") or metodo_def.get("series_padrao", 1),
                                "drops_por_serie": config_usuario.get("drops_por_serie") or metodo_def.get("drops_por_serie", 3),
                                "reps_iniciais": config_usuario.get("reps_iniciais") or metodo_def.get("reps_iniciais", "até a falha")
                            }
                        elif metodo_def.get("tipo") == "amrap":
                            config = {
                                "tipo": "amrap",
                                "tempo": config_usuario.get("tempo") or metodo_def.get("tempo_minutos", 10)
                            }
                        elif metodo_def.get("tipo") == "emom":
                            config = {
                                "tipo": "emom",
                                "duracao": config_usuario.get("duracao") or metodo_def.get("duracao_minutos", 10),
                                "reps_por_minuto": config_usuario.get("reps_por_minuto") or metodo_def.get("reps_por_minuto", "5-10")
                            }
                        elif metodo_def.get("tipo") == "circuito":
                            config = {
                                "tipo": "circuito",
                                "series": config_usuario.get("series") or metodo_def.get("series_padrao", 3),
                                "reps_por_exercicio": config_usuario.get("reps_por_exercicio") or metodo_def.get("reps_por_exercicio", "10-15"),
                                "exercicios_por_circuito": config_usuario.get("exercicios_por_circuito") or metodo_def.get("exercicios_por_circuito", "6-8")
                            }
                        else:
                            # Fixo, negativa, isometria, etc.
                            config = {
                                "tipo": metodo_def.get("tipo", "fixo"),
                                "series": config_usuario.get("series") or metodo_def.get("series_padrao", 3),
                                "reps": config_usuario.get("reps") or metodo_def.get("exemplo_reps", "12")
                            }
                        
                        # Aplica filtro de restrição
                        ex_norm = normalizar_texto(nome)
                        proibido = False
                        motivo = ""
                        for termo, cond, obs in termos_proibidos:
                            if termo in ex_norm:
                                proibido = True
                                motivo = f"{cond} — {obs}"
                                break
                        
                        # Formata a linha
                        if config.get("tipo") == "progressivo":
                            reps_str = " → ".join(config.get("reps_por_serie", []))
                            carga_str = " → ".join(config.get("carga_por_serie", []))
                            linha = f"{nome} — {config.get('series', 3)} séries | reps: {reps_str} | carga: {carga_str} | intervalo: {intervalo}"
                        elif config.get("tipo") == "drop":
                            linha = f"{nome} — {config.get('series', 1)} série(s) com {config.get('drops_por_serie', 3)} drops | reps: {config.get('reps_iniciais', 'falha')}"
                        elif config.get("tipo") == "superset":
                            linha = f"{nome} (em superset) — {config.get('series', 3)}×{config.get('reps_por_exercicio', '10-12')}"
                        elif config.get("tipo") == "amrap":
                            linha = f"{nome} — AMRAP por {config.get('tempo', 10)} minutos"
                        elif config.get("tipo") == "emom":
                            linha = f"{nome} — EMOM por {config.get('duracao', 10)} min | {config.get('reps_por_minuto', '5-10')} reps/min"
                        elif config.get("tipo") == "circuito":
                            linha = f"{nome} (circuito) — {config.get('series', 3)} rodadas | {config.get('reps_por_exercicio', '10-15')} reps/exercício"
                        else:
                            series = config.get('series', kw.get('num_series', '3'))
                            reps = config.get('reps', kw.get('num_reps', '12'))
                            linha = f"{nome} — {series}×{reps} | intervalo: {intervalo}"
                        
                        if proibido:
                            montado_html += f"<li><del>{linha}</del> ⚠️ <em>Contraindicado: {motivo}</em></li>"
                        else:
                            montado_html += f"<li>{linha}</li>"
                    else:
                        montado_html += f"<li>{ex}</li>"
            montado_html += "</ul>"

    # Alertas, balanço, frequência cardíaca e o restante do HTML (igual ao seu original, mantido)
    alertas_html = ""
    for cond in condicoes:
        if cond in RESTRICOES:
            _, _, obs = RESTRICOES[cond]
            alertas_html += f'<div class="alerta"><strong>{cond}:</strong> {obs}</div>'
    for lesao in lesoes:
        if lesao in RESTRICOES_LESOES:
            _, _, obs = RESTRICOES_LESOES[lesao]
            alertas_html += f'<div class="alerta"><strong>{lesao}:</strong> {obs}</div>'

    balanco_html = ""
    if get_atual > 0:
        kcal_semana = kw.get('kcal_semana', 0)
        sessoes_semana = kw.get('sessoes_semana', 0)
        get_com = round(get_atual + kcal_semana / 7) if kcal_semana > 0 else get_atual
        balanco_html = f"""
        <h2>⚖️ Balanço Energético</h2>
        <table>
          <tr><th>GET em repouso (sem treino)</th><td>{get_atual:.0f} kcal/dia</td></tr>
          <tr><th>Gasto médio c/ treino ({sessoes_semana}x/sem)</th>
              <td>+{kcal_semana/7:.0f} kcal/dia</td></tr>
          <tr><th>GET total estimado</th><td><strong>{get_com} kcal/dia</strong></td></tr>
        </table>
        """

    fc_html = ""
    if fc_repouso > 0 and fcm_estimada > 0:
        fc_html = f"""
        <h2>❤️ Frequência Cardíaca</h2>
        <table>
            <tr><th>FC de Repouso</th><td>{fc_repouso} bpm</td>
                <th>FC Máxima Estimada</th><td>{fcm_estimada} bpm</td></tr>
            <tr><th>Zona Leve (60-70%)</th><td colspan="3">{fcm_estimada*0.6:.0f} - {fcm_estimada*0.7:.0f} bpm</td></tr>
            <tr><th>Zona Moderada (70-80%)</th><td colspan="3">{fcm_estimada*0.7:.0f} - {fcm_estimada*0.8:.0f} bpm</td></tr>
            <tr><th>Zona Intensa (80-90%)</th><td colspan="3">{fcm_estimada*0.8:.0f} - {fcm_estimada*0.9:.0f} bpm</td></tr>
        </table>
        """

    # O restante do HTML (cabeçalho, corpo, rodapé) é igual ao seu original
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Plano de Treino — BioGestão 360</title>
<style>
  body{{font-family:Arial,sans-serif;max-width:960px;margin:40px auto;color:#1a1a2e;line-height:1.6}}
  h1{{color:#0f3460;border-bottom:3px solid #0f3460;padding-bottom:8px}}
  h2{{color:#16213e;border-left:5px solid #0f3460;padding-left:12px;margin-top:30px}}
  h3{{color:#0f3460}}
  h4{{color:#16213e;margin:10px 0 5px}}
  table{{width:100%;border-collapse:collapse;margin:15px 0}}
  th{{background:#0f3460;color:#fff;padding:10px;text-align:left}}
  td{{padding:8px 10px;border-bottom:1px solid #ddd}}
  tr:nth-child(even) td{{background:#f8f9fa}}
  .alerta{{background:#fff3cd;border-left:4px solid #ffc107;padding:10px;margin:8px 0;border-radius:4px}}
  .aviso-seg{{background:#ffeaea;border-left:4px solid #dc3545;padding:12px;margin:15px 0;border-radius:4px;font-size:13px}}
  .metric{{display:inline-block;background:#0f3460;color:#fff;border-radius:8px;
           padding:15px 25px;margin:8px;text-align:center;min-width:140px}}
  .metric span{{display:block;font-size:26px;font-weight:bold}}
  ul{{padding-left:20px}} li{{margin:3px 0}}
  footer{{margin-top:40px;color:#888;font-size:12px;text-align:center;border-top:1px solid #ddd;padding-top:15px}}
  .badge{{display:inline-block;background:#e8f4fd;border:1px solid #0f3460;border-radius:4px;
          padding:2px 8px;font-size:12px;color:#0f3460;margin:2px}}
</style>
</head>
<body>
<h1>🏋️ BioGestão 360 — Plano de Treino</h1>
<p>Gerado em: <strong>{now}</strong></p>

<h2>👤 Dados do Aluno / Paciente</h2>
<table>
  <tr><th>Nome</th><td>{kw.get('nome_aluno') or '—'}</td>
      <th>Idade</th><td>{kw.get('idade_aluno','—')} anos</td></tr>
  <tr><th>Sexo biológico</th><td>{kw.get('sexo_aluno','—')}</td>
      <th>Objetivo</th><td>{kw.get('objetivo','—')}</td></tr>
</table>

<h2>🏅 Profissional / Local</h2>
<table>
  <tr><th>Instrutor / Professor</th><td>{kw.get('nome_instrutor') or '—'}</td>
      <th>CREF</th><td>{kw.get('cref') or '—'}</td></tr>
  <tr><th>Local de prática</th><td colspan="3">{kw.get('local_treino') or '—'}</td></tr>
</table>

<h2>📋 Anamnese Física</h2>
<table>
  <tr><th>Nível</th><td>{kw.get('nivel','—')}</td>
      <th>Frequência</th><td>{kw.get('frequencia','—')}/semana</td></tr>
  <tr><th>Liberação médica</th><td>{kw.get('liberacao','—')}</td>
      <th>Exames cardíacos</th><td>{kw.get('exames','—')}</td></tr>
  <tr><th>Condições de saúde / Lesões</th><td colspan="3">{cond_html}</td></tr>
</table>

{f'<h2>⚠️ Alertas de Saúde</h2>{alertas_html}' if alertas_html else ''}
{fc_html}

<h2>🏊 Modalidade</h2>
<table>
  <tr><th>Categoria</th><td>{kw.get('categoria','—')}</td>
      <th>Atividade</th><td>{kw.get('atividade','—')}</td></tr>
  <tr><th>MET</th><td>{kw.get('met_val','—')}</td>
      <th>Duração/sessão</th><td>{kw.get('duracao_min','—')} min</td></tr>
  <tr><th>Sessões/semana</th><td>{kw.get('sessoes_semana','—')}</td>
      <th>Peso</th><td>{kw.get('peso_treino','—')} kg</td></tr>
</table>

<h2>🔥 Calorias Queimadas</h2>
<div>
  <div class="metric">🔥 Por sessão<span>{kw.get('kcal_sessao',0):.0f} kcal</span></div>
  <div class="metric">📅 Por semana<span>{kw.get('kcal_semana',0):.0f} kcal</span></div>
  <div class="metric">📆 Por mês<span>{kw.get('kcal_mes',0):.0f} kcal</span></div>
</div>
<p><small>Fórmula MET: {kw.get('met_val','—')} × {kw.get('peso_treino','—')}kg × {kw.get('duracao_min',0)/60:.2f}h = {kw.get('kcal_sessao',0):.1f} kcal/sessão</small></p>

{f'<h2>📋 Sugestão Automática de Treino</h2>{sug_html}' if sug_html else ''}
{f'<h2>🛠️ Treino Personalizado</h2>{montado_html}' if montado_html else ''}
{balanco_html}

<h2>⚠️ Avisos de Segurança</h2>
<div class="aviso-seg">
  <strong>Este documento é apenas um guia de planejamento e não substitui avaliação presencial.</strong><br>
  • Consulte médico antes de iniciar qualquer programa de exercícios.<br>
  • Exija CREF ativo do profissional responsável pelo seu treino.<br>
  • Para atividades aquáticas supervisionadas: verifique Curso de Socorrismo Aquático do profissional.<br>
  • Pare imediatamente se sentir dor no peito, falta de ar intensa, tontura ou dor articular aguda.<br>
  • Hidrate-se, realize aquecimento e resfriamento em toda sessão.<br>
  • Progressão gradual: nunca aumente carga ou volume mais de 10% por semana.<br>
  • Monitore sua frequência cardíaca durante o exercício, mantendo-a na zona alvo.
</div>

<footer>
  BioGestão 360 v5.0 | Plano de Treino gerado em {now}<br>
  Profissional responsável: {kw.get('nome_instrutor') or '—'} | CREF: {kw.get('cref') or '—'}<br>
  Este documento não substitui avaliação presencial de profissional de Educação Física habilitado (CREF).<br>
  Referência MET: Ainsworth BE et al. Compendium of Physical Activities. Med Sci Sports Exerc. 2011.
</footer>
</body></html>"""