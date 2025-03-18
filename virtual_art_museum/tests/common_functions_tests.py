import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from data_aquisition.common_functions import (
    print_example_rows, century_mapping, image_processing_europeana,
    blend_datasources, reorder_columns
)

class TestCommonFunctions(unittest.TestCase):
    """Test cases for common functions"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data"""
        # Create sample MET data
        cls.met_data = pd.DataFrame({
            'Object Number': ['1', '2'],
            'Title': ['Art1', 'Art2'],
            'Culture': ['French', 'British'],
            'Tags': ['painting, oil', 'sculpture, marble'],
            'Year': [1800, 1900],
            'Repository': ['MET', 'MET'],
            'Medium': ['oil', 'marble'],
            'Artist': ['Artist1', 'Artist2'],
            'Department': ['Paintings', 'Sculptures']
        })
        
        # Create sample Europeana data
        cls.euro_data = pd.DataFrame({
            'europeana_id': ['E1', 'E2'],
            'title': ['Euro Art1', 'Euro Art2'],
            'creator': ['Euro Artist1', 'Euro Artist2'],
            'description': ['oil painting', 'marble sculpture'],
            'country': ['France', 'United Kingdom'],
            'provider': ['Museum1', 'Museum2'],
            'year': [1850, 1950],
            'repository': ['Europeana', 'Europeana']
        })

    def test_century_mapping(self):
        """Test century mapping function"""
        test_cases = [
            (1, "1st century AD"),
            (150, "2nd century AD"),
            (250, "3rd century AD"),
            (1800, "19th century AD"),
            (-500, "5th century BC"),
            (2020, "Unknown"),
            (-1, -1)
        ]
        
        for year, expected in test_cases:
            with self.subTest(year=year):
                result = century_mapping(year)
                self.assertEqual(result, expected)

    def test_image_processing_europeana(self):
        """Test Europeana image processing"""
        euro_processed, met_processed = image_processing_europeana(
            self.met_data.copy(), self.euro_data.copy()
        )
        
        # Test column renaming
        self.assertIn('Object Number', euro_processed.columns)
        self.assertIn('Title', euro_processed.columns)
        
        # Test culture mapping
        self.assertEqual(euro_processed.loc[0, 'Culture'], 'French')
        self.assertEqual(euro_processed.loc[1, 'Culture'], 'British')
        
        # Test tag processing
        self.assertIn('Tags', euro_processed.columns)
        
        # Test year processing
        self.assertTrue(all(isinstance(x, int) for x in euro_processed['Year']))

    def test_blend_datasources(self):
        """Test blending of data sources"""
        blended = blend_datasources(self.met_data.copy(), self.euro_data.copy())
        
        # Test length
        self.assertEqual(len(blended), len(self.met_data) + len(self.euro_data))
        
        # Test content preservation
        self.assertTrue(all(x in blended['Repository'].unique() 
                          for x in ['MET', 'Europeana']))

    def test_reorder_columns(self):
        """Test column reordering"""
        df1, df2 = reorder_columns(self.met_data.copy(), self.euro_data.copy())
        
        # Test column order matches
        self.assertEqual(list(df1.columns), list(df2.columns))
        
        # Test no data loss
        self.assertEqual(len(df1), len(self.met_data))
        self.assertEqual(len(df2), len(self.euro_data))
