from bs4 import BeautifulSoup
import os


# Función para obtener la información del desarrollador desde un archivo HTML
def obtener_info_desarrollador(archivo_html):

    try:
        # Leer el archivo HTML del desarrollador
        with open(archivo_html, "r", encoding="utf-8") as file:
            contenido_html = file.read()

        # Analizar el HTML con BeautifulSoup
        soup_desarrollador = BeautifulSoup(contenido_html, "html.parser")

        if "search" in archivo_html:
            # Si es una página de búsqueda, extraer el nombre del desarrollador del div con clase 'searchtag tag_dynamic'
            nombre_desarrollador_div = soup_desarrollador.find(
                "div", class_="searchtag tag_dynamic"
            )

            if nombre_desarrollador_div:
                # Extraer el texto del <span class="label">
                nombre_desarrollador_span = nombre_desarrollador_div.find(
                    "span", class_="label"
                )

                if nombre_desarrollador_span and nombre_desarrollador_span.text.strip():
                    # Si hay un texto, limpiamos y lo retornamos
                    nombre_desarrollador = nombre_desarrollador_span.text.replace(
                        "Desarrollador: ", ""
                    ).strip()
                else:
                    print(
                        "No se encontró el nombre del desarrollador dentro del <span class='label'>"
                    )

            seguidores = "No disponible"
            juegos_creados = extraer_dato_con_bucle(
                soup_desarrollador, "col search_name ellipsis", "title", "span"
            )

        else:
            # Extraer el nombre del desarrollador
            nombre_desarrollador = (
                soup_desarrollador.find("div", id="header_curator_details")
                .find("a")
                .text.strip()
            )

            # Extraer el número de seguidores del desarrollador
            seguidores = extraer_dato(soup_desarrollador, "num_followers")

            # Extraer los juegos creados por el desarrollador
            juegos_creados = extraer_dato_con_bucle(
                soup_desarrollador, "recommendation", "color_created", "span"
            )

        # Almacenar toda la información en un diccionario
        desarrollador_info = {
            "nombre": nombre_desarrollador,
            "seguidores": seguidores,
            "juegos_creados": juegos_creados,
        }

        return desarrollador_info

    except Exception as e:
        print(f"Error al procesar el archivo {archivo_html}: {e}")
        return None


# Función para extraer un dato específico del HTML
def extraer_dato(soup, clase=None, id=None, buscar_enlace=False):

    if clase and id:
        elemento = soup.find("div", class_=clase, id=id)
    elif clase:
        elemento = soup.find("div", class_=clase)
    elif id:
        elemento = soup.find("div", id=id)
    else:
        return "No disponible"

    # Si se encontró el elemento y se quiere buscar un enlace dentro de él
    if elemento and buscar_enlace:
        enlace = elemento.find("a")
        return enlace.text.strip() if enlace else "No disponible"

    return elemento.text.strip() if elemento else "No disponible"


# Función para extraer datos con bucles (listas)
def extraer_dato_con_bucle(soup, clase_padre, clase_a_buscar, etiqueta_a_buscar="div"):
    lista = []

    # Buscar todos los elementos con la clase padre
    bucle = soup.find_all("div", class_=clase_padre)

    for i in bucle:
        # Extraer el dato de la etiqueta especificada (por defecto 'div', pero puede ser 'span')
        dato = i.find(etiqueta_a_buscar, class_=clase_a_buscar)
        if dato:
            texto_dato = dato.text.strip()
            lista.append(texto_dato)

    return lista


def procesar_desarrolladores():
    # Carpeta donde están los archivos HTML de los desarrolladores
    carpeta_html = os.path.join(
        os.getcwd(), "scraping", "htmls", "html_desarrolladores"
    )
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    desarrolladores_info = []

    # Procesar cada archivo HTML
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        desarrollador_info = obtener_info_desarrollador(ruta_archivo)

        if desarrollador_info:
            desarrolladores_info.append(desarrollador_info)

    return desarrolladores_info


# PARA PROBAR SOLO LA EJECUCIÓN DE ESTE SCRIPT
def main():
    # Carpeta donde están los archivos HTML de los desarrolladores
    carpeta_html = os.path.join(
        os.getcwd(), "..", "scraping", "htmls", "html_desarrolladores"
    )
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    desarrolladores_info = []

    # Procesar cada archivo HTML
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        desarrollador_info = obtener_info_desarrollador(ruta_archivo)

        if desarrollador_info:
            desarrolladores_info.append(desarrollador_info)

    # Guardar los datos en un archivo JSON
    with open("desarrolladores_info.json", "w", encoding="utf-8") as json_file:
        json.dump(desarrolladores_info, json_file, ensure_ascii=False, indent=4)

    print(
        f"Se han guardado los datos de {len(desarrolladores_info)} desarrolladores en 'desarrolladores_info.json'."
    )


if __name__ == "__main__":
    main()
