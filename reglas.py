import pandas as pd

def validar_registro(fila):
    errores = []

    for col in fila.index:

        valor = fila.get(col)

        # 🔵 CASO REAL: columna principal = P4, P5, etc.
        if not col.endswith("X"):

            col_x = col + "_9X"
            col_19x = col + "_19X"

            # ✅ caso "9"
            if col_x in fila.index:
                if valor == 9:
                    if pd.isna(fila[col_x]) or str(fila[col_x]).strip() == "":
                        errores.append({
                            "variable": col_x,
                            "error": "Seleccionó «Otro» pero no especificó"
                        })

            # ✅ caso "19"
            if col_19x in fila.index:
                if valor == 19:
                    if pd.isna(fila[col_19x]) or str(fila[col_19x]).strip() == "":
                        errores.append({
                            "variable": col_19x,
                            "error": "Seleccionó Otro (19)' pero no especificó"
                        })

    return errores