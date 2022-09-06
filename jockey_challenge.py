
###################################################
############## jockey challgenge monte carlo
##################################################
#run after getting the tierce investments.  

import pandas as pd
import numpy as np
import os 

pd.set_option('display.max_rows',None)

np.random.seed(10)

nUnbrokenTies = 0

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
print(path_to_directory)

path_to_file = path_to_directory + 'race_parameters' + '.txt'
RaceParameters = pd.read_csv(path_to_file)  
print(RaceParameters)

sDate = RaceParameters.at[0,'sDate']
sRace = str(RaceParameters.at[0,'sRace'])
firstRace = int(RaceParameters.at[0,'firstRace'])
lastRace = int(RaceParameters.at[0,'lastRace'])
sVenue = RaceParameters.at[0,'sVenue']


#map of Jockey names to Jockey selection numbers.
path_to_file = path_to_directory + 'JockeySelections' + '.csv'
TodaysJockeySelections = pd.read_csv(path_to_file)
TodaysJockeySelections.drop('OtherNumber',axis=1,inplace=True)
TodaysJockeySelections.sort_values(by='JockeyNumber',inplace=True)
TodaysJockeySelections.reindex

SimJockeyPoints = TodaysJockeySelections.copy(deep=True)
SimJockeyPoints['TotalPoints'] = 0
SimJockeyPoints['TotalWins'] = 0
SimJockeyPoints['nRuns'] = 0
#print(SimJockeyPoints)

#JockeyTierce for all races of the day.... concat all the JockeyTierces for individual races.
JockeyTierceChance = pd.DataFrame()

#contruct jockey challenge matrix based on all races for the day.
#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    #print(sRace)

    path_to_file = path_to_directory + 'JockeyTierce' + sRace + '.csv'
    tempJockeyTierce = pd.read_csv(path_to_file)  

    JockeyTierceChance = pd.concat([JockeyTierceChance, tempJockeyTierce], ignore_index=True )
    #print(JockeyTierceChance.head())
    #print(JockeyTierceChance.tail())

#end iRace

JockeyTierceChance['CumTierceCh'] = JockeyTierceChance[['Race','TierceCh']].groupby('Race').cumsum()

#default is to shift one down with NaN as the 1st thing of the group.
JockeyTierceChance['ShiftTierceCh'] = JockeyTierceChance.groupby('Race')['CumTierceCh'].shift()
JockeyTierceChance.fillna(0,inplace=True)
print(JockeyTierceChance.head())


#run a race day's simulation nSims times.
nSims = 10000
iNextPrint = 0
nProgressPrints = 20
for iter in range(nSims): 
    #print("nSims = " + str(iter/nSims) )

    if int(iter/nSims*nProgressPrints) >= iNextPrint:
        iNextPrint = iNextPrint + 1
        print(SimJockeyPoints)
        print("pctSims = " + str(iter/nSims) )

    ###################### throw the darts at each race (groupby Race) ############
    # (do not use groupby('Race).sample, as that gives an equal chance to each trifecta combo not proportional to chance.)
    JockeyTierce = JockeyTierceChance.copy(deep=True)
    JockeyTierce['dart'] = JockeyTierce.groupby('Race').Race.transform(func = lambda x : np.random.random())
    #python note: below does not work
    #JockeyTierce['winner'] = JockeyTierce['dart'] > JockeyTierce['ShiftTriCh'] and JockeyTierce['dart'] < JockeyTierce['CumTriCh']
    #  
    #python note: below works https://stackoverflow.com/questions/30912403/appending-boolean-column-in-panda-dataframe
    #our trifecta model chances (based on ex = w x qp x q) is probably more accurate than tierce investment chances
    # although skewed towards favorites. (TriCh vs TierceCh)
    # use trifacta chances based on Wx x Qxy x Wy public win and quinella odds.
    #JockeyTierce['winner'] = (JockeyTierce['dart'] > JockeyTierce['ShiftTriCh']) & (JockeyTierce['dart'] < JockeyTierce['CumTriCh']) 
    # use trifecta changes basedon public tierce investments?
    JockeyTierce['winner'] = (JockeyTierce['dart'] > JockeyTierce['ShiftTierceCh']) & (JockeyTierce['dart'] < JockeyTierce['CumTierceCh']) 
    JockeyTierce['bWinner'] = JockeyTierce['winner'].astype(int)
    #print(JockeyTierce)
    #print(JockeyTierce.head())
    #print(JockeyTierce.tail())

    Points = JockeyTierce.copy(deep=True)
    Points.drop(['Race','Hx','Hy','Hz','TierceCh','CumTierceCh','ShiftTierceCh','dart','winner'], axis=1, inplace=True)

    Points1 = Points.copy(deep=True)
    Points1['Points1'] = 12 * Points['bWinner']
    Points1.drop(['Jy','Jz'], axis=1, inplace=True)
    Points1.rename(columns = {'Jx':'JockeyNumber'}, inplace=True)
    #print(Points1.tail())
    RaceDayPoints1 = Points1.groupby(['JockeyNumber']).sum().reset_index()
    RaceDayPoints1.rename(columns = {'bWinner':'nWins'}, inplace=True)
    #print(RaceDayPoints1)
    

    Points2 = Points.copy(deep=True)
    Points2['Points2'] = 6 * Points['bWinner']
    Points2.drop(['Jx','Jz'], axis=1, inplace=True)
    Points2.rename(columns = {'Jy':'JockeyNumber'}, inplace=True)
    #print(Points2.tail())
    RaceDayPoints2 = Points2.groupby(['JockeyNumber']).sum().reset_index()
    RaceDayPoints2 = RaceDayPoints2.groupby(['JockeyNumber']).sum().reset_index()
    RaceDayPoints2.rename(columns = {'bWinner':'nPlaces'}, inplace=True)
    #print(RaceDayPoints2)
    

    Points3 = Points.copy(deep=True)
    Points3['Points3'] = 4 * Points['bWinner']
    Points3.drop(['Jx','Jy'], axis=1, inplace=True)
    Points3.rename(columns = {'Jz':'JockeyNumber'}, inplace=True)
    #print(Points3.tail())
    RaceDayPoints3 = Points3.groupby(['JockeyNumber']).sum().reset_index()
    RaceDayPoints3.rename(columns = {'bWinner':'nShows'}, inplace=True)
    #print(RaceDayPoints3)
    
    RaceDayPoints = RaceDayPoints1.merge(RaceDayPoints2.merge(RaceDayPoints3, on='JockeyNumber', how='inner'), on='JockeyNumber', how='inner')
    RaceDayPoints['Points'] = RaceDayPoints['Points1'] + RaceDayPoints['Points2'] + RaceDayPoints['Points3']
    RaceDayPoints.drop(['Points1','Points2','Points3'], axis=1, inplace=True)
    MaxPoints = RaceDayPoints.max(axis=0)
    #print(RaceDayPoints)
    #print(MaxPoints)
    RaceDayPoints['isWinner'] = RaceDayPoints['Points'] == MaxPoints['Points']
    RaceDayPoints['Winner'] = RaceDayPoints['isWinner'].astype(int)
    RaceDayPoints['TiePoints'] = 0

    #Winners = RaceDayPoints.apply(lambda x : 1 if x['Winner'] == 1 else 0, axis = 1)
    #count winners
    #print(RaceDayPoints)
    AllTotals = RaceDayPoints.sum(axis=0)
    #and break ties.
    #if more than one winner for the race day.
    
    if AllTotals['Winner'] > 1:
        #print("break at wins")
        #print(AllTotals)
        #kkkkkkkkkkkkkkkk
        RaceDayPoints['TiePoints'] = RaceDayPoints['Points'] + RaceDayPoints['Winner'] * RaceDayPoints['nWins']
        #print(RaceDayPoints)
        MaxPoints = RaceDayPoints.max(axis=0)
        RaceDayPoints['isWinner'] = RaceDayPoints['TiePoints'] == MaxPoints['TiePoints']
        RaceDayPoints['Winner'] = RaceDayPoints['isWinner'].astype(int)
        #print(RaceDayPoints)
        #kkkkkkkkkkkkkkk
        #check for ties again. 
        
        AllTotals = RaceDayPoints.sum(axis=0)
        RaceDayPoints['TiePoints'] = 0
        if AllTotals['Winner'] > 1:
            #print("break at 2nd place")
            #print(AllTotals)
            #kkkkkkkkkkkkkkkk
            RaceDayPoints['TiePoints'] = RaceDayPoints['Points'] + RaceDayPoints['Winner'] * RaceDayPoints['nWins']
            RaceDayPoints['TiePoints'] = RaceDayPoints['TiePoints'] + RaceDayPoints['Winner'] * RaceDayPoints['nPlaces']
            MaxPoints = RaceDayPoints.max(axis=0)
            RaceDayPoints['isWinner'] = RaceDayPoints['TiePoints'] == MaxPoints['TiePoints']
            RaceDayPoints['Winner'] = RaceDayPoints['isWinner'].astype(int)
            #check for ties and break them with number of shows.
            AllTotals = RaceDayPoints.sum(axis=0)
            #print(AllTotals)
            #print(RaceDayPoints)
            RaceDayPoints['TiePoints'] = 0
            #kkkkkkkkkkkkkkkk
            
            if AllTotals['Winner'] > 1:
                #print("break at 3rd place")
                #print(RaceDayPoints)
                #print(AllTotals)
                #kkkkkkkkkkkkkkkkkkkkkkkkkk
                RaceDayPoints['TiePoints'] = RaceDayPoints['Points'] + RaceDayPoints['Winner'] * RaceDayPoints['nWins']
                RaceDayPoints['TiePoints'] = RaceDayPoints['TiePoints'] + RaceDayPoints['Winner'] * RaceDayPoints['nPlaces']
                RaceDayPoints['TiePoints'] = RaceDayPoints['TiePoints'] + RaceDayPoints['Winner'] * RaceDayPoints['nShows']
                MaxPoints = RaceDayPoints.max(axis=0)
                RaceDayPoints['isWinner'] = RaceDayPoints['TiePoints'] == MaxPoints['TiePoints']
                RaceDayPoints['Winner'] = RaceDayPoints['isWinner'].astype(int)
                #the jockey club now breaks ties at 4th place.  we will not, as that
                #requires a superfecta model to get 4th place (instead of our trifecta model).
                AllTotals = RaceDayPoints.sum(axis=0)
                #print(RaceDayPoints)
                #print(AllTotals)
                #kkkkkkkkkkkkkkk
                #### would break ties at 4th place here.
                if AllTotals['Winner'] > 1: 
                    nUnbrokenTies = nUnbrokenTies + 1
                    #kkkkkkkkkkkkkkkk
            
            
    #need these to resolve ties... don't need for total monte carlo results
    RaceDayPoints.drop(['nWins','nPlaces','nShows','TiePoints'], axis=1, inplace=True)
    #print(RaceDayPoints)
    

    SimJockeyPoints = SimJockeyPoints.merge(RaceDayPoints,on='JockeyNumber', how='inner')
    
    
    #SimJockeyPoints['isWinner'] = SimJockeyPoints['Points'] == MaxPoints['Points']
    #SimJockeyPoints['Winner'] = SimJockeyPoints['isWinner'].astype(int)
    SimJockeyPoints['TotalWins'] = SimJockeyPoints['TotalWins'] + SimJockeyPoints['Winner']
    # 'JockeyPoints' are the actual points the jockey has so far (for betting during the race day)
    # Points and TotalPoints are the simulated total points on the races that we're simulating on.
    SimJockeyPoints['TotalPoints'] = SimJockeyPoints['TotalPoints'] + SimJockeyPoints['Points']  + SimJockeyPoints['JockeyPoints']
    SimJockeyPoints['nRuns'] = SimJockeyPoints['nRuns'] + 1
    #print(RaceDayPoints1)
    #print(RaceDayPoints2)
    #print(RaceDayPoints3)
    #print(SimJockeyPoints)
    #kkkkkkkkkkkk

    SimJockeyPoints.drop(['Points','isWinner','Winner'],axis=1,inplace=True)



#end iter
print("unbroken ties")
print(nUnbrokenTies)

SimJockeyChallenge = SimJockeyPoints.copy(deep=True)
SimJockeyChallenge['ExpectedPoints'] = SimJockeyChallenge['TotalPoints'] / SimJockeyChallenge['nRuns']
SimJockeyChallenge['RawChance'] = 100 * SimJockeyChallenge['TotalWins'] / SimJockeyChallenge['nRuns'] 
#this algorithm doesn't take into account ties for the jockey challenge for the day 
#(ties in points are broken by more winners, more places, more shows, etc.)
AllTotals = SimJockeyChallenge.sum(axis=0)
print(AllTotals)
SimJockeyChallenge['Chance'] = 100 * SimJockeyChallenge['RawChance'] / AllTotals['RawChance']
SimJockeyChallenge['Pay'] = 100 / SimJockeyChallenge['Chance']
#some times we get inf for the Pay.
#use 9999 ~= nSims = 10000
SimJockeyChallenge.replace([np.inf],9999, inplace=True)


print(SimJockeyChallenge)


SimJockeyChallenge.to_csv(path_to_directory + 'SimJockeyChallenge' + '.csv', index=False)


