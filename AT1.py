import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

const = pd.read_csv('./F1_Constructor_Standings.csv')
driver = pd.read_csv('./F1_Driver_Standings.csv')
race = pd.read_csv('./F1_Race_Results.csv')

#for riley
#instead of creating more columns for each value of episode, have an array that has all the values of episodes you would like to 
#have. next, append the total amount of shows that have that many episodes to a new array. Convert this array to np array if
#needed, and then graph using those values. To get y axis, remember the scale of the original array.


def menu():
    global menuVar
    menuVar = int(input('''
    Press 1 to see a list of teams competeing.
    Press 2 to see how track times have changed throughout the years on a certain track.
    Press 3 to see a list of the top 10 drivers in F1.
    Press 4 to see a comparison between two drivers.
    Press 0 to quit.
    '''))


#list of teams competeing
def competeing():

    const.drop_duplicates(subset='Team',inplace=True, keep='first', ignore_index=True)
    totalTeams = const['Team']

    print(totalTeams)

#lap times per track over time
def trackTimes():

    userRace = input('which track would you like to see the average track times for? (Capitalise the name of the country)')
        
    graph = race.loc[race['Grand Prix'] == userRace]#finds all rows that are raced on a track specified by userRace

    graph[['Day', 'Month', 'Year',]] = graph['Date'].str.split(expand=True) #breaks up the time data into a graphable form
    graph[['Hour', 'Min','Sec']] = graph['Time'].str.split(':', expand=True) #breaks up lap time data into a graphable form
    graph = graph.drop(['Time','Date'], 1) #removes old, useless columns
        
    datatypes = {'Year': 'int', 'Hour': 'float', 'Min': 'float', 'Sec': 'float'} #sets new dtypes for columns
    graph = graph.astype(datatypes)

    for i in range(len(graph)):
        graph['Hour'].iloc[i] = graph['Hour'].iloc[i]*60**2
        graph['Min'].iloc[i] = graph['Min'].iloc[i]*60
        graph['Avg'] = (graph['Hour'] + graph['Min'] + graph['Sec']) / graph['Laps'] 
        #This loop converts all the time into seconds, and then divides by laps to get the average time of one lap
        
    graph = graph.reset_index(drop=True)#cleaning the data
    graph = graph.drop([2], axis = 0)

    plt.plot(graph['Year'], graph['Avg'], color='red')
    plt.xlabel('Year')
    plt.ylabel('Average Time (S)')
    plt.title(f'Average lap times of {userRace} over time')#f string is used to have an easy, reactive title
    plt.show()
        #Building Graph
    print(graph)
        #limitation of data, while times and place are specified, track is not. Many countries have multiple tracks and thus the
        #time can be vastly different.


#top 10 drivers of all time
def top10():
    
    #these drivers are sorted by the amount of championships won in their career divided by the amount of championships ran, aka win%

    topDrive = driver
    topDrive = topDrive.sort_values('Driver')
    topDrive = topDrive.astype({'PTS': 'float'}) #sets data type to a number instead of a string to allow for maths
        
    Drivers = topDrive['Driver'].nunique() #fetches the number of drivers
        
    totalDriver = []
    for i in range(len(topDrive)):
        if topDrive.iloc[i, 1] not in totalDriver:
            totalDriver.append(topDrive.iloc[i, 1])
        else: 
            pass
    #finds all the drivers and appends them to a list
    totalScore = []
    for i in range(len(totalDriver)):
        tempScore = topDrive.loc[topDrive['Driver'] == totalDriver[i]]
        tempScore['PTS'].astype('float')
        totalScore.append(tempScore['PTS'].sum()/len(tempScore))
        #finds the total score that each driver has, then calculates the average points per race
    totalDriver = np.array(totalDriver) 
        #converting type of array to allow for it to go into a dataframe easily
        
    bestDriver = pd.DataFrame(columns=['Name','Avg Points']) #creating a new dataframe to display the data
    bestDriver['Avg Points'] = totalScore
    bestDriver['Avg Points'] = bestDriver['Avg Points'].round()
    bestDriver['Name'] = totalDriver.tolist()
        
    bestDriver = bestDriver.sort_values('Avg Points', ascending=False)
    bestDriver = bestDriver.reset_index(drop=True)

    print(bestDriver.head(10))
    #This code gives the average points each driver recives per race, and then shows the best 10 drivers.
    #This has flaws, as the point system changed over time and thus different time periods gave different amount of points

#compare different drivers
def compareDriver():

    compDriver = input("Select two drivers (Fname and Sname) that you want to be compared. Seperate names by a /")#collects the users drivers
    userDrivers = compDriver.split('/')#splits the input into an array
    driver1 = userDrivers[0]
    driver2 = userDrivers[1]#grabs both of the drivers names
    
    compareDriver = pd.DataFrame(columns =[f'{driver1}',f'{driver2}'], index=['Races','Avg Pos','Years Driven'])
    
    compare = driver.loc[driver['Driver'].str.contains(f'{driver1}|{driver2}', case=False)]#finds all rows that have the driver's names inside of them
    compare = compare.sort_values('Year')
        
    raceAmounts = {}
    ptsAmounts = {}
    yearTotal = {}
        
    for i in range(2):
        tempAmount = compare.loc[compare['Driver'].str.contains(vars()['driver' + str(i+1)], case=False)]
        raceAmounts["totalAmount" + str(i+1)] = len(tempAmount)#grabs total amount of races of each driver
        
        tempAmount['Pos'] = tempAmount['Pos'].astype(int)    
        tempPTS = tempAmount['Pos']/len(tempAmount)
        
        ptsAmounts["Pos" + str(i+1)] = tempPTS.sum()#total amount of points of each driver

        tempYear = compare.loc[compare['Driver'].str.contains(vars()['driver' + str(i+1)], case=False)]
        tempYear = tempYear['Year'].str.slice(0,4)
        teampYear = tempYear.sort_values(ascending=True)
        tempYear = tempYear.astype(int)
        yearTotal['Year' + str(i+1)] = tempYear.iloc[-1]-tempYear.iloc[0]#total years each driver drove for
            
        compareDriver.loc['Races',vars()["driver"+str(i+1)]] = raceAmounts['totalAmount' + str(i+1)]
        compareDriver.loc['Avg Pos',vars()["driver"+str(i+1)]] = ptsAmounts['Pos' + str(i+1)]
        compareDriver.loc['Years Driven', vars()["driver"+str(i+1)]] = yearTotal['Year' + str(i+1)]
        #adds all of the stats to a readable dataframe
        #vars() is used in this for loop to make querying the dataframe with a for loop possible
        #dictionaries are used to allow for variable generation through a for loop
        #the name of the variable within the dictionary is the key, and the value of the dictionary is the value of the variable
    print(compareDriver)
    categories = ['Races','Avg Pos','Years Driven']
    print(categories)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=compareDriver[f'{driver1}'].tolist(),
        theta=categories,
        fill='toself',
        name=driver1,
        ))
    fig.add_trace(go.Scatterpolar(
        r=compareDriver[f'{driver2}'].tolist(),
        theta=categories,
        fill='toself',
        name=driver2,
        ))
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, compareDriver.max()]
        )),
    title=go.layout.Title(text=f'{driver1} vs {driver2}', xanchor='left',y=0.9, font_size=30),
    showlegend=True,
    legend_xanchor='left',
    legend_x = 1, legend_y = 0.97,
    margin_autoexpand=True,
    margin_t=0, margin_l=0, margin_r=0, margin_b=0,
    )
    fig.show()
    #graphing the comparison with plotly
    
menu()

while True:
    if menuVar == 1:
        competeing()
    if menuVar == 2:
        trackTimes()
    if menuVar == 3:
        top10()
    if menuVar == 4:
        compareDriver()
    if menuVar == 0:
        quit()
    menu()