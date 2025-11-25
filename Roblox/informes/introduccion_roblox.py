from string import Template
import os


def generar_intro():
    yaml_metadatos = """---
geometry: margin=2cm
fontsize: 12pt
fontfamily: times
papersize: a4
header-includes:
  - \\usepackage{graphicx}
---

"""
    return yaml_metadatos


def generar_portada():
    portada = r"""
\begin{titlepage}
\begin{center}

\includegraphics[width=0.3\textwidth]{ucm.png} \\[1cm] 

{\Huge \textbf{Análisis de Roblox como red social}} \\[0.5cm]

{\Large Análisis de Redes Sociales} \\[1.5cm]

{\Large \textbf{Miguel Ángel Molina de la Rosa}} \\[0.5cm]

{\Large \textbf{Carmen Miguel Spínola}} \\[1cm]

\textbf{Universidad Complutense de Madrid} \\[0.5cm]

\textbf{Facultad de Informática} \\[1.5cm]

{\Large 12-01-2025} \\

\end{center}
\end{titlepage}

\clearpage
\tableofcontents
\clearpage
"""
    return portada


def generar_introduccion():
    template_introduccion = r"""
# Introducción

El presente informe tiene como objetivo mostrar los resultados obtenidos en el análisis de la red relativa a la página 'Roblox' como proyecto final de la asignatura Análisis de Redes Sociales de la Universidad Complutense de Madrid. 
El documento está principalmente dividido dos partes: el análisis del contenido y el análisis de la estructura de la red.

## Análisis del contenido

Se calculan gráficas y métricas clasificadas en:

- Datos primitivos:
    - Gráfica de usuarios con más amigos.
    - Gráfica de grupos con más miembros.
    - Juegos por idiomas disponibles.
    - Palabras más comunes en descripciones de juegos.
    - Emoticonos más comunes en nombres de juegos.

- Datos derivados:
    - Análisis de sentimientos en descripciones de juegos.
    - Palabras más comunes en descripciones negativas de juegos.
    - Palabras más comunes en descripciones positivas de juegos.

- Datos agregados:
    - Número total de juegos, grupos y usuarios recogidos en la muestra.
    - Media, máximo y mínimo de amigos, miembros de grupos y precios de servidor privado.

\clearpage
## Análisis de la estructura de la red

Se analiza la red formada por los usuarios, grupos y juegos de Roblox. Se calculan métricas sobre:

- Grado de los nodos.
- Coeficiente de clustering.
- Distancias.
- Medidas probabilísticas.

El objetivo del análisis es obtener una visión general de la red y de las relaciones entre los nodos que la componen.
\clearpage
"""

    return template_introduccion


def generar_resultados():
    introduccion = generar_intro() + generar_portada() + generar_introduccion()
    nombre_archivo = "informe_introduccion.md"
    carpeta_destino = "informesGenerados"
    os.makedirs(carpeta_destino, exist_ok=True)
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
    with open(ruta_completa, "w", encoding="utf-8") as archivo:
        archivo.write(introduccion)
