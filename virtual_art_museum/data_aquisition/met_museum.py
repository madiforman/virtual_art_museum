"""
===============================================
Metropolitan Museum of Art - Data Acquisition
===============================================

This module contains the code for acquiring data from the Metropolitan Museum of Art (MET).
We began by downloading the MetObjects.txt file from the MET's github page. In order to
prevent objects without images from being used in our streamlit app, this script queries
the MET API for the associated image url. If none is found, this object is removed from 
our data. Once this has been done for all 48,4956 objects, the data is filtered and
manipulated in order to be used in our app. Finally, the data is saved to a new csv file
so that we do not have to load unnecessary data later on in our app.

Classes
----------
    MetMuseum
References
----------
    https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
Authors
----------
    Madison Sanchez-Forman and Mya Strayer
"""
import os 
import random
import re
import time
import asyncio
import aiohttp

import requests
import pandas as pd 
from tqdm import tqdm
import numpy as np

from .async_utils import filter_images
from .common_functions import print_example_rows, century_mapping


class MetMuseum:
    """
    Class for quereying, manipulating, and saving data from the Metropolitan Museum of Art.

    This class contains the functionality for querying the MET API, cleaning results, and
    saving the finalized version of the originally downloaded data. 

    Parameters
    ----------
    file_path : str
        path to met objects file. Can either be the unfiltered or filtered version.
    is_test : bool, optional
        if true, only the first 250 objects will be used. will be used in test cases.

    Attributes
    ----------
    df : pd.DataFrame
        dataframe of met objects.
    """

    def __init__(self, file_path, is_test=False):
        """ Initalizes class with given file path and optional test flag """
        self.df = pd.read_csv(file_path, dtype='str')
        if is_test:
            self.df = self.df[:100]

    def _request_image_urls(self):
        """
        Requests image urls from the MET API. This calls the async_utils.py file to
        process the data as efficiently as possible.

        Returns
        -------
        pd.DataFrame
            dataframe of met objects with new image urls if they exist
        """
        self.df = filter_images(self.df, 'MET')
        return self.df

    def get_n_random_objs(self, n):
        """
        Returns sample of N random objects from dataframe
        Parameters
        ----------
        n : int number of objects to return

        Returns
        -------
        pd.DataFrame df of sample
        """
        return self.df.sample(n)

    def split_delimited(self, cell):
        if isinstance(cell, str) and '|' in cell:
            items = [item.strip() for item in cell.split('|')]
            return ", ".join(items)
        return cell
    
    def clean_culture(self, culture):
        ''' Gets rid of possibly / probably and splits at the comma '''
        if not isinstance(culture, str):
            return culture
            
        cleaned = re.sub(r'\b(?:probably|possibly)\b\s*', '', culture, flags=re.IGNORECASE)
        cleaned = cleaned.split(',')[0].strip()
        return cleaned

    def replace_empty(self):
        ''' Replaces unknown values with a string for the pop-up '''
        for col in self.df.columns:
            is_empty = (
                self.df[col].isna() |
                (self.df[col] == None) |
                (self.df[col].astype(str).str.strip() == ''))

            self.df.loc[is_empty, col] = f"{col} unknown"

        return self.df
    
    def clean_title(self, title):
        ''' Makes a cleaner title to print '''
        if not isinstance(title, str):
            return title

        cleaned = re.sub(r'\([^)]*\)', '', title)
        cleaned = re.sub(r'^\W+|\W+$', '', cleaned)
        return cleaned.strip()
        
    def process_data(self):
        """ Mya comment here """
        cols_to_keep = ['Object Number', 'Title', 'Culture', 'Artist Display Name', 
                        'Artist Display Bio', 'Object Begin Date', 'Medium', 'Dimensions',
                        'Repository', 'Tags', 'image_url']

        self.df = self.df[cols_to_keep]
        # Change repository to MET
        self.df['Repository'] = 'MET'
        self.df['Object Begin Date'] = self.df['Object Begin Date'].astype(int)

        # Rename columns to be more readable
        self.df.rename(columns = {'Artist Display Name' : 'Artist',
                           'Artist Display Bio' : 'Artist biographic information',
                           'Object Begin Date' : 'Year'}, inplace=True)
        
        # Split delimited values into a list
        for col in self.df.columns:
            self.df[col] = self.df[col].apply(self.split_delimited)

        # Clean culture column
        self.df['Culture'] = self.df['Culture'].apply(self.clean_culture)
        
        # Replace empty values with 'Uknown'
        self.df = self.replace_empty()

        # Clean title column
        self.df['Title'].apply(self.clean_title)

        # Create Century column
        self.df['Century'] = self.df['Year'].apply(century_mapping)
        return self.df
        
    def create_final_csv(self, path, save_final=False):
        """
        Runs the above functions to create the final MET data we will use later on.

        Parameters
        ----------
        filename : str
            name of final .csv file
        save_final : bool, optional
            T/F on if actually want to save the result right now, by default False
        """
        self.df = self._request_image_urls()
        self.df = self.process_data()
        if save_final:
            self.df.to_csv(path, index=False)
        print_example_rows(self.df, n=5)
        return None
    
    def filter_and_save(self, filename):
        """
        Filters the dataframe and saves it to a new csv file.
        """
        self.df = self.process_data()
        self.df.to_csv(filename, index=False)
        
        
def main():
    """
    Instantiate MetMuseum class with original file, query, filter, save.
    """
    met = MetMuseum('data/MetObjects_final.csv', is_test=True)
    met.create_final_csv(path='data/MetObjects_final_filteredII.csv', save_final=True)
    print(f"Length of final filtered dataframe: {len(met.df)}")

if __name__ == "__main__":
    main()
