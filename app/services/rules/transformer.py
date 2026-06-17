def transformar_condicion(cond):
    if cond is None:
        return ""

    cond = str(cond)

    cond = cond.replace("<>", "!=")
    cond = cond.replace("=", "==")
    cond = cond.replace("\n", " and ")
    cond = cond.replace("AND", "and")
    cond = cond.replace("OR", "or")
    cond = cond.replace("NULL", "None")

    return cond