import os
import json


def crear_grafo(ruta_json):
    # Cargar el archivo JSON
    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
            print("Archivo cargado con éxito")
    except FileNotFoundError:
        print(f"El archivo 'dataset.json' no se encuentra en la ruta especificada.")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON.")
        return None

    # Diccionario de nodos y aristas
    grafo = {"nodos": [], "aristas": []}

    # Guardamos los nombres de los nodos de cada tipo para comprobar existencia
    nombres_juegos = set()
    nombres_desarrolladores = set()
    nombres_usuarios = set()
    nombres_comunidades = set()
    nombres_eventos = set()

    # Procesar nodos de juegos
    for juego in data["juegos"]:
        grafo["nodos"].append(
            {
                "id": juego["nombre"],
                "tipo": "juego",
                "atributos": {
                    "precio": juego.get("precio"),
                    "descripcion": juego.get("descripcion"),
                    "reseñas": juego.get("reseñas"),
                    "desarrollador": juego.get("desarrollador"),
                    "fecha": juego.get("fecha"),
                    "generos": juego.get("generos"),
                },
            }
        )
        nombres_juegos.add(juego["nombre"])

    # Procesar nodos de desarrolladores
    for desarrollador in data["desarrolladores"]:
        grafo["nodos"].append(
            {
                "id": desarrollador["nombre"],
                "tipo": "desarrollador",
                "atributos": {
                    "seguidores": desarrollador.get("seguidores"),
                    "juegos_creados": desarrollador.get("juegos_creados"),
                },
            }
        )
        nombres_desarrolladores.add(desarrollador["nombre"])

    # Procesar nodos de usuarios
    for usuario in data["usuarios"]:
        grafo["nodos"].append(
            {
                "id": usuario["nombre"],
                "tipo": "usuario",
                "atributos": {
                    "nacionalidad": usuario.get("nacionalidad"),
                    "nivel": usuario.get("nivel"),
                    "actividad_reciente": usuario.get("actividad_reciente"),
                    "juego_favorito": usuario.get("juego_favorito"),
                },
            }
        )
        nombres_usuarios.add(usuario["nombre"])

    # Procesar nodos de eventos
    for evento in data["eventos"]:
        grafo["nodos"].append(
            {
                "id": evento["titulo"],
                "tipo": "evento",
                "atributos": {
                    "descripcion": evento.get("descripcion"),
                    "juego": evento.get("juego"),
                },
            }
        )
        nombres_eventos.add(evento["titulo"])

    # Procesar nodos de juegos
    for comunidad in data["comunidades"]:
        grafo["nodos"].append(
            {
                "id": "Comunidad " + comunidad["nombre"],
                "tipo": "comunidad",
                "atributos": {
                    "descripcion": comunidad.get("descripcion"),
                    "lema": comunidad.get("reseñas"),
                    "creaciones_mas_populares": comunidad.get(
                        "creaciones_mas_populares"
                    ),
                },
            }
        )
        nombres_comunidades.add(comunidad["nombre"])

    # Crear aristas bidireccionales entre nodos existentes

    # Aristas entre juego y desarrollador
    for juego in data["juegos"]:
        if juego["desarrollador"] in nombres_desarrolladores:
            grafo["aristas"].append(
                {
                    "nodos": {juego["nombre"], juego["desarrollador"]},
                    "tipo": "creado_por",
                }
            )

    # Aristas entre juego y comunidad
    for comunidad in data["comunidades"]:
        for juego in data["juegos"]:
            if juego["nombre"] == comunidad["nombre"]:
                grafo["aristas"].append(
                    {
                        "nodos": {juego["nombre"], "Comunidad " + comunidad["nombre"]},
                        "tipo": "comunidad de",
                    }
                )

    # Aristas entre juego y usuarios
    for juego in data["juegos"]:
        for usuario in juego.get("nombres_usuarios_que_comentan", []):
            if usuario in nombres_usuarios:
                grafo["aristas"].append(
                    {"nodos": {juego["nombre"], usuario}, "tipo": "comentado_por"}
                )

    # Aristas entre juego y eventos
    for juego in data["juegos"]:
        for evento in juego.get("eventos", []):
            if evento in nombres_eventos:
                grafo["aristas"].append(
                    {"nodos": {juego["nombre"], evento}, "tipo": "evento_de"}
                )

    return grafo


def crear_diccionario(grafo):
    diccionario_ady = {}

    # Inicializar diccionario de adyacencia
    for nodo in grafo["nodos"]:
        diccionario_ady[nodo["id"]] = set()

    # Crear aristas bidireccionales
    for arista in grafo["aristas"]:

        nodo1, nodo2 = list(arista["nodos"])
        diccionario_ady[nodo1].add(nodo2)
        diccionario_ady[nodo2].add(nodo1)

    return diccionario_ady


def crea_diccionario_grado_nodos(diccionario_ady):
    dicc_grado = {}

    # Calcula el grado de cada nodo
    for nodo, adys in diccionario_ady.items():
        dicc_grado[nodo] = len(adys)

    return dicc_grado


def crea_diccionario_clustering(diccionario_ady):
    diccionario_clust = {}

    # Calcula el coeficiente de clustering para cada nodo
    for nodo, adys in diccionario_ady.items():
        grado = len(adys)  # Grado del nodo
        if grado < 2:
            # Si el grado es menor que 2, el coeficiente de clustering es 0
            coeficiente_clustering = 0
        else:

            aristas_entre_vecinos = 0
            # Compara cada par de vecinos
            for vecino1 in adys:
                for vecino2 in adys:
                    if vecino1 != vecino2 and vecino2 in diccionario_ady.get(
                        vecino1, []
                    ):
                        aristas_entre_vecinos += 1

            # Fórmula del coeficiente de clustering
            coeficiente_clustering = (2 * aristas_entre_vecinos) / (grado * (grado - 1))
        diccionario_clust[nodo] = coeficiente_clustering

    return diccionario_clust
