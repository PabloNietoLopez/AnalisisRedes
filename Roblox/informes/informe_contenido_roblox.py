from string import Template
import datetime
import os


def generar_introduccion():

    yaml_metadatos = """

# Análisis de contenido de Roblox
"""
    return yaml_metadatos


def informe_mas_amigos(diccionario):
    template_resultados = r"""
## Gráfica de usuarios con más amigos

![Gráfica de los usuarios con más amigos]({grafica_amigos})

- Conclusiones:

Esta gráfica muestra los 10 usuarios con más amigos en la plataforma Roblox.

Las relaciones de amistad entre usuarios sirven para que estos puedan interactuar y jugar juntos en la plataforma. Otro tipo de interacción que se puede dar entre usuarios es seguirse mutuamente, lo que permite estar al tanto de las actividades de otros usuarios. En la muestra, resultaba más común tener amigos que seguidores, lo que sugiere que los usuarios prefieren establecer relaciones más cercanas con otros usuarios y no se da tanta importancia al seguimiento (aunque los creadores más populares suelen acumular muchos seguidores, la mayoría de usuarios de la plataforma tienen amigos y no seguidores).

El usuario con más amigos supera los 250 y, como se ha podido comprobar, se trata de una cuenta no muy longeva. El número de amigos se explica con el hecho de pertenecer a un grupo con muchos miembros, lo que facilita la interacción con otros usuarios y la posibilidad de hacer amigos. En el resto de casos, observamos el mismo fenómeno: son usuarios que pertenecen a grupos con muchos miembros y, por tanto, tienen más posibilidades de hacer amigos. La única excepción es el usuario `taypoal` que, a pesar de pertenecer a un grupo con pocos miembros, tiene un número elevado de amigos.

En general, puede establecerse una relación directa tal que los usuarios con más amigos suelen pertenecer a grupos con muchos miembros. Por lo que se concluye que la posibilidad de pertenecer a grupos en Roblox cumple su función: permite a los usuarios relacionarse entre sí y establecen entornos de colaboración y amistad entre personas con intereses comunes. 

"""
    return template_resultados.format(
        grafica_amigos=diccionario.get("usuarios_mas_amigos"),
    )


def informe_mas_miembros(diccionario):
    template_resultados = r"""
\clearpage
## Gráfica de grupos con más miembros

![Gráfica de los grupos con más miembros]({grafica_miembros})

- Conclusiones:

Esta gráfica muestra los 5 grupos con más miembros en la plataforma Roblox donde los grupos son conjuntos de creadores que se unen para colaborar en un mismo juego. 

Es común que, cuando un juego se hace muy popular, el grupo aumente su tamaño para poder cubrir la demanda de los jugadores arreglando bugs y añadiendo nuevo contenido al juego. Este fenómeno se corrobora en esta muestra: los juegos que se han cogido son muy virales por lo que aparecen grupos con muchos miembros como se refleja en la gráfica.

Se concluye entonces que los grupos con más miembros suelen pertenecer a juegos muy populares y virales en la plataforma Roblox.

"""
    return template_resultados.format(
        grafica_miembros=diccionario.get("grupos_mas_miembros"),
    )


def informe_idiomas(diccionario):
    template_resultados = r"""
\clearpage

## Gráfica del número de juegos por idioma disponible.

![Gráfica de juegos por idioma]({grafica_idiomas})

- Conclusiones:

La gráfica muestra el número de juegos disponibles en la plataforma Roblox por idioma (por defecto hace referencia al idioma inglés que es el original de la plataforma).

Se observa como todos los juegos están disponibles en múltiples idiomas. En la muestra, al extraerse los datos desde la plataforma en español, se obtienen bastantes juegos que están en este idioma, aunque sorprende que no llegue al número de juegos que están en idiomas menos populares como el polaco. Este hecho puede deberse a que no haya muchos creadores hipanohablantes o a que, simplemente, Roblox no esté tan extendido en países de habla hispana como en otros países.

En general, se puede concluir que la plataforma Roblox es accesible para usuarios de todo el mundo, ya que los juegos están disponibles en múltiples idiomas, lo que facilita la interacción entre usuarios de diferentes países y culturas. Además, la plataforma se adapta a las preferencias de los usuarios, ya que pueden jugar en su idioma nativo, lo que mejora la experiencia de usuario. El inglés ya no ocupa ese lugar principal que si tiene en otras plataformas y, aunque se establece como el común entre todos los usuarios, existe una gran variedad.

"""
    return template_resultados.format(
        grafica_idiomas=diccionario.get("juegos_por_idioma"),
    )


def informe_palabrascomunes(diccionario):
    template_resultados = r"""
\clearpage
## Gráfica de las palabras más comunes en las descripciones de los juegos

![Gráfica de palabras más comunes]({grafica_palabras})

- Conclusiones:

Se analizan las descripciones de los juegos y, como resulta lógico, entre las palabras más comunes obtenemos `roblox`, `game` o `created`. Al tratarse de descripciones de juegos también se encuentra que el vocabulario empleado debe ser sencillo, directo y atrayente para los jugadores. Por ello, se repiten palabras como `unique`, `new` o `experiences`.

En general, se puede concluir que las descripciones de los juegos en Roblox siguen un patrón común en cuanto a vocabulario y estructura, lo que facilita la búsqueda de juegos por parte de los usuarios. Además, las palabras más comunes reflejan las características más importantes de los juegos, lo que permite a los usuarios hacerse una idea de lo que pueden esperar de cada juego antes de jugarlo. Quizás por esto último, al haber en la muestra juegos de categorías muy variadas, no se repitan demsiado palabras que reflejen un tipo de juego en concreto.

"""
    return template_resultados.format(
        grafica_palabras=diccionario.get("palabras_comunes")
    )


def informe_emoticonos(diccionario):
    template_resultados = r"""
\clearpage
## Gráfica de los emoticonos más comunes en los nombres de los juegos

![Gráfica de los emoticonos más comunes]({grafica_emoticonos})

- Conclusiones:

Este aspecto parece ser algo extraño de analizar en cualquier otra plataforma de juegos pero en Roblox, al ser una plataforma que permite a los usuarios crear sus propios juegos, se da la posibilidad de que los nombres de los juegos contengan emoticonos. Esto, unido a que Roblox está dirigido a un público más infantil, hace que los emoticonos resulten muy comúnes en los títulos de los juegos y se conviertan en un elemento más de atracción para los jugadores.

Por otro lado, los títulos de los juegos se cambian en cada actuaización y los juegos más populares varían continuamente. Esto afecta al hecho de que, al estar en época navideña, los emoticonos más comunes sean los relacionados con la Navidad y el Invierno. En su momento, destacaban los emoticonos relacionados con Halloween y, en general, los emoticonos más comunes son los que reflejan la actualidad y las festividades del momento.

En general, se puede concluir que los emoticonos en los nombres de los juegos son una forma de atraer a los jugadores y sirven de indicador de actualidad de los juegos en la plataforma Roblox. Además, los emoticonos son una forma de expresión que permite a los creadores de juegos transmitir emociones y sensaciones a los jugadores, lo que mejora la experiencia de usuario y hace que los juegos sean más atractivos y divertidos.

"""
    return template_resultados.format(
        grafica_emoticonos=diccionario.get("emoticonos_comunes")
    )


def informe_sentimientos(diccionario):
    template_resultados = r"""
\clearpage
## Análisis de sentimientos en las descripciones de los juegos

![Gráfica del sentimiento]({grafica_sentimiento})

- Conclusiones:

Como podía intuirse, el sentimiento que trasmiten las descripciones de los juegos es, en su mayoría positivo, ya que tratan de atraer al jugador para que juegue a ese juego. Aunque también se encuentran descripciones negativas, estas representan un porcentaje muy bajo en comparación pero es un hecho que será analizado más adelante.

En general, se puede concluir que las descripciones de los juegos en Roblox son positivas y optimistas, lo que refleja la intención de los creadores de juegos de atraer a los jugadores y hacer que se diviertan. Deben reflejar para lo que está concebido un juego: una forma de entretenimiento y diversión.

"""
    return template_resultados.format(
        grafica_sentimiento=diccionario.get("sentimiento")
    )


def informe_palabras_negativas(diccionario):
    template_resultados = r"""
\clearpage
## Palabras más comunes en descripciones negativas de juegos

![Gráfica de las palabras negativas]({grafica_negativas})

- Conclusiones:

Dejando de lado las palabras que aparecen por ser las más comunes y las que compartirían tanto descripciones positivas como negativas, se encuentra la palabra `horror` como negativa. Esto sugiere que el clasificaor de texto por sentimiento está estableciendo las descripciones de juegos de miedo o de terror como negativas.

Como las descripciones negativas suponían una muestra muy pequeña, se puede concluir que no hay descripciones negativas como tal sino que se trata de descripciones de juegos de terror o miedo que, por su temática, son clasificadas como negativas. Entonces, tenemos que las descripciones serían positivas tal como se presupone que la primera impresión de un juego debería ser.
"""
    return template_resultados.format(
        grafica_negativas=diccionario.get("palabras_negativas")
    )


def informe_palabras_positivas(diccionario):
    template_resultados = r"""
\clearpage
## Palabras más comunes en descripciones positivas de juegos

![Gráfica de las palabras positivas]({grafica_positivas})

- Conclusiones:

Vuelven a aparecer las palabras más comunes en las descripciones en general ya que serán las buscadas por los usuarios cuando estén en la plataforma. 

Tras el análisis de los textos, se concluye que las descripciones de los juegos en Roblox, que don la pieza de texto más pública y accesible, son positivas como se esperaba de una plataforma de juegos en su mayoría infantiles.
"""
    return template_resultados.format(
        grafica_positivas=diccionario.get("palabras_positivas")
    )


def informe_datos_agregados(diccionario):
    template_resultados = r"""
\clearpage
## Métricas sobre la muestra

- El número de grupos es {num_grupos}.

- El número de usuarios es {num_usuarios}. 

Esto se debe a que resultaba inviable analizar todos los miembros de los grupos ya que, como se ha visto, los grupos superaban el millón de miembros. Por tanto, se ha cogido un conjunto de miembros que resultase manejable para el análisis.

- El número de juegos es {num_juegos}. 

El número de juegos hace referencia al número de ellos de los que se ha obtenido información detallada y que han sido usados para el análsis de contenido. Existe en el dataset un apartado de juegos recomendados por usuario que se utilizará posteriormente para el análisis de la estructura.

- El número máximo de amigos es {amigos_max}.

- El número mínimo de amigos es {amigos_min}.

- La media de amigos es {amigos_media:.2f}. 

Como puede observarse, el número de amigos es variable en un rango desde 0 a 283 pero la media se mantiene casi 59 amigos por usuario. 

Si se entiende el concepto de amigo como otro usuario con el que jugar habitualmente, es un número bastante elevado aunque, como se ha visto, los usuarios de la muestra pertencen a grupos muy grandes. Estos no se cree que representen el perfil de jugador casual que es un sector importante también en la plataforma.

- El número máximo de miembros en un grupo es {miembros_max}.

- El número mínimo de miembros en un grupo es {miembros_min}.

- La media de miembros en un grupo es {miembros_media:.2f}. 

Tal y como se comentaba antes, los grupos recogidos en la muestra son muy numerosos y, aunque el número de miembros varía en un rango muy grande, la media se mantiene en un número muy elevado.

- El precio máximo de un servidor privado es {precio_max}.

- El precio mínimo de un servidor privado es {precio_min}.

- El precio medio de un servidor privado es {precio_media:.2f}. 

Un servidor privado es un espacio en el que los usuarios pueden jugar sin ser molestados por otros jugadores. De esta manera, el usuario puede disfrutar de una experiencia de juego más tranquila y personalizada, eligiendo quien puede unirse a su sesión. 

El precio de un servidor privado lo establece el creador del juego por lo que es muy variable. Este viene dado en Robux, la moneda de la plataforma, y como referencia se tiene que 100 Robux son 1 euro de manera aproximada. Por tanto, el precio medio de un servidor privado no llega si quiera al euro, lo que sugiere que es bastante barato si consideramos que los juegos de la muestra son muy populares.

"""
    return template_resultados.format(
        num_grupos=diccionario.get("numero_de_grupos"),
        num_usuarios=diccionario.get("numero_de_usuarios"),
        num_juegos=diccionario.get("numero_de_juegos"),
        amigos_max=diccionario.get("max_amigos"),
        amigos_min=diccionario.get("min_amigos"),
        amigos_media=diccionario.get("media_amigos"),
        miembros_max=diccionario.get("max_miembros_grupo"),
        miembros_min=diccionario.get("min_miembros_grupo"),
        miembros_media=diccionario.get("media_miembros_grupo"),
        precio_max=diccionario.get("max_precio_servidor"),
        precio_min=diccionario.get("min_precio_servidor"),
        precio_media=diccionario.get("media_precio_servidor"),
    )


def conclusiones():
    # Crear el template con las conclusiones finales del análisis de contenido
    template_probabilidad = r"""
\clearpage
## Conclusiones

- Datos primitivos:

Dejan entrever la presencia de juegos muy populares en la muestra recogida. Esto se debe a que los datos se extraen desde la página principal de Roblox, donde están en portada los juegos más virales y jugados del momento. Esto provoca que los grupos sean muy numerosos y que los miembros de estos cuenten con muchos amigos.
Una conclusión interesante de esto último es la preferencia de vínculos de amistad en retrimento de las relaciones de seguimiento: se observa que los usuarios apenas acumulan seguidores mientras que su número de amigos es muy elevado. Probablemente se deba a que la relación de amistad se da entre los dos usuarios y permite a estos juagr juntos mientras que el seguimiento no te aporta estas características. Entre usuarios se priorizan entonces las relaciones más cercanas y la posibilidad de juego online frente a la popularidad.  

Por otro lado, un síntoma de la expansión global de Roblox es la disponibilidad de varios idiomas en los juegos. Aunque incluir varios idiomas como disponibles en un juego puede ser simplemente una estrategia para atraer jugadores, es innegable el alcance global de Roblox.

Por último, en el poco análisis de texto que se ha podido realizar en esta plataforma, se tiene que en las descripciones de los juegos se repiten gran cantidad de palabras que serán claves para que un juego aparezca fácilmente al realizar una búsqueda sencilla. También destaca la presencia de emoticonos en la plataforma como símbolo de actualidad de los juegos y juventud de los jugadores.

- Datos derivados:

El análisis de sentimientos en Roblox lleva a pensar en el fuerte sentimiento positivo de la plataformas debido a el público al que se dirige. Las descripciones de los juegos en las que se realiza el análisis muestran la necesidad de crear expectación en el jugador y atraerlo.
Mucho más interesante hubiese resultado tener acceso a los chats que se dan en lo juegos. Seguramente esto hubiera supuesto un análisis más extenso y variado donde realmente se viesen los sentimientos que despiertan los juegos en los usuarios y como estos responden ante ellos.

- Datos agregados:

Representan una muestra más de los datos conseguidos y evidencian la presencia de juegos y grupos muy importantes actualmente en la plataforma (número muy alto de miembros en los grupos, usuarios con muchos amigos, etc.).


Mencionar que en el proceso de análsis se han esquivado ciertas dificultades y enfrentado problemas de privacidad que hacen que el análisis de contenido no pueda ser tan profundo como se pretendía. Últimamente Roblox se ha visto envuelto en varias polémicas, por lo que la plataforma ha optado por endurecer la privacidad haciendo un trabajo como este más costoso.
Entre las conclusiones que pueden sacarse se obtiene que Roblox es una plataforma principalmente enfocada un plúbico muy joven y que, a priori, no parece ser un entorno inseguro para los niños. Poner en valor también el trabajo por atraer a jugadores y la creatividad por parte de los creadores de juegos de la plataforma, que actualizan estos frecuentemente para mantener el interés y aplican ciertos métodos para captar la atención de los usuarios. Conseguir que un juego sea muy popular no es tarea fácil si se considera que todos los juegos tienen una apariencia muy similar al estar creados de forma sencilla con las herramientas que pone Roblox a disposición de los creadores.
\clearpage
"""
    return template_probabilidad.format()


def generar_resultados(diccionario):
    introduccion = generar_introduccion()

    informes = []
    informes.append(introduccion)

    # Datos primitivos
    informes.append(informe_mas_amigos(diccionario))
    informes.append(informe_mas_miembros(diccionario))
    informes.append(informe_idiomas(diccionario))
    informes.append(informe_palabrascomunes(diccionario))
    informes.append(informe_emoticonos(diccionario))

    # Datos derivados
    informes.append(informe_sentimientos(diccionario))
    informes.append(informe_palabras_negativas(diccionario))
    informes.append(informe_palabras_positivas(diccionario))

    # Datos agregados
    informes.append(informe_datos_agregados(diccionario))

    informes.append(conclusiones())

    informe_completo = "\n".join(informes)

    ahora = datetime.datetime.now()
    fecha_hora = ahora.strftime("%d-%m-%Y_%H-%M")
    nombre_archivo = f"informe_roblox_contenido_{fecha_hora}.md"
    carpeta_destino = "InformesGenerados"
    os.makedirs(carpeta_destino, exist_ok=True)
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
    with open(ruta_completa, "w", encoding="utf-8") as archivo:
        archivo.write(informe_completo)
