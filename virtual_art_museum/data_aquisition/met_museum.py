import requests
import random
from piece import Piece

class MetMuseum:
    def __init__(self, url):
        self.url = url
        self.deparments = self.get_all_departments()
        self.all_ids = self.get_all_object_ids()

    def create_piece(self, object_id):
        response = requests.get(f"{self.url}objects/{object_id}")
        if self.check_status(response):
            return Piece(object_id, response.json())

    def get_objects_by_query(self, query):
        response = requests.get(f"{self.url}search?hasImages=true&q={query}")
        if self.check_status(response):
            ids = response.json()['objectIDs']
            pieces = [self.create_piece(id) for id in ids]
        else:
            return []

    def get_N_random_objects(self, N):
        pieces = [self.create_piece(id) for id in random.sample(self.all_ids, N) if self.create_piece(id) is not None]
        return pieces

    def get_all_object_ids(self): #probably wont use this -> it will take forever to get all the objects
        response = requests.get(f"{self.url}objects")
        if self.check_status(response):
            object_ids = response.json()['objectIDs']
            return object_ids
        
    def get_all_objects_in_department(self, department_id):
        response = requests.get(f"{self.url}objects?departmentIds={department_id}")
        if self.check_status(response):
            all_objects = list(response.json()['objectIDs'])
            pieces = [self.create_piece(id) for id in all_objects[:1]]
            return pieces

    def get_all_departments(self):
        response = requests.get(f"{self.url}departments")
        dict = {}
        if self.check_status(response):
            for item in response.json()['departments']:
                dict[item['departmentId']] = item['displayName']
            return dict

    def check_status(self, response):
        if response.status_code == 200:
            return True
        else:
            print(f"Error getting {response.url}", response.status_code)
            return False

def main():
    met = MetMuseum("https://collectionapi.metmuseum.org/public/collection/v1/")
    print(met.get_objects_by_query("sunflowers"))

if __name__ == "__main__":
    main()