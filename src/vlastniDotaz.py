from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

MONGO_USER = "user"
MONGO_PASSWD = "passwd"
MONGO_URI = "mongodb://{}:{}@localhost:10022/upa"
CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(CONNECTION_STRING)

#Databaze and Collection initialization
mydb = client["upa"]
infected_db = mydb['osoby']
death_db = mydb['umrti']
death_vaccination_db = mydb['ockovani-umrti']

months = ["leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen", "září", "říjen", "listopad", "prosinec" ]

#Empty arrays for plotting data
datum_arr = []
infected_home_country_arr = []
infected_foreign_country_arr = []
death_covid_arr = []
death_vaccination_arr = []
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
        infection_foreign_country = infected_db.find({"datum":  {'$regex': year}})
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
        infected_home_country_total_count = infected_db.count_documents({"datum":  {'$regex': year}}) - infection_foreign_country_total_count

        datum_arr.append(year)
        infected_foreign_country_arr.append(infection_foreign_country_total_count)
        infected_home_country_arr.append(infected_home_country_total_count)
        year = year_clear

#Sorting dictonary and choosing top 10 countries
foreign_country_infection_dictionary_sorted = dict(sorted(foreign_country_infection_dictionary.items(), key=lambda x: x[1], reverse=True))
top_ten_foreign_counties = dict(list(foreign_country_infection_dictionary_sorted.items())[:10])


# ###################################################################################################################   PART 2   ###################################################################################################################
# DEATH ON COVID vs DEATH after vaccination
for month in range(12): 
    #Date extracting
    year = '2021-'
    if month + 1 < 10:
        year += "0" + (str(month + 1))
    else:
        year += (str(month + 1))

    #Death on covid  - calculated according to records counts per month 
    death_covid_total_count = death_db.count_documents({"datum":  {'$regex': year}})    

    #Death on vaccination  - calculated according to records counts per month 
    death_vaccination = death_vaccination_db.find({"datum":  {'$regex': year}}) 
    death_vaccination_total_count = 0
    for o in death_vaccination:
        death_vaccination_total_count += o['zemreli_dokoncene_ockovani']

    death_covid_arr.append(death_covid_total_count)
    death_vaccination_arr.append(death_vaccination_total_count)

#Charts plotting
plt.style.use('seaborn')
fig, axs = plt.subplots(2, figsize=(15,12))

countries = list(top_ten_foreign_counties.keys())
y_pos = np.arange(len(countries))
countries_value = list(top_ten_foreign_counties.values())

axs[0].barh(y_pos, countries_value, align='center', color='darkblue')
axs[0].set_yticks(y_pos)
axs[0].set_yticklabels(countries)
axs[0].invert_yaxis()
axs[0].set_xlabel('Počet nakažených')
axs[0].set_title('TOP 10 zemí, kde se obyvatelé ČR nakazili', fontsize=20)

chart2 = {'mesice': months, 'umrti covid': death_covid_arr, 'umrti ockovani': death_vaccination_arr}
df2 = pd.DataFrame(chart2,columns=['mesice','umrti covid', 'umrti ockovani'])
axs[1].plot(df2['mesice'], df2['umrti covid'],  marker='o', markerfacecolor='darkolivegreen', label='Počty úmrtí na covid', color='olive')
axs[1].plot(df2['mesice'], df2['umrti ockovani'], marker='o', markerfacecolor='darkred', label='Počty úmrtí na očkování',  color='maroon', linewidth=3)
axs[1].set_title('Poměr počtú úmrtí na covid a na očkování', fontsize=20)
axs[1].legend()

plt.show()
plt.savefig('vlastni-dotaz.png')
