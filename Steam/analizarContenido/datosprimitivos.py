import matplotlib.pyplot as plt
from collections import Counter


def obtener_datos_primitivos(
    juegos, desarrolladores, usuarios, comentarios, eventos, comunidades
):
    """
    Función para generar gráficos basados en los datos primitivos.
    """
    graficar_generos_juegos(juegos)
    graficar_reseñas_juegos(juegos)
    graficar_seguidores_desarrolladores(desarrolladores)
    graficar_precios_juegos(juegos)


def graficar_precios_juegos(juegos):
    """
    Genera un gráfico de barras para comparar la cantidad de juegos que tienen cada precio.
    """
    for juego in juegos:
        if juego["precio"].lower() == "free to play":
            juego["precio"] = "0,00€"

    precios = []
    for juego in juegos:
        precio_str = juego["precio"]
        try:
            precio_num = float(precio_str.replace("€", "").replace(",", "."))
            precios.append(precio_num)
        except ValueError:
            precios.append(None)

    precios = [precio for precio in precios if precio is not None]
    contador_precios = Counter(precios)

    precios_unicos = list(contador_precios.keys())
    cantidad_juegos = list(contador_precios.values())
    precios_unicos.sort()
    cantidad_juegos_sorted = [contador_precios[precio] for precio in precios_unicos]

    plt.figure(figsize=(10, 6))
    plt.bar(
        [f"{precio}€" for precio in precios_unicos],
        cantidad_juegos_sorted,
        color="skyblue",
    )
    plt.title("Cantidad de Juegos por Precio", fontsize=14)
    plt.xlabel("Precio (€)", fontsize=12)
    plt.ylabel("Número de Juegos", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("analizarContenido/imagenes/precios_juegos.png")
    plt.show()


def graficar_generos_juegos(juegos):
    """
    Genera un gráfico de barras para comparar la cantidad de juegos por género.
    """
    generos = []
    for juego in juegos:
        if "generos" in juego:
            generos.extend(juego["generos"])

    contador_generos = Counter(generos)
    generos_unicos = list(contador_generos.keys())
    cantidad_juegos = list(contador_generos.values())

    plt.figure(figsize=(10, 6))
    plt.bar(generos_unicos, cantidad_juegos, color="salmon")
    plt.title("Cantidad de Juegos por Género", fontsize=14)
    plt.xlabel("Género", fontsize=12)
    plt.ylabel("Número de Juegos", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("analizarContenido/imagenes/juegos_genero.png")
    plt.show()


def graficar_reseñas_juegos(juegos):
    """
    Genera un gráfico de pastel para comparar la cantidad de juegos por tipo de reseña.
    """
    reseñas = []
    for juego in juegos:
        if "reseñas" in juego:
            reseñas.append(juego["reseñas"])

    contador_reseñas = Counter(reseñas)
    tipos_reseñas = list(contador_reseñas.keys())
    cantidad_juegos = list(contador_reseñas.values())

    plt.figure(figsize=(8, 8))
    plt.pie(
        cantidad_juegos,
        labels=tipos_reseñas,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"],
    )
    plt.title("Distribución de Reseñas de Juegos", fontsize=14)
    plt.axis("equal")
    plt.savefig("analizarContenido/imagenes/reseñas_juegos.png")
    plt.show()


def graficar_seguidores_desarrolladores(desarrolladores):
    """
    Genera un gráfico de barras horizontal con el número de seguidores por desarrollador.

    :param desarrolladores: Lista de diccionarios con 'nombre' y 'seguidores' de los desarrolladores.
                            Ejemplo: [{"nombre": "Valve", "seguidores": "779,059"}, ...]
    """
    # Extraer los nombres y convertir los seguidores a enteros
    nombres = []
    seguidores = []

    for desarrollador in desarrolladores:
        try:
            # Obtener el nombre y el número de seguidores
            nombre = desarrollador.get("nombre", "")
            seguidores_raw = desarrollador.get("seguidores", "")

            # Validar que los datos no estén vacíos o sean incorrectos
            if nombre and seguidores_raw:
                # Eliminar comas y convertir el número de seguidores a entero
                seguidores_clean = str(seguidores_raw).replace(",", "")
                seguidores.append(int(seguidores_clean))
                nombres.append(nombre)
        except (KeyError, ValueError):
            continue  # Ignorar desarrolladores con datos faltantes o formato incorrecto

    # Verificar si tenemos datos antes de continuar
    if not nombres or not seguidores:
        return

    # Ordenar por seguidores de forma descendente
    datos_ordenados = sorted(zip(seguidores, nombres), reverse=True)
    seguidores, nombres = zip(*datos_ordenados)

    # Crear el gráfico de barras horizontal
    plt.figure(figsize=(12, 8))
    plt.barh(nombres, seguidores, color="teal")

    # Personalizar la gráfica
    plt.title("Número de Seguidores por Desarrollador", fontsize=16)
    plt.xlabel("Número de Seguidores", fontsize=14)
    plt.ylabel("Desarrolladores", fontsize=14)
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.gca().invert_yaxis()  # Invertir el eje Y para mostrar el más seguido arriba

    # Mostrar la gráfica
    plt.tight_layout()
    plt.savefig("analizarContenido/imagenes/seguidores_desarrolladores.png")
    plt.show()


def grafico_cantidad_por_rango_precio(juegos):
    rangos = {"<10": 0, "10-30": 0, "30-60": 0, ">60": 0}
    for juego in juegos:
        precio = juego["precio"]
        if precio < 10:
            rangos["<10"] += 1
        elif precio <= 30:
            rangos["10-30"] += 1
        elif precio <= 60:
            rangos["30-60"] += 1
        else:
            rangos[">60"] += 1

    plt.bar(rangos.keys(), rangos.values(), color="teal")
    plt.title("Cantidad de juegos por rango de precio")
    plt.xlabel("Rango de precio")
    plt.ylabel("Cantidad de juegos")
    plt.savefig("analizarContenido/imagenes/cantidad_rango_precio.png")
    plt.show()
