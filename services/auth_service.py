import json
import os

RUTA = "data/usuarios.json"


def cargar_usuarios():
    if os.path.exists(RUTA):
        with open(RUTA, "r") as f:
            return json.load(f)
    return {}


def validar_usuario(usuario, password):

    usuarios = cargar_usuarios()

    if usuario in usuarios:

        password_guardado = usuarios[usuario]["password"]

        # ✅ COMPARACIÓN DIRECTA (SIN HASH)
        if password == password_guardado:
            return True, usuarios[usuario]

    return False, None