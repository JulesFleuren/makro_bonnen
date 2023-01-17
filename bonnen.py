# TODO: Make it work for pdfs where the articles are split over multiple pages
# TODO: make it automatically recognize certain articles


from pdfminer.high_level import extract_text
import pandas as pd
import numpy as np
import time

# CONFIG
btw_codes = {"1":1.21, "5":1.09, "0":1}
btw_codes_percentage = {"1":21, "5":9, "0":0}

# make amount in cents into correct format for printing
def as_bedrag(amount):
    if len(str(amount)) > 2:
        return f"{str(amount)[:-2]},{str(amount)[-2:]}"
    if len(str(amount)) == 2:
        return f"0,{str(amount)}"
    if len(str(amount)) == 1:
        return f"0,0{str(amount)}"


filename = r"bon"
text = extract_text(f'{filename}.pdf')

lines = text.splitlines()


# find the line which contains the word "Artikelnummer"
start_line = [i for i, line in enumerate(lines) if 'Artikelnummer' in line][0]

# find the line which contains the word "Aantal stuks"
end_line = [i for i, line in enumerate(lines) if "Aantal stuks" in line][0]


# dataframe that will contain all articles and their information
articles_dtypes = np.dtype([('Statiegeld', bool), 
                            ('Artikelnummer', str), 
                            ('Artikelomschrijving', str),
                            ('Prijs st/kg', str),
                            ('Stuks per eenheid', str), 
                            ('Prijs per collo', str),
                            ('Aantal', str),
                            ('Bedrag', str),
                            ('BTW', str),
                            ('Code korting', str),
                            ('Prijs st/kg na korting', str)])
articles = pd.DataFrame(np.empty(0, dtype=articles_dtypes))


# go trough all lines containing articles and extract the information
for i, line in enumerate(lines[start_line+3:end_line]):
    if "----------------" in line:
        end_articles = i
        break

    if not line=="" and not "ARTIKELEN---" in line:
        split_line = line.split()[::-1]
        article = pd.DataFrame(np.empty(1, dtype=articles_dtypes))
        
        first_entry = split_line.pop()
        if first_entry == '+':
            article['Artikelnummer'] = split_line.pop()
            article['Statiegeld'] = True
        else:
            article['Artikelnummer'] = first_entry
            article['Statiegeld'] = False

        # find stuks per eenheid indicator
        for i, entry in enumerate(split_line):
            if len(entry) == 2 and entry.isupper():
                article['Stuks per eenheid'] = split_line[i+1]
                article['Prijs st/kg'] = split_line[i+2]
                article['Prijs per collo'] = split_line[i-1]
                article['Aantal'] = split_line[i-2]
                article['Bedrag'] = split_line[i-3]
                article['BTW'] = split_line[i-4]
                article['Artikelomschrijving'] = " ".join(split_line[:i+2:-1])

                split_line = split_line[:i-4]
                if split_line[0] == 'A':
                    split_line = split_line[1:]
                if len(split_line) == 2:
                    article['Code korting'] = split_line[1]
                    article['Prijs st/kg na korting'] = split_line[0]
                if len(split_line) == 1:
                    article['Code korting'] = ""
                    article['Prijs st/kg na korting'] = split_line[0]
                break
        
        # append article to articles
        articles = pd.concat([articles, article], ignore_index=True)

# dataframe that will contain all articles and their information
kortingen_dtypes = np.dtype([('Artikelomschrijving', str),
                            ('Bedrag', str),
                            ('BTW', str),
                            ('Code korting', str)])
kortingen = pd.DataFrame(np.empty(0, dtype=kortingen_dtypes))

# go trough all lines containing kortingen and extract the information
for i, line in enumerate(lines[start_line+end_articles+4:end_line]):
    if "----------------" in line:
        break

    if not line=="" and not "Totaal extra voordeel" in line:
        split_line = line.split()[::-1]
        korting = pd.DataFrame(np.empty(1, dtype=kortingen_dtypes))

        korting['Code korting'] = split_line.pop(0)
        korting['BTW'] = split_line.pop(0)
        korting['Bedrag'] = split_line.pop(0)
        korting['Artikelomschrijving'] = ' '.join(split_line[::-1])
        kortingen = pd.concat([kortingen, korting], ignore_index=True)

# find the line which contains the word "Netto totaal"
# netto_totaal_line = [i for i, line in enumerate(lines) if "Netto totaal" in line][0]
netto_totaal_line = end_line
netto_totaal = int(lines[netto_totaal_line].split()[-1].replace(',', ''))

# find the line which contains the word "Te betalen"
te_betalen_line = [i for i, line in enumerate(lines[end_line:]) if "Te betalen" in line][0] + end_line
te_betalen = int(lines[te_betalen_line].split()[-1].replace(',', ''))

# 'Bedrag (x100)' column is amount of money in cents represented as an integer, can be used to avoid rounding errors
# fill 'Bedrag (x100)' column
articles['Bedrag (x100)'] = np.zeros(len(articles), dtype=int)
for i, s in enumerate(articles['Bedrag']):
    bedrag = s.replace(',', '')

    if bedrag != '' and bedrag[-1] == "-":
        articles.loc[i, 'Bedrag (x100)'] = int("-" + bedrag[:-1])
    else:
        articles.loc[i, 'Bedrag (x100)'] = int(bedrag)

kortingen['Bedrag (x100)'] = np.zeros(len(kortingen), dtype=int)
for i, s in enumerate(kortingen['Bedrag']):
    bedrag = s.replace(',', '').replace("-", "")
    kortingen.loc[i, 'Bedrag (x100)'] = int(bedrag)

# # convert strings in these columns to int or float
# for column in ['Prijs st/kg', 'Stuks per eenheid', 'Prijs per collo', 'Aantal', 'Bedrag', 'BTW', 'Prijs st/kg na korting']:
#     for i, s in enumerate(articles[column]):
#         articles.loc[i, column] = s.replace(',', '.')

#     for i, price in enumerate(articles[column]):
#         if price != '' and price[-1] == "-":
#             articles.loc[i, column] = "-" + price[:-1]
#     articles[column] = pd.to_numeric(articles[column])

# for column in ['Bedrag', 'BTW']:
#     for i, s in enumerate(kortingen[column]):
#         kortingen.loc[i, column] = s.replace(',', '.').replace('-','')
        
#     kortingen[column] = pd.to_numeric(kortingen[column])


# subtract kortingen from articles
articles['Bedrag na korting (x100)'] = articles['Bedrag (x100)']
for i, korting in kortingen.iterrows():
    articles.loc[articles['Code korting'] == korting['Code korting'], 'Bedrag na korting (x100)'] -= korting['Bedrag (x100)']

articles['Bedrag na korting incl. BTW (x100)'] = articles['Bedrag na korting (x100)']
# add column with bedrag incl. BTW
for code in btw_codes:
    articles.loc[articles['BTW'] == code, 'Bedrag na korting incl. BTW (x100)'] = np.around((articles['Bedrag na korting (x100)']*btw_codes[code])).astype(int)

# check if the total amount of money netto is correct
if articles['Bedrag na korting (x100)'].sum() != netto_totaal:
    print("Error: total amount of money netto is not correct")
    print(f"Total amount of money should be {as_bedrag(netto_totaal)}, but is {as_bedrag(articles['Bedrag na korting (x100)'].sum())}")
    exit()

# check if the total amount of money including btw is correct
if articles['Bedrag na korting incl. BTW (x100)'].sum() != te_betalen:
    print("Warning: totaal bedrag incl. BTW klopt niet")
    print(f"Totaal bedrag volgens bon: {as_bedrag(te_betalen)}, totaal bedrag: {as_bedrag(articles['Bedrag na korting incl. BTW (x100)'].sum())}")
    print(f"verschil: {as_bedrag(articles['Bedrag na korting incl. BTW (x100)'].sum() - te_betalen)}")
    input("press enter to continue")

# add column with doel
articles['Groep'] = ''
for i, row in articles.iterrows():
    with_btw = str(row['Bedrag na korting incl. BTW (x100)'])
    without_btw = str(row['Bedrag na korting (x100)'])
    print(f"{row['Artikelomschrijving']:40}", end='')
    if row['Statiegeld']:
        print(" (statiegeld) ", end='')
    else:
        print(" "*14, end='')
    print(f"incl:{as_bedrag(with_btw):>8}\texcl:{as_bedrag(without_btw):>8}", end='')
    
    articles.loc[i, 'Groep'] = input(": ")


# print articles grouped by doel
# boekingen = pd.DataFrame(columns=['Grootboekrekening', 'Omschrijving', 'Bedrag'])
for groep in articles['Groep'].unique():
    print()
    print(f"groep {groep}")
    print(articles[articles['Groep'] == groep][['Artikelomschrijving', 'Stuks per eenheid', 'Aantal', 'Bedrag na korting incl. BTW (x100)']].to_string()) 
    total_amount_with_btw = articles[articles['Groep'] == groep]['Bedrag na korting incl. BTW (x100)'].sum()
    for code in btw_codes:
        if len(articles[(articles['Groep'] == groep) & (articles['BTW'] == code)]) > 0:
            total_amount_without_btw = articles[(articles['Groep'] == groep) & (articles['BTW'] == code)]['Bedrag na korting (x100)'].sum()
            print(f"Totaalbedrag excl btw code {code} ({btw_codes_percentage[code]}%):\t{as_bedrag(total_amount_without_btw)}")
    print(f"Totaalbedrag incl btw:\t\t\t{as_bedrag(total_amount_with_btw)}")
    # grootboekrekening = input("grootboekrekening: ")
    # omschrijving = input("Omschrijving: ")

    # boekingen = boekingen.append({'Grootboekrekening': grootboekrekening,
    #          'Bedrag': articles[articles['Groep'] == groep]['Bedrag na korting incl. BTW'].sum(),
    #          'Omschrijving': omschrijving}, ignore_index=True)
# print(boekingen.to_string())

print()
print(f"Totaal bedrag volgens bon: {as_bedrag(te_betalen)}, totaal bedrag: {as_bedrag(articles['Bedrag na korting incl. BTW (x100)'].sum())}")
print(f"verschil: {as_bedrag(articles['Bedrag na korting incl. BTW (x100)'].sum() - te_betalen)}")
