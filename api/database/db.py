from pymongo import MongoClient

mongo_uri = "mongodb+srv://cmpe295b:cmpe295bfinalproject@cmpe295bmasterproject.at3cjun.mongodb.net/test"
client = MongoClient(mongo_uri,compressors="snappy")
db = client.CMPE295BMasterProject
recipe_dataset = db.recipe_dataset
user_dataset = db.user

def initialize_db(app):
    db.init_app(app)
    