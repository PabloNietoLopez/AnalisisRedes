from bs4 import BeautifulSoup
import os


# Función para obtener la información del juego desde un archivo HTML
def obtener_info_juego_desde_html(ruta_archivo):
    try:
        # Leer el contenido del archivo HTML
        with open(ruta_archivo, "r", encoding="utf-8") as file:
            contenido_html = file.read()

        # Analizar el HTML con BeautifulSoup
        soup_juego = BeautifulSoup(contenido_html, "html.parser")

        # Extraer datos del juego
        nombre = extraer_dato(soup_juego, "apphub_AppName")
        precio = extraer_dato(soup_juego, "game_purchase_price")
        descripcion = extraer_dato(soup_juego, "game_description_snippet")
        reseñas = extraer_reseñas(soup_juego)
        desarrollador = extraer_dato(
            soup_juego, "summary column", "developers_list", True
        )
        fecha = extraer_dato(soup_juego, "date")
        requisitos_min = extraer_dato(soup_juego, "game_area_sys_req_leftCol")
        requisitos_recom = extraer_dato(soup_juego, "game_area_sys_req_rightCol")
        # Buscar el elemento <span> que contiene los géneros
        span_elemento = soup_juego.find(
            "span", {"data-panel": '{"flow-children":"row"}'}
        )
        generos = []
        if span_elemento:
            # Buscar todos los enlaces <a> dentro del <span>
            enlaces = span_elemento.find_all("a")
            # Extraer el texto de cada enlace
            generos = [enlace.text.strip() for enlace in enlaces]
        # Extraer datos adicionales (nombres de usuarios, comentarios, eventos)
        nombres_usuarios = extraer_dato_con_bucle(
            soup_juego, "review_box", "persona_name"
        )
        comentarios = extraer_dato_con_bucle(soup_juego, "review_box", "content")
        eventos = extraer_dato_con_bucle(
            soup_juego, "_22jEpNTfml-w_aRJV-fKDm", "_2jc1DpJ_WzFtigRh5qDWce"
        )

        # Consolidar la información en un diccionario
        juego_info = {
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion,
            "reseñas": reseñas,
            "desarrollador": desarrollador,
            "fecha": fecha,
            "requisitos_minimos": requisitos_min,
            "requisitos_recomendados": requisitos_recom,
            "generos": generos,
            "nombres_usuarios_que_comentan": nombres_usuarios,
            "comentarios": comentarios,
            "eventos": eventos,
        }

        return juego_info

    except Exception as e:
        print(f"Error al procesar el archivo {ruta_archivo}: {e}")
        return None


# Función para extraer un dato del HTML
def extraer_dato(soup, clase=None, id=None, buscar_enlace=False):
    try:
        if clase and id:
            elemento = soup.find("div", class_=clase, id=id)
        elif clase:
            elemento = soup.find("div", class_=clase)
        elif id:
            elemento = soup.find("div", id=id)
        else:
            return "No disponible"

        if elemento and buscar_enlace:
            enlace = elemento.find("a")
            return enlace.text.strip() if enlace else "No disponible"

        return elemento.text.strip() if elemento else "No disponible"

    except Exception as e:
        print(f"Error al extraer dato: {e}")
        return "No disponible"


# Función para extraer datos con bucles (listas)
def extraer_dato_con_bucle(soup, clase_padre, clase_a_buscar, etiqueta_a_buscar="div"):
    try:
        lista = []
        elementos_padres = soup.find_all("div", class_=clase_padre)

        for elemento_padre in elementos_padres:
            dato = elemento_padre.find(etiqueta_a_buscar, class_=clase_a_buscar)
            if dato:
                lista.append(dato.text.strip())

        return lista

    except Exception as e:
        print(f"Error al extraer datos con bucle: {e}")
        return []


# Función para extraer reseñas
def extraer_reseñas(soup_juego):
    try:
        reseña_positive = soup_juego.find("span", class_="game_review_summary positive")
        reseña_negative = soup_juego.find("span", class_="game_review_summary negative")
        reseña_not_enough = soup_juego.find(
            "span", class_="game_review_summary not_enough_reviews"
        )
        reseña_mixed = soup_juego.find("span", class_="game_review_summary mixed")

        if reseña_positive:
            return reseña_positive.text.strip()
        elif reseña_negative:
            return reseña_negative.text.strip()
        elif reseña_not_enough:
            return reseña_not_enough.text.strip()
        elif reseña_mixed:
            return reseña_mixed.text.strip()
        else:
            return "No disponible"

    except Exception as e:
        print(f"Error al extraer reseñas: {e}")
        return "No disponible"


def procesar_juegos():

    # Usar una ruta relativa para acceder al directorio html_juegos
    carpeta_html = os.path.join(
        os.getcwd(), "scraping", "htmls", "html_juegos"
    )  # Carpeta donde están los archivos HTML
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    juegos_info = []

    # Procesar cada archivo HTML
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        juego_info = obtener_info_juego_desde_html(ruta_archivo)

        if juego_info:
            juegos_info.append(juego_info)

    # Retornar la lista con la información de los juegos
    return juegos_info


# PARA PROBAR SOLO LA EJECUCIÓN DE ESTE SCRIPT
def main():
    # Usar una ruta relativa para acceder al directorio html_juegos
    carpeta_html = os.path.join(
        os.getcwd(), "..", "scraping", "htmls", "html_juegos"
    )  # Carpeta donde están los archivos HTML
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    juegos_info = []

    # Procesar cada archivo HTML
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        juego_info = obtener_info_juego_desde_html(ruta_archivo)

        if juego_info:
            juegos_info.append(juego_info)

    # Guardar los datos en un archivo JSON
    with open("juegos_info.json", "w", encoding="utf-8") as json_file:
        json.dump(juegos_info, json_file, ensure_ascii=False, indent=4)

    print(
        f"Se han guardado los datos de {len(juegos_info)} juegos en 'juegos_info.json'."
    )


if __name__ == "__main__":
    main()
