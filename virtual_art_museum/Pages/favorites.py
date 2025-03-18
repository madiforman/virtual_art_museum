import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import json
import os

# Favorites Page
st.set_page_config(
    page_title="MoVA - Favorites",
    layout="wide"
)

st.markdown("""
    <style>
        .title-font {
            font-family: 'Arial', sans-serif;
            font-size: 36px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<p class='title-font'>❤️ Favorites</p>", unsafe_allow_html=True)

# Load favorites from cache
FAVORITES_CACHE_FILE = "favorites_cache.json"
if os.path.exists(FAVORITES_CACHE_FILE):
    with open(FAVORITES_CACHE_FILE, "r") as f:
        st.session_state.favorites = json.load(f)
else:
    st.session_state.favorites = []

if st.session_state.favorites:
    images = []
    captions = []
    for favorite in st.session_state.favorites:
        response = requests.get(favorite['image_url'])
        img = Image.open(BytesIO(response.content))
        images.append(img)
        captions.append(favorite['Title'])
    
    # Resize images to the same width (e.g., 300px) while maintaining aspect ratio
    resized_images = []
    target_width = 300
    for img in images:
        aspect_ratio = img.height / img.width
        new_height = int(target_width * aspect_ratio)
        resized_img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
        resized_images.append(resized_img)
    
    # Create a collage of the images
    max_images_per_row = 3
    spacing = 20  # Space between images
    caption_height = 40  # Increased space for captions
    background_color = (240, 240, 240)  # Light gray background
    
    # Calculate canvas width and height
    canvas_width = (target_width + spacing) * max_images_per_row + spacing
    canvas_height = 0
    row_height = 0
    for i, img in enumerate(resized_images):
        if i % max_images_per_row == 0:
            canvas_height += row_height + spacing + caption_height
            row_height = 0
        row_height = max(row_height, img.height)
    canvas_height += row_height + spacing + caption_height

    # Create the canvas
    canvas = Image.new('RGB', (canvas_width, canvas_height), background_color)
    draw = ImageDraw.Draw(canvas)

    # Load a larger font for captions
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Larger font size
    except:
        font = ImageFont.load_default()  # Fallback to default font

    # Paste images onto the canvas and add captions
    x_offset = spacing
    y_offset = spacing
    row_height = 0
    for i, img in enumerate(resized_images):
        if i % max_images_per_row == 0 and i != 0:
            y_offset += row_height + spacing + caption_height
            x_offset = spacing
            row_height = 0
        canvas.paste(img, (x_offset, y_offset))
        
        # Add caption below the image
        caption = captions[i]
        text_bbox = draw.textbbox((0, 0), caption, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x_offset + (target_width - text_width) // 2
        text_y = y_offset + img.height + 10  # Increase spacing
        draw.text((text_x, text_y), caption, fill="black", font=font)
        
        x_offset += img.width + spacing
        row_height = max(row_height, img.height)
    
    # Save to BytesIO and provide a single download button
    img_byte_arr = BytesIO()
    canvas.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    st.download_button(
        label="Download",
        data=img_byte_arr,
        file_name="favorites.png",
        mime="image/png"
    )

    # Display favorites in a 3-column layout
    n = len(st.session_state.favorites)
    rows = n // 3
    i = 0

    for row in range(rows):
        pics = st.columns([3, 3, 3], vertical_alignment='center')
        for pic in pics:
            with pic:
                favorite = st.session_state.favorites[i]
                st.image(favorite['image_url'], caption=favorite['Title'])
                if st.button(f"❌", key=f"remove_{i}"):
                    st.session_state.favorites.pop(i)
                    with open(FAVORITES_CACHE_FILE, "w") as f:
                        json.dump(st.session_state.favorites, f)
                    st.rerun()
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium')
        for j in range(leftovers):
            with lastrow[j]:
                favorite = st.session_state.favorites[i]
                st.image(favorite['image_url'], caption=favorite['Title'])
                if st.button(f"❌", key=f"remove_{i}"):
                    st.session_state.favorites.pop(i)
                    with open(FAVORITES_CACHE_FILE, "w") as f:
                        json.dump(st.session_state.favorites, f)
                    st.rerun()
                i += 1
else:
    st.write("No favorites yet. Add some using the ❤️ button!")
