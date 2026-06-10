from tkinter import messagebox
import customtkinter as ctk
from config import *
from services.config_service import guardar_config, cargar_config


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

        self.slider = ctk.CTkSlider(self, from_=0, to=1, number_of_steps=20)
        self.slider.set(self.cfg.get("umbral_semantico", 0.5))
        self.slider.pack(pady=10)

        # TEMA
        ctk.CTkLabel(self, text="Modo de tema").pack()

        self.tema = ctk.CTkOptionMenu(
            self,
            values=["Claro", "Oscuro"]
        )
        self.tema.set(self.cfg.get("tema", "Claro"))
        self.tema.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Guardar",
            command=self.guardar
        ).pack()

    def guardar(self):

        self.cfg["umbral_semantico"] = self.slider.get()
        self.cfg["tema"] = self.tema.get()

        guardar_config(self.cfg)

        if self.tema.get() == "Oscuro":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

        messagebox.showinfo("Guardado", "Configuración guardada correctamente")