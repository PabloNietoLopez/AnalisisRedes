import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from collections import defaultdict
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_imagenes = os.path.join(ruta_base, "Imagenes")
os.makedirs(ruta_imagenes, exist_ok=True)


def obtener_datos_derivados(data, diccionario_informe):
    """
    Realiza:
    - Análisis de sentimientos en descripciones de juegos.
    - Palabras negativas más comunes en descripciones de juegos.
    - Palabras positivas más comunes en descripciones de juegos.

    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    # Obtener los sentimientos de las descripciones de los juegos
    df_sentimientos = analizar_sentimiento_descripciones(data)
    # Generar gráfica
    print("Generando gráfica de sentimiento de las descripciones...")
    grafica_sentimiento(df_sentimientos, diccionario_informe)

    df_palabras = analizar_sentimiento_palabras(data)

    # Generar gráfica de palabras negativas más repetidas
    df_palabras_neg = palabras_negativas_mas_repetidas(df_palabras, num_palabras=10)
    # Generar gráfica
    print("Generando gráfica de palabras negativas más comunes...")
    grafica_palabras_negativas(df_palabras_neg, diccionario_informe)

    # Generar gráfica de palabras positivas más repetidas
    df_palabras_pos = palabras_positivas_mas_repetidas(df_palabras, num_palabras=10)
    # Generar gráfica
    print("Generando gráfica de palabras positivas más comunes...")
    grafica_palabras_positivas(df_palabras_pos, diccionario_informe)


def analizar_sentimiento_descripciones(data):
    """
    Guarda el sentimiento de las descripciones por número de juegos en un DataFrame.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    sentimientos = defaultdict(int)

    for juego in data:
        if "Descripcion" in juego:
            descripcion = juego["Descripcion"]

            blob = TextBlob(descripcion)
            polaridad = blob.sentiment.polarity  # Sentimiento de la descripción

            if polaridad > 0:
                sentimiento = "Positivo"
            elif polaridad == 0:
                sentimiento = "Neutral"
            else:
                sentimiento = "Negativo"

            sentimientos[sentimiento] += 1

    # Convertir el resultado a un DataFrame para facilitar el análisis
    df_sentimientos = pd.DataFrame(
        list(sentimientos.items()), columns=["Sentimiento", "Numero_de_juegos"]
    )

    return df_sentimientos


def grafica_sentimiento(df, diccionario_informe):
    """
    Genera una gráfica de barras con el número de juegos por sentimiento.
    Parámetros:
        df (DataFrame): DataFrame con los sentimientos y el número de juegos.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    if df.empty:
        print("No se encontraron descripciones para graficar.")
        return

    # Graficar los resultados
    plt.figure(figsize=(8, 6))
    plt.bar(df["Sentimiento"], df["Numero_de_juegos"], color=["green", "yellow", "red"])
    plt.title("Análisis de Sentimiento de las Descripciones de Juegos")
    plt.xlabel("Sentimiento")
    plt.ylabel("Número de juegos")
    plt.tight_layout()
    grafica_path = os.path.join(ruta_imagenes, "sentimiento.png")
    diccionario_informe["sentimiento"] = grafica_path
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


def analizar_sentimiento_palabras(data):
    """
    Guarda el sentimiento de las palabras en las descripciones de los juegos en un DataFrame.
    Parámetros:
        data (list): Lista de diccionarios con los datos de Roblox.
    """
    palabras = []

    for juego in data:
        if "Descripcion" in juego:
            descripcion = juego["Descripcion"]

            blob = TextBlob(descripcion)
            polaridad = blob.sentiment.polarity  # Sentimiento de la descripción

            # Categorizar el sentimiento
            if polaridad > 0:
                sentimiento = "Positivo"
            elif polaridad == 0:
                sentimiento = "Neutral"
            else:
                sentimiento = "Negativo"

            palabras.append((sentimiento, descripcion))

    # Convertir el resultado a un DataFrame para facilitar el análisis
    if palabras:  # Asegurarse de que la lista no esté vacía
        df_palabras = pd.DataFrame(palabras, columns=["Sentimiento", "Descripcion"])
    else:
        # Si la lista está vacía, se devuelve un DataFrame vacío con las columnas correctas
        df_palabras = pd.DataFrame(columns=["Sentimiento", "Descripcion"])
    return df_palabras


def palabras_negativas_mas_repetidas(df, num_palabras=10):
    """
    Obtiene en un DataFrame las palabras más comunes en las descripciones con sentimiento negativo y su frecuencia.
    Parámetros:
        df (DataFrame): DataFrame con los sentimientos y descripciones.
        num_palabras (int): Número de palabras más comunes a extraer.
    """
    # Asegurarse de que el DataFrame contiene datos
    if df.empty:
        print("El DataFrame está vacío.")
        return pd.DataFrame(columns=["Palabra", "Frecuencia"])

    # Extraer todas las palabras de las descripciones con sentimiento negativo
    palabras_negativas = []
    for descripcion in df[df["Sentimiento"] == "Negativo"]["Descripcion"]:
        tokens = preprocess(descripcion)
        palabras_negativas.extend(eliminar_stopwords(tokens))

    # Contar las palabras más frecuentes en las descripciones negativas
    word_counts = Counter(palabras_negativas).most_common(num_palabras)

    # Crear un DataFrame para las palabras y sus frecuencias
    words_df = pd.DataFrame(word_counts, columns=["Palabra", "Frecuencia"])

    return words_df


def grafica_palabras_negativas(df, diccionario_informe):
    """
    Grafica las palabras más frecuentes en las descripciones negativas.
    Parámetros:
        df (DataFrame): DataFrame con las palabras y sus frecuencias.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    plt.figure(figsize=(10, 6))
    plt.barh(df["Palabra"], df["Frecuencia"], color="salmon")
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabra")
    plt.title(f"Top 10 palabras más comunes en descripciones negativas")
    plt.gca().invert_yaxis()  # Invertir el eje Y para que la palabra más frecuente esté arriba
    plt.tight_layout()
    grafica_path = os.path.join(ruta_imagenes, "palabras_negativas.png")
    diccionario_informe["palabras_negativas"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()


def palabras_positivas_mas_repetidas(df, num_palabras=10):
    """
    Obtiene en un DataFrame las palabras más comunes en las descripciones con sentimiento positivo y su frecuencia.
    Parámetros:
        df (DataFrame): DataFrame con los sentimientos y descripciones.
        num_palabras (int): Número de palabras más comunes a extraer.
    """
    # Asegurarse de que el DataFrame contiene datos
    if df.empty:
        print("El DataFrame está vacío.")
        return pd.DataFrame(columns=["Palabra", "Frecuencia"])

    # Extraer todas las palabras de las descripciones con sentimiento negativo
    palabras_positivas = []
    for descripcion in df[df["Sentimiento"] == "Positivo"]["Descripcion"]:
        tokens = preprocess(descripcion)
        palabras_positivas.extend(eliminar_stopwords(tokens))

    # Contar las palabras más frecuentes en las descripciones positivas
    word_counts = Counter(palabras_positivas).most_common(num_palabras)

    # Crear un DataFrame para las palabras y sus frecuencias
    words_df = pd.DataFrame(word_counts, columns=["Palabra", "Frecuencia"])

    return words_df


def grafica_palabras_positivas(df, diccionario_informe):
    """
    Grafica las palabras más frecuentes en las descripciones negativas.
    Parámetros:
        df (DataFrame): DataFrame con las palabras y sus frecuencias.
        diccionario_informe (dict): Diccionario donde guardaremos los resultados.
    """
    plt.figure(figsize=(10, 6))
    plt.barh(df["Palabra"], df["Frecuencia"], color="lightgreen")
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabra")
    plt.title(f"Top 10 palabras más comunes en descripciones positivas")
    plt.gca().invert_yaxis()  # Invertir el eje Y para que la palabra más frecuente esté arriba
    plt.tight_layout()
    grafica_path = os.path.join(ruta_imagenes, "palabras_positivas.png")
    diccionario_informe["palabras_positivas"] = grafica_path
    plt.savefig(grafica_path)
    plt.show()
