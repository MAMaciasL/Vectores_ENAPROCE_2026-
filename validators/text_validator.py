import pandas as pd
import re


def esta_vacio(valor):

    return pd.isna(valor) or str(valor).strip() == ""

def longitud_valida(texto, maximo):

    return len(str(texto).strip()) <= maximo

def longitud_minima(texto, minimo):

    return len(str(texto).strip()) >= minimo

def texto_basura(texto):

    texto = str(texto).strip().lower()

    if len(set(texto)) <= 2 and len(texto) >= 5:
        return True

    basura = [
        "na",
        "n/a",
        "asdf",
        "xxx",
        ".",
        "-",
        "  ",
        " ",
        "hhhhhhhh",
        "aaaaaaa",
        "xxxxxxx",
        "........",
        "-------",
        "asdf",
        "qwerty",
        "xxxx",
        "aaaa",
        "bbbb",
        "hhhh"
    ]

    return texto in basura


def solo_numeros(texto):

    return str(texto).strip().isdigit()


def caracteres_invalidos(texto):

    patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,()-]+$"

    return not bool(re.match(patron, str(texto)))