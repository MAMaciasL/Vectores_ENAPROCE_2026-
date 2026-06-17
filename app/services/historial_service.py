import pandas as pd
import os
from datetime import datetime

RUTA = "data/historial.csv"

def guardar_historial(ruta_archivo, total_registros, total_errores):

    nuevo = pd.DataFrame([{
        "archivo": ruta_archivo,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "registros": total_registros,
        "errores": total_errores
    }])

    if os.path.exists(RUTA):
        df = pd.read_csv(RUTA)
        df = pd.concat([df, nuevo], ignore_index=True)
    else:
        df = nuevo

    df.to_csv(RUTA, index=False)


def obtener_historial():
    if os.path.exists(RUTA):
        return pd.read_csv(RUTA)
    return pd.DataFrame(columns=["archivo", "fecha", "registros", "errores"])