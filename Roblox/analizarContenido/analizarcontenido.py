import analizarContenido.datosprimitivos as datosprimitivos
import analizarContenido.datosderivados as datosderivados
import analizarContenido.datosagregados as datosagregados
import json
import os

# DATOS PRIMITIVOS
# Gráfica de usuarios con más amigos
# Gráfica de grupos con más miembros
# Juegos por idiomas disponibles
# Palabras más comunes en descripciones de juegos
# Emoticonos más comunes en nombres de juegos

# DATOS DERIVADOS
# Análisis de sentimientos en descripciones de juegos
# Palabras negativas más comunes en descripciones de juegos
# Palabras positivas más comunes en descripciones de juegos

# DATOS AGREGADOS
# Número total de juegos
# Número total de grupos
# Número total de usuarios
# Media/max/min de amigos/seguidores
# Media/max/min de miembros de grupos
# Media/max/min de precios de servidor privado


def analizar(ruta_carpeta="dataSets"):
    """
    Función que realiza el análisis del contenido del json de Roblox.
    Parámetros:
        ruta_carpeta: Ruta de la carpeta que contiene el archivo json.
    """
    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith(".json"):
            ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
    diccionario_informe = {}
    datosprimitivos.obtener_datos_primitivos(data, diccionario_informe)
    datosderivados.obtener_datos_derivados(data, diccionario_informe)
    datosagregados.obtener_datos_agregados(data, diccionario_informe)
    return diccionario_informe
