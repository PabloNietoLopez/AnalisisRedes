import matplotlib.pyplot as plt
from collections import Counter
import warnings
import re

# Silenciar warnings específicos (ES UN WARNING PARA LOS CARACTERES CHINOS, NO UN ERROR)
warnings.filterwarnings("ignore", category=UserWarning, message=".*Glyph.*missing.*")


def obtener_datos_agregados(
    juegos, desarrolladores, usuarios, comentarios, eventos, comunidades
):

    graficar_juegos_por_fecha(juegos)
    graficar_juegos_creados_desarrolladores(desarrolladores)
    grafico_valoracion_promedio_por_genero(juegos, comentarios)


def graficar_juegos_por_fecha(juegos):
    """
    Genera un gráfico de barras para mostrar la cantidad de juegos lanzados por año.
    """
    fechas = []

    for juego in juegos:
        if "fecha" in juego:
            # Extraer solo el año de la fecha de lanzamiento
            try:
                año = juego["fecha"].split()[-1]  # Tomamos el último elemento (el año)
                fechas.append(año)
            except IndexError:
                continue  # Si la fecha no tiene formato esperado, ignorar

    # Contar cuántos juegos hay por año
    contador_fechas = Counter(fechas)

    # Extraer los años y la cantidad de juegos por año
    años = list(contador_fechas.keys())
    cantidad_juegos = list(contador_fechas.values())

    # Ordenar por año
    años_sorted = sorted(años, key=lambda x: int(x))
    cantidad_juegos_sorted = [contador_fechas[año] for año in años_sorted]

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(años_sorted, cantidad_juegos_sorted, color="lightgreen")

    # Personalizar la gráfica
    plt.title("Cantidad de Juegos Lanzados por Año", fontsize=14)
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Número de Juegos", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Mostrar la gráfica
    plt.tight_layout()
    plt.savefig("analizarContenido/imagenes/juegos_fechas.png")
    plt.show()


def graficar_juegos_creados_desarrolladores(desarrolladores):
    """
    Genera un gráfico de barras horizontal con el número de juegos creados por desarrollador.

    :param desarrolladores: Lista de diccionarios con 'nombre' y 'juegos_creados' de los desarrolladores.
                            Ejemplo: [{"nombre": "Valve", "juegos_creados": [...]}, ...]
    """
    # Extraer los nombres y la cantidad de juegos creados
    nombres = []
    juegos_creados = []

    for desarrollador in desarrolladores:
        try:
            nombre = desarrollador["nombre"]
            juegos = desarrollador.get(
                "juegos_creados", []
            )  # Obtener juegos creados, por defecto lista vacía
            if isinstance(juegos, list):  # Verificar que juegos_creados sea una lista
                juegos_creados.append(len(juegos))
            else:
                juegos_creados.append(0)  # Si no es una lista, poner 0 juegos
            nombres.append(nombre)
        except KeyError:
            continue  # Ignorar desarrolladores con datos faltantes

    # Ordenar por número de juegos creados de forma descendente
    datos_ordenados = sorted(zip(juegos_creados, nombres), reverse=True)
    juegos_creados, nombres = zip(*datos_ordenados)

    # Crear el gráfico de barras horizontal
    plt.figure(figsize=(12, 8))
    plt.barh(nombres, juegos_creados, color="orange")

    # Personalizar la gráfica
    plt.title("Número de Juegos Creados por Desarrollador", fontsize=16)
    plt.xlabel("Número de Juegos", fontsize=14)
    plt.ylabel("Desarrolladores", fontsize=14)
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.gca().invert_yaxis()  # Invertir el eje Y para mostrar el más productivo arriba

    # Mostrar la gráfica
    plt.tight_layout()
    plt.savefig("analizarContenido/imagenes/juegos_desarrolladores.png")
    plt.show()


def grafico_valoracion_promedio_por_genero(juegos, comentarios):
    valoraciones_por_genero = {}
    numJuego = 0
    numCom = 0
    i = 0
    # Recorremos cada juego y sus comentarios
    for juego in juegos:
        variable = juego["nombre"]
        grupo = comentarios[i]
        comen = grupo[0]
        variableP = comen["juego_que_comenta"]
        variable1 = re.sub(r"[^a-zA-Z0-9]", "", variable)
        variable2 = re.sub(r"[^a-zA-Z0-9]", "", variableP)
        numJuego = numJuego + 1
        valoraciones_numericas = []

        if variable1 == variable2:
            # Obtener los comentarios del juego (están en la sublista correspondiente)
            valoraciones = [
                comentario["valoracion"]
                for comentario in comentarios[i]
                if comentario["valoracion"] != "No disponible"
            ]
            numCom = numCom + 1
            # Convertir las valoraciones a valores numéricos
            for valoracion in valoraciones:
                if valoracion == "Recomendado":
                    valoraciones_numericas.append(1)
                elif valoracion == "No recomendado":
                    valoraciones_numericas.append(0)
        else:
            i = i - 1

        i = i + 1

        if valoraciones_numericas:  # Solo procesar si hay valoraciones válidas
            for genero in juego["generos"]:
                # Guardar las valoraciones correspondientes a cada género
                valoraciones_por_genero.setdefault(genero, []).extend(
                    valoraciones_numericas
                )

    # Calcular la valoración promedio por género
    generos = list(valoraciones_por_genero.keys())
    promedios = [
        sum(valoraciones) / len(valoraciones)
        for valoraciones in valoraciones_por_genero.values()
    ]

    # Crear el gráfico de barras
    plt.bar(generos, promedios, color="cyan")
    plt.title("Valoración promedio por género (Recomendado/No Recomendado)")
    plt.xlabel("Género")
    plt.ylabel("Valoración promedio")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("analizarContenido/imagenes/promedio_por_genero.png")
    plt.show()
