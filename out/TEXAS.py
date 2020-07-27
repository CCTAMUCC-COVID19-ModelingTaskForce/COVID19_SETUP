import os, sys
import csv
import json
import numpy as np
import re
from time import strptime
import subprocess
import pandas as pd

from collections import defaultdict
from datetime import datetime
import datetime
from .utils import store_data, stoi

# ------------------------------------------------------------------------
# Globals
counties = ['hale', 'marion', 'roberts', 'childress', 'sutton', 'martin', 'llano', 'victoria', 'callahan', 'archer', 'young', 'donley', 'stephens', 'washington', 'wichita', 'lamb', 'san_patricio', 'winkler', 'kimble', 'smith', 'presidio', 'armstrong', 'jasper', 'garza', 'deaf_smith', 'waller', 'jim_wells', 'gaines', 'hansford', 'harrison', 'hartley', 'floyd', 'wilson', 'uvalde', 'refugio', 'bell', 'nueces', 'dawson', 'mitchell', 'dallas', 'gray', 'hutchinson', 'collingsworth', 'hays', 'hood', 'wise', 'crane', 'hall', 'de_witt', 'burnet', 'mcculloch', 'rusk', 'howard', 'walker', 'cooke', 'concho', 'burleson', 'menard', 'sherman', 'glasscock', 'shackelford', 'pecos', 'fannin', 'anderson', 'henderson', 'titus', 'newton', 'potter', 'jim_hogg', 'la_salle', 'hill', 'freestone', 'jack', 'galveston', 'irion', 'knox', 'motley', 'jeff_davis', 'brazos', 'robertson', 'bexar', 'reeves', 'mason', 'lamar', 'lynn', 'brazoria', 'williamson', 'san_jacinto', 'matagorda', 'rockwall', 'ward', 'wood', 'comanche', 'gregg', 'coryell', 'cottle', 'van_zandt', 'caldwell', 'morris', 'mclennan', 'franklin', 'dallam', 'comal', 'terry', 'hopkins', 'kerr', 'san_saba', 'mills', 'tarrant', 'shelby', 'oldham', 'kenedy', 'medina', 'panola', 'jefferson', 'bee', 'terrell', 'liberty', 'el_paso', 'lampasas', 'atascosa', 'lee', 'angelina', 'milam', 'red_river', 'bowie', 'bastrop', 'rains', 'cochran', 'navarro', 'ochiltree', 'parmer', 'bandera', 'chambers', 'edwards', 'upshur', 'brooks', 'throckmorton', 'ector', 'real', 'montgomery', 'montague', 'foard', 'randall', 'gillespie', 'somervell', 'hardin', 'ellis', 'denton', 'culberson', 'brewster', 'blanco', 'hemphill', 'haskell', 'upton', 'mcmullen', 'nolan', 'dickens', 'kendall', 'val_verde', 'aransas', 'live_oak', 'goliad', 'hudspeth', 'borden', 'orange', 'trinity', 'duval', 'karnes', 'johnson', 'grayson', 'wheeler', 'castro', 'falls', 'lubbock', 'andrews', 'cass', 'jackson', 'reagan', 'sterling', 'swisher', 'san_augustine', 'wilbarger', 'zavala', 'coleman', 'hockley', 'kent', 'cameron', 'erath', 'lipscomb', 'calhoun', 'fort_bend', 'loving', 'zapata', 'king', 'guadalupe', 'delta', 'austin', 'hamilton', 'baylor', 'maverick', 'fayette', 'crosby', 'carson', 'taylor', 'collin', 'dimmit', 'cherokee', 'bailey', 'kaufman', 'lavaca', 'kinney', 'runnels', 'hunt', 'brown', 'moore', 'tom_green', 'grimes', 'leon', 'hardeman', 'scurry', 'houston', 'crockett', 'midland', 'eastland', 'sabine', 'tyler', 'nacogdoches', 'kleberg', 'schleicher', 'palo_pinto', 'harris', 'willacy', 'webb', 'starr', 'polk', 'clay', 'parker', 'bosque', 'fisher', 'camp', 'hidalgo', 'frio', 'wharton', 'jones', 'coke', 'yoakum', 'travis', 'gonzales', 'stonewall', 'colorado', 'limestone', 'madison', 'briscoe', ]
parserName = 'TEXAS'

# Cases, deaths, recoveries
# Population data by age group
FILE_POP = ""
LOC = "Texas A&M University - Corpus Christi"
start = "03-04"
year = "2020"
cols = ['time', 'cases', 'deaths', 'hospitalized', 'icu', 'recovered']

# ------------------------------------------------------------------------
# Functions

# ------------------------------------------------------------------------
# Main point of entry
def parse():
    # Access files
    dfCasesFile = "../COVID19_SETUP/out/texas_cases.csv"
    dfDeathsFile = "../COVID19_SETUP/out/texas_fatalities.csv"
    #dfRecoveredFile = "../COVID19_CoastalBend/coastalBend_caseCounts.csv.3"

    # Init output data
    regions = defaultdict(list)
    nrows = 0
    dates = []

    # Make empty counts data frame
    todays_date = datetime.datetime.now().date()
    index = pd.date_range(start = "03-04-2020", end = todays_date)
    df = pd.DataFrame(index = index, columns = cols)
    df = df.fillna(0) # with 0s rather than NaNs
    df['time'] = ["{}-{:02}-{:02}".format(i.year, i.month, i.day) for i in index]
    
    # Read cases data
    dfCases = pd.read_csv(dfCasesFile)
    dfCases['Name'] = dfCases['Name'].str.lower()
    dfCases.columns = [c.replace('Cases_', '2020-').replace('Cases', '2020-').lower() for c in dfCases.columns.to_list()]
    # Filter by counties
    dfCases = dfCases[dfCases['name'].isin(counties)]

    # Read fatalities data
    dfDeaths = pd.read_csv(dfDeathsFile)
    dfDeaths['Name'] = dfDeaths['Name'].str.lower()
    dfDeaths.columns = [c.replace('Fatalities_', '2020-').replace('Fatalities', '2020-').lower() for c in dfDeaths.columns.to_list()]
    # Filter by counties
    dfDeaths = dfDeaths[dfDeaths['name'].isin(counties)]

    # Populate table
    prevCase = 0
    prevDeath = 0
    for t in df['time']:
        try:
            prevCase = dfCases[t].sum()
            df.loc[df['time'] == t, 'cases'] = prevCase
        except:
            df.loc[df['time'] == t, 'cases'] = prevCase # Repeat
        
        try:
            prevDeath = dfDeaths[t].sum()
            df.loc[df['time'] == t, 'deaths'] = prevDeath
        except:
            df.loc[df['time'] == t, 'deaths'] = prevDeath # Repeat

    # Combine into table
    #for r in range(len(dates)):
    #    regions["CoastalBend"].append([dates[r], int(cases[r]), int(deaths[r]), None, None, int(recovered[r])])

    for t in df['time']:
        regions[parserName].append([t, int(df.loc[df['time'] == t, 'cases']),
                 int(df.loc[df['time'] == t, 'deaths']),
                 None,
                 None,
                 None,
                ])

    store_data(regions, parserName, cols)


if __name__ == '__main__':
    parse()

