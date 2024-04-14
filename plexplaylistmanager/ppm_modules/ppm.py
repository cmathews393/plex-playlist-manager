from .radarr import RadarrAPI
from .plex import PlexService
from .sonarr import SonarrAPI
from typing import List, Dict

def radarr_tag_sync(users: List):
    plex = PlexService()
    movies = []
    radarr = RadarrAPI()
    movie_dict = radarr.get_radarr_tags()
    plex_users = [user.lower() for user in users]
    for key in movie_dict:
        if key.lower() in plex_users:
            for movie_id in movie_dict[key]:
                movie_title = radarr.get_movie_titles(movie_id)

                movies.append(movie_title)
    return movies
            # plex.create_requests_list("Movies", movies, key)



def radarr_tag_sync2(users: List[str]) -> Dict[str, List[str]]:
    """Sync movies based on Radarr tags and Plex user list, outputting a dictionary of users to their movies."""
    plex = PlexService()
    radarr = RadarrAPI()
    movie_dict = radarr.get_radarr_tags()
    plex_users = [user.lower() for user in users]

    user_movies = {user: [] for user in plex_users}  # Prepare a dictionary to store movies per user

    for key, movie_ids in movie_dict.items():
        user_key = key.lower()  # Normalize key for case-insensitive comparison
        if user_key in plex_users:
            for movie_id in movie_ids:
                movie_title = radarr.get_movie_titles(movie_id)
                user_movies[user_key].append(movie_title)  # Append movie title to the appropriate user

    # Optionally, create a request list in Plex for each user
    for user in plex_users:
        if user_movies[user]:  # Check if there are movies listed
            plex.create_requests_list("Movies", user_movies[user], user)

    return plex_users, user_movies

def sync_movies(plex_users, user_movies):
    plex = PlexService()
    for user in plex_users:
        if user_movies[user]:  # Check if there are movies listed
            plex.create_requests_list("Movies", user_movies[user], user)

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
    return shows
            # plex.create_requests_list("TV Shows", shows, key)
