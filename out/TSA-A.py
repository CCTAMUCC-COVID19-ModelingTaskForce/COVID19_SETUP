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
counties = ['sherman', 'roberts', 'ochiltree', 'childress', 'parmer', 'carson', 'potter', 'donley', 'randall', 'moore', 'armstrong', 'hemphill', 'deaf_smith', 'dallam', 'wheeler', 'hansford', 'hartley', 'gray', 'hutchinson', 'oldham', 'collingsworth', 'hall', 'swisher', 'briscoe', 'lipscomb', ]
parserName = 'TSA-A'

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

