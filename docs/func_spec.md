**Functional Specification**

**Background:** This project intends to create a Streamlit app that allows users to peruse artworks, apply simple filters, interact with them to learn more, and save aside their selected favorites in a downloadable view.  

**User profile:**  Our system will be used by both the general audience who are interested in art and analysts who can engage with data. They definitely can interact with the web app because Streamlit provides a user-friendly interface.

**Data Sources:**

_Metropolitan Museum of Art_ - https://metmuseum.github.io/. 
We will download a bulk file that has everything except the image URLs and prior to building the app, filter out any objects that don't have an image to display. We will process the data to remove unnecessary columns, increase readability and create fields like Century.
    
_Europeana_ - https://europeana.atlassian.net/wiki/spaces/EF/pages/2385739812/Search+API+Documentation#Query,-Filter,-and-Faceting-Fields. It is a massive dataset that we have to query for general art terms. Structures similarly with columns as titles, creators, etc.

**Use Cases:**

    1. Building a list of desired art
    2. Learning more about an art piece    
    
**User Stories:**

    1. 
        Who: Hugh is an art history student at a University in Alabama interested in exploring historical art.  
        Wants: to find a website that allows him to examine art from the United States and Europe at the same time.    
        Interaction methods: Hugh will be scrolling through the database and exploring similar artworks  
        Needs: To go through a large quantity of art and be able to find similar works or more information on a given piece  
        Skills: Not many skills needed, basic use of computer  
        
    2.   
        Who: Nancie is an art collector in Paris, France looking to find a large amount of contemporary art and pursue it for her collection.  
        Wants: To filter art by artist/century/movement  
        Interaction Methods: Clean filtering, add to favorites and download it to see how it can look on her wall  
        Needs: Find location of artist or collection  
        Skills: More advanced background on art (i.e. movement names, mediums, etc)   

**Use Cases:**

    1. Use Case 1 
        - Objective of the user: Building a list of desired artworks. The default page will display a collection of images from the MET and Europeana. Users can use the search bar to filter the images by year, style, keywords, or other criteria  
        - Expected interactions between the user and our system:  
            - We expect the user to filter the images based on their preferences and add them to favorites for easy access  
            - The favorites page will include a download functionality  
            
    2. Use Case 2
        - Objective of the user: learning more about an art piece  
        - Expected interactions between the user and our system  
            - Users can click on the “more details” button for detailed information on each artwork  
