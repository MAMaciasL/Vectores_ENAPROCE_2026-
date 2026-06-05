import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

from config import *
from views.main_view import MainView
from services.auth_service import validar_usuario


class LoginView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)
        self.configure(fg_color=COLOR_FONDO)

        self.bg_label = None
        self.show_password = False

        self.crear_ui()

    # =========================
    # LOGIN
    # =========================
    def verificar_login(self):

        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        valido, data = validar_usuario(usuario, password)

        if valido:

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

    def crear_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =========================
        # PANEL IZQUIERDO
        # =========================
        self.left = ctk.CTkFrame(self, fg_color="transparent")
        self.left.grid(row=0, column=0, sticky="nsew")

        self.left.bind("<Configure>", self.actualizar_fondo)

        # =========================
        # PANEL DERECHO
        # =========================
        right = ctk.CTkFrame(self, fg_color=COLOR_FONDO)
        right.grid(row=0, column=1, sticky="nsew")

        form = ctk.CTkFrame(right, fg_color="transparent")
        form.place(relx=0.5, rely=0.5, anchor="center")

        try:
            logo_img = Image.open("assets/images/logo_inegi.png").convert("RGBA")

            self.logo = ctk.CTkImage(
                light_image=logo_img,
                size=(180, 60)
            )

            ctk.CTkLabel(
                form,
                image=self.logo,
                text="",
                fg_color="transparent"
            ).pack(pady=(0, 15))

        except Exception as e:
            print("Error logo:", e)

        # TITULO
        ctk.CTkLabel(
            form,
            text="Bienvenido",
            font=(FONT, 28, "bold"),
            text_color=COLOR_TITULOS
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            form,
            text="Ingresa tus credenciales",
            font=(FONT, 13),
            text_color=COLOR_GRIS
        ).pack(pady=(0, 20))

        # INPUT USUARIO
        self.entry_usuario = ctk.CTkEntry(
            form,
            placeholder_text="Usuario",
            width=240,
            height=36
        )
        self.entry_usuario.pack(pady=6)

        # =========================
        # PASSWORD
        # =========================
        frame_pass = ctk.CTkFrame(form, width=240, height=36, fg_color="transparent")
        frame_pass.pack(pady=6)
        frame_pass.pack_propagate(False)

        self.entry_password = ctk.CTkEntry(
            frame_pass,
            placeholder_text="Contraseña",
            show="●"
        )
        self.entry_password.place(x=0, y=0, relwidth=1, relheight=1)

        self.btn_show_password = ctk.CTkButton(
            frame_pass,
            text="👁",
            width=30,
            height=30,
            fg_color="gray",
            hover_color=COLOR_PRINCIPAL,
            command=self.toggle_password
        )

        self.btn_show_password.place(relx=1.0, rely=0.5, anchor="e", x=-8)

        self.entry_password.bind("<Return>", lambda e: self.verificar_login())
        self.entry_usuario.bind("<Return>", lambda e: self.entry_password.focus_set())

        # BOTON
        ctk.CTkButton(
            form,
            text="Ingresar",
            width=160,
            height=36,
            font=(FONT, 14, "bold"),
            fg_color=COLOR_PRINCIPAL,
            hover_color=COLOR_SECUNDARIO,
            command=self.verificar_login
        ).pack(pady=(15, 5))

        # FOOTER
        ctk.CTkLabel(
            form,
            text="INEGI • Sistema de Validación",
            font=(FONT, 10),
            text_color=COLOR_GRIS
        ).pack(pady=(10, 0))

    def toggle_password(self):

        if self.show_password:
            self.entry_password.configure(show="●")
            self.show_password = False
        else:
            self.entry_password.configure(show="")
            self.show_password = True

    # =========================
    # FONDO
    # =========================
    def actualizar_fondo(self, event):

        if event.width < 50 or event.height < 50:
            return

        try:
            img = Image.open("assets/images/fondo_sidebar.jpg")
            img = img.resize((event.width, event.height))

            self.bg_img = ctk.CTkImage(
                light_image=img,
                size=(event.width, event.height)
            )

            if self.bg_label is None:
                self.bg_label = ctk.CTkLabel(self.left, text="")
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.bg_label.configure(image=self.bg_img)

        except Exception as e:
            print("Error fondo:", e)
