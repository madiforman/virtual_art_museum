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

import random
import math
import os


current_dir = os.path.dirname(os.path.abspath(__file__))

met_path = os.path.join(current_dir, 'data_aquisition', 'MetObjects_final.csv')
met = MetMuseum(met_path)
data = met.get_n_random_objs(9)

def image_processing_met(data):
    data = data[['Object Number', 'Title', 'Culture', 'Artist Display Name', 
                 'Artist Display Bio', 'Object Begin Date', 'Medium', 'Dimensions',
                'Repository', 'Tags', 'image_url']]

    data['Repository'] = 'MET'
    data['Object Begin Date'] = data['Object Begin Date'].astype(int)

    data.rename(columns = {'Artist Display Name' : 'Artist',
                           'Artist Display Bio' : 'Artist biographic information',
                           'Object Begin Date' : 'Year'}, inplace=True)

    for col in data.columns:
        if not col == 'Tags':
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
    if 'medium' not in st.session_state:
        st.session_state.medium = []
    if 'years' not in st.session_state:
        st.session_state.years = (int(min(data['Year'])), int(max(data['Year'])))
    if 'datasource' not in st.session_state:
        st.session_state.datasource = None

    st.sidebar.header('Advanced filters')

    reset_button = st.sidebar.button('Reset Filters')
    # reset filters when clicked
    if reset_button:
        st.session_state.filters_reset = True
        st.session_state.search = ''
        st.session_state.medium = []
        st.session_state.years = (int(min(data['Year'])), int(max(data['Year'])))
        st.session_state.datasource = None
        st.rerun()

    search = st.sidebar.text_input("🔍︎ Search by keyword: ", value=st.session_state.search)

    medium_list = ['idk man', 'just trying my best', 'hope this works']
    medium = st.sidebar.multiselect("Mediums: ", medium_list, 
                                    default=st.session_state.medium)

    years = st.sidebar.slider('Time Period: ', 
                              min_value = int(min(data['Year'])),
                              max_value = int(max(data['Year'])),
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

    if st.session_state.medium:
        data = data[data['medium'].isin(st.session_state.medium)]

    data = data[(data['year'] >= st.session_state.years[0]) & (data['year'] <= st.session_state.years[1])]

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
# sidebar_setup() this little b*tch is having an issue with the years
st.write(data)
image_gallery(data)