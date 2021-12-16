# Ukládání a příprava dat COVID - 19

## Autoři
- xkrizo03 Hana Křížová  
- xkaspa48 Aleš Kašpárek
- xjahod06 Vojtěch Jahoda 

## požadavky pro spuštění
 - docker 3.7
 - 64-bit OS
 - Mongo

## Spuštění
1. otevření kořenového adresáře
2. spuštění příkazu `sudo docker-compose up --build`
3. připojení do databáze pomocí `mongo mongodb://user:passwd@localhost:10022/upa`

### stáhnutí dat do databáze a inicializace
data jsou stáhnuta pomocí scriptu `main.py` a veškeré závislosti obsaženy v souboru `requirements.txt`, tato část lze provést pomocí scriptu `feed_db.sh`. který provede sérii příkazů:
```
pip3 install -r requirements.txt
cd src/
python3 ./main.py
cd ..
```

### extrakce dat z DB do csv souboru
extrakce je provedena ve scriptech
`dotazA-prepare.py` pro dotazy A
`dotazB-prepare.py` pro dotaz B
`vlastniDotaz-prepare.py` pro dotaz C
`dotazC.py` pro dotaz typu C spolu s extrakci dat pro dolovani

veškeré csv soubory jsou následně uloženy do složky `csv`

celkově lze tato extrakce provést pomocí příkazu `extract_data.sh`, který provede sérii příkazů:

```
cd src/
python3 dotazA_prepare.py
python3 dotazB_prepare.py
python3 dotazC_prepare.py
python3 vlastniDotaz_prepare.py
cd ..
```

### vykreslení grafů
grafy jsou vykreslovány do složky `dotazy-png` a vytvářejí je scripty:
`dotazA-plot.py` pro dotazy A
`dotazB-plot.py` pro dotaz B
`vlastniDotaz-plot.py` pro dotaz C

celkově lze grafy vykreslit pomocí příkazu `plot_queries.sh`, který provede sérii příkazů:

```
cd src/
python3 dotazA_plot.py
python3 dotazB_plot.py
python3 vlastniDotaz_plot.py
cd ..
```

více informací o fungování dotazů v `doc.pdf`
informace o csv souborech v `popis_struktury_csv.pdf` 
