import click
import Scraping.scrapearHTML as scrapearHTML
import analizarEstructura.crearEdgeList as crearEdgeList
import Scraping.ApiHTML as ApiHTML
import json
import analizarContenido.analizarcontenido as analizarcontenido
import analizarEstructura.analizarEstructura as analizarestructura
import extraerDatosHTML.analizarHTML as analizarHTML
import informes.introduccion_roblox as introduccion_roblox
import informes.informe_contenido_roblox as informe_contenido_roblox
import informes.informe_estructura_roblox as informe_estructura_roblox
import os


@click.group(invoke_without_command=True)
@click.pass_context
def menu(ctx):
    """
    Menú interactivo para scraping y análisis de datos de Roblox.

    Si no se invoca con un subcomando desde la terminal (por ejemplo,
    "python mainroblox.py scrape"), se mostrará un menú iterativo.
    """
    # Opcional: Ajustar el directorio de trabajo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    print(f"Directorio actual cambiado a: {os.getcwd()}")

    # Si no se recibió ningún subcomando (por ejemplo, "scrape", "analyze", etc.)
    # entonces entramos en el menú interactivo.
    if ctx.invoked_subcommand is None:
        while True:
            click.echo("\n--- Menú Roblox ---")
            click.echo("1) Scrape (API o Selenium)")
            click.echo("2) Análisis de archivos HTML")
            click.echo("3) Análisis de contenido y estructura")
            click.echo("4) Salir")

            # Solicitamos al usuario la elección
            choice = click.prompt("Selecciona una opción", type=int)

            if choice == 1:
                ctx.invoke(scrape)
            elif choice == 2:
                ctx.invoke(analyze_html_files)
            elif choice == 3:
                ctx.invoke(analyze)
            elif choice == 4:
                ctx.invoke(salir)
                break  # Salimos del bucle y finalizamos el programa
            else:
                click.echo("Opción no válida. Intenta nuevamente.")


@menu.command()
def scrape():
    """Obtener datos usando API o scraping (Selenium)."""
    option = click.prompt("¿Deseas usar 'api' o 'scraping'?", type=str)
    if option == "api":
        click.echo("Iniciando extracción de datos con la API...")
        get_html_from_api()
    elif option == "scraping":
        click.echo("Iniciando scraping de datos con Selenium...")
        scrapearHTML.scrape_roblox_data()
    else:
        click.echo("Opción no válida.")


def get_html_from_api():
    """Ejemplo de función para obtener HTML/JSON desde la API de Roblox."""
    universe_ids = [
        "5569032992",
        "1234567890",
        "292439477",
        "606849621",
        "2041312716",
        "2753915549",
        "920587237",
        "286090429",
        "4954752502",
        "2414851778",
        "2248408710",
        "4042427666",
        "2377868068",
    ]
    url = f"https://games.roblox.com/v1/games?universeIds={','.join(universe_ids)}"

    data = ApiHTML.extraer_html_api(url)
    if data:
        # Convertir a JSON si es dict
        if isinstance(data, dict):
            data_str = json.dumps(data, ensure_ascii=False, indent=4)
            file_name = "datos_api_roblox.json"
        else:
            data_str = data
            file_name = "datos_api_roblox.html"

        with open(file_name, "w", encoding="utf-8") as file:
            file.write(data_str)

        click.echo(f"Datos extraídos y guardados en '{file_name}'.")
    else:
        click.echo("No se pudo obtener datos de la API.")


@menu.command()
def analyze_html_files():
    """Analizar los archivos HTML extraídos y generar JSON."""
    folder = click.prompt(
        "Especifica la carpeta donde están los archivos HTML (por defecto 'html_scrape')",
        default="html_scrape",
    )
    output_json = click.prompt(
        "Especifica el nombre del archivo JSON de salida (por defecto 'datos_roblox.json')",
        default="datos_roblox.json",
    )
    click.echo("Analizando archivos HTML extraídos...")
    analizarHTML.analyze_html_to_json(folder=folder, output_json=output_json)
    click.echo(f"Análisis completado. Datos guardados en '{output_json}'.")


@menu.command()
def analyze():
    """Analizar el contenido y la estructura de los datos."""
    click.echo("Analizando el contenido de los datos...")
    diccionario_contenido = analizarcontenido.analizar()
    introduccion_roblox.generar_resultados()
    informe_contenido_roblox.generar_resultados(diccionario_contenido)

    click.echo("Analizando la estructura de la red...")
    edgeList = crearEdgeList.obtener_edgelist()
    diccionario_estructura = analizarestructura.analizar(edgeList, nombre_red="Roblox")
    informe_estructura_roblox.generar_resultados(diccionario_estructura)


@menu.command()
def salir():
    """Salir del programa."""
    click.echo("Saliendo del programa...")
    raise SystemExit(0)


if __name__ == "__main__":
    menu()
