
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