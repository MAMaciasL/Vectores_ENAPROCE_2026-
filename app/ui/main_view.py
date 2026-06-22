import customtkinter as ctk
from config import *
from app.ui.validacion_view import ValidacionView
from app.ui.historial_view import HistorialView
from app.ui.config_view import ConfigView
from app.ui.reportes_view import ReportesView
from app.services.app_state import AppState, cargar_historial

AppState.historial_reportes = cargar_historial()


class MainView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)
        self.configure(fg_color=COLOR_FONDO)

        # GRID BASE
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_sidebar()
        self.crear_container()

        self.mostrar_vista("validacion")
        

    # =========================
    # SIDEBAR
    # =========================
    def crear_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            fg_color=COLOR_PRINCIPAL,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # LOGO / TITULO
        ctk.CTkLabel(
            self.sidebar,
            text="ENIFARM",
            font=(FONT, 20, "bold"),
            text_color="white"
        ).pack(pady=(30, 20))

        # BOTONES MENU
        self.botones = {}

        menu_items = {
            "validacion": "📂 Validación",
            "reportes": "📊 Reportes",
            "historial": "🕘 Historial",
            "config": "⚙ Configuración"
        }

        for key, label in menu_items.items():

            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                fg_color="transparent",
                hover_color="#0B6E4F",
                anchor="w",
                height=45,
                command=lambda k=key: self.mostrar_vista(k)
            )

            btn.pack(fill="x", padx=15, pady=5)

            self.botones[key] = btn

        user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_frame.pack(side="bottom", fill="x", pady=20)

        ctk.CTkLabel(
        user_frame,
        text="👤 Admin",
        font=(FONT, 14),
        text_color="white"
        ).pack(anchor="center", padx=20, pady=5)

        ctk.CTkButton(
        user_frame,
        text="Cerrar sesión",
        fg_color=COLOR_OK,
        hover_color=COLOR_ERROR,
        command=self.logout
        ).pack(fill="x", padx=20)

    # =========================
    # CONTENEDOR VISTAS
    # =========================
    def crear_container(self):

        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.container.grid(row=0, column=1, sticky="nsew")

        self.vistas = {}

    # =========================
    # NAVEGACION
    # =========================
    def mostrar_vista(self, vista):

        # limpiar vista actual
        for widget in self.container.winfo_children():
            widget.destroy()

        # reset botones
        for btn in self.botones.values():
            btn.configure(fg_color="transparent")

        # activar botón
        self.botones[vista].configure(fg_color="#0B6E4F")

        # cargar vista
        if vista == "validacion":
            frame = ValidacionView(self.container)

        elif vista == "historial":
            frame = HistorialView(self.container)

        elif vista == "config":
            frame = ConfigView(self.container)

        elif vista == "reportes":
            frame = ReportesView(self.container)

        frame.pack(fill="both", expand=True)

    # =========================
    # LOGOUT
    # =========================
    def logout(self):

        self.destroy()

        from app.ui.login_view import LoginView

        login = LoginView(self.master)
        login.pack(fill="both", expand=True)