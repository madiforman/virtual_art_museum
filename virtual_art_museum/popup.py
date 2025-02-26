import streamlit as st
import requests

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

# Fetch the image data
def popup_posts():
    temp = get_posts()

    if temp and temp.get("primaryImage"):
        image_url = temp["primaryImage"]
        title = temp.get("title", "No description available.")  
        name=temp.get("artistDisplayName","No artist name available")


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
                width: 100vw;
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

            .artist-header {{color:gray;
                font-size: 20px;
                font-family: Verdana, sans-serif;
                margin-bottom: 0;}}
            
            .title-header {{color:gray;
                font-size: 20px;
                font-family: Verdana, sans-serif;
                margin-bottom: 0;}}

            .close-btn {{
                position: absolute;
                top: 15px;
                right: 25px;
                background: lightgray;
                color: white;
                border: none;
                padding: 8px 14px;
                font-size: 10px;
                cursor: pointer;
                border-radius: 5px;
            }}

            .clickable-image {{
                cursor: pointer;
            }}
        </style>

        <div class="clickable-image" onclick="openPopup()">
            <img src="{image_url}" alt="Thumbnail Image" width="300">
        </div>
        <div class="popup-overlay" id="popupOverlay">
            <div class="popup-container">
                <button class="close-btn" onclick="closePopup()">X</button>
                <div class="popup-image">
                    <img src="{image_url}" alt="Enlarged Image">
                </div>
                <div class="popup-text">
                    
                    <p class="title-header">Title</p>
                    <p>{title}</p>
                    <p class="artist-header">Artist</p>
                    <p>{name}</p> 
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
        </script>
        """

        # Render the HTML code
        st.components.v1.html(html_code, height=600)
popup_posts()