import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp
import random
import os
from estructura import generar_diccionario
import warnings

# Silenciar warnings específicos (ES UN WARNING PARA LOS CARACTERES CHINOS, NO UN ERROR)
warnings.filterwarnings("ignore", category=UserWarning, message=".*Glyph.*missing.*")
diccionario = {}  # Diccionario que contiene la lista de adyacencia
diccionario_grados = {}  # Diccionario con los grados de los nodos
diccionario_clustering = (
    {}
)  # Diccionario con los coeficientes de clustering de los nodos
diccionario_resul = {}  # Diccionario con los resultados del análisis para el informe
edges = []  # Lista de aristas


# FUNCIÓN DE ENLACE CON EL MAIN
def analizar_estructura():
    # generar_informe_introduccion.generar_resultados()
    ruta_json = os.path.join(os.getcwd(), "analizarHTML", "dataset.json")
    grafo = generar_diccionario.crear_grafo(ruta_json)

    if grafo:
        global diccionario
        diccionario = generar_diccionario.crear_diccionario(grafo)
        global edges
        edges = obtener_aristas(diccionario)
        global diccionario_grados
        diccionario_grados = generar_diccionario.crea_diccionario_grado_nodos(
            diccionario
        )
        global diccionario_clustering
        diccionario_clustering = generar_diccionario.crea_diccionario_clustering(
            diccionario
        )
    nodos_aristas()
    grados_clustering()
    grados_clustering_hubs()
    cnj_grados_clustering()
    visualizacion(grafo)
    media_distancia()
    calculo_diametro()
    distribucion_distancias()
    probabilidad()
    salir()


# FUNCIONES PARA EL MENÚ
def obtener_aristas(diccionario_ady):
    aristas = []

    # Recorremos el diccionario de adyacencia para obtener las aristas
    for nodo, vecinos in diccionario_ady.items():
        for vecino in vecinos:
            # Añadir la arista (nodo, vecino) si no está ya añadida (para evitar duplicados)
            if (vecino, nodo) not in aristas:
                aristas.append((nodo, vecino))

    return aristas


def nodos_aristas():
    nodos = len(diccionario)
    print(f"El número de nodos en la red es: {nodos}")
    aristas = len(edges)
    print(f"El número de aristas en la red es: {aristas}")
    # Se añaden para el informe
    global diccionario_resul
    diccionario_resul["num_nodos"] = nodos
    diccionario_resul["num_aristas"] = aristas


def grados_clustering():
    grafica_grados(diccionario_grados)
    grafica_clustering(diccionario_clustering)


def grados_clustering_hubs():
    grafica_grados_con_hubs(diccionario_grados)
    grafica_clustering_con_hubs(diccionario_clustering)


def cnj_grados_clustering():
    grafica_conjunta_grados_clustering(diccionario_grados, diccionario_clustering)


def visualizacion(grafo):
    visualizar_red(grafo)


def media_distancia():
    dist_media = calcular_distancia_media(diccionario)
    print(f"La distancia media de la red es: {dist_media}")
    global diccionario_resul
    diccionario_resul["distancia_media"] = dist_media


def calculo_diametro():
    diametro = calcular_diametro(diccionario)
    print(f"El diámetro de la red es: {diametro}")
    global diccionario_resul
    diccionario_resul["diametro"] = diametro


def distribucion_distancias():
    distribucion_distancias1 = calcular_distribucion_distancias(diccionario_grados)
    global diccionario_resul
    diccionario_resul["distribucion_distancias1"] = distribucion_distancias1


def probabilidad():
    nodos = len(diccionario)
    aristas = len(edges)
    pr = calcular_probabilidad_enlace(nodos, aristas)
    print(f"La probabilidad de enlace de la red es: {pr}")
    esperanza = calcular_esperanza_grado(diccionario_grados)
    print(f"La esperanza del grado de la red es: {esperanza}")
    varianza = calcular_varianza_grado(diccionario_grados, esperanza)
    print(f"La varianza del grado de la red es: {varianza}")
    global diccionario_resul
    diccionario_resul["esperanza"] = esperanza
    diccionario_resul["varianza"] = varianza
    diccionario_resul["probabilidad"] = pr


def salir():
    return diccionario_resul


# FUNCIONES PARA EL ANÁLISIS
def grafica_grados(dicc_grados):
    # Crear listas para nodos y sus grados
    nodos = list(dicc_grados.keys())
    grados = list(dicc_grados.values())
    # Crear el gráfico de dispersión
    plt.figure(figsize=(12, 6))
    plt.scatter(nodos, grados)
    plt.title("Distribución de los grados de los nodos")
    plt.xlabel("Nodo")
    plt.ylabel("Grado")
    global diccionario_resul
    archivo_grafico = f"analizarEstructura/distribucion_grados.png"
    diccionario_resul["distribucion_grados"] = archivo_grafico
    plt.savefig(archivo_grafico)
    plt.show()


def grafica_grados_con_hubs(dicc_grados):
    corte_hub = int(
        input("Introduce el valor a partir del cual un nodo se considera hub: ")
    )
    # Crear listas para nodos y sus grados
    nodos = list(dicc_grados.keys())
    grados = list(dicc_grados.values())
    # Crear el gráfico de dispersión
    plt.figure(figsize=(12, 6))
    for n, g in zip(nodos, grados):
        if g >= corte_hub:
            plt.scatter(n, g, color="red")
        else:
            plt.scatter(n, g, color="blue")
    plt.title("Distribución de los grados de los nodos identificando hubs")
    plt.xlabel("Nodo")
    plt.ylabel("Grado")
    # Definir el nombre del archivo de la visualización
    global diccionario_resul
    archivo_grafico = f"analizarEstructura/distribucion_grados_hubs.png"
    diccionario_resul["distribucion_grados_hubs"] = archivo_grafico
    plt.savefig(archivo_grafico)
    plt.show()


def grafica_clustering(diccionario_clustering):
    # Crear listas para nodos y sus coeficientes de clustering
    nodos = list(diccionario_clustering.keys())
    clustering_coef = [
        diccionario_clustering[nodo] for nodo in nodos
    ]  # Directamente usar el valor
    # Crear el gráfico de dispersión
    plt.figure(figsize=(12, 6))
    plt.scatter(nodos, clustering_coef, alpha=0.6)
    # Títulos y etiquetas
    plt.title("Distribución de los coeficientes de clustering de los nodos")
    plt.xlabel("Nodo")
    plt.ylabel("Coeficiente de Clustering")
    # Definir el nombre del archivo de la visualización
    global diccionario_resul
    archivo_grafico = f"analizarEstructura/distribucion_clustering.png"
    diccionario_resul["distribucion_clustering"] = archivo_grafico
    plt.savefig(archivo_grafico)
    plt.show()


def grafica_clustering_con_hubs(diccionario_clustering):
    # Crear listas para nodos y sus coeficientes de clustering
    nodos = list(diccionario_clustering.keys())

    clustering_coef = [
        diccionario_clustering[nodo] for nodo in nodos
    ]  # Directamente usar el valor
    # Definir un umbral para identificar los hubs
    umbral_hub = float(
        input(
            "Introduce el umbral de coeficiente de clustering para identificar los hubs: "
        )
    )
    # Crear listas para colores y tamaños de los nodos
    colores = []
    for coef in clustering_coef:
        if coef >= umbral_hub:
            colores.append("red")  # Hubs se pintan de rojo
        else:
            colores.append("green")  # Nodos no hubs se pintan de verde
    # Crear el gráfico de dispersión
    plt.figure(figsize=(12, 6))
    plt.scatter(nodos, clustering_coef, color=colores, alpha=0.6)
    # Títulos y etiquetas
    plt.title("Distribución de los coeficientes de clustering de los nodos")
    plt.xlabel("Nodo")
    plt.ylabel("Coeficiente de Clustering")
    # Definir el nombre del archivo de la visualización
    global diccionario_resul
    archivo_grafico = f"analizarEstructura/distribucion_clustering_hubs.png"
    diccionario_resul["distribucion_clustering_hubs"] = archivo_grafico
    plt.savefig(archivo_grafico)
    plt.show()


def visualizar_red(grafo):
    # Crear un grafo vacío de NetworkX
    G = nx.Graph()

    # Añadir los nodos al grafo
    for nodo in grafo["nodos"]:
        G.add_node(nodo["id"], tipo=nodo["tipo"], atributos=nodo["atributos"])

    # Añadir las aristas al grafo
    for arista in grafo["aristas"]:
        nodos = list(arista["nodos"])  # Los nodos conectados por la arista
        G.add_edge(nodos[0], nodos[1], tipo=arista["tipo"])

    # Dibujar el grafo con etiquetas
    nx.draw(
        G, with_labels=True, node_color="lightblue", font_weight="bold", node_size=2000
    )
    global diccionario_resul
    archivo_grafico = f"analizarEstructura/visualizacion.png"
    diccionario_resul["visualizacion_grafo"] = archivo_grafico
    plt.savefig(archivo_grafico)
    plt.show()


def grafica_conjunta_grados_clustering(diccionario_grados, diccionario_clustering):
    # Extraer listas de grados y coeficientes de clustering
    nodos = list(diccionario_grados.keys())
    grados = list(diccionario_grados.values())

    clustering_coef = [
        diccionario_clustering[nodo] for nodo in nodos
    ]  # Directamente usar el valor
    # Crear el gráfico de dispersión
    plt.figure(figsize=(12, 6))
    plt.scatter(grados, clustering_coef, alpha=0.6)
    plt.title("Distribución conjunta de Grados y Coeficientes de Clustering")
    plt.xlabel("Grado")
    plt.ylabel("Coeficiente de Clustering")
    # Definir el nombre del archivo de la visualización
    global diccionario_resul
    archivo_grafico = f"analizarEstructura/cnj_grados_clustering.png"
    diccionario_resul["cnj_grados_clustering"] = archivo_grafico
    plt.savefig(archivo_grafico)
    plt.show()


def bfs(diccionario, nodo_inicial):
    visitados = set()  # Conjunto de nodos visitados
    distancias = {nodo_inicial: 0}  # Distancias desde el nodo inicial
    cola = [nodo_inicial]  # Cola para el BFS
    while cola:
        nodo = cola.pop(0)  # Sacar el primer nodo de la cola
        if nodo not in visitados:
            visitados.add(nodo)  # Marcar como visitado
            # Explorar los vecinos del nodo actual
            for vecino in diccionario[nodo]:
                if vecino not in distancias:
                    distancias[vecino] = distancias[nodo] + 1
                    cola.append(vecino)
    return distancias, visitados


def calcular_distancia_media(diccionario):
    nodos = list(diccionario.keys())  # Lista de todos los nodos
    suma_distancias = 0
    total_pares = 0
    visitados_global = set()  # Conjunto para nodos ya visitados
    for nodo in nodos:
        if nodo in visitados_global:
            continue
        # Ejecutar BFS desde el nodo actual
        distancias, visitados_local = bfs(diccionario, nodo)
        # Actualizar nodos visitados globalmente
        visitados_global.update(visitados_local)
        # Calcular suma de distancias y actualizar total de pares
        suma_distancias += sum(distancias.values())
        total_pares += len(distancias) - 1  # Excluir distancia al nodo inicial
    if total_pares > 0:
        distancia_media = suma_distancias / total_pares
    else:
        print("El grafo no tiene pares de nodos conectados.")
    return distancia_media


def calcular_diametro(diccionario):
    nodos = list(diccionario.keys())  # Lista de nodos
    max_distancia = 0  # Para almacenar la mayor distancia encontrada
    visitados_global = set()  # Nodos que ya hemos procesado
    for nodo in nodos:
        if nodo in visitados_global:
            continue  # Si ya procesamos este nodo, lo ignoramos
        # Ejecutar BFS desde este nodo
        distancias, visitados_local = bfs(diccionario, nodo)
        # Actualizar el conjunto de nodos visitados globalmente
        visitados_global.update(visitados_local)
        # Actualizar la distancia máxima (diámetro)
        max_distancia = max(max_distancia, max(distancias.values()))
    return max_distancia


def calcular_distribucion_distancias(dicc_grado):
    # Determinar el umbral para considerar un nodo como hub
    umbral_hub = int(
        input("Introduce el umbral de grado para considerar un nodo como hub: ")
    )
    # Identificar los hubs en el grafo
    hubs = [nodo for nodo, grado in dicc_grado.items() if grado >= umbral_hub]
    if not hubs:
        print("No se encontraron hubs con el umbral especificado.")
        return
    print(f"Hubs identificados: {hubs}")
    # Calcular distancias desde cada hub
    distancias_globales = []
    for hub in hubs:
        distancias, _ = bfs(diccionario, hub)
        distancias_globales.extend(distancias.values())
    # Llamar a la función para graficar el histograma
    graficar_histograma_distancias(distancias_globales)
    return distancias_globales


def graficar_histograma_distancias(
    distancias, titulo="Distribución de distancias desde los hubs"
):
    plt.figure(figsize=(12, 6))
    plt.hist(
        distancias, bins=range(1, max(distancias) + 2), edgecolor="black", alpha=0.7
    )
    plt.title(titulo)
    plt.xlabel("Distancia")
    plt.ylabel("Frecuencia")
    # Definir el nombre del archivo de la visualización
    global diccionario_resul
    archivo_grafico = f"analizarEstructura/distribucion_distancias.png"
    diccionario_resul["distribucion_distancias"] = archivo_grafico
    plt.savefig(archivo_grafico)
    plt.show()


def calcular_esperanza_grado(diccionario_grados):
    grados = list(diccionario_grados.values())
    esperanza = sum(grados) / len(grados)
    return esperanza


def calcular_probabilidad_enlace(nodos, aristas):
    if nodos <= 1:
        print("La probabilidad de enlace no está definida para grafos con 0 o 1 nodo.")
        return 0
    probabilidad = (2 * aristas) / (nodos * (nodos - 1))
    return probabilidad


def calcular_varianza_grado(diccionario_grados, esperanza):
    grados = list(diccionario_grados.values())
    varianza = sum((grado - esperanza) ** 2 for grado in grados) / len(grados)
    return varianza
