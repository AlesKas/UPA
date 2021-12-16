from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from os import getenv

MONGO_USER = "user"
MONGO_PASSWD = "passwd"
MONGO_URI = "mongodb://{}:{}@localhost:10022/upa"
CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(CONNECTION_STRING)

#Databaze and Collection initialization
mydb = client["upa"]
infected_db = mydb['osoby']
capacity_db = mydb['kapacity-intenzivni-pece-zdravotnicke-zarizeni']
hospitalization_db = mydb['hospitalizace']

months = ["leden", "únor", "březen", "duben", "květen", "červen",
          "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]

#Empty arrays for plotting data
infected_home_country_arr = []
infected_foreign_country_arr = []
upv_total_capacity_arr = []
upv_hospitalization_capacity_arr = []
year_arr = []
foreign_country_infection_dictionary = {}

# ###################################################################################################################   PART 1   ###################################################################################################################
# TOP 10 FOREIGN COUNTRIES WHERE INFECTION COME FROM
years = ["2020-", "2021-"]
for year in years:
    year_clear = year

    for month in range(12):
        if month + 1 < 10:
            year += "0" + (str(month + 1))
        else:
            year += (str(month + 1))

        #Total count of infected in foreign country
        infection_foreign_country = infected_db.find(
            {"datum":  {'$regex': year}})
        infection_foreign_country_total_count = 0
        for hos in infection_foreign_country:
            if (hos['nakaza_v_zahranici'] == 1):
                infection_foreign_country_total_count += 1

                #Get rid of NAN values
                if pd.isna(hos['nakaza_zeme_csu_kod']):
                    continue

                if hos['nakaza_zeme_csu_kod'] in foreign_country_infection_dictionary:
                    foreign_country_infection_dictionary[hos['nakaza_zeme_csu_kod']] += 1
                else:
                    foreign_country_infection_dictionary[hos['nakaza_zeme_csu_kod']] = 1

        #Total count of infected - calculated according to records counts for each month
        infected_home_country_total_count = infected_db.count_documents(
            {"datum":  {'$regex': year}}) - infection_foreign_country_total_count

        infected_foreign_country_arr.append(
            infection_foreign_country_total_count)
        infected_home_country_arr.append(infected_home_country_total_count)
        year = year_clear

#Sorting dictonary and choosing top 10 countries
foreign_country_infection_dictionary_sorted = dict(sorted(
    foreign_country_infection_dictionary.items(), key=lambda x: x[1], reverse=True))
top_ten_foreign_counties = dict(
    list(foreign_country_infection_dictionary_sorted.items())[:10])


# ###################################################################################################################   PART 2   ###################################################################################################################
# UPV (UMELA PLICNI VENTILACE) CAPACITY
for month in range(12):
    #Date extracting
    year = '2020-'
    if month + 1 < 10:
        year += "0" + (str(month + 1))
    else:
        year += (str(month + 1))
    year_arr.append(year)

    upv_total_capacity_per_month = capacity_db.find(
        {"datum":  {'$regex': year}})
    upv_total_capacity_count = 0
    for upv in upv_total_capacity_per_month:
        upv_total_capacity_count += upv['upv_kapacita_celkem']
    upv_total_capacity_arr.append(upv_total_capacity_count)

    hospitalization_upv_per_month = hospitalization_db.find(
        {"datum":  {'$regex': year}})
    hospitalization_upv_total_count = 0
    for hos in hospitalization_upv_per_month:
        hospitalization_upv_total_count += hos['upv']
    upv_hospitalization_capacity_arr.append(hospitalization_upv_total_count)

countries = list(top_ten_foreign_counties.keys())
y_pos = np.arange(len(countries))
countries_value = list(top_ten_foreign_counties.values())
chart1 = {'zeme': countries, 'pocet nakazenych': countries_value}
df1 = pd.DataFrame(chart1, columns=['zeme', 'pocet nakazenych'])
chart2 = {'mesice': months, 'upv celkova kapacita': upv_total_capacity_arr,
          'upv hospitalizace': upv_hospitalization_capacity_arr}
df2 = pd.DataFrame(
    chart2, columns=['mesice', 'upv celkova kapacita', 'upv hospitalizace'])

#Export to CSV file
df1.to_csv('../csv/Top_10_cizich_zemi_nakazy.csv', encoding='UTF-16')
df2.to_csv('../csv/Pomer_mezi_vyuzitou_a_celkovou_kapacitou_upv.csv', encoding='UTF-16')
