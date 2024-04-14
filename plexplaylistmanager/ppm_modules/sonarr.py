import json
import httpx
from confighandler import read_config

class SonarrAPI:
    def __init__(self):
        self.config = read_config("sonarr")
        self.base_url = self.config.get("url")
        self.api_key = self.config.get("apikey")
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
        except Exception as e:
            print(f"Error during request: {e}")
            return None

    def get_sonarr_tags(self):
        endpoint = "/api/v3/tag/detail"
        result = self.make_request(endpoint)
        user_shows = {}
        if result:
            for entry in result:
                username = entry['label']
                show_ids = entry['seriesIds']  # In Sonarr, it's seriesIds not movieIds
                user_shows[username] = show_ids
        return user_shows
    
    def get_show_titles(self, id):
        endpoint = f"/api/v3/series/{id}"  # In Sonarr, it's series not movie
        result = self.make_request(endpoint)
        if result:
            show_name = result.get('title', 'Unknown Show')
            return show_name
        return "Unknown Show"  # Return a default name if the show is not found

