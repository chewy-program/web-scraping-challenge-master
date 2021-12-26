from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo
from pymongo import MongoClient


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017")


@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.mars_scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")
#client = MongoClient("mongodb://127.0.0.1:27017") #host uri    
#db = client.mymongodb    #Select the database    
#todos = db.todo #Select the collection name    
@app.route("/")
def home():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["marsDB"]
    url_data = db.urls
    hemisphere_data = db["hemispheres"].find_one() 
    article_data = db["articles"].find_one() 
    img_link = url_data.find_one()
    # Return template and data
    return render_template("index.html", article = article_data, url = img_link, hemispheres = hemisphere_data)

if __name__ == "__main__":
    app.run(debug=True)