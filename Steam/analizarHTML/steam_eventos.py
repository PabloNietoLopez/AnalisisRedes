import os
import re
from bs4 import BeautifulSoup


# Función para obtener la información del evento desde un archivo HTML
def obtener_info_evento(archivo_html):
    try:
        # Leer el archivo HTML
        with open(archivo_html, "r", encoding="utf-8") as file:
            contenido_html = file.read()

        # Analizar el HTML con BeautifulSoup
        soup_evento = BeautifulSoup(contenido_html, "html.parser")

        # Extraer los datos del evento

        titulo_completo = soup_evento.title.text.strip()
        nombre_evento = extraer_titulo_con_guiones(titulo_completo)

        # Buscar la etiqueta <meta> con el atributo name='Description'
        descripcion_meta = soup_evento.find("meta", attrs={"name": "Description"})

        # Extraer el contenido del atributo 'content'
        if descripcion_meta and "content" in descripcion_meta.attrs:
            descripcion = descripcion_meta.attrs["content"].strip()
        else:
            print("No se encontró la descripción.")

        nombre_juego = extraer_primera_parte(titulo_completo)

        evento_info = {
            "titulo": nombre_evento,
            "descripcion": descripcion,
            "juego": nombre_juego,
        }

        return evento_info

    except Exception as e:
        print(f"Error al procesar el archivo {archivo_html}: {e}")
        return None


def extraer_titulo_con_guiones(titulo):
    # Usamos una expresión regular para extraer lo que está entre los guiones
    match = re.search(r" - (.*?) - ", titulo)
    if match:
        return match.group(
            1
        ).strip()  # Devuelve el texto entre los guiones, eliminando los espacios
    return None  # Si no se encuentra el patrón, devuelve None


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


def extraer_primera_parte(titulo):
    # Usamos una expresión regular para extraer lo que está antes del primer guion
    match = re.match(r"^(.*?) -", titulo)
    if match:
        return match.group(
            1
        ).strip()  # Devuelve el texto antes del primer guion, eliminando los espacios
    return None  # Si no se encuentra el patrón, devuelve None


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


def procesar_eventos():
    # Carpeta donde están los archivos HTML de los eventos
    carpeta_html = os.path.join(os.getcwd(), "scraping", "htmls", "html_eventos")
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    eventos_info = []

    # Procesar cada archivo HTML
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        evento_info = obtener_info_evento(ruta_archivo)

        if evento_info:
            eventos_info.append(evento_info)

    return eventos_info


# PARA PROBAR SOLO LA EJECUCIÓN DE ESTE SCRIPT
def main():
    # Carpeta donde están los archivos HTML de los eventos
    carpeta_html = os.path.join(os.getcwd(), "..", "scraping", "htmls", "html_eventos")
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    eventos_info = []

    # Procesar cada archivo HTML
    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        evento_info = obtener_info_evento(ruta_archivo)

        if evento_info:
            eventos_info.append(evento_info)

    # Guardar los datos en un archivo JSON
    with open("eventos_info.json", "w", encoding="utf-8") as json_file:
        json.dump(eventos_info, json_file, ensure_ascii=False, indent=4)

    print(
        f"Se han guardado los datos de {len(eventos_info)} eventos en 'eventos_info.json'."
    )


if __name__ == "__main__":
    main()
