from xml.etree.ElementTree import TreeBuilder
import pandas as pd
import numpy as np
import os
from datetime import datetime

pd.set_option('display.max_rows',None)

cTakeout = 0.25
np.random.seed(10)

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

sType = 'tcebank'

#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)

    path_to_file = path_to_directory + sType + sRace + '.txt'
    print(path_to_file)

    with open(path_to_file,'r') as oddsFile:
        sOut = oddsFile.read()
    oddsFile.close()
    #print(sOut)

    #get update time
    iPos = sOut.find("OUT",1)
    sUpdateTime = sOut[iPos+6:iPos+12]
    print(sUpdateTime)
    print(sDate)
    sUpdateDateTime = sDate + ' ' + sUpdateTime[0:2] + ':' + sUpdateTime[2:4] + ':' + sUpdateTime[4:6]
    dUpdateTime = datetime.strptime(sUpdateDateTime , '%Y-%m-%d %H:%M:%S')
    print(dUpdateTime)

    #get tierce investments string.
    iPos = sOut.find(";",1)
    jPos = sOut.find('"}', iPos+1)
    sInvestments = sOut[iPos+1 : jPos]
    print(sInvestments)

    #get top 10 bankers for each horse, 1, 2, 3, 4...
    #or each horse, split on ";"
    lBankers = sInvestments.split(";")
    #print(lBankers)
    
    BankerListOfFields = []
    for item in lBankers :
        #print(item)
        splitItem = item.split("|") 
        #split item looks like ['1', '1-2-9=289', '1-3-10=282', '1-9-2=244', '1-9-6=313', '1-9-10=240', '1-9-11=179', '1-10-3=245', '1-10-9=225', '1-10-11=297', '1-11-9=212']
        #print(splitItem)
        #remove 1st element of splitItem list (the banker).  this gives us just the trifecta combos and pays for that banker.
        lComboPays = splitItem[1:11]
        #print(lComboPays)
        
        for ComboPay in lComboPays:
            #print(ComboPay)
            #split ComboPay on "="
            splitComboPay = ComboPay.split("=")
            pay = splitComboPay[1]
            pay = pay.replace("SCR","0")
            #print(pay)
            #split on the first part of ComboPay on "-" to get the horses (trifecta combo)
            horseCombo = splitComboPay[0].split("-")
            #print(horseCombo)
            xhorse = horseCombo[0]
            yhorse = horseCombo[1]
            zhorse = horseCombo[2]
            BankerListOfFields.append( [ int(xhorse), int(yhorse) , int(zhorse), int(pay)] )

    #print(placeListOfFields)
    BankerPays = pd.DataFrame(BankerListOfFields, columns=['xhorseno', 'yhorseno', 'zhorseno', 'PayBank' ])
    #print(BankerPays.head())
    
    #let's keep rows where pay is greater than zero AND less than 999
    BankerPays = BankerPays[ (BankerPays['PayBank'] > 0) & (BankerPays['PayBank'] < 999) ]

    BankerPays['Race'] = iRace
    BankerPays['UpdateTimeBank'] = dUpdateTime
    BankerPays.sort_values(by=['Race','xhorseno', 'yhorseno', 'zhorseno'], ascending=True, inplace=True)

    #let's not compute chances just yet.
    """"
    BankerPays['Top10Ch'] = 1 / BankerPays['PayTop10']
    #compute chances
    AllTotals = BankerPays.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
    print(AllTotals)
    #normalize the partial list of all chances to 1 for now.
    BankerPays['Top10Ch'] = BankerPays['Top10Ch'] / AllTotals['Top10Ch']
    BankerPays['Race'] = iRace

    AllTotals = BankerPays.sum(axis=0)  
    print(AllTotals)
    """
    BankerPays.to_csv(path_to_directory + sType + sRace + '.csv', index=False)
    print(BankerPays)

#end Race

