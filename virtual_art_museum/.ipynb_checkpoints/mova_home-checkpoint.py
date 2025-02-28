import streamlit as st
import pandas as pd
import random
import math
import os


# Page and Sidebar configuation
st.set_page_config(
    page_title="MoVA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

data = pd.DataFrame({
    'title': ['Vétheuil in Summer', 
              'Madonna and Child', 
              'View of Genzano with a Rider and Peasant', 
              'Diana Leaving for the Hunt', 
              'The Marriage of Cupid and Psyche',
              'Mrs. Walter Rathbone Bacon',
              'The Rehearsal Onstage',
              'The Nightingale Sings',  
              'Potted Pansies'],
    'artist': ['Claude Monet',
               'Simon Vouet',  
               'Boccaccio Boccaccino', 
               'Camille Corot',
               'Andrea Schiavone',
               'Anders Zorn', 
               'Edgar Degas',
               'Mikhail Vasilievich Nesterov',  
               'Henri Fantin-Latour'],
    'year': [1880, 1506, 1843, 1635, 1540, 1897, 1874, 1923, 1883],
    'medium': ['Oil', 'Oil', 'Oil', 'Oil', 'Oil', 'Oil', 'Ink', 'Oil', 'Oil'],
    'datasource': ['MET', 'Europeana', 'MET', 'Europeana', 'Europeana', 'MET', 'MET', 'Europeana', 'MET'],
    'image': ['https://collectionapi.metmuseum.org/api/collection/v1/iiif/437111/796133/restricted', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/435682/789857/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/439360/799573/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/890822/2151253/restricted', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/437638/801063/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/437966/796372/main-image',  'https://collectionapi.metmuseum.org/api/collection/v1/iiif/436156/795921/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/437198/2056636/restricted',  'https://collectionapi.metmuseum.org/api/collection/v1/iiif/629928/1350639/main-image']
}) 

st.logo("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA%20bw%20logo.png?raw=true", size="large")

if 'filters_reset' not in st.session_state:
    st.session_state.filters_reset = False
if 'search' not in st.session_state:
    st.session_state.search = ''
if 'medium' not in st.session_state:
    st.session_state.medium = []
if 'years' not in st.session_state:
    st.session_state.years = (min(data['year']), max(data['year']))
if 'datasource' not in st.session_state:
    st.session_state.datasource = None

st.sidebar.header('Advanced filters')

reset_button = st.sidebar.button('Reset Filters')
if reset_button:
    st.session_state.filters_reset = True
    st.session_state.search = ''
    st.session_state.medium = []
    st.session_state.years = (min(data['year']), max(data['year']))
    st.session_state.datasource = None
    st.rerun()

search = st.sidebar.text_input("🔍︎ Search by keyword: ", value=st.session_state.search)

medium_list = data['medium'].unique().tolist()
medium = st.sidebar.multiselect("Mediums: ", medium_list, default=st.session_state.medium)

years = st.sidebar.slider('Time Period: ', 
                          min_value=min(data['year']),
                          max_value=max(data['year']),
                          value=st.session_state.years)

datasource = st.sidebar.radio('Datasource: ', ['MET', 'Europeana'], index=None if st.session_state.get('datasource', None) is None else ['MET', 'Europeana'].index(st.session_state.datasource))

st.session_state.search = search
st.session_state.medium = medium
st.session_state.years = years
st.session_state.datasource = datasource

# Header configuation
col1, col2, col3 = st.columns([20,1,1])

with col1:
    st.image("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA_logo.png?raw=true", width=400)

with col2:
    st.page_link("https://catgdp.streamlit.app/", label='##', icon='✨', help='Favorites')

with col3:
    if(st.button("📊")):
        with st.spinner():
            st.write('Done')
    
st.markdown("#")  
st.markdown("#")

def image_processing_europeana(data):
    for row in data:
        if type(data.loc[row, 'year']) != int:
            year = data.loc[row, 'year']

def image_processing_met(data):
    ## do something
    return
    
def blend_datasources(met_data, europeana_data):
    # randomize the datasources for the display
    return

# Filtered data
def filter_data(data):
    if search:
        mask = False
        for column in data.columns:
            # create a boolean mask for which data points contain search parameter
            mask = mask | data[column].astype(str).str.contains(search, case=False, na=False)
        data = data[mask]

    if medium:
        data = data[data['medium'].isin(medium)]

    data = data[(data['year'] >= years[0]) & (data['year'] <= years[1])]

    if datasource == 'MET':
        data = data[data['datasource'] == 'MET']
    elif datasource == 'Europeana':
        data = data[data['datasource'] == 'Europeana']
    

# Printing images
def image_gallery(data):
    n = len(data)
    rows = n // 3
    i = 0

    for row in range(rows):
        pics = st.columns([3,3,3], vertical_alignment='center')
        for pic in pics:
            with pic:
                #splitting in case we want to add more to the caption
                caption = data.iloc[i, 0]
                st.image(data.iloc[i,5], caption=caption)
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium')
        for j in range(leftovers):
            with lastrow[j]:
                caption = data.iloc[i,0]
                st.image(data.iloc[i,5], caption=caption)
                i += 1
                
image_gallery(filtered)