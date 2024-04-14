from .radarr import RadarrAPI
from .plex import PlexService
from .sonarr import SonarrAPI
from typing import List

def radarr_tag_sync(users: List):
    plex = PlexService()
    movies = []
    radarr = RadarrAPI()
    movie_dict = radarr.get_radarr_tags()
    plex_users = users
    for key in movie_dict:
        if key in plex_users:
            for movie_id in movie_dict[key]:
                movie_title = radarr.get_movie_titles(movie_id)

                movies.append(movie_title)
            plex.create_requests_list("Movies", movies, key)



def sonarr_tag_sync(users: List):
    plex = PlexService()
    shows = []
    sonarr = SonarrAPI()
    show_dict = sonarr.get_sonarr_tags()
    plex_users = users
    for key in show_dict:
        if key in plex_users:
            for show_id in show_dict[key]:
                show_title = sonarr.get_show_titles(show_id)
                shows.append(show_title)
            plex.create_requests_list("TV Shows", shows, key)
