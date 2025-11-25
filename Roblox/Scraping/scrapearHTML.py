import os
import toml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def cargar_configuracion(ruta_archivo):
    """Carga configuraciones desde un archivo TOML."""
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"No se encontró el archivo de configuración: {ruta_archivo}"
        )
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return toml.load(archivo)


def guardar_html(carpeta, subcarpeta, nombre_archivo, contenido):
    """Guarda contenido HTML en una subcarpeta específica."""
    ruta = os.path.join(carpeta, subcarpeta)
    if not os.path.exists(ruta):
        os.makedirs(ruta)

    ruta_archivo = os.path.join(ruta, f"{nombre_archivo}.html")
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    print(f"HTML guardado: {ruta_archivo}")


def intentar_cargar_url(driver, url, intentos=3, delay=5):
    """Carga una URL con reintentos en caso de fallo."""
    for intento in range(intentos):
        try:
            driver.get(url)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return True
        except Exception as e:
            print(f"Error en intento {intento + 1} al cargar {url}: {e}")
            time.sleep(delay)
    return False


def scrape_roblox_data(carpeta="html_scrape", config_path="Scraping/config.toml"):
    """
    Realiza scraping de juegos, grupos y perfiles de miembros en Roblox.
    """
    config = cargar_configuracion(config_path)
    url_charts = config["urls"]["charts"]

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Paso 1: Acceder a la página principal de Roblox
        if not intentar_cargar_url(driver, url_charts):
            print("No se pudo acceder a la página de charts.")
            return

        # Esperar y capturar enlaces de juegos
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "game-card-link"))
        )
        juegos = driver.find_elements(By.CLASS_NAME, "game-card-link")
        urls_juegos = [juego.get_attribute("href") for juego in juegos]
        print(f"Se encontraron {len(urls_juegos)} juegos.")

        # Paso 2: Procesar cada juego
        for idx_juego, juego_url in enumerate(urls_juegos, start=1):
            try:
                if not intentar_cargar_url(driver, juego_url):
                    print(f"No se pudo acceder al juego: {juego_url}")
                    continue

                subcarpeta_juego = f"juego{idx_juego}"
                html_juego = driver.page_source

                # Paso 3: Buscar enlace del grupo/creador
                grupo_o_usuario = driver.find_element(
                    By.CSS_SELECTOR, "a.text-name.text-overflow"
                )
                grupo_o_usuario_url = grupo_o_usuario.get_attribute("href")
                guardar_html(carpeta, subcarpeta_juego, "juego", html_juego)

                if "/communities/" in grupo_o_usuario_url:
                    # Es un grupo
                    print(f"Accediendo al grupo: {grupo_o_usuario_url}")
                    if not intentar_cargar_url(driver, grupo_o_usuario_url):
                        continue

                    html_grupo = driver.page_source
                    guardar_html(carpeta, subcarpeta_juego, "grupo", html_grupo)

                    # Paso 4: Buscar miembros del grupo
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, ".group-members-list .list-item.member")
                        )
                    )
                    miembros = driver.find_elements(
                        By.CSS_SELECTOR, ".group-members-list .list-item.member"
                    )
                    urls_miembros = [
                        miembro.find_element(
                            By.CSS_SELECTOR, 'a[href*="/users/"]'
                        ).get_attribute("href")
                        for miembro in miembros
                    ]
                    print(f"Se encontraron {len(urls_miembros)} miembros.")

                    # Capturar HTML de cada miembro
                    for idx_miembro, miembro_url in enumerate(urls_miembros, start=1):
                        if not intentar_cargar_url(driver, miembro_url):
                            continue
                        html_miembro = driver.page_source
                        guardar_html(
                            carpeta,
                            os.path.join(subcarpeta_juego, "miembros"),
                            f"miembro_{idx_miembro}",
                            html_miembro,
                        )

            except Exception as e:
                print(f"Error al procesar el juego {juego_url}: {e}")

    finally:
        driver.quit()
