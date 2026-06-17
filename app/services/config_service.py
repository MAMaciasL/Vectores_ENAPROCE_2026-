import json
import os

RUTA = "data/config.json"

DEFAULT = {
    "tema": "light",
    "umbral_semantico": 0.55
}


def cargar_config():
    if os.path.exists(RUTA):
        with open(RUTA, "r") as f:
            return json.load(f)
    return DEFAULT


def guardar_config(cfg):
    os.makedirs("data", exist_ok=True)
    with open(RUTA, "w") as f:
        json.dump(cfg, f, indent=4)