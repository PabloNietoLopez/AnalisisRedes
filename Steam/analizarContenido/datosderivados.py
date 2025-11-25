import matplotlib.pyplot as plt
from collections import Counter
import re
import nltk

nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict
import numpy as np

sid = SentimentIntensityAnalyzer()


def obtener_datos_derivados(
    juegos, desarrolladores, usuarios, comentarios, eventos, comunidades
):

    graficar_almacenamiento(juegos)
    grafico_promedio_valoraciones(juegos, comentarios)
    grafico_valoracion_con_comunidad(juegos, comentarios, comunidades)
    grafico_distribucion_sentimientos_barras(juegos, comentarios)
    grafica_sentimiento_medio_total(comentarios)


def extraer_almacenamiento(requisito_str):
    """
    Extrae la cantidad de almacenamiento de los requisitos de un string.
    """
    almacenamiento = re.search(r"Almacenamiento: (\d+\s?[GM]B)", requisito_str)
    return almacenamiento.group(1) if almacenamiento else "Desconocido"


def analizar_almacenamiento(juegos):
    """
    Analiza los requisitos de almacenamiento de los juegos y extrae los valores clave.
    """
    almacenamientos = []

    for juego in juegos:
        # Si existen los campos de almacenamiento, extraemos los valores
        if "requisitos_minimos" in juego:
            minimos = extraer_almacenamiento(juego["requisitos_minimos"])
            almacenamientos.append(minimos)

        if "requisitos_recomendados" in juego:
            recomendados = extraer_almacenamiento(juego["requisitos_recomendados"])
            almacenamientos.append(recomendados)

    # Filtrar los valores "Desconocido"
    almacenamientos = [a for a in almacenamientos if a != "Desconocido"]

    return almacenamientos


def convertir_a_gb(almacenamiento):
    """
    Convierte los valores de almacenamiento (GB, MB) a un valor numérico en GB.
    """
    # Si el valor está en MB, lo convertimos a GB
    if "MB" in almacenamiento:
        valor = int(re.search(r"(\d+)", almacenamiento).group(1))
        return valor / 1024  # Convertir MB a GB
    elif "GB" in almacenamiento:
        valor = int(re.search(r"(\d+)", almacenamiento).group(1))
        return valor
    return 0


def graficar_almacenamiento(juegos):
    """
    Genera un gráfico para comparar las cantidades de almacenamiento más comunes en los juegos.
    """
    almacenamientos = analizar_almacenamiento(juegos)

    # Contar la frecuencia de los distintos valores de almacenamiento
    contador_almacenamiento = Counter(almacenamientos)

    # Convertir los valores a GB para ordenar
    almacenamientos_numericos = [
        (almacenamiento, convertir_a_gb(almacenamiento))
        for almacenamiento in contador_almacenamiento.keys()
    ]

    # Ordenar los valores por tamaño (en GB)
    almacenamientos_numericos.sort(key=lambda x: x[1])

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(
        [a[0] for a in almacenamientos_numericos],
        [contador_almacenamiento[a[0]] for a in almacenamientos_numericos],
        color="lightgreen",
    )

    # Personalizar la gráfica
    plt.title("Requisitos de Almacenamiento de Juegos", fontsize=14)
    plt.xlabel("Espacio de Almacenamiento", fontsize=12)
    plt.ylabel("Número de Juegos", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Mostrar la gráfica
    plt.tight_layout()
    plt.savefig("analizarContenido/imagenes/almacenamiento_juegos.png")
    plt.show()


def grafico_promedio_valoraciones(juegos, comentarios):
    valoraciones_promedio = {}
    i = 0
    numJuego = 0

    # Recorremos los juegos y los comentarios correspondientes
    for juego in juegos:
        variable = juego["nombre"]
        numJuego = numJuego + 1
        grupo = comentarios[i]
        comen = grupo[0]
        variableP = comen["juego_que_comenta"]
        variable1 = re.sub(r"[^a-zA-Z0-9]", "", variable)
        variable2 = re.sub(r"[^a-zA-Z0-9]", "", variableP)

        valoraciones_numericas = []

        if variable1 == variable2:
            # Obtener las valoraciones de la sublista correspondiente al juego
            valoraciones = [
                comentario["valoracion"]
                for comentario in comentarios[i]
                if comentario["valoracion"] != "No disponible"
            ]

            # Convertir las valoraciones a valores numéricos (1 = Recomendado, 0 = No Recomendado)
            for valoracion in valoraciones:
                if valoracion == "Recomendado":
                    valoraciones_numericas.append(1)
                elif valoracion == "No recomendado":
                    valoraciones_numericas.append(0)
        else:
            i = i - 1

        i = i + 1

        # Calcular el promedio si hay valoraciones válidas
        if valoraciones_numericas:
            valoraciones_promedio[juego["nombre"]] = sum(valoraciones_numericas) / len(
                valoraciones_numericas
            )
        else:
            valoraciones_promedio[juego["nombre"]] = 0

    # Crear una figura más ancha para evitar solapamientos en el eje X
    plt.figure(figsize=(12, 6))  # Ajusta el tamaño de la figura (ancho, alto)

    # Crear gráfico de barras con las valoraciones promedio por juego
    plt.bar(
        valoraciones_promedio.keys(), valoraciones_promedio.values(), color="purple"
    )
    plt.title("Promedio de valoraciones por juego")
    plt.ylabel("Valoración promedio")
    plt.xticks(rotation=45, ha="right")  # Gira los nombres 45° y alinea a la derecha
    plt.tight_layout()

    # Guardar la figura y mostrarla
    plt.savefig("analizarContenido/imagenes/promedio_valoraciones.png")
    plt.show()


def grafico_valoracion_con_comunidad(juegos, comentarios, comunidades):

    valoracion_con_comunidad = []
    valoracion_sin_comunidad = []
    juegos_con_comunidad = []
    esta = False
    i = 0
    numJuego = 0

    for comunidad in comunidades:
        if comunidad["nombre_juego"] != "No disponible":
            juegos_con_comunidad.append(comunidad["nombre_juego"])

    # Recorremos los juegos y los comentarios correspondientes
    for juego in juegos:

        variable = juego["nombre"]
        numJuego = numJuego + 1
        grupo = comentarios[i]
        comen = grupo[0]
        variableP = comen["juego_que_comenta"]
        variable1 = re.sub(r"[^a-zA-Z0-9]", "", variable)
        variable2 = re.sub(r"[^a-zA-Z0-9]", "", variableP)
        valoraciones_numericas = []

        if variable1 == variable2:
            # Obtener las valoraciones de la sublista correspondiente al juego
            valoraciones = [
                comentario["valoracion"]
                for comentario in comentarios[i]
                if comentario["valoracion"] != "No disponible"
            ]

            # Convertir las valoraciones a valores numéricos (1 = Recomendado, 0 = No Recomendado)

            for valoracion in valoraciones:
                if valoracion == "Recomendado":
                    valoraciones_numericas.append(1)
                elif valoracion == "No Recomendado":
                    valoraciones_numericas.append(0)
        else:
            i = i - 1

        i = i + 1

        # Calcular el promedio si hay valoraciones válidas
        promedio = (
            sum(valoraciones_numericas) / len(valoraciones_numericas)
            if valoraciones_numericas
            else 0
        )

        # Clasificar el juego según si tiene comunidad

        for jueg in juegos_con_comunidad:
            if juego["nombre"] == jueg:
                esta = True

        if esta:
            valoracion_con_comunidad.append(promedio)
        else:
            valoracion_sin_comunidad.append(promedio)

        esta = False

    # Crear gráfico de barras comparando las valoraciones promedio con y sin comunidad
    promedio_con_comunidad = (
        sum(valoracion_con_comunidad) / len(valoracion_con_comunidad)
        if valoracion_con_comunidad
        else 0
    )
    promedio_sin_comunidad = (
        sum(valoracion_sin_comunidad) / len(valoracion_sin_comunidad)
        if valoracion_sin_comunidad
        else 0
    )

    plt.bar(
        ["Con Comunidad", "Sin Comunidad"],
        [promedio_con_comunidad, promedio_sin_comunidad],
        color=["blue", "gray"],
    )
    plt.title("Valoraciones promedio según comunidad")
    plt.ylabel("Valoración promedio")
    plt.savefig("analizarContenido/imagenes/valoraciones_comunidad.png")
    plt.show()


# Función para calcular el sentimiento de cada comentario
def calcular_sentimiento(comentarios):
    sentimientos = []
    for comentario in comentarios:
        # Obtenemos el texto del comentario
        texto = comentario["descripcion"]
        # Calculamos el sentimiento usando SentimentIntensityAnalyzer
        puntaje_sentimiento = sid.polarity_scores(texto)
        # El puntaje positivo, negativo y neutral de cada comentario
        sentimientos.append(puntaje_sentimiento["compound"])
    return sentimientos


def grafico_distribucion_sentimientos_barras(juegos, comentarios):
    # Diccionario para almacenar los sentimientos por juego
    sentimientos_por_juego = defaultdict(
        lambda: {"positivo": 0, "negativo": 0, "neutral": 0}
    )

    # Iterar sobre los juegos y sus correspondientes lotes de comentarios
    for juego, comentarios_lote in zip(juegos, comentarios):
        for comentario in comentarios_lote:
            descripcion = comentario["descripcion"]
            puntaje = sid.polarity_scores(descripcion)["compound"]

            # Clasificar el sentimiento
            sentimiento = (
                "positivo"
                if puntaje > 0.05
                else "negativo" if puntaje < -0.05 else "neutral"
            )
            sentimientos_por_juego[juego["nombre"]][sentimiento] += 1

    # Preparar datos para la gráfica
    juegos_nombres = list(sentimientos_por_juego.keys())
    positivos = [sentimientos_por_juego[juego]["positivo"] for juego in juegos_nombres]
    negativos = [sentimientos_por_juego[juego]["negativo"] for juego in juegos_nombres]
    neutrales = [sentimientos_por_juego[juego]["neutral"] for juego in juegos_nombres]

    # Índices para el gráfico
    x = np.arange(len(juegos_nombres))  # Posiciones de las barras

    # Configurar el tamaño de la gráfica
    plt.figure(figsize=(12, 6))  # Ajusta el tamaño (ancho, alto)

    # Crear las barras
    bar_width = 0.2
    plt.bar(x - bar_width, positivos, width=bar_width, color="green", label="Positivo")
    plt.bar(x, neutrales, width=bar_width, color="gray", label="Neutral")
    plt.bar(x + bar_width, negativos, width=bar_width, color="red", label="Negativo")

    # Configurar el gráfico
    plt.xticks(x, juegos_nombres, rotation=45, ha="right")  # Rotar y alinear etiquetas
    plt.title("Distribución de Sentimientos por Juego")
    plt.ylabel("Número de Comentarios")
    plt.xlabel("Juegos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("analizarContenido/imagenes/distribucion_sentimientos.png")
    plt.show()


def grafica_sentimiento_medio_total(comentarios):
    # Lista para almacenar todos los puntajes de sentimiento
    puntajes_totales = []

    # Iterar sobre todos los lotes de comentarios
    for comentarios_lote in comentarios:
        for comentario in comentarios_lote:
            descripcion = comentario["descripcion"]
            puntaje = sid.polarity_scores(descripcion)["compound"]
            puntajes_totales.append(puntaje)

    # Calcular el promedio general de sentimiento
    sentimiento_promedio_total = (
        sum(puntajes_totales) / len(puntajes_totales) if puntajes_totales else 0
    )

    # Crear la gráfica de una sola barra
    plt.figure(figsize=(5, 6))
    colores = [
        (
            "red"
            if sentimiento_promedio_total < 0
            else "green" if sentimiento_promedio_total > 0 else "gray"
        )
    ]
    plt.bar(
        ["Sentimiento Medio Total"],
        [sentimiento_promedio_total],
        color=colores,
        width=0.6,
    )

    # Agregar detalles a la gráfica
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")  # Línea neutral
    plt.title("Sentimiento Medio Total de los Comentarios")
    plt.ylabel("Sentimiento Promedio")
    plt.ylim(-1, 1)  # Escala de sentimiento (-1: muy negativo, 1: muy positivo)
    plt.tight_layout()

    # Mostrar valor numérico encima de la barra
    plt.text(
        0,
        sentimiento_promedio_total
        + (0.05 if sentimiento_promedio_total >= 0 else -0.05),
        f"{sentimiento_promedio_total:.2f}",
        ha="center",
        va="bottom" if sentimiento_promedio_total >= 0 else "top",
    )
    plt.savefig("analizarContenido/imagenes/sentimiento_medio_total.png")
    plt.show()
