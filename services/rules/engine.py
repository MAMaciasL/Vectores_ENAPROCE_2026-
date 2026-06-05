from services.rules.transformer import transformar_condicion


def evaluar_condicion(row, condicion):
    try:
        entorno = row.to_dict()
        return eval(condicion, {}, entorno)
    except:
        return False

def ejecutar_validaciones(df, vectores):

    resultados = []

    for _, row in df.iterrows():

       #print(f"Procesando encuesta ID: {row.get('ID_CAT_ENCUESTAS_INFO', 'N/A')}")

        errores_fila = []

        id_encuesta = row.get("ID_CAT_ENCUESTAS_INFO")

        for _, v in vectores.iterrows():

            tipo = str(v.get("TIPO", "")).strip().upper()

            if tipo not in ["I", "O"]:
                continue

            nombre_vector = v.get("NOMBRE VECTOR 2026")

            precond_raw = v.get("FILTRO / PRECONDICIÓN\nENAPROCE 2026")
            algoritmo_raw = v.get("ALGORITMO \n (valor teórico)\nENAPROCE 2026")

            precond = transformar_condicion(precond_raw)
            algoritmo = transformar_condicion(algoritmo_raw)

            variable = "N/A"
            if algoritmo:
                import re
                vars_detectadas = re.findall(r'P[A-Z0-9_]+', algoritmo)
                if vars_detectadas:
                    variable = vars_detectadas[0]

            # -----------------------------
            # PRECONDICIÓN
            # -----------------------------
            if precond:
                if not evaluar_condicion(row, precond):
                    continue

            # -----------------------------
            # ERROR
            # -----------------------------
            if algoritmo:

                
                if evaluar_condicion(row, algoritmo):
                    print("ID:", id_encuesta)
                    print("Expr:", algoritmo)
                    print("Valor:", row.get(variable))
                    print("Resultados:", resultados)
                    print("------")

                    if resultados:
                        print ("Error detectado")

                    errores_fila.append({
                        "vector": nombre_vector,
                        "variable": variable,
                        "mensaje": "Error de validación"
                    })

        if errores_fila:
            resultados.append({
                "ID_CAT_ENCUESTAS_INFO": id_encuesta,
                "errores": errores_fila
            })

        #print("=== FILAS EN DF ===", len(df))
        #print("=== FILAS EN VECTORES ===", len(vectores))

    return resultados