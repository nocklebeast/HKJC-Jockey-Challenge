
import pandas as pd
import numpy as np
import os

data={'sRace':['1'], 'firstRace':['1'], 'lastRace':['10'], 'sDate':['2022-09-11'], 'sVenue':['ST'] }

# Create DataFrame  
race_parameters = pd.DataFrame(data)  
  
# Print the output.  

print(race_parameters)

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'
race_parameters.to_csv(path_to_directory + 'race_parameters' + '.txt', index=False)

