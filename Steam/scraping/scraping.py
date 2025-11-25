import toml
import requests
from bs4 import BeautifulSoup
import creacion_html
import webdriver


# Función para cargar la URL desde el archivo de configuración
def cargar_configuracion(file_path):
    with open(file_path, "r") as f:
        return toml.load(f).get("url")


def obtener_html_nodo(enlace, nombre_carpeta, contenido):
    # Comprobar o crear la estructura de archivos necesaria
    ruta_diccionario = creacion_html.comprobar_existencia_archivos(nombre_carpeta)
    diccionario = creacion_html.cargar_diccionario(ruta_diccionario)

    # Verificar si ya existe el archivo HTML crudo
    if enlace not in diccionario:

        contenido_html = contenido  # Codificar en utf-8 para evitar problemas
        creacion_html.guardar_html_crudo(enlace, contenido_html, nombre_carpeta)


def iniciar_parte_dinamica(driver, enlace_juego):
    driver.get(enlace_juego)

    if "agecheck" in driver.current_url:
        # Esperar a que el desplegable sea visible y seleccionar el año
        webdriver.seleccionar_valor_desplegable(driver, "#ageYear", "2000")
        # Esperar a que el botón de verificación sea clickeable y hacer clic
        webdriver.hacer_click(driver, "#view_product_page_btn")

        webdriver.esperar_segundos(1)

    # Simular scroll hacia abajo para cargar más reseñas
    webdriver.hacer_scroll(driver, 1)  # Ajusta el número de scrolls según la necesidad

    # Devuelve el HTML crudo directamente desde el driver
    return driver.page_source


# Función principal
def main():
    # Cargar la URL desde el archivo de configuración
    url = cargar_configuracion(r"scraping\url.toml")

    # EXCEPCION STEAMDECK
    url_a_omitir = (
        "https://store.steampowered.com/app/1675200/Steam_Deck/?snr=1_7_7_7000_150_1"
    )

    # Realizar la solicitud HTTP a la URL
    respuesta = requests.get(url)

    if respuesta.status_code == 200:

        soup = BeautifulSoup(respuesta.text, "html.parser")

        juegos = soup.find_all("a", class_="search_result_row")

        # Inicializar contador de juegos procesados
        contador = 0

        for juego in juegos:

            enlace_juego = juego["href"]

            if enlace_juego != url_a_omitir:

                print(f"Accediendo a: {enlace_juego}")

                # JUEGOS
                driver = webdriver.configurar_driver()
                page_source = iniciar_parte_dinamica(driver, enlace_juego)
                webdriver.cerrar_navegador(driver)
                obtener_html_nodo(enlace_juego, "html_juegos", page_source)

                # COMENTARIOS Y USUARIOS
                soup_juego = BeautifulSoup(page_source, "html.parser")
                comentarios = soup_juego.find_all("div", class_="review_box")

                # Verificar si se han encontrado comentarios
                if comentarios:
                    comentarios_str = "".join(
                        [comentario.prettify() for comentario in comentarios]
                    )
                    obtener_html_nodo(enlace_juego, "html_comentarios", comentarios_str)

                    # Iterar sobre cada bloque de reseña, con un contador para limitar a 10
                    contador_comentarios = 0
                    # Iterar sobre cada bloque de reseña
                    for comentario in comentarios:
                        if contador_comentarios >= 10:
                            break  # Salir del bucle si ya se han procesado 10 comentarios

                        # Verificar si el comentario tiene el enlace del usuario
                        persona_name = comentario.find("div", class_="persona_name")
                        if persona_name:
                            enlace_usuario = persona_name.find("a")["href"]
                            driver_usuario = webdriver.configurar_driver()
                            usuario_page_source = iniciar_parte_dinamica(
                                driver_usuario, enlace_usuario
                            )
                            webdriver.cerrar_navegador(driver_usuario)
                            obtener_html_nodo(
                                enlace_usuario, "html_usuarios", usuario_page_source
                            )

                            # Incrementar el contador después de procesar el usuario
                            contador_comentarios += 1
                        else:
                            print(
                                f"Comentario sin enlace de usuario encontrado. Comentario: {comentario}"
                            )
                else:
                    print("No se encontraron comentarios para este juego.")

                # DESARROLLADORES

                enlace_desarrollador = soup_juego.find(
                    "div", id="developers_list"
                ).find("a")["href"]
                driver_desarrollador = webdriver.configurar_driver()
                desarrollador_page_source = iniciar_parte_dinamica(
                    driver_desarrollador, enlace_desarrollador
                )
                webdriver.cerrar_navegador(driver_desarrollador)
                obtener_html_nodo(
                    enlace_desarrollador,
                    "html_desarrolladores",
                    desarrollador_page_source,
                )

                # COMUNIDADES

                div_details_total = soup_juego.find_all("div", class_="details_block")

                div_details = None
                for div in div_details_total:
                    if not div.has_attr("id"):
                        div_details = div
                        break

                # Busca todos los enlaces <a> con la clase específica
                if div_details:
                    enlaces = div_details.find_all("a", href=True)
                    enlace_comunidad = (
                        None  # Inicializa la variable para el enlace específico
                    )
                    for enlace in enlaces:
                        if (
                            "href" in enlace.attrs
                            and "Visitar el Workshop" in enlace.text.strip()
                        ):
                            enlace_comunidad = enlace["href"]
                            print(f"Enlace encontrado: {enlace_comunidad}")
                            break  # Sale del bucle una vez que se encuentra el enlace
                    if not enlace_comunidad:
                        print(
                            "No se encontró el enlace con el texto 'Visitar el Workshop'."
                        )
                else:
                    print("No se encontró el div con la clase 'details_block'.")

                if enlace_comunidad:
                    driver_comunidad = webdriver.configurar_driver()
                    comunidad_page_source = iniciar_parte_dinamica(
                        driver_comunidad, enlace_comunidad
                    )
                    webdriver.cerrar_navegador(driver_comunidad)
                    obtener_html_nodo(
                        enlace_comunidad, "html_comunidades", comunidad_page_source
                    )
                else:
                    print("No tiene comunidad de modificadores")

                # EVENTOS
                contenedor = soup_juego.find("div", class_="_1snIw0RvJduvDtqpmwtKJ9")

                # Verificar si el contenedor de eventos existe y tiene enlaces
                if contenedor and contenedor.find_all("a", href=True):
                    enlaces_eventos = contenedor.find_all("a", href=True)

                    for enlace in enlaces_eventos:
                        # Verifica si el enlace tiene una URL válida
                        if enlace["href"]:
                            driver_evento = webdriver.configurar_driver()
                            evento_page_source = iniciar_parte_dinamica(
                                driver_evento, enlace["href"]
                            )
                            webdriver.cerrar_navegador(driver_evento)
                            obtener_html_nodo(
                                enlace["href"], "html_eventos", evento_page_source
                            )
                else:
                    print("No se encontraron eventos para este juego.")

                # Incrementar el contador
                contador += 1
                print(f"Juegos procesados: {contador}")

                # Verificar si se alcanzó el límite de juegos
                if contador >= 20:
                    print(
                        "Se alcanzó el límite de juegos procesados. Deteniendo el programa."
                    )
                    break

    else:
        print(
            f"Error al realizar la solicitud. Código de estado: {respuesta.status_code}"
        )


if __name__ == "__main__":
    main()
