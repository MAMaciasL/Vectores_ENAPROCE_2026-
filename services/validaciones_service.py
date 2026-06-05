import pandas as pd
from services.rules.loader import cargar_vectores
from services.rules.engine import ejecutar_validaciones


def validar_archivo(ruta):

    # ✅ leer archivo SIN cambiar nada
    df = pd.read_excel(ruta)
    df.columns = df.columns.str.strip()

    # ✅ vectores originales
    vectores = cargar_vectores("data/Vectores_Enaproce_2026_220526.xlsx")

    # ✅ ejecutar motor original
    resultados = ejecutar_validaciones(df, vectores)

    # ✅ convertir a formato tabla UI
    lista = []

    for r in resultados:
        lista.append({
            "ID_CAT_ENCUESTAS_INFO": r["ID"],
            "vector": r["VECTOR"],
            "variable": r["ERROR"],  # 👈 aquí va la expresión
            "mensaje": "Error de validación"
        })

    df_errores = pd.DataFrame(lista)

    # asegurar columnas
    columnas = ["ID_CAT_ENCUESTAS_INFO", "vector", "variable", "mensaje"]
    for col in columnas:
        if col not in df_errores.columns:
            df_errores[col] = ""

    return df, df_errores