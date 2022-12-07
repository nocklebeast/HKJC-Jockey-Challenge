#process jockey odds info from jockey challenge

from calendar import isleap
import pandas as pd
import numpy as np
import os
import json
from hkjc_functions import read_race_parameters

pd.set_option('display.max_rows',None)

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
path_to_raw = cwd + '\\odds_files\\' + '\\odds_raw\\'

firstRace, lastRace, sDate, sVenue, jType = read_race_parameters(path_to_raw + 'race_parameters.txt')

for sType in [jType]:
    if sType == 'jkc':
        #jword = 'jockey'
        Jword = 'Jockey'
    else:
        #jword = 'trainer'
        Jword = 'Trainer'

    #print(path_to_directory)
    path_to_file = path_to_raw + sType + '.txt' 

    try:
        with open(path_to_file,mode='r', encoding='utf-8') as oddsFile:
            sRawJockey = oddsFile.read()
    except :
        print('failed to open ' + path_to_file  + '. Perhaps there is not ' + sType + ' challenge today.')
        break

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

    """
    could try this instead.
    #convert the series into a dictionary and then into a dataframe 
    #the dataframe conversion is expecting a dictionary of LISTS  (key:value=a list)
    #use index=[0] to convert the values into a list 
    #see https://www.geeksforgeeks.org/how-to-fix-if-using-all-scalar-values-you-must-pass-an-index/
    dctSingleOtherJockey = SingleOtherJockey.to_dict()
    """
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

    dfJockeys.to_csv(path_to_directory + 'Raw' + Jword + 's.csv', index=False)

    dfJockeys.drop(['nameCH'],axis= 1, inplace=True  )
    dfJockeys['Points'] = dfJockeys['Points'].replace(to_replace='---',value='0')
    dfJockeys['Points'] = dfJockeys['Points'].astype(int)
    dfJockeys['Points'] = dfJockeys['Points'].replace(to_replace=-1,value=0)
    

    dfJockeys.rename(columns={'num':sType+'Number','nameEN':sType+'Name','opOdds':sType+'OpeningOdds'}, inplace=True)
    dfJockeys.rename(columns={'preOdds':sType+'PreviousOdds','latestOdds':sType+'CurrentOdds','Points':sType+'Points'}, inplace=True)
    dfJockeys.rename(columns={'sRides':sType+'Rides','RRides':sType+'RemainingRides'}, inplace=True)
    dfJockeys[sType+'Rides'] = dfJockeys[sType+'Rides'].astype(int)
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
    dfJockeys[sType+'OtherNumber'] = dJockeyInfo.get('OTHER_NO')
    dfJockeys['updResultRaceNo'] = dJockeyInfo.get('updResultRaceNo')
    #print("dfJockeys")
    #print(dfJockeys)
    dfJockeys.to_csv(path_to_directory + 'df' + Jword + 's' + '.csv', index=False)

    JockeySelections = dfJockeys.copy(deep=True)
    #
    JockeySelections.drop([sType+'OpeningOdds', 'inPlayUpTo', 'stage', \
                    'close', 'firstRace', 'excludeRace', \
                    sType+'Rides', 'lastRace', \
                    'updResultRaceNo', sType+'PreviousOdds' ], axis=1, inplace=True)
    #print("JockeySelections")
    #print(JockeySelections)
    JockeySelections.to_csv(path_to_directory + Jword + 'Selections' + '.csv', index=False)

    #other jockeys  
    #list of dictionaries corresponding to each jockey with a "other" jockey/selection number.
    lOther = dJockeyInfo.get('OS')
    #on special occassions (like HK International Races) there are not "other jockeys".
    #let's check to see if we have other jockeys.
    if len(lOther) <= 0:
        print("no other jockeys today")
        OtherNumber = 0
        OtherOdds = 999
    else:

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

        dfOtherJockeys.to_csv(path_to_directory + 'RawOther' + Jword + 's' + '.csv', index=False)

        dfOtherJockeys.drop(['nameCH',],axis= 1, inplace=True  )
        dfOtherJockeys.rename(columns={'num':sType+'Number','nameEN':sType+'Name'}, inplace=True)
        dfOtherJockeys[sType+'Number'] = dJockeyInfo.get('OTHER_NO')
        dfOtherJockeys.drop(['code','order','betSelDetails'],axis=1, inplace=True)
        dfOtherJockeys['Points'] = dfOtherJockeys['Points'].replace(to_replace='---',value='0')
        dfOtherJockeys['Points'] = dfOtherJockeys['Points'].astype(int)
        #sometimes jockey club reports other points as "-1" ???? just reset to 0 I think.
        dfOtherJockeys['Points'] = dfOtherJockeys['Points'].replace(to_replace=-1,value=0)

        
        dfOtherJockeys.rename(columns={'Points':sType+'Points'}, inplace=True)
        dfOtherJockeys.rename(columns={'sRides':sType+'Rides','RRides':sType+'RemainingRides'}, inplace=True)
        #dfOtherJockeys['Rides'] = dfJockeys['Rides'].astype(int)
        #print(dfOtherJockeys)

        OtherJockeySelections = dfOtherJockeys.copy(deep=True)
        OtherJockeySelections.drop([sType+'Rides'], axis=1, inplace=True)
        #print("OtherJockeySelections")
        #print(OtherJockeySelections)
        OtherJockeySelections.to_csv(path_to_directory + 'Other' + Jword +'Selections' + '.csv', index=False)

        #later, merge race entry(jockeys) with jockey selections
        #JockeySelections = pd.read_csv(path_to_directory + 'JockeySelections' + '.csv')
        #print(JockeySelections)
        dfOtherNumber = JockeySelections[JockeySelections[sType+'Name'] == 'Others']
        
        OtherNumber = dfOtherNumber[sType+'OtherNumber'].loc[dfOtherNumber.index[0]]
        OtherOdds = dfOtherNumber[sType+'CurrentOdds'].loc[dfOtherNumber.index[0]]
        #print(OtherNumber)
        #print(OtherOdds)

    if OtherNumber == 0:
        AllJockeySelections = JockeySelections.copy(deep=True)
        AllJockeySelections[sType+'OtherNumber'] = OtherNumber
    else:
        #let's also concat the Other Jockey Selections 
        # so that we can map all the other jockeys by their names to other number properly.
        OtherJockeySelections = pd.read_csv(path_to_directory + 'Other' + Jword + 'Selections' + '.csv')
        OtherJockeySelections[sType+'OtherNumber'] = OtherNumber
        AllJockeySelections = pd.concat([JockeySelections,OtherJockeySelections], axis=0)
        
    #fill in the current Odds for other jockeys with the correct odds for others.
    AllJockeySelections[sType+'CurrentOdds'].fillna(OtherOdds,inplace=True)

    #"LSE" is "out" mathematically impossible to win, let's give that jockey odds of 9999 (which is a number)
    AllJockeySelections[sType+'CurrentOdds'] = AllJockeySelections[sType+'CurrentOdds'].replace(to_replace='LSE',value='9999')

    AllJockeySelections.to_csv(path_to_directory + 'All' + Jword + 'Selections' + '.csv', index=False)
    print(AllJockeySelections)

#end sType