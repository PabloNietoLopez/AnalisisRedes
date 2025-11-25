import os
import sys
from pathlib import Path
import click


@click.command()
@click.option("--modulo", default="scraping", help="Script a utilizar")
def ejecutar_analisis(modulo):

    # Realizar el análisis de datos
    if modulo == "analizarContenido":
        script_path = "analizarContenido/analizarcontenido.py"
    elif modulo == "analizarEstructura":
        script_path = "analizarEstructura/analizarEstructura.py"
    elif modulo == "analizarHTML":
        script_path = "analizarHTML/analizar_HTML.py"
    elif modulo == "scraping":
        script_path = "scraping/scraping.py"

    # Verificar si el archivo existe
    if not Path(script_path).exists():
        print(f"Error: El archivo '{script_path}' no existe.")
        sys.exit(1)

    # Ejecutar el script
    os.system(f"python {script_path}")


if __name__ == "__main__":
    ejecutar_analisis()
