import requests
import random
from piece import Piece
import pandas as pd
import os
from tabulate import tabulate
class MetMuseum:
    def __init__(self):
        self.df = pd.read_csv('MetObjects.txt', dtype='str')
        self.fields = self.df.columns
        self.departments = self.get_all_departments()
        self.table = self.show_fields()

    def show_fields(self):
        table = []
        fields_per_row = 4
        row = []
        
        for i, field in enumerate(self.fields, 1):
            row.append(field)
            if i % fields_per_row == 0:
                table.append(row)
                row = []
    
        # Add any remaining fields
        if row:
            while len(row) < fields_per_row:
                row.append('')
            table.append(row)

        table = tabulate(table, tablefmt='grid')
        return table
    def request_image_url(self, object_id):
        response = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}")
        if self.check_status(response):
            return response.json()['primaryImage']
        else:
            return None

    def get_metadata(self, object_id):
        row = self.df[self.df['Object Number'] == object_id]
        metadata = {
            'object_id': row['Object Number'],
            'title': row['Title'],
            'artist': row['Artist Display Name'],
            'department': row['Department'],
           # 'image_url': self.request_image_url(object_id)
        }
        print(metadata)
        return metadata
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

    # def get_N_random_objects(self, N):
    #     pieces = [self.create_piece(id) for id in random.sample(self.all_ids, N) if self.create_piece(id) is not None]
    #     return pieces

    def get_all_object_ids(self): #probably wont use this -> it will take forever to get all the objects
        return self.df['Object Number'].tolist()

    def get_all_objects_in_department(self, department_id):
        return self.df[self.df['Department'] == department_id]

    def get_all_departments(self):
        return self.df['Department'].unique()

    def check_status(self, response):
        if response.status_code == 200:
            return True
        else:
            print(f"Error getting {response.url}", response.status_code)
            return False

def main():
    met = MetMuseum()
    print(met.df.head())
    # print(met.df['Object Number'])
    print(met.table)
    print(met.get_metadata('43652'))
if __name__ == "__main__":
    main()