**Component Specification:**

**Data manager:**

    1) What it does  
        - Queries MET and Europeana data  
        - Provides ability to filter or search data   
    2) Required input    
        - Users can enter search words in the search bar or apply   filters   
    3) Output   
        - The homepage shows queried data (images and basic art details) in a grid format  
        - When users perform a search or apply filters, the interface updates automatically   
        
**Visualization manager:**  

    1) What it does  
        - Saves favorite artworks   
        - Analytical charts / visualization  
    2) Required input
        - Users can click the ‘Favorites’ button to add to their favorites  
        - Users can view the analytics page to view useful insights  
    3) Output
        - When users click the favorites button, the corresponding image will be added to the Favorites page  
        - We envision adding an analytics page on the artworks of interest  

**App Functionality:**

    1) What it does  
        Searching:  
            - Ability to search by keyword  
            - Filter data to range of years or by time period  
            - View artwork by region  
            - Select specific art styles  
        Favoriting:  
            - Save aside a select number of favorited artwork   
            - Ability to save a 'gallery view' of a user's favorites  
        Clicking:  
            - Show more information about the selected artpiece  
            - Ability to easily return to the homepage 

    2) Required input  
    These functionalities will support the data and visualization managers. Hence, it requires the same type of input from users  

    3) Output  
    It allows the data and visualization managers to perform seamlessly  

**User Interaction/Workflow Walkthrough:**

    Basic examples:  
        - User enters the site and scrolls through ~15 pictures   
        - User opens sidebar to select more specific filters (Style, Time Period, etc.)  
        - User continues to scroll and selects pieces for the favorites  
        - User clicks on 'Favorites' button and is brought to favorites page  
        - User downloads their gallery view   
    More specific examples:  
        - User enters the site and sees a beautiful Van Gogh  
        - They've never heard of Van Gogh so they click on the picture to find out the artist  
        - They LOVE it so they search 'Van Gogh' in the keyword search and filter the results to Impressionism  
        - ** From the Analytics tab, they look at what proportion of the Van Goghs in our database are from European versus American museums
