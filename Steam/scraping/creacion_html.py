import os
import json


def comprobar_existencia_archivos(nombre_carpeta):
    # Ruta base general para todas las carpetas HTML
    carpeta_base = "scraping\htmls"
    carpeta_html = os.path.join(carpeta_base, nombre_carpeta)
    ruta_diccionario = os.path.join(carpeta_html, "diccionario_html.json")

    # Asegurarte de que existe la carpeta base, la carpeta específica y el diccionario
    if not os.path.exists(carpeta_base):
        os.makedirs(carpeta_base)

    if not os.path.exists(carpeta_html):
        os.makedirs(carpeta_html)

    if not os.path.exists(ruta_diccionario):
        with open(ruta_diccionario, "w", encoding="utf-8") as archivo:
            json.dump({}, archivo)

    return ruta_diccionario


def cargar_diccionario(ruta_diccionario):
    """Carga el diccionario de URLs desde el archivo JSON."""
    with open(ruta_diccionario, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_diccionario(diccionario, ruta_diccionario):
    """Guarda el diccionario de URLs en el archivo JSON."""
    with open(ruta_diccionario, "w", encoding="utf-8") as archivo:
        json.dump(diccionario, archivo, ensure_ascii=False, indent=4)


import os


def obtener_nombre_archivo_unico(nombre_base, carpeta, extension="html"):
    """
    Genera un nombre de archivo único en una carpeta específica.
    Si el archivo contiene 'view' en el nombre y ya existe, añade un sufijo numérico.
    """
    # Si el nombre contiene 'view', añade un sufijo numérico
    if "view" or "developer" in nombre_base:
        nombre_final = f"{nombre_base}.{extension}"
        contador = 1

        # Mientras el archivo exista, agrega un sufijo
        while os.path.exists(os.path.join(carpeta, nombre_final)):
            nombre_final = f"{nombre_base}_{contador}.{extension}"
            contador += 1
    else:
        nombre_final = f"{nombre_base}.{extension}"

    return nombre_final


def guardar_html_crudo(enlace, contenido_html, nombre_carpeta):
    """Guarda el contenido HTML crudo en un archivo y actualiza el diccionario."""
    ruta_diccionario = comprobar_existencia_archivos(nombre_carpeta)
    diccionario = cargar_diccionario(ruta_diccionario)

    # Usar el ID del juego (extraído de la URL) como nombre base del archivo
    nombre_base = enlace.split("/")[-2]  # Extrae el ID o nombre para usarlo como base
    carpeta_base = "scraping\htmls"
    carpeta_html = os.path.join(carpeta_base, nombre_carpeta)

    # Obtener un nombre único para el archivo
    nombre_archivo = obtener_nombre_archivo_unico(nombre_base, carpeta_html)
    ruta_archivo = os.path.join(carpeta_html, nombre_archivo)

    # Guardar el HTML en el archivo
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_html)

    # Actualizar el diccionario con el nuevo nombre de archivo
    diccionario[enlace] = nombre_archivo
    guardar_diccionario(diccionario, ruta_diccionario)

    return ruta_archivo


def cargar_html_crudo(nombre_archivo, nombre_carpeta):
    """Carga el contenido HTML desde un archivo."""
    carpeta_base = "scraping\htmls"
    carpeta_html = os.path.join(carpeta_base, nombre_carpeta)
    ruta_archivo = os.path.join(carpeta_html, nombre_archivo)
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return archivo.read()
