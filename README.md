# Analisis de Redes sociales - Menú Principal

Este programa permite seleccionar y ejecutar diferentes entornos y funciones relacionadas con análisis y scraping de datos en los sistemas de **Roblox** y **Steam**.

## Uso

### 1. Roblox

Debe ejecutarse el entorno de Roblox:

```bash
uv run main.py roblox
```

### Comandos:
Una vez dentro del entorno de Roblox, se imprimirá un menú interactivo para que el usuario teclee el número de la opción elegida. Estas son:

- `1) Scrape (API o Selenium)`: Obtener datos usando API o scraping.
- `2) Análisis de archivos HTML`: Analizar los archivos HTML extraídos.
- `3) Análisis de contenido y estructura`: Analizar el contenido y la estructura de los datos.
- `4) Salir`: Salir del programa.
  
## Ejemplo:

__Analizar HTML (Roblox)__:
```bash
uv run main.py roblox

--- Menú Roblox ---
1) Scrape (API o Selenium)
2) Análisis de archivos HTML
2) Análisis de archivos HTML
3) Análisis de contenido y estructura
3) Análisis de contenido y estructura
4) Salir
Selecciona una opción: 2
```

### 2. Steam

Ejecuta el entorno de Steam:

### Comandos:
- `analizarContenido`: Analizar el contenido de los datos
- `analizarEstructura`: Analizar la estructura de los datos.
- `analizarHTML`: Analizar los archivos HTML extraídos.
- `scraping`: Obtener datos scraping.

## Ejemplo:

__Analizar HTML (Steam)__:
```bash
uv run main.py steam --modulo analizarContenido
```





  
