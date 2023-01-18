
import pandas as pd
import os
import shutil
import numpy as np
import itertools

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as soup
import json

#import requests
import time 

def read_race_parameters(path_to_file: str) :
    
    RaceParameters = pd.read_csv(path_to_file)  
    print(RaceParameters)

    sDate = RaceParameters.at[0,'sDate']
    firstRace = int(RaceParameters.at[0,'firstRace'])
    lastRace = int(RaceParameters.at[0,'lastRace'])
    sVenue = RaceParameters.at[0,'sVenue']
    jType = RaceParameters['ChallengeType'][0]

    """
    print(sDate)
    print(firstRace)
    print(lastRace)
    print(sVenue)
    print(jType)
    """
    return firstRace, lastRace, sDate, sVenue, jType

def renormalize_column(df: pd.DataFrame, sColumn: str, newColumn=''):
    AllTotals = df.sum(axis=0)  #axis=0 gives the sum of all rows of each column in the AllTotals dataframe. axis=1, sums columns for each row
    if len(newColumn) > 0:
        df[newColumn] = df[sColumn] / AllTotals[sColumn]
    else:
        df[sColumn] = df[sColumn] / AllTotals[sColumn]
    #print(df.head())
    
def fetch_odds(RaceNo: int, sDataType: str, sRaceDate: str, sRaceVenue: str,  path_to_write_directory: str) :
    sRaceNo = str(RaceNo)

    base_url = 'https://bet.hkjc.com/racing/getJSON.aspx' 
    isTypeStartEnd = (sDataType == 'winplaodds')

    betParams = {'type': sDataType, 'date': sRaceDate, 'venue': sRaceVenue}
    sParams = 'type=' + sDataType + '&date=' + sRaceDate + '&venue=' + sRaceVenue  

    if not isTypeStartEnd :
        betParams['raceno'] = sRaceNo
        sParams = sParams + '&raceno=' + sRaceNo 
    else :
        betParams['start'] = sRaceNo
        betParams['end'] = sRaceNo 
        sParams = sParams + '&start=' + sRaceNo + '&end=' + sRaceNo 

    race_url = base_url + '?' + sParams
    #print(race_url)

    WebDriverOptions = Options()
    WebDriverOptions.headless = True
    
    browser = webdriver.Firefox(options=WebDriverOptions)
    browser.get(race_url)
    time.sleep(4)
    #print("browser page source")
    #print(browser.page_source)
    txtPage = browser.page_source
    browser.close

    #just really need to get the text between the curly brackets {"OUT":""}
    #print("soup html.parser")
    mySoup = soup(txtPage, 'html.parser')
    #print(mySoup)
    #print("just the text")
    #besure to include the (), get something different otherwise.
    justText = mySoup.get_text()
    #print(justText)

    #write text file of the string for later processing.
    path_to_file = path_to_write_directory  + '\\' + sDataType + sRaceNo + '.txt'

    with open(path_to_file,'w') as oddsFile:
        oddsFile.write(justText)
        oddsFile.close()

    return
#end def 


def fetch_results(RaceNo: int, sRaceDate: str, sRaceVenue: str,  path_to_write_directory: str) :
    sRaceNo = str(RaceNo)

    #https://racing.hkjc.com/racing/information/English/racing/LocalResults.aspx
    #https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate=2023/01/15&Racecourse=ST&RaceNo=2
    base_url = 'https://racing.hkjc.com/racing/information/English/racing/LocalResults.aspx' 

    slashRaceDate = sRaceDate.replace("-","/")
    sParams = 'RaceDate=' + sRaceDate + '&Racecourse=' + sRaceVenue + '&RaceNo=' + sRaceNo 


    race_url = base_url + '?' + sParams
    #print(race_url)

    WebDriverOptions = Options()
    WebDriverOptions.headless = True
    
    browser = webdriver.Firefox(options=WebDriverOptions)
    browser.get(race_url)
    time.sleep(10)
    #print("browser page source")
    #print(browser.page_source)
    txtPage = browser.page_source
    browser.close

    print(txtPage)


    #write text file of the string for later processing.
    path_to_file = path_to_write_directory  + '\\results_' + sRaceNo  + '.txt'

    #write page source for later (optional) processing.
    #use encoding='utf-8' when writing chinese characters.
    with open(path_to_file,'w',encoding='utf-8') as oddsFile:
        oddsFile.write(txtPage)
        oddsFile.close()

    #get results status.
    #no results or unofficial or with dividends

    iPos = txtPage.find("Unofficial")
    jPos = txtPage.find("Winning Combination", iPos+1)
    #print(iPos,jPos)

    weHaveResults = iPos > 0 or jPos > 0

    return weHaveResults
#end def  


def fetch_raceday_results(lastRace: int, sRaceDate: str, sRaceVenue: str,  path_to_write_directory: str) :
    #this function gives the "results status" for each race (pending or unofficial results /dividends)
    # (race has run or it hasn't run yet.)

    #this page gives all the results for all the races of the day.
    base_url = 'https://racing.hkjc.com/racing/information/English/Racing/ResultsAll.aspx' 
    #view-source:https://racing.hkjc.com/racing/information/English/Racing/ResultsAll.aspx?RaceDate=2023/01/18

    slashRaceDate = sRaceDate.replace("-","/")
    sParams = 'RaceDate=' + slashRaceDate 
    #+ '&Racecourse=' + sRaceVenue 
    #+ '&RaceNo=' + sRaceNo 

    race_url = base_url + '?' + sParams
    print(race_url)

    WebDriverOptions = Options()
    WebDriverOptions.headless = True
    
    browser = webdriver.Firefox(options=WebDriverOptions)
    browser.get(race_url)
    time.sleep(10)
    #print("browser page source")
    #print(browser.page_source)
    txtPage = browser.page_source
    browser.close

    #print(txtPage)

    #write text file of the string for later possible processing.
    path_to_file = path_to_write_directory  + '\\raceday_results' + '.txt'

    #write page source for later (optional) processing.
    #use encoding='utf-8' when writing chinese characters.
    with open(path_to_file,'w',encoding='utf-8') as oddsFile:
        oddsFile.write(txtPage)
        oddsFile.close()

    #get results status.
    #no results or unofficial or with dividends

    #create an array of zeros... we'll turn 'em into the position of that info in the 
    # web page. 
    RacePos = [0]*(lastRace+2)


    for iRace in range(1,lastRace+1):
        sRace = str(iRace)
        RacePos[iRace] = txtPage.find("Race " + sRace)
        print(iRace, RacePos[iRace])
    RacePos[lastRace+1] = txtPage.find("Dividend Note")
    print(lastRace+1, RacePos[lastRace+1])

    RaceResults = [0]*(lastRace+1)
    for iRace in range(1,lastRace+1):
        sRace = str(iRace)
        uPos = txtPage.find("Unofficial",RacePos[iRace],RacePos[iRace+1])
        dPos = txtPage.find("Winning Combination",RacePos[iRace],RacePos[iRace+1])
        
        RaceResults[iRace] = uPos > 0 or dPos > 0
        print(iRace, uPos, dPos, RaceResults[iRace])

    dfRaceResults = pd.DataFrame(RaceResults, columns=['isRaceFinished'])
    dfRaceResults = dfRaceResults.rename_axis('Race').reset_index()
    dfRaceResults = dfRaceResults[dfRaceResults['Race'] > 0]

    return dfRaceResults
#end def  
