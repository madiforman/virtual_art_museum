"""
Module for testing the functions that are used in the common_functions.py file.
Thie means they were applied to both data sources.

Tests
----------
    print_example_rows
    century_mapping
    image_processing_europeana
    blend_datasources
    reorder_columns
"""
import io
import sys
import unittest

import pandas as pd

from data_aquisition.common_functions import (
    blend_datasources,
    century_mapping,
    image_processing_europeana,
    print_example_rows,
    reorder_columns
)

class TestCommonFunctions(unittest.TestCase):
    """Test cases for common functions"""
    def setUp(self):
        self.sample_df = pd.DataFrame({
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3]
        })

        # Create sample MET DataFrame
        self.sample_met_df = pd.DataFrame({
            'Object Number': ['1', '2'],
            'Title': ['Art1', 'Art2'],
            'Artist': ['Artist1', 'Artist2'],
            'Description': ['Desc1', 'Desc2'],
            'Department': ['Dep1', 'Dep2'],
            'Year': [1800, 1900],
            'Culture': ['British, French', 'Italian'],
            'Medium': ['Oil', 'Canvas'],
            'Tags': ['landscape, nature', 'portrait'],
            'Repository': ['MET', 'MET'],
            'Artist biographic information': ['Bio1', 'Bio2'],
            'Dimensions': ['10x20', '30x40']
        })

        # Create sample Europeana DataFrame
        self.sample_europeana_df = pd.DataFrame({
            'europeana_id': ['E1', 'E2'],
            'title': ['Euro Art1', 'Euro Art2'],
            'creator': ['Creator1', 'Unknown'],
            'description': ['landscape painting', 'Unknown'],
            'provider': ['Provider1', 'Provider2'],
            'year': [1850, 'Unknown'],
            'country': ['United Kingdom', 'France']
        })

    def capture_output(self, func, *args):
        """ Helper method to capture stdout """
        captured_output = io.StringIO()
        sys.stdout = captured_output
        func(*args)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def test_print_example_rows(self):
        """ Test print_example_rows function - test only necessary to increase coverage """
        output = self.capture_output(print_example_rows, self.sample_df, 2)
        self.assertIn('\tcol1: a', output)
        self.assertIn('\tcol2: 1', output)
        self.assertIn('\tcol1: b', output)
        self.assertIn('\tcol2: 2', output)

    def test_century_mapping(self):
        """ Test century_mapping function """
        self.assertEqual(century_mapping(1850), "19th century AD")
        self.assertEqual(century_mapping(-500), "5th century BC")
        self.assertEqual(century_mapping(101), "2nd century AD")
        self.assertEqual(century_mapping(2020), "Unknown")
        self.assertEqual(century_mapping(900000000), "Unknown")

    def test_image_processing_europeana(self):
        """ Test image_processing_europeana function """
        processed_europeana, met_processed = image_processing_europeana(
            self.sample_met_df.copy(), self.sample_europeana_df.copy()
        )
        self.assertEqual(len(processed_europeana), 2)
        self.assertEqual(len(met_processed), 2)

        self.assertIn('Object Number', processed_europeana.columns)
        self.assertIn('Title', processed_europeana.columns)
        self.assertIn('Artist', processed_europeana.columns)

        # Test new columns
        self.assertIn('Medium', processed_europeana.columns)
        self.assertIn('Tags', processed_europeana.columns)
        self.assertIn('Repository', processed_europeana.columns)

        # Test country mapping
        self.assertEqual(processed_europeana.loc[0, 'Culture'], 'British')
        self.assertEqual(processed_europeana.loc[1, 'Culture'], 'French')

        # Test creator cleaning
        self.assertEqual(processed_europeana.loc[1, 'Artist'], 'Artist unknown')

    def test_blend_datasources(self):
        """Test blend_datasources function"""
        # process data
        processed_europeana, processed_met = image_processing_europeana(
            self.sample_met_df,
            self.sample_europeana_df
        )
        blended = blend_datasources(processed_met, processed_europeana)
        # test length
        self.assertEqual(
            len(blended),
            len(processed_met) + len(processed_europeana)
        )

    def test_reorder_columns(self):
        """Test reorder_columns function"""
        # process data
        processed_europeana, processed_met = image_processing_europeana(
            self.sample_met_df,
            self.sample_europeana_df
        )
        # then reorder
        df1, df2 = reorder_columns(processed_met, processed_europeana)
        # test column order
        self.assertTrue(all(df1.columns == df2.columns))
        # test that all columns from df1 are present in df2
        self.assertEqual(set(df1.columns), set(df2.columns))

if __name__ == '__main__':
    unittest.main()
