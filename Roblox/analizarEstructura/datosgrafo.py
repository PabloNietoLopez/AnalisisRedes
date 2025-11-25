import matplotlib.pyplot as plt
import networkx as nx
import random
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagenes = os.path.join(ruta_base, "Imagenes")
os.makedirs(ruta_imagenes, exist_ok=True)


def calcular(edges, diccionario, diccionario_resul, grado_hub):
    """
    Calcula:
    - Número de nodos y aristas.
    - Visualización de la red.

    Parámetros:
        edges (list): Lista de tuplas que representan las aristas.
        diccionario (dict): Diccionario de nodos y sus vecinos.
        diccionario_resul (dict): Diccionario donde guardaremos los resultados.
        grado_hub (int): El valor umbral de grado para los hubs.
    """
    nodos, aristas = nodos_aristas(edges, diccionario, diccionario_resul)
    print(f"La red tiene {nodos} nodos y {aristas} aristas.")

    visualizar_red(diccionario, diccionario_resul, grado_hub)


def nodos_aristas(edges, diccionario, diccionario_resul):
    """
    Calculo del número de nodos y aristas

    Parámetros:
        edges (list): Lista de tuplas que representan las aristas.
        diccionario (dict): Diccionario de nodos y sus vecinos.
        diccionario_resul (dict): Diccionario donde guardaremos los resultados.
    """
    nodos = len(diccionario)
    aristas = len(edges)
    diccionario_resul["num_nodos"] = nodos
    diccionario_resul["num_aristas"] = aristas
    return nodos, aristas


def visualizar_red(diccionario, diccionario_resul, hub_threshold, tamano_muestra=100):
    """
    Crea la imagen del grafo con la visualización de los nodos y aristas. Representa los hubs con un color rojo.

    Parámetros:
        diccionario (dict): Diccionario de nodos y sus vecinos.
        diccionario_resul (dict): Diccionario donde guardaremos los resultados.
        hub_threshold (int): Umbral de grado para identificar los hubs.
        tamano_muestra (int): Tamaño de la muestra/número de nodos para la visualización.
    """
    total_nodos = len(diccionario)
    if tamano_muestra > total_nodos:
        tamano_muestra = total_nodos
    G_completo = nx.from_dict_of_lists(diccionario)
    nodo_inicial = random.choice(list(diccionario.keys()))
    nodos_bfs = list(nx.bfs_tree(G_completo, source=nodo_inicial).nodes)
    if len(nodos_bfs) > tamano_muestra:
        nodos_muestra = nodos_bfs[:tamano_muestra]
    else:
        nodos_muestra = nodos_bfs
    G_muestra = G_completo.subgraph(nodos_muestra)
    node_degrees = dict(G_muestra.degree())
    node_colors = [
        "red" if node_degrees[node] >= hub_threshold else "blue"
        for node in G_muestra.nodes()
    ]
    node_sizes = [
        300 if node_degrees[node] >= hub_threshold else 100
        for node in G_muestra.nodes()
    ]
    plt.figure(figsize=(10, 8))
    nx.draw(
        G_muestra,
        with_labels=False,
        node_color=node_colors,
        node_size=node_sizes,
        font_weight="bold",
        edge_color="black",
        width=0.5,
    )
    plt.title(
        f"Visualización de Subgrafo Conexo con BFS (Muestra de {len(nodos_muestra)} nodos)"
    )
    nombre_red = diccionario_resul.get("nombre_red", "red_sin_nombre")
    grafica_path = os.path.join(ruta_imagenes, f"visualizacion_grafo_{nombre_red}.png")
    diccionario_resul["visualizacion_grafo"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()
