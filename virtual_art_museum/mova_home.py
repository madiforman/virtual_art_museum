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

MET_PATH = os.path.join(base_dir, "data", "MetObjects_final_filtered_processed.csv")
EUROPEANA_PATH = os.path.join(base_dir, "data", "Europeana_data_processed.csv")
BLENDED_PATH = os.path.join(base_dir, "data", "blended_data.csv")

@st.cache_data # Caches the result so it doesn't reload every time Streamlit reruns
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
        print(f"Loaded {len(final_df)} rows\n{final_df['Repository'].value_counts()}")
        return final_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# def blend_datasources(met_data, europeana_data):
#     """
#     Takes the pre-processed MET and Europeana datasets,
#     ensures they follow the same format, randomly 
#     combines them, and orders them according to height.
#     For odd number rows, tallest photo should be in the center;
#     for even number rows, shortest photo is centered.
#     """
#     combined = pd.concat([met_data, europeana_data], ignore_index=True)
#     combined = combined.sample(frac=1).reset_index(drop=True)
#     return combined

def page_setup():
    """ Page configuation """
    st.set_page_config(
        page_title="MoVA",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    if 'filters_reset' not in st.session_state:
        st.session_state.filters_reset = False
    if 'search' not in st.session_state:
        st.session_state.search = ''
    if 'culture' not in st.session_state:
        st.session_state.culture = []
    #if 'years' not in st.session_state:
        #st.session_state.years = (min(data['Year'].astype(int)), max(data['Year'].astype(int)))
    if 'datasource' not in st.session_state:
        st.session_state.datasource = None

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
        if(st.button("📊")):
            with st.spinner():
                time.sleep(15)
                st.write('Done')
    
    st.markdown("#")  
    st.markdown("#")

def sidebar_setup(data):
    """ Sidebar configuration """
    
    st.sidebar.header('Advanced filters')

    reset_button = st.sidebar.button('Reset Filters')
    # reset filters when clicked
    if reset_button:
        st.session_state.filters_reset = True
        st.session_state.search = ''
        st.session_state.culture = []
        st.session_state.years = (min(data['Year'].astype(int)), max(data['Year'].astype(int)))
        st.session_state.datasource = None
        st.rerun()

    search = st.sidebar.text_input("🔍︎ Search by keyword: ", value=st.session_state.search)

    culture_list = data["Culture"].unique().tolist()
    culture = st.sidebar.multiselect("Culture: ", culture_list, 
                                    default=st.session_state.culture)

    years = st.sidebar.slider('Time Period: ', 
                              min_value = min(data['Year'].astype(int)),
                              max_value = max(data['Year'].astype(int)),
                              value=st.session_state.years)

    datasource = st.sidebar.radio('Datasource: ', ['MET', 'Europeana'], 
                                  index=None if st.session_state.get('datasource', None) is None 
                                  else ['MET', 'Europeana'].index(st.session_state.datasource)) 

def filter_data(data):
    """
    Filters the combined dataframe based on user inputs
    """
    
    if st.session_state.search:
        mask = False
        for column in data.columns:
            # create a boolean mask for which data points contain search parameter
            mask = mask | data[column].astype(str).str.contains(st.session_state.search, 
                                                                case=False, na=False)
        data = data[mask]

    if st.session_state.culture:
        data = data[data['Culture'].isin(st.session_state.culture)]

    data = data[(data['Year'] >= st.session_state.years[0]) & (data['Year'] <= st.session_state.years[1])]

    if st.session_state.datasource == 'MET':
        data = data[data['datasource'] == 'MET']
    elif st.session_state.datasource == 'Europeana':
        data = data[data['datasource'] == 'Europeana']

    return data

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
                #splitting in case we want to add more to the caption
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

def main():
    page_setup()
    print("Loading data")
    data = load_blended_cached(BLENDED_PATH)
    # sidebar_setup(data)
    image_gallery(data.sample(n=100))


if __name__ == "__main__":
    main()