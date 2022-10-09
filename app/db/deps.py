from pymongo import MongoClient
import urllib

MONGO_SRV = 'mongodb+srv://Sagar:'+urllib

# DB
mongo_client = MongoClient(MONGO_SRV)
db = mongo_client['Channels']