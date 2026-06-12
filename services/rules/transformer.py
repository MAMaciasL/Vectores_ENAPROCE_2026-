import re

def variables_en_condicion(cond):
    return re.findall(r'\bP[A-Z0-9_]+\b', cond)

def transformar_condicion(cond):

    if cond is None:
        return ""

    cond = str(cond).upper()

    cond = cond.replace("<>", "!=")

    cond = re.sub(r'(?<!!|>|=)=(?!=)', '==', cond)

    cond = cond.replace("\n", " and ")
    cond = cond.replace("AND", "and")
    cond = cond.replace("OR", "or")

    cond = cond.replace("NULL", "None")

    return cond