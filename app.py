from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



# Define the flask root route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    #img_dict = mongo.db.mars.find({'hemisphere_image_urls.0.img_url'})
    return render_template("index.html", mars=mars)

# Set up the scraping route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__":
    app.run()