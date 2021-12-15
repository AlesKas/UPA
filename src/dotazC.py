import pandas as pd
from pymongo import MongoClient, collection

MONGO_USER = "user"
MONGO_PASSWD = "passwd"
MONGO_URI = "mongodb://{}:{}@localhost:10022/upa"
CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(CONNECTION_STRING)

#Databaze and Collection initialization
mydb = client["upa"]
cities_db = mydb['mesta']
cities_infection_db = mydb['obce']
cities_vaccination_db = mydb['ockovani-geografie']

cities_arr = []
age_0_14_arr = []
age_15_59_arr = []
age_60_plus_arr = []
infection_arr = []
vaccination_arr = []
year = '2020-12-31'

#Find all cities in DB
cities_query = cities_db.find()
for city in cities_query:
    if city['vuzemi_txt'] in cities_arr:
        continue
    else:
        if "KRAJ" in city['vuzemi_txt'].upper():
            continue
        elif "republika" in city['vuzemi_txt']:
            continue
        elif "-venkov" in city['vuzemi_txt']:
            continue
        elif "-jih" in city['vuzemi_txt']:
            continue
        elif "-sever" in city['vuzemi_txt']:
            continue
        elif "-západ" in city['vuzemi_txt']:
            continue
        elif "-východ" in city['vuzemi_txt']:
            continue
        elif "Praha" in city['vuzemi_txt']:
            continue
        else:
            cities_arr.append(city['vuzemi_txt'])

#Choose only first 50 cities 
cities_arr = cities_arr[0:50]

# ################################################################################################### FINDING DATA FOR CITIES ###################################################################################################
for city in cities_arr:    
    #Number of people between 0-14 age
    age_0_14_counter = 0
    query_0_5 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "0 až 5 (více nebo rovno 0 a méně než 5)", "pohlavi_txt" : float('nan')})
    query_5_10 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "5 až 10 (více nebo rovno 5 a méně než 10)", "pohlavi_txt" : float('nan')})
    query_10_15 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "10 až 15 (více nebo rovno 10 a méně než 15)", "pohlavi_txt" : float('nan')})
    
    for q in query_0_5: age_0_14_counter += q["hodnota"]
    for q in query_5_10: age_0_14_counter += q["hodnota"]
    for q in query_10_15: age_0_14_counter += q["hodnota"]
    age_0_14_arr.append(age_0_14_counter)

    #Number of people between 15-59 age
    age_15_59_counter = 0
    query_15_20 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "15 až 20 (více nebo rovno 15 a méně než 20)", "pohlavi_txt" : float('nan')})
    query_20_25 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "20 až 25 (více nebo rovno 20 a méně než 25)", "pohlavi_txt" : float('nan')})
    query_25_30 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "25 až 30 (více nebo rovno 25 a méně než 30)", "pohlavi_txt" : float('nan')})
    query_30_35 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "30 až 35 (více nebo rovno 30 a méně než 35)", "pohlavi_txt" : float('nan')})
    query_35_40 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "35 až 40 (více nebo rovno 35 a méně než 40)", "pohlavi_txt" : float('nan')})
    query_40_45 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "40 až 45 (více nebo rovno 40 a méně než 45)", "pohlavi_txt" : float('nan')})
    query_45_50 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "45 až 50 (více nebo rovno 45 a méně než 50)", "pohlavi_txt" : float('nan')})
    query_50_55 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "50 až 55 (více nebo rovno 50 a méně než 55)", "pohlavi_txt" : float('nan')})
    query_55_60 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "55 až 60 (více nebo rovno 55 a méně než 60)", "pohlavi_txt" : float('nan')})
    
    for q in query_15_20: age_15_59_counter += q["hodnota"]
    for q in query_20_25: age_15_59_counter += q["hodnota"]
    for q in query_25_30: age_15_59_counter += q["hodnota"]
    for q in query_30_35: age_15_59_counter += q["hodnota"]
    for q in query_35_40: age_15_59_counter += q["hodnota"]
    for q in query_40_45: age_15_59_counter += q["hodnota"]
    for q in query_45_50: age_15_59_counter += q["hodnota"]
    for q in query_50_55: age_15_59_counter += q["hodnota"]
    for q in query_55_60: age_15_59_counter += q["hodnota"]
    age_15_59_arr.append(age_15_59_counter)
    
    #Number of people between 60+ age
    age_60_plus_counter = 0
    query_60_65 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "60 až 65 (více nebo rovno 60 a méně než 65)", "pohlavi_txt" : float('nan')})
    query_65_70 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "65 až 70 (více nebo rovno 65 a méně než 70)", "pohlavi_txt" : float('nan')})
    query_70_75 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "70 až 75 (více nebo rovno 70 a méně než 75)", "pohlavi_txt" : float('nan')})
    query_75_80 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "75 až 80 (více nebo rovno 75 a méně než 80)", "pohlavi_txt" : float('nan')})
    query_80_85 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "80 až 85 (více nebo rovno 80 a méně než 85)", "pohlavi_txt" : float('nan')})
    query_85_90 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "85 až 90 (více nebo rovno 85 a méně než 90)", "pohlavi_txt" : float('nan')})
    query_90_95 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "90 až 95 (více nebo rovno 90 a méně než 95)", "pohlavi_txt" : float('nan')})
    query_95_100 = cities_db.find({"casref_do":  {'$regex': year}, "vuzemi_txt": city, "vek_txt": "Od 95 (ví­ce nebo rovno 95)", "pohlavi_txt" : float('nan')})
    
    for q in query_60_65: age_60_plus_counter += q["hodnota"]
    for q in query_65_70: age_60_plus_counter += q["hodnota"]
    for q in query_70_75: age_60_plus_counter += q["hodnota"]
    for q in query_75_80: age_60_plus_counter += q["hodnota"]
    for q in query_80_85: age_60_plus_counter += q["hodnota"]
    for q in query_85_90: age_60_plus_counter += q["hodnota"]
    for q in query_90_95: age_60_plus_counter += q["hodnota"]
    for q in query_95_100: age_60_plus_counter += q["hodnota"]
    age_60_plus_arr.append(age_60_plus_counter)

    #INFECTION AND VACCINATION COUNTER per city for 2021
    year2 = "2021-"
    infection_counter = 0
    vaccination_counter = 0

    if "-město" in city:
        city = city[:-6]
 
    query_infection = cities_infection_db.find({"obec_nazev":  city, "datum":  {'$regex': year2}})
    query_vaccination = cities_vaccination_db.find({"orp_bydliste":  city, "datum":  {'$regex': year2}})
        
    for q in query_infection: infection_counter += q['nove_pripady'] 
    for q in query_vaccination: vaccination_counter += q['pocet_davek']  
    
    infection_arr.append(infection_counter)
    vaccination_arr.append(vaccination_counter)

#Export to CSV file
chart = {'mesta': cities_arr, 'pocet obyvatel 0-14 let': age_0_14_arr, 'pocet obyvatel 15-59 let': age_15_59_arr, 'pocet obyvatel 60+': age_60_plus_arr, 'pocet nakazenych za posledni 4 mesice': infection_arr, 'pocet ockovani za posledni 4 mesice': vaccination_arr}
df = pd.DataFrame(chart,columns=['mesta','pocet obyvatel 0-14 let', 'pocet obyvatel 15-59 let', 'pocet obyvatel 60+', 'pocet nakazenych za posledni 4 mesice', 'pocet ockovani za posledni 4 mesice'])
df.to_csv('Mesta_dolovani.csv', encoding='UTF-16')

