import urllib3
import requests
from decouple import config
from plexapi.server import PlexServer

def connect_plex():
    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )  # Plex API hates SSL or something idk it was annoying
    session = requests.Session()  # Open session
    session.verify = False  # Ignore SSL errors
    PLEX_SERVER_URL = config("PLEX_URL")
    PLEX_SERVER_TOKEN = config("PLEX_TOKEN")
    return PlexServer(PLEX_SERVER_URL, PLEX_SERVER_TOKEN, session=session)