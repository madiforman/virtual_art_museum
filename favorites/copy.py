import streamlit as st
import time
import os

# Page Configuration
st.set_page_config(
    page_title="MoVA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.logo("https://github.com/madiforman/virtual_art_museum/blob/main/images/MoVA%20bw%20logo.png?raw=true", size="large")

# Sidebar Filters
st.sidebar.header('Advanced filters')
search = st.sidebar.text_input("🔍︎ Search by keyword: ")
reset_button = st.sidebar.button('Reset Filters')
style_list = ['All', 'Impressionism', 'Modern', 'Renaissance', 'Photography', 'Contemporary']
styles = st.sidebar.multiselect("Styles: ", style_list)
years = st.sidebar.slider('Time Period: ', 1400, 2025, (1400, 2025))
century_list = ['All', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st']
centuries = st.sidebar.multiselect('Century: ', century_list)
region = st.sidebar.radio('Region: ', ['United States', 'Europe'])

# Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Main Page", "Favorites"])

# Paths
FAVORITES_FILE = "favorites.txt"

# Functions for Favorites
def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        f.writelines(fav + "\n" for fav in favorites)

def add_to_favorites(image_url):
    favorites = load_favorites()
    if image_url not in favorites:
        favorites.append(image_url)
        save_favorites(favorites)
        st.experimental_rerun()

def remove_from_favorites(image_url):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav != image_url]
    save_favorites(favorites)
    st.experimental_rerun()

# Image Gallery
pictures = [
    {"url": "https://th.bing.com/th/id/R.652ffd1ad31d0a07b39f2fa0a2ff0cdb?rik=G2jTQRchxN%2bPEw&riu=http%3a%2f%2fhotsigns.net%2fassets%2fimages%2femogee+230.png&ehk=tFPLTpwA1vI00Uu1Jx2jc3bEYikAnSD5TdWbKiHT5Sg%3d&risl=&pid=ImgRaw&r=0", "title": "Funny Emoji", "artist": "Unknown"},
    {"url": "https://www.pngitem.com/pimgs/m/128-1285712_smiley-tongue-face-emoji-png-squinting-face-with.png", "title": "Squinting Emoji", "artist": "Anonymous"},
    {"url": "https://th.bing.com/th/id/OIP.A3JHJSrrZOKuuDVFH9M_VgHaGs?rs=1&pid=ImgDetMain", "title": "Abstract Face", "artist": "Modern Art"}
]

# Display Gallery with Clickable Popups
def display_gallery(images, show_remove=False):
    st.write("Click an image for details.")

    cols = st.columns(3)  # 3-column layout
    for i, img in enumerate(images):
        with cols[i % 3]:  # Ensure images are evenly distributed
            if st.button(f"🖼️ {img['title']}", key=f"popup_{i}"):  # Clicking opens popup
                st.session_state.selected_image = img
                st.experimental_rerun()

            st.image(img["url"], caption=f"{img['title']} by {img['artist']}", use_container_width=True)

            if show_remove:
                if st.button(f"❌ Remove", key=f"remove_{i}"):
                    remove_from_favorites(img["url"])
            else:
                if st.button(f"⭐ Add to Favorites", key=f"fav_{i}"):
                    add_to_favorites(img["url"])

# Popup with Image Details
if "selected_image" in st.session_state:
    img = st.session_state.selected_image
    st.image(img["url"], caption=img["title"], use_container_width=True)
    st.write(f"**Title:** {img['title']}")
    st.write(f"**Artist:** {img['artist']}")
    if st.button("⭐ Add to Favorites"):
        add_to_favorites(img["url"])
    if st.button("❌ Remove from Favorites"):
        remove_from_favorites(img["url"])
    if st.button("Close"):
        del st.session_state.selected_image
        st.experimental_rerun()

# Handle Navigation
if page == "Main Page":
    st.title("🎨 Art Gallery")
    display_gallery(pictures)

elif page == "Favorites":
    st.title("🌟 Your Favorites Gallery")
    favorites = [{"url": fav, "title": "Favorite Art", "artist": "Unknown"} for fav in load_favorites()]
    if favorites:
        display_gallery(favorites, show_remove=True)
    else:
        st.write("No favorites added yet!")
