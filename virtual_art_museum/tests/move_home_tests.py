import unittest
import pandas as pd
import numpy as np

from my_other_file import my_functions

class test_image_processing_met(unittest.TestCase):
    ''' Tests the image_processing_met function from the mova_home file '''
    def setup(self):
        ''' Sets up a dummy dataframe to test '''
        self.test_data = pd.DataFrame({
            'ID': ['2011.604.5.497', '2000.284.45', '26.2.11'],
            'Title': ['Terracotta rim fragment of a kylix (drinking cup)', '[piece]', 'Headrest of Khentika'],
            'Culture': ['Greek, Attic', 'Indonesia (Java)', 'probably Egyptian'],
            'Artist': ['Artist One | Artist Two', ' ', 'Big Bird'],
            'Year': [-600, -510, 64],
            'Material': ['Terracotta', 'Bronze|Wood', 'Travertine (Egyptian alabaster)'],
            'Repository': ['Metropolitan Museum of Art', 'the MET', ' '],
            'Tags': ['pottery|cup', np.nan, 'furniture'],
            'URL': ['https://images.metmuseum.org/example1.jpg', 'https://images.metmuseum.org/example2.jpg', 'https://images.metmuseum.org/example3.jpg']
        })

        self.processed_data = image_processing_met(self.test_data)

    def test_delimited_values_splitting(self):
        ''' Test if pipe-delimited values are converted to comma-separated strings '''
        self.assertEqual(self.processed_data.loc[0, 'Artist'], 'Artist One, Artist Two"
        self.assertEqual(self.processed_data.loc[1, 'Material'], 'Bronze, Wood')
        self.assertEqual(self.processed_data.loc[0, 'Tags'], 'pottery, cup')
        
    def test_title_parentheses_removal(self):
        ''' Tests that the caption title removes any extra characters and parenthetical values '''
        self.assertEqual(self.processed_data.loc[0, 'caption_title'], 'Terracotta rim fragment of a kylix')
        self.assertEqual(self.processed_data.loc[0, 'caption_title'], 'piece')
        
    def test_culture_cleaning(self):
        ''' Test if 'probably' and text after comma is removed from Culture '''
        self.assertEqual(self.processed_data.loc[0, 'Culture'], 'Greek')
        self.assertEqual(self.processed_data.loc[1, 'Culture'], 'Indonesia')
        self.assertEqual(self.processed_data.loc[2, 'Culture'], 'Egyptian')
        
    def test_year_to_century_mapping(self):
        ''' Test if years are correctly mapped to centuries '''
        self.assertEqual(self.processed_data.loc[0, 'Century'], '6th century BC')
        self.assertEqual(self.processed_data.loc[1, 'Century'], '6th century BC')
        self.assertEqual(self.processed_data.loc[2, 'Century'], '1st century AD')
        
    def test_empty_values_replacement(self):
        ''' Test if empty values are replaced with column-specific unknown text '''
        self.assertEqual(self.processed_data.loc[1, 'Tags'], 'Tags unknown')
        self.assertEqual(self.processed_data.loc[1, 'Artist'], 'Artist unknown')

    def test_source_overwrite(self):
        ''' Tests that all sources are overwritten to 'MET' '''
        self.assertEqual(self.process_data.loc[0, 'datasource'], 'MET')
        self.assertEqual(self.process_data.loc[1, 'datasource'], 'MET')
        self.assertEqual(self.process_data.loc[2, 'datasource'], 'MET')
        
    def test_dataframe_structure(self):
        """Test if the DataFrame structure is maintained with the correct columns"""
        expected_columns = list(self.test_data.columns) + ['caption_title'] + ['Century']
        self.assertListEqual(list(self.processed_data.columns), expected_columns)
        
