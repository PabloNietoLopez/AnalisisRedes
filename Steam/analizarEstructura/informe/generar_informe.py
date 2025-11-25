import os
from datetime import datetime
from estructura import analizador


def generar_intro():
    yaml_metadatos = """---
documentclass: scrreport
papersize: a4
lang: es
babel-lang: spanish
---
"""
    return yaml_metadatos


def generar_portada():
    portada = r"""
\begin{titlepage}
\begin{center}

\includegraphics[width=0.3\textwidth]{ucm.png} \\[1cm] 

{\Huge \textbf{Análisis de Steam como red social}} \\[0.5cm]

{\Large Análisis de Redes Sociales} \\[1.5cm]

{\Large \textbf{Manuel Pardo Cerdeño}} \\[0.5cm]

{\Large \textbf{Pablo Nieto López}} \\[1cm]

\textbf{Universidad Complutense de Madrid} \\[0.5cm]

\textbf{Facultad de Informática} \\[1.5cm]

{\Large 12-01-2025} \\

\end{center}
\end{titlepage}

\clearpage
"""
    return portada


def introduccion():
    return """
# Informe de la Red Steam
"""


def nodos_aristas():
    return f"""
## 1. Número de Nodos y Enlaces

**Qué son los nodos y enlaces?**  
Los nodos representan las entidades o elementos de la red, mientras que los enlaces son las conexiones entre ellos.

- **Número total de nodos**: {analizador.diccionario_resul['num_nodos']}  
- **Número total de enlaces**: {analizador.diccionario_resul['num_aristas']}  

El análisis de la red muestra un total de 796 nodos y 592 enlaces, lo que sugiere una estructura densa y bien conectada. Esta proporción implica una red suficientemente compleja para soportar interacciones dinámicas y distribución eficiente de información entre los nodos. Sin embargo, la relación entre nodos y enlaces también indica que existen limitaciones en la conectividad, lo que podría reflejar cierta fragmentación en la red. Este comportamiento es típico de redes con comunidades internas y puntos de conexión centrales (hubs).
"""


def grados_clustering():
    return f"""
\clearpage
## 2. Gráfica de la distribución de grados y Coeficientes de Clustering

**Distribución de grados:** Expresa la frecuencia con la que aparecen diferentes grados en la red.  

![Distribución de grados](../{analizador.diccionario_resul['distribucion_grados']})

**Coeficiente de Clustering:** Evalúa la tendencia de los nodos a agruparse en comunidades.  

![Coeficiente de Clustering](../{analizador.diccionario_resul['distribucion_clustering']})

La distribución de grados revela una estructura jerárquica, con pocos nodos altamente conectados (hubs) y muchos nodos con conexiones mínimas. Esto es indicativo de una topología en forma de "estrella", donde los hubs actúan como puntos de conexión fundamentales.
El coeficiente de clustering demuestra que estos hubs facilitan la creación de comunidades más pequeñas dentro de la red, promoviendo la cohesión local. Sin embargo, esto también puede resultar en una menor conexión global entre comunidades.
La razon por la que nos sale 0 en el coeficiente de clustering es debido a que este coeficiente mide la posibilidad de que se formen triangulos, es decir, que los vecinos de una comunidad esten comunicados entre si y dado que la conexion entre usuarios es privada las conexiones entre vecinos suele ser nula. 
"""


def grados_clustering_hubs():
    return f"""
\clearpage
## 3. Distribución de grados y clustering con hubs

**Gráficas considerando hubs:**  

![Distribución de grados con hubs](../{analizador.diccionario_resul['distribucion_grados_hubs']})  
![Coeficiente de clustering con hubs](../{analizador.diccionario_resul['distribucion_clustering_hubs']})

La presencia de hubs es crucial para el funcionamiento de la red, ya que no solo centralizan conexiones, sino que también refuerzan la estructura comunitaria. Estos nodos centrales aseguran que la red pueda resistir la desconexión de nodos periféricos y facilitan la transmisión eficiente de información. Sin embargo, también hacen que la red sea vulnerable a la pérdida o inactividad de estos hubs.
"""


def conjunto_grados_clustering():
    return f"""
\clearpage
## 4. Distribución conjunta de Grados y Coeficientes de Clustering

![Distribución conjunta](../{analizador.diccionario_resul['cnj_grados_clustering']})

La combinación de grados y coeficientes de clustering refuerza la idea de que esta red presenta características de "estrella". Aunque se generan muchas minicomunidades, la desconexión entre ellas indica que la red no es completamente robusta a nivel global. Esto sugiere que, aunque la red facilita interacciones dentro de comunidades locales, la comunicación entre diferentes grupos depende en gran medida de los hubs.
"""


def visualizacion():
    return f"""
\clearpage
## 5. Visualización del Grafo

![Visualización del grafo](../{analizador.diccionario_resul['visualizacion_grafo']})

La visualización del grafo confirma que la red combina propiedades de un "Small World" con una estructura en "Estrella". Los hubs no solo actúan como conectores principales, sino que también promueven una alta interconexión local. Sin embargo, las comunidades periféricas parecen estar menos integradas, lo que puede limitar el flujo de información en ciertos casos.
Debo destacar que en este grafo si se hubiese recogido un nodo más habria una conexión más representativa de Estrella y Small World, este nodo seria la interfaz del propio Steam, la cual conectaria a los juegos entre ellos y a su vez los juegos conectarias a los usuarios, comunidades y eventos.
"""


def media_distancia():
    return f"""
\clearpage
## 6. Distancia Media

**Distancia Media**: {analizador.diccionario_resul['distancia_media']}  

Una distancia media de 1.29 indica que la red está altamente interconectada, permitiendo la rápida difusión de mensajes entre los nodos. Este valor es característico de redes optimizadas para la eficiencia, donde la mayoría de las conexiones se pueden establecer en pocos pasos.
"""


def calculo_diametro():
    return f"""
## 7. Diámetro

**Diámetro**: {analizador.diccionario_resul['diametro']}  

El diámetro de la red, con un valor de 3, refuerza la idea de un "Small World". Esto significa que incluso los nodos más alejados están separados por solo tres pasos, lo que garantiza una conectividad global efectiva, independientemente de la ubicación dentro de la red.
Debemos tener en cuenta eso si que lo que tenemos aqui es una red "Estrella" con muchas comunidades pequeñas que acabarian conectadas a un hub centrico.
"""


def distribucion_distancias():
    return f"""
\clearpage
## 8. Distribución de Distancias desde los Hubs

![Distribución de distancias](../{analizador.diccionario_resul['distribucion_distancias']})

La mayoría de los nodos están a pocos pasos de los hubs principales, lo que resalta su importancia estratégica. Esto asegura que la red sea altamente accesible y que los hubs actúen como puntos de difusión clave para las comunidades conectadas.
"""


def probabilidad():
    return f"""
## 9. Esperanza, Varianza y Probabilidad de Enlace

- **Esperanza**: {analizador.diccionario_resul['esperanza']}  
- **Varianza**: {analizador.diccionario_resul['varianza']}  
- **Probabilidad de Enlace**: {analizador.diccionario_resul['probabilidad']}  

Esperanza:  Indica que, en promedio, los nodos tienen pocas conexiones, aunque los hubs compensan esta baja conectividad local.
Varianza: Refleja una distribución de enlaces desigual, lo que es consistente con la existencia de hubs.
Probabilidad de enlace: Muestra que, aunque la red es grande, la posibilidad de que dos nodos aleatorios estén conectados directamente es baja, lo que refuerza la idea de comunidades interconectadas por hubs.

Estos valores refuerzan que la red tiene características de "Estrella" y la formacion de muchas pequeñas comunidades.
"""


# Función para generar el informe completo
def generar_informe_completo():

    print("Análisis completo. Generando informe...")

    # Crear el contenido del informe
    secciones = [
        generar_portada(),
        generar_intro(),
        introduccion(),
        nodos_aristas(),
        grados_clustering(),
        grados_clustering_hubs(),
        conjunto_grados_clustering(),
        visualizacion(),
        media_distancia(),
        calculo_diametro(),
        distribucion_distancias(),
        probabilidad(),
    ]

    contenido_informe = "\n".join(secciones)

    # Crear el nombre del archivo con la fecha y hora actuales
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"analizarEstructura/informe_red_{fecha_hora_actual}.md"

    # Guardar el informe en un archivo Markdown
    with open(nombre_archivo, "w", encoding="utf-8") as archivo_md:
        archivo_md.write(contenido_informe)

    print(f"Informe generado exitosamente: {nombre_archivo}")


# Punto de entrada principal
if __name__ == "__main__":
    generar_informe_completo()
