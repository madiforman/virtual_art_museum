"""
Module for testing the async_utils module

Tests
----------
    test_check_europeana_response
    test_fetch
    test_filter_objects
"""
import unittest
from unittest.mock import Mock, patch

import asyncio
import aiohttp
from data_aquisition.async_utils import (
    check_europeana_response,
    fetch,
    filter_objects
)
import pandas as pd

class TestAsyncUtils(unittest.TestCase):
    """
    Test the async_utils module
    """
    def test_check_europeana_response(self):
        """
        Test the check_europeana_response function

        Tests
        -----
        valid dropbox URL with valid content
        valid dropbox URL with invalid content
        non-dropbox URL
        """
        # Test valid dropbox URL with valid content
        url = "https://www.dropbox.com/valid/image.jpg"
        content = b'\x89PNG\r\n\x1a\n\x00\x00'
        self.assertEqual(check_europeana_response(url, content), url)

        # Test valid dropbox URL with invalid content
        content = b'<!DOCTYPE html>'
        self.assertEqual(check_europeana_response(url, content), "")

        # Test non-dropbox URL
        url = "https://example.com/image.jpg"
        self.assertEqual(check_europeana_response(url, content), url)

    async def test_fetch(self):
        """
        Test the fetch function

        Tests
        -----
        MET API success case
        MET API no image case
        invalid source
        EUROPEANA API success case
        EUROPEANA API no image case
        """
        # Mock session for testing
        mock_session = Mock(spec=aiohttp.ClientSession)

        # Test MET API success case
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = asyncio.coroutine(
                            lambda: {"primaryImage": "http://example.com/image.jpg"}
                            )

        # following line is needed to mock the async context manager
        mock_session.get.return_value.__aenter__.return_value = mock_response
        result = await fetch(mock_session, "http://api.met.com/object/123", "MET")
        self.assertEqual(result, "http://example.com/image.jpg")

        # Test MET API no image case
        mock_response.json = asyncio.coroutine(lambda: {"primaryImage": ""})
        result = await fetch(mock_session, "http://api.met.com/object/123", "MET")
        self.assertEqual(result, "")

        # Test invalid source
        with self.assertRaises(ValueError):
            await fetch(mock_session, "http://example.com", "INVALID")

        # Following tests are for EUROPEANA cases

        # Test case 1: Valid non-dropbox URL
        regular_url = "https://example.com/image.jpg"
        mock_session.get.return_value.__aenter__.return_value = mock_response
        result = await fetch(mock_session, regular_url, "EUROPEANA")
        self.assertEqual(result, regular_url)

        # Test case 2: Valid dropbox URL with valid content
        dropbox_url = "https://www.dropbox.com/valid/image.jpg"
        mock_response.content = Mock()
        mock_response.content.read = asyncio.coroutine(lambda _: b'\x89PNG\r\n\x1a\n\x00\x00')
        result = await fetch(mock_session, dropbox_url, "EUROPEANA")
        self.assertEqual(result, dropbox_url)

        # Test case 3: Dropbox URL with invalid content (HTML)
        mock_response.content.read = asyncio.coroutine(lambda _: b'<!DOCTYPE html>')
        result = await fetch(mock_session, dropbox_url, "EUROPEANA")
        self.assertEqual(result, "")

        # Test case 4: Failed request (non-200 status)
        mock_response.status = 404
        result = await fetch(mock_session, regular_url, "EUROPEANA")
        self.assertEqual(result, "")

    def test_filter_objects(self):
        """
        Test the filter_objects function to ensure it filters the objects correctly

        Tests
        -----
        MET data
        EUROPEANA data
        """
        # Test MET data
        met_data = pd.DataFrame({
            'Object ID': [1, 2, 3],
            'Title': ['A', 'B', 'C']
        })

        with patch('data_aquisition.async_utils.run') as mock_run:
            mock_run.return_value = pd.DataFrame({
                'Object ID': [1, 2],
                'Title': ['A', 'B'],
                'image_url': ['url1', 'url2']
            })

            result = filter_objects(met_data, "MET")
            self.assertEqual(len(result), 2)
            self.assertTrue('image_url' in result.columns)
