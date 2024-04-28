import sqlite3

import httpx

from plexplaylistmanager.modules.confighandler.main import read_config


class LidarrAPI:
    """Handle interactions with the Lidarr API to manage music libraries."""

    def __init__(self):
        self.config = read_config("lidarr")
        self.base_url = self.config.get("url")
        self.api_key = self.config.get("api_key")
        self.headers = {"X-Api-Key": self.api_key}

    def make_request(self, endpoint_path=""):
        """Make an HTTP request to the specified Lidarr API endpoint."""
        full_url = self.base_url + endpoint_path
        try:
            response = httpx.get(full_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print(f"Error during request: {e}")
            return None

    def get_lidarr_tags(self):
        """Retrieve all tags with associated artist IDs from Lidarr."""
        endpoint = "/api/v1/tag/detail"
        result = self.make_request(endpoint)
        user_artists = {}
        if result:
            for entry in result:
                username = entry["label"]
                artist_ids = entry[
                    "artistIds"
                ]  # In Lidarr, it's artistIds not seriesIds
                user_artists[username] = artist_ids
        return user_artists

    def get_artist_name(self, artist_id: int) -> str:
        """Retrieve artist name from local DB or API if not found."""
        conn = sqlite3.connect("ppm.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS artists (id INTEGER PRIMARY KEY, name TEXT)",
        )
        conn.commit()

        # Check if the artist is already in the database
        cursor.execute("SELECT name FROM artists WHERE id = ?", (artist_id,))
        result = cursor.fetchone()

        if result:
            name = result[0]
        else:
            # Make the API request if artist not found in DB
            endpoint = f"/api/v1/artist/{artist_id}"
            api_result = self.make_request(endpoint)
            name = api_result.get("artistName", "Unknown Artist")

            # Insert the new artist name into the database
            cursor.execute(
                "INSERT INTO artists (id, name) VALUES (?, ?)",
                (artist_id, name),
            )
            conn.commit()

        cursor.close()
        conn.close()
        return name
