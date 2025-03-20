## MoVa Streamlit App

## How to Run the App Locally

[](#)

### 1\. Clone the Git Repo

[](#)

First, to obtain a local copy of our repository, run the following `git` command:

```shell
git clone https://github.com/madiforman/virtual_art_museum.git
```

[](#)

### 2\. Local Environment Setup

[](#)

Next, install our `conda` environment `vamenv` as specified in the file `environment.yml`:

```shell
conda env create -f environment.yml
```

Once the Conda environment is created, it can be activated and deactivated with the following commands:

```shell
conda activate vamenv
conda deactivate
```

[](#)

### 3\. Local Environment Setup

Let's begin! Open the virtual_art_museum folder inside our virtual_art_museum directory and run this command:

```shell
streamlit run mova_home.py
```
Your browser should open the new tab with our MoVA's Home Page:

![Figure_1](Screenshots/1.png)

You can access the images from MET Museum and Europeana in one place now! WOW!

![Figure_2](Screenshots/2.png)

The user has an ability to add the images to Favorites and click the button for more details:

![Figure_3](Screenshots/3.png)
![Figure_4](Screenshots/4.png)

While adding to your Favorites, you will be notified by the message in the green box (if added successfully, 
yellow - if this image is already in  your Favorites).

![Figure_5](Screenshots/5.png)

Clicking on the Details button will give you more information about the art piece:

![Figure_6](Screenshots/16.png)

Additionally, our app allows you to play with different filters to choose the most suitable art:

![Figure_7](Screenshots/7.png)

At the top right corner we installed a Favorites page and Refresh button so that you can update the list of images on the main:

![Figure_8](Screenshots/8.png)
![Figure_9](Screenshots/9.png)

If you click on this lovely red heart, it will bring you to our Favorites page. Here you have an opportunity to Download and Remove images.

![Figure_10](Screenshots/10.png)
![Figure_12](Screenshots/12.png)
![Figure_13](Screenshots/13.png)
![Figure_14](Screenshots/14.png)

Downloaded Favorites image would look like that:
![Figure_14](Screenshots/15.png)

I hope you find it useful!
