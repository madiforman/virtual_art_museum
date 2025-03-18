import streamlit as st
import os
from PIL import Image, ImageDraw
import base64
from io import BytesIO

# Function to get images from the 'favorites' directory
def load_favorites():
    favorites_folder = "favorites"
    if not os.path.exists(favorites_folder):
        os.makedirs(favorites_folder)
    return [os.path.join(favorites_folder, img) for img in os.listdir(favorites_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

# Function to create a gallery image with frames
def create_gallery_with_frames(images, frame_style):
    """Generate a single JPG file containing all favorite images with frames."""
    
    # Define frame styles with border colors
    frame_colors = {
        "Ornate Gold": (218, 165, 32),  # Gold
        "Classic Gold": (184, 134, 11),  # Dark Gold
        "Vintage Bronze": (139, 69, 19)  # Bronze
    }
    
    frame_color = frame_colors.get(frame_style, (0, 0, 0))
    border_thickness = 20  # Thickness of the frame
    
    img_size = (300, 300)  # Resize all images to a fixed size
    padding = 40  # Space between images
    columns = 3  # Number of images per row
    rows = (len(images) + columns - 1) // columns  # Calculate required rows

    # Create blank canvas (background)
    width = columns * (img_size[0] + padding) + padding
    height = rows * (img_size[1] + padding) + padding
    gallery_image = Image.new("RGB", (width, height), (255, 255, 255))

    draw = ImageDraw.Draw(gallery_image)

    for idx, img_path in enumerate(images):
        img = Image.open(img_path).convert("RGB")
        img = img.resize(img_size)

        # Calculate position on canvas
        x = (idx % columns) * (img_size[0] + padding) + padding
        y = (idx // columns) * (img_size[1] + padding) + padding

        # Draw the frame
        draw.rectangle(
            [(x - border_thickness, y - border_thickness), 
             (x + img_size[0] + border_thickness, y + img_size[1] + border_thickness)], 
            outline=frame_color, width=border_thickness
        )

        # Paste image inside the frame
        gallery_image.paste(img, (x, y))

    # Convert to JPG format
    img_bytes = BytesIO()
    gallery_image.save(img_bytes, format="JPEG")
    return img_bytes.getvalue()

# Function to enable downloading the favorites page
def download_favorites(images, frame_style):
    """Creates and provides a downloadable JPG file of the favorites page with frames."""
    if images:
        img_data = create_gallery_with_frames(images, frame_style)
        st.download_button(
            label="📥 Download Favorites as JPG",
            data=img_data,
            file_name="favorites_gallery_with_frames.jpg",
            mime="image/jpeg"
        )

# Streamlit App
st.sidebar.header("Favorites Page")
frame_choices = ["Ornate Gold", "Classic Gold", "Vintage Bronze"]
selected_frame = st.sidebar.selectbox("Choose a frame:", frame_choices)

# Load actual favorite images
favorite_images = load_favorites()
if favorite_images:
    st.title("🎨 Your Favorites Gallery")
    st.write("Enjoy your collection of favorite photos displayed in a museum-style setup!")
    
    # Display images with frames in Streamlit
    st.image([Image.open(img).resize((300, 300)) for img in favorite_images], width=300)
    
    # Download Button with Frames
    download_favorites(favorite_images, selected_frame)
else:
    st.write("No favorites added yet! Start selecting your best photos.")
