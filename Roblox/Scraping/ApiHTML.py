import requests
import os


def extraer_html_api(url, params=None, headers=None, filename="Scraping_api.html"):
    """
    Extrae el HTML o JSON de una URL específica de la API de Roblox.

    Parámetros:
    - url (str): La URL de la API a la que se hará la solicitud.
    - params (dict, opcional): Parámetros adicionales para la solicitud.
    - headers (dict, opcional): Encabezados HTTP personalizados.

    Retorna:
    - dict o str: La respuesta en formato JSON si es válida, o texto HTML.
    """
    # Encabezado por defecto si no se proporciona uno
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            # Obtenemos el contenido HTML
            html_text = response.text

            # Si el usuario quiere guardar en un archivo
            if filename:
                os.makedirs("dataSets", exist_ok=True)
                with open(
                    os.path.join("dataSets", filename), "w", encoding="utf-8"
                ) as f:
                    f.write(html_text)

            return html_text

    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None
