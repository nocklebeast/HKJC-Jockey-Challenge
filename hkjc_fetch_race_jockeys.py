#see this example
# https://learn.circuit.rocks/how-to-extract-data-from-webpages-using-python
# info on requests package: https://docs.python-requests.org/en/master/user/quickstart/#cookies

# hkjc specific example found on the web!  https://python-forum.io/thread-16837.html
# https://selenium-python.readthedocs.io/installation.html

#need to install gecko driver (for firefox) for windows.
# http://www.learningaboutelectronics.com/Articles/How-to-install-geckodriver-Python-windows.php

#from tracemalloc import stop
#import urllib.request as ul
from calendar import different_locale
from tracemalloc import stop
from bs4 import BeautifulSoup as soup
import numpy as np
import pandas as pd
import json
import os
import requests
import time 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from hkjc_functions import read_race_parameters

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
path_to_raw = path_to_directory + '\\odds_raw\\'


#jType = 'jkc'
#tType = 'tnc'

firstRace, lastRace, sDate, sVenue, jType = read_race_parameters(path_to_raw + 'race_parameters.txt')

#https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=en&date=2022-05-15&venue=ST&raceno=1

#use these headless options to not have the browser pop up.
WebDriverOptions = Options()
#WebDriverOptions.headless = True

#by hand press the race buttons.
browser = webdriver.Firefox(options=WebDriverOptions)
#browser = webdriver.Firefox()
#browser = webdriver.Chrome(options=WebDriverOptions)

#later, merge race entry(jockeys) with jockey selections
#get ALL jockey selections to get names and points of all the other jockeys.
JockeySelections = pd.read_csv(path_to_directory + 'AllJockeySelections' + '.csv')
print(JockeySelections)
if JockeySelections[jType+'OtherNumber'][0] == 0:
    OtherNumberJockey = 0
else:
    dfOtherNumberJockey = JockeySelections[JockeySelections[jType+'Name'] == 'Others']
    OtherNumberJockey = dfOtherNumberJockey[jType+'OtherNumber'].loc[dfOtherNumberJockey.index[0]]
print(OtherNumberJockey)

"""
#sometimes no trainer challenge
try:
    TrainerSelections = pd.read_csv(path_to_directory + 'AllTrainerSelections' + '.csv')
    print(TrainerSelections)
    dfOtherNumberTrainer = TrainerSelections[TrainerSelections[tType+'Name'] == 'Others']
    OtherNumberTrainer = dfOtherNumberTrainer[tType+'OtherNumber'].loc[dfOtherNumberTrainer.index[0]]
    isTrainerExist = True
except :
    OtherNumberTrainer = 0
    isTrainerExist = False
print(OtherNumberTrainer)
"""

for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)

    base_url = 'https://bet.hkjc.com/racing/pages/odds_wp.aspx'
    #?lang=en&date=2022-05-15&venue=ST&raceno=1'

    sParams = 'lang=' + 'en' + '&date=' + sDate + '&venue=' + sVenue + '@raceno=' + sRace
    race_url = base_url + '?' + sParams
    print(race_url)

    browser.get(race_url)
    #browser.get(race_url)
    #time.sleep(13)
    time.sleep(15)
    txtPage = browser.page_source

    #write text file of the string for later processing.
    path_to_file = path_to_raw  + '\\jky_race_' + sRace  + '.txt'

    #write page source for later (optional) processing.
    #use encoding='utf-8' when writing chinese characters.
    with open(path_to_file,'w',encoding='utf-8') as oddsFile:
        oddsFile.write(txtPage)
        oddsFile.close()

    #print(txtPage)
    
    #same as above.
    #pageSource = browser.find_element_by_xpath("//*").get_attribute("outerHTML")    
    #print(pageSource)

    iPos = txtPage.find("normalRunnerList")
    jPos = txtPage.find("{",iPos+1)
    iPos = jPos

    jPos = txtPage.find("}]",iPos+1)


    #everything between (and including) { } for ALL the horses
    #sRunnerList = txtPage[iPos : jPos+1]

    #remove first {
    sRunnerList = txtPage[iPos+1 : jPos+1]
    #let's get rid of all the double quotes " 
    sRunnerList = sRunnerList.replace('"','')
    #print(sRunnerList)
    # is there an easy way to json to data frame?
    # need to map horse number "num" with "jkcName"
    lRunners = sRunnerList.split("},{")
    print(lRunners[3])

    aRunners = np.array(lRunners)
    #print(aRunners)
    dfRunners = pd.DataFrame(aRunners,columns=['RaceEntry'], dtype='string')
    #print(dfRunners)

    dfRunners['lRaceEntry'] = dfRunners['RaceEntry'].str.split(',')
    #print(dfRunners)

    df2 = pd.DataFrame(dfRunners['lRaceEntry'].to_list())
    #print(df2)
    #keep 0 = horseno, 9 = jockey name, 13 = trainer name.
    df2.drop([1,2,3,4,5,6,7,8,10,11,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29], axis=1, inplace=True)
    #print(df2)

    dfHorse =  pd.DataFrame( df2[0].str.split(':'))
    dfJockey = pd.DataFrame( df2[9].str.split(':'))
    dfTrainer = pd.DataFrame(df2[13].str.split(':'))
    #print(dfHorse)
    #print(dfJockey)


    dfH2 = pd.DataFrame(dfHorse[0].to_list())
    dfJ2 = pd.DataFrame(dfJockey[9].to_list())
    dfT2 = pd.DataFrame(dfTrainer[13].to_list())
    #print(dfH2)
    #print(dfJ2)
    #print(dfT2)

    dfRaceEntry = pd.DataFrame()
    dfRaceEntry['horseno'] = dfH2[1]
    dfRaceEntry['Race'] = iRace
    if jType == 'jkc':
        dfRaceEntry[jType+'Name'] = dfJ2[1]
    else:
        dfRaceEntry[jType+'Name'] = dfT2[1]

    dfRaceEntry = dfRaceEntry.reindex(columns=[ 'Race', 'horseno', jType+'Name'] )
    dfRaceEntry['horseno'] = dfRaceEntry['horseno'].astype(int)
    print(dfRaceEntry)

    #merge in jockey selections
    #be sure to not throw away "other jockeys"
    #left: use only keys from left frame, similar to a SQL left outer join; preserve key order.
    print(dfRaceEntry)
    print(JockeySelections)
    RaceEntryA = dfRaceEntry.merge(JockeySelections, on=jType+'Name', how='left')
    print(RaceEntryA)

    RaceEntryA[jType+'Number'].fillna(OtherNumberJockey,inplace=True)
    #deal with "other"
    RaceEntryA[jType+'Number'] = RaceEntryA[jType+'Number'].astype(int)
    RaceEntryA.drop([jType+'OtherNumber'], axis=1, inplace=True)
    print(RaceEntryA) 

    """  let's have jockey only for now.
    if isTrainerExist :
        #merge in trainer selections
        #be sure to not throw away "other trainers"
        #left: use only keys from left frame, similar to a SQL left outer join; preserve key order.
        print(TrainerSelections)
        RaceEntry = RaceEntryA.merge(TrainerSelections, on=tType+'Name', how='left')
        print(RaceEntry)

        RaceEntry[tType+'Number'].fillna(OtherNumberJockey,inplace=True)
        #deal with "other"
        RaceEntry[tType+'Number'] = RaceEntry[tType+'Number'].astype(int)
        RaceEntry.drop([tType+'OtherNumber'], axis=1, inplace=True)
        print(RaceEntry) 
    else:
        RaceEntry= RaceEntryA.copy(deep=True)
    """
    RaceEntry= RaceEntryA.copy(deep=True)
    RaceEntry.to_csv(path_to_directory + 'RaceEntry' + sRace + '.csv', index=False)

    #don't need the jockey names for jockey challenge, let's drop them. (just needed for merging selections and horseno)
    #perhaps should keep jockey names here?
    RaceEntry.drop([jType+'Name'],axis=1,inplace=True)

    #create an exacta grid jockey race entries, then keep x != y.
    xyRace = pd.merge(RaceEntry,RaceEntry,how='cross')
    xyRace = xyRace[xyRace.horseno_x != xyRace.horseno_y]
    xyRace.drop(['Race_y'],axis=1,inplace=True)
    xyRace.rename({'Race':'Race_x'}, axis=1)

    xyRace = xyRace.reindex(columns=['horseno_x','horseno_y', \
                            jType+'Number_x', jType+'Number_y' ] )
                            #tType+'Number_x', tType+'Number_y' ] )
    xyRace.sort_values(by=['horseno_x','horseno_y'], inplace=True)
    #print(xyRace.head())

    #create trifecta grid of jockey numbers.
    xyzRace = pd.merge(xyRace,RaceEntry,how='cross')
    xyzRace = xyzRace[xyzRace.horseno_x != xyzRace.horseno]
    xyzRace = xyzRace[xyzRace.horseno_y != xyzRace.horseno]

    xyzRace.rename(columns={'horseno':'horseno_z', jType+'Number':jType+'Number_z' }, inplace=True)
    """
    if isTrainerExist:
        xyzRace.rename(columns={tType+'Number':tType+'Number_z' }, inplace=True)
        reindexColumns = ['horseno_x','horseno_y','horseno_z', \
                                        jType+'Number_x', jType+'Number_y', jType+'Number_z' , \
                                        tType+'Number_x', tType+'Number_y', tType+'Number_z'  ]
    else:
    """
    reindexColumns = ['horseno_x','horseno_y','horseno_z', \
                                        jType+'Number_x', jType+'Number_y', jType+'Number_z'  ]
    xyzRace = xyzRace.reindex(columns=reindexColumns)

    xyzRace.sort_values(by=['horseno_x','horseno_y','horseno_z'], inplace=True)

    print(xyzRace)
    xyzRace.to_csv(path_to_directory + 'xyzRace' + sRace + '.csv', index=False)
    
#end of for loop on iRace

browser.close
