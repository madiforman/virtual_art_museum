import streamlit as st
import pandas as pd
import random
import math
import os
import time

# Page and Sidebar configuration
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
    'artist': ['Simon Vouet', 
               'Claude Monet', 
               'Boccaccio Boccaccino', 
               'Camille Corot',
               'Andrea Schiavone',
               'Anders Zorn', 
               'Edgar Degas',
               'Mikhail Vasilievich Nesterov',  
               'Henri Fantin-Latour'],
    'year': [1880, 1506, 1843, 1635, 1540, 1897, 1874, 1923, 1883],
    'medium': ['Oil', 'Oil', 'Oil', 'Oil', 'Oil', 'Oil', 'Ink', 'Oil', 'Oil'],
    'region': ['Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe'],
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
if 'region' not in st.session_state:
    st.session_state.region = None
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

st.sidebar.header('Advanced filters')

reset_button = st.sidebar.button('Reset Filters')
if reset_button:
    st.session_state.filters_reset = True
    st.session_state.search = ''
    st.session_state.medium = []
    st.session_state.years = (min(data['year']), max(data['year']))
    st.session_state.region = None
    st.rerun()

search = st.sidebar.text_input("🔍︎ Search by keyword: ", value=st.session_state.search)

medium_list = data['medium'].unique().tolist()
medium = st.sidebar.multiselect("Mediums: ", medium_list, default=st.session_state.medium)

years = st.sidebar.slider('Time Period: ', 
                          min_value=min(data['year']),
                          max_value=max(data['year']),
                          value=st.session_state.years)

region = st.sidebar.radio('Region: ', ['United States', 'Europe'], index=None if st.session_state.get('region', None) is None else ['United States', 'Europe'].index(st.session_state.region))

st.session_state.search = search
st.session_state.medium = medium
st.session_state.years = years
st.session_state.region = region

# Header configuration
col1, col2, col3 = st.columns([20,1,1])

with col1:
    st.image("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA_logo.png?raw=true", width=400)

with col2:
    st.page_link("pages/favorites.py", label='##', icon='✨', help='Favorites')

with col3:
    if(st.button("📊")):
        with st.spinner():
            time.sleep(20)
            st.write('Done')
    
st.markdown("#")
st.markdown("#")   

# Filtered data
filtered = data.copy()

if search:
    mask = False
    for column in filtered.columns:
        mask = mask | filtered[column].astype(str).str.contains(search, case=False, na=False)
    filtered = filtered[mask]

if medium:
    filtered = filtered[filtered['medium'].isin(medium)]

filtered = filtered[(filtered['year'] >= years[0]) & (filtered['year'] <= years[1])]

if region == 'United States':
    filtered = filtered[filtered['region'] == 'United States']
elif region == 'Europe':
    filtered = filtered[filtered['region'] == 'Europe']

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
                # Add a button to add/remove from favorites
                if st.button(f"❤️ {caption}", key=f"fav_{i}"):
                    if caption not in st.session_state.favorites:
                        st.session_state.favorites.append(caption)
                    else:
                        st.session_state.favorites.remove(caption)
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium')
        for j in range(leftovers):
            with lastrow[j]:
                caption = data.iloc[i,0]
                st.image(data.iloc[i,5], caption=caption)
                # Add a button to add/remove from favorites
                if st.button(f"❤️ {caption}", key=f"fav_{i}"):
                    if caption not in st.session_state.favorites:
                        st.session_state.favorites.append(caption)
                    else:
                        st.session_state.favorites.remove(caption)
                i += 1
                
image_gallery(filtered)

# Create a new file named favorites.py in the pages directory
# Add the following code to favorites.py to display the favorites

# pages/favorites.py


import streamlit as st

st.set_page_config(
    page_title="Favorites",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Your Favorites")

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if st.session_state.favorites:
    for favorite in st.session_state.favorites:
        st.write(favorite)
        if st.button(f"Remove {favorite}", key=f"remove_{favorite}"):
            st.session_state.favorites.remove(favorite)
            st.rerun()
else:
    st.write("You have no favorites yet.")
