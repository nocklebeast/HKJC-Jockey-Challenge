#collapse trifecta chance to exacta chance.
#and this script may end up doing quite a bit... could break things up later.
#
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

sType = 'jkc'
sThing = 'Jockey'
tType = 'tnc'
#jockey-tierce has the trainer info in it (from hkjc_process_tierce_investments)
"""
if sType == 'jkc':
    sThing = 'Jockey'
else:
    sThing = 'Trainer'
"""

#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)
        
    path_to_file = path_to_directory + 'JockeyTierce_org' + sRace + '.csv'
    TierceChance = pd.read_csv(path_to_file)
    TierceChance_org = TierceChance.copy(deep=True)
    #print(TierceChance.head(2))

    #drop a bunch of extra columns
    #TierceChance.drop(['Jx','Jy', 'Jz','JNx','JNy','JNz'], axis=1, inplace=True)
    TierceChance.drop([sType+'No_x', sType+'No_y',sType+'No_z'], axis=1, inplace=True)
    TierceChance.drop([tType+'No_x', tType+'No_y',tType+'No_z'], axis=1, inplace=True)
    TierceChance.drop([sType+'Nx', sType+'Ny',sType+'Nz'], axis=1, inplace=True)
    TierceChance.drop([tType+'Nx', tType+'Ny',tType+'Nz'], axis=1, inplace=True)
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
    #print(AllTotals)

    ExactaChance.sort_values(['Race','horseno_x','horseno_y']).reset_index
    ExactaChance.rename(columns={'horseno_x':'Hx','horseno_y':'Hy'},inplace=True)
    print(ExactaChance.describe())
    #todo: deal with 999's ????
    ExactaChance.drop(columns=['TierceCh','fctpays','fctChance'],inplace=True)

    #merge with original jockey tierce and save
    JockeyTierceWithFactor = pd.merge(TierceChance_org,ExactaChance, on=['Race','Hx','Hy'], how='inner')
    JockeyTierceWithFactor['TierceCh_org'] = JockeyTierceWithFactor['TierceCh']
    JockeyTierceWithFactor['TierceCh'] = JockeyTierceWithFactor['TierceCh_org'] * JockeyTierceWithFactor['ForecastFactor']
    JockeyTierceWithFactor.to_csv(path_to_directory + sThing+'Tierce_fct' + sRace + '.csv', index=False)
    #in the tierce grid.
    # New Tierce Chance(x,y,z) = ExFctChance(x,y) / ExTceCh(x,y)     * old TierceChance(x,y,z)
    # ExFctChance(x,y) / ExTceCh(x,y) is our factor ForecastFactor
    #AllTotals = JockeyTierceWithFactor.sum(axis=0)
    #print(AllTotals)
    
    #now let's create a Exacta quinella chance, then we'll merge in the 
    # quinella chance and then create a quinella factor so that our tierce chances
    # take up the same space as the quinella grid... the most liquid (and probably predictive)
    # HK betting market.
        
    #read fct chance, swap x and y and merge and then add Exy + Eyx to get the exacta
    # implied quinella chance.
    path_to_file = path_to_directory + 'fct' + 'Chance' + sRace + '.csv'
    xyExChance = pd.read_csv(path_to_file)
    xyExChance.rename(columns={'fctChance':'fctChance_x'},inplace=True)
    yxExChance = xyExChance.copy(deep=True)
    xyExChance.rename(columns={'fctChance_x':'fctChance_y'},inplace=True)
    xyExChance.rename(columns={'horseno_x':'Hx'},inplace=True)
    xyExChance.rename(columns={'horseno_y':'Hy'},inplace=True)

    #swap x and y for yx dataframe.
    yxExChance.rename(columns={'horseno_x':'Hy'},inplace=True)
    yxExChance.rename(columns={'horseno_y':'Hx'},inplace=True)

    FctQChance = pd.merge(xyExChance,yxExChance,on=['Race','Hx','Hy'], how='inner')
    #add xy and yx exactas (fct)
    FctQChance['FctQChance'] = ( FctQChance['fctChance_x'] + FctQChance['fctChance_y'] ) / 2
    FctQChance.drop(columns=['fctpays_x','fctpays_y'], inplace=True)
    #print(FctQChance.head())
    #renormalize???? we're good.
    #AllTotals = FctQChance.sum(axis=0)
    #print(AllTotals)

    path_to_file = path_to_directory + 'Ex' + 'qin' + 'Chance' + sRace + '.csv'
    ExQChance = pd.read_csv(path_to_file)
    ExQChance.drop(columns=['qinpays'],inplace=True)
    ExQChance.rename(columns={'horseno_x':'Hx','horseno_y':'Hy'},inplace=True)
    #AllTotals = ExQChance.sum(axis=0)
    #print(AllTotals)
    
    #merge the quinella and the exacta chances (both are normalized to one)
    ExFctQChance = pd.merge(FctQChance,ExQChance,on=['Race','Hx','Hy'], how='inner')

    #quinella factor weighs Q chance over Fct q-implied chance.... so that space in the exacta grid 
    # occupies the same probability space as in the quinella grid.
    ExFctQChance['QuinellaFactor'] = ExFctQChance['qinChance'] / ExFctQChance['FctQChance']
    ExFctQChance.drop(columns=['fctChance_y', 'fctChance_x','FctQChance','qinChance'],inplace=True)
    #print(ExFctQChance.head())
    #print(ExFctQChance.describe())

    #merge in this new factor to JockeyTierceWithFactor and save
    JockeyTierceWithFactorNew = pd.merge(JockeyTierceWithFactor,ExFctQChance, on=['Race','Hx','Hy'], how='inner')
    JockeyTierceWithFactorNew['Factor'] = JockeyTierceWithFactorNew['ForecastFactor'] * JockeyTierceWithFactorNew['QuinellaFactor'] 
    print(JockeyTierceWithFactorNew.head())
    print(JockeyTierceWithFactorNew.describe())
    
    #alter the tierce chance once more and save.
    JockeyTierceWithFactorNew['TierceCh_fctFactor'] = JockeyTierceWithFactorNew['TierceCh']
    JockeyTierceWithFactorNew['TierceCh'] = JockeyTierceWithFactorNew['TierceCh_fctFactor'] * JockeyTierceWithFactorNew['QuinellaFactor']

    #save this latest augmented tierce chance dataframe.
    JockeyTierceWithFactorNew.to_csv(path_to_directory + sThing+'Tierce_new_new' + sRace + '.csv', index=False)
    print(JockeyTierceWithFactorNew.head())
    print(JockeyTierceWithFactorNew.describe())
    AllTotals = JockeyTierceWithFactorNew.sum(axis=0)
    print(AllTotals)
    
    ### todo need to drop some columns. ##########################################################
    #drop some columns. and save for the jockey challenge.
    JockeyTierceWithFactorNew.drop(columns=['ForecastFactor','TierceCh_org','QuinellaFactor','Factor','TierceCh_fctFactor'],inplace=True)
    JockeyTierceWithFactorNew.to_csv(path_to_directory + sThing+'Tierce' + sRace + '.csv', index=False)

#end Race


