import pandas as pd

def validar_registro(fila):

    errores = []

    def valor_numerico(valor):

        try:
            return int(float(valor))
        except:
            return None

    # =====================================================
    # VECTOR 02O01
    # =====================================================

    if valor_numerico(fila.get("P2_9")) and valor_numerico(fila.get("P2_9")) > 0:

        if pd.isna(fila.get("P2_9X")) or str(fila.get("P2_9X")).strip() == "":

            errores.append({
                "vector": "E_ENAPROCE_02O01",
                "variable": "P2_9X",
                "mensaje": "No especificó 'Otra' fuente de capital"
            })

    # =====================================================
    # VECTOR 03O01
    # =====================================================

    valores_p3 = [
        valor_numerico(fila.get("P3_1")),
        valor_numerico(fila.get("P3_2")),
        valor_numerico(fila.get("P3_3"))
    ]

    if 19 in valores_p3:

        if pd.isna(fila.get("P3_19X")) or str(fila.get("P3_19X")).strip() == "":

            errores.append({
                "vector": "E_ENAPROCE_03O01",
                "variable": "P3_19X",
                "mensaje": "No especificó 'Otro' factor de ubicación"
            })

    # =====================================================
    # VECTOR 04O01
    # =====================================================

    if valor_numerico(fila.get("P4")) == 9:

        if pd.isna(fila.get("P4_9X")) or str(fila.get("P4_9X")).strip() == "":

            errores.append({
                "vector": "E_ENAPROCE_04O01",
                "variable": "P4_9X",
                "mensaje": "No especificó 'Otro(a)' propietario o accionista"
            })

    # =====================================================
    # VECTOR 05O01
    # =====================================================

    if valor_numerico(fila.get("P5")) == 9:

        if pd.isna(fila.get("P5_9X")) or str(fila.get("P5_9X")).strip() == "":

            errores.append({
                "vector": "E_ENAPROCE_05O01",
                "variable": "P5_9X",
                "mensaje": "No especificó 'Otro(a)' en toma de decisiones"
            })

    return errores