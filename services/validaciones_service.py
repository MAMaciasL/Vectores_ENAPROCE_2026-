import pandas as pd
from services.rules.loader import cargar_vectores
from services.rules.engine import ejecutar_validaciones
#from validators.semantic import es_semanticamente_similar

def validar_archivo(ruta):

    #Leer archivo
    df = pd.read_excel(ruta)
    df.columns = df.columns.str.strip()

    errores = []
    # errores += validar_otros(df)
    # errores += validar_otros_semantica(df)
    df_errores = pd.DataFrame(errores)

    

    #Vectores
    vectores = cargar_vectores("data/Vectores_Enaproce_2026_220526.xlsx")

    #Ejecutar motor
    resultados = ejecutar_validaciones(df, vectores)

    #Convertir a formato tabla UI
    lista = []

    for r in resultados:
        lista.append({
            "ID_CAT_ENCUESTAS_INFO": r["ID"],
            "Nombre Vector": r["VECTOR"],
            "Variables Involucradas": r.get("VARIABLES INVOLUCRADAS", ""),
            "Procedimiento": r.get("PROCEDIMIENTO", "")
        })

    df_errores = pd.DataFrame(lista)

    columnas = ["ID_CAT_ENCUESTAS_INFO", "Nombre Vector", "Variables Involucradas", "Procedimiento"]
    for col in columnas:
        if col not in df_errores.columns:
            df_errores[col] = ""

    return df, df_errores


#def validar_otros(df):
#    errores = []
#    columnas = df.columns
#    for col in columnas:
#        if col.endswith("_9") or col.endswith("_19") or col.endswith("_9A") or col.endswith("_9B"):
#            col_txt = col + "X"
#            if col_txt in columnas:
#                mask = (
#                    df[col].notna() & 
#                    (df[col] != "") &
#                    (
#                        df[col_txt].isna() | 
#                        (df[col_txt].astype(str).str.strip() == "")
#                    )
#                )
#                filas_error = df[mask]
#                for _, fila in filas_error.iterrows():
#                    errores.append({
#                        "ID_CAT_ENCUESTAS_INFO": fila["ID_CAT_ENCUESTAS_INFO"],
#                        "Nombre Vector": col,
#                        "Variables Involucradas": f"{col}, {col_txt}",
#                        "Procedimiento": "Seleccionó 'Otro' pero no especificó"
#                    })
#    return errores
#
#
#def validar_otros_semantica(df):
#
#    errores = []
#
#    for col in df.columns:
#
#        if col.endswith("X"):
#
#            if col in CATALOGOS_OTROS:
#
#                catalogo = CATALOGOS_OTROS[col]
#
#                for _, fila in df.iterrows():
#
#                    texto = fila[col]
#
#                    if pd.isna(texto) or str(texto).strip() == "":
#                        continue
#
#                    es_similar, opcion, score = es_semanticamente_similar(
#                        texto,
#                        catalogo
#                    )
#
#                    if es_similar:
#
#                        errores.append({
#                            "ID_CAT_ENCUESTAS_INFO": fila["ID_CAT_ENCUESTAS_INFO"],
#                            "Nombre Vector": col,
#                            "Variables Involucradas": col,
#                            "Procedimiento": f"Texto similar a catálogo ('{opcion}') con score {round(score,2)} → no usar 'Otro'"
#                        })
#
#    return errores