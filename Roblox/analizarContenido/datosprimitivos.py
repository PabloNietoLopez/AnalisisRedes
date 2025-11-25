import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from collections import defaultdict
import re
import nltk
from nltk.corpus import stopwords
import os

# Descargar stopwords de NLTK
nltk.download("stopwords")
nltk.download("punkt")

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagenes = os.path.join(ruta_base, "Imagenes")
os.makedirs(ruta_imagenes, exist_ok=True)


def obtener_datos_primitivos(data, diccionario_informe):
    """
    Realiza:
    - Gráfica de usuarios con más amigos.
    - Gráfica de grupos con más miembros.
    - Gráfica de número de juegos por idioma.
    - Gráfica de las palabras más comunes en las descripciones de los juegos.
    - Gráfica de los emoticonos más comunes en los títulos de los juegos.

    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    # Obtener los usuarios con más amigos
    df_usuarios = obtener_usuarios_con_mas_amigos(data)
    # Generar gráfica
    print("Generando gráfica de usuarios con más amigos...")
    grafica_usuarios_con_mas_amigos(df_usuarios, diccionario_informe)

    # Obtener los grupos con más miembros
    df_grupos = obtener_grupos_con_mas_miembros(data)
    # Generar gráfica
    print("Generando gráfica de grupos con más miembros...")
    grafica_grupos_con_mas_miembros(df_grupos, diccionario_informe)

    # Obtener el número de juegos por idioma
    df_idiomas = contar_idiomas(data)
    # Generar gráfica
    print("Generando gráfica de número de juegos por idioma...")
    grafica_idiomas(df_idiomas, diccionario_informe)

    # Obtener las palabras más comunes en las descripciones de los juegos
    df_palabras = obtener_palabras_comunes(data)
    # Generar gráfica
    print(
        "Generando gráfica de las palabras más comunes en las descripciones de los juegos..."
    )
    grafica_palabras_comunes(df_palabras, diccionario_informe)

    # Obtener los emoticonos más comunes en los títulos de los juegos
    df_emoticonos = obtener_emoticonos_comunes(data)
    # Generar gráfica
    print("Generando gráfica de los emoticonos más comunes...")
    grafica_emoticonos_comunes(df_emoticonos, diccionario_informe)


def obtener_usuarios_con_mas_amigos(data):
    """
    Guarda en un DataFrame los usuarios con más amigos en Roblox.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    usuarios = []

    # Recorrer los grupos en los datos
    for grupo in data:
        # Verificar si el grupo tiene miembros
        if "Creador" in grupo and "Miembros" in grupo["Creador"]:
            for miembro in grupo["Creador"]["Miembros"]:
                nombre_usuario = miembro["Nombre"]
                if "Estadisticas" in miembro and "Friends" in miembro["Estadisticas"]:
                    amigos = miembro["Estadisticas"]["Friends"]
                usuarios.append((nombre_usuario, amigos))

    # Crear un DataFrame con los usuarios y sus estadísticas
    df = pd.DataFrame(usuarios, columns=["Usuario", "Amigos"])

    return df


def grafica_usuarios_con_mas_amigos(df, diccionario_informe):
    """
    Grafica los 10 usuarios con más amigos y guarda la imagen en el diccionario para el informe.
    Parámetros:
        df (DataFrame): DataFrame con los usuarios y sus amigos.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    # Obtener los 10 usuarios con más amigos
    top_usuarios = df.nlargest(10, "Amigos")

    # Graficar los resultados
    plt.figure(figsize=(12, 6))
    plt.bar(top_usuarios["Usuario"], top_usuarios["Amigos"], color="skyblue")
    plt.title("Usuarios con más amigos en Roblox")
    plt.xlabel("Usuario")
    plt.ylabel("Cantidad de Amigos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    grafica_path = os.path.join(ruta_imagenes, "usuarios_mas_amigos.png")
    diccionario_informe["usuarios_mas_amigos"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


def obtener_grupos_con_mas_miembros(data):
    """
    Guarda en un DataFrame los grupos con más miembros en Roblox.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    grupos = []

    # Recorrer los datos y extraer los grupos y su número de miembros
    for grupo in data:
        if "Creador" in grupo and "NombreGrupo" in grupo["Creador"]:
            if grupo["Creador"]["Tipo"] == "Grupo":
                nombre_grupo = grupo["Creador"]["NombreGrupo"]
                num_miembros = float(grupo["Creador"]["NumeroMiembros"])
            grupos.append((nombre_grupo, num_miembros))

    # Crear un DataFrame con los grupos y su número de miembros
    df = pd.DataFrame(grupos, columns=["Grupo", "Miembros"])

    return df


def grafica_grupos_con_mas_miembros(df, diccionario_informe):
    """
    Grafica los 10 grupos con más miembros y guarda la imagen en el diccionario para el informe.
    Parámetros:
        df (DataFrame): DataFrame con los grupos y sus miembros.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    if df.empty:
        print("No se encontraron grupos para graficar.")
        return

    # Obtener los 10 grupos con más miembros
    top_grupos = df.nlargest(10, "Miembros")

    # Graficar los resultados
    plt.figure(figsize=(12, 6))
    plt.bar(top_grupos["Grupo"], top_grupos["Miembros"], color="lightcoral")
    plt.title("Grupos con más miembros en Roblox")
    plt.xlabel("Grupo")
    plt.ylabel("Número de Miembros")
    plt.xticks(rotation=45)
    plt.tight_layout()
    grafica_path = os.path.join(ruta_imagenes, "grupos_mas_miembros.png")
    diccionario_informe["grupos_mas_miembros"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


# Diccionario de correspondencia de abreviaturas de idiomas a nombre completo
IDIOMAS_CORRESPONDENCIA = {
    "es": "Español",
    "en": "Inglés",
    "x-default": "Por defecto",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano",
    "pt": "Portugués",
    "pl": "Polaco",
    "ja": "Japonés",
    "ko": "Coreano",
    "zh": "Chino",
    "id": "Indonesio",
    "tr": "Turco",
    "th": "Tailandés",
    "vi": "Vietnamita",
    "ru": "Ruso",
    "ar": "Árabe",
    "hi": "Hindi",
    "sv": "Sueco",
    "no": "Noruego",
    "da": "Danés",
    "fi": "Finlandés",
}


def contar_idiomas(data):
    """
    Guarda en un DataFrame el número de juegos por idioma disponible.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    idiomas_count = defaultdict(int)

    # Recorrer los datos y contar los idiomas disponibles en cada juego
    for juego in data:
        if "IdiomasDisponibles" in juego:
            idiomas = juego["IdiomasDisponibles"]
            for idioma in idiomas:
                # Reemplazar la abreviatura del idioma por su nombre completo
                idioma_completo = IDIOMAS_CORRESPONDENCIA.get(
                    idioma, idioma
                )  # Usa la abreviatura si no se encuentra el nombre completo
                idiomas_count[idioma_completo] += 1

    # Convertir el resultado a un DataFrame para facilitar el análisis
    df_idiomas = pd.DataFrame(
        list(idiomas_count.items()), columns=["Idioma", "Numero_de_juegos"]
    )

    return df_idiomas


def grafica_idiomas(df, diccionario_informe):
    """
    Grafica el número de juegos por idioma y guarda la imagen en el diccionario para el informe.
    Parámetros:
        df (DataFrame): DataFrame con los idiomas y el número de juegos.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    if df.empty:
        print("No se encontraron idiomas para graficar.")
        return

    # Graficar los resultados
    plt.figure(figsize=(12, 6))
    plt.bar(df["Idioma"], df["Numero_de_juegos"], color="skyblue")
    plt.title("Número de juegos por idioma")
    plt.xlabel("Idioma")
    plt.ylabel("Número de juegos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    grafica_path = os.path.join(ruta_imagenes, "juegos_por_idioma.png")
    diccionario_informe["juegos_por_idioma"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


# Función para preprocesar texto tokenizando y convirtiendo a minúsculas
def preprocess(text):
    tknzr = nltk.tokenize.TweetTokenizer()
    tokens = [t.lower() for t in tknzr.tokenize(text)]
    return tokens


# Función para eliminar palabras vacías (stopwords) del texto
def eliminar_stopwords(tokens):
    stop_words = set(stopwords.words("english"))
    stop_words_es = set(stopwords.words("spanish"))
    filtered_tokens = [
        word
        for word in tokens
        if word not in stop_words and word not in stop_words_es and word.isalpha()
    ]
    return filtered_tokens


def obtener_palabras_comunes(data):
    """
    Guarda en un DataFrame las palabras más comunes en las descripciones de los juegos.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    palabras = []

    # Recorrer los datos y extraer las descripciones de los juegos
    for juego in data:
        if "Descripcion" in juego:
            descripcion = juego["Descripcion"]
            tokens = preprocess(descripcion)
            tokens_filtrados = eliminar_stopwords(tokens)
            palabras.extend(tokens_filtrados)

    # Contar las frecuencias de cada palabra
    contador_palabras = Counter(palabras)

    # Crear un DataFrame con las palabras y su frecuencia
    df_palabras = pd.DataFrame(
        contador_palabras.items(), columns=["Palabra", "Frecuencia"]
    )

    return df_palabras


def grafica_palabras_comunes(df, diccionario_informe):
    """
    Grafica las 10 palabras más comunes en las descripciones de los juegos y guarda la imagen en el diccionario para el informe.
    Parámetros:
        df (DataFrame): DataFrame con las palabras y su frecuencia.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    if df.empty:
        print("No se encontraron palabras para graficar.")
        return

    # Obtener las 10 palabras más comunes
    top_palabras = df.nlargest(10, "Frecuencia")

    # Graficar los resultados
    plt.figure(figsize=(12, 6))
    plt.bar(top_palabras["Palabra"], top_palabras["Frecuencia"], color="lightgreen")
    plt.title("Palabras más comunes en las descripciones de los juegos de Roblox")
    plt.xlabel("Palabra")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    grafica_path = os.path.join(ruta_imagenes, "palabras_comunes.png")
    diccionario_informe["palabras_comunes"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


# Expresión regular para encontrar emoticonos
emoji_pattern = re.compile(
    "[\U0001F600-\U0001F64F"  # Emoticonos
    "\U0001F300-\U0001F5FF"  # Símbolos y pictogramas
    "\U0001F680-\U0001F6FF"  # Transporte y mapas
    "\U0001F700-\U0001F77F"  # Alquimia
    "\U0001F780-\U0001F7FF"  # Geometría
    "\U0001F800-\U0001F8FF"  # Manos y señales
    "\U0001F900-\U0001F9FF"  # Emojis de personas y cuerpos
    "\U0001FA00-\U0001FA6F"  # Más emojis de personas
    "\U0001FA70-\U0001FAFF"  # Más símbolos y pictogramas
    "\U00002700-\U000027BF"  # Emoticonos pequeños
    "]+",
    flags=re.UNICODE,
)


def obtener_emoticonos_comunes(data):
    """
    Guarda en un DataFrame los emoticonos más comunes en los títulos de los juegos.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    emoticonos = []

    # Recorrer los datos y extraer los títulos de los juegos
    for juego in data:
        if "Titulo" in juego:
            titulo = juego["Titulo"]
            # Buscar todos los emoticonos en el título
            emoticonos_en_titulo = emoji_pattern.findall(titulo)
            emoticonos.extend(emoticonos_en_titulo)

    # Contar las frecuencias de cada emoticono
    contador_emoticonos = Counter(emoticonos)

    # Crear un DataFrame con los emoticonos y su frecuencia
    df_emoticonos = pd.DataFrame(
        contador_emoticonos.items(), columns=["Emoticono", "Frecuencia"]
    )

    return df_emoticonos


def grafica_emoticonos_comunes(df, diccionario_informe):
    """
    Grafica los 10 emoticonos más comunes en los títulos de los juegos y guarda la imagen en el diccionario para el informe.
    Parámetros:
        df (DataFrame): DataFrame con los emoticonos y su frecuencia.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    if df.empty:
        print("No se encontraron emoticonos para graficar.")
        return

    # Obtener los 10 emoticonos más comunes
    top_emoticonos = df.nlargest(10, "Frecuencia")

    plt.rcParams["font.family"] = "Segoe UI Emoji"  # Fuente que soporta emojis
    # Graficar los resultados
    plt.figure(figsize=(12, 6))
    plt.bar(
        top_emoticonos["Emoticono"], top_emoticonos["Frecuencia"], color="lightcoral"
    )
    plt.title("Emoticonos más comunes en los títulos de los juegos de Roblox")
    plt.xlabel("Emoticono")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    grafica_path = os.path.join(ruta_imagenes, "emoticonos_comunes.png")
    diccionario_informe["emoticonos_comunes"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()
