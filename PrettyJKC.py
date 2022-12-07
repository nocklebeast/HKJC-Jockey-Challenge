#make sim JKC dataframe pretty for output

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import os

pd.set_option('display.max_rows',None)

cwd = os.getcwd()
print("My current directory is : " + cwd)
path_to_directory = cwd + '\\odds_files\\'

path_to_file = path_to_directory + 'race_parameters' + '.txt'
RaceParameters = pd.read_csv(path_to_file)  
print(RaceParameters)

sDate = RaceParameters.at[0,'sDate']
sRace = str(RaceParameters.at[0,'sRace'])
firstRace = int(RaceParameters.at[0,'firstRace'])
lastRace = int(RaceParameters.at[0,'lastRace'])
sVenue = RaceParameters.at[0,'sVenue']


for sType in ['tnc','jkc']:
    if sType == 'jkc':
        sThing = "Jockey"
    else:
        sThing = "Trainer"

    if firstRace > 1 and sType == 'tnc':
        print("Trainer challenge is only available before the start of the first race of the day.")
        print("")
    else:

        #map of Jockeys to Jockey selection numbers.
        path_to_file = path_to_directory + 'Sim' + sThing + 'Challenge' + '.csv'
        SimJockeyChallenge = pd.read_csv(path_to_file)
        print(SimJockeyChallenge)
        #drop selection that doesn't have a valid jkcNumber (like Other when there are not Others)
        SimJockeyChallenge.fillna(value=0)
        SimJockeyChallenge = SimJockeyChallenge[ SimJockeyChallenge[sType+'Number'] > 0 ]
        print(SimJockeyChallenge)
        PrettyJKC = SimJockeyChallenge.copy(deep=True)

        #format smaller numbers first 
        PrettyJKC.loc[PrettyJKC['Pay'] < 10, 'sPay'] = PrettyJKC['Pay'].map('{:,.2f}'.format)  #fixed point number format.
        PrettyJKC.loc[PrettyJKC['Pay'] >= 10, 'sPay'] = PrettyJKC['Pay'].map('{:,.1f}'.format)  
        PrettyJKC.loc[PrettyJKC['Pay'] >= 100, 'sPay'] = PrettyJKC['Pay'].map('{:.0f}'.format)  #no decimal and no 1000's commas.

        PrettyJKC['Chance'] = round(PrettyJKC['Chance'],2)
        PrettyJKC['ExpectedPoints'] = round(PrettyJKC['ExpectedPoints'],0)
        PrettyJKC['ExpectedPoints'] = PrettyJKC['ExpectedPoints'].astype(int)

        PrettyJKC.drop(['TotalPoints', 'RawChance','Pay','TotalWins','nRuns'], axis=1, inplace=True)
        PrettyJKC.rename(columns={'sPay':'Estimated Odds'}, inplace=True)
        PrettyJKC['Estimated Odds'] = PrettyJKC['Estimated Odds'].astype(float)
        PrettyJKC.rename(columns={sType+'Name':sThing}, inplace=True)
        PrettyJKC.rename(columns={sType+'CurrentOdds':'Current Odds'}, inplace=True)
        PrettyJKC.rename(columns={sType+'Points':sThing +' Points'}, inplace=True)
        PrettyJKC.rename(columns={'ExpectedPoints':'Expected Points'}, inplace=True)
        #order jockeys by expected points.
        PrettyJKC.sort_values(by=['Expected Points','Estimated Odds','Current Odds'],ascending=False,inplace=True)

        #check to see if there are zero previous points (usually when first race == 1)
        AllTotals = PrettyJKC.sum(axis=0)
        isFirstRace = AllTotals['Jockey Points'] == 0.0
        print(isFirstRace) 


        ##########################################################################################
        ### POINTS ### POINTS ### POINTS ### POINTS ### POINTS ### POINTS 
        ### create a bar plot of current POINTS before a particular race 
        #   and expected points at the end of the day for the jockey challenge.
        #g=green, b=blue, r=red, w=white, m=magenta

        #plt.style.use('classic')
        #plt.rcParams['legend.fontsize'] = 'medium'

        #axes[0] is first row axes[1] is second row of plt.subplots(nrows=2,ncols=1)
        fig, axes = plt.subplots(nrows=2,ncols=1, figsize=(5.8,7.5))

        sns.set_color_codes('pastel')
        # draw expected points first, then draw current points on top of expected points
        # 2nd bars [1] on top of 1st bars[0]

        sns.barplot(x = 'Expected Points', y = sThing, data = PrettyJKC,
                    label = 'Expected Points', color = 'b', edgecolor='w', ax=axes[0], orient='h')

        #next barplot is draw on top of bar plot above ^^^ (green on top of blue)
        if not isFirstRace:
            sns.barplot(x = sThing+' Points', y = sThing, data = PrettyJKC, 
                    label = 'Current Points', color = 'g', edgecolor = 'w', ax=axes[0], orient='h')
                        

        if not isFirstRace:                
            axes[0].legend(ncol = 2, loc = 'best') #'lower right')
            axes[0].bar_label(axes[0].containers[0], padding = 5) #expected points
            axes[0].bar_label(axes[0].containers[1], padding = 5, label_type='center') #current points
            
        else: 
            axes[0].legend(ncol = 1, loc = 'best')
            axes[0].bar_label(axes[0].containers[0], padding = 5) #expected points

        #axes[0].set_facecolor('g') #sets area of that axes to that color.

        sns.despine(left = True, bottom = True, ax=axes[0])

        sPlotTitle = sThing + " Challenge Points"
        axes[0].set_title(sPlotTitle)

        #create a simple/pretty dataframe for the odds table.
        #sort again by odds, so order and colors are correct on odds table.
        PrettyJKC.sort_values(by='Estimated Odds',ascending=True,inplace=True)
        PrettyOdds = PrettyJKC.copy(deep=True)
        PrettyOdds.drop([sType+'Number', sThing+' Points','Expected Points','Chance',sType+'RemainingRides'], axis=1, inplace=True)
        PrettyOdds.rename(columns={'Current Odds': 'Current HKJC Odds'}, inplace=True)
        
        #let's build color array based on if HKJC's odds are greater than our estimated pay/odds.
        #AFTER sorting jockeys by estimated odds.
        colors = PrettyJKC.copy(deep=True)
        colors['HKJCPay'] = colors['Current Odds'].astype(float)
        colors['OurPay'] = colors['Estimated Odds'].astype(float)
        colors['Nice Price'] = colors['HKJCPay'] > colors['OurPay']
        colors.loc[ colors['Nice Price'] == True, 'color'] = 'g'
        colors.loc[ colors['Nice Price'] == False, 'color'] = 'w'
        #print(colors)
        print(PrettyJKC)

        print(PrettyOdds)

        #hints on tables.
        # https://stackoverflow.com/questions/56409487/how-to-plot-a-table-of-pandas-dataframe-using-matplotlib
        # https://www.statology.org/matplotlib-table/ 
        # https://www.geeksforgeeks.org/matplotlib-axes-axes-table-in-python/ 
        # https://matplotlib.org/stable/api/table_api.html?highlight=table#matplotlib.table.Table
        # https://www.pythonpool.com/matplotlib-table/


        #fig.patch.set_visible(False)  #causes oddness with out the figure's face/patch (background or font weights) in saving plot.
        #fig.set_facecolor('green') # does this do anything? yes if set transparent to false when saving plot?
        #hide the axes
        axes[1].axis('off')
        axes[1].axis('tight')

        #create table
        #color rows green with good prices. create color array based on colors data frame
        colordf = pd.DataFrame()
        #count the number of columns in PrettyOdds, to color all the rows/columns
        nColumns = PrettyOdds.shape[1] #[0,1]= [rows,columns]
        for iCol in range(1,nColumns+1):
            sCol = "C" + str(iCol)  
            colordf[sCol] = colors['color']
        colorarray = colordf.to_numpy()
        #print(colorarray)

        table = axes[1].table(cellText = PrettyOdds.values, colLabels = PrettyOdds.columns,
                            cellColours = colorarray, loc='upper left'  )

        sTitle = sThing+" Challenge Odds"
        #how to not superimpose title on top of table?  set loc='upper left' above, this sets the location of the title.
        axes[1].set_title(sTitle)

        #this sets the title of the set of (sub)plots
        PrettyJKC.sort_values(by='Estimated Odds',ascending=False,inplace=True)
        Fave2Win = PrettyJKC[sThing][0]
        sOverallTitle = Fave2Win + ' projected to win '
        print(Fave2Win)
        if sVenue == "ST": 
            sFullVenue = "Sha Tin"
        else: sFullVenue = "Happy Valley"
        sOverallTitle = sOverallTitle + sThing+" Challenge" + "\n" + "(before the start of race " + sRace + " on " + sDate + " at " + sFullVenue + ")"
        plt.suptitle(sOverallTitle) #, fontweight='medium')

        #let's see all the Jockeys and labels on vertical axis.
        plt.tight_layout()

        path_to_file = path_to_directory + sType+'_points'
        #plt.savefig(path_to_file, transparent=True, facecolor = fig.get_facecolor(), edgecolor='none', dpi=100) 
        #plt.savefig(path_to_file, transparent=True, facecolor = 'white', edgecolor='none', dpi=100) 
        #plt.savefig(path_to_file + '.png', transparent=False, edgecolor='none', dpi=100, format='png') 
        plt.savefig(path_to_file + '.jpg', transparent=True, edgecolor='none', dpi=100, format='jpg') 
        plt.show()



        ### create a pie plot of chances the jockey will win the jockey challenge.
        PrettyJKC.drop([sType+'RemainingRides'], axis=1, inplace=True)

        PieJKC = PrettyJKC.copy(deep=True)
        print(PieJKC)
   

        #remove low probability jockeys.  Keep jockeys greater than minPct chance.
        minPct = 2.6
        PieJKC = PieJKC[ PieJKC['Chance'] > minPct]
        #print(PieJKC)
        
        #replace last probablities with "The Rest"
        AllTotals = PieJKC.sum(axis=0)
        #print(AllTotals)
        #JockeyNumber  jockeyName  CurrentOdds  JockeyPoints  ExpectedPoints  Chance   Pay
        #need to add a new row for "The Rest".
        TheRest = [99, 'The Rest', 999, 0, 0, 100-AllTotals['Chance'], 999]  
        #convert that list to a dictionary and then a dataframe and concat the two dataframes to append the row.
        dctTheRest = dict(zip(PieJKC.columns, TheRest))
        dfTheRest = pd.DataFrame(dctTheRest, index=[0])
        #print(dfTheRest)

        PieJKC = pd.concat([PieJKC, dfTheRest], axis=0)
        print(PieJKC)

        plt.pie(PieJKC["Chance"], 
                labels=PieJKC[sThing],
                autopct='%1.0f%%')


        sTitle = "Chance of Winning the " + sThing + " Challenge"
        plt.suptitle(sTitle)
        if sVenue == "ST": 
            sFullVenue = "Sha Tin"
        else: sFullVenue = "Happy Valley"

        sSubTitle = "before the start of race " + sRace + " on " + sDate + " at " + sFullVenue
        plt.title(sSubTitle)

        plt.tight_layout()
        path_to_file = path_to_directory + sType+'_odds' + '.jpg'
        plt.savefig(path_to_file, transparent=True, facecolor='w')
        plt.show()

    #end if print("Trainer challenge is only available before the start of the first race of the day.")
#end sType for loop.

