import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

from config import *
from views.main_view import MainView

USUARIO = "Admin"
PASSWORD = "1234"


class LoginView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        self.configure(fg_color=COLOR_FONDO)

        self.crear_ui()

    def crear_ui(self):

        card = ctk.CTkFrame(
            self,
            width=350,
            height=360,
            fg_color=COLOR_CARD,
            corner_radius=15
        )

        card.place(relx=0.5, rely=0.5, anchor="center")

        # LOGO
        try:

            img = Image.open("assets/images/logo_inegi.png")

            self.logo = ctk.CTkImage(
                light_image=img,
                size=(150, 55)
            )

            ctk.CTkLabel(
                card,
                image=self.logo,
                text=""
            ).pack(pady=(30, 15))

        except:
            pass

        titulo = ctk.CTkLabel(
            card,
            text="Inicio de sesión",
            font=(FONT, 28, "bold")
        )

        titulo.pack(pady=(10, 20))

        self.entry_usuario = ctk.CTkEntry(
            card,
            placeholder_text="Usuario",
            width=150,
            height=40
        )
        
        self.entry_usuario.pack(pady=10)

        self.entry_password = ctk.CTkEntry(
            card,
            placeholder_text="Contraseña",
            show="*",
            width=150,
            height=40
        )
        
        self.entry_password.pack(pady=10)
        self.entry_password.bind("<Return>", lambda e: self.verificar_login())
        self.entry_usuario.bind("<Return>", lambda e: self.entry_password.focus_set())


        btn = ctk.CTkButton(
            card,
            text="Ingresar",
            fg_color=COLOR_PRINCIPAL,
            hover_color=COLOR_SECUNDARIO,
            width=350,
            height=42,
            command=self.verificar_login
        )

        btn.pack(pady=20)

    def verificar_login(self):

        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        if usuario == USUARIO and password == PASSWORD:

            self.destroy()

            self.master.geometry("1400x800")
            self.master.state("zoomed")
            main_view = MainView(self.master)
            main_view.pack(fill="both", expand=True)

        else:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos"
            )