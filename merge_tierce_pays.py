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


for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    Top20Pays = pd.read_csv(path_to_directory + 'tcetop' + sRace + '.csv')
    print(Top20Pays)
    BankerPays = pd.read_csv(path_to_directory + 'tcebank' + sRace + '.csv')
    print(BankerPays)

    Pays = Top20Pays.merge(BankerPays,how='outer', on=['Race','xhorseno','yhorseno','zhorseno']) 
    Pays.sort_values(by=['Race','xhorseno','yhorseno','zhorseno'], inplace=True)

    print(Pays)


    #Pay = Pay Bank (banker top 10) if not null.  
    #print(Pays['PayBank'].notnull())

    Pays.loc[ Pays['PayBank'].notnull() , 'Pay' ] = Pays['PayBank']
    Pays.loc[ ( Pays['Pay'].isnull() ) & ( Pays['PayTop20'].notnull() ) , 'Pay'  ] = Pays['PayTop20']

    #The replace Pay with top 20 pay if top 20 pay is not null and update time for Top20 Pay is more recent.
    #Pays.loc[ ( Pays['PayTop20'].notnull() ) & ( Pays['UpdateTimeTop20'] > Pays['UpdateTimeBank'] ) , 'Pay' ] = Pays['PayTop20']
    
    
    #now same with the update times.
    Pays.loc[ Pays['UpdateTimeBank'].notnull() , 'UpdateTime' ] = Pays['UpdateTimeBank']
    Pays.loc[ ( Pays['UpdateTimeTop20'].notnull() ) & ( Pays['UpdateTimeTop20'] > Pays['UpdateTimeBank'] ) , 'UpdateTime' ] = Pays['UpdateTimeTop20']
    #drop the original pays and times now that we've merge by horse-combo and most recent update times.
    #Pays.drop(['PayBank', 'PayTop20', 'UpdateTimeTop20' , 'UpdateTimeBank'], axis=1, inplace=True)
    Pays.reset_index(inplace=True)
    print(Pays)

    Pays.to_csv(path_to_directory + 'TiercePays' + sRace + '.csv', index=False)


#end Race


######################todo merge (loop) over all races #########################
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





