import requests
import random
import pandas as pd
import os
from tabulate import tabulate
class MetMuseum:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path, dtype='str')
        self.fields = self.df.columns
        self.departments = self.get_all_departments()
        self.ids_without_image = []

    def show_fields(self):
        fields_list = list(self.df.columns)
        table = []
        for i in range(0, len(fields_list), 6):
            fields = fields_list[i:i+6]
            table.append(fields)
        print(tabulate(table, tablefmt='grid'))
        return

    def request_image_url(self, object_id):
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'primaryImage' in data and data['primaryImage']:
                return data['primaryImage']
            else:
                self.ids_without_image.append(object_id)
                return False
        else:
            print(f"Error getting {response.url}", response.status_code)
            return False

    def get_n_random_objects(self, n):
        objs = self.df.sample(n)
        data = [self.get_metadata(id) for id in objs['Object ID']]
        return data

    def get_metadata(self, object_id):
        if object_id not in self.ids_without_image:
            row = self.df.loc[self.df['Object ID'] == object_id].to_dict(orient='records')
            url = self.request_image_url(object_id)
            if url:
                metadata = {
                    'object_id': row[0]['Object ID'],
                    'title': row[0]['Title'],
                    'artist': row[0]['Artist Display Name'],
                    'department': row[0]['Department'],
                    'medium': row[0]['Medium'],
                    'artist bio': row[0]['Artist Display Bio'],
                    'region': row[0]['Region'],
                    'image_url': url
                }
                return metadata
        else: 
            raise ValueError(f"Object ID {object_id} has no image")

    def get_all_objects_in_department(self, department_id):
        objs = self.df[self.df['Department'] == department_id]
        data = [self.get_metadata(obj['Object ID']) for _, obj in objs.iterrows()]
        return data

    def get_all_departments(self):
        return self.df['Department'].unique()


def main():
    met = MetMuseum('MetObjects.txt')
    data = met.get_n_random_objects(3)
    print(data)
if __name__ == "__main__":
    main()







    #def get_n_random_objects(self, n):
    #     objs = self.df.sample(n)
    #     print(objs)
    #     data = [self.get_metadata(obj['Object Number']) for _, obj in objs.iterrows()]
    #     return data
    # def create_piece(self, object_id):
    #     response = requests.get(f"{self.url}objects/{object_id}")
    #     if self.check_status(response):
    #         return Piece(object_id, response.json())

    # def get_objects_by_query(self, query):
    #     response = requests.get(f"{self.url}search?hasImages=true&q={query}")
    #     if self.check_status(response):
    #         ids = response.json()['objectIDs']
    #         pieces = [self.create_piece(id) for id in ids]
    #     else:
    #         return []
