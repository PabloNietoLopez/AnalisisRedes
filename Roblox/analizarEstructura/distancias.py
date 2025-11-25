import matplotlib.pyplot as plt
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagenes = os.path.join(ruta_base, "Imagenes")
os.makedirs(ruta_imagenes, exist_ok=True)


def calcular(diccionario, diccionario_grados, diccionario_resul, grado_hub):
    """
    Calcula:
    - Distancia media entre nodos.
    - Diámetro de la red.
    - Distribución de distancias desde los hubs.

    Parámetros:
        diccionario (dict): Diccionario de nodos y sus vecinos.
        dicc_grados (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son sus grados.
        diccionario_resul (dict): Diccionario donde guardaremos el path de la imagen
                                  resultante.
        grado_hub (int): El valor umbral de grado para los hubs.
    """
    media = media_distancia(diccionario, diccionario_resul)
    print(f"La distancia media entre nodos es de {media:.2f}.")

    diametro = calculo_diametro(diccionario, diccionario_resul)
    print(f"El diámetro de la red es de {diametro}.")

    distribucion_distancias(
        diccionario, diccionario_grados, diccionario_resul, grado_hub
    )


def media_distancia(diccionario, diccionario_resul):
    """
    Calcula la distancia media entre nodos: calcular_distancia_media()
    Guarda los resultados en el diccionario de resultados.
    """
    dist_media = calcular_distancia_media(diccionario)
    diccionario_resul["distancia_media"] = dist_media
    return dist_media


def calculo_diametro(diccionario, diccionario_resul):
    """
    Calcula la el diámetro del grafo: calcular_diametro()
    Guarda los resultados en el diccionario de resultados.
    """
    diametro = calcular_diametro(diccionario)
    diccionario_resul["diametro"] = diametro
    return diametro


def distribucion_distancias(
    diccionario, diccionario_grados, diccionario_resul, grado_hub
):
    distribucion_distancias = calcular_distribucion_distancias(
        diccionario, diccionario_grados, diccionario_resul, grado_hub
    )


def calcular_distancia_media(diccionario):
    """
    Calcula la distancia media entre nodos.

    Parámetros:
        diccionario (dict): Diccionario de nodos y sus vecinos.
    """
    nodos = list(diccionario.keys())
    suma_distancias = 0
    total_pares = 0
    visitados_global = set()
    for nodo in nodos:
        if nodo in visitados_global:
            continue
        distancias, visitados_local = bfs(diccionario, nodo)
        visitados_global.update(visitados_local)
        suma_distancias += sum(distancias.values())
        total_pares += len(distancias) - 1
    if total_pares > 0:
        distancia_media = suma_distancias / total_pares
    else:
        distancia_media = 0
    return distancia_media


def calcular_diametro(diccionario):
    """
    Calcula el diámetro de la red.

    Parámetros:
        diccionario (dict): Diccionario de nodos y sus vecinos.
    """
    nodos = list(diccionario.keys())
    max_distancia = 0
    visitados_global = set()
    for nodo in nodos:
        if nodo in visitados_global:
            continue
        distancias, visitados_local = bfs(diccionario, nodo)
        visitados_global.update(visitados_local)
        max_distancia = max(max_distancia, max(distancias.values()))
    return max_distancia


def calcular_distribucion_distancias(
    diccionario, dicc_grado, diccionario_resul, umbral_hub
):
    """
    Calcula las distancias entre los hubs a partir de un valor específico de grado: bfs()
    Crea un histograma con la distribución de distancias entre los hubs: graficar_histograma_distancias()

    Parámetros:
        diccionario (dict): Diccionario de nodos y sus vecinos.
        dicc_grado (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son sus grados.
        diccionario_resul (dict): Diccionario donde guardaremos el path de la imagen
                                    resultante.
        umbral_hub (int): El valor umbral de grado para identificar los hubs.
    """
    hubs = [nodo for nodo, grado in dicc_grado.items() if grado >= umbral_hub]
    if not hubs:
        print("No se encontraron hubs con el umbral especificado.")
        return None
    print(f"Hubs identificados: {hubs}")
    distancias_globales = []
    for hub in hubs:
        distancias, _ = bfs(diccionario, hub)
        distancias_globales.extend(distancias.values())
    graficar_histograma_distancias(distancias_globales, diccionario_resul)
    return distancias_globales


def graficar_histograma_distancias(
    distancias, diccionario_resul, titulo="Distribución de distancias desde los hubs"
):
    """
    Crea un histograma con la distribución de distancias entre los hubs.
    """
    plt.figure(figsize=(12, 6))
    plt.hist(
        distancias, bins=range(1, max(distancias) + 2), edgecolor="black", alpha=0.7
    )
    plt.title(titulo)
    plt.xlabel("Distancia")
    plt.ylabel("Frecuencia")
    nombre_red = diccionario_resul.get("nombre_red", "red_sin_nombre")
    grafica_path = os.path.join(
        ruta_imagenes, f"distribucion_distancias_{nombre_red}.png"
    )
    diccionario_resul["distribucion_distancias"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


def bfs(diccionario, nodo_inicial):
    """
    Realiza un recorrido en anchura (BFS) desde un nodo inicial.
    """
    visitados = set()
    distancias = {nodo_inicial: 0}
    cola = [nodo_inicial]
    while cola:
        nodo = cola.pop(0)
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in diccionario[nodo]:
                if vecino not in distancias:
                    distancias[vecino] = distancias[nodo] + 1
                    cola.append(vecino)
    return distancias, visitados
