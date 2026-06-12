import pandas as pd
import os
from datetime import datetime

RUTA = "data/historial.csv"


def guardar_historial(nombre_archivo, total, errores):

    os.makedirs("data", exist_ok=True)

    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "archivo": nombre_archivo,
        "registros": total,
        "errores": errores
    }

    df = pd.DataFrame([registro])

    if os.path.exists(RUTA):
        df.to_csv(RUTA, mode="a", header=False, index=False)
    else:
        df.to_csv(RUTA, index=False)


def obtener_historial():

    if os.path.exists(RUTA):
        return pd.read_csv(RUTA)

    return pd.DataFrame()