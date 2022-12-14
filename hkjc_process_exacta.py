
import pandas as pd
import os
from hkjc_functions import read_race_parameters, renormalize_column

pd.set_option('display.max_rows',None)


cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
path_to_raw = cwd + '\\odds_files\\' + '\\odds_raw\\'

firstRace, lastRace, sDate, sVenue, jType = read_race_parameters(path_to_raw + 'race_parameters.txt')

sType = 'fct'
print(sType)

#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)


    path_to_file = path_to_raw + sType + sRace + '.txt'
    print(path_to_file)

    with open(path_to_file,'r') as oddsFile:
        sOut = oddsFile.read()
        #oddsFile.close() don't need this with 'with' context.
        #print(file.closed) check to see if file closed.
    print(sOut)

    #get update time
    iPos = sOut.find("OUT",1)
    sUpdateTime = sOut[iPos+6:iPos+12]
    print(sUpdateTime)
 
    #get odds strings.
    iPos = sOut.find("@@@;",1)
    sOdds = sOut[iPos+4 : -4]
    print(sOdds)

    #split up each 2-horse combination into a list, Fields.
    Fields = sOdds.split(";")
    print(Fields)

    #make a list of odds where the odds lists is a list of the horse numbers, odds, and special bit.
    ListOfFields = []
    for item in Fields :
        #print(item)
        lOddsSemiSplit = item.split("=")
        lHorses = str(lOddsSemiSplit[0]).split("-")
        #switch scratched horses "SCR" to "0" on the odds.
        lOddsSemiSplit[1] = lOddsSemiSplit[1].replace("SCR","0")
        lOdds = [ int(lHorses[0]), int(lHorses[1]) , float(lOddsSemiSplit[1]), int(lOddsSemiSplit[2]) ]
        print(lOdds)
        ListOfFields.append(lOdds)
        #ListOfFields.append(item.split("="))
    print(ListOfFields)

    #creates a dataframe/table with the horseno combo as x-y horsenos.
    Pays = pd.DataFrame(ListOfFields, columns=['horseno_x', 'horseno_y', sType+'pays', sType+'IsSpecial'])
    #drop scratched, keep rows with Pay > 0    
    Pays = Pays[Pays[sType+'pays'] > 0]
    Pays['Race'] = iRace
    print(Pays.head())
    Pays.to_csv(path_to_directory + sType+'Pays' + sRace + '.csv', index=False)

    Chance = Pays.copy()
    Chance.drop([sType+'IsSpecial'], axis=1, inplace=True)
    Chance[sType+'Chance'] = 1 / Chance[sType+'pays'] 
    #print(Chance.head(5))

    renormalize_column(Chance, sType+'Chance')
    #check normalization
    #AllTotals = Chance.sum(axis=0) 
    #print(AllTotals)
    #let's keep pays for now.
    #Chance.drop([sType+'pays'], axis=1, inplace=True)
    print(Chance.head(5))
    print(Chance.tail(5))
    #AllTotals = Chance.sum(axis=0) 


    Chance.to_csv(path_to_directory + sType+'Chance' + sRace + '.csv', index=False)

#end race.





