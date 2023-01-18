
import os
import shutil

from hkjc_functions import read_race_parameters
from hkjc_functions import fetch_results
from hkjc_functions import fetch_raceday_results


cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
path_to_raw = cwd + '\\odds_files\\' + '\\odds_raw\\'

path_to_file = path_to_directory + 'race_parameters' + '.txt'

firstRace, lastRace, sDate, sVenue, jType = read_race_parameters(path_to_file)


haveResults = fetch_raceday_results(lastRace,sDate,sVenue,path_to_directory)
print("we have results for races ")
print(haveResults)


