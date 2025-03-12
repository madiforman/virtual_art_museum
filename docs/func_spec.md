Functional Specification  

Background: This project intends to create a Streamlit app that allows users to peruse artworks, apply simple filters, interact with them to learn more, and save aside their selected favorites in a downloadable view.  

User Stories:  
    1. 
        Who: Hugh is an art history student at a University in Alabama interested in exploring historical art.  
        Wants: to find a website that allows him to examine art from the United States and Europe at the same time.    
        Interaction methods: Hugh will be scrolling through the database and exploring similar artworks  
        Needs: To go through a large quantity of art and be able to find similar works or more information on a given piece  
        Skills: Not many skills needed, basic use of computer  
    2.   
        Who: Nancie is an art collector in Paris, France looking to find a large amount of contemporary art and pursue it for her collection.  
        Wants: To filter art by artist/century/movement  
        Interaction methods: Clean filtering   
        Needs: Find location of artist or collection   
        Skills: More advanced background on art (i.e. movement names, mediums, etc)  
    3. 
        Who: Rosey is a data analyst at an art gallery and looking to analyze data from two large art hubs (i.e. New York and Europe) trying to analyze the differences between these two regions.  
        Wants: Explore differences in art from different regions and see what art to put in her gallery based on different trends  
        Interaction methods: Analytics dashboard of art trends in NY vs Europe  
        Needs: Analytics dashboard of art trends in NY vs Europe  
        Skills: Advanced computational skills - can easily navigate the analytics page   

Data Sources:  
    1) Metropolitan Museum of Art - https://metmuseum.github.io/  
        - We will be using the datasets provided by the Metropolitan Museum of Art (MET) of information on artworks in its collections for unrestricted commercial and noncommercial use, available through its API  
        - The artwork information is provided in dictionary format (JSON)  
        - The artwork images are in JPEG format  
        - https://github.com/metmuseum/openaccess also provides a CSV file containing artwork information. However, the images still have to be retrieved via API requests  

    2) Europeana - https://europeana.atlassian.net/wiki/spaces/EF/pages/2385739812/Search+API+Documentation#Query,-Filter,-and-Faceting-Fields  
        - We will also be using metadata records and media provided by Europeana on its repository  
        - The Europeana Search API allows users to conduct a keyword search, and the API will return all results that match the keyword  
        - Responses are formatted in JSON  

Use Cases:
    1. Use Case 1 
        - Objective of the user: Building a list of desired artworks. The default page will display a collection of images from the MET and Europeana. Users can use the search bar to filter the images by year, style, keywords, or other criteria  
        - Expected interactions between the user and our system:  
            - We expect the user to filter the images based on their preferences and add them to favorites for easy access  
            - The favorites page will include a download functionality  
            
    2. Use Case 2
        - Objective of the user: learning more about an art piece  
        - Expected interactions between the user and our system  
            - Users can click on the “more details” button for detailed information on each artwork

Milestones:  
    Preliminary plan:  
    - Collect and preprocess large datasets containing images and artwork information from the MET and Europeana databases and them  - Compile them into a Pandas dataframe  
    - Develop a Streamlit app that retrieves and display the data as a virtual art museum  
    - Add pop-up functionality and a favorites page with a download option  

1. Basic data aquisition  
    - Collect and preprocess datasets from the MET  
    - Collect and preprocess datasets from Europeana  
2. Homepage  
    - Design a basic grid layout with a search bar  
    - Integrate it with MET and Europeana data to begin designing the virtual art museum   
3. Single piece pop up  
    - Explore ways to implement pop-up functionality within Streamlit’s basic framework  
    - Integrate with the main homepage  
4. Favorites page  
    - Create a favorites page that updates as users select their favorite images  
    - Add a download option  
5. Analytics  
    - Create an analytics page containing valuable insights for data professionals/enthusiasts  
6. Personalization  
    - Enable users to filter artwork based on their preferences or  goals  
    - The favorites page will allow users to save and revisit their favorite art pieces  