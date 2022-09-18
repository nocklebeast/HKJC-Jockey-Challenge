###################################################
############## jockey challgenge monte carlo
##################################################
#run after getting the tierce investments.  

from lib2to3.pgen2.literals import simple_escapes
from tokenize import Single
import pandas as pd
import numpy as np
import os 

pd.set_option('display.max_rows',None)

np.random.seed(10)

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
path_to_file = path_to_directory + 'AllJockeySelections' + '.csv'
TodaysJockeySelections = pd.read_csv(path_to_file)
OtherNumber = TodaysJockeySelections['OtherNumber'][0]
TodaysJockeySelections.drop('OtherNumber',axis=1,inplace=True)
TodaysJockeySelections = TodaysJockeySelections.loc[TodaysJockeySelections["jockeyName"] != 'Others' ]
TodaysJockeySelections.sort_values(by=['JockeyNumber','jockeyName'],inplace=True)
TodaysJockeySelections.reindex

SimJockeyPoints = TodaysJockeySelections.copy(deep=True)
SimJockeyPoints['TotalPoints'] = 0
SimJockeyPoints['TotalWins'] = 0
SimJockeyPoints['nRuns'] = 0
nUnbrokenTies = 0
print(SimJockeyPoints)

#JockeyTierce for all races of the day.... concat all the JockeyTierces for individual races.
JockeyTierceChance = pd.DataFrame()

#construct jockey challenge matrix based on all races for the day.
#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    #print(sRace)

    path_to_file = path_to_directory + 'JockeyTierce' + sRace + '.csv'
    tempJockeyTierce = pd.read_csv(path_to_file)  

    JockeyTierceChance = pd.concat([JockeyTierceChance, tempJockeyTierce], ignore_index=True )
    #print(JockeyTierceChance.head())
#end iRace
#JockeyTierceChance.sort_values(by=['Race','Jx','Jy','Jz'])
JockeyTierceChance.to_csv(path_to_directory + 'JockeyTierceChance' + '.csv', index=False)

# let's not do the weighted select by hand.
#JockeyTierceChance['CumTierceCh'] = JockeyTierceChance[['Race','TierceCh']].groupby('Race').cumsum()
# default is to shift one down with NaN as the 1st thing of the group.
#JockeyTierceChance['ShiftTierceCh'] = JockeyTierceChance.groupby('Race')['CumTierceCh'].shift()
#JockeyTierceChance.fillna(0,inplace=True)
#
# Note, sorting the array (but keeping the random seed constant) slightly alters the results.
#JockeyTierceChance.sort_values(by=['Race','TierceCh'], inplace=True)
# select with weights below must be implemented similarly as calculating a cumulative chance above
# (because I got the same result as above method as select with weights methods with the same random seed)

#run a race day's simulation nSims times.
#nSims = 10007
#nSims = 5003
#nSims = 2003
nSims = 1009

iNextPrint = 0
nProgressPrints = 20
for iter in range(nSims): 
    if int(iter/nSims*nProgressPrints) >= iNextPrint:
        iNextPrint = iNextPrint + 1
        print(SimJockeyPoints)
        print("pctSims = " + str(iter/nSims) )

    ###################### throw the darts at each race (groupby Race) with weights set as the tierce chance.############
    # using 'TierceCh" as weight.... trifecta horse combos with higher chances are more likely to be sampled.

    JockeyTierce = JockeyTierceChance.copy(deep=True)
    # select a single (n=1) winning trifecta combination for each race.
    simulated_winners = JockeyTierce.groupby('Race').sample(n=1,weights='TierceCh')
    simulated_winners['bWinner'] = 1
    #just keep the winner column, then merge back into JockeyTierceChance.
    simulated_winners = simulated_winners['bWinner']
    #left join winners onto JockeyTierceChance
    JockeyTierce = pd.merge(JockeyTierce,simulated_winners, left_index=True, right_index=True, how='left')
    JockeyTierce['bWinner'].fillna(0,inplace=True)
    JockeyTierce['bWinner'] = JockeyTierce['bWinner'].astype(int)
    #print(JockeyTierce.head())

    # we need to score each individual jockey by their names (not by jockey number)
    #  each individual "other" jockey must be score separate from the "other" jockeys.
    # instead of groupby.sum on jockey number we groupby.sum on jockey name below.

    Points = JockeyTierce.copy(deep=True)
    Points.drop(['Race','Hx','Hy','Hz','TierceCh'], axis=1, inplace=True)
    #print(Points.head())
    
    Points1 = Points.copy(deep=True)
    Points1['Points1'] = 12 * Points['bWinner']
    Points1.drop(['Jy','Jz'], axis=1, inplace=True)
    Points1.drop(['JNy','JNz'], axis=1, inplace=True)
    Points1.rename(columns = {'Jx':'JockeyNumber'}, inplace=True)
    # group on name not number
    Points1.drop('JockeyNumber', axis=1, inplace=True)
    Points1.rename(columns = {'JNx':'jockeyName'}, inplace=True)
    RaceDayPoints1 = Points1.groupby(['jockeyName']).sum().reset_index()
    RaceDayPoints1.rename(columns = {'bWinner':'nWins'}, inplace=True)
    #print(RaceDayPoints1)

    Points2 = Points.copy(deep=True)
    Points2['Points2'] = 6 * Points['bWinner']
    Points2.drop(['Jx','Jz'], axis=1, inplace=True)
    Points2.drop(['JNx','JNz'], axis=1, inplace=True)
    Points2.rename(columns = {'Jy':'JockeyNumber'}, inplace=True)
    Points2.drop('JockeyNumber', axis=1, inplace=True)
    #print(Points2.tail())
    Points2.rename(columns = {'JNy':'jockeyName'}, inplace=True)
    RaceDayPoints2 = Points2.groupby(['jockeyName']).sum().reset_index()
    RaceDayPoints2.rename(columns = {'bWinner':'nPlaces'}, inplace=True)
    #print(RaceDayPoints2)

    Points3 = Points.copy(deep=True)
    Points3['Points3'] = 4 * Points['bWinner']
    Points3.drop(['Jx','Jy'], axis=1, inplace=True)
    Points3.drop(['JNx','JNy'], axis=1, inplace=True)
    Points3.rename(columns = {'Jz':'JockeyNumber'}, inplace=True)
    Points3.drop('JockeyNumber', axis=1, inplace=True)
    Points3.rename(columns = {'JNz':'jockeyName'}, inplace=True)
    #print(Points3.tail())
    RaceDayPoints3 = Points3.groupby(['jockeyName']).sum().reset_index()
    RaceDayPoints3.rename(columns = {'bWinner':'nShows'}, inplace=True)
    #print(RaceDayPoints3)
    
    #merge on jockey name, not number.
    #also merge in previous points in SimJockeyPoints
    mergeWithRaceDayPoints = SimJockeyPoints.copy(deep=True)
    mergeWithRaceDayPoints.drop(columns=['JockeyNumber','CurrentOdds','RemainingRides','TotalPoints','TotalWins','nRuns'],inplace=True)
    RaceDayPoints = mergeWithRaceDayPoints.merge(RaceDayPoints1.merge(RaceDayPoints2.merge(RaceDayPoints3, 
                    on='jockeyName', how='inner'), 
                    on='jockeyName', how='inner'),
                    on='jockeyName', how='inner')
    #RaceDayPoints = RaceDayPoints.merge(SimJockeyPoints,on='jockeyName',how='inner')
    #add total simulated points and previous points from the actual race day.
    RaceDayPoints['Points'] = RaceDayPoints['Points1'] + RaceDayPoints['Points2'] + RaceDayPoints['Points3'] + RaceDayPoints['JockeyPoints']
    #SimJockeyPoints contains the points for each jockey from previous races 
    # (at some point let's include number of previous 1st,2nd,3rd,4th in that file too)
    #print(RaceDayPoints)
    RaceDayPoints.drop(['JockeyPoints'], axis=1, inplace=True)
    RaceDayPoints.drop(['Points1','Points2','Points3'], axis=1, inplace=True)
    #print(RaceDayPoints)
    
    MaxPoints = RaceDayPoints.max(axis=0)
    #print(RaceDayPoints)
    #print(MaxPoints)
    RaceDayPoints['isWinner'] = RaceDayPoints['Points'] == MaxPoints['Points']
    RaceDayPoints['Winner'] = RaceDayPoints['isWinner'].astype(int)
    RaceDayPoints['TiePoints'] = 0

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
    
    #merge on name, not number. we'll continue to keep track of average points and wins for 
    #each individual (other) jockey... and then sum over all the wins and points for each
    #winning individual (other) jockey.
    SimJockeyPoints = SimJockeyPoints.merge(RaceDayPoints,on='jockeyName', how='inner')
    #print(SimJockeyPoints)
    
    #SimJockeyPoints['isWinner'] = SimJockeyPoints['Points'] == MaxPoints['Points']
    #SimJockeyPoints['Winner'] = SimJockeyPoints['isWinner'].astype(int)
    SimJockeyPoints['TotalWins'] = SimJockeyPoints['TotalWins'] + SimJockeyPoints['Winner']
    # 'JockeyPoints' are the actual points the jockey has so far (for betting during the race day)
    # Points and TotalPoints are the simulated total points on the races that we're simulating on.
    # we already added the previous points ("JockeyPoints") in the simulation... don't add them a 2nd time here.
    SimJockeyPoints['TotalPoints'] = SimJockeyPoints['TotalPoints'] + SimJockeyPoints['Points']  #+ SimJockeyPoints['JockeyPoints']
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

#split off the others from the named jockeys
#then add up points and wins for the other jockeys and tack back onto named jockeys that one 'other' row

SimNamedJockeys = SimJockeyPoints.copy(deep=True)
SimNamedJockeys = SimNamedJockeys.loc[ SimJockeyPoints['JockeyNumber'] != OtherNumber]
SimNamedJockeys['ExpectedPoints'] = SimNamedJockeys['TotalPoints'] / SimNamedJockeys['nRuns']
SimNamedJockeys['RawChance'] = 100 * SimNamedJockeys['TotalWins'] / SimNamedJockeys['nRuns'] 
#print(SimNamedJockeys)

SimOtherJockeys = SimJockeyPoints.copy(deep=True)
SimOtherJockeys = SimOtherJockeys.loc[ SimJockeyPoints['JockeyNumber'] == OtherNumber]
SimOtherJockeys['ExpectedPoints'] = SimOtherJockeys['TotalPoints'] / SimOtherJockeys['nRuns']
SimOtherJockeys['RawChance'] = 100 * SimOtherJockeys['TotalWins'] / SimOtherJockeys['nRuns'] 
#print(SimOtherJockeys)

OtherJockey = SimOtherJockeys.copy(deep=True)
OtherJockeySum = OtherJockey.sum(axis=0)
OtherJockeyMax = OtherJockey.max(axis=0)
SingleOtherJockey = OtherJockeyMax.copy(deep=True)
SingleOtherJockey['jockeyName'] = 'Other'
SingleOtherJockey['RawChance'] = OtherJockeySum['RawChance']

#print(type(SingleOtherJockey)) #series
#print(SingleOtherJockey.keys())

#convert the series into a dictionary and then into a dataframe 
#the dataframe conversion is expecting a dictionary of LISTS  (key:value=a list)
#use index=[0] to convert the values into a list 
#see https://www.geeksforgeeks.org/how-to-fix-if-using-all-scalar-values-you-must-pass-an-index/
dctSingleOtherJockey = SingleOtherJockey.to_dict()
#print(dctSingleOtherJockey)
dfSingleOtherJockey = pd.DataFrame(dctSingleOtherJockey, index=[0])
print(dfSingleOtherJockey)


SimJockeyChallenge = SimNamedJockeys.copy(deep=True)
print("before")
print(SimJockeyChallenge)

#add the one "other" jockey row.
#SimJockeyChallenge = pd.concat([SimJockeyChallenge, dfSingleOther], ignore_index=True )
#SimJockeyChallenge = SimJockeyChallenge.append(pd.DataFrame(SingleOtherJockey))
SimJockeyChallenge = pd.concat([SimJockeyChallenge, dfSingleOtherJockey], axis=0)

print("raw simjockey challgenge")
print(SimJockeyChallenge)


#re-normalize.
#this algorithm doesn't take into account ties for the jockey challenge for the day 
#(ties in points are broken by more winners, more places, more shows, more 4ths.)
AllTotals = SimJockeyChallenge.sum(axis=0)
print(AllTotals)
SimJockeyChallenge['Chance'] = 100 * SimJockeyChallenge['RawChance'] / AllTotals['RawChance']
SimJockeyChallenge['Pay'] = 100 / SimJockeyChallenge['Chance']
#some times we get inf for the Pay.
#use 9999 ~= nSims = 10000
SimJockeyChallenge.replace([np.inf],9999, inplace=True)


print(SimJockeyChallenge)
SimJockeyChallenge.to_csv(path_to_directory + 'SimJockeyChallenge' + '.csv', index=False)
SumJKC = SimJockeyChallenge.sum(axis=0)
print(SumJKC)

