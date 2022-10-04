#see this example
# https://learn.circuit.rocks/how-to-extract-data-from-webpages-using-python
# info on requests package: https://docs.python-requests.org/en/master/user/quickstart/#cookies

# hkjc specific example found on the web!  https://python-forum.io/thread-16837.html
# https://selenium-python.readthedocs.io/installation.html

#need to install gecko driver (for firefox) for windows.
# http://www.learningaboutelectronics.com/Articles/How-to-install-geckodriver-Python-windows.php

#from tracemalloc import stop
#import urllib.request as ul
from tracemalloc import stop
from bs4 import BeautifulSoup as soup
import pandas as pd
import json
import os

import requests
import time 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

#race_day_url = 'https://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date=2022-05-01&venue=ST&start=8&end=8'


cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'

path_to_file = path_to_directory + 'race_parameters' + '.txt'
RaceParameters = pd.read_csv(path_to_file)  
print(RaceParameters)

sDate = RaceParameters.at[0,'sDate']
sRace = RaceParameters.at[0,'sRace']
firstRace = int(RaceParameters.at[0,'firstRace'])
lastRace = int(RaceParameters.at[0,'lastRace'])
sVenue = RaceParameters.at[0,'sVenue']

print(sDate)
print(sRace)
print(firstRace)
print(lastRace)
print(sVenue)


for iRace in range(firstRace,lastRace+1) :

    sRace = str(iRace)
    #lBetTypes=[ 'winplaodds', 'qin', 'qpl', 'fct', 'tceinv' , 'tcetop', 'tcebank', 'tri']
    #let's only fetch odds we use for handicapping the jockey challenge.
    #'tceinv' is tierce investments.
    #'tcetop' is tierce top 20
    #'tcebank' is tierce top 10 bankers.
    #'tri' is full trio grid.
    #lBetTypes=[ 'tceinv', 'tcetop', 'tcebank', 'tri']
    #lBetTypes=[ 'tceinv', 'fct', 'qin']
    #lBetTypes=[ 'winplaodds', 'qin', 'qpl', 'fct', 'tceinv' , 'tcetop', 'tcebank', 'tri']
    lBetTypes=[ 'tceinv', 'fct', 'qin'] #, 'qpl']

    for sType in lBetTypes:
        print(sRace)
        print(sType)

        base_url = 'https://bet.hkjc.com/racing/getJSON.aspx' 
        isTypeStartEnd = (sType == 'winplaodds')

        betParams = {'type': sType, 'date': sDate, 'venue': sVenue}
        sParams = 'type=' + sType + '&date=' + sDate + '&venue=' + sVenue  

        if not isTypeStartEnd :
            betParams['raceno'] = sRace
            sParams = sParams + '&raceno=' + sRace 
        else :
            betParams['start'] = sRace
            betParams['end'] = sRace 
            sParams = sParams + '&start=' + sRace + '&end=' + sRace 

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
        path_to_file = path_to_directory  + '\\' + sType + sRace + '.txt'

        with open(path_to_file,'w') as oddsFile:
            oddsFile.write(justText)
            oddsFile.close()

    #end for loop on lBetTypes

#end of for loop on iRace


# now fetch jockey odds
# fetch jockey challenge odds with hkjc_fetch_jkc.py
