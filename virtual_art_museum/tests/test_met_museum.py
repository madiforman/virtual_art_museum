"""
This module contains tests for the MetMuseum class. It mocks the entire pipeline
that was perfomed on all 400,000+ objects in the Met collection.

Tests
-------
    - Test the full pipeline
    - Test the split_delimited method
    - Test the clean_title method
    - Test the clean_culture method

Note
-------
    Since the original file is 400,000+ rows, I have mocked the data to be 2000 rows
    I am loading from the file that already had objects without images removed. 
    Therefore I added a mock "bad row" to the dataframe to test filtering functionality.
"""
import unittest
import os
import tracemalloc
import warnings
from unittest.mock import patch

import pandas as pd

from data_aquisition.met_museum import MetMuseum # pylint: disable=import-error

class MetMuseumTests(unittest.TestCase):
    ''' Tests the MetMuseum class '''
    def setUp(self):
        ''' Sets up the test data '''
        tracemalloc.start()
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.test_size = 50

        self.test_data = pd.DataFrame([{
            'Object Number': '1234567',
            'Object ID': '34', # real object id with known url 
            'Department': 'Test Department',
            'Title': 'Test Title',
            'Culture': 'Test Culture',
            'Artist Display Name': 'Test Artist',
            'Artist Display Bio': 'Test Bio',
            'Object Begin Date': '1847',
            'Medium': 'Test Medium',
            'Repository': 'MET',
            'Tags': 'Test Tags',

        }] * self.test_size)  # Replicate the row 50 times
        bad_row = pd.DataFrame([{
            'Object ID': '123456789021394871478891498290',
            'Department': 'Test Department',
            'Title': 'Test Title',
            'Culture': 'Test Culture',
            'Artist Display Name': 'Test Artist',
            'Artist Display Bio': 'Test Bio',
            'Object Begin Date': '1954',
            'Medium': 'Test Medium',
            'Repository': 'MET',
            'Tags': 'Test Tags',
        }])

        self.test_data = pd.concat([self.test_data, bad_row], ignore_index=True)
        
        # Create the data directory if it doesn't exist
        os.makedirs('./data', exist_ok=True)
        
        # Save the test data
        self.test_data.to_csv('./data/test_met_objects.csv', index=False)

    def tearDown(self):
        ''' Cleans up the test data '''
        tracemalloc.stop()
        if os.path.exists('./data/test_met_objects.csv'):
            os.remove('./data/test_met_objects.csv')
        if os.path.exists('./data/processed_met_objects.csv'):
            os.remove('./data/processed_met_objects.csv')

    @patch('data_aquisition.met_museum.filter_objects')
    def test_full_pipeline(self, mock_filter_objects):
        """ Tests the full pipeline with mocked API calls """
        # Mock the API response
        mock_df = self.test_data.copy()
        mock_df['image_url'] = 'https://images.metmuseum.org/CRDImages/ad/original/204788.jpg'
        mock_filter_objects.return_value = mock_df[:self.test_size]  # Return mocked data without bad row

        # # Run the test with mocked API
        met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)

        # Verify the mock was called
        mock_filter_objects.assert_called_once()

        # Verify that the bad object was filtered out
        self.assertEqual(len(met.df), self.test_size)
        self.assertEqual(met.df.loc[0, 'image_url'],
                        'https://images.metmuseum.org/CRDImages/ad/original/204788.jpg')

    def test_split_delimited(self):
        """ Tests the split_delimited method """
        met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=False)
        test_cell = "value1|value2|value3"
        result = met.split_delimited(test_cell)
        self.assertEqual(result, "value1, value2, value3")
        
    def test_clean_title(self):
        """ Tests the clean_title method """
        met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=False)
        test_title = "Art piece (test)"
        result = met.clean_title(test_title)
        self.assertEqual(result, "Art piece")
        
    def test_clean_culture(self):
        """ Tests the clean_culture method """
        met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=False)
        test_culture = "probably Greek, ancient"
        result = met.clean_culture(test_culture)
        self.assertEqual(result, "Greek")

    def test_replace_empty(self):
        """ Tests the replace_empty method """
        met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=False)
        met.df.loc[0, 'Artist Display Bio'] = ''
        met.replace_empty()
        self.assertEqual(met.df.loc[0, 'Artist Display Bio'], 'Artist Display Bio unknown')
        
    def test_process_data(self):
        """ Tests the process_data method """
        met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)
        self.assertEqual(met.df.loc[0, 'Repository'], 'MET')
        self.assertEqual(met.df.loc[0, 'Year'], 1847)
        self.assertEqual(met.df.loc[0, 'Description'], 'Description unknown')

    def test_filter_and_save(self):
        """ Tests the filter_and_save method """
        met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=False)
        met.filter_and_save('./data/test_met_objects.csv', process_data=False)
        self.assertTrue(os.path.exists('./data/test_met_objects.csv'))
        
if __name__ == '__main__':
    unittest.main()
