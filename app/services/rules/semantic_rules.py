from app.services.rules.semantic_validator import es_semanticamente_similar
from app.validators.catalogo_validator import FUENTES_CAPITAL

def validar_otro_fuentes(row):

    valor = row.get("P2_9X")

    if not valor:
        return None

    es_valido, opcion, score = es_semanticamente_similar(
        valor,
        FUENTES_CAPITAL
    )

    if not es_valido:
        return {
            "error": True,
            "campo": "P2_9X",
            "mensaje": f"No reconocido: '{valor}' → parecido a '{opcion}'",
            "score": score
        }

    return {
        "error": False,
        "campo": "P2_9X",
        "mensaje": f"'{valor}' interpretado como '{opcion}'",
        "score": score
    }