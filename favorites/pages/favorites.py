import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO

# Favorites Page
st.set_page_config(
    page_title="MoVA - Favorites",
    layout="wide"
)

st.title("Favorites")

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if st.session_state.favorites:
    # Download all favorites as a single PNG
    if st.button("️Download"):
        images = []
        for favorite in st.session_state.favorites:
            response = requests.get(favorite['image'])
            img = Image.open(BytesIO(response.content))
            images.append(img)
        
        # Resize images to the same width (e.g., 300px) while maintaining aspect ratio
        resized_images = []
        target_width = 300
        for img in images:
            aspect_ratio = img.height / img.width
            new_height = int(target_width * aspect_ratio)
            resized_img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
            resized_images.append(resized_img)
        
        # Calculate the size of the final canvas
        max_images_per_row = 3
        spacing = 20  # Space between images
        background_color = (240, 240, 240)  # Light gray background

        # Calculate canvas width and height
        canvas_width = (target_width + spacing) * max_images_per_row + spacing
        canvas_height = 0
        row_height = 0
        for i, img in enumerate(resized_images):
            if i % max_images_per_row == 0:
                canvas_height += row_height + spacing
                row_height = 0
            row_height = max(row_height, img.height)
        canvas_height += row_height + spacing

        # Create the canvas
        canvas = Image.new('RGB', (canvas_width, canvas_height), background_color)

        # Paste images onto the canvas
        x_offset = spacing
        y_offset = spacing
        row_height = 0
        for i, img in enumerate(resized_images):
            if i % max_images_per_row == 0 and i != 0:
                y_offset += row_height + spacing
                x_offset = spacing
                row_height = 0
            canvas.paste(img, (x_offset, y_offset))
            x_offset += img.width + spacing
            row_height = max(row_height, img.height)
        
        # Save to BytesIO and provide download link
        img_byte_arr = BytesIO()
        canvas.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        st.download_button(
            label="📥",
            data=img_byte_arr,
            file_name="favorites.png",
            mime="image/png"
        )

    # Display favorites in a 3-column layout
    n = len(st.session_state.favorites)
    rows = n // 3
    i = 0

    for row in range(rows):
        pics = st.columns([3,3,3], vertical_alignment='center')
        for pic in pics:
            with pic:
                favorite = st.session_state.favorites[i]
                st.image(favorite['image'], caption=favorite['title'])
                
                # Remove from Favorites button
                if st.button(f"❌", key=f"remove_{i}"):
                    st.session_state.favorites.pop(i)
                    st.success(f"Removed '{favorite['title']}' from favorites!")
                    st.rerun()
                i += 1

    leftovers = n % 3
    if leftovers > 0:
        lastrow = st.columns(leftovers, gap='medium')
        for j in range(leftovers):
            with lastrow[j]:
                favorite = st.session_state.favorites[i]
                st.image(favorite['image'], caption=favorite['title'])
                
                # Remove from Favorites button
                if st.button(f"❌", key=f"remove_{i}"):
                    st.session_state.favorites.pop(i)
                    st.success(f"Removed '{favorite['title']}' from favorites!")
                    st.rerun()
                i += 1
else:
    st.write("No favorites yet. Add some using the ❤️ button!")
