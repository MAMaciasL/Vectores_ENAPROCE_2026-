import customtkinter as ctk
from services.app_state import AppState


class ReportesView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Reportes", font=("Arial", 20)).pack()

        self.texto = ctk.CTkTextbox(self, width=600, height=400)
        self.texto.pack()

        self.generar()

    def generar(self):

        df = AppState.resultados_actuales

        if df is None or df.empty:
            self.texto.insert("0.0", "Sin errores")
            return

        vectores = df["vector"].value_counts()
        variables = df["variable"].value_counts()

        txt = "TOP VECTORES\n\n"
        txt += str(vectores.head(10)) + "\n\n"

        txt += "TOP VARIABLES\n\n"
        txt += str(variables.head(10))

        self.texto.insert("0.0", txt)