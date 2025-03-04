import streamlit as st
import time
import requests
# next steps: replace title with logo (explore st.logo() capabilities), fix aspect ratio, move filters to sidebar
# if time: play with staggering for the photos, randomize function for the sizes, make filters do something
# rewrite the README.md and work on Tech Review


# Page and Sidebar configuation
st.set_page_config(
    page_title="MoVA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

'''if 'reset' not in st.session_state:
    st.session_state.reset = False'''

# q for Madi: should filters be affected by themselves?
st.logo("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA%20bw%20logo.png?raw=true", size="large")
#st.image("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA%20bw%20logo.png?raw=true", size="large")
st.sidebar.header('Advanced filters')
search = st.sidebar.text_input("🔍︎ Search by keyword: ")
st.write(search)
# TODO: search pic df for keyword partial match

reset_button = st.sidebar.button('Reset Filters')
if reset_button:
    st.session_state.reset = True
    st.experimental_rerun()
else:
    st.session_state.reset = False

'''xbox = st.sidebar.button('Reset Filters', key='reset')
if xbox:
    st.session_state.reset = True
    st.experimental_rerun()
else:
        st.session_state.reset = False'''
        
style_list = ['All', 'Impressionism', 'Modern', 'Renaissance', 'Photography', 'Contemporary'] #replace w df values
styles = st.sidebar.multiselect("Styles: ", style_list)

years = st.sidebar.slider('Time Period: ', 1400, 2025, (1400, 2025)) #replace w min and max year

century_list = ['All', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st']
centuries = st.sidebar.multiselect('Century: ', century_list)

region = st.sidebar.radio('Region: ', ['United States', 'Europe'])
if region == 'United States':
    st.write('Filtered to US') #replace w filter
if region == 'Europe':
    st.write('Filtered to Europe') #replace w filter

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

def get_posts():
    
    url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/45734'
    try: 
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print("error", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
            print("error", e)
            return None

def popup_posts(pic_input):


    #temp = get_posts()

    '''if temp and temp.get("primaryImage"):
        image_url = temp["primaryImage"]
        title = temp.get("title", "No description available.")  
        name=temp.get("artistDisplayName","No artist name available")
        year=temp.get("objectDate","No year available")
        medium=temp.get("medium","No year available")
        repository=temp.get("repository","No year available")'''

    
    image_url = pic_input
    title = "title"
    name="artist"
    year="year"
    medium=""
    repository=""


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
            display: none;
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
            width : 0.8 * screen.availWidth
            #width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: row;
            overflow: auto;
            border: white; /* Border color on all four sides */
            font-family: Verdana, sans-serif; /* Font */
            box-sizing: border-box; /* Ensure padding and border are included in the element's total width and height */
        }}

        .popup-image {{
            width: 50%;
            height:100%
            display: flex;
            align-items: center;
            justify-content: center;
            background:white;
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

        .artist-header {{color:black;
            font-size: 16px;
            font-family: Verdana, sans-serif;
            margin-bottom: 0;}}
        
        .title-header {{color:black;
            font-size: 20px;
            font-family: Verdana, sans-serif;
            margin-bottom: 0;}}
        .artdetail-header {{color:black;
            font-size: 20px;
            font-family: Verdana, sans-serif;
            margin-bottom: 0;}}

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

        <div class="clickable-image">
            <button onclick="openPopup()">
                More details
            </button>
            </div>

        <div class="popup-overlay" id="popupOverlay">
            <div class="popup-container">
                <button class="close-btn" onclick="closePopup()">X</button>
                <button class="favorite-btn" onclick="toggleFavorite(this)">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M12 .587l3.668 7.568L24 9.423l-6 5.847 1.417 8.253L12 18.897l-7.417 4.626L6 15.27 0 9.423l8.332-1.268z"/>
                    </svg>
                </button>
                <div class="popup-image">
                    <img src="{image_url}" alt="Enlarged Image">
                </div>
                <div class="popup-text">
                    <p class="title-header">{title}</p>
                    <p class="artist-header">{name}, {year}</p>
                    <p class="artdetail-header">Art Details</p>
                    <p class="artist-header">Medium: {medium}</p>
                    <p class="artist-header">Location: {repository}</p>
                
                    
                </div>
            </div>
        </div>

        <script>
            function openPopup() {{
                document.getElementById('popupOverlay').style.display = 'flex';
            }}
            function closePopup() {{
                document.getElementById('popupOverlay').style.display = 'none';
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
    st.components.v1.html(html_code, height=600)
    

pictures = ["https://th.bing.com/th/id/R.652ffd1ad31d0a07b39f2fa0a2ff0cdb?rik=G2jTQRchxN%2bPEw&riu=http%3a%2f%2fhotsigns.net%2fassets%2fimages%2femogee+230.png&ehk=tFPLTpwA1vI00Uu1Jx2jc3bEYikAnSD5TdWbKiHT5Sg%3d&risl=&pid=ImgRaw&r=0", "https://www.pngitem.com/pimgs/m/128-1285712_smiley-tongue-face-emoji-png-squinting-face-with.png", "https://th.bing.com/th/id/OIP.A3JHJSrrZOKuuDVFH9M_VgHaGs?rs=1&pid=ImgDetMain", "https://th.bing.com/th/id/OIP.J4CzP2aeSk750Kq5aNmf8gHaH7?rs=1&pid=ImgDetMain", "https://thumbs.dreamstime.com/b/tongue-out-emoticon-17346266.jpg", "https://th.bing.com/th/id/R.4810be7b90e7e7fefba0524864635491?rik=38gM7WchPblIyA&riu=http%3a%2f%2fclipart-library.com%2fimages%2fLTdjGjXyc.jpg&ehk=XKyEcy%2bhvoTlMiHEoj%2fzXmZfpbWP2ty3iST90PSfSHo%3d&risl=&pid=ImgRaw&r=0", "https://hotemoji.com/images/emoji/b/tgkksj1h79afb.png", "https://em-content.zobj.net/thumbs/120/apple/325/face-savoring-food_1f60b.png", "https://th.bing.com/th/id/OIP.1u6PlP-Par84QQJxhJ6VoQHaHk?pid=ImgDet&w=474&h=484&rs=1"]     

pic1, pic2, pic3 = st.columns([3,3,3], vertical_alignment='center')
with pic1:
    st.image(pictures[0], caption="Title, author, year.")
    popup_posts(pictures[0])
with pic2:
    st.image(pictures[1], caption="Title, author, year.", use_container_width=True)
    popup_posts(pictures[1])
    
with pic3:
    st.image(pictures[2], caption="Title, author, year.", use_container_width=True)
    popup_posts(pictures[2])

pic4, pic5, pic6 = st.columns([3,3,3], vertical_alignment='center')
with pic4:
    st.image(pictures[3], caption='Title, author, year.', use_container_width=True)
    
with pic5:
    st.image(pictures[4], caption='Title, author, year.', use_container_width=True)

with pic6:
    st.image(pictures[5], caption='Title, author, year.', use_container_width=True)

pic7, pic8, pic9 = st.columns([3,3,3], vertical_alignment='center')
with pic7:
    st.image(pictures[6], caption='Title, author, year.', use_container_width=True)

with pic8:
    st.image(pictures[7], caption='Title, author, year.', use_container_width=True)

with pic9:
    st.image(pictures[8], caption='Title, author, year.', use_container_width=True)



