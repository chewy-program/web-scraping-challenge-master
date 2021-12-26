# %%
import pandas as pd 
from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pymongo



def mars_scrape(): 
    #connect to Mongo
    conn = "mongodb://localhost:27017/marsDB"
    client = pymongo.MongoClient(conn)
    #create DB 
    db = client.marsDB
    #create collections
    urlDB = db.urls
    hemisphereDB = db.hemispheres 
    articleDB = db.articles
    urlDB.drop()
    hemisphereDB.drop()
    articleDB.drop()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    marsurl = 'https://redplanetscience.com/'
    browser.visit(marsurl)

    # %%
    article_info = []
    for x in range(10):
            # HTML object
            html = browser.html
            # Parse HTML with Beautiful Soup
            soup = BeautifulSoup(html, 'html.parser')
            # Retrieve all elements that contain book information
            articles = soup.find_all('div', class_ = "list_text")

            # Scrape the [Mars News Site](https://redplanetscience.com/) and collect the latest News Title and Paragraph Text. 
            for article in articles:
                # Use Beautiful Soup's find() method to navigate and retrieve attributes
                #Assign the text to variables that you can reference later.
                title = article.find('div', class_= "content_title").text
                paragraph = article.find('div', class_ = "article_teaser_body").text
                article_dict = {
                    "title" : title, 
                    "paragraph" : paragraph
                }
                
                article_info.append(article_dict)
                articleDB.insert_one(article_dict)
    # %%
    jplurl = 'https://spaceimages-mars.com'
    browser.visit(jplurl)

    # %%
    featured_image_url = []

    # %%
    for x in range(50):
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        # Retrieve all elements that contain book information
        images = soup.find_all('div', class_="thmb")

        # Use splinter to navigate the site and find the image url for the current Featured Mars Image 
        #and assign the url string to a variable called `featured_image_url`.
        for image in images:
            div = image.find('img')
            src = div['src']
            link = ('https://spaceimages-mars.com/' + src)
            nospace = link.replace(' ', '%20')
            url_dict = {
                    "image_path" : nospace
                }
            featured_image_url.append(url_dict)
            urlDB.insert_one(url_dict)

    # %%
    marsfactsurl = 'https://galaxyfacts-mars.com'
    browser.visit(marsfactsurl)

    # %%
    # Visit the Mars Facts webpage [here](https://galaxyfacts-mars.com) 
    tables = pd.read_html(marsfactsurl)
    tables

    # %%
    #Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    marsdf = tables[1]
    marsdf.columns = ['Index', 'Mars']
    marsdf

        # %%
    total_df = tables[0]
    total_df.columns = ['Index', 'Mars', 'Earth']
    total_df

        # %%
        #Use Pandas to convert the data to a HTML table string.
    totalhtml = total_df.to_html()
    marshtml = marsdf.to_html()
    text_file = open("marsfacts.html", "w")
    text_file.write(totalhtml)
    text_file.write(marshtml)
    text_file.close()
    # %%
    #Visit the astrogeology site [here](https://marshemispheres.com/) to obtain high resolution images for each of Mar's hemispheres.
    hemiurl = 'https://marshemispheres.com/'
    browser.visit(hemiurl)


    # %%
    #Save both the image url string for the full resolution hemisphere image, 
    #and the Hemisphere title containing the hemisphere name. 
    #Use a Python dictionary to store the data using the keys `img_url` and `title`.
    hemi_list_dict= []
    for x in range(50):
        # HTML object
        html = browser.html
            # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
            # Retrieve all elements that contain book information
        links = soup.find_all('div', class_="item")

            # Use splinter to navigate the site and find the image url for the current Featured Mars Image 
            #and assign the url string to a variable called `featured_image_url`.
        for link in links:
            img = link.find('div', class_ = "description")
            img_link = img.find('a')
            href = img_link['href']
            img_url = ("https://marshemispheres.com/" + href)
            title = link.find('p').text
            marshemi_dict = {
                "img_url" : img_url,
                "title" : title
                }
            hemi_list_dict.append(marshemi_dict)
            hemisphereDB.insert_one(marshemi_dict) 
            

    browser.quit()
# Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` 
# that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

    marsdata = {
        "hemisphere" :hemi_list_dict, 
        "urlclean" : featured_image_url, 
        "marsfacts" : article_info}
    print(marsdata)