import streamlit as st
import pandas as pd
import random
import math
import os
import time


# Page and Sidebar configuation
st.set_page_config(
    page_title="MoVA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

data = pd.DataFrame({
    'title': ['Diana Leaving for the Hunt', 
              'Vétheuil in Summer', 
              'Madonna and Child', 
              'View of Genzano with a Rider and Peasant', 
              'Mrs. Walter Rathbone Bacon', 
              'The Marriage of Cupid and Psyche', 
              'The Nightingale Sings', 
              'The Rehearsal Onstage', 
              'Potted Pansies'],
    'artist': ['Simon Vouet', 
               'Claude Monet', 
               'Boccaccio Boccaccino', 
               'Camille Corot', 
               'Anders Zorn', 
               'Andrea Schiavone', 
               'Mikhail Vasilievich Nesterov', 
               'Edgar Degas', 
               'Henri Fantin-Latour'],
    'year': [1635, 1880, 1506, 1843, 1897, 1540, 1923, 1874, 1883],
    'medium': ['Oil', 'Oil', 'Oil', 'Oil', 'Oil', 'Oil', 'Oil', 'Ink', 'Oil'],
    'region': ['Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe'],
    'image': ['https://collectionapi.metmuseum.org/api/collection/v1/iiif/890822/2151253/restricted', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/437111/796133/restricted', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/435682/789857/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/439360/799573/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/437966/796372/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/437638/801063/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/437198/2056636/restricted', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/436156/795921/main-image', 'https://collectionapi.metmuseum.org/api/collection/v1/iiif/629928/1350639/main-image']
}) 

# q for Madi: should filters be affected by themselves?
st.logo("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA%20bw%20logo.png?raw=true", size="large")

if 'filters_reset' not in st.session_state:
    st.session_state.filters_reset = False

st.sidebar.header('Advanced filters')

<<<<<<< HEAD:streamlit_play.py
xbox = st.sidebar.button('Reset Filters')
if xbox:
    st.session_state.filters_reset = True
    st.session_state.search = ''
    st.session_state.medium = 'Oil'
    st.session_state.years = (min(data['year']), max(data['year']))
    st.session_state.region = None

search = st.sidebar.text_input("🔍︎ Search by keyword: ", value=st.session_state.get('search', ''))
=======
xbox = st.sidebar.button('Reset Filters', key='reset')
# if xbox:
#     st.session_state.reset = True
#     st.experimental_rerun()
# else:
#         st.session_state.reset = False
>>>>>>> main:virtual_art_museum/streamlit_play.py
        
medium_list = data['medium'].unique()
medium = st.sidebar.multiselect("Mediums: ", medium_list, default=st.session_state.get('medium', 'Oil'))

years = st.sidebar.slider('Time Period: ', min_value=min(data['year']), max_value=max(data['year']), value=(min(data['year']), max(data['year']))) # st.session_state.get('years', (min(data['year']), max(data['year'])))) #replace w min and max year

region = st.sidebar.radio('Region: ', ['United States', 'Europe'], index=None if st.session_state.get('region', None) is None else ['United States', 'Europe'].index(st.session_state.get('region', 'United States')))
if region == 'United States':
    st.write('Filtered to US') #replace w filter
if region == 'Europe':
    st.write('Filtered to Europe') #replace w filter

st.session_state.search = search
st.session_state.medium = medium
st.session_state.years = years
st.session_state.region = region

# Header configuation
col1, col2, col3 = st.columns([20,1,1])

with col1:
    st.image("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA_logo.png?raw=true", width=400)

with col2:
    st.page_link("https://www.moma.org", label='##', icon='✨', help='Favorites')

with col3:
    if(st.button("📊")):
        with st.spinner():
            time.sleep(20)
            st.write('Done')
    
st.markdown("#")
st.markdown("#")   

def image_gallery(data):
    i = 0
    for row in range(math.ceil(len(data)/3)):
        pictures = st.columns([3,3,3], vertical_alignment='center')
        for pic in pictures:
            with pic:
                st.image(data.iloc[i, 5], caption=data.iloc[i, 0])
                i += 1
image_gallery(data)