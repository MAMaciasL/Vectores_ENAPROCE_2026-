import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os

# =========================
# CONFIGURACIÓN
# =========================
USUARIO = "admin"
PASSWORD = "1234"

# Colores estilo INEGI
COLOR_FONDO = "#F4F6F9"
COLOR_VERDE = "#000000"
COLOR_GRIS = "#4D4D4D"
COLOR_BOTON = "#003CFF"
COLOR_BOTON_HOVER = "#00A86B"

# FUNCIÓN LOGIN
def verificar_login():
    usuario = entrada_usuario.get()
    password = entrada_password.get()

    if usuario == USUARIO and password == PASSWORD:
        messagebox.showinfo("Acceso correcto", "Bienvenido al sistema")

        ventana.destroy()

        # Ejecutar app.py
        os.system("python app.py")

    else:
        messagebox.showerror(
            "Error",
            "Usuario o contraseña incorrectos"
        )

# EFECTO HOVER BOTÓN
def on_enter(e):
    boton_login["background"] = COLOR_BOTON_HOVER

def on_leave(e):
    boton_login["background"] = COLOR_BOTON

# VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("INEGI - Inicio de Sesión")
ventana.geometry("600x500")
ventana.configure(bg=COLOR_FONDO)
ventana.resizable(False, False)

frame = tk.Frame(
    ventana,
    bg="white",
    bd=2,
    relief="solid"
)
frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=420)

# LOGO INEGI
try:
    imagen = Image.open("logo_inegi.png")
    imagen = imagen.resize((140, 50))

    logo = ImageTk.PhotoImage(imagen)

    label_logo = tk.Label(
        frame,
        image=logo,
        bg="white"
    )
    label_logo.pack(pady=20)

except:
    label_logo = tk.Label(
        frame,
        text="LOGO INEGI",
        font=("Arial", 20, "bold"),
        fg=COLOR_VERDE,
        bg="white"
    )
    label_logo.pack(pady=20)

# TÍTULO
titulo = tk.Label(
    frame,
    text="Inicio de Sesión",
    font=("Arial", 22, "bold"),
    fg=COLOR_VERDE,
    bg="white"
)
titulo.pack(pady=10)

# USUARIO
label_usuario = tk.Label(
    frame,
    text="Usuario",
    font=("Arial", 12),
    fg=COLOR_GRIS,
    bg="white"
)
label_usuario.pack(pady=(20, 5))

entrada_usuario = tk.Entry(
    frame,
    font=("Arial", 14),
    width=25,
    bd=2
)
entrada_usuario.pack(ipady=5)

# PASSWORD
label_password = tk.Label(
    frame,
    text="Contraseña",
    font=("Arial", 12),
    fg=COLOR_GRIS,
    bg="white"
)
label_password.pack(pady=(20, 5))

entrada_password = tk.Entry(
    frame,
    font=("Arial", 14),
    width=25,
    show="*",
    bd=2
)
entrada_password.pack(ipady=5)

# BOTÓN LOGIN
boton_login = tk.Button(
    frame,
    text="INGRESAR",
    font=("Arial", 13, "bold"),
    bg=COLOR_BOTON,
    fg="white",
    activebackground=COLOR_BOTON_HOVER,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=20,
    height=2,
    command=verificar_login
)

boton_login.pack(pady=35)

# Hover
boton_login.bind("<Enter>", on_enter)
boton_login.bind("<Leave>", on_leave)

# FOOTER
footer = tk.Label(
    ventana,
    text="Instituto Nacional de Estadística y Geografía",
    font=("Arial", 10),
    fg=COLOR_GRIS,
    bg=COLOR_FONDO
)
footer.pack(side="bottom", pady=10)

# EJECUTAR
ventana.mainloop()