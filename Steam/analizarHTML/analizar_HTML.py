from steam_juegos import procesar_juegos
from steam_eventos import procesar_eventos
from steam_desarrolladores import procesar_desarrolladores
from steam_usuarios import procesar_usuarios
from steam_comentarios import procesar_comentarios
from steam_comunidades import procesar_comunidades
import json


def main():
    # Procesar cada conjunto de datos
    lista_juegos = procesar_juegos()
    lista_eventos = procesar_eventos()
    lista_desarrolladores = procesar_desarrolladores()
    lista_usuarios = procesar_usuarios()
    lista_comentarios = procesar_comentarios()
    lista_comunidades = procesar_comunidades()

    # Combinar las listas en un diccionario
    dataset = {
        "juegos": lista_juegos,
        "eventos": lista_eventos,
        "desarrolladores": lista_desarrolladores,
        "usuarios": lista_usuarios,
        "comentarios": lista_comentarios,
        "comunidades": lista_comunidades,
    }

    # Guardar el dataset en un archivo JSON
    with open("analizarHTML\dataset.json", "w", encoding="utf-8") as json_file:
        json.dump(dataset, json_file, ensure_ascii=False, indent=4)

    print(f"El dataset se ha guardado correctamente en 'dataset.json'.")


if __name__ == "__main__":
    main()
