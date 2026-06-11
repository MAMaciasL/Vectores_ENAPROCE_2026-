from services.rules.transformer import transformar_condicion


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

        if "PRECOND" in col_upper or "FILTRO" in col_upper:
            col_precond = col

        if "VARIABLES" in col_upper:
            col_variables = col

        if "PROCEDIMIENTO" in col_upper:
            col_procedimiento = col

    # =========================
    # LOOP PRINCIPAL
    # =========================
    for _, row in df.iterrows():

        id_encuesta = row.get("ID_CAT_ENCUESTAS_INFO")

        for _, v in vectores.iterrows():

            tipo = str(v.get("TIPO", "")).strip().upper()

            if tipo not in ["I", "O"]:
                continue

            nombre_vector = v.get("NOMBRE VECTOR 2026")

            precond_raw = v.get(col_precond)
            algoritmo_raw = v.get(col_algoritmo)
            variables_raw = v.get(col_variables)
            procedimiento_raw = v.get(col_procedimiento)

            # transformar
            precond = transformar_condicion(precond_raw)
            algoritmo = transformar_condicion(algoritmo_raw)

            # =========================
            # PRECONDICIÓN
            # =========================
            if precond and not evaluar_condicion(row, precond):
                continue

            # =========================
            # VALIDACIÓN
            # =========================
            if algoritmo and evaluar_condicion(row, algoritmo):

                resultados.append({
                    "ID": id_encuesta,
                    "VECTOR": nombre_vector,
                    "VARIABLES INVOLUCRADAS": (
                        " | ".join(str(variables_raw).split())
                        if variables_raw else ""
                    ),
                    "PROCEDIMIENTO": (
                        str(procedimiento_raw).replace("\n", ", ").strip()
                        if procedimiento_raw else ""
                    )
                })

    return resultados
