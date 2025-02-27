Technology Review

**Markdown Section 1: Background & Use Case**

● What’s your application?

A virtual art museum 

● What use case are you trying to solve?

Use Cases: 

View and explore art pieces using various filters and download favorite artworks 
resettable filters for time period, art style and region, which will allow users to explore similar artworks
users will be able to select the ‘Favorites’ page and view a printable version of their favorite artworks 
Click an image to learn more about the specific artwork
the  pop-up window will show more details about the artwork, such as title, artist name, year, style, and location
View the analytics page 

● What about it needs a Python library?
Finding a python library that allows someone to build a web application with minimal coding experience

**Markdown Section 2: Python Package Choices**

● Find 2-3 Python libraries that potentially address your use case
Flask
Streamlit
● Describe the libraries

1) Flask
Author: Armin Ronacher 
ReadMe: “Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.”
https://github.com/pallets/flask
Flask is a lot simpler than other development frameworks for python web apps however requires heavier lifting to build out a web application. 

2) Streamlit
Author :  Pablo Fonseca (need to confirm) 
ReadMe: “Streamlit lets you transform Python scripts into interactive web apps in minutes, instead of weeks. Build dashboards, generate reports, or create chat apps.”
https://github.com/streamlit/streamlit/blob/develop/README.md
Streamlit is the simplest and fastest of development frameworks for python
Overall: 
	The two packages we chose to compare and contrast are Flask and Streamlit. Flask is a general purpose kit for building a web application from scratch. It gives you the fundamental pieces of building the web application but allows you to control its functionality. In contrast, Streamlit is marketed towards data scientists. According to Restack, “Streamlit simplifies data app creation with minimal code, making it ideal for data scientists and analysts”. Between the two packages there is a tradeoff between control and simplicity. Flask allows for a more granular definition of the aesthetics and functionality of a webpage at the expense of simplicity of use. Given our individual backgrounds and desire for a simple aesthetic, Streamlit meets the needs of our use case. The other package our application will depend on is Requests. This will be needed to make API requests to the associated databases. 

**Markdown Section 3: Package Comparison** 

For the package comparison, we explored using Flask and Streamlit. Both are python wrappers that allow a developer to create a webpage application based on a python file, however Flask additionally requires an html file to be developed in order to run the web component of the application. Streamlit offers ease-of-use and has been designed to easily create data-driven applications using pandas but is limited by its built-in components and layout functionality, while Flask on the other hand, has much greater flexibility. It can incorporate HTML, CSS, and external libraries, and has greater computational efficiency compared to Streamlit, but requires manual setup for the frontend. While both have the necessary functionality to support our application’s use cases, Streamlit is much more compatible with Python’s pandas structure and can filter and search data easier than Flask. From examples and the package documentation, Streamlit poses two issues for our project: lag times (delays) as the application gets more complex, and difficulties embedding CSS/HTML code into Streamlit components (Streamlit does allow for CSS/HTML code to be embedded, but as separate components). Flask has much better computational speed and is easily embeddable with other frameworks, but requires the developers to have strong understanding of HTML/CSS frameworks.

[Streamlit]
image view via API : 
st.image: ://docs.streamlit.io/develop/api-reference/media/st.image
filter: 
st.selectbox: https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox
st.multiselect
https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect
Download (check if it works for images): 
st.download_button: https://docs.streamlit.io/develop/api-reference/widgets/st.download_button
-Open issues: 
Download delay : https://github.com/streamlit/streamlit/issues/5053?utm_source=chatgpt.com
[Flask]
image view via API
https://flask.palletsprojects.com/en/stable/api/
filter: might not be available 
send_file : https://flask.palletsprojects.com/en/stable/api/#flask.send_file
Open issues: Custom commands
https://github.com/pallets/flask/issues/5673

**Markdown Section 4: Your Choice**

● What did you choose to use?

We compared two Python libraries: Flask and Streamlit and decided to use Streamlit.

● Why did you choose it?

First, Streamlit does not require any deep knowledge or coding experience. It is a perfect solution for easy projects that are time-limited, especially data science projects. Additionally, Streamlit provides built-in components for interactive visualization widgets and updates the app automatically when changes are made in the code.

**Markdown Section 5: Drawbacks/Remaining Concerns**

● Is there anything in the “con” list to be concerned about?

Yes, streamlit has a few drawbacks. 
Streamlit’s simplicity comes at the cost of limited control over the app’s design and layout. Customizing the UI beyond the built-in components can be challenging. Regarding the scalability, Streamlit is not designed for large-scale production applications. It may struggle with performance issues when handling high traffic or complex workflows. Also, managing app state, such as preserving user inputs across interactions, can be difficult in Streamlit, as it reruns the entire script on every interaction. Compared to Flask, Streamlit is less flexible for building general-purpose web applications, as it is specifically optimized for data-centric use cases.

● Will you have to mitigate any drawbacks?

Yes, we will need to address some of these drawbacks:
For the basic UI needs, we will use Streamlit’s built-in components. If more customization is required, we may consider integrating custom HTML/CSS.

● What will you watch out for?

We will ensure the app remains intuitive and responsive, even with limited customization options and produces the desired output properly, does not lag and freeze. We will monitor the app’s performance, especially as the dataset or user interactions grow in complexity.
If the project evolves beyond Streamlit’s capabilities, we will be prepared to transition to a more flexible framework like Flask.

