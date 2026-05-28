import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import threading
import os

from reglas import validar_registro

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

COLOR_PRINCIPAL = "#006847"
COLOR_SECUNDARIO = "#008C5A"
COLOR_FONDO = "#F4F6F9"
COLOR_TABLA = "#FFFFFF"

# CLASE PRINCIPAL
class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Ventana
        self.title("Validador ENAPROCE")
        self.geometry("1200x700")
        self.configure(fg_color=COLOR_FONDO)

        # Variables
        self.df_errores = pd.DataFrame()

        # Crear interfaz
        self.crear_header()
        self.crear_botones()
        self.crear_tabla()
        self.crear_footer()

    # ======================================
    # HEADER
    # ======================================

    def crear_header(self):

        frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_PRINCIPAL,
            height=80,
            corner_radius=0
        )

        frame.pack(fill="x")

        titulo = ctk.CTkLabel(
            frame,
            text="Validador de Cuestionarios ENAPROCE",
            font=("Arial", 28, "bold"),
            text_color="white"
        )

        titulo.pack(pady=20)

    # ======================================
    # BOTONES
    # ======================================

    def crear_botones(self):

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=15)

        self.btn_cargar = ctk.CTkButton(
            frame,
            text="Seleccionar Excel",
            fg_color=COLOR_PRINCIPAL,
            hover_color=COLOR_SECUNDARIO,
            command=self.cargar_archivo,
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )

        self.btn_cargar.pack(side="left", padx=10)

        self.btn_exportar = ctk.CTkButton(
            frame,
            text="Descargar errores",
            fg_color="#1F6AA5",
            hover_color="#144870",
            command=self.exportar_excel,
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )

        self.btn_exportar.pack(side="left", padx=10)

        self.label_estado = ctk.CTkLabel(
            frame,
            text="Esperando archivo...",
            font=("Arial", 13)
        )

        self.label_estado.pack(side="right", padx=20)

    # ======================================
    # TABLA
    # ======================================

    def crear_tabla(self):

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("ID", "Fila", "Variable", "Error")

        self.tabla = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            height=20
        )

        # Encabezados
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ======================================
    # FOOTER
    # ======================================

    def crear_footer(self):

        footer = ctk.CTkLabel(
            self,
            text="INEGI - Sistema de Validación",
            font=("Arial", 12)
        )

        footer.pack(pady=10)

    # ======================================
    # CARGAR ARCHIVO
    # ======================================

    def cargar_archivo(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel", "*.xlsx")]
        )

        if not ruta:
            return

        self.label_estado.configure(
            text="Procesando archivo..."
        )

        # Hilo para evitar congelamiento
        hilo = threading.Thread(
            target=self.procesar_archivo,
            args=(ruta,)
        )

        hilo.start()

    # ======================================
    # PROCESAR ARCHIVO
    # ======================================

    def procesar_archivo(self, ruta):

        try:

            df = pd.read_excel(ruta)

            lista_errores = []

            for index, fila in df.iterrows():

                errores = validar_registro(fila)

                for e in errores:

                    lista_errores.append({
                        "ID": fila.get("ID_MUESTRA"),
                        "Fila": index + 1,
                        "Variable": e["variable"],
                        "Error": e["error"]
                    })

            self.df_errores = pd.DataFrame(lista_errores)

            self.actualizar_tabla()

            self.label_estado.configure(
                text=f"Errores encontrados: {len(lista_errores)}"
            )

            messagebox.showinfo(
                "Proceso terminado",
                f"Validación completada\nErrores: {len(lista_errores)}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ACTUALIZAR TABLA

    def actualizar_tabla(self):

        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # Insertar nuevos datos
        for _, fila in self.df_errores.iterrows():

            self.tabla.insert(
                "",
                "end",
                values=(
                    fila["ID"],
                    fila["Fila"],
                    fila["Variable"],
                    fila["Error"]
                )
            )

    # EXPORTAR EXCEL

    def exportar_excel(self):

        if self.df_errores.empty:

            messagebox.showwarning(
                "Sin datos",
                "No hay errores para exportar"
            )

            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            title="Guardar archivo"
        )

        if not ruta:
            return

        self.df_errores.to_excel(
            ruta,
            index=False
        )

        messagebox.showinfo(
            "Exportado",
            "Archivo guardado correctamente"
        )

# EJECUTAR
if __name__ == "__main__":

    app = App()
    app.mainloop()