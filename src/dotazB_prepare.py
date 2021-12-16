from pymongo import MongoClient
import pandas as pd

MONGO_USER = "user"
MONGO_PASSWD = "passwd"
MONGO_URI = "mongodb://{}:{}@localhost:10022/upa"
CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(CONNECTION_STRING)

#SOUTH MORAVIA REGION - JMR
jmr_region = 'CZ064'
jmr_habitants = 1195327
cz_habitants = 10702942 - jmr_habitants #CZ habitants without JMR habitants

months = ["leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen", "září", "říjen", "listopad", "prosinec" ]

#Databaze and Collection initialization
mydb = client["upa"]
infected_db = mydb['osoby']
recovery_db = mydb['vyleceni']
death_db = mydb['umrti']
vaccination_db = mydb['ockovani']

#Empty arrays for plotting data
jmr_infected_arr = []
jmr_recovery_arr = []
jmr_death_arr = []
jmr_vaccination_arr = []
cz_infected_arr = []
cz_recovery_arr = []
cz_death_arr = []
cz_vaccination_arr = []

for month in range(12): 
    #Date extracting
    year = '2021-'
    if month + 1 < 10:
        year += "0" + (str(month + 1))
    else:
        year += (str(month + 1))
    
    #INFECTED in JMR per one habitant and per month - calculated according to records counts for JMR region divided by JMR habitants
    jmr_infected = (infected_db.count_documents({"datum":  {'$regex': year}, "kraj_nuts_kod": {'$regex': jmr_region}}))/jmr_habitants
       
    #INFECTED in CZ per one habitant and per month - calculated according to records counts for all regions (minus infected people in JMR region) divided by CZ habitants (without JMR habitants)
    cz_infected = ((infected_db.count_documents({"datum":  {'$regex': year}}))-jmr_infected)/cz_habitants
    
    #RECOVERY in JMR per one habitant and per month 
    jmr_recovery = (recovery_db.count_documents({"datum":  {'$regex': year}, "kraj_nuts_kod": {'$regex': jmr_region}}))/jmr_habitants

    #RECOVERY in CZ per one habitant and per month 
    cz_recovery = ((recovery_db.count_documents({"datum":  {'$regex': year}}))-jmr_recovery)/cz_habitants

    #DEATH in JMR per one habitant and per month
    jmr_death = (death_db.count_documents({"datum":  {'$regex': year}, "kraj_nuts_kod": {'$regex': jmr_region}}))/jmr_habitants

    #DEATH in CZ per one habitant and per month
    cz_death = ((death_db.count_documents({"datum":  {'$regex': year}}))-jmr_death)/cz_habitants

    #VACCINATION in JMR  - sum of values in columns 'celkem_davek' only for JMR region divided by JMR habitants
    jmr_vaccination = vaccination_db.find({"datum":  {'$regex': year}, "kraj_nuts_kod": {'$regex': jmr_region}})
    jmr_vaccination_total_count = 0
    for o in jmr_vaccination:
        jmr_vaccination_total_count += o['celkem_davek']
    jmr_vaccination_total_count /= jmr_habitants

    #VACCINATION in CZ - sum of values in columns 'celkem_davek' for CZ (minus vaccination in JMR region) divided by CZ habitants (without JMR habitants)
    cz_vaccination = vaccination_db.find({"datum":  {'$regex': year}})
    cz_vaccination_total_count = 0
    for o in cz_vaccination:
        cz_vaccination_total_count += o['celkem_davek']
    cz_vaccination_total_count -= jmr_vaccination_total_count
    cz_vaccination_total_count /= cz_habitants
    
    jmr_infected_arr.append(jmr_infected)
    cz_infected_arr.append(cz_infected)
    jmr_recovery_arr.append(jmr_recovery)
    cz_recovery_arr.append(cz_recovery)
    jmr_death_arr.append(jmr_death)
    cz_death_arr.append(cz_death)
    jmr_vaccination_arr.append(jmr_vaccination_total_count)
    cz_vaccination_arr.append(cz_vaccination_total_count)
  
chart1 = {'mesice': months, 'nakazeni_jmr': jmr_infected_arr,
          'nakazeni_cz': cz_infected_arr}
df1 = pd.DataFrame(chart1, columns=['mesice', 'nakazeni_jmr', 'nakazeni_cz'])
chart2 = {'mesice': months, 'vyleceni_jmr': jmr_recovery_arr,
          'vyleceni_cz': cz_recovery_arr}
df2 = pd.DataFrame(chart2, columns=['mesice', 'vyleceni_jmr', 'vyleceni_cz'])
chart3 = {'mesice': months, 'umrti_jmr': jmr_death_arr,
          'umrti_cz': cz_death_arr}
df3 = pd.DataFrame(chart3, columns=['mesice', 'umrti_jmr', 'umrti_cz'])
chart4 = {'mesice': months, 'ockovani_jmr': jmr_vaccination_arr,
          'ockovani_cz': cz_vaccination_arr}
df4 = pd.DataFrame(chart4, columns=['mesice', 'ockovani_jmr', 'ockovani_cz'])


#Export to CSV file
df1.to_csv('../csv/Pocty_nakazenych_JMR.csv', encoding='UTF-16')
df2.to_csv('../csv/Pocty_vylecenych_JMR.csv', encoding='UTF-16')
df3.to_csv('../csv/Pocty_umrti_JMR.csv', encoding='UTF-16')
df4.to_csv('../csv/Pocty_ockovani_JMR.csv', encoding='UTF-16')
