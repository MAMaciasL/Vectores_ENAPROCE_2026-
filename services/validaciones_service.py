import pandas as pd

from validators.reglas_enaproce import validar_registro

def validar_archivo(ruta):

    df = pd.read_excel(ruta)

    lista_errores = []

    for index, fila in df.iterrows():

        errores = validar_registro(fila)

        for e in errores:

            lista_errores.append({

            "ID_CAT_ENCUESTAS_INFO": fila.get("ID_CAT_ENCUESTAS_INFO"),
            "vector": e.get("vector"),
            "variable": e.get("variable"),
            "mensaje": e.get("mensaje")
            
            })

    return df, pd.DataFrame(lista_errores)