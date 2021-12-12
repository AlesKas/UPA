import pandas as pd
from pymongo import MongoClient
from datetime import timedelta, datetime

#Creating Mongo client
MONGO_USER = "user"
MONGO_PASSWD = "passwd"
MONGO_URI = "mongodb://{}:{}@localhost:10022/upa"
CSV_URL = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/{}.csv"
CSV_FILES = ["zakladni-prehled", "kraj-okres-testy", "hospitalizace", "ockovani", "ockovani-umrti", "ockovani-zakladni-prehled", "osoby", "testy-pcr-antigenni", "umrti", "vyleceni"]
CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(CONNECTION_STRING)
db = client["upa"]

# filterDate for filtering records
# Can be changed by changing timedelta
filterDate = datetime.now() - timedelta(730)
filterDate = datetime.strftime(filterDate, '%Y-%m-%d')


for csv_file in CSV_FILES:
    # Create collection for each csv data
    column = db[csv_file]
    data_url = CSV_URL.format(csv_file)
    df = pd.read_csv(data_url)
    # Parse date column 
    # Only ockovani-zakladni-prehled does not have datum key
    if csv_file != "ockovani-zakladni-prehled":
        # Filter records
        df = df[pd.to_datetime(df['datum']) >= filterDate]
        # remove rows thats already inserted in db
        if (list(column.find()) != []):
            df = pd.concat([df,df.loc[df['datum'].isin(pd.DataFrame(list(column.find())).datum)]]).drop_duplicates(keep=False)
    df_data = df.to_dict('records')
    # Insert records to DB
    if df_data != []:
        column.insert_many(df_data)

#Add kapacity-intenzivni-pece-zdravotnicke-zarizeni for vlastni dotaz
capacity_url = 'https://dip.mzcr.cz/api/v1/kapacity-intenzivni-pece-zdravotnicke-zarizeni.csv'
capacity_db = db['kapacity-intenzivni-pece-zdravotnicke-zarizeni']
capacity_df = pd.read_csv(capacity_url)
capacity_data = capacity_df.to_dict('records')
capacity_db.insert_many(capacity_data, ordered=False)
