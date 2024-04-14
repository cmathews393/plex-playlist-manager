import json
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
            with open("data_file.json", "w") as file:
                json.dump(data, file, indent=4)
            return data
        except:
            print("Error during request:")
            return None

    def get_radarr_tags(self):
        
        endpoint = "/api/v3/tag/detail"
        result = self.make_request(endpoint)
        user_movies = {}
        for entry in result:
            username = entry['label']
            movie_ids = entry['movieIds']
            user_movies[username] = movie_ids
        return user_movies
    
    def get_movie_titles(self, id):
        endpoint = f"/api/v3/movie/{id}"
        result = self.make_request(endpoint)
        movie_name = result['title']
        return movie_name
