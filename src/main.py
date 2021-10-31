import pandas as pd
from os import getenv
from pymongo import MongoClient
from datetime import timedelta, datetime

#Creating Mongo client
MONGO_USER = getenv("MONGO_USERNAME")
MONGO_PASSWD = getenv("MONGO_PASSWORD")
MONGO_URI = getenv("MONGO_URI")
CSV_URL = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/{}.csv"
CSV_FILES = ["zakladni-prehled", "kraj-okres-testy"]
CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(CONNECTION_STRING)
db = client["upa"]

# filterDate for filtering records
# Can be changed by changing timedelta
filterDate = datetime.now() - timedelta(1)
filterDate = datetime.strftime(filterDate, '%Y-%m-%d')


for csv_file in CSV_FILES:
    # Create collection for each csv data
    column = db[csv_file]
    data_url = CSV_URL.format(csv_file)
    df = pd.read_csv(data_url)
    # Parse date column 
    df['datum'] = pd.to_datetime(df["datum"])
    # Filter records
    df = df[df['datum'] >= filterDate]
    df_data = df.to_dict('records')
    # Insert records to DB
    column.insert_many(df_data)
