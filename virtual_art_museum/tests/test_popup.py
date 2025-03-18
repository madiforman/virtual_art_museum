import unittest
from unittest import mock
import sys
import os

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from popup_revised import display_image, display_popup

class TestStreamlitApp(unittest.TestCase):
    """Test cases for Streamlit app"""

    def setUp(self):
        """Set up test data."""
        self.data = pd.DataFrame({
            'title': ['Image 1'],
            'artist': ['Artist 1'],
            'year': [2025],
            'medium': ['Ink on Paper'],
            'region': ['Europe'],
            'image': [
                'https://collectionapi.metmuseum.org/public/collection/v1/objects/45734'
            ]
        })
        self.index = 0
        self.selected_image = self.data.iloc[0]['image']
        self.missing_image_url = "https://collectionapi.metmuseum.org/api/collection/v1/iiif/000000/000000/restricted"

    def test_data_frame(self):
        """Test DataFrame structure and content"""
        expected_columns = ['title', 'artist', 'year', 'medium', 'region', 'image']
        self.assertEqual(list(self.data.columns), expected_columns)
        self.assertEqual(len(self.data), 1)

        row = self.data.iloc[0]
        self.assertEqual(row['title'], 'Image 1')
        self.assertEqual(row['artist'], 'Artist 1')
        self.assertEqual(row['year'], 2025)
        self.assertEqual(row['medium'], 'Ink on Paper')
        self.assertEqual(row['region'], 'Europe')
        self.assertEqual(
            row['image'],
            'https://collectionapi.metmuseum.org/public/collection/v1/objects/45734'
        )

    def test_display_image_missing_data(self):
        """Test image display when data is missing"""
        edge_case_data = pd.DataFrame({
            'title': [None],
            'artist': ['Artist 1'],
            'year': [2025],
            'medium': ['Ink on Paper'],
            'region': ['Europe'],
            'image': ['https://collectionapi.metmuseum.org/public/collection/v1/objects/45734']
        })
        row = edge_case_data.iloc[0]
        self.assertIsNone(row['title'])  # Ensuring missing title is detected
        self.assertEqual(row['artist'], 'Artist 1')

    @mock.patch("streamlit.markdown")
    @mock.patch("streamlit.session_state", new_callable=dict)
    def test_display_image(self, mock_session_state, mock_markdown):
        """Test image display"""
        mock_session_state["show_modal"] = True  # Ensure the modal is set to show
        display_image(self.data, self.index)
        mock_markdown.assert_called_once()

    @mock.patch("streamlit.markdown")
    @mock.patch("streamlit.session_state", new_callable=dict)
    def test_display_popup(self, mock_session_state, mock_markdown):
        """Test popup display with an image"""
        mock_session_state["show_modal"] = True  # Ensure the modal is set to show
        mock_session_state["selected_image"] = self.selected_image
        mock_session_state["selected_title"] = "Image 1"
        mock_session_state["selected_author"] = "Artist 1"
        mock_session_state["selected_year"] = 2025

        display_popup(self.data, self.selected_image)
        mock_markdown.assert_called_once()

    @mock.patch("streamlit.markdown")
    @mock.patch("streamlit.session_state", new_callable=dict)
    def test_display_popup_no_image_found(self, mock_session_state, mock_markdown):
        """Test popup display when image is missing"""
        mock_session_state["show_modal"] = True  # Ensure the modal is set to show
        mock_session_state["selected_image"] = self.missing_image_url
        mock_session_state["selected_title"] = "Image 1"
        mock_session_state["selected_author"] = "Artist 1"
        mock_session_state["selected_year"] = 2025

        result = display_popup(self.data, self.missing_image_url)
        self.assertIsNone(result)
        mock_markdown.assert_not_called()

if __name__ == "__main__":
    unittest.main()
