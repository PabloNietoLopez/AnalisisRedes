import json
import os
import requests
from bs4 import BeautifulSoup


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


# Función para obtener la información del usuario
def obtener_info_usuario(ruta_archivo):
    contenido_html = leer_html_local(ruta_archivo)
    if contenido_html:

        soup_usuario = BeautifulSoup(contenido_html, "html.parser")

        nombre_span = extraer_dato(
            soup_usuario, clase="actual_persona_name", etiqueta_a_buscar="span"
        )

        estado = extraer_dato(soup_usuario, clase="profile_private_info")
        if not estado:
            nacionalidad = extraer_dato(soup_usuario, "header_real_name ellipsis")
            if disponible(nacionalidad):
                # Divide el texto en partes utilizando el espacio en blanco como separador
                partes = nacionalidad.split()
                # Selecciona la parte que te interesa (la localidad)
                nacionalidad = " ".join(partes[1:])

            nivel_padre = extraer_dato(soup_usuario, "persona_name persona_level")
            nivel = nivel_padre.split()[1]

            descripcion = extraer_dato(soup_usuario, "profile_summary noexpand")

            if not descripcion:
                descripcion = extraer_dato(soup_usuario, "profile_summary")

            juego_favorito = extraer_dato_con_bucle(
                soup_usuario,
                "profile_customization_header",
                "showcase_item_detail_title",
            )

            # Extraer la actividad reciente (pueden ser varios juegos)
            actividad_reciente = extraer_dato_con_bucle(
                soup_usuario, "recent_game", "game_name"
            )
        else:
            nacionalidad = "PRIVADO"
            nivel = "PRIVADO"
            descripcion = "PRIVADO"
            juego_favorito = "PRIVADO"
            actividad_reciente = "PRIVADO"

        # Almacenar toda la información en un diccionario
        usuario_info = {
            "nombre": nombre_span,
            "nacionalidad": nacionalidad,
            "nivel": nivel,
            "descripcion": descripcion,
            "juego_favorito": juego_favorito,
            "actividad_reciente": actividad_reciente,
        }

        return usuario_info
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
        return None
    else:
        return elemento.text.strip() if elemento.text.strip() != "" else "No disponible"


def extraer_dato_con_bucle(soup, clase_padre, clase_a_buscar, etiqueta_a_buscar="div"):
    lista = []
    bucle = soup.find_all("div", class_=clase_padre)

    for i in bucle:
        dato = i.find(etiqueta_a_buscar, class_=clase_a_buscar)
        if dato:
            texto_dato = dato.text.strip()
            lista.append(texto_dato)

    if not lista:
        return "No disponible"
    else:
        return lista


def procesar_usuarios():
    # Ruta de la carpeta que contiene los archivos HTML
    carpeta_html = os.path.join(os.getcwd(), "scraping", "htmls", "html_usuarios")

    # Obtener la lista de archivos HTML en la carpeta
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]

    # Lista para almacenar la información procesada de los usuarios
    usuarios_info = []

    # Procesar cada archivo HTML
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")

        # Obtener información del usuario desde el archivo
        usuario_info = obtener_info_usuario(ruta_archivo)

        # Si se extrajo información válida, agregarla a la lista
        if usuario_info:
            usuarios_info.append(usuario_info)

    return usuarios_info


def main():
    carpeta_html = os.path.join(os.getcwd(), "..", "scraping", "htmls", "html_usuarios")
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    usuarios_info = []

    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        usuario_info = obtener_info_usuario(ruta_archivo)
        if usuario_info:
            usuarios_info.append(usuario_info)

    with open("usuarios_info.json", "w", encoding="utf-8") as json_file:
        json.dump(usuarios_info, json_file, ensure_ascii=False, indent=4)

    print(
        f"Se han guardado los datos de {len(usuarios_info)} usuarios en 'usuarios_info.json'."
    )


if __name__ == "__main__":
    main()
