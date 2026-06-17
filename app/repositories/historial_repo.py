import json
import os
from app.utils.path_utils import resource_path

HISTORIAL_PATH = resource_path("data/historial_reportes.json")

def cargar_historial():
    if not os.path.exists(HISTORIAL_PATH):
        return []

    try:
        with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_historial(historial):
    os.makedirs(os.path.dirname(HISTORIAL_PATH), exist_ok=True)

    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)