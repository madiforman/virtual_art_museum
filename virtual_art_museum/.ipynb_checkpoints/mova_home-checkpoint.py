"""
MoVA homepage:
    - Configures page / sidebar components
    - Allows user to add / reset filters for data
    - Processes MET and Europeana data
    - Blends the data and sorts images by size
    - Filters data based on user input
    - Displays images
"""
import time

import streamlit as st
import pandas as pd
import numpy as np

from math import ceil

import random
import math
import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))

#MET_PATH = os.path.join(base_dir, "data", "MetObjects_final_filtered_processed.csv")
#EUROPEANA_PATH = os.path.join(base_dir, "data", "Europeana_data_processed.csv")
BLENDED_PATH = os.path.join(base_dir, "data", "blended_data.csv")

 # Caches the result so it doesn't reload every time Streamlit reruns
@st.cache_data
def load_blended_cached(path: str, sample_size: int = 10000) -> pd.DataFrame:
    """
    Loads stratified sample of data with repository proportions assuming 80% MET and 20% Europeana.

    Parameters:
        path (str): Path to the data file
        sample_size (int): Number of rows to sample
    ----------
    Returns:
        pd.DataFrame: A dataframe containing the sampled data
    """
    try:
        repo_proportions = {
            'MET': 0.8,        # Assuming 80% of data is MET
            'Europeana': 0.2   # Assuming 20% is Europeana
        }
        # # samples per repository
        samples_per_repo = {
            repo: int(sample_size * prop)
            for repo, prop in repo_proportions.items()
        }
        # Sample from each repository
        samples = [
            pd.read_csv(path).query(f"Repository == '{repo}'").sample(n=count, random_state=42)
            for repo, count in samples_per_repo.items()
        ]
        # Combine and shuffle
        final_df = pd.concat(samples, ignore_index=True).sample(frac=1, random_state=42)
        #print(f"Loaded {len(final_df)} rows\n{final_df['Repository'].value_counts()}")
        return final_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def initialize_session_state(data):
    ''' Initialze session state variables '''
    if 'search' not in st.session_state:
        st.session_state.search = ''
    if 'culture' not in st.session_state:
        st.session_state.culture = []
    if 'years' not in st.session_state:
        st.session_state.years = (min(data['Year'].astype(int)), 2025)
    if 'datasource' not in st.session_state:
        st.session_state.datasource = None
    
def reset_filters(data):
    ''' Resets all filters to default values '''
    st.session_state.search = ''
    st.session_state.culture = []
    st.session_state.years = (min(data['Year'].astype(int)), 2025)
    st.session_state.datasource = None

def refresh_data():
    ''' Clear cached data and rerun app '''
    load_blended_cached.clear()

    if 'original_data' in st.session_state:
        del st.session_state['original_data']
    
    st.rerun()

@st.cache_data
def filter_data(data, search, culture, years, datasource):
    """ Filters the dataframe based on user inputs """
    if search:
        mask = False
        for column in data.columns:
            # create a boolean mask for which data points contain search parameter
            mask = mask | data[column].astype(str).str.contains(search, 
                                                                case=False, na=False)
        data = data[mask]

    if culture:
        data = data[data['Culture'].isin(culture)]

    data = data[(data['Year'] >= years[0]) & (data['Year'] <= years[1])]

    if datasource == 'MET':
        data = data[data['Repository'] == 'MET']
    elif datasource == 'Europeana':
        data = data[data['Repository'] == 'Europeana']

    return data

def sidebar_setup(data):
    ''' Sets up the sidebar UI '''
    st.sidebar.header('Advanced filters')

    reset_button = st.sidebar.button('Reset Filters', on_click=reset_filters, args=(data,))

    search = st.sidebar.text_input("🔍︎ Search by keyword: ",
                                   key = "search")

    all_cultures = data["Culture"].unique().tolist()
    culture_list = [culture for culture in all_cultures if culture != 'Culture unknown']
    culture = st.sidebar.multiselect("Culture: ",
                                     culture_list,
                                     key="culture")

    years = st.sidebar.slider('Time Period: ', 
                              min_value = min(data['Year'].astype(int)),
                              max_value = 2025,
                              key = "years")

    datasource = st.sidebar.radio('Datasource: ',
                                  ['MET', 'Europeana'], 
                                  index = None,
                                  key = "datasource")

def image_gallery(data):
    """
    Prints images in 1x3 rows alongside their captions
    For the final row, prints the number of images left (1X1 or 1x2)
    """
    n = len(data)
    rows = n // 3
    # initialize iterator for row value
    i = 0

    image_index = data.columns.tolist().index('image_url')
    title_index = data.columns.tolist().index('Title')

    for row in range(rows):
        pics = st.columns([3,3,3], gap='medium', vertical_alignment='center')
        for pic in pics:
            with pic:
                caption = data.iloc[i, title_index]
                st.image(data.iloc[i, image_index], caption=caption)
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium', vertical_alignment='center')
        for j in range(leftovers):
            with lastrow[j]:
                caption = data.iloc[i, title_index]
                st.image(data.iloc[i, image_index], caption=caption)
                i += 1
    
def homepage():
    ''' Initializes the UI and layout of the homepage '''
    st.set_page_config(
        page_title="MoVA",
        layout="wide",
        initial_sidebar_state="collapsed")

    if 'original_data' not in st.session_state:
        st.session_state.original_data = load_blended_cached(BLENDED_PATH).sample(n=100)

    initialize_session_state(st.session_state.original_data)

    st.logo("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA%20bw%20logo.png?raw=true",
        size="large")

    col1, col2, col3 = st.columns([20,1,1])

    with col1:
        st.image("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA_logo.png?raw=true",
                width=400)

    with col2:
        # Replace w/ Zhansaya's page link?
        st.page_link("https://catgdp.streamlit.app/", label='##', icon='✨', help='Favorites')

    with col3:
        reset = st.button('↻', on_click = refresh_data, help='Refresh data')
    
    st.markdown("#")  
    st.markdown("#")
    
    sidebar_setup(st.session_state.original_data)

    filtered_data = filter_data(
        st.session_state.original_data,
        st.session_state.search,
        st.session_state.culture,
        st.session_state.years,
        st.session_state.datasource
    )

    image_gallery(filtered_data)



def main():
    homepage()

if __name__ == "__main__":
    main()

