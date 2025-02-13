import streamlit as st
import requests
#images -> primaryImage
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
            
temp = get_posts()
st.image(temp['primaryImage'])
