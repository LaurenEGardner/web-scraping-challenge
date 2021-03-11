from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars as sm

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")
collection = mongo.db.destination

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    # @TODO: YOUR CODE HERE!
    mars_data = collection.find_one()
    print(mars_data)

    # Return template and data
    return render_template("index.html", mars=mars_data)