from pymongo import MongoClient
import pandas as pd

MONGO_USER = "user"
MONGO_PASSWD = "passwd"
MONGO_URI = "mongodb://{}:{}@localhost:10022/upa"
CONNECTION_STRING = MONGO_URI.format(MONGO_USER, MONGO_PASSWD)

client = MongoClient(CONNECTION_STRING)

#Databaze and Collection initialization
mydb = client["upa"]
infected_db = mydb['osoby']
recovery_db = mydb['vyleceni']
hospitalization_db = mydb['hospitalizace']
tests_db = mydb['testy-pcr-antigenni']
vaccination_db = mydb['ockovani']
vaccination_overall_view_db = mydb['ockovani-zakladni-prehled']

regions = ["Královéhradecký kraj", "Ústecký kraj", "Hlavní město Praha", "Pardubický kraj", "Kraj Vysočina", "Jihočeský kraj", "Moravskoslezský kraj", "Středočeský kraj", "Plzeňský kraj", "Jihomoravský kraj", "Zlínský kraj", "Karlovarský kraj", "Liberecký kraj", "Olomoucký kraj"]
regions_label = [label.replace(' ', '\n') for label in regions]

#Empty arrays for plotting data
datum_arr = []
infected_arr = []
recovery_arr = []
hospitalization_arr = []
tests_arr = []
vaccination_regions_arr = []
vaccination_female_arr = []
vaccination_male_arr = []
vaccination_0_24_arr = []
vaccination_25_59_arr = []
vaccination_60_arr = []

years = ["2020-", "2021-"]
####################################################################################################################   PART 1   ###################################################################################################################
for year in years:
    year_clear = year

    for month in range(12): 
        if month + 1 < 10:
            year += "0" + (str(month + 1))
        else:
            year += (str(month + 1))

        #Total count of infected and recoveries - calculated according to records counts for each month
        infected_total_count = infected_db.count_documents({"datum":  {'$regex': year}})
        recovery_total_count = recovery_db.count_documents({"datum":  {'$regex': year}})
        
        #Total count of hospitalization - sum of values in column pacient_prvni_zaznam for each month
        hospitalization_per_month = hospitalization_db.find({"datum":  {'$regex': year}})
        hospitalization_total_count = 0
        for hos in hospitalization_per_month:
            hospitalization_total_count += hos['pacient_prvni_zaznam']
  
        #Total count of performed test - sum of values in columns pocet_PCR_testy and pocet_AG_testy for each month
        test_per_month = tests_db.find({"datum":  {'$regex': year}})
        test_total_count = 0
        for test in test_per_month:
            test_total_count += test['pocet_PCR_testy'] + test['pocet_AG_testy']

        datum_arr.append(year)
        infected_arr.append(infected_total_count)
        recovery_arr.append(recovery_total_count)
        hospitalization_arr.append(hospitalization_total_count)
        tests_arr.append(test_total_count)
        year = year_clear

chart1 = {'datum': datum_arr, 'pocet nakazenych': infected_arr,
          'pocet vylecenych': recovery_arr, 'pocet hospitalizovanych': hospitalization_arr}
df1 = pd.DataFrame(chart1, columns=[
                   'datum', 'pocet nakazenych', 'pocet vylecenych', 'pocet hospitalizovanych'])
chart2 = {'datum': datum_arr, 'pocet provedenych testu': tests_arr}
df2 = pd.DataFrame(chart2, columns=['datum', 'pocet provedenych testu'])

#export to csv
df1.to_csv('../csv/Pocty_nakazenych_vylecenych_hospitalizovanych.csv', encoding='UTF-16')
df2.to_csv('../csv/Pocty_provedenych_testu.csv', encoding='UTF-16')

# ###################################################################################################################   PART 2   ###################################################################################################################
for one_region in regions:
    #Total count of vaccination per region - sum of values in columns 'celkem_davek' per region
    vaccination_per_region = vaccination_db.find({"kraj_nazev":  {'$regex': one_region}})
    vaccination_per_region_total_count = 0
    for o in vaccination_per_region:
        vaccination_per_region_total_count += o['celkem_davek']
   
    #Vacination according to sex gender and age
    vaccination_per_region_from_overall_view = vaccination_overall_view_db.find({"kraj_nazev":  {'$regex': one_region}})
    vaccination_per_woman_total_count = 0
    vaccination_per_man_total_count = 0
    vaccination_0_24_counter = 0
    vaccination_25_59_counter = 0
    vaccination_60_counter = 0

    #Age calculation - sum of values in columns 'pocet_davek' per region
    for vac in vaccination_per_region_from_overall_view:
        age_group = vac['vekova_skupina'].split("-")
        if (len(age_group) == 2):
            if (int(age_group[1]) <= 24):
                vaccination_0_24_counter += vac['pocet_davek']
            elif (int(age_group[1]) <= 59):
                vaccination_25_59_counter += vac['pocet_davek']
            else:
                vaccination_60_counter += vac['pocet_davek']
        else:
            vaccination_60_counter += vac['pocet_davek']

        #Sex gender calculation - sum of values in columns 'pocet_davek' per region
        if(vac['pohlavi'] == "M"):
            vaccination_per_man_total_count += vac['pocet_davek']
        else:
            vaccination_per_woman_total_count += vac['pocet_davek']
    
    vaccination_regions_arr.append(vaccination_per_region_total_count)
    vaccination_male_arr.append(vaccination_per_man_total_count)
    vaccination_female_arr.append(vaccination_per_woman_total_count)
    vaccination_0_24_arr.append(vaccination_0_24_counter)
    vaccination_25_59_arr.append(vaccination_25_59_counter)
    vaccination_60_arr.append(vaccination_60_counter)


chart3 = {'kraje': regions, 'ockovani': vaccination_regions_arr}
chart4 = {'kraje': regions, 'ockovani_muzi': vaccination_male_arr,
          'ockovani_zeny': vaccination_female_arr}
chart5 = {'kraje': regions, 'ockovani_do_24': vaccination_0_24_arr,
          'ockovani_24_59': vaccination_25_59_arr, 'ockovani_nad_59': vaccination_60_arr}

df3 = pd.DataFrame(chart3, columns=['kraje', 'ockovani'])
df4 = pd.DataFrame(chart4, columns=['kraje', 'ockovani_muzi', 'ockovani_zeny'])
df5 = pd.DataFrame(chart5, columns=['kraje', 'ockovani_do_24', 'ockovani_24_59', 'ockovani_nad_59'])

#Export to CSV file
df3.to_csv('../csv/Celkovy_pocet_ockovani_dle_kraju.csv', encoding='UTF-16')
df4.to_csv('../csv/Pocty_ockovani_dle_pohlavi_a_kraju.csv', encoding='UTF-16')
df5.to_csv('../csv/Pocty_ockovani_dle_veku_a_kraju.csv', encoding='UTF-16')
