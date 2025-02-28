import os # standard library
import requests
import random

import pandas as pd # third party
from tabulate import tabulate
import numpy as np

# if local files needed put here

class MetMuseum:
    """
    Initialize the MetMuseum class
    Params: file_path - str path to the csv file containing the metadata
    """

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path, dtype='str') # read in csv file
        self.fields = self.df.columns # get all fields in the dataframe
        self.departments = self.get_all_departments() # get all departments in the dataframe

    def show_fields(self):
        """
        Print all fields in the dataframe
        """
        fields_list = list(self.df.columns)
        table = []
        for i in range(0, len(fields_list), 6):
            fields = fields_list[i:i+6]
            table.append(fields)
        print(tabulate(table, tablefmt='grid'))
        return None

    def request_image_url(self, object_id):
        """
        Request image url for a given object id
        Params: object_id - str id of the object to request url for
        Returns: 
            False - returns False if either the request fails or the object has no image
            url - link to image if it exists, False otherwise
        """
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
        response = requests.get(url)

        if response.status_code == 200: # successful request
            data = response.json()
            if 'primaryImage' in data and data['primaryImage']: # primary image is main display image
                return data['primaryImage']
            else:
                return False
        else:
            print(f"Error getting {response.url}", response.status_code) # print response error
            return False

    def _remove_objects_without_image(self): #underscore means private; no need to run this ever again
        """
        Remove objects without image from dataframe; will only be ran once at the beginning
        Once all objects have been removed -> write to new csv file
        """
        all_ids = self.df['Object ID'] # get all object ids

        print("Beginning removal...")
        for id in all_ids:
            if not self.request_image_url(id): # make request for each object
                self.df.drop(self.df.loc[self.df['Object ID'] == id].index, inplace=True)

        self.df.to_csv('MetObjects_Final.csv', index=True)
        print(f"Finished removal. Final length of df: {len(self.df)}")
        return None

    def get_n_random_objects(self, n):
        """
        Get n random objects from dataframe
        Params: n - int number of objects to get
        Returns: list of metadata for the objects
        """
        objs = self.df.sample(n)
        data = [self.get_metadata(id) for id in objs['Object ID']]
        return data

    def get_metadata(self, object_id):
        """
        Get metadata for a given object id
        Params: object_id - str id of the object to get metadata for
        Returns: metadata for the object
        """
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
        """ 
        Returns all object ids for objects in a given department
        Params: 
        """
        objs = self.df[self.df['Department'] == department_id]
        data = [self.get_metadata(obj['Object ID']) for _, obj in objs.iterrows()]
        return data

    def get_all_departments(self):
        return self.df['Department'].unique()


def main():
    print("Starting to remove...")
    met = MetMuseum('MetObjects.txt')
    met.remove_objects_without_image()
    print("Done removing")

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
