#collapse trifecta chance to exacta chance.

import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'

path_to_file = path_to_directory + 'race_parameters' + '.txt'
RaceParameters = pd.read_csv(path_to_file)  
print(RaceParameters)

sDate = RaceParameters.at[0,'sDate']
sRace = str(RaceParameters.at[0,'sRace'])
firstRace = int(RaceParameters.at[0,'firstRace'])
lastRace = int(RaceParameters.at[0,'lastRace'])
sVenue = RaceParameters.at[0,'sVenue']

#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)
        
    path_to_file = path_to_directory + 'JockeyTierce_org' + sRace + '.csv'
    TierceChance = pd.read_csv(path_to_file)
    TierceChance_org = TierceChance.copy(deep=True)

    #drop a bunch of extra columns
    TierceChance.drop(['Jx','Jy', 'Jz','JNx','JNy','JNz'], axis=1, inplace=True)
    TierceChance.sort_values(['Race','Hx','Hy','Hz'],inplace=True)
    #print(TierceChance.head(15))
    #collapse and sum on race, x, y horse numbers.
    ExTceChance = TierceChance.groupby(['Race','Hx','Hy']).sum().reset_index()
    #print(ExTceChance.head(15))
    ExTceChance.drop(['Hz'],axis=1,inplace=True)
    ExTceChance.rename(columns={'Hx':'horseno_x','Hy':'horseno_y'},inplace=True)
    #print(ExTceChance.head(15))

    #now let's merge with forecast exacta chances and compute a factor for merging back into tierce.
    path_to_file = path_to_directory + 'fctChance' + sRace + '.csv'
    ExFctChance = pd.read_csv(path_to_file)
    #print(ExFctChance.head(15))

    ExactaChance = pd.merge(ExTceChance, ExFctChance, on=['Race','horseno_x','horseno_y'], how='inner')
    ExactaChance['ForecastFactor'] = ExactaChance['fctChance'] / ExactaChance['TierceCh']
    #print(ExactaChance.head(15))
    AllTotals = ExactaChance.sum(axis=0)
    print(AllTotals)

    ExactaChance.sort_values(['Race','horseno_x','horseno_y']).reset_index
    ExactaChance.rename(columns={'horseno_x':'Hx','horseno_y':'Hy'},inplace=True)
    print(ExactaChance.describe())
    #todo: deal with 999's ????
    ExactaChance.drop(columns=['TierceCh','fctpays','fctChance'],inplace=True)

    #merge with original jockey tierce and save
    JockeyTierceWithFactor = pd.merge(TierceChance_org,ExactaChance, on=['Race','Hx','Hy'], how='inner')
    JockeyTierceWithFactor['TierceCh_org'] = JockeyTierceWithFactor['TierceCh']
    JockeyTierceWithFactor['TierceCh'] = JockeyTierceWithFactor['TierceCh_org'] * JockeyTierceWithFactor['ForecastFactor']

    #print(JockeyTierceWithFactor.head(25))
    AllTotals = JockeyTierceWithFactor.sum(axis=0)
    print(AllTotals)
    #in the tierce grid.
    # New Tierce Chance(x,y,z) = ExFctChance(x,y) / ExTceCh(x,y)     * old TierceChance(x,y,z)
    # ExFctChance(x,y) / ExTceCh(x,y) is our factor ForecastFactor
    JockeyTierceWithFactor.to_csv(path_to_directory + 'JockeyTierce_new' + sRace + '.csv', index=False)
    JockeyTierceWithFactor.drop(columns=['TierceCh_org','ForecastFactor'],inplace=True)
    JockeyTierceWithFactor.to_csv(path_to_directory + 'JockeyTierce' + sRace + '.csv', index=False)
    print(JockeyTierceWithFactor.head(25))
    

#end Race


