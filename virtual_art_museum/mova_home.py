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

import random
import math
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# pylint: disable= import-error, 
from data_aquisition.met_museum import MetMuseum

met_path = os.path.join(current_dir, 'data_aquisition', 'MetObjects_final.csv')
met = MetMuseum(met_path)
data = met.get_n_random_objs(18)

# CULTURES = ['American', 'British', 'Bohemian', 'Canadian', 'Chinese', 'Dutch', 
#    'European', 'French', 'Finnish', 'Flemish', 'German', - madi will work on this

def image_processing_met(data):
    '''
    Processes MET dataset to make it readable for later functions.

    Processing steps:
        - Filter out irrelevant columns
        - Change 'Repository' values to 'MET'
        - Rename columns to be more readable
        - Replace None values with [column name] unknown
        - Split delimited values into a list
        - Create a century column based on the years?
    '''
    data = data[['Object Number', 'Title', 'Culture', 'Artist Display Name', 
                 'Artist Display Bio', 'Object Begin Date', 'Medium', 'Dimensions',
                'Repository', 'Tags', 'image_url']]

    data['Repository'] = 'MET'
    data['Object Begin Date'] = data['Object Begin Date'].astype(int)

    data.rename(columns = {'Artist Display Name' : 'Artist',
                           'Artist Display Bio' : 'Artist biographic information',
                           'Object Begin Date' : 'Year'}, inplace=True)

    for col in data.columns:
            
        if not col == 'Tags' or col == 'Culture':
            data[col] = data[col].apply(
                lambda x: f"{col} unknown" if pd.isna(x) or x == ' ' else x
            )
            
        if isinstance(data[col].iloc[0], str) and '|' in data[col].iloc[0]:
            data[col] = data[col].apply(
                lambda x: [item.strip() for item in x.split('|')] if isinstance(x, str) else []
            )    
            
    return data


def image_processing_europeana(data):
    ## do something
    return

def blend_datasources(met_data, europeana_data):
    """
    Takes the pre-processed MET and Europeana datasets,
    randomly combines them, and orders them according to height.
    For odd number rows, tallest photo should be in the center;
    for even number rows, shortest photo is centered.
    """
    return

def page_setup():
    """ Page configuation """
    st.set_page_config(
        page_title="MoVA",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

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

def sidebar_setup():
    """ Sidebar configuration """

    # initialize session state values
    if 'filters_reset' not in st.session_state:
        st.session_state.filters_reset = False
    if 'search' not in st.session_state:
        st.session_state.search = ''
    if 'culture' not in st.session_state:
        st.session_state.culture = []
    if 'years' not in st.session_state:
        st.session_state.years = (min(data['Year'].astype(int)), max(data['Year'].astype(int)))
    if 'datasource' not in st.session_state:
        st.session_state.datasource = None

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

    for row in range(rows):
        pics = st.columns([3,3,3], gap='medium', vertical_alignment='center')
        for pic in pics:
            with pic:
                #splitting in case we want to add more to the caption
                caption = data.iloc[i, 1]
                st.image(data.iloc[i,-1], caption=caption)
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium', vertical_alignment='center')
        for j in range(leftovers):
            with lastrow[j]:
                caption = data.iloc[i,1]
                st.image(data.iloc[i,-1], caption=caption)
                i += 1

data = image_processing_met(data)
page_setup()
sidebar_setup()
image_gallery(data)