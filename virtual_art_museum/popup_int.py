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

    def split_delimited(cell):
        ''' Splits delimited cells into lists '''
        if isinstance(cell, str) and '|' in cell:
            items = [item.strip() for item in cell.split('|')]
            return ", ".join(items)
        return cell

    for col in data.columns:
        data[col] = data[col].apply(split_delimited)

    def clean_culture(culture):
        ''' Gets rid of possibly / probably and splits at the comma '''
        if not isinstance(culture, str):
            return culture
            
        cleaned = re.sub(r'\b(?:probably|possibly)\b\s*', '', culture, flags=re.IGNORECASE)
        cleaned = cleaned.split(',')[0].strip()
        return cleaned

    data['Culture'] = data['Culture'].apply(clean_culture)

    def replace_empty(df):
        ''' Replaces unknown values with a string for the pop-up '''
        for col in df.columns:
            is_empty = (
                df[col].isna() |
                (df[col] == None) |
                (df[col].astype(str).str.strip() == ''))

            df.loc[is_empty, col] = f"{col} unknown"

        return df

    data = replace_empty(data)

    def clean_title(title):
        ''' Makes a cleaner title to print '''
        if not isinstance(title, str):
            return title

        cleaned = re.sub(r'\([^)]*\)', '', title)
        cleaned = re.sub(r'^\W+|\W+$', '', cleaned)
        return cleaned.strip()

    data['caption_title'] = data['Title'].apply(clean_title)

    def century_mapping(year):
        ''' Creates a century value for applicable years '''
        if isinstance(year, int):
            century = ceil(abs(year) / 100)
            if year < 0:
                return f"{century}th century BC"
            else:
                if century == 1:
                    return f"{century}st century AD"
                elif century == 2:
                    return f"{century}nd century AD"
                elif century == 3:
                    return f"{century}rd century AD"
                else:
                    return f"{century}th century AD"
        return year

    data['Century'] = data['Year'].apply(century_mapping)
            
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
                caption = data.iloc[i, -2]
                st.image(data.iloc[i,-3], caption=caption) #jen's note - not sure if the added code will work with this line
                ### adding popup code ###
                artist = data.iloc[i, 1]
                year = data.iloc[i, 2]
                image_url = data.iloc[i, 5]
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="{image_url}" style="width: 100%; max-width: 800px;"/>
                        <p>{caption}, {artist}, {year}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                if st.button(f"View details", key=f"button_{i}"):
                    st.session_state["selected_image"] = image_url
                    st.session_state["selected_title"] = caption
                    st.session_state["selected_author"] = artist
                    st.session_state["selected_year"] = year
                    st.session_state["show_modal"] = True  # Open the pop-up
                    st.rerun()  # Refresh UI to prevent double rendering
                #popup ended#
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium', vertical_alignment='center')
        for j in range(leftovers):
            with lastrow[j]:
                caption = data.iloc[i,-2]
                st.image(data.iloc[i,-3], caption=caption)
                 ### adding popup code ###
                artist = data.iloc[i, 1]
                year = data.iloc[i, 2]
                image_url = data.iloc[i, 5]
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="{image_url}" style="width: 100%; max-width: 800px;"/>
                        <p>{caption}, {artist}, {year}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                if st.button(f"View details", key=f"button_{i}"):
                    st.session_state["selected_image"] = image_url
                    st.session_state["selected_title"] = caption
                    st.session_state["selected_author"] = artist
                    st.session_state["selected_year"] = year
                    st.session_state["show_modal"] = True  # Open the pop-up
                    st.rerun()  # Refresh UI to prevent double rendering
                #popup ended#
                i += 1
##popup code added##

# Pop-up section (Only displayed when an image is selected)
if st.session_state.get("show_modal", False):
    image_url = st.session_state["selected_image"]
    title = st.session_state["selected_title"]
    author = st.session_state["selected_author"]
    year = st.session_state["selected_year"]
    medium = data[data['image'] == image_url]['medium'].values[0]
    region = data[data['image'] == image_url]['region'].values[0]
    
    # Use HTML to display the image without the enlarge/reduce button
    st.markdown(
        f"""
        <div style="text-align: center; position: relative;">
            <button style="position: absolute; top: 10px; right: 10px; background-color: skyblue; color: white; border: none; padding: 10px; cursor: pointer; border-radius: 5px;">X</button>
            <img src="{image_url}" style="width: 100%; max-width: 800px;"/>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write(f"### **{title}**")
    st.write(f"#### **By {author}, {year}**")
    st.write(f"Medium: {medium}")
    st.write(f"Region: {region}")

    # "Close" button (Fully resets state and refreshes UI)
    if st.button("Close"):
        st.session_state["show_modal"] = False  
        st.session_state["selected_image"] = None
        st.session_state["selected_title"] = ""
        st.session_state["selected_author"] = ""
        st.session_state["selected_year"] = ""
        st.rerun()  # Forces UI refresh to show images again
#popup code ended#
data = image_processing_met(data)
page_setup()
sidebar_setup()
# st.write(data) uncomment if you want to see how data is being stored :)
image_gallery(data)