import customtkinter as ctk

from config import *
from views.validacion_view import ValidacionView


class MainView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        self.configure(
            fg_color=COLOR_FONDO
        )

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_sidebar()

        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.container.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.validacion_view = ValidacionView(
            self.container
        )

        self.validacion_view.pack(
            fill="both",
            expand=True
        )

    def crear_sidebar(self):

        sidebar = ctk.CTkFrame(
            self,
            width=240,
            fg_color=COLOR_PRINCIPAL,
            corner_radius=0
        )

        sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        sidebar.grid_propagate(False)

        menu_items = [
            "📂 Validación",
            "📊 Reportes",
            "🕘 Historial",
            "⚙ Configuración",
            "❓ Ayuda"
        ]

        for item in menu_items:

            btn = ctk.CTkButton(
                sidebar,
                text=item,
                fg_color="transparent",
                hover_color="#00553A",
                anchor="w",
                height=45
            )

            btn.pack(fill="x", padx=15, pady=5)