import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from app.services.mapeo_automatico import detectar_campos


class MapeoView(tk.Toplevel):

    def __init__(self, master, df):
        super().__init__(master)

        self.title("Configuración de Mapeo")
        self.geometry("600x400")

        self.df = df
        self.columnas = list(df.columns)

        self.campos = {
            "ID_CAT_ENCUESTAS_INFO": tk.StringVar(),
            "ANALISTA": tk.StringVar(),
            "RAZON_SOCIAL": tk.StringVar(),
            "NOMBRE_EMPRESA": tk.StringVar(),
            "TELEFONO": tk.StringVar(),
            "CORREO": tk.StringVar(),
            "INFORMANTE": tk.StringVar(),
        }

        self.crear_ui()

        self.auto_detectar()

    # =========================
    # UI
    # =========================
    def crear_ui(self):

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        row = 0

        for campo, var in self.campos.items():

            ttk.Label(frame, text=campo).grid(
                row=row, column=0, sticky="w", pady=5
            )

            combo = ttk.Combobox(
                frame,
                textvariable=var,
                values=self.columnas,
                width=40
            )

            combo.grid(row=row, column=1, pady=5)

            row += 1

        # BOTONES
        ttk.Button(frame, text="Auto detectar",
                   command=self.auto_detectar).grid(row=row, column=0)

        ttk.Button(frame, text="Guardar",
                   command=self.guardar).grid(row=row, column=1)

        row += 1

        ttk.Button(frame, text="Cargar",
                   command=self.cargar).grid(row=row, column=0)

        ttk.Button(frame, text="Usar mapeo",
                   command=self.aceptar).grid(row=row, column=1)

    # =========================
    # AUTO MAPEO
    # =========================
    def auto_detectar(self):

        mapa = detectar_campos(self.df)

        for campo, col in mapa.items():
            if col:
                self.campos[campo].set(col)

    # =========================
    # GUARDAR JSON
    # =========================
    def guardar(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".json"
        )

        if not path:
            return

        data = {k: v.get() for k, v in self.campos.items()}

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Éxito", "Mapeo guardado")

    # =========================
    # CARGAR JSON
    # =========================
    def cargar(self):

        path = filedialog.askopenfilename()

        if not path:
            return

        with open(path) as f:
            data = json.load(f)

        for campo, valor in data.items():
            if campo in self.campos:
                self.campos[campo].set(valor)

    def auto_detectar(self):

        mapa = detectar_campos(self.df)

        if mapa is None:
            messagebox.showerror("Error", "No se pudo detectar el mapeo")
            return

        for campo, col in mapa.items():
            if col:
                self.campos[campo].set(col)

    # =========================
    # ACEPTAR
    # =========================
    def aceptar(self):

        self.resultado = {k: v.get() for k, v in self.campos.items()}

        self.destroy()