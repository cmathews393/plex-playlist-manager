import requests
import urllib3
from plexapi.server import PlexServer
from confighandler import read_config
from typing import List

class PlexService:
    def __init__(self):
        self.config = read_config("plex")
        self.server_url = self.config.get("url")
        self.server_token = self.config.get("api_key")
        self.plex = self.connect_plex()
        self.replace = self.config.get("replace")
        self.requests_playlist = self.config.get("requests_playlist"), "My Requests"

    def connect_plex(self):
        self.session = requests.Session()
        self.session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return PlexServer(self.server_url, self.server_token, session=self.session)
    
    def get_plex_users(self):
        try:
            users = self.plex.myPlexAccount().users()
            return [user.username for user in users]  # Assuming 'title' holds the user's name
        except Exception as e:
            #TODO log this
            return None

    def check_tracks_in_plex(self, spotify_tracks):
        music_lib = self.plex.library.section("Music")
        plex_tracks = []
        orig_tracks = []

        for track_name, artist_name in spotify_tracks:
            artist_tracks_in_plex = music_lib.search(title=artist_name)
            if artist_tracks_in_plex:
                try:
                    for track in artist_tracks_in_plex:
                        plex_track = track.track(title=track_name)
                        if plex_track:
                            plex_tracks.append(plex_track)
                        else:
                            orig_tracks.append([track_name, "Song Not in Plex"])
                except Exception as plex_search_exception:
                    print(plex_search_exception)
            else:
                continue

        return plex_tracks

    def create_or_update_playlist(
        self, playlist_name, playlist_id, tracks
    ):
        existing_playlist = self.find_playlist_by_name(playlist_name)
        if existing_playlist:
            if self.replace:
                existing_playlist.delete()
                return self.create_playlist(playlist_name, playlist_id, tracks)
            else:
                existing_playlist.addItems(tracks)
                return existing_playlist
        else:
            return self.create_playlist(playlist_name, playlist_id, tracks)

    def find_playlist_by_name(self, playlist_name):
        playlists = self.plex.playlists()
        for playlist in playlists:
            if playlist.title == playlist_name:
                return playlist
        return None

    def create_playlist(self, playlist_name, playlist_id, tracks):
        try:
            new_playlist = self.plex.createPlaylist(playlist_name, items=tracks)
            return new_playlist
        except Exception as e:
            print(f"Error creating playlist {playlist_name}: {e}")
            return None

    def create_requests_list(self, section_name: str, titles: List[str], user_name: str) -> str:
        """Adds a list of titles to a new playlist on a Plex server."""
        print("got users")
        users = self.plex.myPlexAccount().users()
        print("iterated users")
        print(users)  # Debug print to show all users

        # Find the user in a case-insensitive manner but preserve the actual username
        for plexuser in users:
            print(plexuser.title)
            if user_name.lower() in plexuser.title.lower():
                user = plexuser
        # user = next((user for user in users if user_name.lower() in user.username.lower()), None)

                if not user:
                    print("User not found.")
                    return "User not found."  # It's good to return after finding no user to stop execution

        print(f"connecting as user: {user.username}")  # user.username preserves the actual case
        plex = PlexServer(self.server_url, user.get_token(self.plex.machineIdentifier), session=self.session)
        print("success")

        section = plex.library.section(section_name)
        print(f"section is {section}")
        items = []
        for user_title in titles:
            print(user_title)
            search_result = section.search(title=user_title)  # Perform the search
            if search_result:
                # If search_result is not empty, append the found movie objects to items
                items.extend(search_result)  # Assuming search_result is a list of Movie objects
                print(f"Found and added: {[item.title for item in search_result]}")
            else:
                print(f"Not found: {user_title}")

        if not items:
            raise ValueError("No items found to add to the playlist.")

        plex.createPlaylist(self.requests_playlist, items=items)
        return f'Playlist "{self.requests_playlist}" created successfully with {len(items)} items.'