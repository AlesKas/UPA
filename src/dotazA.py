from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from os import getenv

MONGO_USER = getenv("MONGO_USERNAME")
MONGO_PASSWD = getenv("MONGO_PASSWORD")
MONGO_URI = getenv("MONGO_URI")
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
# ###################################################################################################################   PART 1   ###################################################################################################################
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
        
#print(infected_arr)
#print(recovery_arr)
#print(hospitalization_arr)
#print(tests_arr)

#Charts plotting
plt.style.use('seaborn')
fig, axs = plt.subplots(2, figsize=(15,10))

#Rotation on axis x
for ax in fig.axes:
    ax.tick_params(axis='x', labelrotation=45)
fig.suptitle('Dotazy skupiny A - část I.', fontsize=20)

#Chart for plotting infected, recoveries and hospitalization
chart1 = {'datum': datum_arr, 'pocet nakazenych': infected_arr, 'pocet vylecenych': recovery_arr, 'pocet hospitalizovanych': hospitalization_arr}
df1 = pd.DataFrame(chart1,columns=['datum','pocet nakazenych', 'pocet vylecenych', 'pocet hospitalizovanych'])
axs[0].plot(df1['datum'], df1['pocet nakazenych'],  marker='o', markerfacecolor='deepskyblue', label='Počty nakažených osob', color='lightskyblue')
axs[0].plot(df1['datum'], df1['pocet vylecenych'], marker='o', markerfacecolor='red', label='Počty vyléčených osob',  color='salmon', linewidth=3)
axs[0].plot(df1['datum'], df1['pocet hospitalizovanych'], marker='o', markerfacecolor='lime', label='Počty hospitalizovaných osob', color='springgreen', linestyle='dashed', linewidth=2)
axs[0].legend()

#Chart for tests (PCR and antigen)
chart2 = {'datum': datum_arr, 'pocet provedenych testu': tests_arr}
df2 = pd.DataFrame(chart2, columns=['datum','pocet provedenych testu'])
axs[1].plot(df2['datum'], df2['pocet provedenych testu'], marker='o', markerfacecolor='orchid', label='Počty provedených testů (PCR a antigenní)', color='fuchsia')
axs[1].set_yscale('symlog')
axs[1].legend()
plt.show()

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

#Chart plotting
fig2, axs2 = plt.subplots(3, sharex=False, sharey=True, figsize=(15,13))
for ax in fig2.axes:
    ax.tick_params(axis='x', labelright=50, labelsize = 8)
fig2.suptitle('Dotazy skupiny A - část II.', fontsize=20)

#Chart for total count of vaccination per region
width = 0.2
chart1 = {'kraje': regions_label, 'ockovani': vaccination_regions_arr}
df3 = pd.DataFrame(chart1,columns=['kraje','ockovani'])
axs2[0].bar(df3['kraje'], df3['ockovani'], width, label='Celkový počet očkování', color='indianred')
axs2[0].yaxis.get_major_formatter().set_scientific(False)
axs2[0].yaxis.get_major_formatter().set_useOffset(False)
axs2[0].legend()

#Chart for counts of vaccinated women or man per region
position = np.arange(len(regions))
chart2 = {'kraje': regions_label, 'ockovani_muzi': vaccination_male_arr, 'ockovani_zeny': vaccination_female_arr}
df4 = pd.DataFrame(chart2,columns=['kraje','ockovani_muzi', 'ockovani_zeny'])
axs2[1].bar(position, df4['ockovani_muzi'], width, label='Počty očkovaných mužů', color='aquamarine', align='center')
axs2[1].bar(position+width, df4['ockovani_zeny'], width, label='Počty očkovaných žen', color='orange', align='center')
axs2[1].yaxis.get_major_formatter().set_scientific(False)
axs2[1].yaxis.get_major_formatter().set_useOffset(False)
axs2[1].set_xticks(position)
axs2[1].set_xticklabels(regions_label)
axs2[1].legend()

#Chart for total count of vaccination per region
width2 = 0.2
chart3 = {'kraje': regions_label, 'ockovani_do_24': vaccination_0_24_arr, 'ockovani_24_59': vaccination_25_59_arr, 'ockovani_nad_59': vaccination_60_arr}
df5 = pd.DataFrame(chart3,columns=['kraje','ockovani_do_24', 'ockovani_24_59', 'ockovani_nad_59'])
axs2[2].bar(position-width2, df5['ockovani_do_24'], width2, label='Počty očkovaných do 24 let', color='lightcoral', align='center')
axs2[2].bar(position, df5['ockovani_24_59'], width2, label='Počty očkovaných mezi 25 - 59', color='gold', align='center')
axs2[2].bar(position+width2, df5['ockovani_nad_59'], width2, label='Počty očkovaných nad 60', color='springgreen', align='center')
axs2[2].yaxis.get_major_formatter().set_scientific(False)
axs2[2].yaxis.get_major_formatter().set_useOffset(False)
axs2[2].set_xticks(position)
axs2[2].set_xticklabels(regions_label)
axs2[2].legend()
plt.show()
