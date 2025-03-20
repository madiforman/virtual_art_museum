"""
Unit tests for the favorites module.

This module tests the functionality of favorites.py, ensuring that:
- Favorites can be loaded and saved correctly.
- A collage of images can be created from favorites.

Tests cover both file operations and UI components using mocks.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
from io import BytesIO
import os
import requests
from PIL import Image

# Import functions from favorites.py
from Pages.favorites import load_favorites, save_favorites, create_collage, display_favorites, main
FAVORITES_CACHE_FILE = "favorites_cache.json"

class TestFavorites(unittest.TestCase):
    """Tests for the favorites module."""

    def setUp(self):
        """Set up test data with sample favorites."""
        self.test_favorites = [
            {"image_url": "http://example.com/image1.jpg", "Title": "Artwork 1"},
            {"image_url": "http://example.com/image2.jpg", "Title": "Artwork 2"},
        ]

    @patch('builtins.open')
    @patch('os.path.exists')  # Add os.path.exists patch
    def test_load_favorites_empty(self, mock_exists, mock_file):
        """Test that load_favorites returns an empty list when the cache file is empty"""
        # Set up os.path.exists to return False
        mock_exists.return_value = False
        
        # Call the function
        favorites = load_favorites()
        
        # Verify results
        self.assertEqual(favorites, [])
        
        # Verify that exists was checked and open was never called
        mock_exists.assert_called_once_with(FAVORITES_CACHE_FILE)
        mock_file.assert_not_called()
    
    @patch('builtins.open')
    @patch('os.path.exists')
    def test_load_favorites_with_data(self, mock_exists, mock_file):
        """Test that load_favorites correctly loads data from a non-empty cache file"""
        # Setup test data
        test_data = [{'image_url': 'test_url', 'Title': 'Test Art'}]
        
        # Mock os.path.exists to return True
        mock_exists.return_value = True
        
        # Setup mock to return JSON string directly
        mock_context = MagicMock()
        mock_context.read.return_value = json.dumps(test_data)
        mock_file.return_value.__enter__.return_value = mock_context
        
        # Call the function
        favorites = load_favorites()

        # Verify results
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites, test_data)
        
        # Verify the mocks were called correctly
        mock_exists.assert_called_once_with(FAVORITES_CACHE_FILE)
        mock_file.assert_called_once_with(FAVORITES_CACHE_FILE, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_favorites(self, mock_json_dump, mock_file):
        """Test that save_favorites correctly writes data to the cache file."""
        save_favorites(self.test_favorites)
        mock_file.assert_called_with(FAVORITES_CACHE_FILE, "w", encoding="utf-8")
        mock_json_dump.assert_called_with(self.test_favorites, mock_file())

    @patch("requests.get")
    def test_create_collage(self, mock_get):
        """Test that create_collage generates an image collage from a list of images."""
        mock_response = MagicMock()
        mock_response.content = BytesIO().getvalue()
        mock_get.return_value = mock_response

        images = [Image.new("RGB", (100, 100)) for _ in range(2)]
        captions = ["Caption 1", "Caption 2"]
        result = create_collage(images, captions)
        self.assertIsInstance(result, BytesIO)

if __name__ == "__main__":
    unittest.main()