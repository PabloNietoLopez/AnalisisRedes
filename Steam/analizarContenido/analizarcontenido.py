import os
import json
from datosprimitivos import obtener_datos_primitivos
from datosagregados import obtener_datos_agregados
from datosderivados import obtener_datos_derivados
from generar_informe import generar_informe_completo


def cargar_datos_completos(ruta_json):
    """
    Carga los datos completos de juegos y desarrolladores desde un archivo JSON.

    :param ruta_json: Ruta completa al archivo JSON.
    :return: Tupla con dos listas, juegos y desarrolladores.
    """
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    juegos = []
    desarrolladores = []
    eventos = []
    usuarios = []
    comentarios_total = []
    comentarios = []
    comunidades = []

    if "juegos" in datos:
        for juego in datos["juegos"]:
            juegos.append(
                {
                    "nombre": juego.get("nombre", ""),
                    "precio": juego.get("precio", "free to play"),
                    "generos": juego.get("generos", []),
                    "reseñas": juego.get("reseñas", ""),
                    "fecha": juego.get("fecha", ""),
                    "requisitos_minimos": juego.get("requisitos_minimos", ""),
                    "requisitos_recomendados": juego.get("requisitos_recomendados", ""),
                    "desarrollador": juego.get(
                        "desarrollador", ""
                    ),  # Agregamos el campo 'desarrollador'
                }
            )

    if "desarrolladores" in datos:
        for desarrollador in datos["desarrolladores"]:
            desarrolladores.append(
                {
                    "nombre": desarrollador.get("nombre", ""),
                    "seguidores": desarrollador.get("seguidores", "0"),
                    "juegos_creados": desarrollador.get("juegos_creados", []),
                }
            )

    if "usuarios" in datos:
        for usuario in datos["usuarios"]:
            usuarios.append(
                {
                    "nombre": usuario.get("nombre", ""),
                    "nacionalidad": usuario.get("nacionalidad", ""),
                    "nivel": usuario.get("nivel", 0),
                    "descripcion": usuario.get("descripcion", ""),
                    "juego_favorito": usuario.get("juego_favorito", ""),
                    "actividad_reciente": usuario.get("actividad_reciente", []),
                }
            )

    if "comentarios" in datos:
        for juego in datos["comentarios"]:
            for comentario in juego:
                comentarios.append(
                    {
                        "juego_que_comenta": comentario.get("juego_que_comenta", ""),
                        "nombre": comentario.get("nombre", ""),
                        "valoracion": comentario.get("valoracion", 0),
                        "fecha": comentario.get("fecha", ""),
                        "descripcion": comentario.get("descripcion", ""),
                        "horas_jugadas": comentario.get("horas_jugadas", 0),
                        "util": comentario.get("util_personas", 0),
                    }
                )
            comentarios_total.append(comentarios)
            comentarios = []

    if "eventos" in datos:
        for evento in datos["eventos"]:
            eventos.append(
                {
                    "nombre": evento.get("nombre", ""),
                    "descripcion": evento.get("descripcion", ""),
                    "fecha": evento.get("fecha", ""),
                }
            )

    if "comunidades" in datos:
        for comunidad in datos["comunidades"]:
            comunidades.append(
                {
                    "nombre_juego": comunidad.get("nombre", ""),
                    "lema": comunidad.get("lema", ""),
                    "descripcion": comunidad.get("descripcion", ""),
                    "creaciones_populares": comunidad.get("creaciones_populares", []),
                }
            )

    return juegos, desarrolladores, usuarios, comentarios_total, eventos, comunidades


import os


def main():
    # Crear la carpeta "imagenes" si no existe
    carpeta_imagenes = os.path.join(os.getcwd(), "analizarContenido\imagenes")
    os.makedirs(carpeta_imagenes, exist_ok=True)

    # Definir la ruta del archivo JSON
    carpeta_json = os.path.join(os.getcwd(), "analizarHTML")
    ruta_json = os.path.join(carpeta_json, "dataset.json")

    # Cargar los datos del archivo JSON (juegos y desarrolladores)
    juegos, desarrolladores, usuarios, comentarios, eventos, comunidades = (
        cargar_datos_completos(ruta_json)
    )

    # Obtener los datos para análisis
    obtener_datos_primitivos(
        juegos, desarrolladores, usuarios, comentarios, eventos, comunidades
    )
    obtener_datos_agregados(
        juegos, desarrolladores, usuarios, comentarios, eventos, comunidades
    )
    obtener_datos_derivados(
        juegos, desarrolladores, usuarios, comentarios, eventos, comunidades
    )

    # Generar informe completo
    generar_informe_completo()


# Punto de entrada principal
if __name__ == "__main__":
    main()
