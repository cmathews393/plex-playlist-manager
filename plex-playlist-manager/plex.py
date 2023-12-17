import urllib3
import requests
from config_handler import read_config
from plexapi.server import PlexServer


def connect_plex():
    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )  # Plex API hates SSL or something idk it was annoying
    session = requests.Session()  # Open session
    session.verify = False  # Ignore SSL errors
    plex_config = read_config("plex")
    PLEX_SERVER_URL = plex_config.get("url")
    PLEX_SERVER_TOKEN = plex_config.get("apikey")
    print(PLEX_SERVER_TOKEN, PLEX_SERVER_URL)
    return PlexServer(PLEX_SERVER_URL, PLEX_SERVER_TOKEN, session=session)

