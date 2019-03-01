from flask import Flask, jsonify
import pymongo
from scrape_mars import scrape

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.reference_dict
collection = db.scraped_data

app = Flask(__name__)

@app.route("/scrape")
def scrape_function():
	scrape_dict = scrape()
	collection.update({}, scrape_dict, upsert = True)
	return 'successfully scraped'


@app.route("/")
def db_creation():
	collection.find()
	####pass into HTML####





if __name__ == "__main__":
    app.run(debug=True)

