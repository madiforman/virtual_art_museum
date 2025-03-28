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

Functions
----------
    _request_image_urls: Requests image urls from the MET API
    _run_full_pipeline: Runs the full pipeline
    split_delimited: Splits delimited values into a list
    clean_culture: Cleans culture column
    replace_empty: Replaces empty values with 'Unknown'
    process_data: Filters to only relevant columns and renames / cleans columns
    filter_and_save: Filters the dataframe and saves it to a new csv file
    main: Main function to run the pipeline

References
----------
    https://github.com/metmuseum/openaccess

Authors
----------
    Madison Sanchez-Forman and Mya Strayer
"""

import re

import pandas as pd

from data_aquisition.async_utils import filter_objects # pylint: disable=import-error
from data_aquisition.common_functions import ( # pylint: disable=import-error
    print_example_rows,
    century_mapping
)


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

    def __init__(self, file_path, run_full_pipeline=False, save_name='./data/test_met_objects.csv'):
        """ Initalizes class with given file path """
        self.df = pd.read_csv(file_path, dtype='str')
        # If has images is false, we need to run request pipeline
        if run_full_pipeline:
            # save name is set to a test file since we don't want to overwrite the original
            self._run_full_pipeline(path=save_name, save_final=True)

    def _run_full_pipeline(self, path, save_final=False) -> None:
        """
        Runs the above functions to create the final MET data we will use later on.
        This function is only used to aquire image urls at the very beginning of the pipeline

        Parameters
        ----------
        filename : str
            name of final .csv file
        save_final : bool, optional
            T/F on if actually want to save the result right now, by default False
        """
        print("\n\nBeginning to build data from the Metropolitan Museum of Art.")
        print("Requesting image urls...")
        self.df = filter_objects(self.df, 'MET')
        self.df = self.process_data()
        if save_final:
            self.df.to_csv(path, index=False)
        # print("Example row from the final dataframe:")
        # print_example_rows(self.df, n=1)
    def split_delimited(self, cell):
        """
        Splits delimited values into a list
        Parameters
        ----------
        cell : str
            cell to split

        Returns
        -------
        str of split values
        """
        if isinstance(cell, str) and '|' in cell:
            items = [item.strip() for item in cell.split('|')]
            return ", ".join(items)
        return cell

    def clean_culture(self, culture):
        """
        Cleans culture column
        Parameters
        ----------
        culture : str
            culture to clean

        Returns
        -------
        str of cleaned culture 
        """
        if not isinstance(culture, str):
            return "Culture unknown"

        cleaned = re.sub(r'\b(?:probably|possibly)\b\s*', '', culture, flags=re.IGNORECASE)
        cleaned = cleaned.split(',')[0].strip()
        return cleaned

    def replace_empty(self):
        """
        Replaces empty values with 'Unknown'
        Parameters
        ----------
        df : pd.DataFrame
            dataframe to replace empty values in

        Returns
        -------
        pd.DataFrame with empty values replaced with 'Unknown'
        """
        for col in self.df.columns:
            is_empty = (
                self.df[col].isna() |
                (self.df[col] is None) |
                (self.df[col].astype(str).str.strip() == ''))

            self.df.loc[is_empty, col] = f"{col} unknown"

        return self.df

    def clean_title(self, title):
        """
        Cleans title column
        Parameters
        ----------
        title : str
            title to clean

        Returns
        -------
        str of cleaned title
        """
        cleaned = re.sub(r'\([^)]*\)', '', title)
        cleaned = re.sub(r'^\W+|\W+$', '', cleaned)
        return cleaned.strip()

    def process_data(self):
        """
        Filters to only relevant columns and renames / cleans columns
        Returns
        -------
        pd.DataFrame with relevant columns
        """
        cols_to_keep = ['Object Number', 'Department', 'Title', 'Culture',
                        'Artist Display Name', 'Artist Display Bio',
                        'Object Begin Date', 'Medium', 'Repository', 'Tags',
                        'image_url']

        self.df = self.df[cols_to_keep]
        # Change repository to MET
        self.df['Repository'] = 'MET'

        self.df['Description'] = "Description unknown"
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

    def filter_and_save(self, path, process_data=True) -> None:
        """
        Filters the dataframe and saves it to a new csv file. assumes we already have image urls.

        Parameters
        ----------
        path : str
            path to save the final dataframe
        """
        if process_data:
            self.df = self.process_data()
            print_example_rows(self.df, n=1)
        self.df.to_csv(path, index=False)

def main():
    """
    Main function to run the pipeline
    """
    # met = MetMuseum('../data/MetObjects_final.csv', run_full_pipeline=True)
    # met.filter_and_save(path='../data/MetObjects_final_filtered_II.csv')
    # print(f"Length of final filtered dataframe: {len(met.df)}")
    met_test = MetMuseum('../data/MetObjects.txt', run_full_pipeline=True)
    met_test.filter_and_save(path='../data/MetObjects_test.csv', process_data=True)

if __name__ == "__main__":
    main()
