import os
from datetime import datetime


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


def Steam():
    return """

# INTRODUCCION
Este es el informe del trabajo realizado sobre el análisis de datos de Steam, el cual se centra en una variedad de campos informativos obtenidos de diferentes fuentes de datos relacionadas con los juegos, desarrolladores, usuarios, comunidades y comentarios. Estos datos nos aportan la siguiente información clave a tener en cuenta:

- **Nombre del Juego**: Identifica el título del juego analizado.
- **Requisitos Mínimos y Recomendados**: Incluyen información sobre el espacio de almacenamiento necesario y otras especificaciones técnicas.
- **Comentarios**: Contienen descripciones y valoraciones hechas por los usuarios.
- **Valoraciones**: Indican si los usuarios recomiendan o no el juego.
- **Comunidades**: Muestran datos sobre las comunidades activas relacionadas con cada juego.
- **Sentimientos**: Representan las emociones expresadas en los comentarios mediante un análisis de sentimiento.

Teniendo en cuenta estos apartados, el como hemos recogido la información y el como la hemos procesado el informe se dividira en 4 partes distintas, cada una representando los graficos obtenidos con los distintos datos:

- Gráficas e Investigacion de los **Datos Primitivos**.
- Gráficas e Investigacion de los **Datos Derivados**.
- Gráficas e Investigacion de los **Datos Agregados**.

En cada uno de estos apartados se aportan gráficas para mostrar los datos recogidos y se explicara a continuación la interpretacion que le damos a dichos datos.
"""


def DatosPrimitivos():
    return f"""
# Datos Primitivos

## DATOS

El presente informe analiza datos de Steam, en particular, precios, géneros de los juegos, reseñas y seguidores de desarrolladores. Las visualizaciones y resultados se basan en los archivos proporcionados y las gráficas generadas, detalladas en la sección de [RESULTADOS](#resultados).

## RESULTADOS

El código para generar las visualizaciones está diseñado para analizar los datos de precios, géneros de juegos, reseñas y seguidores 
de los desarrolladores, permitiendo observar patrones clave. Las funciones incluyen:

graficar_precios_juegos(): Analiza la cantidad de juegos por precio.

graficar_generos_juegos(): Visualiza la cantidad de juegos por género.

graficar_reseñas_juegos(): Muestra la distribución de las reseñas en un gráfico de pastel.

graficar_seguidores_desarrolladores(): Representa el número de seguidores por desarrollador.

grafico_cantidad_por_rango_precio(): Analiza la cantidad de juegos en distintos rangos de precios.

\clearpage
### Precios de los Juegos

![Precios de los Juegos](../analizarContenido/imagenes/precios_juegos.png)

En este gráfico se muestra la cantidad de juegos disponibles por cada precio. Observamos que la mayoría de los juegos están en el 
rango de precios bajos, siendo los juegos gratuitos una categoría particularmente relevante, lo cual refuerza la popularidad del 
modelo "Free to Play" en la plataforma. También es notable que los precios están distribuidos en tramos específicos, lo que podría 
estar relacionado con estrategias comerciales estandarizadas dentro de Steam.

\clearpage
### Géneros de los Juegos

![Géneros de los Juegos](../analizarContenido/imagenes/juegos_genero.png)

Este gráfico de barras presenta la cantidad de juegos agrupados por género. Destaca la alta popularidad de géneros como "Acción" y 
"Aventura", que reflejan una tendencia general entre los usuarios de Steam hacia experiencias inmersivas y desafiantes. Géneros como 
"Estrategia" y "Indie" también muestran un considerable número de títulos, evidenciando la diversidad en los intereses de los usuarios 
y la amplitud del catálogo disponible.

\clearpage
### Reseñas de los Juegos

![Reseñas de los Juegos](../analizarContenido/imagenes/reseñas_juegos.png)

En este gráfico de pastel, se representa la distribución de reseñas de los juegos en Steam:

53.7% Muy Positivas: La mayoría de los juegos reciben una calificación favorable, lo que refleja una satisfacción general de los 
usuarios.

24.1% Extremadamente Positivas: Una proporción considerable de juegos es altamente valorada, destacándose como éxitos rotundos.

11.1% Mayormente Positivas: Un porcentaje significativo también recibe reseñas mayoritariamente buenas.

7.4% Variadas: Una minoría tiene opiniones mixtas, reflejando experiencias inconsistentes.

3.7% No Disponible: Algunos juegos no cuentan con suficientes datos de reseñas para ser clasificados.

Estas cifras refuerzan la idea de que Steam promueve productos de alta calidad con una gran aceptación entre sus usuarios.

### Seguidores de los Desarrolladores

![Seguidores de los Desarrolladores](../analizarContenido/imagenes/seguidores_desarrolladores.png)

El gráfico muestra el número de seguidores de los principales desarrolladores de Steam. Entre los desarrolladores destacados, nombres  
como Valve y CD Projekt Red lideran con una gran cantidad de seguidores, demostrando la fuerte lealtad y reconocimiento de marca que 
tienen entre los usuarios. Esto subraya la importancia del prestigio y la calidad constante en la industria de los videojuegos.

"""


def DatosAgregados():
    return f"""
# Datos Agregados

## DATOS

En este informe se analizarán los datos agrupados de Steam, la popular plataforma de distribución de videojuegos. Los datos incluyen información sobre las fechas de lanzamiento de juegos, los desarrolladores responsables de su creación y el promedio de calificación por género de juego. A partir de esta información, se buscará identificar tendencias significativas y patrones relevantes en la industria de los videojuegos. Todo esto se detallará en la sección de [RESULTADOS](#resultados)

## RESULTADOS

El análisis realizado tiene como objetivo examinar los datos agrupados relacionados con las fechas de lanzamiento de juegos, el número de juegos creados por desarrolladores y las calificaciones promedio por género en Steam. Las visualizaciones generadas permiten identificar patrones clave en el catálogo de la plataforma y las preferencias de los usuarios.

Juegos por Fecha de Lanzamiento(): Gráfica que relaciona los lanzamientos de los juegos con las fechas

Juegos por Desarrollador(): Gráfica que muestra el número de juegos creados por desarrolladores

Promedio de Calificaciones por Género(): Gráfica que muestra que generos tienen mejores reseñas

\clearpage
### Juegos por Fecha de Lanzamiento

![Juegos por Fecha de Lanzamiento](../analizarContenido/imagenes/juegos_fechas.png)

Este gráfico muestra la distribución de juegos en función de su fecha de lanzamiento. Se observa un aumento significativo en el número de juegos publicados a partir de 2015, lo que refleja un crecimiento en la producción de contenido en la plataforma. Este incremento puede estar relacionado con la creciente popularidad de Steam y la reducción de barreras para desarrolladores independientes. Las caídas en ciertos periodos pueden deberse a factores externos, como crisis económicas o cambios en las políticas de la plataforma.

\clearpage
### Juegos Creados por Desarrolladores

![Juegos Creados por Desarrolladores](../analizarContenido/imagenes/juegos_desarrolladores.png)

En este gráfico se analiza el número de juegos creados por los desarrolladores. La mayoría de los desarrolladores tienen un número limitado de títulos publicados, lo que indica una predominancia de estudios pequeños o independientes. Sin embargo, algunos desarrolladores destacados cuentan con catálogos extensos, lo que refleja la capacidad de los grandes estudios para producir contenido de manera continua y diversificada. Esta disparidad pone de manifiesto la coexistencia de desarrolladores independientes y grandes empresas en la plataforma.

\clearpage
### Promedio de Calificaciones por Género

![Promedio de Calificaciones por Género](../analizarContenido/imagenes/promedio_por_genero.png)

Esta visualización presenta las calificaciones promedio de los juegos, agrupadas por género. Los géneros "RPG" y "Aventura" obtienen las mejores valoraciones promedio, destacándose por su capacidad para ofrecer experiencias narrativas y jugabilidad de alta calidad. En contraste, géneros con menor promedio podrían estar asociados a una mayor variabilidad en la calidad de los títulos disponibles. Esto subraya cómo las expectativas de los usuarios varían según el género y cómo ciertos géneros tienden a satisfacer mejor esas expectativas.
"""


def DatosDerivados():
    return f"""
# Datos Derivados

## DATOS

El objetivo de este informe es analizar datos derivados relacionados con juegos disponibles en la plataforma Steam. Se han empleado distintas visualizaciones y funciones para examinar aspectos como los requisitos de almacenamiento, el promedio de valoraciones por juego, la relación entre valoración y comunidad, y el sentimiento general en los comentarios. Estas análisis permiten identificar patrones relevantes sobre las características de los juegos y las preferencias de los usuarios en esta plataforma.Todo esto sera detallado en la sección de [RESULTADOS](#resultados)

## RESULTADOS
El código para generar las visualizaciones está diseñado para analizar los datos de precios, géneros de juegos, reseñas y seguidores 
de los desarrolladores, permitiendo observar patrones clave. Las funciones incluyen:

graficar_almacenamiento(): Gráfica que muestra el almacenamiento requerido por los juegos.

grafico_promedio_valoraciones(): Gráfica que muestra el promedio de valoraciones por juego.

grafico_valoracion_con_comunidad(): Gráfica que muestra la relación entre como se valora el juego y el hecho de que tenga comunidad o no.

grafico_distribucion_sentimientos_barras(): Gráfica que muestra la distribución de sentimientos en los comentarios por juego.

grafica_sentimiento_medio_total(): Gráfica que muestra el sentimiento medio total de los comentarios de todo los juegos en conjunto.

\clearpage
### Requisitos de Almacenamiento de Juegos

![Requisitos de Almacenamiento de Juegos](../analizarContenido/imagenes/almacenamiento_juegos.png)

Este análisis examina el espacio de almacenamiento requerido por los juegos en Steam. La visualización generada muestra una 
distribución heterogénea, con algunos picos significativos en rangos específicos de almacenamiento. Se observa que la mayoría de los 
juegos requieren entre 20 y 50 GB, mientras que juegos con requisitos superiores a 100 GB son menos comunes pero todavía 
representativos de ciertos títulos modernos que ofrecen gráficos y contenido de alta calidad.

La información derivada de este gráfico puede ser útil tanto para jugadores, al planificar su almacenamiento disponible, como para 
desarrolladores, al optimizar sus requisitos técnicos.

\clearpage
### Promedio de Valoraciones por Juego

![Promedio de Valoraciones por Juego](../analizarContenido/imagenes/promedio_valoraciones.png)

El gráfico de valoraciones promedio por juego permite analizar el nivel de satisfacción de los usuarios. Las valoraciones oscilan 
generalmente entre 0.6 y 1, lo que refleja una tendencia positiva generalizada en la plataforma. Sin embargo, ciertos títulos destacan 
con una valoración promedio cercana al 1, lo que indica una recepción excepcional.

La distribución también pone en evidencia las diferencias en la percepción de calidad entre juegos individuales, subrayando cómo los 
usuarios responden de manera diversa a cada propuesta. Esto es particularmente valioso para identificar las mejores prácticas en el 
diseño de juegos.

\clearpage
### Relación entre Valoración y Comunidad

![Relación entre Valoración y Comunidad](../analizarContenido/imagenes/valoraciones_comunidad.png)

El análisis muestra que los juegos con una comunidad activa tienden a recibir una calificación promedio más alta (1.0), en comparación 
con los juegos sin comunidad, que obtienen una calificación promedio ligeramente menor (aproximadamente 0.9). Esto indica que la 
existencia de una comunidad podría estar relacionada con mejores valoraciones, posiblemente debido a un efecto de respaldo social o 
apoyo entre los miembros.
Cabe destacar que a la comunidad que nosotros nos referimos es a la comunidad de workshop, es decir, el hecho de que el juego permita a los usuarios crear modificaciones del juego y subirlas a la comunidad.
Debido a que la muestra de juegos con workshop es bastante pequeña en comparación a aquellos sin workshop pero que aun asi esa pequeña cantidad de juegos supera la valoración de los que son muchos podemos afirmar que el hecho de dejar a la comunidad crear contenido del juego mejora mucho la valoración.
Sin embargo, es importante considerar otros factores, como la calidad intrínseca del juego, que podrían influir en las calificaciones de manera independiente.

\clearpage
### Sentimientos en los Comentarios

![Sentimientos en los Comentarios](../analizarContenido/imagenes/distribucion_sentimientos.png)

El análisis de los sentimientos asociados a los comentarios de los juegos revela una distribución diversa. Se observan tres categorías 
principales: comentarios positivos (en verde), neutros (en gris) y negativos (en rojo). Aunque la mayoría de los juegos muestran un 
equilibrio entre sentimientos positivos y neutros, algunos títulos tienen una proporción destacada de comentarios negativos. Esto 
sugiere una respuesta polarizada entre los jugadores hacia ciertos juegos. Además, los títulos con mayor proporción de comentarios 
positivos podrían ser buenos ejemplos de diseño y experiencia de usuario.

En términos generales, el sentimiento promedio total de los comentarios (representado en una barra roja con un valor de -0.10) sugiere 
una leve inclinación hacia una percepción negativa. Esto indica que, aunque existen sentimientos positivos hacia muchos títulos, hay 
un espacio considerable para mejorar la experiencia general del usuario.

\clearpage
### Sentimiento Medio Total de los Comentarios

![Sentimiento Medio Total de los Comentarios](../analizarContenido/imagenes/sentimiento_medio_total.png)

La gráfica muestra el promedio total del sentimiento de los comentarios de los usuarios, representado como un valor ligeramente 
negativo (-0.10). Este resultado indica que, en general, los comentarios tienden a ser más críticos que positivos. Aunque el valor no 
es extremo, sugiere que los usuarios expresan más descontento que entusiasmo en sus evaluaciones. Esto podría reflejar expectativas no 
cumplidas, problemas técnicos, o áreas de mejora comunes en los juegos analizados. Es importante para los desarrolladores considerar 
estos sentimientos negativos como una oportunidad para abordar las inquietudes de los jugadores y mejorar la percepción global de sus 
títulos.
También tenemos que tener en cuenta que a pesar de que el sentimiento expresado en los comentarios la gran mayoria de los usuarios si que
recomiendan jugar al juego, lo cual expresa que de media siempre hay alguna que otra queja pero en general los usuarios estan satisfechos
con las experiencias que aportan los títulos.

"""


def Conclusion():
    return f"""

# CONCLUSIÓN

A partir de los datos analizados, es evidente que Steam cuenta con una amplia variedad de juegos, tanto en términos de precios como de 
géneros. Además, los datos de reseñas destacan una aceptación generalizada de los productos, y la distribución de seguidores por 
desarrollador resalta la importancia de nombres clave dentro de la plataforma. Esto permite concluir que Steam ha logrado un 
equilibrio entre diversidad de oferta y calidad percibida, consolidándose como líder en la industria de los videojuegos.
"""


# Función para generar el informe completo
def generar_informe_completo():

    # Crear el contenido del informe
    secciones = [
        generar_portada(),
        generar_intro(),
        Steam(),
        DatosPrimitivos(),
        DatosAgregados(),
        DatosDerivados(),
        Conclusion(),
    ]

    contenido_informe = "\n".join(secciones)

    # Crear el nombre del archivo con la fecha y hora actuales
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"analizarContenido/informe_red_{fecha_hora_actual}.md"

    # Guardar el informe en un archivo Markdown
    with open(nombre_archivo, "w", encoding="utf-8") as archivo_md:
        archivo_md.write(contenido_informe)

    print(f"Informe generado exitosamente: {nombre_archivo}")


# Punto de entrada principal
if __name__ == "__main__":
    generar_informe_completo()
