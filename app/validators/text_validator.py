import pandas as pd
import re


def esta_vacio(valor):
    return pd.isna(valor) or str(valor).strip() == ""


def longitud_valida(texto, maximo):
    return len(str(texto).strip()) <= maximo


def longitud_minima(texto, minimo):
    return len(str(texto).strip()) >= minimo


def es_ruido_semantico(texto):

    texto = str(texto).strip().lower()

    frases_basura = [
        "hola", "hola buen dia", "buen dia",
        "prueba", "pruebas", "test",
        "ok", "bien", "ninguno", "nada",
        "no aplica", "no tengo", "no se"
    ]

    if any(texto.startswith(f) for f in frases_basura):
        return True

    # palabras repetidas tipo "hola hola hola"
    palabras = texto.split()
    if len(set(palabras)) == 1 and len(palabras) >= 3:
        return True

    return False


def texto_basura(texto):

    texto = str(texto).strip().lower()

    # cadenas repetidas tipo "aaaaaaa"
    if len(set(texto)) <= 2 and len(texto) >= 5:
        return True

    # solo símbolos
    if re.fullmatch(r"[^\w\s]+", texto):
        return True

    basura = [
        "na", "n/a", "asdf", "xxx",
        ".", "-", " ",
        "qwerty"
    ]

    return texto in basura


def solo_numeros(texto):
    return str(texto).strip().isdigit()


def caracteres_invalidos(texto):

    texto = str(texto)

    patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,()-]+$"

    if not bool(re.match(patron, texto)):
        return True

    if re.fullmatch(r"[0-9\s]+", texto):
        return True

    return False