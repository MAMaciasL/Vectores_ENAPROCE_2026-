import re

def transformar_condicion(cond):
    if cond is None:
        return ""

    cond = str(cond)

    cond = cond.replace("<>", "!=")
    cond = re.sub(r'(?<![!<>=])=(?!=)', '==', cond)

    cond = cond.replace("\n", " and ")
    cond = cond.replace("AND", "and")
    cond = cond.replace("OR", "or")

    cond = cond.replace("NULL", "None")
    cond = cond.replace("!= None", "is not None")
    cond = cond.replace("== None", "is None")


    return cond