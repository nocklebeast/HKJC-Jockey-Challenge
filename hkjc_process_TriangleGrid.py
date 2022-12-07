

import pandas as pd
import os
from hkjc_functions import read_race_parameters

pd.set_option('display.max_rows',None)

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
path_to_raw = cwd + '\\odds_files\\' + '\\odds_raw\\'

firstRace, lastRace, sDate, sVenue, jType = read_race_parameters(path_to_raw + 'race_parameters.txt')

lBetTypes=['qin', 'qpl']
#lBetTypes=['qin']  #just quinella.

#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)

    for sType in lBetTypes:
        print(sType)

        path_to_file = path_to_raw + sType + sRace + '.txt'
        print(path_to_file)

        with open(path_to_file,'r') as oddsFile:
            sOut = oddsFile.read()
        oddsFile.close()
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
        #print(Fields)

        #make a list of odds where the odds lists is a list of the horse numbers, odds, and special bit.
        ListOfFields = []
        for item in Fields :
            #print(item)
            lOddsSemiSplit = item.split("=")
            lHorses = str(lOddsSemiSplit[0]).split("-")
            #switch scratched horses "SCR" to "0" on the odds.
            lOddsSemiSplit[1] = lOddsSemiSplit[1].replace("SCR","0")
            #it appears that "---" means that the bet type is not offered valid.
            #if there isn't enough horses the quinella place bet is not valid and the odds
            # quoted are "---" instead of "SCR" or an actual number.... what to do in this
            # circumstance.... let's just try saying the odds are all "1" and then the 
            # QP grid will be a random/equal chance matrix.
            lOddsSemiSplit[1] = lOddsSemiSplit[1].replace("---","1")
            lOdds = [ int(lHorses[0]), int(lHorses[1]) , float(lOddsSemiSplit[1]), int(lOddsSemiSplit[2]) ]
            #print(lOdds)
            ListOfFields.append(lOdds)
            #ListOfFields.append(item.split("="))
        #print(ListOfFields)

        #creates a dataframe/table with the horseno combo as x-y horsenos.
        Pays = pd.DataFrame(ListOfFields, columns=['horseno_x', 'horseno_y', sType+'pays', sType+'IsSpecial'])
        #let's keep rows there the pay is greater than zero.
        Pays = Pays[Pays[sType+'pays'] > 0]
        Pays['Race'] = iRace
        #print(Pays)
        Pays.to_csv(path_to_directory + sType+'Pays' + sRace + '.csv', index=False)

        #can we make an exacta grid out of a Q or QP grid? yes.

        xyPays = Pays
        yxPays = Pays.copy(deep=True)

        yxPays.rename(columns={'horseno_x':'horseno_y','horseno_y':'horseno_x'},inplace=True)
        print(yxPays)

        exPays = pd.concat([xyPays,yxPays],ignore_index=True)
        #print(exPays)

        #exOdds.sort_values( ['horseno_x', 'horseno_y'], ascending = [True, True] )
        exPays.sort_values(by=sType+'pays', ascending = True, inplace=True)
        exPays.sort_values(by=['horseno_x','horseno_y'], ascending = [True,True], inplace=True)

        exPays['xy'] = exPays['horseno_x'] + exPays['horseno_y']
        #print(exPays)
        
        exPays.to_csv(path_to_directory + sType+'exPays' + sRace + '.csv', index=False)

        #let's create a triangular chance grid.
        #print(Pays)
        #compute chances. drop isSpecial.
        Chance = Pays.copy()
        Chance.drop([sType+'IsSpecial'], axis=1, inplace=True)
        Chance[sType+'Chance'] = 1 / Chance[sType+'pays'] 
        #print(Chance)
        
        AllTotals = Chance.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
        #print(AllTotals)
        Chance[sType+'Chance'] = Chance[sType+'Chance'] / AllTotals[sType+'Chance'] 
        #print(Chance)
        #check normalization
        AllTotals = Chance.sum(axis=0) 
        #print(AllTotals)
        #let's keep pays for now.
        #Chance.drop([sType+'pays'], axis=1, inplace=True)
        #print(Chance)
        AllTotals = Chance.sum(axis=0) 

        Chance.to_csv(path_to_directory + sType+'Chance' + sRace + '.csv', index=False)

        #let's make a normalized exacta grid of the triangular (qpl and qin) chances.

        #triangles to squares.
        yzChance = Chance.rename(columns={"horseno_x": "horseno_y", "horseno_y": "horseno_x"})
        print(yzChance)

        #merge to create square exacta grid.
        ExQChance = pd.concat([Chance, yzChance],  axis=0 ) #stack vertically.
        ExQChance.sort_values(by=['horseno_x','horseno_y'], inplace=True)
        print(ExQChance)

        #renormalize chances.

        AllTotals = ExQChance.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
        print(AllTotals)
        ExQChance[sType+'Chance'] = ExQChance[sType+'Chance'] / AllTotals[sType+'Chance'] 
        print(ExQChance)
        #check normalization
        AllTotals = ExQChance.sum(axis=0) 
        print(AllTotals)

        ExQChance.to_csv(path_to_directory + 'Ex' + sType + 'Chance' + sRace + '.csv', index=False)


    #end bet types

    #let's merge the two triangular grid chance types.

    #for sType in lBetTypes:
    sType = 'qin'

    path_to_file = path_to_directory + sType + 'Chance' + sRace + '.csv'
    print(path_to_file)
    qinChance = pd.read_csv(path_to_file)
    print(qinChance)
    sType = 'qpl'
    path_to_file = path_to_directory + sType + 'Chance' + sRace + '.csv'
    print(path_to_file)

    qplChance = pd.read_csv(path_to_file)
    print(qplChance)

    #merge quinella and quinella place chance tables/dataframes/grid
    QinQplChance = pd.merge(qinChance,qplChance,on=['Race','horseno_x','horseno_y'], how='inner')
    print(QinQplChance)
    #save to csv, the combined triangular grid.
    QinQplChance.to_csv(path_to_directory + 'QinQplChance' + sRace + '.csv', index=False)

    #let's make a normalized exacta grid of the qpl and qin chances.

    #triangles to squares.
    yxQinQplChance = QinQplChance.rename(columns={"horseno_x": "horseno_y", "horseno_y": "horseno_x"})
    print(yxQinQplChance)

    #merge to create square exacta grid.
    exQinQplChance = pd.concat([QinQplChance, yxQinQplChance],  axis=0 ) #stack vertically.
    exQinQplChance.sort_values(by=['horseno_x','horseno_y'], inplace=True)
    print(exQinQplChance.head())

    #renormalize chances.

    AllTotals = exQinQplChance.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
    print(AllTotals)
    exQinQplChance['qinChance'] = exQinQplChance['qinChance'] / AllTotals['qinChance'] 
    exQinQplChance['qplChance'] = exQinQplChance['qplChance'] / AllTotals['qplChance'] 
    print(exQinQplChance.head())
    #check normalization
    AllTotals = exQinQplChance.sum(axis=0) 
    print(AllTotals)

    exQinQplChance.to_csv(path_to_directory + 'exQinQplChance' + sRace + '.csv', index=False)

    #create a yz version of the qin-qpl exacta grid.
    yzQinQplChance = exQinQplChance.copy(deep=True)
    yzQinQplChance = exQinQplChance.rename(columns={"horseno_x": "horseno_y", "horseno_y": "horseno_z"})
    print(yzQinQplChance.head())
    yzQinQplChance.to_csv(path_to_directory + 'yzQinQplChance' + sRace + '.csv', index=False)

#end iRace




