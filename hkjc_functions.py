
import pandas as pd
import os
import shutil

def read_race_parameters(path_to_file: str) :
    
    RaceParameters = pd.read_csv(path_to_file)  
    print(RaceParameters)

    sDate = RaceParameters.at[0,'sDate']
    firstRace = int(RaceParameters.at[0,'firstRace'])
    lastRace = int(RaceParameters.at[0,'lastRace'])
    sVenue = RaceParameters.at[0,'sVenue']
    jType = RaceParameters['ChallengeType'][0]

    """
    print(sDate)
    print(firstRace)
    print(lastRace)
    print(sVenue)
    print(jType)
    """
    return firstRace, lastRace, sDate, sVenue, jType


def renormalize_column(df: pd.DataFrame, sColumn: str, newColumn=''):
    AllTotals = df.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
    if len(newColumn) > 0:
        df[newColumn] = df[sColumn] / AllTotals[sColumn]
    else:
        df[sColumn] = df[sColumn] / AllTotals[sColumn]
    #print(df.head())
    
