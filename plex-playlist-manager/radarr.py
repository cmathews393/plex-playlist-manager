import requests
from decouple import config
import json
from plexapi.collection import Collection as col
import urllib3
from plexapi.server import PlexServer


class RadarrAPI:
    def __init__(self):
        self.RADARR_IP = "http://192.168.1.160:7878"
        self.RADARR_TOKEN = "2e842c75b67d46a7bd234bbbd3f66568"
        self.RADARR_ENDPOINT = config("RADARR_ENDPOINT", default="/api/v3/")
        self.headers = {"X-Api-Key": self.RADARR_TOKEN}
        self.base_url = f"{self.RADARR_IP}{self.RADARR_ENDPOINT}"

    def make_request(self, endpoint_path=""):
        full_url = self.base_url + endpoint_path
        response = requests.get(full_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            with open("data_file.json", "w") as file:
                json.dump(data, file, indent=4)
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None


def connect_plex():
    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )  # Plex API hates SSL or something idk it was annoying
    session = requests.Session()  # Open session
    session.verify = False  # Ignore SSL errors
    PLEX_SERVER_URL = config("PLEX_URL")
    PLEX_SERVER_TOKEN = config("PLEX_TOKEN")
    return PlexServer(PLEX_SERVER_URL, PLEX_SERVER_TOKEN, session=session)


# Usage
radarr_api = RadarrAPI()
# response = radarr_api.make_request('importlist')
tagslist = radarr_api.make_request("tag")
plex = connect_plex()


def get_radarr_tags(radarr_api):
    tagslist = radarr_api.make_request("tag")
    return tagslist


def get_collectionid(taglist):
    collection_id = taglist["id"]
    collection_name = taglist["label"]
    return collection_id, collection_name


def get_movie_ids(id, radarr_api):
    idlist = radarr_api.make_request(f"tag/detail/{id}")
    movie_ids = idlist["movieIds"]
    return movie_ids


def run_everything(user, plex, taglists, radarr_api):
    for tag in taglists:
        moviesforplex = {}
        colid, colname = get_collectionid(tag)
        radarr_ids = get_movie_ids(colid, radarr_api)
        for movie_id in radarr_ids:
            # Step 5: Get movie details
            movies_response = radarr_api.make_request(f"movie/{movie_id}")
            if isinstance(movies_response, list):
                for movie in movies_response:
                    # Step 6: Extract and print the title
                    movie_title = movie["title"]
                    moviesforplex.append(movie_title)
            else:
                # Single movie case
                movie_title = movies_response["title"]
                moviesforplex.append(movie_title)
                try:
                    movieyear = movies_response["year"]
                    if movies_response["year"]:
                        movieyears.append()
                except:
                    continue
        movies = plex.library.section("Movies")
        for movie in moviesforplex:
            movieinplex = movies.search(title=movie)
            print(movie, movieinplex)


tagslist = get_radarr_tags(radarr_api)
run_everything(user=None, plex=plex, taglists=tagslist, radarr_api=radarr_api)


# for collection in radarrimportlists:
#     collection_name = collection['label']
#     collection_id = collection['id']

#     # Step 3: Get collection details
#     collection_details = radarr_api.make_request(f'tag/detail/{collection_id}')

#     # Step 4: Extract movie IDs
#     movie_ids = collection_details['movieIds']

#     for movie_id in movie_ids:
#         # Step 5: Get movie details
#         movies_response = radarr_api.make_request(f'movie/{movie_id}')

#         # Check if the response is a list and iterate
#         if isinstance(movies_response, list):
#             plexcollection = []

#             for movie in movies_response:
#                 # Step 6: Extract and print the title
#                 movie_title = movie['title']
#                 print(movie_title)
#         else:
#             # Single movie case
#             movie_title = movies_response['title']
#             print(movie_title)

# def checkMoviesInPlex(ple):


# for item in radarrimportlists:
#     collectionname = item['label']
#     print(collectionname)
#     collectionid = item['id']
#     print(collectionid)
#     collectionitems = radarr_api.make_request(f'tag/detail/{collectionid}')
#     print(collectionitems)
#     for id in collectionitems['movieIds']:
#         print(id)
#         itemnames = radarr_api.make_request(f'movie/{id}')
#         for item in itemnames:
#             title = item['title']
#             print(title)
# for item in itemnames:

# movies = []
# movietitle = item['title']
# print(movietitle)
# print(movies)
# movie_ids_by_tag = {}
# for item in radarrimportlists:
#     tag = item['label']
#     movie_ids_by_tag[tag] = item['movieIds']

# print(movie_ids_by_tag)

# for key, value in movie_ids_by_tag.items():
#     print(f"{key}: {value}")
