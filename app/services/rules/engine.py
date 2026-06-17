from app.services.rules.transformer import transformar_condicion
from app.services.rules.semantic_engine import validar_semantica_row


def evaluar_condicion(row, condicion):
    try:
        entorno = row.to_dict()
        return eval(condicion, {}, entorno)
    except:
        return False


def ejecutar_validaciones(df, vectores):

    resultados = []

    col_algoritmo = None
    col_precond = None
    col_variables = None
    col_procedimiento = None

    for col in vectores.columns:

        col_upper = col.upper().strip()

        if "ALGORITMO" in col_upper:
            col_algoritmo = col

        if "FILTRO" in col_upper or "PRECOND" in col_upper:
            col_precond = col

        if "VARIABLES" in col_upper:
            col_variables = col

        if "PROCEDIMIENTO" in col_upper:
            col_procedimiento = col

    for _, row in df.iterrows():

        id_encuesta = row.get("ID_CAT_ENCUESTAS_INFO")

        for _, v in vectores.iterrows():

            tipo = str(v.get("TIPO", "")).strip().upper()

            if tipo not in ["I", "O"]:
                continue

            nombre_vector = v.get("NOMBRE VECTOR 2026")

            precond = transformar_condicion(v.get(col_precond))
            algoritmo = transformar_condicion(v.get(col_algoritmo))

            if precond and not evaluar_condicion(row, precond):
                continue

            if algoritmo and evaluar_condicion(row, algoritmo):

                resultados.append({
                    "ID_CAT_ENCUESTAS_INFO": id_encuesta,
                    "Nombre Vector": nombre_vector,
                    "Variables Involucradas": (
                        ", ".join(str(v.get(col_variables)).replace("\n", " ").split())
                        if v.get(col_variables) else ""
                    ),                    
                    "Procedimiento": (
                    str(v.get(col_procedimiento))
                    .replace("\n", " ")
                    .replace("  ", " ")
                    .strip()
                    if v.get(col_procedimiento) else ""
                )
                })

        validar_semantica_row(row, resultados, id_encuesta)

    return resultados