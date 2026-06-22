import pandas as pd
import time
from app.utils.path_utils import resource_path
from app.repositories.excel_reader import cargar_vectores
from app.services.rules.engine import ejecutar_validaciones


def procesar_archivo_completo(ruta):

    inicio = time.time()

    # =========================
    # LEER DATA
    # =========================
    df = pd.read_excel(ruta, engine="openpyxl")
    df.columns = df.columns.str.strip().str.upper()

    # =========================
    # LEER VECTORES
    # =========================
    ruta_vectores = resource_path("data/Vectores_Enifarm_2026.xlsx")
    vectores = cargar_vectores(ruta_vectores)

    # =========================
    # CONSTRUIR CATALOGO
    # =========================
    #catalogos_auto = construir_catalogos_desde_vectores(vectores)

    # =========================
    # VALIDAR
    # =========================
    resultados = ejecutar_validaciones(df, vectores)
    df_errores = pd.DataFrame(resultados)

    total_registros = len(df)
    total_errores = len(df_errores)

    if not df_errores.empty:
        registros_con_error = df_errores["ID_CAT_ENCUESTAS_INFO"].nunique()
    else:
        registros_con_error = 0

    porcentaje_error = (
        (registros_con_error / total_registros) * 100
        if total_registros > 0 else 0
    )

    tiempo = round(time.time() - inicio, 2)

    return {
        "df": df,
        "df_errores": df_errores,
        "total_registros": total_registros,
        "total_errores": total_errores,
        "registros_con_error": registros_con_error,
        "porcentaje_error": porcentaje_error,
    }