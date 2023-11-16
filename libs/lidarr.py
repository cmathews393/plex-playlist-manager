import requests
from decouple import config

class LIDARRAPI:
    def __init__(self):
        self.LIDARR_IP = ("http://192.168.1.160:8989")
        self.LIDARR_TOKEN = ("61ac351f799d472c9a5aea14a3865306")
        self.LIDARR_ENDPOINT = config("LIDARR_ENDPOINT", default="/api/v3/")
        self.headers = {"X-Api-Key": self.LIDARR_TOKEN}
        self.base_url = f"{self.LIDARR_IP}{self.LIDARR_ENDPOINT}"

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
LIDARR_api = LIDARRAPI()
#response = LIDARR_api.make_request('importlist')
LIDARRimportlists = LIDARR_api.make_request('importlist')

print(LIDARRimportlists)