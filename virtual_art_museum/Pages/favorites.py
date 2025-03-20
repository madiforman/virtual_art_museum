"""
MoVA Favorites - allows users to view, download, and remove favorite images chosen from the homepage.
"""

import json
import os
from io import BytesIO

import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

FAVORITES_CACHE_FILE = "favorites_cache.json"
TARGET_WIDTH = 300
MAX_IMAGES_PER_ROW = 3
SPACING = 20
CAPTION_HEIGHT = 40
BACKGROUND_COLOR = (240, 240, 240)

st.set_page_config(page_title="MoVA - Favorites", layout="wide")

st.markdown(
    """
    <style>
        .title-font {
            font-family: 'Arial', sans-serif;
            font-size: 36px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<p class='title-font'>❤️ Favorites</p>", unsafe_allow_html=True)

def load_favorites() -> list:
    """Load favorites from the cache file."""
    if os.path.exists(FAVORITES_CACHE_FILE):
        with open(FAVORITES_CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []
    
def save_favorites(favorites: list) -> None:
    """Save favorites to the cache file."""
    with open(FAVORITES_CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(favorites, file)

def create_collage(images: list, captions: list) -> BytesIO:
    """Create a collage of images with captions."""
    resized_images = []
    for img in images:
        aspect_ratio = img.height / img.width
        new_height = int(TARGET_WIDTH * aspect_ratio)
        resized_img = img.resize((TARGET_WIDTH, new_height), Image.Resampling.LANCZOS)
        resized_images.append(resized_img)

    canvas_width = (TARGET_WIDTH + SPACING) * MAX_IMAGES_PER_ROW + SPACING
    canvas_height = 0
    row_height = 0
    for i, img in enumerate(resized_images):
        if i % MAX_IMAGES_PER_ROW == 0:
            canvas_height += row_height + SPACING + CAPTION_HEIGHT
            row_height = 0
        row_height = max(row_height, img.height)
    canvas_height += row_height + SPACING + CAPTION_HEIGHT

    canvas = Image.new("RGB", (canvas_width, canvas_height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()

    x_offset = SPACING
    y_offset = SPACING
    row_height = 0
    for i, img in enumerate(resized_images):
        if i % MAX_IMAGES_PER_ROW == 0 and i != 0:
            y_offset += row_height + SPACING + CAPTION_HEIGHT
            x_offset = SPACING
            row_height = 0
        canvas.paste(img, (x_offset, y_offset))

        caption = captions[i]
        text_bbox = draw.textbbox((0, 0), caption, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x_offset + (TARGET_WIDTH - text_width) // 2
        text_y = y_offset + img.height + 10
        draw.text((text_x, text_y), caption, fill="black", font=font)

        x_offset += img.width + SPACING
        row_height = max(row_height, img.height)

    img_byte_arr = BytesIO()
    canvas.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr

def display_favorites(favorites: list) -> None:
    """Display favorites in a 3-column layout."""
    n = len(favorites)
    rows = n // MAX_IMAGES_PER_ROW
    i = 0

    for row in range(rows):
        pics = st.columns([3, 3, 3], vertical_alignment="center")
        for pic in pics:
            with pic:
                favorite = favorites[i]
                st.image(favorite["image_url"], caption=favorite["Title"])
                if st.button(f"❌", key=f"remove_{i}"):
                    favorites.pop(i)
                    save_favorites(favorites)
                    st.rerun()
                i += 1

    leftovers = n % MAX_IMAGES_PER_ROW
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap="medium")
        for j in range(leftovers):
            with lastrow[j]:
                favorite = favorites[i]
                st.image(favorite["image_url"], caption=favorite["Title"])
                if st.button(f"❌", key=f"remove_{i}"):
                    favorites.pop(i)
                    save_favorites(favorites)
                    st.rerun()
                i += 1

def main() -> None:
    """Main function to render the favorites page."""
    if "favorites" not in st.session_state:
        st.session_state.favorites = load_favorites()

    if st.session_state.favorites:
        if st.button("❌ Remove All Favorites", key="remove_all", help="Remove all favorited artworks"):
            st.session_state.favorites = []
            save_favorites(st.session_state.favorites)
            st.rerun()

        images = []
        captions = []
        for favorite in st.session_state.favorites:
            try:
                response = requests.get(favorite["image_url"], timeout=10)
                img = Image.open(BytesIO(response.content))
                images.append(img)
                captions.append(favorite["Title"])
            except requests.RequestException as e:
                st.error(f"Failed to load image: {e}")

        img_byte_arr = create_collage(images, captions)
        st.download_button(
            label="Download",
            data=img_byte_arr,
            file_name="favorites.png",
            mime="image/png",
        )

        display_favorites(st.session_state.favorites)
    else:
        st.write("No favorites yet. Add some using the ❤️ button!")

if __name__ == "__main__":
    main()