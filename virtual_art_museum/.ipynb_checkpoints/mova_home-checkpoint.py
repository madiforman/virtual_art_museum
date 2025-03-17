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

MET_PATH = os.path.join(base_dir, "data", "MetObjects_final_filtered.csv")
EUROPEANA_PATH = os.path.join(base_dir, "data", "Europeana_data.csv")

met = pd.read_csv(MET_PATH)
data = pd.read_csv(EUROPEANA_PATH)

def image_processing_europeana(data):
    """
    Transforms the Europeana data to be 
    compatible with MET merge.
    - Reads through the description column
        and tries to match for any Mediums
        or Tags (based on MET)
    - Updates country column to match any
        culture within the MET data
    - Makes a fake column for Artist Bio
    - Replaces 'Unknown' in year column
        with unrealistic value
    - Renames columns to match MET's
    """
    data['Medium'] = "Medium unknown"
    data['Tags'] = "Tags unknown"
    data['repository'] = "Europeana"

    tags = met['Tags'].str.split(',').explode().unique()
    cultures = met['Culture'].str.split(',').explode().unique()
    
    def find_tags(description):
        ''' Searches through the description
        column, finding any Tag matches '''
        tags_match = []
        
        if description == 'Unknown' or str(description).startswith('warning:'):
            return "Description unknown"

        description = str(description).lower()
        
        for tag in tags:
            if tag.lower() in description:
                tags_match.append(tag)

        return description

    data['description'] = data['description'].apply(find_tags)

    for idx, row in data.iterrows():
        description = str(row['description']).lower()

        tags_match = [tag for tag in tags if tag and tag.lower() in description]
        if tags_match:
            data.at[idx, 'Tags'] = ", ".join(tags_match)

    country_to_culture = {
        'United Kingdom': 'British',
        'England': 'British',
        'Scotland': 'British',
        'Wales': 'British',
        'Ireland': 'Irish',
        'France': 'French',
        'Germany': 'German',
        'Italy': 'Italian',
        'Spain': 'Spanish',
        'Portugal': 'Portuguese',
        'Netherlands': 'Dutch',
        'Belgium': 'Belgian',
        'Switzerland': 'Swiss',
        'Austria': 'Austrian',
        'Greece': 'Greek',
        'Denmark': 'Danish',
        'Sweden': 'Swedish',
        'Norway': 'Norwegian',
        'Finland': 'Finnish',
        'Russia': 'Russian',
        'Poland': 'Polish',
        'Hungary': 'Hungarian',
        'Czech Republic': 'Czech',
        'Romania': 'Romanian',
        'Bulgaria': 'Bulgarian',
        'Turkey': 'Turkish'}

    for culture in cultures:
        country_match = None
        culture = str(culture).strip()

        # Remove suffixes to check for match
        if culture.endswith('ish'):
            country_match = culture[:-3]
        elif culture.endswith('ese'):
            country_match = culture[:-3]
        elif culture.endswith('ian'):
            country_match = culture[:-3]
        elif culture.endswith('ch'):
            country_match = culture[:-2] + 'ce'
        elif culture.endswith('ish'):
            country_match = culture[:-3]

        if country_match and country_match not in country_to_culture.values():
            country_to_culture[country_match] = culture

    def map_countries_to_culture(country):
        ''' Maps countries to respective cultures '''
        if pd.isna(country) or country == 'Unknown':
            return 'Culture unknown'

        country = str(country).strip()

        if country in country_to_culture:
            return country_to_culture[country]

        for known_country, culture in country_to_culture.items():
            if known_country in country:
                return culture

        for culture in cultures:
            culture_lower = culture.lower()
            country_lower = country.lower()
            if culture_lower in country_lower:
                return culture
        
        return 'Culture unknown'

    data['Culture'] = data['country'].apply(map_countries_to_culture)

    def clean_title(title):
        ''' Makes a cleaner title to print '''
        if not isinstance(title, str):
            return title

        comma = title.find(',')
        period = title.find('.')

        if comma == -1 and period == -1:
            return title
        elif comma == -1:
            return title[:period].strip()
        elif period == -1:
            return title[:comma].strip()
        else:
            endpoint = min(idx for idx in [comma, period] if idx >= 0)
            return title[:endpoint].strip()

    data['title'] = data['title'].apply(clean_title)

    def clean_creator(artist):
        if pd.isna(artist) or artist == 'Unknown' or str(artist).startswith('http://'):
            return "Artist unknown"
        return artist  

    data['creator'] = data['creator'].apply(clean_creator)

    data['Artist biographic information'] = "Artist biographic information unknown"
    data['Dimensions'] = "Dimensions unknown"
    data['year'] = data['year'].replace('Unknown', 9999).astype(int)

    data = data.rename(columns = {'europeana_id' : 'Object Number',
                                  'title' : 'Title',
                                  'creator' : 'Artist',
                                  'description' : 'Description',
                                  'provider' : 'Department',
                                  'year' : 'Year',
                                  'repository' : 'Repository'})
    data = data.drop(columns=['country'])
        
    return data

def blend_datasources(met_data, europeana_data):
    """
    Takes the pre-processed MET and Europeana datasets,
    ensures they follow the same format, randomly 
    combines them, and orders them according to height.
    For odd number rows, tallest photo should be in the center;
    for even number rows, shortest photo is centered.
    """
    combined = pd.concat([met_data, europeana_data], ignore_index=True)
    combined = combined.sample(frac=1).reset_index(drop=True)
    return combined

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

def sidebar_setup():
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
    print(data)
    for row in range(rows):
        pics = st.columns([3,3,3], gap='medium', vertical_alignment='center')
        for pic in pics:
            with pic:
                #splitting in case we want to add more to the caption
                caption = data.iloc[i, 1]
                st.image(data.iloc[i,-4])
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium', vertical_alignment='center')
        for j in range(leftovers):
            with lastrow[j]:
                caption = data.iloc[i,1]
                st.image(data.iloc[i,-4], caption=caption)
                i += 1

data = image_processing_europeana(data)
combined = blend_datasources(met, data)
page_setup()
#sidebar_setup()
image_gallery(combined)