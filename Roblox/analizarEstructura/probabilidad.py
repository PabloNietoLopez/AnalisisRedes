def calcular(diccionario_grados, diccionario_resul):
    """
    Calcula:
    - Probabilidad de enlace.
    - Esperanza de grado.
    - Varianza de grado.

    Parámetros:
        diccionario_grados (dict): Diccionario de nodos y sus grados.
        diccionario_resul (dict): Diccionario donde guardaremos los resultados.
    """
    pr, esp, var = probabilidad(diccionario_grados, diccionario_resul)
    print(f"La probabilidad de enlace es de {pr:.5f}.")
    print(f"La esperanza de grado es de {esp:.2f}.")
    print(f"La varianza de grado es de {var:.2f}.")


def probabilidad(diccionario_grados, diccionario_resul):
    """
    Calcula la probabilidad de enlace, la esperanza de grado y la varianza de grado.
    """
    nodos = diccionario_resul["num_nodos"]
    aristas = diccionario_resul["num_aristas"]

    pr = calcular_probabilidad_enlace(nodos, aristas)
    esperanza = calcular_esperanza_grado(diccionario_grados)
    varianza = calcular_varianza_grado(diccionario_grados, esperanza)

    diccionario_resul["esperanza"] = esperanza
    diccionario_resul["varianza"] = varianza
    diccionario_resul["probabilidad"] = pr

    return pr, esperanza, varianza


def calcular_esperanza_grado(diccionario_grados):
    grados = list(diccionario_grados.values())
    return sum(grados) / len(grados)


def calcular_probabilidad_enlace(nodos, aristas):
    if nodos <= 1:
        print("La probabilidad de enlace no está definida para grafos con 0 o 1 nodo.")
        return 0
    return (2 * aristas) / (nodos * (nodos - 1))


def calcular_varianza_grado(diccionario_grados, esperanza):
    grados = list(diccionario_grados.values())
    return sum((grado - esperanza) ** 2 for grado in grados) / len(grados)
