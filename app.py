from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo
from pymongo import MongoClient


# Create an instance of Flask
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
mars_data = scrape_mars.mars_scrape()

@app.route("/scrape")
def scrape():

    # Run the scrape function
    mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")
    mars_data = scrape_mars.mars_scrape()

    # Update the Mongo database using update and upsert=True

    mongo.db.collection.update({}, mars_data, upsert=True)
    
    return redirect("/")   
@app.route("/")
def home():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["marsDB"]
    url_data = db["urls"]
    hemisphere_data = db["hemispheres"].find()
    article_data = db["articles"].find_one() 
    img_link = url_data.find_one()
    # Return template and data
    return render_template("index.html", article = article_data, url = img_link, hemispheres = hemisphere_data)

if __name__ == "__main__":
    app.run(debug=True)