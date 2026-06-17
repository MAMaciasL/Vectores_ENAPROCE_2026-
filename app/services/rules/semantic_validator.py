from sentence_transformers import SentenceTransformer, util
import unicodedata

modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


def limpiar(texto):
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto


def es_semanticamente_similar(texto, catalogo, umbral=0.65):

    if not texto:
        return False, None, 0

    texto = limpiar(texto)

    emb_texto = modelo.encode(texto, convert_to_tensor=True)

    catalogo_limpio = [limpiar(x) for x in catalogo]

    emb_catalogo = modelo.encode(catalogo_limpio, convert_to_tensor=True)

    similitudes = util.cos_sim(emb_texto, emb_catalogo)[0]

    max_index = similitudes.argmax().item()
    max_score = similitudes[max_index].item()

    mejor_opcion = catalogo[max_index]

    if max_score >= umbral:
        return True, mejor_opcion, max_score

    return False, mejor_opcion, max_score