import streamlit as st
import time
# next steps: replace title with logo (explore st.logo() capabilities), fix aspect ratio, move filters to sidebar
# if time: play with staggering for the photos, randomize function for the sizes, make filters do something
# rewrite the README.md and work on Tech Review

# Page and Sidebar configuation
st.set_page_config(
    page_title="MoVA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# q for Madi: should filters be affected by themselves?
st.logo("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA%20bw%20logo.png?raw=true", size="large")
st.sidebar.header('Advanced filters')
search = st.sidebar.text_input("🔍︎ Search by keyword: ")
st.write(search)
# TODO: search pic df for keyword partial match

xbox = st.sidebar.button('Reset Filters', key='reset')
if xbox:
    st.session_state.reset = True
    st.experimental_rerun()
else:
        st.session_state.reset = False
        
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

pictures = ["https://th.bing.com/th/id/R.652ffd1ad31d0a07b39f2fa0a2ff0cdb?rik=G2jTQRchxN%2bPEw&riu=http%3a%2f%2fhotsigns.net%2fassets%2fimages%2femogee+230.png&ehk=tFPLTpwA1vI00Uu1Jx2jc3bEYikAnSD5TdWbKiHT5Sg%3d&risl=&pid=ImgRaw&r=0", "https://www.pngitem.com/pimgs/m/128-1285712_smiley-tongue-face-emoji-png-squinting-face-with.png", "https://th.bing.com/th/id/OIP.A3JHJSrrZOKuuDVFH9M_VgHaGs?rs=1&pid=ImgDetMain", "https://th.bing.com/th/id/OIP.J4CzP2aeSk750Kq5aNmf8gHaH7?rs=1&pid=ImgDetMain", "https://thumbs.dreamstime.com/b/tongue-out-emoticon-17346266.jpg", "https://th.bing.com/th/id/R.4810be7b90e7e7fefba0524864635491?rik=38gM7WchPblIyA&riu=http%3a%2f%2fclipart-library.com%2fimages%2fLTdjGjXyc.jpg&ehk=XKyEcy%2bhvoTlMiHEoj%2fzXmZfpbWP2ty3iST90PSfSHo%3d&risl=&pid=ImgRaw&r=0", "https://hotemoji.com/images/emoji/b/tgkksj1h79afb.png", "https://em-content.zobj.net/thumbs/120/apple/325/face-savoring-food_1f60b.png", "https://th.bing.com/th/id/OIP.1u6PlP-Par84QQJxhJ6VoQHaHk?pid=ImgDet&w=474&h=484&rs=1"]     

pic1, pic2, pic3 = st.columns([3,3,3], vertical_alignment='center')
with pic1:
    st.image(pictures[0], caption="Title, author, year.", use_container_width=True)

with pic2:
    st.image(pictures[1], caption="Title, author, year.", use_container_width=True)
    
with pic3:
    st.image(pictures[2], caption="Title, author, year.", use_container_width=True)

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