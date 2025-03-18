import streamlit as st
import os
from PIL import Image
import base64
from io import BytesIO

# Function to get images from the 'favorites' directory
def load_favorites():
    """Fetch all image files from the favorites folder."""
    favorites_folder = "favorites"
    if not os.path.exists(favorites_folder):
        os.makedirs(favorites_folder)
    return [os.path.join(favorites_folder, img) for img in os.listdir(favorites_folder) if img.endswith(('png', 'jpg', 'jpeg'))]

# Function to save uploaded images to the favorites folder
def save_uploaded_file(uploaded_file):
    """Save uploaded file to the favorites folder."""
    favorites_folder = "favorites"
    if not os.path.exists(favorites_folder):
        os.makedirs(favorites_folder)
    file_path = os.path.join(favorites_folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Function to display images inside frames
def display_favorites(images, frame_style):
    """Display favorite images with proper museum-style frames."""
    st.title("🎨 Your Favorites Gallery")
    st.write("Enjoy your collection of favorite photos displayed in a museum-style setup!")

    cols = st.columns(3)  # Adjust grid layout

    frame_styles = {
        "Ornate Gold": "border: 20px solid gold; padding: 10px; border-radius: 15px;",
        "Classic Gold": "border: 15px solid goldenrod; padding: 10px; border-radius: 5px;",
        "Vintage Bronze": "border: 15px solid saddlebrown; padding: 10px; border-radius: 10px;"
    }

    for i, img_path in enumerate(images):
        with cols[i % 3]:
            if os.path.exists(img_path):  # Ensure image exists
                img = Image.open(img_path)
                st.markdown(
                    f"""
                    <div style="{frame_styles[frame_style]} text-align: center; display: inline-block;">
                        <img src="data:image/png;base64,{image_to_base64(img)}" style="width: 100%;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error(f"Image not found: {img_path}")

# Function to convert images to Base64 for embedding in HTML
def image_to_base64(image):
    """Convert image to Base64 encoding for HTML rendering."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Streamlit App
st.sidebar.header("Favorites Page")
frame_choices = ["Ornate Gold", "Classic Gold", "Vintage Bronze"]
selected_frame = st.sidebar.selectbox("Choose a frame:", frame_choices)

# Image Upload Feature
st.sidebar.subheader("Upload a New Favorite Image")
uploaded_file = st.sidebar.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

# Load actual favorite images
favorite_images = load_favorites()
if favorite_images:
    display_favorites(favorite_images, selected_frame)
else:
    st.write("No favorites added yet! Start selecting your best photos.")
