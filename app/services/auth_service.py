import json
import os
from app.utils.path_utils import resource_path

RUTA = resource_path("data/usuarios.json")


def cargar_usuarios():
    if os.path.exists(RUTA):
        with open(RUTA, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def validar_usuario(usuario, password):

    usuarios = cargar_usuarios()

    if usuario in usuarios:

        password_guardado = usuarios[usuario]["password"]

        if password == password_guardado:
            return True, usuarios[usuario]

    return False, None
