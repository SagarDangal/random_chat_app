from pymongo import MongoClient
import urllib

MONGO_SRV = 'mongodb+srv://Sagar:'+urllib.parse.quote('Appleball@12345')+'@chat.o9rso.mongodb.net/Chat?retryWrites=true&w=majority'

# DB
mongo_client = MongoClient(MONGO_SRV)
db = mongo_client['Channels']