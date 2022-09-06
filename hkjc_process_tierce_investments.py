

from xml.etree.ElementTree import TreeBuilder
import pandas as pd
import numpy as np
import os

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

sType = 'tceinv'

#let's process races within the range set by first and last race.
for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)

    path_to_file = path_to_directory + sType + sRace + '.txt'
    print(path_to_file)

    with open(path_to_file,'r') as oddsFile:
        sOut = oddsFile.read()
    oddsFile.close()
    print(sOut)

    #get update time
    iPos = sOut.find("OUT",1)
    sUpdateTime = sOut[iPos+6:iPos+12]
    print(sUpdateTime)

    #get tierce investments string.
    iPos = sOut.find(";",1)
    jPos = sOut.find('"}', iPos+1)
    sInvestments = sOut[iPos+1 : jPos]
    print(sInvestments)

    #get investments for each position, 1, 2, 3.
    #or each horse, split on ";"
    lHorses = sInvestments.split(";")
    print(lHorses)


    TINVListOfFields = []
    for item in lHorses :
        print(item)
        splitItem = item.split("|") 
        #switch scratched horses "SCR" to "0" on the odds.
        #splitItem[1] = splitItem[1].replace("SCR","0")
        print(splitItem)
        #split investments.
        tinv1 = splitItem[1].split("=")
        tinv2 = splitItem[2].split("=")
        tinv3 = splitItem[3].split("=")
        tinv1[1] = tinv1[1].replace("SCR","0")
        tinv2[1] = tinv2[1].replace("SCR","0")
        tinv3[1] = tinv3[1].replace("SCR","0")
        #how to replace a string with a list with split in a dataframe
        #placeListOfFields.append( [ int(splitItem[0]), (tinv1), (tinv2), (tinv3)   ] )
        TINVListOfFields.append( [ int(splitItem[0]), int(tinv1[1]) , int(tinv2[1]), int(tinv3[1])   ] )
    #print(placeListOfFields)
    TierceInvestments = pd.DataFrame(TINVListOfFields, columns=['horseno', 'TINV1', 'TINV2', 'TINV3' ])
    #let's keep rows where investment is greater than zero.
    TierceInvestments = TierceInvestments[TierceInvestments['TINV1'] > 0]
    TierceInvestments = TierceInvestments[TierceInvestments['TINV2'] > 0]
    TierceInvestments = TierceInvestments[TierceInvestments['TINV2'] > 0]

    #compute chances
    AllTotals = TierceInvestments.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
    print(AllTotals)

    TierceInvestments['T1Ch'] = TierceInvestments['TINV1'] / AllTotals['TINV1']
    TierceInvestments['T2Ch'] = TierceInvestments['TINV2'] / AllTotals['TINV2']
    TierceInvestments['T3Ch'] = TierceInvestments['TINV3'] / AllTotals['TINV3']
    TierceInvestments['Race'] = iRace

    TierceInvestments.to_csv(path_to_directory + 'TierceInvestments' + sRace + '.csv', index=False)
    print(TierceInvestments)
    
    TierceChance = TierceInvestments.copy(deep=True)
    TierceChance.drop(['TINV1', 'TINV2', 'TINV3'], axis=1, inplace=True)

    print(TierceChance)
    TierceChance.to_csv(path_to_directory + 'TierceChance' + sRace + '.csv', index=False)
    

    #create an exacta grid of the win Chance and place chances, with cross merge, then keep x != y.
    xyTierce = pd.merge(TierceChance,TierceChance,how='cross')
    xyTierce = xyTierce[xyTierce.horseno_x != xyTierce.horseno_y]
    xyTierce = xyTierce[xyTierce.Race_x == xyTierce.Race_y]
    xyTierce.drop('Race_y',axis=1,inplace=True)
    xyTierce.rename(columns = {'Race_x':'Race'}, inplace = True)
    xyTierce = xyTierce.reindex(columns=['Race','horseno_x','horseno_y', 'T1Ch_x', 'T1Ch_y', 'T2Ch_x', 'T2Ch_y', 'T3Ch_x', 'T3Ch_y'] )
    xyTierce.sort_values(by=['Race','horseno_x','horseno_y'], inplace=True)
    print(xyTierce.head())
    
    #xyTierce.to_csv(path_to_directory + 'xyWinChance' + sRace + '.csv', index=False)
    
    xyzTierce = pd.merge(xyTierce,TierceChance,how='cross')
    xyzTierce = xyzTierce[xyzTierce.horseno_x != xyzTierce.horseno]
    xyzTierce = xyzTierce[xyzTierce.horseno_y != xyzTierce.horseno]
    xyzTierce = xyzTierce[xyzTierce.Race_x == xyzTierce.Race_y]
    xyzTierce.drop('Race_y',axis=1,inplace=True)
    xyzTierce.rename(columns = {'Race_x':'Race'}, inplace = True)
    xyzTierce.rename(columns={'Race_x':'Race','horseno':'horseno_z', 'T1Ch':'T1Ch_z', 'T2Ch':'T2Ch_z', 'T3Ch': 'T3Ch_z'}, inplace=True)

    #replace T1X = TXYZ123 + TXYZ132 + TXZY123 + TXZY132 
    #gen TXYZ123 = xT1Ch * yT2Ch * zT3Ch / (1-xT2Ch) / (1-xT3Ch-yT3Ch) 
    #gen TXYZ132 = xT1Ch * yT3Ch * zT2Ch / (1-xT3Ch) / (1-xT2Ch-yT2Ch) 
    #gen TXZY123 = xT1Ch * zT2Ch * yT3Ch / (1-xT2Ch) / (1-xT3Ch-zT3Ch) 
    #gen TXZY132 = xT1Ch * zT3Ch * yT2Ch / (1-xT3Ch) / (1-xT2Ch-zT2Ch) 

    #TXYZ1123
    xyzTierce['TierceChance'] = 0
    xyzTierce['TierceChance'] = xyzTierce['TierceChance'] + \
                                xyzTierce.T1Ch_x \
                                * xyzTierce.T2Ch_y \
                                * xyzTierce.T3Ch_z \
                                / (1 - xyzTierce.T2Ch_x) \
                                / (1 - xyzTierce.T3Ch_x - xyzTierce.T3Ch_y)

    #TXYZ132
    xyzTierce['TierceChance'] = xyzTierce['TierceChance'] + \
                                xyzTierce.T1Ch_x \
                                * xyzTierce.T3Ch_y \
                                * xyzTierce.T2Ch_z \
                                / (1 - xyzTierce.T3Ch_x) \
                                / (1 - xyzTierce.T2Ch_x - xyzTierce.T2Ch_y)
    #TXZY123
    xyzTierce['TierceChance'] = xyzTierce['TierceChance'] + \
                                xyzTierce.T1Ch_x \
                                * xyzTierce.T2Ch_z \
                                * xyzTierce.T3Ch_y \
                                / (1 - xyzTierce.T2Ch_x) \
                                / (1 - xyzTierce.T3Ch_x - xyzTierce.T3Ch_z)

    #TXZY132
    xyzTierce['TierceChance'] = xyzTierce['TierceChance'] + \
                                xyzTierce.T1Ch_x \
                                * xyzTierce.T3Ch_z \
                                * xyzTierce.T2Ch_y \
                                / (1 - xyzTierce.T3Ch_x) \
                                / (1 - xyzTierce.T2Ch_x - xyzTierce.T2Ch_z)

    xyzTierce['TierceChance'] = xyzTierce['TierceChance'] / 4

    #print(xyzTierce.head())
    #kkkkkkkkkkkkkkkk
    xyzTierce['TierceChanceX'] = xyzTierce.T1Ch_x \
                                * xyzTierce.T2Ch_y \
                                * xyzTierce.T3Ch_z  
    #check normalization of Tiercechance
    AllTotals = xyzTierce.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
    print(AllTotals)
    #renormalize alt tierce chance
    xyzTierce['TierceChanceX'] = xyzTierce['TierceChanceX'] / AllTotals['TierceChanceX']

    xyzTierce['Pay'] = (1-cTakeout) / xyzTierce['TierceChance']
    xyzTierce['Pay'] = xyzTierce['Pay'].apply(lambda x: round(x, 1))

    xyzTierce['PayX'] = (1-cTakeout) / xyzTierce['TierceChanceX']
    xyzTierce['PayX'] = xyzTierce['PayX'].apply(lambda x: round(x, 1))



    xyzTierce = xyzTierce.reindex(columns=['Race','horseno_x','horseno_y','horseno_z','TierceChance', 'Pay', \
                                            'TierceChanceX', 'PayX', \
                                            'T1Ch_x', 'T1Ch_y', 'T1Ch_z', \
                                            'T2Ch_x', 'T2Ch_y', 'T2Ch_z', \
                                        'T3Ch_x', 'T3Ch_y', 'T3Ch_z'])
    #print(xyzTierce)
    print(xyzTierce.head())


    xyzTierce.to_csv(path_to_directory + 'xyzTierce' + sRace + '.csv', index=False)



    #let's collapse our tierce investment chances to see if 
    #we can reproduce the investment chances we started with.

    xyzTemp = xyzTierce.copy(deep=True)
    xyzTemp.drop(['Pay','PayX','T1Ch_x', 'T1Ch_y', 'T1Ch_z', 'T2Ch_x', 'T2Ch_y', 'T2Ch_z', 'T3Ch_x', 'T3Ch_y', 'T3Ch_z'],axis=1,inplace=True)

    print(xyzTemp.head())
    #xTemp = xyzTemp.groupby('horseno_x').sum(['TierceChance','TierceChanceX']).reset_index()
    xTemp = xyzTemp.groupby(['Race','horseno_x']).sum().reset_index()
    xTemp.drop(['horseno_y', 'horseno_z'],axis=1,inplace=True)

    yTemp = xyzTemp.groupby(['Race','horseno_y']).sum().reset_index()
    #yTemp.drop(['horseno_y', 'horseno_x'],axis=1,inplace=True)

    zTemp = xyzTemp.groupby(['Race','horseno_z']).sum().reset_index()
    print(xTemp)
    print(yTemp)
    print(zTemp)

    #let's NOT merge on trifecta (model) chance.
    #path_to_file = path_to_directory + 'TrifectaChance' + sRace + '.csv' 
    #TrifectaModelChance = pd.read_csv(path_to_file) 
    #TrifectaModelChance.drop(['xyExacta', 'xzExacta', 'yzExacta','TriChLn','ModelPay'], axis=1, inplace=True)
    #print(TrifectaModelChance.head())

    path_to_file = path_to_directory + 'xyzTierce' + sRace + '.csv' 
    TierceInvestmentChance = pd.read_csv(path_to_file) 
    TierceInvestmentChance.drop(['Pay', 'TierceChanceX', 'PayX','T1Ch_x','T1Ch_y','T1Ch_z', \
                                'T2Ch_x','T2Ch_y','T2Ch_z', 'T3Ch_x','T3Ch_y','T3Ch_z' \
                                    ], axis=1, inplace=True)
    print(TierceInvestmentChance.head())

    #JockeyTierce = pd.merge(TrifectaModelChance,TierceInvestmentChance, \
    #                        on=['Race', 'horseno_x','horseno_y','horseno_z'], how='inner')

    JockeyTierce = TierceInvestmentChance.copy(deep=True)

    #JockeyTierce['Equity'] = JockeyTierce['TriCh'] / JockeyTierce['TierceChance'] - 1
    print(JockeyTierce.head())
    AllTotals = JockeyTierce.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
    print(AllTotals)
    #JockeyTierce.drop(columns='Equity',inplace=True)
    JockeyTierce.rename(columns={'TierceChance':'TierceCh'}, inplace=True)

    #now we'll want to merge in the jockey selction numbers (x y and z)
    path_to_file = path_to_directory + 'RaceEntry' + sRace + '.csv' 
    JockeySelectionsRace = pd.read_csv(path_to_file) 
    print(JockeySelectionsRace)

    xJockey = JockeySelectionsRace.copy(deep=True)
    xJockey.rename(columns={'horseno':'horseno_x','JockeyNumber':'jockeyno_x'}, inplace=True)
    xJockey.drop(columns='jockeyName',inplace=True)
    #print(xJockey)
    JockeyTierce = JockeyTierce.merge(xJockey,on=['Race','horseno_x'], how='inner')
    #print(JockeyTierce.head())

    yJockey = JockeySelectionsRace.copy(deep=True)
    yJockey.rename(columns={'horseno':'horseno_y','JockeyNumber':'jockeyno_y'}, inplace=True)
    yJockey.drop(columns='jockeyName',inplace=True)
    #print(xJockey)
    JockeyTierce = JockeyTierce.merge(yJockey,on=['Race','horseno_y'], how='inner')
    #print(JockeyTierce.head())
    
    zJockey = JockeySelectionsRace.copy(deep=True)
    zJockey.rename(columns={'horseno':'horseno_z','JockeyNumber':'jockeyno_z'}, inplace=True)
    zJockey.drop(columns='jockeyName',inplace=True)
    #print(xJockey)
    JockeyTierce = JockeyTierce.merge(zJockey,on=['Race','horseno_z'], how='inner')

    JockeyTierce = JockeyTierce.reindex(columns=['Race','horseno_x','horseno_y', 'horseno_z', \
                                        'jockeyno_x','jockeyno_y', 'jockeyno_z', \
                                        'TriCh', 'TierceCh'])

    JockeyTierce.rename(columns={'horseno_x':'Hx','jockeyno_x':'Jx', \
                                'horseno_y':'Hy','jockeyno_y':'Jy', \
                                'horseno_z':'Hz','jockeyno_z':'Jz'}, inplace=True )
    JockeyTierce.to_csv(path_to_directory + 'JockeyTierce' + sRace + '.csv', index=False)
    print(JockeyTierce.head())

#end Race

