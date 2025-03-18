"""
===============================================
Europeana - Data Acquisition
===============================================

This module contains the code for acquiring data from the Europeana API.
This API contains so much rich and complex data that it is out of the scope
of this project to handle all of it. In order to approach this, we created a list
of common "art terms" to query this data base for. This is found in the 
directory: data/query_terms.csv
We query all these terms and save as much data back as possible. In the future,
we would love to add to this dataset.
Number of unique objects in resultultu
eul
Classes
----------
    Europeana
References
----------
    
Authors
----------
    Madison Sanchez-Forman and Mya Strayer
"""
import math
import requests
import random
import re
import asyncio
import aiohttp
import os

# from dotenv import load_dotenv

import pyeuropeana.utils as utils
import pyeuropeana.apis as apis
import pandas as pd
from tqdm import tqdm

from .async_utils import filter_images
from .common_functions import print_example_rows, century_mapping

class Europeana:
    """
    Class docstring.

    Attributes:
        df (pd.DataFrame): [description]
    """
    def __init__(self, file_path: str):
        self.df = pd.DataFrame()
        if file_path == "":
            self.df = self.create_final(path="", save_final=False)
        else:
           self.df = pd.read_csv(file_path, dtype='str')

    def get_n_random_objs(self, n=10):
        return self.df.sample(n)
    
    def bulk_requests(self):
        """
        Function docstring.

        Returns:
            pd.DataFrame: [description]
        """
        query_terms = pd.read_csv('../data/query_terms.csv', header=None)
        query_terms = set(query_terms.iloc[:, 0].tolist())
        df_list = []
        for query in query_terms:
            cursor = '*'  # Initial cursor value
            total_results = 0
            max_results = 500 # Set a maximum number of results per query
            
            while cursor and total_results < max_results: 
                response = apis.search(
                    query=query,
                    reusability = 'open AND permission', # ensure rights to use the data
                    cursor=cursor, # pass the cursor to the next page
                    qf='LANGUAGE:en AND TYPE:IMAGE', 
                    rows=max_results  # Maximum allowed per request
                )
                if not response.get('items'): # if no results, break
                    break

                df_new = utils.search2df(response)
                self.df = pd.concat([self.df, df_new], ignore_index=True)

                cursor = response.get('nextCursor') # move the pointer
                total_results += len(response.get('items', []))
                print(f"Fetched {total_results} results for query: {query}")

        self.df = self.df.dropna(subset=['image_url'])
        self.df = self.df.drop_duplicates(subset=['image_url'])
        self.df = filter_images(self.df, flag="EUROPEANA")

        print(f"Found {len(self.df)} valid image urls")
        return self.df

    def _extract_year(self, row:pd.Series):
        """
        Function docstring.

        Args:
            row (pd.Series): [description]

        Returns:
            int: [description]
        """
        date_pattern = r'\d{4}' # regex pattern YYYY
        match_description = re.search(date_pattern, str(row['description']))
        match_title = re.search(date_pattern, str(row['title']))
        match_creator = re.search(date_pattern, str(row['creator']))

        if match_description:
            date = match_description.group()
        elif match_title:   
            date = match_title.group()
        elif match_creator:
            date = match_creator.group()
        else:
            return -1
        return date

    def _create_year_column(self):
        """
        Function docstring.

        Returns:
            pd.DataFrame: [description]
        """
        date_pattern = r'\d{4}(-\d{4})?' # regex pattern YYYY or YYYY-YYYY
        self.df['year'] = self.df.apply(self._extract_year, axis=1).astype(int)
        return self.df

    def process_data(self):
        """
        Function docstring.

        Returns:
            pd.DataFrame: [description]
        """
        # Fill missing values with 'Unknown'
        self.df.fillna('Unknown', inplace=True)

        # Keep relevant columns
        cols_to_keep = ['europeana_id', 'image_url', 
                        'title', 'creator', 
                        'description', 'country', 'provider']
        self.df = self.df[cols_to_keep]

        # Create year column
        self.df = self._create_year_column()

        # Add repository column
        self.df['repository'] = 'EUROPEANA'

        # Create Century column
        self.df['Century'] = self.df['year'].apply(century_mapping)
        self.df = self.df.replace(-1, "Unknown")
        return self.df

    def create_final(self, path, save_final=False):
        """
        Function docstring.

        Args:
            path (str): [description]
            save_final (bool, optional): [description]. Defaults to False.

        Returns:
            None
        """
        self.df = self.bulk_requests()
        self.df = self.process_data()
        if save_final:
            self.df.to_csv(path, index=False)
        print_example_rows(self.df, n=5)
        return self.df

def main():
    access_key = os.getenv('API_KEY')
    # os.environ['EUROPEANA_API_KEY'] = access_key
    europeana = Europeana(file_path='')

if __name__ == "__main__":
    main()

