import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

from reglas import validar_registro  # tu función

def procesar_archivo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx")]
    )

    if not ruta:
        return

    try:
        df = pd.read_excel(ruta)

        lista_errores = []

        for index, fila in df.iterrows():
            errores = validar_registro(fila)

            for e in errores:
                lista_errores.append({
                    "id": fila.get("ID_MUESTRA"),
                    "fila": index,
                    "variable": e["variable"],
                    "error": e["error"]
                })

        df_errores = pd.DataFrame(lista_errores)

        df_errores.to_excel("errores.xlsx", index=False)

        messagebox.showinfo(
            "Proceso terminado",
            f"Validación completada.\nErrores encontrados: {len(lista_errores)}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# 🎨 Ventana
ventana = tk.Tk()
ventana.title("Validador ENAPROCE")
ventana.geometry("400x200")

label = tk.Label(ventana, text="Validador de Cuestionarios", font=("Arial", 12))
label.pack(pady=20)

btn = tk.Button(ventana, text="Seleccionar archivo y validar", command=procesar_archivo)
btn.pack(pady=10)

ventana.mainloop()
