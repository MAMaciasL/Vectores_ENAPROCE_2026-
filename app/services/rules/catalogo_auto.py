import re


def limpiar_texto(texto):
    return str(texto).strip().upper()


def extraer_opciones(algoritmo):

    if not algoritmo:
        return []

    return list(set(re.findall(r"'([^']+)'", str(algoritmo))))


def construir_catalogos_desde_vectores(vectores_df):

    catalogos = {}

    for _, row in vectores_df.iterrows():

        algoritmo = row.get("ALGORITMO_LOGICA_NEGOCIO") or row.get("ALGORITMO")
        variables = row.get("VARIABLES")

        if not algoritmo or not variables:
            continue

        variables = limpiar_texto(variables)
        opciones = extraer_opciones(algoritmo)

        if not opciones:
            continue

        for var in variables.split():

            var = var.strip()

            if var not in catalogos:
                catalogos[var] = set()

            catalogos[var].update(opciones)

    return {k: list(v) for k, v in catalogos.items()}