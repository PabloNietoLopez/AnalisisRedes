

# Análisis de la estructura de red de Roblox

En la representación de resultados se han usado muestras de unos 100 nodos para que fuese posible la generación de las gráficas en un tiempo de cómputo razonable. Esto puede afectar a la precisión de los resultados, pero se considera suficiente para obtener una idea general de la estructura de la red.


## Número de nodos y aristas

- Planteamiento del grafo:

Los nodos de la red de Roblox representan a los miembros de un grupo, a los propios grupos y a los juegos. Estos últimos son tanto los juegos scrapeados creados por los grupos (aquellos de los que se obtenía toda la infromación), como los recomendados por los miembros de los grupos.

Los enlaces son las relaciones que se dan entre los nodos: los miembros de un grupo están conectados entre sí, los miembros de un grupo están conectados con los juegos que recomiendan y los grupos están conectados con los juegos que crean.

Así, el grafo de Roblox es un grafo no dirigido con un total de 3 tipos de nodos y 3 tipos de enlaces. Se obtiene un grafo con una estructura de red social, del que se esperan nodos altamente conectados entre sí y nodos que actúan como hubs.

- Resultados y conclusiones:

El número total de nodos en la red es: 3183

El número total de enlaces en la red es: 11926

Estos resultados permiten tener una idea general de la cantidad de información que se maneja en la red. Además, se muestra una gran cantidad de relaciones en relación al número de nodos, lo que sugiere una red densa y altamente conectada: 3.746779767514923 enlaces por nodo en promedio.



\clearpage
## Gráfica de la distribución de los grados y coeficientes de Clustering

- Concepto de grado:

El grado de un nodo en una red es el número de conexiones que tiene con otros nodos, es decir, el número de enlaces que salen o entran en un nodo. 

En esta red social, el grado de un nodo puede representar la cantidad de amigos que tiene una persona, el número de usuarios que recomiendan cierto juego o el número de creadores que participan en la creación de otro.

Con la distribución se pretende reflejar la cantidad de nodos que tienen un determinado grado, lo que permite identificar nodos con un alto número de conexiones (hubs) y nodos con un bajo número de conexiones.

![Gráfica de la distribucion de grados](C:\Users\carme\Desktop\GitHubSOC\SOC\AvancesProyectoFinal\Roblox\analizarEstructura\Imagenes\distribucion_grados_Roblox.png)
\clearpage

- Concepto de coeficiente de Clustering:

Se trata de una medida que se utiliza para evaluar la tendencia de los nodos a agruparse en comunidades: un coeficiente alto significa que es altamente probable que se generen densas conexiones.

En esta red de Roblox, el coeficiente de Clustering puede representar la probabilidad de que los amigos de una persona también sean amigos entre sí, la probabilidad de que los usuarios que recomiendan un juego también recomienden otros juegos o la probabilidad de que los creadores de un grupo también participen en la creación de otros juegos.

![Gráfica de la distribucion de clustering](C:\Users\carme\Desktop\GitHubSOC\SOC\AvancesProyectoFinal\Roblox\analizarEstructura\Imagenes\distribucion_clustering_Roblox.png)

- Conclusiones:

Se obtiene una distribución de grados muy variada, lo que sugiere la presencia de nodos con un alto número de conexiones (hubs) y nodos con un bajo número de conexiones. 

Por otro lado, se obtiene un coeficiente de clustering también variado, lo que indica que la red es poco densa en algunos puntos. 

Estas observaciones sugieren que la red es más bien dispersa en muchos nodos en comparación con otros, aunque también se observan nodos con un alto coeficiente de clustering, lo que indica la presencia de comunidades o grupos de nodos altamente conectados entre sí.



\clearpage
## Gráfica de la distribución de los grados y coeficientes de clustering con hubs

Se entiende por hub a aquellos nodos que tienen un grado muy alto en comparación con el resto de nodos de la red. Se puede introducir un umbral para considerar los hubs.

![Gráfica de la distribucion de grados](C:\Users\carme\Desktop\GitHubSOC\SOC\AvancesProyectoFinal\Roblox\analizarEstructura\Imagenes\distribucion_grados_hubs_Roblox.png)
![Gráfica de la distribucion de coeficientes de Clustering](C:\Users\carme\Desktop\GitHubSOC\SOC\AvancesProyectoFinal\Roblox\analizarEstructura\Imagenes\distribucion_clustering_hubs_Roblox.png)

- Conclusiones:

Se ha considerado hub a aquellos nodos con un grado mayor a 10, lo que permite identificar los nodos más importantes de la red. 

Se obtiene que la mayoría de nodos tienen un grado superior a 10, lo que sugiere la presencia de nodos muy conectados.

En cuanto al coeficiente de Clustering, se ha establecido el umbral en 0.50 y se obtiene un coeficiente de clustering también variado pero con alrededor de la mitad de nodos con un coeficiente superior a 0.50, lo que sugiere la presencia de comunidades o grupos de nodos altamente conectados entre sí.


\clearpage
## Distribución conjunta de grados y coeficientes de Clustering

![Distribución conjunta de grados y coeficientes de Clustering](C:\Users\carme\Desktop\GitHubSOC\SOC\AvancesProyectoFinal\Roblox\analizarEstructura\Imagenes\cnj_grados_clustering_Roblox.png)

- Conclusiones:

La mayoría de nodos se concentran en un rango de grado entre 0 y 100 y el coeficiente de Clustering de estos es variado. 

Aparecen muchos nodos con un alto grado y un bajo coeficiente, lo que indica que son hubs: nodos con un alto número de conexiones pero tienen menos probabilidad de que todos sus vecinos estén conectados entre sí como resulta lógico.

Se observan también nodos con un grado bajo, lo que indica que son nodos aislados o con pocas conexiones.


\clearpage
## Visualización del grafo según el umbral elegido

Se visualiza el grafo según el umbral elegido para los hubs: los nodos considerados hubs en color rojo. Se escoge una muestra de 100 nodos para que sea posible la visualización en un tiempo aceptable.

![Visualización del grafo](C:\Users\carme\Desktop\GitHubSOC\SOC\AvancesProyectoFinal\Roblox\analizarEstructura\Imagenes\visualizacion_grafo_Roblox.png)

- Conclusiones:

Se ha utilizado el umbral en 10 para considerar a un nodo como hub, lo que permite identificar los nodos más importantes de la red.

Aparece un grupo de nodos centrales que actuaría conectando a todos los grupos de nodos ecteriores entre sí. Se observa que, aunque no todos los nodos están conectados directamente, se puede ir de uno a otro en unos pocos pasos gracias al grupo central.


\clearpage
## Distancia media

- Concepto de distancia media entre nodos:

La **distancia media**  entre nodos es una medida que se utiliza para evaluar la eficiencia de una red en términos de comunicación. Se refiere a la cantidad de pasos promedio que se necesitan para ir de un nodo a otro en la red. 

En una red social, la distancia media entre nodos puede representar la cantidad de intermediarios que se necesitan para que un mensaje llegue de una persona a otra.

- Resultados y conclusiones:

La distancia media entre los nodos de la red es: 3.9796372892141267.

Se obtiene una distancia media baja, lo que indica que la red es eficiente en términos de comunicación y que los nodos están altamente conectados entre sí. Esto sugiere que la información puede propagarse rápidamente a través de la red, lo que es una característica deseable en una red social.


## Diámetro

- Concepto de diámetro de una red:

El **diámetro** de una red es la distancia más larga entre dos nodos de la red: el número máximo de pasos que se necesitan para ir de un nodo a otro en la red.

- Resultados y conclusiones:

El diámetro de esta red es: 7.

En consonancia con la distancia media, se obtiene un diámetro bajo lo que indica que la red está muy conectada desde cualquier punto.


\clearpage
## Gráfica de distancias desde los hubs

- Concepto de distancia desde los hubs:

La distancia entre los hubs se refiere a la medida de cuántos pasos separan a los nodos hubs entre sí en una red. En otras palabras, analiza cómo de conectados están los nodos con mayor grado en la red.

![Distribución de distancias desde los hub](C:\Users\carme\Desktop\GitHubSOC\SOC\AvancesProyectoFinal\Roblox\analizarEstructura\Imagenes\distribucion_distancias_Roblox.png)

- Conclusiones:

Se ha usado un umbral de 10 para considerar a un nodo como hub.

La mayoría de hubs tienen una distancia de entre 4 o 5 nodos entre sí, lo que indica que la red es densa y altamente conectada. Esto también sugiere que la información puede propagarse rápidamente a través de la red. El dato esta en consonancia con la media de distancia de la red mostrada anteriormente.

La existencias de hubs con distancias muy cortas es un síntoma más de la alta conectividad de la red.


\clearpage
## Métricas probabilísticas

- Concepto de probabilidad de enlace, varianza y esperanza:

La probabilidad de enlace refleja la probabilidad de que dos nodos estén conectados entre sí. Representa que tan conectados estan los nodos en relación al máximo número de conexiones posibles.

La esperanza representa el grado medio que tiene un nodo en la red, como se explicó anteriormente, el número medio de conexiones de cada nodo.

La varianza representa la dispersión en la cantidad de conexiones que tienen los nodos de la red, es decir, la posibilidad de que haya nodos con muchas conexiones y otros con muy pocas.

- Resultados y conclusiones:

La **probabilidad de enlace** de esta red es: 0.00235.

La **esperanza** de esta red es: 12.79.

La **varianza** de esta red es: 203.6459.

Se muestra una probabilidad de enlace baja, junto con una esperanza moderada y una varianza alta. Esto explica que la red tiene nodos con un número muy diferente de conexiones, lo que puede indicar la presencia tanto de hubs y como de nodos aislados.

Como se vió anteriormente, la red de Roblox es densa y altamente conectada debido al gran número de hubs y los pocos pasos que se necesitan para ir de un nodo a otro, pero no se debe al hecho de que todos los nodos tengan un número similar de conexiones.

Los grupos entonces desempeñan un papel muy importante en la red, ya que son los que conectan a los miembros y a los juegos, lo que puede explicar la alta varianza en la cantidad de conexiones de los nodos (su número de amigos). Estos grupos actuarían como hubs en la red, conectando a los nodos de diferentes tipos y grados, aumentando la conectividad de esta.
\clearpage


\clearpage
## Conclusiones

- Atributos de la red:

Los nodos de la red tienen diferentes roles y características que afectan su conectividad y posición en la red. En particular, se pueden identificar tres tipos principales de nodos:

1. **Miembros de grupos**: Representan a los usuarios individuales que forman parte de los grupos en Roblox. Estos nodos tienen conexiones con el grupo al que pertenecen y con los juegos que recomiendan.

2. **Grupos**: Representan a las comunidades o clanes dentro de Roblox. Los nodos de grupo están conectados tanto con sus miembros como con los juegos que crean y recomiendan.

3. **Juegos**: Representan los juegos creados por los grupos o recomendados por los miembros. Estos nodos están conectados con los grupos que los crean y con los miembros que los recomiendan.

Estos diferentes tipos de nodos y sus conexiones contribuyen a la **variedad de grados de los nodos** ya que existirán nodos con muchas conexiones (grupos) y otros que no tengan tantos enlaces (miembros/juegos).
Anteriormente se demuestra que es una red **altamente conectada** gracias a los nodos de alto grado. La existencia de estos proporciona **robustez** a la red pero también la hace suceptible de sufrir fragmentación ante la eliminación de alguno de ellos.

- Forma de la red:

Como se podía apreciar en la visualización de la muestra, se crea un grafo en el que se observan concentraciones de nodos (grupos) fuertemente conectadas entre sí y que están a su vez conectadas por otros nodos que funcionan como puentes. Estos puentes pueden representar juegos que pertenecen a un grupo y a su vez son recomendados por otros.

Esta disposición del grafo lleva a la conclusión de que se trata de un **grafo con estructura de comunidades o grafo modular**, el cual es un modelo de grafo bastante común en redes sociales.

- Estructura de la red:

Con el análisis anterior y las conclusiones expuestas, se llega a la conclusión de que la red construida es una **red libre de escala**. Esto es debido a que la distribución del número de conexiones refleja la existencia de pocos nodos con un número muy elevado de conexiones (hubs) y muchos nodos con pocas conexiones.

Este tipo de estructura se da de manera natural en distintas redes sociales y Roblox no sería una excepción.

\clearpage
