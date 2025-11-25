import os
import requests
from bs4 import BeautifulSoup
import json


def disponible(elemento):

    if elemento == "No disponible":
        return False
    else:
        return True


# Función para leer archivos HTML locales
def leer_html_local(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error al leer el archivo {ruta_archivo}: {e}")
        return None


def extraer_dato(
    soup, clase=None, id=None, buscar_enlace=False, etiqueta_a_buscar="div"
):

    if clase and id:
        elemento = soup.find(etiqueta_a_buscar, class_=clase, id=id)
    elif clase:
        elemento = soup.find(etiqueta_a_buscar, class_=clase)
    elif id:
        elemento = soup.find(etiqueta_a_buscar, id=id)
    else:
        return "No disponible"

    # Si se encontró el elemento y se quiere buscar un enlace dentro de él
    if elemento and buscar_enlace:
        enlace = elemento.find("a")
        return enlace.text.strip() if enlace else "No disponible"

    if not elemento:
        return "No disponible"
    else:
        return elemento.text.strip() if elemento.text.strip() != "" else "No disponible"


def obtener_nombre_archivo(ruta_html):
    # Obtener el nombre del archivo con extensión
    nombre_con_extension = os.path.basename(ruta_html)
    # Eliminar la extensión .html
    nombre_sin_extension = os.path.splitext(nombre_con_extension)[0]
    return nombre_sin_extension


def obtener_info_coment(ruta_html):

    # Usamos requests solo para obtener la estructura estática de la página
    contenido_html = leer_html_local(ruta_html)
    # Lista para almacenar los datos de cada comentario
    comentarios_info = []

    if contenido_html:
        soup = BeautifulSoup(contenido_html, "html.parser")

        # Encontrar todos los bloques de comentarios
        comentarios = soup.find_all("div", class_="review_box")

        # Extraer los datos específicos para cada comentario
        contador = 0

        for comentario in comentarios:

            if contador >= 50:  # Limitar a los primeros 50 comentarios
                break
            nombre_juego = obtener_nombre_archivo(ruta_html)
            # Extraer cada campo usando la estructura HTML
            usuario = extraer_dato(comentario, clase="persona_name")
            valoracion = obtener_texto_o_default(
                comentario, "title ellipsis", "Valoración no disponible"
            )
            fecha = extraer_dato(comentario, clase="postedDate")
            descripcion = extraer_dato(comentario, clase="content")
            horas_jugadas = extraer_dato(comentario, clase="hours ellipsis")
            util_personas = extraer_dato(comentario, clase="vote_info")

            # Crear diccionario para el comentario actual
            comment_info = {
                "juego_que_comenta": nombre_juego,
                "nombre": usuario,
                "valoracion": valoracion,
                "fecha": fecha,
                "descripcion": descripcion,
                "horas_jugadas": horas_jugadas,
                "util_personas": util_personas,
            }

            # Agregar el diccionario a la lista de comentarios
            comentarios_info.append(comment_info)
            contador = contador + 1

    return comentarios_info if comentarios_info else None


def guardar_comentarios_json(comentarios, filename="comentarios.json"):
    # Si hay comentarios, guardarlos en un archivo JSON
    if comentarios:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(comentarios, file, ensure_ascii=False, indent=4)
    else:
        print("No hay comentarios disponibles.")


def obtener_texto_o_default(elemento, clase, default):
    encontrado = elemento.find("div", class_=clase)
    return encontrado.get_text(strip=True) if encontrado else default


def procesar_comentarios():
    # Ruta de la carpeta que contiene los archivos HTML de comentarios
    carpeta_html = os.path.join(os.getcwd(), "scraping", "htmls", "html_comentarios")

    # Obtener la lista de archivos HTML en la carpeta
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]

    # Lista para almacenar la información procesada de los comentarios
    comentarios_totales = []

    # Procesar cada archivo HTML
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")

        # Obtener información del comentario desde el archivo
        comentario_info = obtener_info_coment(ruta_archivo)

        # Si se extrajo información válida, agregarla a la lista
        if comentario_info:
            comentarios_totales.append(comentario_info)

    return comentarios_totales


def main():
    # URL de ejemplo del juego en Steam
    carpeta_html = os.path.join(
        os.getcwd(), "..", "scraping", "htmls", "html_comentarios"
    )
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    comentarios_totales = []
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        comentario_info = obtener_info_coment(ruta_archivo)

        if comentario_info:
            comentarios_totales.append(comentario_info)

    guardar_comentarios_json(comentarios_totales)


if __name__ == "__main__":
    main()
