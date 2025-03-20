"""
This module contains tests for the Europeana class. It mocks the pipeline
for acquiring and processing art data from the Europeana API.

Tests
-------
    - Test the full pipeline
    - Test year extraction
    - Test data processing
    - Test data cleaning

Note
-------
    Since the API calls are expensive and time-consuming, we'll mock the API responses
    and test the data processing functionality. I added one valid image url to the mock to 
    show that the data processing functionality is working, in contrast to the Met Museum
    test script where we see a bad url filtered out.
"""
import unittest
from unittest.mock import patch
import os
import tracemalloc
import warnings

import pandas as pd

from data_aquisition.europeana import Europeana

class EuropeanaTests(unittest.TestCase):
    """ Tests the Europeana class """
    def setUp(self):
        """ Sets up the test data """
        tracemalloc.start()
        warnings.filterwarnings("ignore", category=ResourceWarning)

        # Create mock test data
        self.test_data = pd.DataFrame({
            'europeana_id': ['test_id_1', 'test_id_2'],
            'image_url': ['http://test1.jpg', 'http://test2.jpg'],
            'title': ['Painting from 1850', 'Sculpture'],
            'creator': ['Artist Name (1820-1880)', 'Unknown'],
            'description': ['Created in 1855', 'Ancient artwork'],
            'country': ['France', 'Italy'],
            'provider': ['Museum 1', 'Museum 2']
        })

    def tearDown(self):
        """ Cleans up the test data """
        tracemalloc.stop()
        if os.path.exists('Europeana_data_test.csv'):
            os.remove('Europeana_data_test.csv')

    @patch('data_aquisition.europeana.apis')
    @patch('data_aquisition.europeana.utils')

    def test_bulk_requests(self, mock_utils, mock_apis):
        """Tests the bulk_requests method"""
        # Mock the API response
        mock_apis.search.return_value = {
            'items': ['item1', 'item2'],
            'nextCursor': None
        }

        # Mock the utils.search2df to return a DataFrame
        mock_utils.search2df.return_value = pd.DataFrame({
            'europeana_id': ['test_id_1'],
            'image_url': ['https://iiif.wellcomecollection.org/image/V0006952.jpg/full/512,/0/default.jpg'],
            'title': ['Painting from 1850'],
            'creator': ['Artist Name'],
            'description': ['Created in 1855'],
            'country': ['France'],
            'provider': ['Museum 1']
        })

        europeana = Europeana(save_final=False)
        result = europeana.bulk_requests(is_test=True)

        self.assertIsInstance(result, pd.DataFrame)

        required_columns = [
                            'europeana_id', 
                            'image_url', 
                            'title', 
                            'creator', 
                            'description', 
                            'country', 
                            'provider'
                            ]

        for column in required_columns:
            self.assertIn(column, result.columns)

        self.assertFalse(result['image_url'].isna().any())

        # test extract year
        europeana.df = self.test_data
        year = europeana.extract_year(self.test_data.iloc[0])
        self.assertEqual(year, '1855')

        # no year present
        row = self.test_data.iloc[1]
        year = europeana.extract_year(row)
        self.assertEqual(year, -1)

        # test process data
        processed_df = europeana.process_data()
        expected_columns = ['europeana_id', 'image_url', 'title', 'creator',
                          'description', 'country', 'provider', 'year', 
                          'repository', 'Century']
        self.assertTrue(all(col in processed_df.columns for col in expected_columns))

        # Check if repository is correctly set
        self.assertTrue(all(processed_df['repository'] == 'EUROPEANA'))

if __name__ == '__main__':
    unittest.main()
