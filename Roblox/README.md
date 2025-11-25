# Notas sobre el proyecto

1. **Problemas intermitentes con la generación de introducción en los informes**  
   A veces, al generar los informes con `pandoc`, la introducción no se incluye correctamente. No hemos sido capaces de identificar la causa exacta, ya que este problema ocurre de manera inconsistente.

2. **Limitaciones de la funcionalidad de la API**  
   - La API no es útil porque no proporciona los HTMLs en el formato adecuado para nuestro análisis.  
   - Además, para acceder a la API es necesario conocer los IDs de los juegos, lo cual limita mucho el tamaño de la muestra y reduce la representatividad de los datos.

3. **Tiempo inicial de compilación elevado**  
   Al principio, el proyecto puede tardar un poco en compilar debido a la necesidad de descargar todos los paquetes de `nltk`, lo que es un proceso pesado pero necesario para su funcionamiento.


# Estructura del proyecto

El proyecto consta de varios módulos y carpetas que se encargan de diferentes fases del análisis y scraping de datos en Roblox:

---

## **mainroblox.py**
Es el script principal del proyecto. Contiene el menú interactivo (definido con `Click`) y enlaza con la opción elegida entre las posibles:
- **`scrape`**: para realizar el proceso de scraping (API o Selenium).
- **`analyze-html-files`**: para analizar los archivos HTML obtenidos.
- **`analyze`**: para ejecutar el análisis del contenido y la estructura de los datos.
- **`salir`**: para finalizar el programa.

---

## **Carpeta Scraping**
Contiene los scripts relacionados con la obtención de datos (scraping) de las páginas de Roblox.

### **scrapearHTML.py**
- Utiliza **Selenium** para navegar por las páginas de Roblox (juegos, grupos, usuarios, etc.).
- Descarga el HTML de cada página y lo guarda localmente en la carpeta `html_scrape`.
- Permite extraer información de varios elementos de la página (enlaces, nombres, descripciones, etc.).

### **ApiHTML.py**
- Utiliza la API de Roblox para obtener el comportamiento anterior pero con otro método.

---

## **Carpeta html_scrape**
Contiene los archivos HTML generados por el script de scraping.  
Cada subcarpeta generalmente corresponde a un **juego** (por ejemplo, `juego1`, `juego2`, etc.) e incluye:
- `juego.html`: información de ese juego concreto.
- `grupo.html` (si aplica) o `usuario.html` (dependiendo de quién sea el creador).
- Una subcarpeta `miembros` con los HTML individuales de una muestra de miembros de un grupo (si el creador es un grupo). 

---

## **Carpeta extraerDatosHTML**
Contiene el script encargado de parsear o extraer información específica de los archivos HTML.

### **analizarHTML.py**
- Lee los archivos HTML de la carpeta `html_scrape`.
- Utiliza **BeautifulSoup** para extraer campos como títulos, descripciones, enlaces, número de miembros, etc.
- Genera un archivo JSON con los datos obtenidos que se guarda en la carpeta `dataSets`.

---

## **Carpeta dataSets**
Aquí se guardan los archivos JSON resultantes del parsing, como:
- `datos_roblox.json`
- `datos_api_roblox.json`  
Esta carpeta es la **entrada** para los análisis posteriores.

---

## **Carpeta analizarContenido**
Contiene los módulos que realizan análisis de contenido.

### **analizarcontenido.py**
Punto de entrada principal. En su interior:
- Invoca a **datosprimitivos**, **datosderivados** y **datosagregados** para calcular diferentes métricas y estadísticas.

#### **datosprimitivos.py**
Analiza información “básica” o directa del JSON, como:
- Usuarios con más amigos.
- Grupos con más miembros.
- Idiomas disponibles.
- Palabras o emoticonos más comunes en descripciones/nombres de juegos, etc.

#### **datosderivados.py**
- Realiza análisis de sentimientos.
- Detecta palabras positivas/negativas en descripciones, obteniendo métricas derivadas de los datos base.

#### **datosagregados.py**
- Calcula valores agregados como número total de juegos, número total de grupos.
- Obtiene medias, máximos y mínimos de ciertas variables.

---

## **Carpeta analizarEstructura**
Realiza el análisis estructural de la red.

### **analizarEstructura.py**
Punto de entrada principal. En su interior, utiliza submódulos como:
- **inicializardiccionarios.py**: inicializa estructuras de datos para el grafo (diccionarios con nodos, aristas, etc.).
- **datosgrafo.py**: calcula cuántos nodos y aristas hay y genera visualizaciones.
- **gradoyclustering.py**: analiza la distribución de grados, coeficiente de clustering e identifica “hubs” basados en umbrales.
- **distancias.py**: calcula la distancia media entre nodos, el diámetro de la red, etc.
- **probabilidad.py**: estima probabilidades de enlace, esperanza y varianza de grado, entre otros aspectos.


---

## **Carpeta informes e informesGenerados**
### **informes**
Contiene los módulos que generan reportes formateados o introducciones a los análisis, como:
- `informe_contenido_roblox.py`
- `informe_estructura_roblox.py`

### **informesGenerados**
Carpeta donde se guardan los **PDF**, **MD** : archivos finales exportados con los resultados del análisis.

---

## **Resumen**
Cada componente del proyecto aporta una parte fundamental al análisis de Roblox:
- **Scraping y Parseo HTML** → Datos primarios y estructurados.
- **Análisis de Contenido** → Información textual y estadística de descripciones, usuarios, juegos, etc.
- **Análisis de Estructura** → Comprensión de la red y conexiones.
- **Informes** → Resultados finales presentados de manera clara.
