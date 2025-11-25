import matplotlib.pyplot as plt
import os
from collections import Counter

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagenes = os.path.join(ruta_base, "Imagenes")
os.makedirs(ruta_imagenes, exist_ok=True)


def calcular(
    diccionario_grados,
    diccionario_clustering,
    diccionario_resul,
    grado_hub,
    clustering_hub,
):
    """
    Crea las gráficas de:
    - Distribución de grados
    - Distribución de coeficientes de clustering
    - Distribución de grados con hubs
    - Distribución de coeficientes de clustering con hubs
    - Gráfica conjunta de grados y coeficientes de clustering.

    Parámetros:
        dicc_grados (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son sus grados.
        diccionario_clustering (dict): Diccionario cuyas keys son nodos y cuyos
                                        values son tuplas con info del coeficiente.
        diccionario_resul (dict): Diccionario donde guardaremos el path de la imagen
                                  resultante.
        grado_hub (int): El valor umbral de grado para los hubs.
        clustering_hub (float): El valor umbral de coeficiente para los hubs.
    """
    grados_clustering(diccionario_grados, diccionario_clustering, diccionario_resul)
    grados_clustering_hubs(
        diccionario_grados,
        diccionario_clustering,
        diccionario_resul,
        grado_hub,
        clustering_hub,
    )
    cnj_grados_clustering(diccionario_grados, diccionario_clustering, diccionario_resul)


def grados_clustering(diccionario_grados, diccionario_clustering, diccionario_resul):
    """
    Crea las gráficas de:
    - Distribución de grados
    - Distribución de coeficientes de clustering
    """
    grafica_grados(diccionario_grados, diccionario_resul)
    grafica_clustering(diccionario_clustering, diccionario_resul)


def grados_clustering_hubs(
    diccionario_grados,
    diccionario_clustering,
    diccionario_resul,
    grado_hub,
    clustering_hub,
):
    """
    Crea las gráficas de:
    - Distribución de grados con hubs
    - Distribución de coeficientes de clustering con hubs
    """
    grafica_grados_con_hubs(diccionario_grados, grado_hub, diccionario_resul)
    grafica_clustering_con_hubs(
        diccionario_clustering, clustering_hub, diccionario_resul
    )


def cnj_grados_clustering(
    diccionario_grados, diccionario_clustering, diccionario_resul
):
    """
    Crea la gráfica conjunta de grados y coeficientes de clustering.
    """
    grafica_conjunta_grados_clustering(
        diccionario_grados, diccionario_clustering, diccionario_resul
    )


def grafica_grados(dicc_grados, diccionario_resul):
    """
    Grafica la distribución de los grados como un histograma
    por cada grado.

    Parámetros:
        dicc_grados (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son us grados.
        diccionario_resul (dict): Diccionario donde guardaremos el path de la imagen
                                  resultante.
    """
    # Obtener los grados de los nodos
    grados = list(dicc_grados.values())

    # Contar la frecuencia de cada grado
    frecuencia_grados = Counter(grados)
    grados_unicos = list(frecuencia_grados.keys())
    frecuencias = list(frecuencia_grados.values())

    # Crear la gráfica
    plt.figure(figsize=(12, 6))
    plt.bar(grados_unicos, frecuencias, color="skyblue", edgecolor="black")
    plt.title("Distribución de los grados de los nodos")
    plt.xlabel("Grado")
    plt.ylabel("Frecuencia")

    # Guardar la gráfica
    nombre_red = diccionario_resul.get("nombre_red", "red_desconocida")
    grafica_path = os.path.join(ruta_imagenes, f"distribucion_grados_{nombre_red}.png")
    diccionario_resul["distribucion_grados"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


def grafica_clustering(diccionario_clustering, diccionario_resul, bins=10):
    """
    Grafica la distribución de los coeficientes de clustering como un histograma
    por cada coeficiente.

    Parámetros:
        diccionario_clustering (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son tuplas con info del coeficiente
                                       de clustering.
        diccionario_resul (dict): Diccionario donde guardaremos el path de la imagen
                                  resultante.
        bins (int): Número de intervalos para el histograma.
    """
    # Extraer todos los coeficientes de clustering
    clustering_coef = [
        diccionario_clustering[nodo][0] for nodo in diccionario_clustering
    ]

    # Crear la figura
    plt.figure(figsize=(12, 6))

    # Histograma de la distribución de los coeficientes de clustering
    plt.hist(clustering_coef, bins=bins, color="lightgreen", edgecolor="black")

    # Personalizar el título y ejes
    plt.title("Distribución de los coeficientes de clustering")
    plt.xlabel("Coeficiente de Clustering")
    plt.ylabel("Frecuencia")

    # Guardar la gráfica
    nombre_red = diccionario_resul.get("nombre_red", "red_desconocida")
    grafica_path = os.path.join(
        ruta_imagenes, f"distribucion_clustering_{nombre_red}.png"
    )
    diccionario_resul["distribucion_clustering"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


def grafica_grados_con_hubs(dicc_grados, corte_hub, diccionario_resul):
    """
    Grafica la distribución de los grados como un histograma
    por cada grado. Los nodos que superen un umbral se mostrarán en rojo.

    Parámetros:
        dicc_grados (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son us grados.
        diccionario_resul (dict): Diccionario donde guardaremos el path de la imagen
                                  resultante.
        corte_hub (int): El valor umbral para los hubs.
    """
    # Obtener los grados de los nodos
    grados = list(dicc_grados.values())

    # Contar la frecuencia de cada grado
    frecuencia_grados = Counter(grados)

    # Separar grados en dos grupos: hubs y no hubs
    grados_unicos = list(frecuencia_grados.keys())
    frecuencias = list(frecuencia_grados.values())

    colores = ["red" if g >= corte_hub else "blue" for g in grados_unicos]

    # Crear la gráfica de barras
    plt.figure(figsize=(12, 6))
    plt.bar(grados_unicos, frecuencias, color=colores, edgecolor="black")
    plt.title("Distribución de los grados de los nodos identificando hubs")
    plt.xlabel("Grado")
    plt.ylabel("Frecuencia")

    # Guardar la gráfica
    nombre_red = diccionario_resul.get("nombre_red", "red_desconocida")
    grafica_path = os.path.join(
        ruta_imagenes, f"distribucion_grados_hubs_{nombre_red}.png"
    )
    diccionario_resul["distribucion_grados_hubs"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


def grafica_clustering_con_hubs(
    diccionario_clustering, umbral, diccionario_resul, bins=10
):
    """
    Grafica la distribución de los coeficientes de clustering como un histograma
    por cada coeficiente. Los coeficientes que superen un umbral se mostrarán en
    rojo.

    Parámetros:
        diccionario_clustering (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son tuplas con info del coeficiente
                                       de clustering.
        diccionario_resul (dict): Diccionario donde guardaremos el path de la imagen
                                  resultante.
        bins (int): Número de bins intervalos para el histograma.
        umbral (float): El valor umbral para cambiar el color a rojo.
    """
    # Extraer todos los coeficientes de clustering
    clustering_coef = [
        diccionario_clustering[nodo][0] for nodo in diccionario_clustering
    ]

    # Separar los coeficientes en dos grupos según el umbral
    coeficientes_rojos = [coef for coef in clustering_coef if coef > umbral]
    coeficientes_normales = [coef for coef in clustering_coef if coef <= umbral]

    # Crear la figura
    plt.figure(figsize=(12, 6))

    # Histograma de los coeficientes normales (en color verde)
    plt.hist(
        coeficientes_normales,
        bins=bins,
        color="lightgreen",
        edgecolor="black",
        label="Coef. < umbral",
    )

    # Histograma de los coeficientes que superan el umbral (en color rojo)
    plt.hist(
        coeficientes_rojos,
        bins=bins,
        color="red",
        edgecolor="black",
        label="Coef. > umbral",
    )

    # Personalizar el título y ejes
    plt.title("Distribución de los coeficientes de clustering distinguiendo hubs")
    plt.xlabel("Coeficiente de Clustering")
    plt.ylabel("Frecuencia")
    plt.legend()

    # Guardar la gráfica
    nombre_red = diccionario_resul.get("nombre_red", "red_desconocida")
    grafica_path = os.path.join(
        ruta_imagenes, f"distribucion_clustering_hubs_{nombre_red}.png"
    )
    diccionario_resul["distribucion_clustering_hubs"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


def grafica_conjunta_grados_clustering(
    diccionario_grados, diccionario_clustering, diccionario_resul
):
    """
    Grafica la que representa un nodo con su grado en el eje x y su coeficiente
    de clústering en el y.

    Parámetros:
        dicc_grados (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son us grados.
        diccionario_clustering (dict): Diccionario cuyas keys son nodos y cuyos
                                       values son tuplas con info del coeficiente
                                       de clustering.
        diccionario_resul (dict): Diccionario donde guardaremos el path de la imagen
                                  resultante.
    """
    nodos = list(diccionario_grados.keys())
    grados = [diccionario_grados[nodo] for nodo in nodos]
    clustering_coef = [diccionario_clustering[nodo][0] for nodo in nodos]
    plt.figure(figsize=(12, 6))
    plt.scatter(grados, clustering_coef, alpha=0.6)
    plt.title("Gráfica conjunta de Grados y Coeficientes de Clustering")
    plt.xlabel("Grado")
    plt.ylabel("Coeficiente de Clustering")
    nombre_red = diccionario_resul.get("nombre_red", "red_desconocida")
    grafica_path = os.path.join(
        ruta_imagenes, f"cnj_grados_clustering_{nombre_red}.png"
    )
    diccionario_resul["cnj_grados_clustering"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()
