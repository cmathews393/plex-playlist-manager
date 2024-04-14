from plexapi.server import PlexServer
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def create_playlist_for_user(baseurl, token, user_name, playlist_name, movies):
    """
    Create a playlist in Plex for a specific user.
    
    Args:
    baseurl (str): URL to the Plex server.
    token (str): Your Plex authentication token.
    user_name (str): Name of the user for whom to create the playlist.
    playlist_name (str): Name of the new playlist.
    movies (list): List of movie titles to add to the playlist.
    
    Returns:
    str: Status message indicating success or failure.
    """
    session = requests.Session()
    session.verify = False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Connect to the Plex server
    plex = PlexServer(baseurl, token, session=session)
    
    # Find the specified user
    users = plex.myPlexAccount().users()
    user = next((user for user in users if user.username == user_name), None)
    if not user:
        return "User not found."
    
    # Switch to the user's Plex server view
    plex = PlexServer(baseurl, user.get_token(plex.machineIdentifier), session=session)
    
    # Access the main movie library
    movies_section = plex.library.section('Movies')
    
    # Find movies by title and prepare for the playlist
    movie_items = [movies_section.get(movie) for movie in movies if movies_section.get(movie)]
    if not movie_items:
        return "No movies found to add to the playlist."
    
    # Create the playlist
    plex.createPlaylist(playlist_name, items=movie_items)
    
    return "Playlist created successfully."

# Example usage:
baseurl = 'https://192.168.1.160:32400'
token = '2PygzSbEB3DQ6i-NVtLn'
user_name = 'tylersnyder887'
playlist_name = 'Favorite Sci-Fi Movies'
movies = ['Interstellar', 'The Matrix', 'Blade Runner']

result = create_playlist_for_user(baseurl, token, user_name, playlist_name, movies)
print(result)
