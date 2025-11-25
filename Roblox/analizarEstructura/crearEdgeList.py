import os
import json
from itertools import combinations
import pandas as pd


def obtener_edgelist():
    # Ruta de la carpeta que contiene todos los archivos JSON
    carpeta_datos = "dataSets"

    # Inicializar la lista para almacenar todas las aristas
    edgelist = []

    # Iterar sobre todos los archivos en la carpeta 'dataSets'
    for archivo in os.listdir(carpeta_datos):
        if archivo.endswith(".json"):
            # Construir la ruta completa del archivo
            file_path = os.path.join(carpeta_datos, archivo)

            # Leer el archivo JSON
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Procesar cada experiencia del JSON actual
            for experiencia in data:
                titulo_juego = experiencia.get("Titulo", "Sin Titulo")
                grupo_creador = experiencia.get("Creador", {}).get(
                    "NombreGrupo", "Sin Grupo"
                )
                miembros_grupo = experiencia.get("Creador", {}).get("Miembros", [])

                # 1. Conectar miembros del mismo grupo entre sí
                nombres_miembros = [
                    miembro.get("Nombre", "Sin Nombre") for miembro in miembros_grupo
                ]
                edgelist.extend(combinations(nombres_miembros, 2))

                # 2. Conectar cada miembro del grupo a los juegos que recomienda
                for miembro in miembros_grupo:
                    nombre_jugador = miembro.get("Nombre", "Sin Nombre")
                    juegos_favoritos = miembro.get("JuegosFavoritos", [])
                    for juego in juegos_favoritos:
                        edgelist.append((nombre_jugador, juego))

                # 3. Conectar el grupo creador al juego principal
                edgelist.append((grupo_creador, titulo_juego))

    # Crear un DataFrame con la lista de aristas
    edgelist_df = pd.DataFrame(edgelist, columns=["Nodo 1", "Nodo 2"])

    return edgelist_df
