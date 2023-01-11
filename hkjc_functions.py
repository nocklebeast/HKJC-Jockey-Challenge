
import pandas as pd
import os
import shutil

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as soup
import json

import requests
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
#end def fetch_odds