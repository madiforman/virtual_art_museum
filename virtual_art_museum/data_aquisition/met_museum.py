"""
This module

References:
    https://realpython.com/python-concurrency/
    https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

"""
import os # standard library
import random
import time
import asyncio
import aiohttp
from collections import Counter

import requests
import pandas as pd # third party
from tqdm import tqdm
import matplotlib.pyplot as plt
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
    
    def fetch_img(self, object_id):
        url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'primaryImage' in data and data['primaryImage']:
                    return data['primaryImage']
                else:
                    return False
        except Exception as e:
            return False

    async def _async_fetch_img(self, session:aiohttp.ClientSession, url:str) -> str | bool:
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
            return await self._async_fetch_img(session, url)

    async def _run(self):
        all_ids = self.df['Object ID'].tolist()
        tasks = []
        max_requests = 1000
        semaphore = asyncio.Semaphore(max_requests)
        url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
        
        # Create client session that will ensure 1 connection per request
        async with aiohttp.ClientSession() as session:
            for obj_id in all_ids:
                request_url = f"{url}/{obj_id}"
                task = asyncio.ensure_future(self._bound_fetch(semaphore, session, request_url))
                tasks.append((obj_id, task))
            print(f"All {len(tasks)} tasks created. Waiting for responses...")

            for obj_id, task in tqdm(tasks, total=len(tasks)):
                await task
            image_url_dict = {obj_id: task.result() for obj_id, task in tasks if task.result() != False}
            valid_ids = list(image_url_dict.keys())
        print(f"Found {len(valid_ids)} objects with valid images ({len(valid_ids)/len(all_ids)*100:.1f}%)")

        filtered_df = self.df[self.df['Object ID'].isin(valid_ids)].copy()
        filtered_df['image_url'] = filtered_df['Object ID'].map(image_url_dict)
        print(f"Original dataframe shape: {self.df.shape}")
        print(f"Filtered dataframe shape: {filtered_df.shape}")
        return filtered_df
        
    def get_n_random_objs(self, n):
        """
        Get n random objects from dataframe
        Params: n - int number of objects to get
        Returns: list of metadata for the objects
        """
        objs = self.df.sample(n)
        # data = [self.get_metadata(id) for id in objs['Object ID']]
        return objs

    def get_metadata(self, object_id):
        """
        Get metadata for a given object id; this was written before saving the image urls to a csv file.
        May become deprecated in the future. (unnecessary if we're not making api calls)
        Params: object_id - str id of the object to get metadata for
        Returns: metadata for the object
        """
        row = self.df.loc[self.df['Object ID'] == object_id].to_dict(orient='records')
        url = self.fetch_img(object_id)
        if url:
            metadata = {
                'object_id': row[0]['Object ID'],
                'title': row[0]['Title'],
                'artist': row[0]['Artist Display Name'],
                'department': row[0]['Department'],
                'medium': row[0]['Medium'],
                'artist bio': row[0]['Artist Display Bio'],
                'region': row[0]['Region'],
                'date': row[0]['Object Date'],
                'image_url': url
            }
            return metadata
        else: 
            raise ValueError(f"Object ID {object_id} has no image")

    # def clean_cultures(self):
    #     # Get culture counts, excluding null values
    #     culture_counts = self.df['Culture'].value_counts()
    #     top_cultures = culture_counts.head(20)

    #     plt.figure(figsize=(15, 8))
    #     bars = plt.bar(range(len(top_cultures)), top_cultures.values)
    #     plt.xticks(range(len(top_cultures)), top_cultures.index, rotation=45, ha='right')
        
    #     for bar in bars:
    #         height = bar.get_height()
    #         plt.text(bar.get_x() + bar.get_width()/2., height,
    #                 f'{int(height):,}',
    #                 ha='center', va='bottom')
            
    #     plt.title('20 Most Common Cultures in Met Museum Collection')
    #     plt.xlabel('Culture')
    #     plt.ylabel('Number of Objects')
    #     plt.tight_layout()
    #     plt.figure(figsize=(10, 6))
    #     plt.hist(culture_counts)
    #     plt.show()
        
def main():
    met = MetMuseum('MetObjects_final.csv')
    # print(met.df.columns)
    # cultures = met.df['Culture'].unique()
    # for c in cultures:
    #     print(c)

    #met.clean_cultures()

if __name__ == "__main__":
    main()
