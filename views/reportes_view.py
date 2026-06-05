import customtkinter as ctk
import pandas as pd
from config import *


class ReportesView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="transparent")

        ctk.CTkLabel(
            self,
            text="Reportes",
            font=(FONT, 20, "bold")
        ).pack(pady=10)

        self.texto = ctk.CTkTextbox(self, width=600, height=400)
        self.texto.pack(pady=10)

    def generar(self, df_errores):

        if df_errores.empty:
            self.texto.insert("0.0", "Sin errores")
            return

        # TOP VECTORES
        top_vectores = df_errores["vector"].value_counts()

        # TOP VARIABLES
        top_vars = df_errores["variable"].value_counts()

        reporte = "=== TOP VECTORES ===\n"
        reporte += str(top_vectores.head(10)) + "\n\n"

        reporte += "=== TOP VARIABLES ===\n"
        reporte += str(top_vars.head(10))

        self.texto.delete("0.0", "end")
        self.texto.insert("0.0", reporte)
