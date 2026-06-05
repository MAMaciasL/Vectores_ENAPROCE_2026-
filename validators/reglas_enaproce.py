import pandas as pd

from validators.text_validator import *
from validators.semantic_validator import *
from validators.catalogs import *
from validators.vector_validator import * 

def validar_registro(fila):

    errores = []

    def valor_numerico(valor):

        try:
            return int(float(valor))
        except:
            return None
        
    # =====================================================
    # VECTOR 02O01
    # =====================================================

    valor = valor_numerico(fila.get("P2_9"))

    if valor is not None and valor > 0:

        validar_otro(
            errores=errores,
            texto=fila.get("P2_9X"),
            variable="P2_9X",
            vector="E_ENAPROCE_02O01",
            catalogo=FUENTES_CAPITAL,
            descripcion="otra fuente de capital"
        )

    # =====================================================
    # VECTOR 03O01
    # =====================================================
    
    valores_p3 = [
    valor_numerico(fila.get("P3_1")),
    valor_numerico(fila.get("P3_2")),
    valor_numerico(fila.get("P3_3"))
]

    if 19 in valores_p3:

        validar_otro(
            errores=errores,
            texto=fila.get("P3_19X"),
            variable="P3_19X",
            vector="E_ENAPROCE_03O01",
            catalogo=FACTORES_UBICACION,
            descripcion="otro factor de ubicación"
    )

    # =====================================================
    # VECTOR 04O01
    # =====================================================

    valor = valor_numerico(fila.get("P4"))

    if valor is not None and valor == 9:

        validar_otro(
            errores=errores,
            texto=fila.get("P4_9X"),
            variable="P4_9X",
            vector="E_ENAPROCE_04O01",
            catalogo=PROPIETARIOS_ACCIONISTAS,
            descripcion="otro(as) propietarios(as) o accionistas mayoristas(as)"
        )

    # =====================================================
    # VECTOR 05O01
    # =====================================================

    valor = valor_numerico(fila.get("P5"))

    if valor is not None and valor == 9:

        validar_otro(
            errores=errores,
            texto=fila.get("P5_9X"),
            variable="P5_9X",
            vector="E_ENAPROCE_05O01",
            catalogo=PERSONAS_QUE_TOMAN_DECISIONES,
            descripcion="otro(a) quien toma las decisiones de la empresa"
        )

    # =====================================================
    # VECTOR 06I01
    # =====================================================

    p6_1 = valor_numerico(fila.get("P6_1"))
    p6_4_1 = valor_numerico(fila.get("P6_4_1"))

    if p6_1 is not None and p6_1 == 1:
        if p6_4_1 is None or p6_4_1 <= 0:
            errores.append({
                "vector": "E_ENAPROCE_06I01",
                "variable": "P6_4_1",
                "mensaje": "Inconsistencia: hombre con propiedad en 0"
            })

    # =====================================================
    # VECTOR 06I02
    # =====================================================
    p6_4_2 = valor_numerico(fila.get("P6_4_2"))

    if p6_1 == 2:
        if p6_4_2 is None or p6_4_2 <= 0:
            errores.append({
                "vector": "E_ENAPROCE_06I02",
                "variable": "P6_4_2",
                "mensaje": "Inconsistencia: mujer con propiedad en 0"
            })

    return errores
