import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#load data from csv
df1 = pd.read_csv('../csv/Pocty_nakazenych_JMR.csv', encoding='UTF-16')
df2 = pd.read_csv('../csv/Pocty_vylecenych_JMR.csv', encoding='UTF-16')
df3 = pd.read_csv('../csv/Pocty_umrti_JMR.csv', encoding='UTF-16')
df4 = pd.read_csv('../csv/Pocty_ockovani_JMR.csv', encoding='UTF-16')

months = ["leden", "únor", "březen", "duben", "květen", "červen",
          "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]

#Charts plotting
plt.style.use('seaborn')
fig, axs = plt.subplots(4, sharex=False, figsize=(20, 15))
fig.suptitle('Dotazy skupiny B\nJihomoravský kraj a covid', fontsize=20)
fig.text(0.06, 0.5, 'Počty na jednoho obyvatele kraje/republiky',
         va='center',  fontsize=18, rotation='vertical')

#Chart for Quater 1 - INFECTED
position = np.arange(len(months))
width = 0.2

axs[0].bar(position, df1['nakazeni_jmr'], width,
           label='Počty nakažených v JMR', color='plum', align='center')
axs[0].bar(position+width, df1['nakazeni_cz'], width,
           label='Počty nakažených v CZ', color='darkslategray', align='center')
axs[0].set_title('Nakažení', y=1.0, x=0.0)
axs[0].set_xticks(position)
axs[0].set_xticklabels(months)
axs[0].set_yscale('log', base=10)
axs[0].legend()

#Chart for Quater 2 - RECOVERY
axs[1].bar(position, df2['vyleceni_jmr'], width,
           label='Počty vyléčených v JMR', color='plum', align='center')
axs[1].bar(position+width, df2['vyleceni_cz'], width,
           label='Počty vyléčených v CZ', color='darkslategray', align='center')
axs[1].set_title('Vyléčení', y=1.0, x=0.0)
axs[1].set_xticks(position)
axs[1].set_xticklabels(months)
axs[1].set_yscale('log', base=10)
axs[1].legend()

#Chart for Quater 3 - DEATH
axs[2].bar(position, df3['umrti_jmr'], width,
           label='Počty zemřelých v JMR', color='plum', align='center')
axs[2].bar(position+width, df3['umrti_cz'], width,
           label='Počty zemřelých v CZ', color='darkslategray', align='center')
axs[2].set_title('Úmrtí', y=1.0, x=0.0)
axs[2].set_xticks(position)
axs[2].set_xticklabels(months)
axs[2].set_yscale('log', base=10)
axs[2].legend()

#Chart for Quater 4 - VACCINATION
axs[3].bar(position, df4['ockovani_jmr'], width,
           label='Počty očkovaných v JMR', color='plum', align='center')
axs[3].bar(position+width, df4['ockovani_cz'], width,
           label='Počty očkovaných v CZ', color='darkslategray', align='center')
axs[3].set_title('Očkovaní', y=1.0, x=0.0)
axs[3].set_xticks(position)
axs[3].set_xticklabels(months)
axs[3].set_yscale('log', base=10)
axs[3].legend()

plt.show()
fig.savefig('../dotazy-png/dotazB.png')
