# README

Este proyecto permite ejecutar diferentes scripts de análisis y scraping relacionados con la red Steam. Los scripts están organizados en subcarpetas y este comando permite ejecutar el script correspondiente según la subcarpeta proporcionada.

## Comandos Disponibles

- `analizarContenido`: Ejecuta el script `analizarContenido/analizarcontenido.py`. El programa analiza los datos del dataset y convierte los datos crudos y derivados obtenidos en gráficas que los permitan visualizar y entender.
- `analizarEstructura`: Ejecuta el script `analizarEstructura/analizarEstructura.py`. El programa analiza los datos del dataset, extrayendo de ellos la estructura de grafo y calculando diversas propiedades. Todo ello se guarda en un informe. 
- `analizarHTML`: Ejecuta el script `analizarHTML/analizar_HTML.py`. El programa analiza los datos de los html guardados y se guardan en un dataset en formato **json**.
- `scraping`: Ejecuta el script `scraping/scraping.py`. El programa se descargalos dato de las red, guardando el conjunto de ficheros html resultantes.

Ademas existe una subcarpeta llamada `Informes` que contiene los informes de contenido y estructura en formato **pdf**. No se puede ejecutar.

## Requisitos

- Python 3.x.
- Instalar `uv` (`pip install uv`).


## Uso

Para ejecutar un script específico, usamos **click**. Abre una terminal y navega al directorio donde se encuentra este script. Luego, ejecuta el siguiente comando, reemplazando `<subcarpeta>` por el nombre de la subcarpeta deseada:
```bash
uv run main.py --modulo <subcarpeta>
```
## Manejo de Errores

Si el archivo correspondiente al script no existe, el script mostrará un mensaje de error:
Error: El archivo `<script_path>` no existe.
