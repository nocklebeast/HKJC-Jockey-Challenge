
import pandas as pd
import os
from datetime import datetime

pd.set_option('display.max_rows',None)

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

sType = 'tcetop'
print(sType)

#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)

    path_to_file = path_to_directory + sType + sRace + '.txt'
    print(path_to_file)

    with open(path_to_file,'r') as oddsFile:
        sOut = oddsFile.read()
    print(sOut)

    #get update time
    iPos = sOut.find("OUT",1)
    sUpdateTime = sOut[iPos+6:iPos+12]
    print(sUpdateTime)
    sUpdateDateTime = sDate + ' ' + sUpdateTime[0:2] + ':' + sUpdateTime[2:4] + ':' + sUpdateTime[4:6]
    dUpdateTime = datetime.strptime(sUpdateDateTime , '%Y-%m-%d %H:%M:%S')

    #get odds strings.
    iPos = sOut.find("@@@;",1)
    sOdds = sOut[iPos+4 : -4]  
    #print(sOdds)

    #split up each 3-horse combination into a list, Fields.
    Fields = sOdds.split(";")
    #print(Fields)

    #make a list of odds where the odds lists is a list of the horse numbers, odds, and special bit.
    ListOfFields = []
    for item in Fields :
        #print(item)
        lOddsSemiSplit = item.split("=")
        lHorses = str(lOddsSemiSplit[0]).split("-")
        #print(lHorses)
        #switch scratched horses "SCR" to "0" on the odds.
        ########todo: do we need this?
        #lOddsSemiSplit[1] = lOddsSemiSplit[1].replace("SCR","0")
        #print(lOddsSemiSplit)
        lOdds = [ int(lHorses[0]), int(lHorses[1]) , int(lHorses[2]), int(lOddsSemiSplit[1]) ]
        #print(lOdds)
        ListOfFields.append(lOdds)
        #ListOfFields.append(item.split("="))
    #print(ListOfFields)

    #creates a dataframe/table with the horseno combo as x-y-z horsenos.
    Pays = pd.DataFrame(ListOfFields, columns=['xhorseno', 'yhorseno', 'zhorseno', 'PayTop20'])
    #drop scratched, keep rows with Pay > 0    
    Pays = Pays[ (Pays['PayTop20'] > 0) & (Pays['PayTop20'] < 999) ]

    Pays['Race'] = iRace
    Pays['UpdateTimeTop20'] = dUpdateTime
    Pays.sort_values(by=['Race','xhorseno', 'yhorseno', 'zhorseno'], ascending=True, inplace=True)
    print(Pays)
    Pays.to_csv(path_to_directory + sType + sRace + '.csv', index=False)

    #let's not comput chances just yet.
    """
    Chance = Pays.copy()
    Chance[sType+'Chance'] = 1 / Chance[sType+'pays'] 

    print(Chance)

    AllTotals = Chance.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
    print(AllTotals)
    Chance[sType+'Chance'] = Chance[sType+'Chance'] / AllTotals[sType+'Chance'] 
    print(Chance)
    #check normalization
    #AllTotals = Chance.sum(axis=0) 
    #print(AllTotals)
    #let's keep pays for now.
    #Chance.drop([sType+'pays'], axis=1, inplace=True)
    #print(Chance)
    #AllTotals = Chance.sum(axis=0) 


    Chance.to_csv(path_to_directory + sType+'Chance' + sRace + '.csv', index=False)
    """

#end race.





