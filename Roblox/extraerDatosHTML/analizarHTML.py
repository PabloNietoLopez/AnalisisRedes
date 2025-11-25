import os
import json
from bs4 import BeautifulSoup


def parse_game_page(html_content):
    """Parsea el HTML de la página de un juego para extraer detalles."""
    soup = BeautifulSoup(html_content, "html.parser")
    data = {}

    # Extrae el nombre del juego
    title_tag = soup.find("h1", class_="game-name")
    data["Titulo"] = title_tag.text.strip() if title_tag else "No disponible"

    # Extrae la descripción del juego
    description_tag = soup.find("pre", class_="text game-description")
    if description_tag:
        data["Descripcion"] = description_tag.text.strip()
    else:
        meta_description = soup.find("meta", {"name": "description"})
        data["Descripcion"] = (
            meta_description["content"].strip()
            if meta_description and meta_description.get("content")
            else "No disponible"
        )
    # Extrae los detalles del creador del juego
    creator_tag = soup.find("a", class_="text-name text-overflow")
    if creator_tag:
        data["Creador"] = creator_tag.text.strip()
        data["Creador_URL"] = creator_tag["href"]
        data["TipoCreador"] = (
            "Grupo" if "communities" in creator_tag["href"] else "Individuo"
        )
    else:
        data["Creador"] = "No disponible"
        data["Creador_URL"] = None
        data["TipoCreador"] = "Desconocido"

    # Extrae los detalles del servidor privado
    server_price_tag = soup.find("div", {"data-private-server-price": True})
    data["PrecioServidorPrivado"] = (
        server_price_tag["data-private-server-price"]
        if server_price_tag
        else "No disponible"
    )

    server_limit_tag = soup.find("div", {"data-private-server-limit": True})
    data["MaximoJugadoresServidorPrivado"] = (
        server_limit_tag["data-private-server-limit"]
        if server_limit_tag
        else "No disponible"
    )

    # Extrae el ID
    universe_id_tag = soup.find("div", {"data-universe-id": True})
    data["UniversoID"] = (
        universe_id_tag["data-universe-id"] if universe_id_tag else "No disponible"
    )

    # Extrae juegos recomendados por el creador
    recommended_games = []
    recommended_tags = soup.select(".recommended-experiences-container .game-card")
    for game_tag in recommended_tags:
        game_name = game_tag.find("span", class_="game-card-name")
        game_url = game_tag.find("a", href=True)
        players_tag = game_tag.find("span", class_="game-card-players")
        if game_name and game_url:
            recommended_games.append(
                {
                    "Nombre": game_name.text.strip(),
                    "URL": game_url["href"],
                    "JugadoresActivos": (
                        players_tag.text.strip() if players_tag else "No disponible"
                    ),
                }
            )
    data["JuegosRecomendados"] = recommended_games

    # Extrae la imagen del juego
    game_image_tag = soup.find("meta", property="og:image")
    data["ImagenJuego"] = (
        game_image_tag["content"]
        if game_image_tag and game_image_tag.get("content")
        else "No disponible"
    )

    # Extrae los idiomas disponibles
    hreflang_tags = soup.find_all("link", rel="alternate")
    languages = []
    for tag in hreflang_tags:
        if "hreflang" in tag.attrs:
            languages.append(tag["hreflang"])
    data["IdiomasDisponibles"] = languages if languages else "No disponible"

    # Extrae la fecha de lanzamiento
    release_date_tag = soup.find("div", class_="text-lead")
    data["FechaLanzamiento"] = (
        release_date_tag.text.strip() if release_date_tag else "No disponible"
    )

    return data


def parse_group_page(html_content):
    """Parsea el HTML de la página de un grupo para extraer detalles."""
    soup = BeautifulSoup(html_content, "html.parser")
    data = {}

    # Extrae el nombre del grupo
    group_name_tag = soup.find("meta", property="og:title")
    if group_name_tag and group_name_tag.get("content"):
        data["NombreGrupo"] = group_name_tag["content"].strip()
    else:
        data["NombreGrupo"] = "No disponible"

    # Extrae la descripción del grupo
    description_meta = soup.find("meta", property="og:description")
    if description_meta and description_meta.get("content"):
        data["DescripcionGrupo"] = description_meta["content"].strip()

        # Extrae el número de miembros que viene en la descripción
        members_info = (
            description_meta["content"].split(" with ")[1].split(" members.")[0]
            if " with " in description_meta["content"]
            else "No disponible"
        )
        data["NumeroMiembros"] = members_info.strip()
    else:
        data["DescripcionGrupo"] = "No disponible"
        data["NumeroMiembros"] = "No disponible"

    # Extrae la URL del grupo
    group_url_meta = soup.find("meta", property="og:url")
    data["URLGrupo"] = (
        group_url_meta["content"].strip()
        if group_url_meta and group_url_meta.get("content")
        else "No disponible"
    )

    # Extrae la imagen del grupo
    group_image_meta = soup.find("meta", property="og:image")
    data["ImagenGrupo"] = (
        group_image_meta["content"].strip()
        if group_image_meta and group_image_meta.get("content")
        else "No disponible"
    )

    # Extrae los idiomas disponibles
    hreflang_tags = soup.find_all("link", rel="alternate")
    languages = []
    for tag in hreflang_tags:
        if "hreflang" in tag.attrs:
            languages.append(tag["hreflang"])
    data["IdiomasSoportados"] = languages if languages else "No disponible"

    return data


def parse_member_page(html_content):
    """Parsea el HTML de la página de un miembro para extraer detalles."""
    soup = BeautifulSoup(html_content, "html.parser")
    data = {}

    # Extrae el nombre del miembro
    name_tag = soup.find("meta", property="og:title")
    data["Nombre"] = (
        name_tag["content"].split("'s Profile")[0].strip()
        if name_tag and name_tag.get("content")
        else "No disponible"
    )

    # Extrae la descripción del miembro
    description_tag = soup.find("meta", property="og:description")
    data["Descripcion"] = (
        description_tag["content"].strip()
        if description_tag and description_tag.get("content")
        else "No disponible"
    )

    # Extrae la URL del perfil
    profile_url_tag = soup.find("meta", property="og:url")
    data["Perfil_URL"] = (
        profile_url_tag["content"]
        if profile_url_tag and profile_url_tag.get("content")
        else "No disponible"
    )

    # Extrae la imagen de perfil
    profile_image_tag = soup.find("meta", property="og:image")
    data["Imagen_Perfil"] = (
        profile_image_tag["content"]
        if profile_image_tag and profile_image_tag.get("content")
        else "No disponible"
    )

    # Extrae el alias si está disponible
    alias_container = soup.find("div", class_="aliases-container")
    if alias_container:
        alias_tag = alias_container.find("span", class_="alias-name")
        data["Alias"] = alias_tag.text.strip() if alias_tag else "No disponible"
    else:
        data["Alias"] = "No disponible"

    # Extrae estadísticas de amigos, seguidores y seguidos
    stats = {}
    stats_tags = soup.select("div.header-details ul.details-info li")
    for stat in stats_tags:
        label = stat.find("div", class_="text-label")
        value = stat.find("span", class_="font-header-2")
        if label and value:
            stats[label.text.strip()] = int(value["title"])
    data["Estadisticas"] = stats

    # Extrae la fecha de unión
    join_date_tag = soup.find("li", class_="profile-stat")
    if join_date_tag:
        label = join_date_tag.find("p", class_="text-label")
        value = join_date_tag.find("p", class_="text-lead")
        if label and value and label.text.strip() == "Join Date":
            data["FechaUnion"] = value.text.strip()
    else:
        data["FechaUnion"] = "No disponible"

    # Extrae juegos favoritos
    favorites = []
    favorite_tags = soup.select(".favorite-games-container .game-card-name")
    for game_tag in favorite_tags:
        if game_tag.get("title"):
            favorites.append(game_tag["title"])
    data["JuegosFavoritos"] = favorites

    # Extrae el estado de actividad
    activity_status_tag = soup.find("span", class_="activity-status")
    data["EstadoActividad"] = (
        activity_status_tag.text.strip() if activity_status_tag else "No disponible"
    )

    # Extrae grupos destacados
    groups = []
    group_tags = soup.select(".groups-showcase .group-card a")
    for group_tag in group_tags:
        if group_tag.get("href"):
            groups.append({"Nombre": group_tag.text.strip(), "URL": group_tag["href"]})
    data["GruposDestacados"] = groups

    # Extrae el equipamiento actual
    items = []
    item_tags = soup.select(".current-items img")
    for item_tag in item_tags:
        if item_tag.get("alt") and item_tag.get("src"):
            items.append(
                {"Nombre": item_tag["alt"].strip(), "Imagen_URL": item_tag["src"]}
            )
    data["EquipamientoActual"] = items

    return data


def analyze_html_to_json(
    folder="html_scrape", output_folder="dataSets", output_json="datos_jerarquicos.json"
):
    """Analiza los archivos HTML extraídos y guarda los datos en un archivo JSON."""
    if not os.path.exists(folder):
        print(f"La carpeta '{folder}' no existe.")
        return

    games = []

    # Iterar sobre cada subfichero(juego1, juego2, etc.)
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            # Paths de los archivos de juego, grupo y usuario
            game_file = os.path.join(subfolder_path, "juego.html")
            group_file = os.path.join(subfolder_path, "grupo.html")
            user_file = os.path.join(subfolder_path, "usuario.html")
            members_folder = os.path.join(subfolder_path, "miembros")

            # Parsea el archivo de juego
            game_data = {}
            if os.path.exists(game_file):
                with open(game_file, "r", encoding="utf-8") as file:
                    game_content = file.read()
                    game_data = parse_game_page(game_content)

            # Parsea el archivo de grupo o usuario
            if os.path.exists(group_file):
                with open(group_file, "r", encoding="utf-8") as file:
                    group_content = file.read()
                    group_data = parse_group_page(group_content)
                    group_data["Tipo"] = "Grupo"
            elif os.path.exists(user_file):
                with open(user_file, "r", encoding="utf-8") as file:
                    user_content = file.read()
                    group_data = parse_member_page(user_content)
                    group_data["Tipo"] = "Usuario"
            else:
                group_data = {"Tipo": "Desconocido", "Detalles": "No disponible"}

            # Parsea los archivos de los miembros si es un grupo
            if group_data.get("Tipo") == "Grupo" and os.path.exists(members_folder):
                members = []
                member_files = os.listdir(members_folder)
                for member_file in member_files:
                    member_path = os.path.join(members_folder, member_file)
                    with open(member_path, "r", encoding="utf-8") as file:
                        member_content = file.read()
                        member_data = parse_member_page(member_content)
                        members.append(member_data)
                group_data["Miembros"] = members

            # Agrega los datos del juego al diccionario del grupo
            game_data["Creador"] = group_data
            games.append(game_data)

    output_path = os.path.join(output_folder, output_json)
    # Guarda los datos en un archivo JSON
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(games, json_file, ensure_ascii=False, indent=4)

    print(f"Datos analizados y guardados en '{output_json}'.")
