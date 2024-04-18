import json
import sqlite3
from .confighandler import read_config
import httpx
# test


class RadarrAPI:
    def __init__(self):
        self.config = read_config("radarr")
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
        except:
            print("Error during request:")
            return None

    def get_radarr_tags(self):
        endpoint = "/api/v3/tag/detail"
        result = self.make_request(endpoint)
        user_movies = {}
        for entry in result:
            username = entry["label"]
            movie_ids = entry["movieIds"]
            user_movies[username] = movie_ids
        return user_movies

    def get_movie_titles(self, movie_id: int) -> str:
        """Retrieve movie title from local DB or API if not found."""
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT)"
        )
        conn.commit()

        # Check if the movie is already in the database
        cursor.execute("SELECT title FROM movies WHERE id = ?", (movie_id,))
        result = cursor.fetchone()

        if result:
            title = result[0]
        else:
            # Make the API request if movie not found in DB
            endpoint = f"/api/v3/movie/{movie_id}"
            api_result = self.make_request(endpoint)
            title = api_result["title"]

            # Insert the new movie title into the database
            cursor.execute(
                "INSERT INTO movies (id, title) VALUES (?, ?)", (movie_id, title)
            )
            conn.commit()

        cursor.close()
        conn.close()
        return title
