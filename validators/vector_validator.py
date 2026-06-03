from validators.text_validator import *
from validators.semantic_validator import *


def validar_otro(
    errores,
    texto,
    variable,
    vector,
    catalogo,
    descripcion
):

    if esta_vacio(texto):

        errores.append({
            "vector": vector,
            "variable": variable,
            "mensaje": f"No especificó {descripcion}"
        })

        return

    # LONGITUD MAXIMA
    if not longitud_valida(texto, 60):

        errores.append({
            "vector": vector,
            "variable": variable,
            "mensaje": "Supera la longitud máxima"
        })

    # LONGITUD MINIMA
    if not longitud_minima(texto, 6):

        errores.append({
            "vector": vector,
            "variable": variable,
            "mensaje": "Longitud mínima no alcanzada"
        })

    # TEXTO BASURA
    if texto_basura(texto):

        errores.append({
            "vector": vector,
            "variable": variable,
            "mensaje": "Texto inválido"
        })

    # SOLO NUMEROS
    if solo_numeros(texto):

        errores.append({
            "vector": vector,
            "variable": variable,
            "mensaje": "No puede contener solo números"
        })

    # CARACTERES INVALIDOS
    if caracteres_invalidos(texto):

        errores.append({
            "vector": vector,
            "variable": variable,
            "mensaje": "Contiene caracteres inválidos"
        })

    # SEMANTICA
    similar, opcion, _ = es_semanticamente_similar(
        texto,
        catalogo
    )

    if similar:

        errores.append({
            "vector": vector,
            "variable": variable,
            "mensaje": f"La respuesta es similar a '{opcion}'"
        })


def validar_vector_6(fila, errores):

    def valor_numerico(valor):
        try:
            return int(float(valor))
        except:
            return None

    p6_1 = valor_numerico(fila.get("P6_1"))
    p6_4_1 = valor_numerico(fila.get("P6_4_1"))
    p6_4_2 = valor_numerico(fila.get("P6_4_2"))

    # =====================================================
    # VECTOR 06I01
    # =====================================================
    if p6_1 == 1:
        if p6_4_1 is None or p6_4_1 <= 0:
            errores.append({
                "vector": "E_ENAPROCE_06I01",
                "variable": "P6_4_1",
                "mensaje": "Reconsulta: Hombre con porcentaje de propiedad en 0"
            })

    # =====================================================
    # VECTOR 06I02
    # =====================================================
    if p6_1 == 2:
        if p6_4_2 is None or p6_4_2 <= 0:
            errores.append({
                "vector": "E_ENAPROCE_06I02",
                "variable": "P6_4_2",
                "mensaje": "Reconsulta: Mujer con porcentaje de propiedad en 0"
            })

