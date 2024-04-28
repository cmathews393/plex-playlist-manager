import sqlite3

import httpx

from plexplaylistmanager.modules.confighandler.main import read_config


class SonarrAPI:
    def __init__(self):
        self.config = read_config("sonarr")
        self.base_url = self.config.get("url")
        self.api_key = self.config.get("api_key")
        self.headers = {"X-Api-Key": self.api_key}

    def make_request(self, endpoint_path=""):
        full_url = self.base_url + endpoint_path
        try:
            response = httpx.get(full_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print(f"Error during request: {e}")
            return None

    def get_sonarr_tags(self):
        endpoint = "/api/v3/tag/detail"
        result = self.make_request(endpoint)
        user_shows = {}
        if result:
            for entry in result:
                username = entry["label"]
                show_ids = entry["seriesIds"]  # In Sonarr, it's seriesIds not movieIds
                user_shows[username] = show_ids
        return user_shows

    def get_show_titles(self, show_id: int) -> str:
        """Retrieve show title from local DB or API if not found."""
        conn = sqlite3.connect("ppm.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS shows (id INTEGER PRIMARY KEY, title TEXT)",
        )
        conn.commit()

        # Check if the show is already in the database
        cursor.execute("SELECT title FROM shows WHERE id = ?", (show_id,))
        result = cursor.fetchone()

        if result:
            title = result[0]
        else:
            # Make the API request if show not found in DB
            endpoint = f"/api/v3/series/{show_id}"
            api_result = self.make_request(endpoint)
            title = api_result.get("title", "Unknown Show")

            # Insert the new show title into the database
            cursor.execute(
                "INSERT INTO shows (id, title) VALUES (?, ?)",
                (show_id, title),
            )
            conn.commit()

        cursor.close()
        conn.close()
        return title
