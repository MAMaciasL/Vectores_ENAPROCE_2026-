from services.rules.transformer import transformar_condicion


def evaluar_condicion(row, condicion):
    try:
        entorno = row.to_dict()
        return eval(condicion, {}, entorno)
    except:
        return False


def ejecutar_validaciones(df, vectores):

    resultados = []

    # =========================
    # DETECTAR COLUMNAS
    # =========================
    col_algoritmo = None
    col_precond = None

    for col in vectores.columns:

        col_upper = col.upper().strip()

        if "ALGORITMO" in col_upper:
            col_algoritmo = col

        if "PRECOND" in col_upper or "FILTRO" in col_upper:
            col_precond = col

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

            #Obtener textos correctamente
            precond_raw = v.get(col_precond)
            algoritmo_raw = v.get(col_algoritmo)

            #Transformar
            precond = transformar_condicion(precond_raw)
            algoritmo = transformar_condicion(algoritmo_raw)

            # =========================
            # DEBUG
            # =========================
            #print("---- DEBUG ----")
            #print("ID:", id_encuesta)
            #print("VECTOR:", nombre_vector)
            #print("PRECOND:", precond)
            #print("ALGORITMO:", algoritmo)
            #print("----------------")

            # =========================
            # PRECONDICIÓN
            # =========================
            if precond:
                if not evaluar_condicion(row, precond):
                    continue

            # =========================
            # ERROR
            # =========================
            if algoritmo:
                if evaluar_condicion(row, algoritmo):

                    #print("🚨 ERROR DETECTADO")

                    resultados.append({
                        "ID": id_encuesta,
                        "VECTOR": nombre_vector,
                        "ERROR": algoritmo
                    })

    return resultados