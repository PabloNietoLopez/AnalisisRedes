import numpy as np


def obtener_datos_agregados(data, diccionario_informe):
    """
    Calcula los datos agregados de Roblox y los guarda en un diccionario:
    - Número total de juegos.
    - Número total de grupos.
    - Número total de usuarios.
    - Media, máximo y mínimo de amigos/seguidores.
    - Media, máximo y mínimo de miembros de grupos.
    - Media, máximo y mínimo de precios de servidor privado.

    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    num_grupos, num_usuarios, num_juegos = contar_elementos(data)
    amigos_max, amigos_min, amigos_media = calcular_estadisticas_amigos(data)
    miembros_max, miembros_min, miembros_media = calcular_estadisticas_grupos(data)
    precio_max, precio_min, precio_media = calcular_estadisticas_precios(data)

    diccionario_informe["numero_de_grupos"] = num_grupos
    diccionario_informe["numero_de_usuarios"] = num_usuarios
    diccionario_informe["numero_de_juegos"] = num_juegos
    diccionario_informe["max_amigos"] = amigos_max
    diccionario_informe["min_amigos"] = amigos_min
    diccionario_informe["media_amigos"] = amigos_media
    diccionario_informe["max_miembros_grupo"] = miembros_max
    diccionario_informe["min_miembros_grupo"] = miembros_min
    diccionario_informe["media_miembros_grupo"] = miembros_media
    diccionario_informe["max_precio_servidor"] = precio_max
    diccionario_informe["min_precio_servidor"] = precio_min
    diccionario_informe["media_precio_servidor"] = precio_media


def contar_elementos(data):
    """
    Cuenta el número de grupos, usuarios y juegos en los datos de Roblox.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    num_grupos = 0
    num_usuarios = 0
    num_juegos = 0

    # Recorrer los datos para contar los grupos, usuarios y juegos
    for juego in data:
        if "Creador" in juego:
            # Contar el grupo
            if "NombreGrupo" in juego["Creador"]:
                num_grupos += 1

        if "Miembros" in juego.get("Creador", {}):
            # Contar los usuarios en el grupo
            num_usuarios += len(juego["Creador"]["Miembros"])

        if "Titulo" in juego:
            # Contar los juegos
            num_juegos += 1

    return num_grupos, num_usuarios, num_juegos


def calcular_estadisticas_amigos(data):
    """
    Calcula media/max/min de amigos de los usuarios en Roblox.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    amigos_list = []

    # Recorrer los datos para obtener la información necesaria
    for juego in data:
        # Analizar los usuarios
        if "Creador" in juego and "Miembros" in juego["Creador"]:
            for miembro in juego["Creador"]["Miembros"]:
                if "Estadisticas" in miembro:
                    amigos_list.append(
                        miembro["Estadisticas"].get("Friends", 0)
                    )  # Obtener número de amigos

    # Calcular las estadísticas para amigos de usuarios
    if amigos_list:
        amigos_max = max(amigos_list)
        amigos_min = min(amigos_list)
        amigos_media = np.mean(amigos_list)
    else:
        amigos_max = amigos_min = amigos_media = 0

    return amigos_max, amigos_min, amigos_media


def calcular_estadisticas_grupos(data):
    """
    Calcula media/max/min de miembros de grupos en Roblox.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Rob
    """
    miembros_list = []

    # Recorrer los datos para obtener la información necesaria
    for juego in data:
        # Analizar los grupos
        if (
            "Creador" in juego
            and "NombreGrupo" in juego["Creador"]
            and "Miembros" in juego["Creador"]
        ):
            miembros_list.append(
                int(juego["Creador"]["NumeroMiembros"])
            )  # Número de miembros en el grupo

    # Calcular las estadísticas para miembros de grupos
    if miembros_list:
        miembros_max = max(miembros_list)
        miembros_min = min(miembros_list)
        miembros_media = np.mean(miembros_list)
    else:
        miembros_max = miembros_min = miembros_media = 0

    return miembros_max, miembros_min, miembros_media


def calcular_estadisticas_precios(data):
    """
    Calcula media/max/min de precios de servidor privado en Roblox.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Rob
    """
    precios_servidor = []

    # Recorrer los datos para obtener la información necesaria
    for juego in data:
        # Analizar los precios de servidor
        if "PrecioServidorPrivado" in juego:
            precio = float(juego["PrecioServidorPrivado"])
            if precio is not None:
                precios_servidor.append(precio)

    # Calcular las estadísticas para los precios de los servidores
    if precios_servidor:
        precio_max = max(precios_servidor)
        precio_min = min(precios_servidor)
        precio_media = np.mean(precios_servidor)
    else:
        precio_max = precio_min = precio_media = 0

    return precio_max, precio_min, precio_media
