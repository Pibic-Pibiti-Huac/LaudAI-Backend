import re
import json

def cot_prompt_report_message(report: str, examples_on: bool = True) -> list[dict]:
    cot_examples = """
EXEMPLOS:

Laudo:
- Opacidade ovalada em projeção peri-hilar esquerda, medindo 0,9 cm (vaso em projeção axial?).
- Seios costofrênicos livres.
- Placas parenquimatosas calcificadas em crossa da aorta. 
- Índice cardiotorácico preservado.
- Osteófitos marginais em corpos vertebrais dorsais.

Resposta:
{{
    "extracao": {{
        "c1": "Osteófitos marginais em corpos vertebrais dorsais",
        "c2": "Opacidade ovalada em projeção peri-hilar esquerda, medindo 0,9 cm (vaso em projeção axial?)",
        "c3": "Seios costofrênicos livres",
        "c4": "Índice cardiotorácico preservado",
        "c5": "Placas parenquimatosas em crossa da aorta"
    }},
    "avaliacao": {{
        "c1": "A menção a 'osteófitos marginais em corpos vertebrais dorsais' refere-se a uma alteração localizada da coluna vertebral, não a uma avaliação global da estrutura óssea.",
        "c2": "Não há menção a avaliação global dos pulmões, apenas alterações locais.",
        "c3": "A menção a 'seios costofrênicos livres' é uma avaliação direta de pelo menos um seio costofrênico.",
        "c4": "A menção a 'índice cardiotorácico preservado' é uma avaliação fundamentada explicitamente no ICT.",
        "c5": "Placas parenquimatosas em crossa da aorta' refere-se a uma estrutura mediastinal (aorta), portanto, envolve avaliação do mediastino."
    }},
    "notas": {{
        "c1": 0,
        "c2": 0,
        "c3": 1,
        "c4": 1,
        "c5": 1
    }}
}}

---

Laudo:
- Transparência pulmonar preservada.
- Mediastino sem alterações.
- Imagem cardíaca de configuração e dimensões normais.
- Alterações degenerativas da coluna dorsal.

Resposta:
{{
    "extracao": {{
        "c1": "Alterações degenerativas da coluna dorsal",
        "c2": "Transparência pulmonar preservada",
        "c3": "ausente",
        "c4": "Imagem cardíaca de configuração e dimensões normais",
        "c5": "Mediastino sem alterações"
    }},
    "avaliacao": {{
        "c1": "A menção a 'alterações degenerativas da coluna dorsal' é uma alteração localizada e não uma avaliação global da estrutura óssea.",
        "c2": "A menção a 'transparência pulmonar preservada' é uma avaliação global do estado geral do parênquima pulmonar.",
        "c3": "ausente",
        "c4": "A avaliação da área cardíaca menciona 'configuração e dimensões normais', mas não menciona explicitamente o ICT, portanto, não atende ao critério.",
        "c5": "Avaliação do mediastino é feita com a menção a mediastino sem alterações."
    }},
    "notas": {{
        "c1": 0,
        "c2": 1,
        "c3": 0,
        "c4": 0,
        "c5": 1
    }}
}}

---

Laudo:
- Nódulo hiperdenso em lobo superior direito, medindo 6mm (granuloma calcificado). 
- Restante do parênquima pulmonar preservado.
- Obliteração do seio costofrênico direito (derrame / espessamento pleural).
- Espondilose dorsal, associado a acentuação da cifose.
- Redução difusa da densidade óssea.

Resposta:
{{
    "extracao": {{
        "c1": "Redução difusa da densidade óssea",
        "c2": "Restante do parênquima pulmonar preservado",
        "c3": "Obliteração do seio costofrênico direito (derrame / espessamento pleural)",
        "c4": "ausente",
        "c5": "ausente"
    }},
    "avaliacao": {{
        "c1": "A avaliação cita alterações locais, como 'espondilose dorsal, associado a acentuação da cifose', mas traz avaliação global de 'redução difusa da densidade óssea'.",
        "c2": "A avaliação menciona globalmente a estrutura pulmonar com 'restante do parênquima pulmonar preservado', e traz alterações locais de 'nódulo hiperdenso em lobo superior direito, medindo 6mm (granuloma calcificado)'.",
        "c3": "A menção a 'obliteração do seio costofrênico direito (derrame / espessamento pleural)' é uma avaliação direta de pelo menos um seio costofrênico.",
        "c4": "ausente",
        "c5": "ausente"
    }},
    "notas": {{
        "c1": 1,
        "c2": 1,
        "c3": 1,
        "c4": 0,
        "c5": 0
    }}
}}

---

Laudo:
- Transparência pulmonar normal.
- Seios costofrênicos livres.
- Índice cardiotorácico aumentado.
- Aorta alongada e com placas parietais em sua crossa.
- Rarefação óssea difusa.
- Eixo vertebral dorsal desviado à direita

Resultiado:
{{
    "extracao": {{
        "c1": 
    }}
}}
"""

    criteria = """
c1
Verifique se existe avaliação GLOBAL da estrutura óssea.
Considere apenas avaliações do estado geral da estrutura óssea; menções apenas a alterações localizadas não satisfazem este critério.

c2
Verifique se existe avaliação GLOBAL dos pulmões.
Considere apenas avaliações do estado geral do parênquima pulmonar; menções apenas a alterações localizadas não satisfazem este critério.

c3
Verifique se existe avaliação de pelo menos um seio costofrênico.

c4
Verifique se existe avaliação da área cardíaca fundamentada explicitamente no Índice Cardiotorácico (ICT).
Avaliações da área cardíaca que não mencionam explicitamente o ICT não satisfazem este critério.

c5
Verifique se existe avaliação do mediastino ou de alguma estrutura mediastinal.
A avaliação pode ser direta ou indireta, desde que envolva o mediastino ou uma estrutura mediastinal.
"""

    system_prompt = f"""
Você é um avaliador especializado em qualidade estrutural de laudos de radiografia de tórax.
Avalie o laudo segundo os critérios.
Regras:
{criteria}

Para cada critério, siga OBRIGATORIAMENTE esta ordem:
1. Extração: copie LITERALMENTE o(s) trecho(s) do laudo relevantes para o critério.
   Se não houver nenhum trecho relevante, escreva "ausente".
2. Avaliação: com base SOMENTE no(s) trecho(s) extraído(s) no passo anterior 
   (não use outras partes do laudo), decida se o critério é satisfeito.
3. Nota: atribua 0 ou 1 com base exclusivamente na avaliação do passo 2. Se o critério foi satisfeito, atribua 1. Caso contrário, atribua 0.

NUNCA decida a nota antes de completar a extração e a avaliação.
NUNCA extraia um trecho de um critério diferente do que está sendo avaliado.

Responda somente no formato:
{{
 "extracao": {{
   "c1": "...", "c2": "...", "c3": "...", "c4": "...", "c5": "..."
 }},
 "avaliacao": {{
   "c1": "...", "c2": "...", "c3": "...", "c4": "...", "c5": "..."
 }},
 "notas": {{
   "c1":0 ou 1, "c2":0 ou 1, "c3":0 ou 1, "c4":0 ou 1, "c5":0 ou 1
 }}
}}
"""
    
    user_prompt = f"""Avalie o laudo radiográfico abaixo conforme os critérios e regras definidos.

LAUDO:
--------------------
{report}
--------------------

Retorne APENAS o JSON de avaliação. Nenhum texto fora do JSON.
Garanta que o JSON seja BEM FORMADO.

{cot_examples if examples_on else ""}
"""
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]