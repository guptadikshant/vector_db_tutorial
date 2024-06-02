import os
import pymongo
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGODB_URL = os.getenv("MONGODB_URL")

client = pymongo.MongoClient(MONGODB_URL)

db = client.sample_mflix
collection = db.movies

items = collection.find().limit(5)

for item in items:
    print(item)

