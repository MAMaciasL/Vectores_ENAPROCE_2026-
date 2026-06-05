from tkinter import messagebox

import customtkinter as ctk
from config import *
from services.config_service import *


class ConfigView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color="transparent")

        self.cfg = cargar_config()

        ctk.CTkLabel(
            self,
            text="Configuración",
            font=(FONT, 20, "bold")
        ).pack(pady=10)

        # UMBRAL
        ctk.CTkLabel(self, text="Umbral semántico").pack()

        self.slider = ctk.CTkSlider(
            self,
            from_=0,
            to=1,
            number_of_steps=20
        )
        self.slider.set(self.cfg["umbral_semantico"])
        self.slider.pack(pady=10)

        # BOTON GUARDAR
        ctk.CTkButton(
            self,
            text="Guardar",
            command=self.guardar
        ).pack()

    def guardar(self):

        self.cfg["umbral_semantico"] = self.slider.get()
        guardar_config(self.cfg)
        messagebox.showinfo("Guardado", "Configuración guardada correctamente")