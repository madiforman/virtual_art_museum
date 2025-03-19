import unittest
import sys
import os
from unittest.mock import patch, MagicMock, call
from io import StringIO
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mova_home import image_gallery, homepage, load_blended_cached, initialize_session_state
from mova_home import sidebar_setup, filter_data, refresh_data, reset_filters

from mova_home import BLENDED_PATH

class TestMovaHome(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_load_blended_cached_success(self, mock_read_csv):
        ''' Tests the load_blended_cached function '''
        met_data = pd.DataFrame({
            'Repository': ['MET'] * 1000,
            'Title': [f'MET Item {i}' for i in range(1000)],
            'Year': [2000 + i % 25 for i in range(1000)]
        })
        
        europeana_data = pd.DataFrame({
            'Repository': ['Europeana'] * 500,
            'Title': [f'Europeana Item {i}' for i in range(500)],
            'Year': [1900 + i % 50 for i in range(500)]
        })
        
        full_data = pd.concat([met_data, europeana_data], ignore_index=True)
        mock_read_csv.return_value = full_data
        
        met_query_result = met_data.copy()
        europeana_query_result = europeana_data.copy()
        
        met_sample_result = met_data.iloc[:800].copy()
        europeana_sample_result = europeana_data.iloc[:200].copy()
        
        def mock_query(query_string):
            if "Repository == 'MET'" in query_string:
                return met_query_result
            elif "Repository == 'Europeana'" in query_string:
                return europeana_query_result
            return pd.DataFrame()
        
        full_data.query = MagicMock(side_effect=mock_query)

        met_query_result.sample = MagicMock(return_value=met_sample_result)
        europeana_query_result.sample = MagicMock(return_value=europeana_sample_result)
        
        result = load_blended_cached("test_path.csv", sample_size=1000)
        
        self.assertEqual(len(result), 1000)
        
        mock_read_csv.assert_called_once_with("test_path.csv")
        
        full_data.query.assert_any_call("Repository == 'MET'")
        full_data.query.assert_any_call("Repository == 'Europeana'")
        
        full_data_met.sample.assert_called_once_with(n=800, random_state=42)
        full_data_europeana.sample.assert_called_once_with(n=200, random_state=42)
    
    @patch('pandas.read_csv')
    @patch('streamlit.error')
    def test_load_blended_cached_file_not_found(self, mock_error, mock_read_csv):
        ''' Tests for when the file is not found '''
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        
        result = load_blended_cached("non_existent_file.csv")
        
        self.assertTrue(result.empty)
        mock_error.assert_called_once()
        self.assertIn("Error loading data", mock_error.call_args[0][0])
    
    @patch('pandas.read_csv')
    @patch('streamlit.error')
    def test_load_blended_cached_invalid_file_format(self, mock_error, mock_read_csv):
        ''' Tests for parsing error handling '''
        mock_read_csv.side_effect = pd.errors.ParserError("Error parsing file")
        
        result = load_blended_cached("invalid_format.csv")
        
        self.assertTrue(result.empty) 
        mock_error.assert_called_once()
        self.assertIn("Error loading data", mock_error.call_args[0][0])
    
    @patch('pandas.read_csv')
    def test_load_blended_cached_custom_sample_size(self, mock_read_csv):
        ''' Tests load_blended_cached with custom sample size '''
        met_data = pd.DataFrame({
            'Repository': ['MET'] * 5000,
            'Title': [f'MET Item {i}' for i in range(5000)]
        })
        
        europeana_data = pd.DataFrame({
            'Repository': ['Europeana'] * 2000,
            'Title': [f'Europeana Item {i}' for i in range(2000)]
        })
        
        full_data = pd.concat([met_data, europeana_data], ignore_index=True)
        mock_read_csv.return_value = full_data
        
        met_query_result = met_data.copy()
        europeana_query_result = europeana_data.copy()
        
        met_sample_result = met_data.iloc[:4000].copy()
        europeana_sample_result = europeana_data.iloc[:1000].copy()
        
        def mock_query(query_string):
            if "Repository == 'MET'" in query_string:
                return met_query_result
            elif "Repository == 'Europeana'" in query_string:
                return europeana_query_result
            return pd.DataFrame()
        
        full_data.query = MagicMock(side_effect=mock_query)

        met_query_result.sample = MagicMock(return_value=met_sample_result)
        europeana_query_result.sample = MagicMock(return_value=europeana_sample_result)
        
        result = load_blended_cached("test_path.csv", sample_size=5000)
        
        met_query_result.sample.assert_called_once_with(n=4000, random_state=42)
        europeana_query_result.sample.assert_called_once_with(n=1000, random_state=42)
    
    @patch('pandas.read_csv')
    @patch('streamlit.error')
    def test_load_blended_cached_missing_repository_column(self, mock_error, mock_read_csv):
        ''' Tests load_blended_cached when Repository is missing '''
        invalid_data = pd.DataFrame({
            'Title': [f'Item {i}' for i in range(100)],
            'Year': [2000 + i % 25 for i in range(100)]
        })
        
        mock_read_csv.return_value = invalid_data
        
        result = load_blended_cached("test_path.csv")
        
        self.assertTrue(result.empty)
        mock_error.assert_called_once()
        self.assertIn("Error loading data", mock_error.call_args[0][0])
    
    def test_initialize_empty_session_state(self):
        ''' Tests the session state function '''
        data = pd.DataFrame({'Year': [2010, 2015, 2020]})

        session_state_mock = {}
        
        with patch('streamlit.session_state', session_state_mock):
            initialize_session_state(data)
            
            self.assertEqual(session_state_mock['search'], '')
            self.assertEqual(session_state_mock['culture'], [])
            self.assertEqual(session_state_mock['years'], (2010, 2025))
            self.assertIsNone(session_state_mock['datasource'])
    
    def test_preserves_existing_values(self):
        ''' Tests that existing values are preserved '''
        data = pd.DataFrame({'Year': [2012, 2018, 2022]})
        
        session_state_mock = {'search': 'existing search'}
        
        with patch('streamlit.session_state', session_state_mock):
            initialize_session_state(data)
            
            self.assertEqual(session_state_mock['search'], 'existing search') # should be preserved
            self.assertEqual(session_state_mock['culture'], [])
            self.assertEqual(session_state_mock['years'], (2012, 2025))
            self.assertIsNone(session_state_mock['datasource'])
    
    def test_reset_filters(self):
        ''' Tests the reset_filters function '''
        data = pd.DataFrame({'Year': [2010, 2015, 2020]})
        
        session_state_mock = {
            'search': 'test', 
            'culture': ['Greek'], 
            'years': (1800, 1900), 
            'datasource': 'MET'
        }
        
        with patch('streamlit.session_state', session_state_mock):
            reset_filters(data)
            
            self.assertEqual(session_state_mock['search'], '')
            self.assertEqual(session_state_mock['culture'], [])
            self.assertEqual(session_state_mock['years'], (2010, 2025))
            self.assertIsNone(session_state_mock['datasource'])

    def test_refresh_data_with_original_data(self, mock_rerun):
        ''' Tests if cache was cleared and the file was reran '''
        session_state_mock = {'original_data': pd.DataFrame()}
        
        with patch('streamlit.session_state', session_state_mock), \
             patch('mova_home.load_blended_cached') as mock_load_blended, \
             patch('streamlit.rerun') as mock_rerun:
                
            mock_load_blended.clear = MagicMock()
            
            refresh_data()
            
            mock_load_blended.clear.assert_called_once()
            self.assertNotIn('original_data', session_state_mock)
            mock_rerun.assert_called_once()
    
    def test_filter_data_no_filters(self):
        ''' Tests filter_data when no filters passed '''
        data = pd.DataFrame({
            'Year': [2010, 2015, 2020],
            'Culture': ['Greek', 'Roman', 'Egyptian'],
            'Repository': ['MET', 'Europeana', 'MET'],
            'Title': ['Vase', 'Statue', 'Painting']
        })
        
        result = filter_data(data, '', [], (2000, 2025), None)
        
        pd.testing.assert_frame_equal(result, data)
    
    def test_filter_data_search(self):
        ''' Tests filter_data when search input passed '''
        data = pd.DataFrame({
            'Year': [2010, 2015, 2020],
            'Culture': ['Greek', 'Roman', 'Egyptian'],
            'Repository': ['MET', 'Europeana', 'MET'],
            'Title': ['Vase', 'Statue', 'Painting']
        })
        
        result = filter_data(data, 'vase', [], (2000, 2025), None)
        
        expected = data.iloc[[0]]
        pd.testing.assert_frame_equal(result, expected)
    
    def test_filter_data_culture(self):
        ''' Tests filter_data when culture input passed '''
        data = pd.DataFrame({
            'Year': [2010, 2015, 2020],
            'Culture': ['Greek', 'Roman', 'Egyptian'],
            'Repository': ['MET', 'Europeana', 'MET'],
            'Title': ['Vase', 'Statue', 'Painting']
        })
        
        result = filter_data(data, '', ['Greek', 'Egyptian'], (2000, 2025), None)
        
        expected = data.iloc[[0, 2]]
        pd.testing.assert_frame_equal(result, expected)
    
    def test_filter_data_years(self):
        ''' Tests filter_data when year input passed '''
        data = pd.DataFrame({
            'Year': [2010, 2015, 2020],
            'Culture': ['Greek', 'Roman', 'Egyptian'],
            'Repository': ['MET', 'Europeana', 'MET'],
            'Title': ['Vase', 'Statue', 'Painting']
        })
        
        result = filter_data(data, '', [], (2015, 2020), None)
        
        expected = data.iloc[[1, 2]]
        pd.testing.assert_frame_equal(result, expected)
    
    def test_filter_data_datasource_met(self):
        ''' Tests filter_data when Repository set to MET '''
        data = pd.DataFrame({
            'Year': [2010, 2015, 2020],
            'Culture': ['Greek', 'Roman', 'Egyptian'],
            'Repository': ['MET', 'Europeana', 'MET'],
            'Title': ['Vase', 'Statue', 'Painting']
        })
        
        result = filter_data(data, '', [], (2000, 2025), 'MET')
        
        expected = data.iloc[[0, 2]]
        pd.testing.assert_frame_equal(result, expected)
    
    def test_filter_data_datasource_europeana(self):
        ''' Tests filter_data when Repository set to Europeana '''
        data = pd.DataFrame({
            'Year': [2010, 2015, 2020],
            'Culture': ['Greek', 'Roman', 'Egyptian'],
            'Repository': ['MET', 'Europeana', 'MET'],
            'Title': ['Vase', 'Statue', 'Painting']
        })
        
        result = filter_data(data, '', [], (2000, 2025), 'Europeana')
        
        expected = data.iloc[[1]]
        pd.testing.assert_frame_equal(result, expected)
    
    def test_filter_data_combined_filters(self):
        ''' Tests filter_data when multiple inputs passed '''
        data = pd.DataFrame({
            'Year': [2010, 2015, 2020],
            'Culture': ['Greek', 'Roman', 'Egyptian'],
            'Repository': ['MET', 'Europeana', 'MET'],
            'Title': ['Vase', 'Statue', 'Painting']
        })
        
        result = filter_data(data, 'paint', ['Egyptian'], (2015, 2025), 'MET')
        
        expected = data.iloc[[2]]
        pd.testing.assert_frame_equal(result, expected)

    def test_sidebar_setup(self, mock_sidebar):
        ''' Tests sidebar is setup appropriately  '''
        data = pd.DataFrame({
            'Year': [2010, 2015, 2020],
            'Culture': ['Greek', 'Roman', 'Culture unknown'],
            'Repository': ['MET', 'Europeana', 'MET'],
            'Title': ['Vase', 'Statue', 'Painting']
        })
        
        with patch('streamlit.sidebar') as mock_sidebar:
            mock_header = MagicMock()
            mock_sidebar.header = mock_header
            
            mock_button = MagicMock()
            mock_sidebar.button = mock_button
            
            mock_text_input = MagicMock()
            mock_sidebar.text_input = mock_text_input
            
            mock_multiselect = MagicMock()
            mock_sidebar.multiselect = mock_multiselect
            
            mock_slider = MagicMock()
            mock_sidebar.slider = mock_slider
            
            mock_radio = MagicMock()
            mock_sidebar.radio = mock_radio
            
            sidebar_setup(data)
            
            mock_header.assert_called_once_with('Advanced filters')
            mock_button.assert_called_once()
            self.assertEqual(mock_button.call_args[0][0], 'Reset Filters')
            
            mock_text_input.assert_called_once()
            self.assertEqual(mock_text_input.call_args[0][0], '🔍︎ Search by keyword: ')
            self.assertEqual(mock_text_input.call_args[1]['key'], 'search')
            
            mock_multiselect.assert_called_once()
            self.assertEqual(mock_multiselect.call_args[0][0], 'Culture: ')
            self.assertEqual(sorted(mock_multiselect.call_args[0][1]), sorted(['Greek', 'Roman']))
            self.assertEqual(mock_multiselect.call_args[1]['key'], 'culture')
            
            mock_slider.assert_called_once()
            self.assertEqual(mock_slider.call_args[0][0], 'Time Period: ')
            self.assertEqual(mock_slider.call_args[1]['min_value'], 2010)
            self.assertEqual(mock_slider.call_args[1]['max_value'], 2025)
            self.assertEqual(mock_slider.call_args[1]['key'], 'years')
            
            mock_radio.assert_called_once()
            self.assertEqual(mock_radio.call_args[0][0], 'Datasource: ')
            self.assertEqual(mock_radio.call_args[0][1], ['MET', 'Europeana'])
            self.assertEqual(mock_radio.call_args[1]['index'], None)
            self.assertEqual(mock_radio.call_args[1]['key'], 'datasource')

    def test_image_gallery_renders_correct_number_of_artworks(self, mock_button, mock_caption, mock_markdown, mock_columns):
        ''' Tests the image_gallery function for sample data '''
        sample_data = pd.read_csv(StringIO("""
        id,Title,Artist,image_url
        1,Starry Night,Vincent van Gogh,https://example.com/starry_night.jpg
        2,Mona Lisa,Leonardo da Vinci,https://example.com/mona_lisa.jpg
        3,The Persistence of Memory,Salvador Dali,https://example.com/persistence_memory.jpg
        4,The Scream,Edvard Munch,https://example.com/scream.jpg
        5,Guernica,Pablo Picasso,https://example.com/guernica.jpg
        """))
        
        with patch('streamlit.columns') as mock_columns, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.caption') as mock_caption, \
             patch('streamlit.button') as mock_button:
            
            mock_col = MagicMock()
            mock_columns.return_value = [mock_col, mock_col, mock_col, mock_col]
            
            mock_button.return_value = False
            
            image_gallery(sample_data)
            
            mock_columns.assert_called_once_with(4, gap='medium')
            
            self.assertEqual(mock_markdown.call_count, 5)
            
            self.assertEqual(mock_caption.call_count, 5)
            
            self.assertEqual(mock_button.call_count, 5)

    def test_image_gallery_truncates_long_titles(self, mock_button, mock_caption, mock_markdown, mock_columns):
        ''' Verifies the image_gallery cleans the titles '''
        long_title_data = pd.DataFrame({
            'id': [1],
            'Title': ['This is a very long title that should be truncated by the function because it exceeds fifty characters'],
            'Artist': ['Test Artist'],
            'image_url': ['https://example.com/test.jpg']
        })
        
        with patch('streamlit.columns') as mock_columns, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.caption') as mock_caption, \
             patch('streamlit.button') as mock_button:
            
            mock_col = MagicMock()
            mock_columns.return_value = [mock_col, mock_col, mock_col, mock_col]
            
            mock_button.return_value = False
            
            expected_caption = 'This is a very long title that should be truncated'
            
            image_gallery(long_title_data)
            
            mock_caption.assert_called_once_with(expected_caption)

    def test_image_gallery_calls_popup_when_button_clicked(self, mock_popup, mock_button, mock_caption, mock_markdown, mock_columns):
        ''' Tests image_gallery when the button is clicked '''
        sample_data = pd.read_csv(StringIO("""
        id,Title,Artist,image_url
        1,Starry Night,Vincent van Gogh,https://example.com/starry_night.jpg
        2,Mona Lisa,Leonardo da Vinci,https://example.com/mona_lisa.jpg
        3,The Persistence of Memory,Salvador Dali,https://example.com/persistence_memory.jpg
        4,The Scream,Edvard Munch,https://example.com/scream.jpg
        5,Guernica,Pablo Picasso,https://example.com/guernica.jpg
        """))
        
        with patch('streamlit.columns') as mock_columns, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.caption') as mock_caption, \
             patch('streamlit.button') as mock_button, \
             patch('mova_home.display_artwork_popup') as mock_popup:
            
            mock_col = MagicMock()
            mock_columns.return_value = [mock_col, mock_col, mock_col, mock_col]
            
            mock_button.side_effect = [True, False, False, False, False]
            
            image_gallery(sample_data)
            
            mock_popup.assert_called_once()
            
            artwork_dict = mock_popup.call_args[0][0]
            
            self.assertEqual(artwork_dict['Title'], 'Starry Night')
            self.assertEqual(artwork_dict['Artist'], 'Vincent van Gogh')
            self.assertEqual(artwork_dict['image_url'], 'https://example.com/starry_night.jpg')

    def test_image_gallery_with_empty_dataframe(self, mock_button, mock_caption, mock_markdown, mock_columns):
        ''' Tests image_gallery when dataframe is blank '''
        empty_data = pd.DataFrame(columns=['id', 'Title', 'Artist', 'image_url'])
        
        with patch('streamlit.columns') as mock_columns, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.caption') as mock_caption, \
             patch('streamlit.button') as mock_button:
            
            mock_col = MagicMock()
            mock_columns.return_value = [mock_col, mock_col, mock_col, mock_col]
            
            image_gallery(empty_data)
            
            mock_columns.assert_called_once()

            # no other st functions should be called
            mock_markdown.assert_not_called()
            mock_caption.assert_not_called()
            mock_button.assert_not_called()

    def test_homepage_without_original_data(self, mock_markdown, mock_columns, mock_logo, mock_set_page_config):
        ''' Tests the homepage setup function '''
        session_state_mock = {}
        
        with patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.set_page_config') as mock_set_page_config, \
             patch('streamlit.logo') as mock_logo, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('mova_home.load_blended_cached') as mock_load_blended, \
             patch('mova_home.initialize_session_state') as mock_init_session, \
             patch('mova_home.sidebar_setup') as mock_sidebar, \
             patch('mova_home.filter_data') as mock_filter, \
             patch('mova_home.image_gallery') as mock_gallery:
        
            sample_data = pd.DataFrame({
                'Year': [2010, 2015, 2020],
                'Culture': ['Greek', 'Roman', 'Egyptian'],
                'Repository': ['MET', 'Europeana', 'MET'],
                'Title': ['Vase', 'Statue', 'Painting']
            })
            
            mock_load_blended.return_value = sample_data
            sample_data_sample = sample_data.copy()
            sample_data.sample = MagicMock(return_value=sample_data_sample)
            
            col1_mock = MagicMock()
            col2_mock = MagicMock()
            col3_mock = MagicMock()
            
            col1_mock.__enter__ = MagicMock(return_value=col1_mock)
            col1_mock.__exit__ = MagicMock(return_value=None)
            col1_mock.image = MagicMock()
            
            col2_mock.__enter__ = MagicMock(return_value=col2_mock)
            col2_mock.__exit__ = MagicMock(return_value=None)
            col2_mock.page_link = MagicMock()
            
            col3_mock.__enter__ = MagicMock(return_value=col3_mock)
            col3_mock.__exit__ = MagicMock(return_value=None)
            col3_mock.button = MagicMock()
            
            mock_columns.return_value = [col1_mock, col2_mock, col3_mock]
            
            mock_filter.return_value = sample_data
            
            homepage()
            
            mock_set_page_config.assert_called_once_with(
                page_title="MoVA",
                layout="wide",
                initial_sidebar_state="collapsed"
            )
            
            mock_load_blended.assert_called_once_with(BLENDED_PATH)
            sample_data.sample.assert_called_once_with(n=100)
            
            self.assertIn('original_data', session_state_mock)
            
            mock_init_session.assert_called_once()
            
            mock_logo.assert_called_once()
            
            mock_columns.assert_called_once_with([20, 1, 1])
            
            col1_mock.image.assert_called_once()
            col2_mock.page_link.assert_called_once()
            col3_mock.button.assert_called_once()
            
            # should be 1 -- madi updated
            self.assertEqual(mock_markdown.call_count, 1)
            
            mock_sidebar.assert_called_once()
            mock_filter.assert_called_once()
            mock_gallery.assert_called_once_with(sample_data)
    
    def test_homepage_with_existing_original_data(self, mock_markdown, mock_columns, mock_logo, mock_set_page_config):
        ''' Tests homepage functionality when original data already set '''
        existing_data = pd.DataFrame({'Year': [2010], 'Culture': ['Greek'], 'Repository': ['MET']})
        session_state_mock = {'original_data': existing_data}
        
        with patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.set_page_config') as mock_set_page_config, \
             patch('streamlit.logo') as mock_logo, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('mova_home.load_blended_cached') as mock_load_blended, \
             patch('mova_home.initialize_session_state') as mock_init_session, \
             patch('mova_home.sidebar_setup') as mock_sidebar, \
             patch('mova_home.filter_data') as mock_filter, \
             patch('mova_home.image_gallery') as mock_gallery:
            
            col1_mock = MagicMock()
            col2_mock = MagicMock()
            col3_mock = MagicMock()
            
            col1_mock.__enter__ = MagicMock(return_value=col1_mock)
            col1_mock.__exit__ = MagicMock()
            col1_mock.image = MagicMock()
            
            col2_mock.__enter__ = MagicMock(return_value=col2_mock)
            col2_mock.__exit__ = MagicMock()
            col2_mock.page_link = MagicMock()
            
            col3_mock.__enter__ = MagicMock(return_value=col3_mock)
            col3_mock.__exit__ = MagicMock()
            col3_mock.button = MagicMock()
            
            mock_columns.return_value = [col1_mock, col2_mock, col3_mock]

            mock_filter.return_value = existing_data
            
            homepage()
            
            mock_set_page_config.assert_called_once()
            
            # function should not be called
            load_blended_cached.assert_not_called()
            
            # should be called with existing data
            initialize_session_state.assert_called_once()
            
            mock_logo.assert_called_once()
            mock_columns.assert_called_once()
            
            col1_mock.image.assert_called_once() 
            col2_mock.page_link.assert_called_once()
            col3_mock.button.assert_called_once()
            
            self.assertEqual(mock_markdown.call_count, 1)
            
            sidebar_setup.assert_called_once()
            filter_data.assert_called_once()
            image_gallery.assert_called_once()

if __name__ == '__main__':
    unittest.main()