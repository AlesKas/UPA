import bs4
import pandas as pd
from os import getenv
from pprint import pprint
from pymongo import MongoClient
from urllib.request import urlopen
import pip._vendor.requests

#Creating Mongo client
MONGO_USER = getenv("MONGO_USERNAME")
MONGO_PASSWD = getenv("MONGO_PASSWORD")
MONGO_URI = getenv("MONGO_URI")

CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(MONGO_URI)
mydb = client["upa"]

"""
My local mongodb setting
client = MongoClient('localhost', 27017)
db = client['upa']
"""

#HTML parsing
base_url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19"
data = pip._vendor.requests.get(base_url)
parsed_data = bs4.BeautifulSoup(data.text, "html.parser")
div = parsed_data.find(name="div", id="react-app")
dataset = div.get('data-datasets-metadata')
csv_files_arr = []
header = True

#Search for csv file on web, extract data and isert them to db
for dat in dataset.split(',"url":"'):
    #Skip the header
    if header:
        header = False
        continue

    #Create url for csv files 
    split_dctitle = dat.split('","dc:title":')  
    csv_url = base_url + "/" + split_dctitle[0] 
   
    #Get collection name
    collection_name = split_dctitle[0].split('.csv')
    collection_name = collection_name[0]
    
    #Create new collection
    mycol = mydb[collection_name]

    #Inserting data to mongodb
    if collection_name == 'prioritni-skupiny':
        df = pd.read_csv(csv_url)
        df_data = df.to_dict('records')
        mycol.insert_many(df_data, ordered=False)
      

""""
cursor = mycol.find({})
print(cursor)
for document in cursor: 
    print(document)

"""