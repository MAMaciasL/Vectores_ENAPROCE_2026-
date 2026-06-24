from app.services.rules.semantic_validator import es_semanticamente_similar
from app.validators.text_validator import *
from app.validators.catalogo_validator import *
import re
import pandas as pd



def es_campo_otro(col):
    col = col.upper().strip()
    return col.endswith("_X") or col.endswith("9X") or col.endswith("19X")

def obtener_catalogo(col):

    col = col.upper()

    if col.startswith("P2_9"):
        return FUENTES_CAPITAL

    return None


def validar_texto(valor):

    #if not valor or str(valor).lower() == "nan":
    #    return "Vacío o NAN"
    
    if texto_basura(valor):
        return "Texto basura"

    if not longitud_minima(valor, 6):
        return "Texto muy corto"

    if not longitud_valida(valor, 200):
        return "Texto demasiado largo"

    if caracteres_invalidos(valor):
        return "Caracteres inválidos"

    #if len(valor.split()) <= 1:
    #    return "Texto insuficiente"

    if es_ruido_semantico(valor):
        return "Texto irrelevante"

    if solo_numeros(valor):
        return "Solo números"

    return None



def construir_nombre_vector(col):

    col = col.upper().strip()

    match = re.match(r"P(\d+)", col)

    if not match:
        return f"E_ENIFARM_{col}"

    numero = int(match.group(1))
    prefijo = f"{numero:02d}"

    if not col.endswith("X"):
        return f"E_ENIFARM_{prefijo}"

    if "AX" in col:
        sufijo = "01"
    elif "BX" in col:
        sufijo = "02"
    elif "CX" in col:
        sufijo = "03"
    else:
        sufijo = "01"

    return f"E_ENIFARM_{prefijo}O{sufijo}"


def validar_semantica_row(row, resultados, id_encuesta):

    for col in row.index:

        if not es_campo_otro(col):
            continue

        valor = row.get(col)

        if pd.isna(valor):
            continue

        valor_str = str(valor).strip()

        if valor_str in ["", "0"]:
            continue

        error = validar_texto(valor_str)

        if error:
            nombre_limpio = col.upper().replace("P", "", 1)
            resultados.append({
                "ID_CAT_ENCUESTAS_INFO": id_encuesta,
                "Nombre Vector": construir_nombre_vector(col),
                "Variables Involucradas": col,
                "Procedimiento": f"{error}: {valor_str}"
            })
            continue

        # =========================
        # VALIDACIÓN SEMÁNTICA
        # =========================
        catalogo = obtener_catalogo(col)

        if not catalogo:
            continue

        valido, opcion, score = es_semanticamente_similar(valor_str, catalogo)

        if score < 0.65:
            continue

        if len(valor_str.split()) <= 2:
            continue

        if not valido:
            resultados.append({
                "ID_CAT_ENCUESTAS_INFO": id_encuesta,
                "Nombre Vector": construir_nombre_vector(col),
                "Variables Involucradas": col,
                "Procedimiento": f"{valor_str} → similar a '{opcion}'"
            })

    
