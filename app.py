from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars as sm
import requests

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template
@app.route("/")
def home():

    marsInfo = mongo.db.marsInfo.find_one()
    return render_template("index.html", marsInfo=marsInfo)

# Route that will trigger the web scrape function
@app.route("/scrape")
def scrape():

    marsInfo = mongo.db.marsInfo

    # Run scrape functions and save the data
    marsData = sm.scrapeMars()
    marsInfo.update({}, marsData, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)