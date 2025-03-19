"""
This module contains tests for the popup.py file. It tests the display_artwork_popup
function for both MET and Europeana artwork.

Tests
-------
    - Test the display_artwork_popup function for MET artwork
    - Test the display_artwork_popup function for Europeana artwork
"""
import unittest
from unittest.mock import patch

from popup import display_artwork_popup

class TestPopup(unittest.TestCase):
    """
    Tests the display_artwork_popup function for both MET and Europeana artwork.
    """
    @patch('popup.st')
    def test_display_artwork_popup_met(self, mock_st):
        """
        Tests the display_artwork_popup function for MET artwork.
        """
        # Test data for MET artwork
        met_artwork = {
            'Repository': 'MET',
            'Title': 'Test Artwork',
            'Artist': 'Test Artist',
            'Artist biographic information': 'Test Bio',
            'Century': '19th',
            'Medium': 'Oil on canvas',
            'Culture': 'American',
            'Dimensions': '100 x 100 cm'
        }

        # Call the function
        display_artwork_popup(met_artwork)

        # Verify markdown styling was called
        mock_st.markdown.assert_any_call("""
        <style>
            .artwork-popup {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .artwork-image {
                width: 100%;
                max-height: 60vh;
                object-fit: contain;
            }
            .artwork-title {
                font-size: 24px;
                font-weight: bold;
                margin: 15px 0;
            }
            .artwork-details {
                font-size: 16px;
                color: #4A4A4A;
                margin: 10px 0;
            }
            .artwork-metadata {
                background-color: #F8F9FA;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

        # Verify artwork details were displayed
        mock_st.markdown.assert_any_call("### Test Artwork")
        mock_st.markdown.assert_any_call("**Artist:** Test Artist")
        mock_st.markdown.assert_any_call("**Artist Bio:** Test Bio")
        mock_st.markdown.assert_any_call("**Century:** 19th")
        mock_st.markdown.assert_any_call("**Medium:** Oil on canvas")
        mock_st.markdown.assert_any_call("**Culture:** American")
        mock_st.markdown.assert_any_call("**Dimensions**: 100 x 100 cm")

    @patch('popup.st')
    def test_display_artwork_popup_europeana(self, mock_st):
        """
        Tests the display_artwork_popup function for Europeana artwork.
        """
        # Test data for Europeana artwork
        europeana_artwork = {
            'Repository': 'Europeana',
            'Title': 'Test Europeana',
            'Artist': 'Test Artist',
            'Culture': 'European',
            'Description': 'Test Description'
        }

        # Call the function
        display_artwork_popup(europeana_artwork)

        # Verify artwork details were displayed
        mock_st.markdown.assert_any_call("### Test Europeana")
        mock_st.markdown.assert_any_call("**Artist:** Test Artist")
        mock_st.markdown.assert_any_call("**Culture:** European")
        mock_st.markdown.assert_any_call("**Description:** Test Description")

        # Verify close button was created
        mock_st.button.assert_called_once_with("Close", key="close_popup")

if __name__ == '__main__':
    unittest.main()
