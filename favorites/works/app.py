from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

# Directory to store favorite images
FAVORITES_FOLDER = "favorites"
if not os.path.exists(FAVORITES_FOLDER):
    os.makedirs(FAVORITES_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Function to check valid file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Convert image to Base64 for embedding
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Get all images in the Favorites folder
def load_favorites():
    return [img for img in os.listdir(FAVORITES_FOLDER) if allowed_file(img)]

# Flask route to serve images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(FAVORITES_FOLDER, filename)

# Home Route - Displays Favorite Images
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(FAVORITES_FOLDER, filename))

    favorite_images = load_favorites()
    frame_styles = {
        "Ornate Gold": "border: 20px solid gold; padding: 10px; border-radius: 15px;",
        "Classic Gold": "border: 15px solid goldenrod; padding: 10px; border-radius: 5px;",
        "Vintage Bronze": "border: 15px solid saddlebrown; padding: 10px; border-radius: 10px;"
    }
    return render_template("index.html", images=favorite_images, frame_styles=frame_styles)

# Route to delete an image from Favorites
@app.route("/delete/<filename>")
def delete_image(filename):
    file_path = os.path.join(FAVORITES_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
