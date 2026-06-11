import pandas as pd
from services.rules.loader import cargar_vectores
from services.rules.engine import ejecutar_validaciones


def validar_archivo(ruta):

    #Leer archivo
    df = pd.read_excel(ruta)
    df.columns = df.columns.str.strip()

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