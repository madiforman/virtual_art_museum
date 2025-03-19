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

from data_aquisition.met_museum import MetMuseum

class MetMuseumTests(unittest.TestCase):
    ''' Tests the MetMuseum class '''
    def setUp(self):
        ''' Sets up the test data '''
        tracemalloc.start()
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.test_size = 50

        bad_row = pd.DataFrame([{
                                'Object ID': '123456789021394871478891498290',
                                'Department': 'Test Department',
                                'Title': 'Test Title',
                                'Culture': 'Test Culture',
                                'Artist Display Name': 'Test Artist',
                                'Artist Display Bio': 'Test Bio',
                                'Object Begin Date': 'Test Date',
                                'Medium': 'Test Medium',
                                'Repository': 'Test Repository',
                                'Tags': 'Test Tags',
                                }])
        # mocks how data looked when orginally downloaded from met github
        self.test_data = pd.read_csv('./data/MetObjects_final.csv', dtype=str)[:self.test_size]
        self.test_data = pd.concat([self.test_data, bad_row], ignore_index=True)

        # IMPORTANT: removing image url to mock the way the data was originally downloaded
        self.test_data.pop('image_url')
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

        # Run the test with mocked API
        self.met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)

        # Verify the mock was called
        mock_filter_objects.assert_called_once()

        # Verify that the bad object was filtered out
        self.assertEqual(len(self.met.df), self.test_size)
        self.assertEqual(self.met.df.loc[0, 'image_url'],
                        'https://images.metmuseum.org/CRDImages/ad/original/204788.jpg')

    def test_split_delimited(self):
        """ Tests the split_delimited method """
        self.met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)
        test_cell = "value1|value2|value3"
        result = self.met.split_delimited(test_cell)
        self.assertEqual(result, "value1, value2, value3")
        
    def test_clean_title(self):
        """ Tests the clean_title method """
        self.met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)
        test_title = "Art piece (test)"
        result = self.met.clean_title(test_title)
        self.assertEqual(result, "Art piece")
        
    def test_clean_culture(self):
        """ Tests the clean_culture method """
        self.met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)
        test_culture = "probably Greek, ancient"
        result = self.met.clean_culture(test_culture)
        self.assertEqual(result, "Greek")

    def test_replace_empty(self):
        """ Tests the replace_empty method """
        self.met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)
        self.met.df.loc[0, 'Artist Display Bio'] = ''
        self.met.replace_empty()
        self.assertEqual(self.met.df.loc[0, 'Artist Display Bio'], 'Artist Display Bio unknown')
        
    def test_process_data(self):
        """ Tests the process_data method """
        self.met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)
        self.assertEqual(self.met.df.loc[0, 'Repository'], 'MET')
        self.assertEqual(self.met.df.loc[0, 'Year'], 1847)
        self.assertEqual(self.met.df.loc[0, 'Description'], 'Description unknown')

    def test_filter_and_save(self):
        """ Tests the filter_and_save method """
        self.met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True)
        self.met.filter_and_save('./data/test_met_objects.csv', process_data=False)
        self.assertTrue(os.path.exists('./data/test_met_objects.csv'))
        
if __name__ == '__main__':
    unittest.main()
