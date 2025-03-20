"""
Unit tests for mova_home.py

This module contains tests for the MoVA homepage functionality including:
    - Data loading and caching
    - Session state management
    - Data filtering
    - Filter reset functionality
"""
import unittest
from unittest.mock import patch
import os
import sys

import pandas as pd
import streamlit as st

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mova_home import load_blended_cached, initialize_session_state, filter_data, reset_filters

base_dir = os.path.dirname(os.path.abspath(__file__))

MET_PATH = os.path.join(base_dir, "data", "MetObjects_final_filtered_processed.csv")
EUROPEANA_PATH = os.path.join(base_dir, "data", "Europeana_data_processed.csv")

class TestMoVAHome(unittest.TestCase):
    """ Test the MoVA Home page """
    def setUp(self):
        """ Set up Test Data """
        self.test_data = pd.DataFrame({
            'Title': ['Art 1', 'Art 2', 'Art 3'],
            'Culture': ['French', 'Italian', 'French'],
            'Year': [1800, 1900, 2000],
            'Repository': ['MET', 'Europeana', 'MET'],
            'image_url': ['url1', 'url2', 'url3']
        })

    @patch('pandas.read_csv')
    def test_load_blended_cached(self, mock_read_csv):
        """Test data loading with stratified sampling (70% MET, 30% Europeana)"""
        # Create mock data for both MET and Europeana
        met_data = pd.DataFrame({
            'Title': [f'MET Art {i}' for i in range(7)],
            'Culture': ['French'] * 7,
            'Year': [1800 + i * 10 for i in range(7)],
            'Repository': ['MET'] * 7,
            'image_url': [f'met_url{i}' for i in range(7)]
        })

        europeana_data = pd.DataFrame({
            'Title': [f'Euro Art {i}' for i in range(3)],
            'Culture': ['Italian'] * 3,
            'Year': [1900 + i * 10 for i in range(3)],
            'Repository': ['Europeana'] * 3,
            'image_url': [f'euro_url{i}' for i in range(3)]
        })

        # Configure mock to return different data for each call
        mock_read_csv.side_effect = [met_data, europeana_data]

        # Test with sample_size=10 to match our test data proportions (7 MET, 3 Europeana)
        result = load_blended_cached('fake_met_path', 'fake_europeana_path', sample_size=10)

        # Verify the results
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 10)

        # Check repository proportions
        repo_counts = result['Repository'].value_counts()
        self.assertEqual(repo_counts['MET'], 7)  # 70%
        self.assertEqual(repo_counts['Europeana'], 3)  # 30%

        # Verify both paths were read
        mock_read_csv.assert_called()
        self.assertEqual(mock_read_csv.call_count, 2)

    def test_initialize_session_state(self):
        """Test session state initialization"""
        # Clear existing session state
        for key in ['search', 'culture', 'years', 'datasource', 'favorites']:
            if key in st.session_state:
                del st.session_state[key]

        initialize_session_state(self.test_data)

        self.assertEqual(st.session_state.search, '')
        self.assertEqual(st.session_state.culture, [])
        self.assertEqual(st.session_state.years, (1800, 2025))
        self.assertIsNone(st.session_state.datasource)
        self.assertEqual(st.session_state.favorites, [])

    def test_filter_data(self):
        """Test data filtering"""
        # Test search filter
        filtered = filter_data(self.test_data, 'Art 1', [], (1700, 2025), None)
        self.assertEqual(len(filtered), 1)

        # Test culture filter
        filtered = filter_data(self.test_data, '', ['French'], (1700, 2025), None)
        self.assertEqual(len(filtered), 2)

        # Test year filter
        filtered = filter_data(self.test_data, '', [], (1800, 1900), None)
        self.assertEqual(len(filtered), 2)

        # Test repository filter
        filtered = filter_data(self.test_data, '', [], (1700, 2025), 'MET')
        self.assertEqual(len(filtered), 2)

        # Test combined filters
        filtered = filter_data(self.test_data, 'Art', ['French'], (1800, 1900), 'MET')
        self.assertEqual(len(filtered), 1)

    def test_reset_filters(self):
        """Test filter reset"""
        # Set some filter values
        st.session_state.search = 'test'
        st.session_state.culture = ['French']
        st.session_state.years = (1900, 2000)
        st.session_state.datasource = 'MET'
        
        reset_filters(self.test_data)

        self.assertEqual(st.session_state.search, '')
        self.assertEqual(st.session_state.culture, [])
        self.assertEqual(st.session_state.years, (1800, 2025))
        self.assertIsNone(st.session_state.datasource)

if __name__ == '__main__':
    unittest.main()
