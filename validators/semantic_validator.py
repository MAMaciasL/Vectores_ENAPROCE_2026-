from sentence_transformers import SentenceTransformer, util
import unicodedata

modelo = SentenceTransformer(
    'paraphrase-multilingual-MiniLM-L12-v2'
)

def limpiar(texto):

    texto = str(texto).lower().strip()

    texto = unicodedata.normalize(
        'NFKD',
        texto
    )

    texto = texto.encode(
        'ascii',
        'ignore'
    ).decode('utf-8')

    return texto


def es_semanticamente_similar(
    texto,
    catalogo,
    umbral=0.55
):

    texto = limpiar(texto)

    emb_texto = modelo.encode(
        texto,
        convert_to_tensor=True
    )

    for opcion in catalogo:

        opcion_limpia = limpiar(opcion)

        emb_opcion = modelo.encode(
            opcion_limpia,
            convert_to_tensor=True
        )

        similitud = util.cos_sim(
            emb_texto,
            emb_opcion
        ).item()

        if similitud >= umbral:

            return True, opcion, similitud

    return False, None, 0