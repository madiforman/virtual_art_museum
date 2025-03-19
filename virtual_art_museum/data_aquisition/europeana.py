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
Number of unique objects in result: ~4,000

Classes
----------
    Europeana

References
----------
    https://europeana.eu/api/

Authors
----------
    Madison Sanchez-Forman and Mya Strayer
"""
import re

from dotenv import load_dotenv

from pyeuropeana import utils
from pyeuropeana import apis
import pandas as pd

from async_utils import filter_objects
from common_functions import print_example_rows, century_mapping

class Europeana:
    """
    Class for quereying, manipulating, and saving data from the Europeana API.

    This class contains the functionality for querying the Europeana API, 
    cleaning results, and saving the finalized version of the originally 
    downloaded data.

    Parameters
    ----------
    file_path : str
        path to Europeana objects file. Can either be the unfiltered or filtered version.

    Attributes:
    ----------
    df (pd.DataFrame):
        dataframe of Europeana objects.

    """
    def __init__(self, save_final=False):
        """ Initalalizes class with empty dataframe """
        self.df = pd.DataFrame()
        self.df = self.create_final(path="Europeana_data_test.csv", save_final=save_final)


    def bulk_requests(self):
        """
        Queries the Europeana API for each query term in query_terms.csv
        Saves the results to a dataframe and filters out any objects without images.

        This function interates through each query term in query_terms.csv,
        and queries the Europeana API for each term. It then saves the results
        to a dataframe and filters out any objects without images.

        Returns:
        --------
            pd.DataFrame: dataframe of Europeana objects.
        """
        query_terms = pd.read_csv('../data/query_terms.csv', header=None)
        query_terms = set(query_terms.iloc[:, 0].tolist())
        # df_list = []
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
                # convert the response to a dataframe
                df_new = utils.search2df(response)
                self.df = pd.concat([self.df, df_new], ignore_index=True)

                cursor = response.get('nextCursor') # move the pointer
                total_results += len(response.get('items', []))
                print(f"Fetched {total_results} results for query: {query}")
            break
        self.df = self.df.dropna(subset=['image_url']) # drop any objects without images
        self.df = self.df.drop_duplicates(subset=['image_url']) # drop any duplicate images
        self.df = filter_objects(self.df, flag="EUROPEANA") # filter out any objects without images
        print_example_rows(self.df, n=1)
        print(f"Found {len(self.df)} valid image urls")
        return self.df

    def _extract_year(self, row:pd.Series):
        """
        Extracts the year from the description, title, or creator of an object.

        Parameters
        ----------
            row (pd.Series): row of dataframe

        Returns:
        --------
            int: year of object
        """
        date_pattern = r'\d{4}' # regex pattern YYYY
        # search for the year in the description, title, or creator
        match_description = re.search(date_pattern, str(row['description']))
        match_title = re.search(date_pattern, str(row['title']))
        match_creator = re.search(date_pattern, str(row['creator']))

        # if the year is found, return the year
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
        Creates a year column in the dataframe by searching data for year
        Returns:
        --------
            pd.DataFrame: dataframe of Europeana objects.
        """
        self.df['year'] = self.df.apply(self._extract_year, axis=1).astype(int)
        return self.df

    def process_data(self):
        """
        Processes the dataframe by filling missing values, keeping relevant columns,
        and creating a year column.

        Returns:
        --------
            pd.DataFrame: dataframe of Europeana objects.
        """
        self.df.fillna('Unknown', inplace=True) # fill missing values with 'Unknown'

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
        Creates a final dataframe by running the bulk requests and processing the data.

        Parameters
        ----------
            path (str): path to save the final dataframe
            save_final (bool, optional): whether to save the final dataframe. Defaults to False.

        Returns:
        --------
            pd.DataFrame: dataframe of Europeana objects.
        """
        self.df = self.bulk_requests()
        self.df = self.process_data()
        if save_final:
            self.df.to_csv(path, index=False)
        print_example_rows(self.df, n=5)
        return self.df

def main():
    """
    Main function to run the aquisition pipeline
    """
    Europeana()

if __name__ == "__main__":
    main()
