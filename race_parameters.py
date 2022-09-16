
import pandas as pd
import numpy as np
import os

data={'sRace':['4'], 'firstRace':['4'], 'lastRace':['8'], 'sDate':['2022-09-14'], 'sVenue':['HV'] }

# Create DataFrame  
race_parameters = pd.DataFrame(data)  
  
# Print the output.  

print(race_parameters)

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
race_parameters.to_csv(path_to_directory + 'race_parameters' + '.txt', index=False)

