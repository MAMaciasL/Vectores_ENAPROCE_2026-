from services.rules.transformer import transformar_condicion, variables_en_condicion
import re

def evaluar_condicion(row_dict, condicion):
    try:
        return eval(condicion, {}, row_dict)
    except Exception:
        return False


def ejecutar_validaciones(df, vectores):

    resultados = []
    registros = df.to_dict(orient="records")

    vectores_preparados = []

    # =========================
    # PREPARAR VECTORES
    # =========================
    for _, v in vectores.iterrows():

        tipo = str(v.get("TIPO", "")).strip().upper()

        if tipo not in ["I", "O"]:
            continue

        nombre_vector = v.get("NOMBRE VECTOR 2026")

        precond = transformar_condicion(
            v.get("FILTRO / PRECONDICIÓN\nENAPROCE 2026")
        )

        algoritmo = transformar_condicion(
            v.get("ALGORITMO \n (valor teórico)\nENAPROCE 2026")
        )

        #DETECTAR VARIABLE
        variable = "N/A"
        if algoritmo:
            vars_detectadas = re.findall(r'P[A-Z0-9_]+', algoritmo)
            if vars_detectadas:
                variable = vars_detectadas[0]

        vectores_preparados.append({
            "nombre": nombre_vector,
            "tipo": tipo,
            "precond": precond,
            "algoritmo": algoritmo,
            "variable": variable
        })

    # =========================
    # EJECUCIÓN
    # =========================
    for row in registros:

        errores_fila = []

        for v in vectores_preparados:

            #obtener variables de la condición
            vars_cond = variables_en_condicion(
                (v["precond"] or "") + " " + (v["algoritmo"] or "")
            )

            #crear copia segura del registro
            row_eval = row.copy()

            #rellenar variables faltantes como None
            for var in vars_cond:
                if var not in row_eval:
                    row_eval[var] = None

            #PRECONDICIÓN
            if v["precond"]:
                if not evaluar_condicion(row_eval, v["precond"]):
                    continue

            #ALGORITMO
            if v["algoritmo"]:
                if evaluar_condicion(row_eval, v["algoritmo"]):

                    errores_fila.append({
                        "vector": v["nombre"],
                        "variable": v["variable"],
                        "mensaje": "Error de validación"
                    })

        if errores_fila:
            resultados.append({
                "ID_CAT_ENCUESTAS_INFO": row.get("ID_CAT_ENCUESTAS_INFO"),
                "errores": errores_fila
            })

    return resultados