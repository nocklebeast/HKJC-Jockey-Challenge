#see this example
# https://learn.circuit.rocks/how-to-extract-data-from-webpages-using-python
# info on requests package: https://docs.python-requests.org/en/master/user/quickstart/#cookies

# hkjc specific example found on the web!  https://python-forum.io/thread-16837.html
# https://selenium-python.readthedocs.io/installation.html

#need to install gecko driver (for firefox) for windows.
# http://www.learningaboutelectronics.com/Articles/How-to-install-geckodriver-Python-windows.php

import os
import shutil
import time

from hkjc_functions import read_race_parameters
from hkjc_functions import fetch_odds


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

#def_fetch_odds

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\' 
path_to_raw = cwd + '\\odds_files\\' + '\\odds_raw\\'
print(path_to_raw)

try:
    os.mkdir(path_to_raw)
except OSError as error:
    print(error)


path_to_file = path_to_directory + 'race_parameters' + '.txt'
#copy race_parameters into raw odds
shutil.copyfile(path_to_directory + 'race_parameters.txt', path_to_raw + 'race_parameters.txt')


firstRace, lastRace, sDate, sVenue, jType = read_race_parameters(path_to_file)

start_time = time.time()

for iRace in range(firstRace,lastRace+1) :
    sRace = str(iRace)
    print(sRace)
    #lBetTypes=[ 'tceinv', 'tcetop', 'tcebank', 'tri']
    #lBetTypes=[ 'tceinv', 'fct', 'qin']
    #lBetTypes=[ 'winplaodds', 'qin', 'qpl', 'fct', 'tceinv' , 'tcetop', 'tcebank', 'tri']
    lBetTypes=[ 'tceinv', 'fct', 'qin', 'qpl']
    nBetTypes = len(lBetTypes)
    
    for sType in lBetTypes:
        print(sRace)
        print(sType)
        fetch_odds(sRace,sType, sDate, sVenue,  path_to_raw)


    
    #end for loop on lBetTypes
#end of for loop on iRace

end_time = time.time()
elapsed_time = end_time - start_time


print("FINISHED FETCHING ODDS. " + "Elapsed time in seconds: ", elapsed_time)
print()
print()


