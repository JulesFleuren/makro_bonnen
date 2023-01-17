# makro bonnen
## installatie
Installeer Python en de libraries in requirements.txt

## gebruik

1.  Verander de variabele `filename` naar de naam van de bon die je uit wil splitsen (zonder .pdf)
2.  Run het script
3.  Vul per product in onder welke groep je het wil laten vallen. Dit kan tekst of bijvoorbeeld een nummer zijn
4.  Het programma print per groep de producten uit met daaronder de totaal inclusief en exlusief btw.

Als je de bedragen inclusief BTW gebruikt: het kan gebeuren dat het totaal inclusief BTW niet overeen komt met het totaal te betalen op de bon. Dit heeft te maken met het feit dat makro pas aan het eind de BTW berekend en het scriptje het per artikel doet. Het programma zal dan het verschil printen, je kan dit verschil gewoon van één of meerder groepen aftrekken.

Voorbeeld:

    Warning: totaal bedrag incl. BTW klopt niet
    Totaal bedrag volgens bon: 272,58, totaal bedrag: 272,60
    verschil: 0,02
    press enter to continue
    ARO KEUKENROL 3PLY                                    incl:    5,63     excl:    4,65: 1
    APPEL JONAGOLD 1.5KG                                  incl:   12,26     excl:   11,25: 2
    BANAAN P/KG                                           incl:    2,75     excl:    2,52: 2
    BANAAN P/KG                                           incl:    2,79     excl:    2,56: 2
    BANAAN P/KG                                           incl:    3,48     excl:    3,19: 2
    SINAASAPPEL HAND 2KG BOLLO VV                         incl:    4,63     excl:    4,25: 2
    APPEL ELSTAR 65/75 1.5KG                              incl:    5,65     excl:    5,18: 2
    UNOX CAS TOMAAT 21X175ML                              incl:    8,16     excl:    7,49: 3
    UNOX CAS CHAMPIGNON 21X175ML                          incl:    8,16     excl:    7,49: 3
    MALT SINGLE 25X37G                                    incl:   14,49     excl:   13,29: 3
    MARS 24X51G                                           incl:   12,85     excl:   11,79: 3
    BRAN PILSENER KRAT 24X0.3L                            incl:   27,93     excl:   23,08: 4
    MBS STATIEGELD E 3.90                    (statiegeld) incl:    7,80     excl:    7,80: 4
    BIERBOX BELGIE 5X25CL                                 incl:   14,51     excl:   11,99: 5
    MBS STATIEGELD E 0.50                    (statiegeld) incl:    0,50     excl:    0,50: 5
    RIOB GRN LEMON FT ENV 100X2G                          incl:    6,52     excl:    5,98: 6
    RIOB EARL GR FT ENV 100X2G                            incl:    6,52     excl:    5,98: 6
    RIOB ROOIBOS FT ENV 100X1.5G                          incl:    9,35     excl:    8,58: 6
    DE ROOD VAC SNELF 500G                                incl:   82,67     excl:   75,84: 7
    ARO ORANGE JUICE 1.5L                                 incl:    8,45     excl:    7,75: 2
    ARO APPLE JUICE 1.5L                                  incl:    6,49     excl:    5,95: 2
    ARO VUILNISZAK 2X25X120LSTERK                         incl:   10,03     excl:    8,29: 1
    SORB SCHUURSPONZEN                                    incl:    4,71     excl:    3,89: 1
    ARO HUISH HANDSCHOEN L 3 PAAR                         incl:    1,44     excl:    1,19: 1
    ARO 12PCS LR03 AAA ALKALINE                           incl:    4,83     excl:    3,99: 1

    groep 1
                  Artikelomschrijving Stuks per eenheid Aantal  Bedrag na korting incl. BTW (x100)
    0              ARO KEUKENROL 3PLY                 1      1                                 563
    21  ARO VUILNISZAK 2X25X120LSTERK                 1      1                                1003
    22             SORB SCHUURSPONZEN                20      1                                 471
    23  ARO HUISH HANDSCHOEN L 3 PAAR                 1      1                                 144
    24    ARO 12PCS LR03 AAA ALKALINE                 1      1                                 483
    Totaalbedrag excl btw code 1 (21%):     22,01
    Totaalbedrag incl btw:                  26,64

    groep 2
                  Artikelomschrijving Stuks per eenheid Aantal  Bedrag na korting incl. BTW (x100)
    1            APPEL JONAGOLD 1.5KG                 1      5                                1226
    2                     BANAAN P/KG             1,864      1                                 275
    3                     BANAAN P/KG             1,894      1                                 279
    4                     BANAAN P/KG             2,364      1                                 348
    5   SINAASAPPEL HAND 2KG BOLLO VV                 1      1                                 463
    6        APPEL ELSTAR 65/75 1.5KG                 1      2                                 565
    19          ARO ORANGE JUICE 1.5L                 1      5                                 845
    20           ARO APPLE JUICE 1.5L                 1      5                                 649
    Totaalbedrag excl btw code 5 (9%):      42,65
    Totaalbedrag incl btw:                  46,50

    groep 3
                 Artikelomschrijving Stuks per eenheid Aantal  Bedrag na korting incl. BTW (x100)
    7       UNOX CAS TOMAAT 21X175ML                 1      1                                 816
    8   UNOX CAS CHAMPIGNON 21X175ML                 1      1                                 816
    9             MALT SINGLE 25X37G                25      1                                1449
    10                   MARS 24X51G                 1      1                                1285
    Totaalbedrag excl btw code 5 (9%):      40,06
    Totaalbedrag incl btw:                  43,66

    groep 4
               Artikelomschrijving Stuks per eenheid Aantal  Bedrag na korting incl. BTW (x100)
    11  BRAN PILSENER KRAT 24X0.3L                24      2                                2793
    12       MBS STATIEGELD E 3.90                 1      2                                 780
    Totaalbedrag excl btw code 1 (21%):     23,08
    Totaalbedrag excl btw code 0 (0%):      7,80
    Totaalbedrag incl btw:                  35,73

    groep 5
          Artikelomschrijving Stuks per eenheid Aantal  Bedrag na korting incl. BTW (x100)
    13  BIERBOX BELGIE 5X25CL                 1      1                                1451
    14  MBS STATIEGELD E 0.50                 1      1                                  50
    Totaalbedrag excl btw code 1 (21%):     11,99
    Totaalbedrag excl btw code 0 (0%):      0,50
    Totaalbedrag incl btw:                  15,01

    groep 6
                 Artikelomschrijving Stuks per eenheid Aantal  Bedrag na korting incl. BTW (x100)
    15  RIOB GRN LEMON FT ENV 100X2G                 1      2                                 652
    16    RIOB EARL GR FT ENV 100X2G                 1      2                                 652
    17  RIOB ROOIBOS FT ENV 100X1.5G                 1      2                                 935
    Totaalbedrag excl btw code 5 (9%):      20,54
    Totaalbedrag incl btw:                  22,39

    groep 7
           Artikelomschrijving Stuks per eenheid Aantal  Bedrag na korting incl. BTW (x100)
    18  DE ROOD VAC SNELF 500G                 6      2                                8267
    Totaalbedrag excl btw code 5 (9%):      75,84
    Totaalbedrag incl btw:                  82,67

    Totaal bedrag volgens bon: 272,58, totaal bedrag: 272,60
    verschil: 0,02

Je ziet hier dat het verschil tussen het programma en de bon €0,02 is. Je kan nu bij twee willekeurige posten één cent minder invullen.
