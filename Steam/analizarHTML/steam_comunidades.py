import os
import json
from bs4 import BeautifulSoup


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
    try:
        if clase and id:
            elemento = soup.find(etiqueta_a_buscar, class_=clase, id=id)
        elif clase:
            elemento = soup.find(etiqueta_a_buscar, class_=clase)
        elif id:
            elemento = soup.find(etiqueta_a_buscar, id=id)
        else:
            return "No disponible"

        if elemento and buscar_enlace:
            enlace = elemento.find("a")
            return enlace.text.strip() if enlace else "No disponible"

        return elemento.text.strip() if elemento else "No disponible"
    except Exception as e:
        print(f"Error al extraer dato: {e}")
        return "No disponible"


def extraer_dato_con_bucle(soup, clase_padre, clase_a_buscar, etiqueta_a_buscar="div"):
    try:
        lista = []
        elementos_padres = soup.find_all("div", class_=clase_padre)

        for elemento_padre in elementos_padres:
            dato = elemento_padre.find(etiqueta_a_buscar, class_=clase_a_buscar)
            if dato:
                lista.append(dato.text.strip())

        return lista if lista else "No disponible"
    except Exception as e:
        print(f"Error al extraer datos con bucle: {e}")
        return []


def obtener_info_comunidad(ruta_archivo):
    try:
        contenido_html = leer_html_local(ruta_archivo)
        if not contenido_html:
            return None

        soup_comunidad = BeautifulSoup(contenido_html, "html.parser")

        # Extraer información de la comunidad
        nombre_juego = extraer_dato(soup_comunidad, clase="apphub_AppName ellipsis")
        lema_comunidad = extraer_dato(soup_comunidad, clase="customBrowseTitle")
        descripcion = extraer_dato(soup_comunidad, clase="customBrowseText")
        creaciones_mas_populares = extraer_dato_con_bucle(
            soup_comunidad, "workshop_item_row", "workshop_item_title ellipsis"
        )

        # Consolidar información en un diccionario
        comunidad_info = {
            "nombre": nombre_juego,
            "lema": lema_comunidad,
            "descripcion": descripcion,
            "creaciones_mas_populares": creaciones_mas_populares[:10],
        }

        return comunidad_info
    except Exception as e:
        print(f"Error al procesar el archivo {ruta_archivo}: {e}")
        return None


def procesar_comunidades():
    carpeta_html = os.path.join(os.getcwd(), "scraping", "htmls", "html_comunidades")
    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith(".html")]
    comunidades_info = []

    for archivo in archivos_html:
        ruta_archivo = os.path.join(carpeta_html, archivo)
        print(f"Procesando archivo: {ruta_archivo}")
        comunidad_info = obtener_info_comunidad(ruta_archivo)

        if comunidad_info:
            comunidades_info.append(comunidad_info)

    return comunidades_info


def guardar_comunidades_json(comunidades_info, filename="comunidades_info.json"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(comunidades_info, file, ensure_ascii=False, indent=4)
        print(
            f"Se han guardado los datos de {len(comunidades_info)} comunidades en '{filename}'."
        )
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")


def main():
    comunidades_info = procesar_comunidades()
    guardar_comunidades_json(comunidades_info)


if __name__ == "__main__":
    main()
