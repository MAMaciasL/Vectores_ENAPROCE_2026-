import pandas as pd

from services.rules.loader import cargar_vectores
from services.rules.engine import ejecutar_validaciones


def validar_archivo(ruta):
    # Leer archivo
    df = pd.read_excel(ruta)

    df.columns = df.columns.str.strip().str.upper()

    # Cargar vectores
    vectores = cargar_vectores("data/Vectores_Enaproce_2026_220526.xlsx")

    # Ejecutar validaciones
    resultados = ejecutar_validaciones(df, vectores)

    lista_errores = []

    # Recorrer resultados
    for item in resultados:
        id_encuesta = item.get("ID_CAT_ENCUESTAS_INFO", "N/A")

        for e in item.get("errores", []):
            lista_errores.append({
                "ID_CAT_ENCUESTAS_INFO": id_encuesta,
                "vector": e.get("vector", "N/A"),
                "variable": e.get("variable", "N/A"),
                "mensaje": e.get("mensaje", "Error detectado")
            })

    df_errores = pd.DataFrame(lista_errores)

    columnas = ["ID_CAT_ENCUESTAS_INFO", "vector", "variable", "mensaje"]
    for col in columnas:
        if col not in df_errores.columns:
            df_errores[col] = ""

    return df, df_errores
