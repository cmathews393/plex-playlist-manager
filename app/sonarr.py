import requests
from decouple import config

class SONARRAPI:
    def __init__(self):
        self.SONARR_IP = ("http://192.168.1.160:8989")
        self.SONARR_TOKEN = ("61ac351f799d472c9a5aea14a3865306")
        self.SONARR_ENDPOINT = config("SONARR_ENDPOINT", default="/api/v3/")
        self.headers = {"X-Api-Key": self.SONARR_TOKEN}
        self.base_url = f"{self.SONARR_IP}{self.SONARR_ENDPOINT}"

    def make_request(self, endpoint_path=''):
            full_url = self.base_url + endpoint_path
            response = requests.get(full_url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()   
                return data
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

# Usage
SONARR_api = SONARRAPI()
#response = SONARR_api.make_request('importlist')
SONARRimportlists = SONARR_api.make_request('importlist')

print(SONARRimportlists)