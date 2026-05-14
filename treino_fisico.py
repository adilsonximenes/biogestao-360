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
# BANCO DE EXERCÍCIOS PARA MONTAGEM LIVRE (Seção 5.5)
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
    "Séries convencionais": "Número fixo de séries e repetições. Ex: 3×12 (3 séries de 12 repetições).",
    "Pirâmide crescente": "Aumenta a carga a cada série e diminui as repetições. Ex: 12→10→8 com carga 40→50→60kg.",
    "Pirâmide decrescente": "Diminui a carga a cada série e aumenta as repetições. Ex: 8→10→12 com carga 60→50→40kg.",
    "Drop set": "Ao falhar, reduz a carga imediatamente e continua sem descanso. Máxima intensidade.",
    "Super set": "Dois exercícios em sequência sem descanso — mesmo grupo muscular (intensidade) ou antagonistas (volume).",
    "Tri set": "Três exercícios em sequência sem descanso para o mesmo grupo muscular.",
    "Giant set": "Quatro ou mais exercícios em sequência sem descanso.",
    "Rest-pause": "Uma série até a falha, 10–20s de descanso, continua com mais repetições.",
    "Negativa acentuada": "Fase excêntrica lenta (4–6 segundos). Maior dano muscular e ganho de força.",
    "Isometria": "Contração sem movimento. Ex: segurar 3 segundos no ponto de maior tensão.",
    "Pré-exaustão": "Isolar o músculo principal antes do exercício composto. Ex: crucifixo antes do supino.",
    "Cluster set": "Série com micro-pausas de 10–15s entre grupos de repetições para manter a qualidade.",
    "AMRAP": "As Many Reps As Possible — máximo de repetições com boa forma em um tempo definido.",
    "EMOM": "Every Minute On the Minute — executa X repetições no início de cada minuto.",
    "Circuito": "Série de exercícios realizados em sequência com descanso apenas ao final da rodada.",
}

# ══════════════════════════════════════════════════════════════════════════════
# SUGESTÕES AUTOMÁTICAS
# ══════════════════════════════════════════════════════════════════════════════
SUGESTOES_TREINO = {
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
    ("🏋️ Academia / Musculação", "Iniciante", "4-5x"): {
        "nome": "Upper / Lower Split — Iniciante 4x",
        "descricao": "2 dias MMSS + 2 dias MMII. 4 séries × 10–12 repetições. Intervalo 60–90s.",
        "dias": {
            "Upper A — Empurrar + Puxar (Seg)": [
                "Supino reto (barra) — 4×10",
                "Remada curvada (barra) — 4×10",
                "Desenvolvimento (halteres) — 3×12",
                "Puxada frontal — 3×12",
                "Rosca direta — 3×12",
                "Tríceps pulley — 3×12",
            ],
            "Lower A — Quadríceps (Ter)": [
                "Agachamento livre — 4×10",
                "Leg press 45° — 4×12",
                "Cadeira extensora — 3×15",
                "Panturrilha em pé — 4×15",
                "Prancha — 3×40s",
            ],
            "Upper B (Qui)": [
                "Supino inclinado (halteres) — 4×10",
                "Remada unilateral — 4×10",
                "Elevação lateral — 4×15",
                "Barra fixa assistida — 3×8",
                "Rosca martelo — 3×12",
                "Dips (tríceps) assistido — 3×10",
            ],
            "Lower B — Posterior (Sex)": [
                "Stiff (halteres) — 4×10",
                "Cadeira flexora — 4×12",
                "Hip thrust — 4×12",
                "Avanço (lunge) — 3×10 cada perna",
                "Panturrilha sentado — 4×15",
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
    ("🏊 Aquáticas", "Iniciante", "3x"): {
        "nome": "Natação para Iniciantes — Adaptação ao Meio Aquático",
        "descricao": "Foco em técnica e adaptação. Crawl como nado principal. Progressão semanal.",
        "dias": {
            "Treino 1 (Seg)": [
                "Aquecimento: caminhada na piscina — 5 min",
                "Flutuação ventral e dorsal — 2×25m",
                "Pernada com prancha (crawl) — 4×25m",
                "Braçada assistida com pull buoy — 3×25m",
                "Resfriamento: costas relaxado — 2×25m",
            ],
            "Treino 2 (Qua)": [
                "Aquecimento — 100m livre",
                "Pernada sem prancha — 4×25m",
                "Respiração lateral bilateral — 4×25m",
                "Crawl completo — 4×50m c/ 30s descanso",
            ],
            "Treino 3 (Sex)": [
                "Aquecimento — 200m",
                "Série: 6×50m crawl c/ 30s descanso",
                "Costas (técnica) — 4×25m",
                "Resfriamento — 100m livre",
            ],
        }
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# AVISO DE SEGURANÇA
# ══════════════════════════════════════════════════════════════════════════════
AVISO_SEGURANCA = """
**⚠️ IMPORTANTE — Leia antes de iniciar qualquer atividade física**

Este aplicativo é uma **ferramenta educacional e de apoio ao planejamento**. Ele **não substitui** a avaliação presencial de um profissional habilitado nem prescrição médica.

**Antes de iniciar:**
- Consulte um **médico** para avaliação clínica, especialmente se tiver doenças crônicas, cardiovasculares ou musculoesqueléticas.
- Exija do seu profissional o **CREF ativo** (Conselho Regional de Educação Física). Todo profissional de Educação Física deve apresentar o registro. [Consultar profissional](https://cref-rj.implanta.net.br/servicosOnline/Publico/ConsultaInscritos/) | [Fazer denúncia](https://cref-rj.implanta.net.br/servicosOnline/Publico/Denuncias/)
- Todo profissional de Educação Física que atua com pessoas deve ter o **SBV — Suporte Básico de Vida** (também chamado de BLS — Basic Life Support). Esse curso capacita para RCP (ressuscitação cardiopulmonar) e uso do DEA (desfibrilador). É exigido pelo CREF para atuação em qualquer área da Educação Física.
- Para atividades aquáticas supervisionadas: o profissional deve possuir adicionalmente o **Curso de Primeiros Socorros e Salvamento Aquático**, exigido pelo CREF para atuação em piscinas e ambientes aquáticos.
- **Bacharel em Educação Física com CREF ativo** é o profissional habilitado para prescrever exercícios. Para reabilitação: **Fisioterapeuta com CREFITO ativo**.

**Sinais de alerta — PARE o treino imediatamente se sentir:**
- Dor no peito, falta de ar intensa ou tontura
- Dor aguda em qualquer articulação
- Batimentos cardíacos irregulares
- Visão turva ou desmaio iminente

**Progressão segura:**
- Inicie sempre com intensidade baixa e progrida gradualmente (máximo 10% de volume/semana).
- Respeite os dias de descanso — a recuperação é parte do treino.
- Hidrate-se antes, durante e após o exercício.
- Realize aquecimento (5–10 min) e resfriamento (5 min) em toda sessão.

*BioGestão 360 — para uso por profissionais habilitados e público autocapacitado sob orientação médica.*
"""


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

        lesoes = st.text_area("Lesões atuais ou histórico relevante:",
            placeholder="Ex: entorse de tornozelo há 3 meses, cirurgia de joelho em 2022...",
            key="treino_lesoes", height=70)

    # ── Alertas de condições ──────────────────────────────────────────────────
    condicoes_ativas = [c for c in condicoes if c != "Nenhuma"]
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

    if "Cardiopatia" in condicoes_ativas or "Pós-operatório (< 6 meses)" in condicoes_ativas:
        st.error("🚨 **ATENÇÃO:** Esta condição requer laudo médico por escrito antes de iniciar qualquer atividade física.")

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

    # ── 5.4 SUGESTÃO AUTOMÁTICA ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📋 5.4 — Sugestão de Treino Automática")

    freq_map   = {"1-2x": "3x", "3x": "3x", "4-5x": "4-5x", "6-7x": "6-7x"}
    freq_chave = freq_map.get(frequencia, "3x")
    chave      = (categoria, nivel, freq_chave)
    fallbacks  = [
        (categoria, nivel, "3x"),
        (categoria, "Iniciante", "3x"),
        ("🏋️ Academia / Musculação", nivel, freq_chave),
        ("🏋️ Academia / Musculação", "Iniciante", "3x"),
    ]
    sugestao = SUGESTOES_TREINO.get(chave)
    if not sugestao:
        for fb in fallbacks:
            sugestao = SUGESTOES_TREINO.get(fb)
            if sugestao:
                break

    if sugestao:
        st.success(f"**{sugestao['nome']}**")
        st.write(sugestao["descricao"])
        for dia_t, exs in sugestao["dias"].items():
            with st.expander(f"📅 {dia_t}"):
                for ex in exs:
                    st.write(f"• {ex}")
    else:
        st.info(f"Sugestão automática não disponível para **{categoria} / {nivel} / {frequencia}**. Use a seção 5.5 abaixo para montar seu treino.")

    # ── 5.5 MONTAGEM LIVRE DE TREINO ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🛠️ 5.5 — Monte Seu Próprio Treino (Musculação)")
    st.caption("Escolha os grupos musculares, exercícios e método. Disponível para todos os níveis.")

    treino_montado = {}

    grupos_sel = st.multiselect(
        "Grupos musculares desta sessão:",
        list(BANCO_EXERCICIOS.keys()),
        key="treino_grupos"
    )

    metodo_sel = st.selectbox(
        "Método de treino:",
        list(METODOS_TREINO.keys()),
        key="treino_metodo"
    )
    st.caption(f"📖 **{metodo_sel}:** {METODOS_TREINO[metodo_sel]}")

    col_s, col_r, col_i = st.columns(3)
    with col_s:
        num_series = st.number_input("Séries:", min_value=1, max_value=10, value=3, key="treino_series")
    with col_r:
        num_reps   = st.text_input("Repetições:", value="12", key="treino_reps",
                                   placeholder="Ex: 12 / 10-12 / máx")
    with col_i:
        intervalo  = st.text_input("Intervalo:", value="60s", key="treino_intervalo",
                                   placeholder="Ex: 60s / 90s / 2min")

    for grupo in grupos_sel:
        st.markdown(f"**{grupo}**")
        exs_sel = st.multiselect(
            f"Exercícios — {grupo}:",
            BANCO_EXERCICIOS[grupo],
            key=f"treino_ex_{grupo}"
        )
        if exs_sel:
            treino_montado[grupo] = exs_sel

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
        html = _gerar_relatorio_html(
            nome_aluno=nome_aluno, idade_aluno=idade_aluno, sexo_aluno=sexo_aluno,
            nome_instrutor=nome_instrutor, cref=cref, local_treino=local_treino,
            nivel=nivel, frequencia=frequencia, objetivo=objetivo,
            condicoes=condicoes_ativas, liberacao=liberacao,
            exames=exames, lesoes=lesoes,
            categoria=categoria, atividade=atividade, met_val=met_val,
            peso_treino=peso_treino, duracao_min=duracao_min,
            sessoes_semana=sessoes_semana, kcal_sessao=kcal_sessao,
            kcal_semana=kcal_semana, kcal_mes=kcal_mes,
            sugestao=sugestao, treino_montado=treino_montado,
            metodo_sel=metodo_sel, num_series=num_series,
            num_reps=num_reps, intervalo=intervalo,
            get_atual=get_atual,
        )
        nome_arq = f"treino_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        b64 = base64.b64encode(html.encode("utf-8")).decode()
        st.markdown(
            f'<a href="data:text/html;base64,{b64}" download="{nome_arq}">⬇️ Baixar {nome_arq}</a>',
            unsafe_allow_html=True
        )
        st.success("✅ Relatório gerado!")


# ══════════════════════════════════════════════════════════════════════════════
# GERADOR HTML
# ══════════════════════════════════════════════════════════════════════════════
def _gerar_relatorio_html(**kw):
    now          = datetime.now().strftime("%d/%m/%Y %H:%M")
    sugestao     = kw.get("sugestao")
    treino_m     = kw.get("treino_montado", {})
    condicoes    = kw.get("condicoes", [])
    get_atual    = kw.get("get_atual", 0)

    # Sugestão automática
    sug_html = ""
    if sugestao:
        sug_html = f"<h3>{sugestao['nome']}</h3><p><em>{sugestao['descricao']}</em></p>"
        for dia, exs in sugestao["dias"].items():
            sug_html += f"<h4 style='color:#0f3460'>{dia}</h4><ul>"
            for ex in exs:
                sug_html += f"<li>{ex}</li>"
            sug_html += "</ul>"

    # Treino montado
    montado_html = ""
    if treino_m:
        montado_html = f"""
        <h3>Treino Personalizado — {kw.get('metodo_sel','')}</h3>
        <p><strong>Séries:</strong> {kw.get('num_series','3')} &nbsp;|&nbsp;
           <strong>Repetições:</strong> {kw.get('num_reps','12')} &nbsp;|&nbsp;
           <strong>Intervalo:</strong> {kw.get('intervalo','60s')}</p>
        <p><em>{METODOS_TREINO.get(kw.get('metodo_sel',''), '')}</em></p>
        """
        for grupo, exs in treino_m.items():
            montado_html += f"<h4 style='color:#0f3460'>{grupo}</h4><ul>"
            for ex in exs:
                montado_html += (
                    f"<li>{ex} — "
                    f"{kw.get('num_series','3')}×{kw.get('num_reps','12')}"
                    f" | intervalo: {kw.get('intervalo','60s')}</li>"
                )
            montado_html += "</ul>"

    # Condições
    cond_html = ", ".join(condicoes) if condicoes else "Nenhuma"

    # Alertas
    alertas_html = ""
    for cond in condicoes:
        if cond in RESTRICOES:
            _, _, obs = RESTRICOES[cond]
            alertas_html += f'<div class="alerta"><strong>{cond}:</strong> {obs}</div>'

    # Balanço
    balanco_html = ""
    if get_atual > 0:
        get_com = round(get_atual + kw['kcal_semana'] / 7)
        balanco_html = f"""
        <h2>⚖️ Balanço Energético</h2>
        <table>
          <tr><th>GET em repouso (sem treino)</th><td>{get_atual:.0f} kcal/dia</td></tr>
          <tr><th>Gasto médio c/ treino ({kw['sessoes_semana']}x/sem)</th>
              <td>+{kw['kcal_semana']/7:.0f} kcal/dia</td></tr>
          <tr><th>GET total estimado</th><td><strong>{get_com} kcal/dia</strong></td></tr>
        </table>"""

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
  <tr><th>Condições de saúde</th><td colspan="3">{cond_html}</td></tr>
  <tr><th>Lesões / Histórico</th><td colspan="3">{kw.get('lesoes','—') or '—'}</td></tr>
</table>

{f'<h2>⚠️ Alertas de Saúde</h2>{alertas_html}' if alertas_html else ''}

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
  • Progressão gradual: nunca aumente carga ou volume mais de 10% por semana.
</div>

<footer>
  BioGestão 360 v4.1 | Plano de Treino gerado em {now}<br>
  Profissional responsável: {kw.get('nome_instrutor') or '—'} | CREF: {kw.get('cref') or '—'}<br>
  Este documento não substitui avaliação presencial de profissional de Educação Física habilitado (CREF).<br>
  Referência MET: Ainsworth BE et al. Compendium of Physical Activities. Med Sci Sports Exerc. 2011.
</footer>
</body></html>"""
