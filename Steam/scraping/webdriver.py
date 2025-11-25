from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


# Configurar Selenium con webdriver-manager
def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--log-level=3")  # Reducir logs innecesarios
    chrome_options.add_argument("--headless")  # Opcional para modo sin cabeza

    # Descargar automáticamente la versión adecuada de ChromeDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver


# Función para hacer scroll en la página
def hacer_scroll(driver, num_scrolls):
    try:
        for _ in range(num_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            esperar_segundos(0.5)
    except Exception as e:
        print(f"Error al hacer scroll: {e}")


# Función para hacer clic en un elemento
def hacer_click(driver, selector, espera=10):
    try:
        elemento = WebDriverWait(driver, espera).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        elemento.click()
    except Exception as e:
        print(f"Error al hacer clic en el elemento con selector '{selector}': {e}")


# Función para seleccionar un valor de un desplegable
def seleccionar_valor_desplegable(driver, selector, valor, espera=10):
    try:
        select_element = WebDriverWait(driver, espera).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        select = Select(select_element)
        select.select_by_visible_text(valor)
    except Exception as e:
        print(
            f"Error al seleccionar el valor del desplegable '{valor}' en '{selector}': {e}"
        )


# Función para esperar un tiempo específico
def esperar_segundos(segundos):
    try:
        time.sleep(segundos)
    except Exception as e:
        print(f"Error al esperar: {e}")


# Función para cerrar el navegador
def cerrar_navegador(driver):
    try:
        driver.quit()
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")


# Ejemplo de flujo principal
if __name__ == "__main__":
    driver = configurar_driver()
    try:
        # Ejemplo: abrir una página web
        driver.get("https://store.steampowered.com/")

        # Hacer scroll para cargar más contenido
        hacer_scroll(driver, 5)

        # Hacer clic en un botón (ajusta el selector según sea necesario)
        hacer_click(driver, ".some-button-class")

        # Seleccionar un valor en un desplegable (ajusta el selector y valor)
        seleccionar_valor_desplegable(driver, "#ageYear", "2000")

    except Exception as e:
        print(f"Error general en el flujo principal: {e}")
    finally:
        cerrar_navegador(driver)
