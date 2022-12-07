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

from hkjc_functions import read_race_parameters

#race_day_url = 'https://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date=2022-05-01&venue=ST&start=8&end=8'


cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
path_to_raw = cwd + '\\odds_files\\' + '\\odds_raw\\'

path_to_file = path_to_directory + 'race_parameters' + '.txt'

firstRace, lastRace, sDate, sVenue, jType = read_race_parameters(path_to_file)

print(sDate)
print(firstRace)
print(lastRace)
print(sVenue)

# now fetch jockey odds (and trainer odds)

#https://bet.hkjc.com/racing/getJSON.aspx?type=jkc&date=2022-05-15&venue=ST 
base_url = 'https://bet.hkjc.com/racing/getJSON.aspx' 


lDataType = [jType] #jockey/trainer.  Let's only do either jockey OR trainer not both at once.

for sType in lDataType:
    #deal with race > 1 and tnc.
    #sType = "jkc"
    print(sType)
    if sType == 'tnc' and firstRace > 1:  
        print('There is not trainer challenge after the first race')
    else:
        sParams = 'type=' + sType + '&date=' + sDate + '&venue=' + sVenue  
        race_url = base_url + '?' + sParams
        print(race_url)

        WebDriverOptions = Options()
        WebDriverOptions.headless = True

        browser = webdriver.Firefox(options=WebDriverOptions)
        browser.get(race_url)
        time.sleep(3)
        #print("browser page source")
        #print(browser.page_source)
        txtPage = browser.page_source
        browser.close

        print(txtPage)

        mySoup = soup(txtPage, 'html.parser')
        #print(mySoup)
        #print("just the text")
        #besure to include the (), get something different otherwise.
        justText = mySoup.get_text()
        print(justText)

        #write text file of the string for later processing.
        path_to_file = path_to_raw  + '\\' + sType  + '.txt'

        #use encoding='utf-8' when writing chinese characters.
        with open(path_to_file,'w',encoding='utf-8') as oddsFile:
            oddsFile.write(justText)
            oddsFile.close()