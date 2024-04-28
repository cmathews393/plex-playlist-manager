from plexplaylistmanager.modules.lidarr.main import LidarrAPI
from plexplaylistmanager.modules.radarr.main import RadarrAPI
from plexplaylistmanager.modules.sonarr.main import SonarrAPI


def radarr_tag_sync2(users: list[str]) -> dict[str, list[str]]:
    """Sync movies based on Radarr tags and Plex user list, outputting a dictionary of users to their movies."""
    radarr = RadarrAPI()
    movie_dict = radarr.get_radarr_tags()
    plex_users = [user.lower() for user in users]

    user_movies = {
        user: [] for user in plex_users
    }  # Prepare a dictionary to store movies per user

    for key, movie_ids in movie_dict.items():
        user_key = key.lower()  # Normalize key for case-insensitive comparison
        if user_key in plex_users:
            for movie_id in movie_ids:
                movie_title = radarr.get_movie_titles(movie_id)
                user_movies[user_key].append(
                    movie_title,
                )  # Append movie title to the appropriate user
    if user_movies is {} or None:
        return plex_users, None

    return plex_users, user_movies


def sonarr_tag_sync(users: list[str]) -> dict[str, list[str]]:
    """Sync TV shows based on Sonarr tags and Plex user list, outputting a dictionary of users to their shows."""
    sonarr = SonarrAPI()
    show_dict = sonarr.get_sonarr_tags()
    plex_users = [user.lower() for user in users]

    user_shows = {
        user: [] for user in plex_users
    }  # Prepare a dictionary to store shows per user

    for key, show_ids in show_dict.items():
        user_key = key.lower()  # Normalize key for case-insensitive comparison
        if user_key in plex_users:
            for show_id in show_ids:
                show_title = sonarr.get_show_titles(show_id)
                user_shows[user_key].append(
                    show_title,
                )  # Append show title to the appropriate user

    return plex_users, user_shows


def lidarr_tag_sync(users: list[str]) -> dict[str, list[str]]:
    """Sync music artists based on Lidarr tags and Plex user list, outputting a dictionary of users to their artists."""
    lidarr = LidarrAPI()
    artist_dict = lidarr.get_lidarr_tags()
    plex_users = [user.lower() for user in users]

    user_artists = {
        user: [] for user in plex_users
    }  # Prepare a dictionary to store artists per user

    for key, artist_ids in artist_dict.items():
        user_key = key.lower()  # Normalize key for case-insensitive comparison
        if user_key in plex_users:
            for artist_id in artist_ids:
                artist_name = lidarr.get_artist_name(artist_id)
                user_artists[user_key].append(
                    artist_name,
                )  # Append artist name to the appropriate user

    return plex_users, user_artists


def sync_movies(plex, plex_users, user_movies):
    for user in plex_users:
        if user_movies[user]:  # Check if there are movies listed
            plex.create_requests_list("Movies", user_movies[user], user)


def sync_shows(plex, plex_users: list[str], user_shows: dict[str, list[str]]):
    for user in plex_users:
        if user_shows[user]:  # Check if there are shows listed
            plex.create_requests_list("TV Shows", user_shows[user], user)


def sync_music(plex, plex_users: list[str], user_playlists: dict[str, list[str]]):
    for user in plex_users:
        if user_playlists[user]:
            plex.create_requests_list("Music", user_playlists[user], user)
