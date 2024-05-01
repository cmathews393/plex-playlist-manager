import concurrent.futures
import os
import time
from concurrent.futures import ThreadPoolExecutor

import schedule

from ppm.modules.confighandler.main import read_config, write_config
from ppm.modules.lidarr.main import LidarrAPI as lapi
from ppm.modules.plex.main import PlexService
from ppm.modules.spotify.main import SpotifyService


class Spotiplex:
    def __init__(self):
        self.config = read_config("spotiplex")
        self.spotify_service = SpotifyService()
        self.plex_service = PlexService()
        self.lidarr_api = lapi()

        self.lidarr_sync = (self.config.get("lidarr_sync", "false")).lower()
        self.plex_users = self.config.get("plex_users")
        self.user_list = self.plex_users.split(",") if self.plex_users else []
        self.worker_count = int(self.config.get("worker_count"))
        self.replace_existing = self.config.get("replace_existing")
        self.seconds_interval = int(self.config.get("seconds_interval"))
        if self.lidarr_sync == "true":
            self.sync_lists = self.lidarr_api.get_lidarr_playlists()
        else:
            # This should be an array of arrays to be run by multiple 'threads':
            # For example: [["playlist1"],["playlist2"],["playlist3","playlist4"]]
            self.sync_lists = self.config.get("manual_playlists")
        print(f"Attempting to run for {self.sync_lists}")
        self.default_user = self.plex_service.plex.myPlexAccount().username

        # If the the user list provided is empty, add the default user from the token
        if not self.user_list or len(self.user_list) == 0:
            self.user_list.append(self.default_user)

    def process_for_user(self, user):
        print(f"processing for user {user}")
        if user == self.default_user:
            self.plex_service.plex = self.plex_service.plex
            print(f"Processing playlists for user: {user}")
            print("User matches credentials provided, defaulting.")
        else:
            print(f"Attempting to switch to user {user}")
            self.plex_service.plex = self.plex_service.plex.switchUser(user)

        with ThreadPoolExecutor(max_workers=self.worker_count) as executor:
            futures = [
                executor.submit(
                    self.process_playlist,
                    playlist,
                    self.plex_service,
                    self.spotify_service,
                    self.replace_existing,
                )
                for playlist in self.sync_lists
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Thread resulted in an error: {e}")

    def is_running_in_docker():
        return os.path.exists("/.dockerenv")

    def run(self):
        for user in self.user_list:
            self.process_for_user(user)
        if self.seconds_interval > 0:
            schedule.every(self.seconds_interval).seconds.do(self.run)
            while True:
                schedule.run_pending()
                time.sleep(1)

    def extract_playlist_id(playlist_url):  # parse playlist ID from URL if applicable
        if "?si=" in playlist_url:
            playlist_url = playlist_url.split("?si=")[0]

        return (
            playlist_url.split("playlist/")[1]
            if "playlist/" in playlist_url
            else playlist_url
        )

    def process_playlist(
        self, playlists, plex_service, spotify_service, replace_existing
    ):
        for playlist in playlists:
            try:
                playlist_id = Spotiplex.extract_playlist_id(playlist)
                print(playlist_id)
                playlist_name = spotify_service.get_playlist_name(playlist_id)
                spotify_tracks = spotify_service.get_playlist_tracks(playlist_id)
                plex_tracks = plex_service.check_tracks_in_plex(spotify_tracks)
                plex_service.create_or_update_playlist(
                    playlist_name, playlist_id, plex_tracks
                )
                print(f"Processed playlist '{playlist_name}'.")
            except Exception as e:
                print(f"Error processing playlist '{playlist}':", e)

    def configurator(self):
        # Config for Spotiplex

        print(
            "Welcome to Spotiplex! It seems this is your first run of the application, please enter your configuration variables below. Press Enter to continue..."
        )
        spotiplex_config = {
            "lidarr_sync": input("Enter Lidarr sync option (True/False): "),
            "plex_users": input("Enter comma-separated Plex user names: "),
            "worker_count": int(
                input(
                    "Enter the number of worker threads (Not recommened to exceed core count. 5 is usually a good value.): "
                )
            ),
            "seconds_interval": int(
                input(
                    "Enter the interval in seconds for scheduling, set to 0 if you don't want the script to repeat: "
                )
            ),
            "manual_playlists": input("Enter manual playlists (True/False): "),
        }

        # Config for SpotifyService
        spotify_config = {
            "client_id": input("Enter Spotify client ID: "),
            "api_key": input("Enter Spotify API key: "),
        }
        write_config("spotify", spotify_config)

        # Config for PlexService
        plex_config = {
            "url": input("Enter Plex server URL: "),
            "api_key": input("Enter Plex API key: "),
            "replace": input("Replace existing Plex data? (True/False): "),
        }
        write_config("plex", plex_config)

        lidarr_config = {
            "url": input("Enter Lidarr URL: "),
            "api_key": input("Enter Lidarr API Key: "),
        }
        write_config("lidarr", lidarr_config)

        spotiplex_config["first_run"] = "False"
        write_config("spotiplex", spotiplex_config)

        print("Configuration complete!")


def main():
    spotiplex = Spotiplex()
    spotiplex.run()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
