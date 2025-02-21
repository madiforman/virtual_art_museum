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




# import requests

# # Replace with your actual API key
# api_key = "etendinfi"


# # Basic request to search for "Mona Lisa"


# def fetch_artwork(search_term, key):
#     url = f"https://api.europeana.eu/record/v2/search.json?wskey={key}&query=mona+lisa"

#     params = {
#         "wskey": key,
#         "query": search_term,
#         "qf": "TYPE.IMAGE",
#         "profile": "rich",
#         "media": "true"     #returns results with media 
#     }
#     try:
#         response = requests.get(url, params=params)
#     except requests.RequestsException as e:
#         st.error(f"Error fetching")
#         return None
    
# def display(artwork):   #for artwork inresults["items"]
#     pass

# def main():
#     pass

# if __name__ == "__main__":
#     main()
# response = requests.get(url)
# data = response.json()

# test = data['items']
# for t in test:
#     print(f"{t}\n")
