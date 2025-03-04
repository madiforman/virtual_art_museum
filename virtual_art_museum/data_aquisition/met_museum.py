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
            return await self.async_fetch_img(session, url)

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
    met = MetMuseum('MetObjects_filtered_II.csv')
    print(met.df.columns)
    # final_df = asyncio.run(met.run())
    # final_df.to_csv('MetObjects_filtered_II.csv', index=False)
    # print(f"Original shape: {met.df.shape}")
    # print(f"Filtered shape: {final_df.shape}")


if __name__ == "__main__":
    main()



# class MetMuseum: # total objects: 484,956
#     """
#     Initialize the MetMuseum class
#     Params: file_path - str path to the csv file containing the metadata
#     """

#     def __init__(self, file_path):
#         self.df = pd.read_csv(file_path, dtype='str') # read in csv file
#         self.fields = self.df.columns # get all fields in the dataframe
        
#     def show_fields(self):
#         """
#         Print all fields in the dataframe
#         """
#         fields_list = list(self.df.columns)
#         table = []
#         for i in range(0, len(fields_list), 6):
#             fields = fields_list[i:i+6]
#             table.append(fields)
#         print(tabulate(table, tablefmt='grid'))
#         return None

#     async def request_img_async(self, session:aiohttp.ClientSession, object_id:int) -> str | bool:
#         url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
#         try:
#             async with session.get(url) as response:
#                 if response.status == 200:  # successful request
#                     data = await response.json()
#                     if 'primaryImage' in data and data['primaryImage']:  # primary image is main display image -> check if it exists
#                         return data['primaryImage']
#         except Exception as e:
#             return False  # Silently handle errors during batch processing
#         return False


#     async def _filter_objects_async(self, session:aiohttp.ClientSession, object_ids:list) -> pd.DataFrame:
#         valid_ids = []
#         tasks = []
#         for obj_id in object_ids: # each object id is a task
#             task = self.request_image_async(session, obj_id)
#             tasks.append((obj_id, task))
        
#         processing_size = 100    # this is how many API requests are made concurrently before awaiting their results
#         for i in range(0, len(tasks), processing_size):
#             chunk = tasks[i:i+processing_size] # chunk up the tasks
            
#             for obj_id, task in chunk: # wait for batch to complete
#                 image_url = await task
#                 if image_url != False:  # If image exists
#                     valid_ids.append(obj_id)

#         return self.df[self.df['Object ID'].isin(valid_ids)] # filter valid ids

#     async def run(self):
#         total_requests = len(self.df)
#         url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/"
#         all_ids = self.df['Object ID'].tolist()

#         tasks = []
#         max_requests = 1000
#         semaphore = asyncio.Semaphore(1000)

#         # create client session that will ensure 1 connection per request
#         async with aiohttp.ClientSession() as session:
#             for obj_id in all_ids:
#                 task = asyncio.ensure_future(self.request_img_async(semaphore, obj_id))
#                 tasks.append(task)

#         # run all tasks concurrently
#         results = await asyncio.gather(*tasks, return_exceptions=True)
#         await results
        



#     async def _async_remove_objects(self, batch_size=1000, concurrent_requests=50) -> pd.DataFrame:
#         all_ids = self.df['Object ID'].tolist()
#         final_df = pd.DataFrame(columns=self.fields)
#         start = time.time()
        
#         # Process in batches to manage memory
#         connector = aiohttp.TCPConnector(limit=concurrent_requests)

#         async with aiohttp.ClientSession(connector=connector) as session:
#             for i in range(0, len(all_ids), batch_size):
#                 batch_ids = all_ids[i:i+batch_size]
#                 print(f"Processing batch {i//batch_size + 1}/{(len(all_ids) + batch_size - 1)//batch_size}")
                
#                 batch_df = await self._filter_objects_async(batch_ids, session)
#                 final_df = pd.concat([final_df, batch_df], ignore_index=True)
                
#                 # Report progress
#                 elapsed = time.time() - start
#                 objects_processed = min(i + batch_size, len(all_ids))
#                 percent_complete = objects_processed / len(all_ids) * 100

#         end = time.time()
#         print(f"Time taken: {end-start:.1f} seconds")
#         print(f"Final dataframe shape: {final_df.shape}")
#         print(f"Final num objects: {len(final_df)}")
        
#         return final_df



#         def get_n_random_objects(self, n):
#             """
#             Get n random objects from dataframe
#             Params: n - int number of objects to get
#             Returns: list of metadata for the objects
#             """
#             objs = self.df.sample(n)
#             data = [self.get_metadata(id) for id in objs['Object ID']]
#             return data

#         def get_metadata(self, object_id):
#             """
#             Get metadata for a given object id
#             Params: object_id - str id of the object to get metadata for
#             Returns: metadata for the object
#             """
#             row = self.df.loc[self.df['Object ID'] == object_id].to_dict(orient='records')
#             url = self.request_image_url(object_id)
#             if url:
#                 metadata = {
#                     'object_id': row[0]['Object ID'],
#                     'title': row[0]['Title'],
#                     'artist': row[0]['Artist Display Name'],
#                     'department': row[0]['Department'],
#                     'medium': row[0]['Medium'],
#                     'artist bio': row[0]['Artist Display Bio'],
#                     'region': row[0]['Region'],
#                     'image_url': url
#                 }
#                 return metadata
#             else: 
#                 raise ValueError(f"Object ID {object_id} has no image")

#     def get_all_objects_in_department(self, department_id):
#         """ 
#         Returns all object ids for objects in a given department
#         Params: 
#         """
#         objs = self.df[self.df['Department'] == department_id]
#         data = [self.get_metadata(obj['Object ID']) for _, obj in objs.iterrows()]
#         return data

#     def get_all_departments(self):
#         return self.df['Department'].unique()

# def main():
#     met = MetMuseum('MetObjects_unfiltered.txt')
#     final_df = asyncio.run(met.async_remove_objects()) # run async function with asyncio.run
#     final_df.to_csv('MetObjects_filtered.csv', index=False)

# if __name__ == "__main__":
#     main()

