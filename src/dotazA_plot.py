import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#load data from csv
df1 = pd.read_csv('../csv/Pocty_nakazenych_vylecenych_hospitalizovanych.csv', encoding='UTF-16')
df2 = pd.read_csv('../csv/Pocty_provedenych_testu.csv', encoding='UTF-16')
df3 = pd.read_csv('../csv/Celkovy_pocet_ockovani_dle_kraju.csv', encoding='UTF-16')
df4 = pd.read_csv('../csv/Pocty_ockovani_dle_pohlavi_a_kraju.csv', encoding='UTF-16')
df5 = pd.read_csv('../csv/Pocty_ockovani_dle_veku_a_kraju.csv', encoding='UTF-16')

regions = ["Královéhradecký kraj", "Ústecký kraj", "Hlavní město Praha", "Pardubický kraj", "Kraj Vysočina", "Jihočeský kraj", "Moravskoslezský kraj",
           "Středočeský kraj", "Plzeňský kraj", "Jihomoravský kraj", "Zlínský kraj", "Karlovarský kraj", "Liberecký kraj", "Olomoucký kraj"]
regions_label = [label.replace(' ', '\n') for label in regions]

#part 1
#Charts plotting
plt.style.use('seaborn')
fig, axs = plt.subplots(2, figsize=(15, 10))

#Rotation on axis x
for ax in fig.axes:
    ax.tick_params(axis='x', labelrotation=45)
fig.suptitle('Dotazy skupiny A - část I.', fontsize=20)

#Chart for plotting infected, recoveries and hospitalization
axs[0].plot(df1['datum'], df1['pocet nakazenych'],  marker='o',
            markerfacecolor='deepskyblue', label='Počty nakažených osob', color='lightskyblue')
axs[0].plot(df1['datum'], df1['pocet vylecenych'], marker='o', markerfacecolor='red',
            label='Počty vyléčených osob',  color='salmon', linewidth=3)
axs[0].plot(df1['datum'], df1['pocet hospitalizovanych'], marker='o', markerfacecolor='lime',
            label='Počty hospitalizovaných osob', color='springgreen', linestyle='dashed', linewidth=2)
axs[0].legend()

#Chart for tests (PCR and antigen)
axs[1].plot(df2['datum'], df2['pocet provedenych testu'], marker='o', markerfacecolor='orchid',
            label='Počty provedených testů (PCR a antigenní)', color='fuchsia')
axs[1].set_yscale('symlog')
axs[1].legend()
plt.show()
fig.savefig('../dotazy-png/dotazA-1.png')


#part 2
#Chart plotting
fig2, axs2 = plt.subplots(3, sharex=False, sharey=True, figsize=(15, 13))
for ax in fig2.axes:
    ax.tick_params(axis='x', labelright=50, labelsize=8)
fig2.suptitle('Dotazy skupiny A - část II.', fontsize=20)

#Chart for total count of vaccination per region
width = 0.2
position = np.arange(len(regions))
axs2[0].bar(position, df3['ockovani'], width,
            label='Celkový počet očkování', color='indianred')
axs2[0].yaxis.get_major_formatter().set_scientific(False)
axs2[0].yaxis.get_major_formatter().set_useOffset(False)
axs2[0].set_xticks(position)
axs2[0].set_xticklabels(regions_label)
axs2[0].legend()

#Chart for counts of vaccinated women or man per region
axs2[1].bar(position, df4['ockovani_muzi'], width,
            label='Počty očkovaných mužů', color='aquamarine', align='center')
axs2[1].bar(position+width, df4['ockovani_zeny'], width,
            label='Počty očkovaných žen', color='orange', align='center')
axs2[1].yaxis.get_major_formatter().set_scientific(False)
axs2[1].yaxis.get_major_formatter().set_useOffset(False)
axs2[1].set_xticks(position)
axs2[1].set_xticklabels(regions_label)
axs2[1].legend()

#Chart for total count of vaccination per region
width2 = 0.2
axs2[2].bar(position-width2, df5['ockovani_do_24'], width2,
            label='Počty očkovaných do 24 let', color='lightcoral', align='center')
axs2[2].bar(position, df5['ockovani_24_59'], width2,
            label='Počty očkovaných mezi 25 - 59', color='gold', align='center')
axs2[2].bar(position+width2, df5['ockovani_nad_59'], width2,
            label='Počty očkovaných nad 60', color='springgreen', align='center')
axs2[2].yaxis.get_major_formatter().set_scientific(False)
axs2[2].yaxis.get_major_formatter().set_useOffset(False)
axs2[2].set_xticks(position)
axs2[2].set_xticklabels(regions_label)
axs2[2].legend()
plt.show()
fig2.savefig('../dotazy-png/dotazA-2.png')
