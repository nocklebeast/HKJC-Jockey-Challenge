
import pandas as pd
import numpy as np
import os

data={'sRace':['5'], 'firstRace':['5'], 'lastRace':['11'], 'sDate':['2022-07-16'], 'sVenue':['ST'] }

# Create DataFrame  
race_parameters = pd.DataFrame(data)  
  
# Print the output.  

print(race_parameters)

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
race_parameters.to_csv(path_to_directory + 'race_parameters' + '.txt', index=False)

