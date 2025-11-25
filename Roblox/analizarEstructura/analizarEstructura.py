import analizarEstructura.inicializardiccionarios as inicializardiccionarios
import analizarEstructura.datosgrafo as datosgrafo
import analizarEstructura.gradoyclustering as gradoyclustering
import analizarEstructura.distancias as distancias
import analizarEstructura.probabilidad as probabilidad


def analizar(edgelist_df, nombre_red="Roblox"):
    """
    Función que realiza el análisis de la estructura del grafo formado por Roblox.
    Parámetros:
        edgelist_df: DataFrame que contiene la lista de aristas del grafo.
        nombre_red: Nombre de la red a analizar (Roblox).
    """
    # Convertir el DataFrame a lista de tuplas: cada fila es (Nodo1, Nodo2)
    edges_list = list(edgelist_df.itertuples(index=False, name=None))

    # Inicializar los diccionarios globales
    diccionario, diccionario_grados, diccionario_clustering, diccionario_resul = (
        inicializardiccionarios.inicializar(edges_list, nombre_red)
    )

    # Solicitar los umbrales de grado y clustering
    grado_hub = int(input("Introduce el umbral de grado para identificar los hubs: "))
    clustering_hub = float(
        input(
            "Introduce el umbral de coeficiente de clustering para identificar los hubs: "
        )
    )

    # Cálculos
    datosgrafo.calcular(
        edges_list, diccionario, diccionario_resul, grado_hub
    )  # Número de nodos y aristas; visualización de la red
    gradoyclustering.calcular(
        diccionario_grados,
        diccionario_clustering,
        diccionario_resul,
        grado_hub,
        clustering_hub,
    )  # Distribuciones de grados y coeficientes de clustering
    distancias.calcular(
        diccionario, diccionario_grados, diccionario_resul, grado_hub
    )  # Distancia media y diámetro de la red
    probabilidad.calcular(
        diccionario_grados, diccionario_resul
    )  # Probabilidad de enlace, esperanza y varianza de grado

    # Retornar el diccionario de resultados
    return diccionario_resul
