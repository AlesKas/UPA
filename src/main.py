import pymongo

from os import getenv
from pprint import pprint
from pymongo import MongoClient

MONGO_USER = getenv("MONGO_USERNAME")
MONGO_PASSWD = getenv("MONGO_PASSWORD")
MONGO_URI = getenv("MONGO_URI")

CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(CONNECTION_STRING)
mydb = client["upa"]
mycol = mydb["upa"]
cursor = mycol.find({})
for document in cursor: 
    pprint(document)