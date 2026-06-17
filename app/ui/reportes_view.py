import customtkinter as ctk
from tkinter import ttk
from app.services.app_state import AppState
from config import *
from datetime import datetime
from tkinter import filedialog, messagebox
import pandas as pd

hoy = datetime.now().strftime("%d/%m/%Y")

class ReportesView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.crear_titulo()
        self.crear_tabla()
        self.cargar_datos()

    def crear_titulo(self):

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            self,
            text="Reportes de Procesamiento",
            font=(FONT, 22, "bold"),
            text_color=COLOR_TITULOS
        ).pack(anchor="w", padx=20, pady=(20, 10))

        
        ctk.CTkButton(
            top,
            text="Exportar Excel",
            width=140,
            fg_color=COLOR_PRINCIPAL,
            command=self.exportar_excel
        ).pack(side="right")


    def crear_tabla(self):
        frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = (
            "Fecha", "Archivo", "Registros",
            "Correctos", "Errores", "Tiempo (s)"
        )

        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_datos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for r in getattr(AppState, "historial_reportes", []):
            self.tabla.insert("", "end", values=(
                r["fecha"],
                r["archivo"],
                r["registros"],
                r["correctos"],
                r["errores"],
                r["tiempo"]
            ))

    def exportar_excel(self):

        if not hasattr(AppState, "historial_reportes") or not AppState.historial_reportes:
            messagebox.showwarning(
                "Sin datos",
                "No hay reportes para exportar."
            )
            return
    
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")]
        )
    
        if not ruta:
            return
    
        df = pd.DataFrame(AppState.historial_reportes)
    
        try:
            df.to_excel(ruta, index=False)
            messagebox.showinfo(
                "Exportado",
                "Reporte exportado correctamente."
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo exportar el archivo:\n{e}"
            )