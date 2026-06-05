import customtkinter as ctk
from tkinter import ttk
from config import *
from services.historial_service import obtener_historial


class HistorialView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="transparent")

        ctk.CTkLabel(
            self,
            text="Historial de Validaciones",
            font=(FONT, 20, "bold")
        ).pack(pady=10)

        self.tabla = ttk.Treeview(
            self,
            columns=("fecha", "archivo", "registros", "errores"),
            show="headings"
        )

        for col in ("fecha", "archivo", "registros", "errores"):
            self.tabla.heading(col, text=col)

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar()

    def cargar(self):

        df = obtener_historial()

        for _, fila in df.iterrows():
            self.tabla.insert("", "end", values=tuple(fila))
