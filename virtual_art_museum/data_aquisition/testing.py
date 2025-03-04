import os # standard library
import requests
import random
import time
import asyncio
import aiohttp

import pandas as pd # third party
from tabulate import tabulate
from tqdm import tqdm
import numpy as np

# if local files needed put here

class MetMuseum: # total objects: 484,956
    """
    Initialize the MetMuseum class
    Params: file_path - str path to the csv file containing the metadata
    """

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path, dtype='str') # read in csv file
        self.fields = self.df.columns # get all fields in the dataframe
        
    # def show_fields(self):
    #     """
    #     Print all fields in the dataframe
    #     """
    #     fields_list = list(self.df.columns)
    #     table = []
    #     for i in range(0, len(fields_list), 6):
    #         fields = fields_list[i:i+6]
    #         table.append(fields)
    #     print(tabulate(table, tablefmt='grid'))
    #     return None

    async def fetch_img(self, session:aiohttp.ClientSession, url:str) -> str | bool:
        try:
            async with session.get(url) as response:
                if response.status == 200:  # successful request
                    data = await response.json()
                    if 'primaryImage' in data and data['primaryImage']:
                        return data['primaryImage']
                    else:
                        return False
                else:
                    return False
        except Exception as e:
            return False

    async def _bound_fetch(self, semaphore: asyncio.Semaphore, session: aiohttp.ClientSession, url: str) -> str | bool:
        async with semaphore:
            return await self.fetch_img(session, url)

    async def _run(self):
        all_ids = self.df['Object ID'].tolist()
        tasks, valid_ids = [], []
        max_requests = 1000
        semaphore = asyncio.Semaphore(max_requests)
        url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
        
        # Create client session that will ensure 1 connection per request
        async with aiohttp.ClientSession() as session:
            for obj_id in all_ids:
                request_url = f"{url}/{obj_id}"
                task = asyncio.ensure_future(self.bound_fetch(semaphore, session, request_url))
                tasks.append((obj_id, task))

            print(f"All {len(tasks)} tasks created. Waiting for responses...")
            # tracking task completion
            responses = [await f for f in tqdm(asyncio.as_completed([t for _, t in tasks]), total=len(tasks))]
            valid_ids = [obj_id for obj_id, task in tasks if task.result() != False]
        
        print(f"Found {len(valid_ids)} objects with valid images ({len(valid_ids)/len(all_ids)*100:.1f}%)")
        filtered_df = self.df[self.df['Object ID'].isin(valid_ids)]
        return filtered_df
        
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
    met = MetMuseum('MetObjects_unfiltered.txt')
    final_df = asyncio.run(met.run())
    final_df.to_csv('MetObjects_filtered_II.csv', index=False)
    print(f"Original shape: {met.df.shape}")
    print(f"Filtered shape: {final_df.shape}")


if __name__ == "__main__":
    main()
