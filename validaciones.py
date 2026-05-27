import pandas as pd
from reglas import validar_registro

# Leer archivo Excel
df = pd.read_excel("Vaciado_ENAPROCE2026.xlsx")
print(df.columns.tolist())

errores = []

# Recorrer registros
for i, fila in df.iterrows():
    id_registro = fila["ID_MUESTRA"]

    lista_errores = validar_registro(fila)

    for e in lista_errores:
        errores.append({
            "id": id_registro,
            "variable": e["variable"],
            "error": e["error"]
        })

# Guardar errores
df_errores = pd.DataFrame(errores)
df_errores.to_excel("errores.xlsx", index=False)

print("Validación terminada ✅")
