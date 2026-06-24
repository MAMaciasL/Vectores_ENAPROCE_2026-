import pandas as pd

def detectar_campos(df):

    cols = df.columns

    def find(*keys):
        for k in keys:
            for c in cols:
                if k in c.upper():
                    return c
        return None

    return {
        "CLEE": find("CLEE"),
        "ID": find("ID_CAT"),
        "ANALISTA": find("ANALISTA"),
        "SUPERVISOR": find("SUPERVISOR"),
        "RAZON_SOCIAL": find("RAZON"),
        "NOMBRE_EMPRESA": find("EMPRESA"),
        "TELEFONO": find("TEL"),
        "CORREO": find("CORREO"),
        "INFORMANTE": find("INFORMANTE", "CONTACTO")
    }
