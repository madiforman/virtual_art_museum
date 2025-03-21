"""
MoVA homepage:
    - Configures page / sidebar components
    - Allows user to add / reset filters for data
    - Processes MET and Europeana data
    - Blends the data and sorts images by size
    - Filters data based on user input
    - Displays images
    - Adds to Favorites
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

from popup import display_artwork_popup

base_dir = os.path.dirname(os.path.abspath(__file__))

MET_PATH = os.path.join(base_dir, "data", "MetObjects_final_filtered_processed.csv")
EUROPEANA_PATH = os.path.join(base_dir, "data", "Europeana_data_processed.csv")
BLENDED_PATH = os.path.join(base_dir, "data", "blended_data.csv")

# Caches the result so it doesn't reload every time Streamlit reruns
@st.cache_data
def load_blended_cached(path1: str, path2: str, sample_size: int = 1000) -> pd.DataFrame:
    """
    Loads stratified sample of data with repository proportions assuming 80% MET and 20% Europeana.

    Parameters:
        path (str): Path to the data file
        sample_size (int): Number of rows to sample
    ----------
    Returns:
        pd.DataFrame: A dataframe containing the sampled data
    """
    repo_proportions = {
        'MET': 0.7,        # Stratified sample since we know we have less Europeana data
        'Europeana': 0.3   
    }
    # samples per repository
    samples_per_repo = {
        repo: int(sample_size * prop)
        for repo, prop in repo_proportions.items()
    }
    # Sample from each repository
    samples = [
        pd.read_csv(path1).sample(n=samples_per_repo['MET']),
        pd.read_csv(path2).sample(n=samples_per_repo['Europeana'])
    ]
    # Combine and shuffle
    final_df = pd.concat(samples, ignore_index=True).sample(frac=1, random_state=42)
    print(f"Loaded {len(final_df)} rows\n{final_df['Repository'].value_counts()}")
    return final_df


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
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []    
    
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
    ''' Adds Favorited and Popup Functionality'''
    cols = st.columns(4, gap='medium')
    for idx, artwork in enumerate(data.itertuples()):
        with cols[idx % 4]:
            with st.container():
                st.markdown(f"""
                    <div style='cursor: pointer; transition: transform 0.2s;'
                         onmouseover='this.style.transform="scale(1.02)"'
                         onmouseout='this.style.transform="scale(1)"'>
                        <img src='{artwork.image_url}' style='width: 100%; border-radius: 5px;'>
                    </div>
                """, unsafe_allow_html=True)
            
            st.caption(f"{artwork.Title[:50]}")
            
            # Add to Favorites button
            if st.button(f"Add to Favorites ❤️", key=f"fav_{idx}", use_container_width=True):
                # Store the artwork data as a dictionary
                artwork_dict = {
                    'image_url': artwork.image_url,
                    'Title': artwork.Title
                }
                if artwork_dict not in st.session_state.favorites:
                    st.session_state.favorites.append(artwork_dict)
                    st.success(f"Added '{artwork.Title[:50]}' to favorites!")
                else:
                    st.warning("This artwork is already in your favorites.")

            if st.button(f"Details", key=f"btn_{idx}", use_container_width=True):
                artwork_dict = data.iloc[idx].to_dict()
                display_artwork_popup(artwork_dict)

def display_favorites(data):
    ''' Displays the user's favorited artworks '''
    if not st.session_state.favorites:
        st.write("You have no favorites yet. Add some artworks to your favorites!")
    else:
        st.write("### Your Favorites")
        favorite_data = data[data.index.isin(st.session_state.favorites)]
        image_gallery(favorite_data)

def homepage(path1: str, path2: str):
    ''' Initializes the UI and layout of the homepage '''
    st.set_page_config(
        page_title="MoVA",
        layout="wide",
        initial_sidebar_state="collapsed")

    if 'original_data' not in st.session_state:
        st.session_state.original_data = load_blended_cached(path1, path2).sample(n=250)

    initialize_session_state(st.session_state.original_data)

    st.logo("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA%20bw%20logo.png?raw=true",
        size="large")

    col1, col2, col3 = st.columns([20,1,1])

    with col1:
        st.image("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA_logo.png?raw=true",
                width=300)

    with col2:
        if st.button("❤️"):
            st.switch_page("Pages/favorites.py")

    with col3:
        reset = st.button('↻', on_click = refresh_data, help = 'Refresh data')
    
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
    homepage(MET_PATH, EUROPEANA_PATH)

if __name__ == "__main__":
    main()
