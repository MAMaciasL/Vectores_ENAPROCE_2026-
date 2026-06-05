import pandas as pd

def cargar_vectores(ruta):
    df = pd.read_excel(ruta, engine="openpyxl")
    df.columns = df.columns.str.strip().str.upper()

    df = df.replace(["NULL", "NaN", "nan", ""], None)

    return df
