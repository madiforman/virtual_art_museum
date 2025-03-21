# Museum of Virtual Art (MoVA)
![Build/Test Workflow](https://github.com/madiforman/virtual_art_museum/actions/workflows/build_test.yml/badge.svg)
![Coverage Status](https://coveralls.io/repos/github/madiforman/virtual_art_museum/badge.svg?branch=main)
## Project Type: Data Presentation

## Group Members:
- Madison Sanchez-Forman  
- Mya Strayer  
- Zhansaya Ussembayeva  
- Jennifer Kim  

## Questions of Interest: 
- Can we display archival artwork in a way that allows users to filter through it like they were at a musuem, i.e., by exhibit, artist, artistic movement or time period?  
- Can we pull and combine artworks from two museums into a single collection?  
 
## Project Goals: 
- Create a Streamlit-based web application for a virtual art museum.  
- Display both basic and historic information about artworks.  
- Implement search, filter, save, download and pop-up functionalities.    

## Use Cases: 
- View and explore art pieces using various filters, downloading a view of a user's favorite artworks.     
- Most of the website will be scrollable, with the option to click on an artpiece to learn more about the specific work. Filters for time period, art style, and region will be available on the sidebar and can be reset.  
- After a user has selected their favorite pieces, they will be able to select the 'Favorites' page and view a printable version of their favorite artwork.  

## Data Sources:
    - Metropolitan Museum of Art  
        - extensive database of more than 470,000 artworks from around the world, 
          available via its API  
        - https://metmuseum.github.io/  
    - Europeana 
        - metadata records on Europeana repository,  
          available via its Search API   
        - https://europeana.atlassian.net/wiki/spaces/EF/pages/2385739812/Search+API+Documentation#Query,-Filter,-and-Faceting-Fields  

# Usage: 
```
git clone https://github.com/madiforman/virtual_art_museum.git
conda create -f environment.yml
conda activate vamenv
pip install -e .
cd virtual_art_museum
```
### 1. Run the app:
```
streamlit run mova_home.py
```
### 2. Run Data Acquisition Scripts (please ensure that you have followed the first 5 usage steps)
```
cd data_aquisition
python met_museum.py
OR
python europeana.py
```
### 3. Run Tests
```
coverage run -m unittest discover
coverage report -m
```
