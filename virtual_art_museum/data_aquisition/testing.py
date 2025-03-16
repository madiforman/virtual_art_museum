import streamlit as st
import requests

import asyncio
import aiohttp

import requests
import pandas as pd 
from tqdm import tqdm
import numpy as np


st.image('https://www.dropbox.com/s/u2xvcw1ev2pt32c/DK_Slott%20Moeller_Sankt%20Hans%20Aften_VejleMuseerne.jpg?raw=1')
# def check_europeana_response(url: str, content: bytes) -> str:
#     if url.startswith('https://www.dropbox.com'):
#         if check_dropbox_content(content):
#             return url
#         else:
#             return ""
#     else:
#         return url
    
# async def fetch(session:aiohttp.ClientSession, url:str, flag:str) -> str:
#     try:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 if flag == "MET":
#                     data = await response.json()
#                     return check_met_response(data)
#                 elif flag == "EUROPEANA":
#                     first_bytes = await response.content.read(10)
#                     return check_europeana_response(url, first_bytes)
#             return ""
#     except Exception as e:
#         return ""

# async def bound_fetch(
#                     semaphore: asyncio.Semaphore, 
#                     session: aiohttp.ClientSession, 
#                     url: str, 
#                     flag: str):

#     async with semaphore:
#         return await fetch(session, url, flag)

# async def run(df, flag: str):
#     url_dict = {}
#     if flag == "MET":
#         base_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
#         url_dict = {f"{base_url}/{obj_id}": obj_id for obj_id in df['Object ID'].tolist()}
#     elif flag == "EUROPEANA":
#         url_dict = {url: id for url, id in zip(df['image_url'], df['europeana_id'])}
#     else:
#         raise ValueError(f"Invalid source given: {flag}. Must be either MET or EUROPEANA")

#     tasks = []
#     max_requests = 1000
#     semaphore = asyncio.Semaphore(max_requests)

#     async with aiohttp.ClientSession() as session:
#         for url in url_dict.keys():
#             task = asyncio.ensure_future(bound_fetch(semaphore, session, url, flag))
#             tasks.append((url, task))

#         print(f"All {len(tasks)} tasks created, waiting for responses...")

#         for url, task in tqdm(tasks, total=len(tasks)):
#             await task

#         valid_dictionary = {url_dict[url]: task.result() for url, task in tasks if task.result() != ""}
#         filtered_df = df[df['europeana_id'].isin(valid_dictionary.keys())].copy()
#         print(f"Original shape: {df.shape}")
#         print(f"Filtered shape: {filtered_df.shape}")

#     return filtered_df

# def filter_images(df, flag: str):
#     return asyncio.run(run(df, flag))


# def main():
#     url_bad = 'https://www.dropbox.com/s/bqyj46qv6izr43q/Mainie%20Jellett%2C%20Four%20Element%20Composition.jpg?raw=1'
#     url_good = 'https://www.dropbox.com/s/69i4lf5jxw5sj7f/DK_Zahrtmann_Det%20Mystiske%20Bryllup%20i%20Pistoia_Bornholms%20Kunstmuseum.jpg?raw=1'

#     toy_df = pd.DataFrame({'image_url': [url_bad, url_good], 'europeana_id': [1, 2]})
#     toy_df = filter_images(toy_df, "EUROPEANA")
#     print(toy_df)


# if __name__ == "__main__":
#     main()
