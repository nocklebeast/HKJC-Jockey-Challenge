#see this example
# https://learn.circuit.rocks/how-to-extract-data-from-webpages-using-python
# info on requests package: https://docs.python-requests.org/en/master/user/quickstart/#cookies

# hkjc specific example found on the web!  https://python-forum.io/thread-16837.html
# https://selenium-python.readthedocs.io/installation.html

#need to install gecko driver (for firefox) for windows.
# http://www.learningaboutelectronics.com/Articles/How-to-install-geckodriver-Python-windows.php

#from tracemalloc import stop
#import urllib.request as ul
from bs4 import BeautifulSoup as soup
import pandas as pd
import json
import os
#from multiprocessing import Process

import requests
import time 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

#race_day_url = 'https://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date=2022-05-01&venue=ST&start=8&end=8'

"""
#different odds data types
#lBetTypes=[ 'winplaodds', 'qin', 'qpl', 'fct', 'tceinv' , 'tcetop', 'tcebank', 'tri']
#let's only fetch odds we use for handicapping the jockey challenge.
#'tceinv' is tierce investments.
#'tcetop' is tierce top 20
#'tcebank' is tierce top 10 bankers.
#'tri' is full trio grid.
# winplaodds = win and place odds
# qin = quinella
# qpl = quinella place
# fct = forecase or exacta
"""

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
    print(race_url)

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
    print(justText)

    #write text file of the string for later processing.
    path_to_file = path_to_write_directory  + '\\' + sDataType + sRaceNo + '.txt'

    with open(path_to_file,'w') as oddsFile:
        oddsFile.write(justText)
        oddsFile.close()

    return
#end def fetch_odds

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'

path_to_file = path_to_directory + 'race_parameters' + '.txt'
RaceParameters = pd.read_csv(path_to_file)  
print(RaceParameters)

sDate = RaceParameters.at[0,'sDate']
#sRace = RaceParameters.at[0,'sRace']
firstRace = int(RaceParameters.at[0,'firstRace'])
lastRace = int(RaceParameters.at[0,'lastRace'])
sVenue = RaceParameters.at[0,'sVenue']

print(sDate)
print(firstRace)
print(lastRace)
print(sVenue)

for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    #lBetTypes=[ 'tceinv', 'tcetop', 'tcebank', 'tri']
    #lBetTypes=[ 'tceinv', 'fct', 'qin']
    #lBetTypes=[ 'winplaodds', 'qin', 'qpl', 'fct', 'tceinv' , 'tcetop', 'tcebank', 'tri']
    lBetTypes=[ 'tceinv', 'fct', 'qin', 'qpl']

    for sType in lBetTypes:
        print(sRace)
        print(sType)
        fetch_odds(sRace,sType, sDate, sVenue,  path_to_directory)

    #doesn't seem to be any faster
    """
    if __name__ == "__main__":
        p1 = Process(target=fetch_odds(sRace, 'tceinv', sDate, sVenue,  path_to_directory))
        p2 = Process(target=fetch_odds(sRace, 'fct', sDate, sVenue,  path_to_directory))
        p3 = Process(target=fetch_odds(sRace, 'qin', sDate, sVenue,  path_to_directory))
        p4 = Process(target=fetch_odds(sRace, 'qpl', sDate, sVenue,  path_to_directory))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()

    """

    #end for loop on lBetTypes
#end of for loop on iRace
print("FINISHED FETCHING ODDS")
print()
print()


