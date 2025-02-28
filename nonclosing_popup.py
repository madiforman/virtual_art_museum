import streamlit as st
import pandas as pd
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
    st.page_link("https://www.moma.org", label='##', icon='✨', help='Favorites')

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


# ...existing code...

def image_gallery(data):
    n = len(data)
    rows = n // 3
    i = 0

    title = "title"
    name = "artist name"
    year = "year"
    medium = "medium"
    repository = "location"

    for row in range(rows):
        pics = st.columns([3, 3, 3], vertical_alignment='center')
        for pic in pics:
            with pic:
                # Splitting in case we want to add more to the caption
                caption = data.iloc[i, 0]
                st.image(data.iloc[i, 5], caption=caption)
                if st.button("Click for details", key=f"button_{i}"):
                    # HTML and CSS for click effect
                    html_code = f"""
                    <style>
                        .popup-overlay {{
                            position: fixed;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            background: rgba(0, 0, 0, 0.8);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            z-index: 999;
                        }}

                        .popup-container {{
                            background: white;
                            padding: 20px;
                            border-radius: 10px;
                            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
                            z-index: 1000;
                            width: 80%;
                            height: 80%;
                            display: flex;
                            flex-direction: row;
                            overflow: auto;
                            border: white; /* Border color on all four sides */
                            font-family: Verdana, sans-serif; /* Font */
                            box-sizing: border-box; /* Ensure padding and border are included in the element's total width and height */
                        }}

                        .popup-image {{
                            width: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            background: white;
                        }}

                        .popup-image img {{
                            max-width: 100%;
                            max-height: 100%;
                            object-fit: contain;
                        }}

                        .popup-text {{
                            width: 50%;
                            padding-left: 20px;
                            overflow: auto;
                            display: flex;
                            flex-direction: column;
                            justify-content: top;
                        }}

                        .artist-header {{
                            color: black;
                            font-size: 16px;
                            font-family: Verdana, sans-serif;
                            margin-bottom: 0;
                        }}
                        
                        .title-header {{
                            color: black;
                            font-size: 20px;
                            font-family: Verdana, sans-serif;
                            margin-bottom: 0;
                        }}
                        .artdetail-header {{
                            color: black;
                            font-size: 20px;
                            font-family: Verdana, sans-serif;
                            margin-bottom: 0;
                        }}

                        .close-btn {{
                            position: absolute;
                            top: 15px;
                            right: 25px;
                            background: gainsboro;
                            color: white;
                            border: none;
                            padding: 8px 14px;
                            font-size: 10px;
                            cursor: pointer;
                            border-radius: 5px;
                            height: 30px; /* Set the height of the close button */
                        }}
                        
                        .favorite-btn {{
                            position: absolute;
                            top: 15px;
                            right: 63px;
                            background: none;
                            border: 2px solid gainsboro;
                            border-radius: 50%;
                            cursor: pointer;
                            width: 30px; /* Set the width to match the height of the close button */
                            height: 30px; /* Set the height to match the height of the close button */
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        }}

                        .favorite-btn svg {{
                            fill: none;
                            stroke: gold;
                            stroke-width: 2;
                            width: 24px;
                            height: 24px;
                        }}

                        .clickable-image {{
                            cursor: pointer;
                        }}
                    </style>

                    <div class="popup-overlay" id="popupOverlay_{i}" onclick="closePopup({i})">
                        <div class="popup-container" onclick="event.stopPropagation()">
                            <button class="close-btn" onclick="closePopup({i})">X</button>
                            <button class="favorite-btn" onclick="toggleFavorite(this)">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                                    <path d="M12 .587l3.668 7.568L24 9.423l-6 5.847 1.417 8.253L12 18.897l-7.417 4.626L6 15.27 0 9.423l8.332-1.268z"/>
                                </svg>
                            </button>
                            <div class="popup-image">
                                <img src="{data.iloc[i, 5]}" alt="Enlarged Image">
                            </div>
                            <div class="popup-text">
                                <p class="title-header">{data.iloc[i, 0]}</p>
                                <p class="artist-header">{data.iloc[i, 1]}, {data.iloc[i, 2]}</p>
                                <p class="artdetail-header">Art Details</p>
                                <p class="artist-header">Medium: {data.iloc[i, 3]}</p>
                                <p class="artist-header">Location: {data.iloc[i, 4]}</p>
                            </div>
                        </div>
                    </div>

                    <script>
                        function closePopup(index) {{
                            document.getElementById('popupOverlay_' + index).style.display = 'none';
                        }}
                        function toggleFavorite(button) {{
                            const svg = button.querySelector('svg');
                            if (svg.style.fill === 'gold') {{
                                svg.style.fill = 'white';
                            }} else {{
                                svg.style.fill = 'gold';
                            }}
                        }}
                    </script>
                    """
                    # Render the HTML code
                    st.markdown(html_code, unsafe_allow_html=True)
                
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium')
        for j in range(leftovers):
            with lastrow[j]:
                caption = data.iloc[i, 0]
                st.image(data.iloc[i, 5], caption=caption)
                i += 1

image_gallery(filtered)