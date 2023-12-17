import requests
from config_handler import read_config


class SONARRAPI:
    def __init__(self):
        self.SONARR_CONFIG = read_config("sonarr")
        self.SONARR_IP = self.SONARR_CONFIG.get("url")
        self.SONARR_TOKEN = self.SONARR_CONFIG.get("apikey")
        self.SONARR_ENDPOINT = "/api/v3/"
        self.headers = {"X-Api-Key": self.SONARR_TOKEN}
        self.base_url = f"{self.SONARR_IP}{self.SONARR_ENDPOINT}"

    def make_request(self, endpoint_path=""):
        full_url = self.base_url + endpoint_path
        response = requests.get(full_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

        print(self.SONARR_IP)


request = SONARRAPI()
SONARRAPI.make_request(request)