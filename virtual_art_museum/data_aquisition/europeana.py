import requests
import random
from piece import Piece
#'https://api.europeana.eu/api/v2/search.json?reusability=open&qf=TYPE:IMAGE&query='+query+'&wskey='+key)
class Europeana:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def get_N_random_objects(self, N):
        pass


def main():
    api_key = "etendinfi"
    url = f"https://api.europeana.eu/api/v2/search.json?reusability=open&qf=TYPE:IMAGE&"
    params = {
        "wskey": api_key,
        "query": "mona lisa",
        "qf": "TYPE:IMAGE",
        "reusability": "open"
    }
    response = requests.get(url, params=params)
    # print(response.json()['items'])
    for item in response.json()['items']:
        print(item)
        break
    # print(response.json()['items'][0]['edmIsShownBy'])
    # for item in response.json()['items']:
    #     print(item['edmIsShownBy'])
if __name__ == "__main__":
    main()