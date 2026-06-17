import customtkinter as ctk
from tkinter import ttk
from config import *
from app.services.historial_service import obtener_historial


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

        self.tabla.pack(fill="both", expand=True)

        self.cargar()

    def cargar(self):

        df = obtener_historial()

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for _, fila in df.iterrows():
            self.tabla.insert("", "end", values=tuple(fila))
