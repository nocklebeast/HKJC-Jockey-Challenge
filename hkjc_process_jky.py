#process jockey odds info from jockey challenge

from calendar import isleap
import pandas as pd
import numpy as np
import os
import json

pd.set_option('display.max_rows',None)

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'

#print(path_to_directory)
path_to_file = path_to_directory + 'jkc.txt' 
#print(path_to_file)

with open(path_to_file,mode='r', encoding='utf-8') as oddsFile:
    sRawJockey = oddsFile.read()
#print(sRawJockey)
sJockey = sRawJockey
dJockeyInfo = json.loads(sJockey)

#print(dJockeyInfo)
#for kJockey, vJockey in dJockeyInfo.items():
#    print(kJockey, vJockey)

#list of dictionaries corresponding to each jockey with a "non-other" jockey/selection number.
lSelections = dJockeyInfo.get('S')
#print(lSelections)

#below gives a dataframe with keys as the columns, but the elements are not list/arrays so we get and empty dataframe.
#newdf = pd.DataFrame.from_dict(lSelections[0])
#convert each element to a list, to get from_dict() to work.

#create empty dataframe with the correct columns, will concat to later.
dfJockeys = pd.DataFrame(columns=lSelections[0].keys())

for iSelection in range(0,len(lSelections)  ):
    #print( lSelections[iSelection])
    #convert to dictionary with elements as lists.
    dSingleJockey = dict()
    for kJockey, vJockey in lSelections[iSelection].items():
        #print(kJockey, vJockey)
        lOneThing = list()
        lOneThing.append(vJockey)
        dSingleJockey[kJockey] = lOneThing
    dfSingleJockey = pd.DataFrame.from_dict(dSingleJockey)
    #print(dfSingleJockey)
    dfJockeys = pd.concat([dfJockeys,dfSingleJockey],axis=0)
    #dfJockeys = dfJockeys.append(dfSingleJockey, ignore_index=True)

dfJockeys.drop(['nameCH'],axis= 1, inplace=True  )
dfJockeys['Points'] = dfJockeys['Points'].replace(to_replace='---',value='0')
dfJockeys['Points'] = dfJockeys['Points'].astype(int)

dfJockeys.rename(columns={'num':'JockeyNumber','nameEN':'jockeyName','opOdds':'OpeningOdds'}, inplace=True)
dfJockeys.rename(columns={'preOdds':'PreviousOdds','latestOdds':'CurrentOdds','Points':'JockeyPoints'}, inplace=True)
dfJockeys.rename(columns={'sRides':'Rides','RRides':'RemainingRides'}, inplace=True)
dfJockeys['Rides'] = dfJockeys['Rides'].astype(int)
dfJockeys.drop(['code','status','sStatus','order','combId','lineId','betSelDetails'],axis=1, inplace=True)
#FYI, there's a ton of info after the first race in betSelDetails... a sample
#betSelDetails {'2': {'raceNo': 0, 'points': 24.0, 'place1st': 2, 'dh1st': False, 'point1st': 24.0, 'place2nd': 0, 'dh2nd': False, 'point2nd': 0.0, 'place3rd': 0, 'dh3rd': False, 'point3rd': 0.0, 'place4th': 0, 'nmtr4th': 0, 'dmtr4th': 1, 'rmRides': 7, 'place4thDouble': 0.0}, '4': {'raceNo': 0, 'points': 24.0, 'place1st': 2, 'dh1st': False, 'point1st': 24.0, 'place2nd': 0, 'dh2nd': False, 'point2nd': 0.0, 'place3rd': 0, 'dh3rd': False, 'point3rd': 0.0, 'place4th': 0, 'nmtr4th': 0, 'dmtr4th': 1, 'rmRides': 6, 'place4thDouble': 0.0}, '1': {'raceNo': 0, 'points': 12.0, 'place1st': 1, 'dh1st': False, 'point1st': 12.0, 'place2nd': 0, 'dh2nd': False, 'point2nd': 0.0, 'place3rd': 0, 'dh3rd': False, 'point3rd': 0.0, 'place4th': 0, 'nmtr4th': 0, 'dmtr4th': 1, 'rmRides': 8, 'place4thDouble': 0.0}, '3': {'raceNo': 0, 'points': 24.0, 'place1st': 2, 'dh1st': False, 'point1st': 24.0, 'place2nd': 0, 'dh2nd': False, 'point2nd': 0.0, 'place3rd': 0, 'dh3rd': False, 'point3rd': 0.0, 'place4th': 0, 'nmtr4th': 0, 'dmtr4th': 1, 'rmRides': 6, 'place4thDouble': 0.0}}
#todo: could be useful for resolving ties on races that have already happened and we don't simulate.

dfJockeys['inPlayUpTo'] = dJockeyInfo.get('INPLAYUPTO')
dfJockeys['stage'] = dJockeyInfo.get('STAGE')
dfJockeys['close'] = dJockeyInfo.get('CLOSE')
dfJockeys['firstRace'] = dJockeyInfo.get('FIRST_RACE')
dfJockeys['lastRace'] = dJockeyInfo.get('LAST_RACE')
dfJockeys['excludeRace'] = dJockeyInfo.get('EXCLUDE_RACE')
dfJockeys['OtherNumber'] = dJockeyInfo.get('OTHER_NO')
dfJockeys['updResultRaceNo'] = dJockeyInfo.get('updResultRaceNo')
#print("dfJockeys")
#print(dfJockeys)
dfJockeys.to_csv(path_to_directory + 'dfJockeys' + '.csv', index=False)

JockeySelections = dfJockeys.copy(deep=True)
#
JockeySelections.drop(['OpeningOdds', 'inPlayUpTo', 'stage', \
                'close', 'firstRace', 'excludeRace', \
                'Rides', 'lastRace', \
                'updResultRaceNo', 'PreviousOdds' ], axis=1, inplace=True)
print("JockeySelections")
print(JockeySelections)
JockeySelections.to_csv(path_to_directory + 'JockeySelections' + '.csv', index=False)

#other jockeys  
#list of dictionaries corresponding to each jockey with a "other" jockey/selection number.
lOther = dJockeyInfo.get('OS')

#print(lOther)
#create empty dataframe with the correct columns, will concat to later.
dfOtherJockeys = pd.DataFrame(columns=lOther[0].keys())

for iOther in range(0,len(lOther)  ):
    dSingleJockey = dict()
    for kJockey, vJockey in lOther[iOther].items():
        #print(kJockey, vJockey)
        lOneThing = list()
        lOneThing.append(vJockey)
        dSingleJockey[kJockey] = lOneThing
    dfSingleJockey = pd.DataFrame.from_dict(dSingleJockey)
    #print(dfSingleJockey)
    # do not know what negative points mean in the betSelDetails for individual other jockeys.
    # has no implact on the total point calculation
    dfOtherJockeys = pd.concat([dfOtherJockeys,dfSingleJockey],axis=0)
    #dfJockeys = dfJockeys.append(dfSingleJockey, ignore_index=True)


dfOtherJockeys.drop(['nameCH',],axis= 1, inplace=True  )
dfOtherJockeys.rename(columns={'num':'JockeyNumber','nameEN':'JockeyName'}, inplace=True)
dfOtherJockeys['JockeyNumber'] = dJockeyInfo.get('OTHER_NO')
dfOtherJockeys.drop(['code','order','betSelDetails'],axis=1, inplace=True)
dfOtherJockeys['Points'] = dfOtherJockeys['Points'].replace(to_replace='---',value='0')
dfOtherJockeys['Points'] = dfOtherJockeys['Points'].astype(int)
dfOtherJockeys.rename(columns={'Points':'JockeyPoints'}, inplace=True)
dfOtherJockeys.rename(columns={'sRides':'Rides','RRides':'RemainingRides'}, inplace=True)
#dfOtherJockeys['Rides'] = dfJockeys['Rides'].astype(int)
#print(dfOtherJockeys)

OtherJockeySelections = dfOtherJockeys.copy(deep=True)
OtherJockeySelections.drop(['Rides'], axis=1, inplace=True)
print("OtherJockeySelections")
print(OtherJockeySelections)
OtherJockeySelections.to_csv(path_to_directory + 'OtherJockeySelections' + '.csv', index=False)



