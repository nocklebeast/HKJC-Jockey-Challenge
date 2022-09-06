
#process jockey odds info from jockey challenge

import pandas as pd
import numpy as np
pd.set_option('display.max_rows',None)

path_to_directory = 'M:\\python\\hkjc\\odds_files\\'
#print(path_to_directory)
path_to_file = path_to_directory + 'jkc.txt' 
#print(path_to_file)

with open(path_to_file,mode='r', encoding='utf-8') as oddsFile:
    sRawJockey = oddsFile.read()
oddsFile.close()
#print(sRawJockey)

#remove first { and last ]
iPos = sRawJockey.find("{",0)
jPos = sRawJockey.find("}",iPos+1)
sJockey = sRawJockey[iPos+1 : jPos]

# it might be useful to strip out all the " (do we really need all that?)
sJockey = sJockey.replace('"','')
print(sJockey)

dctJockeyInfo = dict( keyValue.split(":") for keyValue in sJockey.split(",") )
#print(dctJockeyInfo)
for kJockey, vJockey in dctJockeyInfo.items():
    print(kJockey, vJockey)

sSelections = dctJockeyInfo.get('S')
#print (sSelections)
lSelections = sSelections.split("@@@")
#print(lSelections)

#jockey selection/numbers
#strip leading | from strings to avoid empty elements
sJockeyNumbers = lSelections[0]
sJockeyNumbers = sJockeyNumbers.replace("|", " ", 1)
sJockeyNumbers = sJockeyNumbers.strip()
#print(sJockeyNumbers)
lNumbers = sJockeyNumbers.split('|')
#print(lNumbers)
jNumbers = np.array(lNumbers, dtype=np.int8)
#print(jNumbers)
dfJNum = pd.DataFrame(jNumbers,columns=['JockeyNumber'])
#print(dfJNum)


### get jockey names
#strip leading | from strings to avoid empty elements
sJockeyNames = lSelections[2]
sJockeyNames = sJockeyNames.replace("|", " ", 1)
sJockeyNames = sJockeyNames.strip()
lJockeyNames = sJockeyNames.split('|')
jNames = np.array(lJockeyNames)
dfJName = pd.DataFrame(jNames,columns=['jockeyName'])

### get opening odds 
#strip leading | from strings to avoid empty elements
sOpeningOdds = lSelections[6]
sOpeningOdds = sOpeningOdds.replace("|", " ", 1)
sOpeningOdds = sOpeningOdds.strip()
lOpeningOdds = sOpeningOdds.split('|')
aOpeningOdds = np.array(lOpeningOdds)
dfOpeningOdds = pd.DataFrame(aOpeningOdds,columns=['OpeningOdds'])

### get Previous odds 
#strip leading | from strings to avoid empty elements
sPreviousOdds = lSelections[7]
sPreviousOdds = sPreviousOdds.replace("|", " ", 1)
sPreviousOdds = sPreviousOdds.strip()
lPreviousOdds = sPreviousOdds.split('|')
aPreviousOdds = np.array(lPreviousOdds)
dfPreviousOdds = pd.DataFrame(aPreviousOdds,columns=['PreviousOdds'])

### get Current odds 
#strip leading | from strings to avoid empty elements
sCurrentOdds = lSelections[8]
sCurrentOdds = sCurrentOdds.replace("|", " ", 1)
sCurrentOdds = sCurrentOdds.strip()
lCurrentOdds = sCurrentOdds.split('|')
aCurrentOdds = np.array(lCurrentOdds)
dfCurrentOdds = pd.DataFrame(aCurrentOdds,columns=['CurrentOdds'])

### get Jocky Points  
#strip leading | from strings to avoid empty elements
sPoints = lSelections[9]
sPoints = sPoints.replace("|", " ", 1)
#replace "---" points with "0"
sPoints = sPoints.replace("---","0")
sPoints = sPoints.strip()
lPoints = sPoints.split('|')
aPoints = np.array(lPoints)
dfPoints = pd.DataFrame(aPoints,columns=['JockeyPoints'])
#print(dfPoints)

### get Jocky Rides  
#strip leading | from strings to avoid empty elements
sRides = lSelections[10]
sRides = sRides.replace("|", " ", 1)
sRides = sRides.strip()
lRides = sRides.split('|')
aRides = np.array(lRides)
dfRides = pd.DataFrame(aRides,columns=['Rides'])


dfJockeys = pd.concat([dfJNum,dfJName,dfCurrentOdds,dfPoints,dfOpeningOdds,dfPreviousOdds,dfRides], axis=1)
#print(dfJockeys)

dfJockeys['inPlayUpTo'] = dctJockeyInfo.get('INPLAYUPTO')
dfJockeys['stage'] = dctJockeyInfo.get('STAGE')
dfJockeys['close'] = dctJockeyInfo.get('CLOSE')
dfJockeys['firstRace'] = dctJockeyInfo.get('FIRST_RACE')
dfJockeys['lastRace'] = dctJockeyInfo.get('LAST_RACE')
dfJockeys['excludeRace'] = dctJockeyInfo.get('EXCLUDE_RACE')
dfJockeys['OtherNumber'] = dctJockeyInfo.get('OTHER_NO')
dfJockeys['updResultRaceNo'] = dctJockeyInfo.get('updResultRaceNo')
print("dfJockeys")
print(dfJockeys)
dfJockeys.to_csv(path_to_directory + 'dfJockeys' + '.csv', index=False)



JockeySelections = dfJockeys.copy(deep=True)
#
JockeySelections.drop(['OpeningOdds', 'inPlayUpTo', 'stage', \
                'close', 'firstRace', 'excludeRace', \
                'Rides', 'lastRace', \
                'updResultRaceNo', 'PreviousOdds' ], axis=1, inplace=True)
"""
JockeySelections.drop(['OpeningOdds', 'inPlayUpTo', 'stage', \
                'close', 'firstRace', 'excludeRace', \
                'Points', 'Rides', 'lastRace', \
                'updResultRaceNo', 'PreviousOdds', 'CurrentOdds' ], axis=1, inplace=True)
"""
print("JockeySelections")
print(JockeySelections)
JockeySelections.to_csv(path_to_directory + 'JockeySelections' + '.csv', index=False)


sOther = dctJockeyInfo.get('OS')
print (sOther)
lOther = sOther.split("@@@")
#print(lOther)

#other jockeys  
### get jockey names
#strip leading | from strings to avoid empty elements
sJockeyNames = lOther[0]
sJockeyNames = sJockeyNames.replace("|", " ", 1)
sJockeyNames = sJockeyNames.strip()
lJockeyNames = sJockeyNames.split('|')
jNames = np.array(lJockeyNames)
dfJName = pd.DataFrame(jNames,columns=['jockeyName'])

### get Jocky Rides  
#strip leading | from strings to avoid empty elements
sRides = lOther[4]
sRides = sRides.replace("|", " ", 1)
sRides = sRides.strip()
lRides = sRides.split('|')
aRides = np.array(lRides)
dfRides = pd.DataFrame(aRides,columns=['Rides'])

dfOtherJockeys = pd.concat([dfJName,dfRides], axis=1)
dfOtherJockeys['JockeyNumber'] = dctJockeyInfo.get('OTHER_NO')
print("dfOtherJockeys")
print(dfOtherJockeys)


OtherJockeySelections = dfOtherJockeys.copy(deep=True)
OtherJockeySelections.drop(['Rides'], axis=1, inplace=True)
print("OtherJockeySelections")
print(OtherJockeySelections)
OtherJockeySelections.to_csv(path_to_directory + 'OtherJockeySelections' + '.csv', index=False)



