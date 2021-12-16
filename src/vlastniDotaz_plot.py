import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#load data from csv
df1 = pd.read_csv('../csv/Top_10_cizich_zemi_nakazy.csv', encoding='UTF-16')
df2 = pd.read_csv('../csv/Pomer_mezi_vyuzitou_a_celkovou_kapacitou_upv.csv', encoding='UTF-16')

#Charts plotting
plt.style.use('seaborn')
fig, axs = plt.subplots(2, figsize=(15, 12))
y_pos = np.arange(len(df1['zeme']))
axs[0].barh(y_pos, df1['pocet nakazenych'], align='center', color='darkblue')
axs[0].set_yticks(y_pos)
axs[0].set_yticklabels(df1['zeme'])
axs[0].invert_yaxis()
axs[0].set_xlabel('Počet nakažených')
axs[0].set_title('TOP 10 zemí, kde se obyvatelé ČR nakazili', fontsize=20)

width = 0.2
position = np.arange(len(df2['mesice']))
axs[1].bar(position, df2['upv hospitalizace'], width,
           label='Obsazenost umělé plicní ventilaci',  color='deepskyblue', align='center')
axs[1].bar(position+width, df2['upv celkova kapacita'], width,
           label='Celková kapacita umělé plicní ventilace', color='salmon', align='center')
axs[1].set_title(
    'Poměr mezi využitou a celkovou kapacitou umělé plicní ventilace', fontsize=20)
axs[1].yaxis.get_major_formatter().set_scientific(False)
axs[1].yaxis.get_major_formatter().set_useOffset(False)
axs[1].set_xticks(position)
axs[1].set_xticklabels(df2['mesice'])
axs[1].legend()

plt.show()
fig.savefig('../dotazy-png/vlastni-dotaz.png')
