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

import pandas as pd

from data_aquisition.met_museum import MetMuseum

class MetMuseumTests(unittest.TestCase):
    ''' Tests the MetMuseum class '''
    def setUp(self):
        ''' Sets up the test data '''
        tracemalloc.start()
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.test_size = 1500

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

    def test_full_pipeline(self):
        """
        Tests the full pipeline from the MetMuseum class. 

        This tests that the full Met Museum pipeline runs without errors and 
        that the output is as expected. Processing of the data will also be 
        tested explicitly below to avoid reinstantiating the MetMuseum class
        querying multiple times.

        It includes the following steps:
            - Requesting image urls for each unique object id
            - Cleaning the data
            - Filtering the data
            - Saving the data
        """
        self.met = MetMuseum('./data/test_met_objects.csv', run_full_pipeline=True) # pylint: disable=attribute-defined-outside-init

        # Test to see if the dataframe is the correct size
        # Size was 2000 rows, but 1 bad row was added so we should see 2000 if filtering
        # was done correctly
        self.assertEqual(len(self.met.df), self.test_size)
        print("Successfully filtered out bad rows")

        # Test to see if the recently queried image url is as expected
        self.assertEqual(self.met.df.loc[0, 'image_url'],
                        'https://images.metmuseum.org/CRDImages/ad/original/204788.jpg') 

        # 1) split_delimited
        test_cell = "value1|value2|value3"
        result = self.met.split_delimited(test_cell)
        self.assertEqual(result, "value1, value2, value3")

        # 2) clean_title
        test_title = "Art piece (test)"
        result = self.met.clean_title(test_title)
        self.assertEqual(result, "Art piece")

        # 3) clean_culture
        test_culture = "probably Greek, ancient"
        result = self.met.clean_culture(test_culture)
        self.assertEqual(result, "Greek")

        # 4) replace_empty
        self.met.df.loc[0, 'Artist Display Bio'] = ''
        self.met.replace_empty()
        self.assertEqual(self.met.df.loc[0, 'Artist Display Bio'], 'Artist Display Bio unknown')

        # 5) Verifying process_data worked as expected
        self.assertEqual(self.met.df.loc[0, 'Repository'], 'MET')
        self.assertEqual(self.met.df.loc[0, 'Year'], 1847)
        self.assertEqual(self.met.df.loc[0, 'Description'], 'Description unknown')

        # test saving
        self.met.filter_and_save('./data/test_met_objects.csv', process_data=False)
        self.assertTrue(os.path.exists('./data/test_met_objects.csv'))

if __name__ == '__main__':
    unittest.main()
