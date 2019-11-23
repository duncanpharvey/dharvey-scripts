import itertools
import pandas as pd
import matplotlib.pyplot as plt
import math

class Team:
    def __init__(self, name, currentwins, points, ranksummary):
        self.name = name
        self.currentwins = currentwins
        self.points = points
        self.ranksummary = ranksummary

ranksummarybase = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}

chubba = Team("chubba chubba choo choo", 9, 1078.4, ranksummarybase.copy())
golladays = Team("happy golladays", 8, 1167.76, ranksummarybase.copy())
bortles = Team("bortles' chortles", 7, 1168.58, ranksummarybase.copy())
job = Team("do your job", 7, 1120.26, ranksummarybase.copy())
obj = Team("bend it like obj", 7, 1043.60, ranksummarybase.copy())
luck = Team("outta luck", 6, 1050.30, ranksummarybase.copy())
apple = Team("the big apple", 6, 957.44, ranksummarybase.copy())
allstars = Team("all stars", 5, 1028.62, ranksummarybase.copy())
krakens = Team("the purple krakens", 3, 900.70, ranksummarybase.copy())
juju = Team("got that good juju", 3, 894.96, ranksummarybase.copy())
charm = Team("fifth time's a charm", 3, 862.12, ranksummarybase.copy())
ships = Team("sinking ships losing 'chips", 2, 940.90, ranksummarybase.copy())

teams = [chubba, golladays, bortles, job, obj, luck, apple, allstars,
         krakens, juju, charm, ships]

game1 = [golladays, ships]
game2 = [obj, chubba]
game3 = [apple, krakens]
game4 = [charm, job]
game5 = [luck, bortles]
game6 = [allstars, juju]

game7 = [golladays, krakens]
game8 = [ships, chubba]
game9 = [job, obj]
game10 = [bortles, apple]
game11 = [juju, charm]
game12 = [allstars, luck]

game13 = [golladays, bortles]
game14 = [krakens, ships]
game15 = [chubba, job]
game16 = [obj, juju]
game17 = [apple, allstars]
game18 = [charm, luck]

games = [game1, game2, game3, game4, game5, game6, game7, game8, game9, game10,
         game11, game12, game13, game14, game15, game16, game17, game18]

#find all possible scenarios
results = list(itertools.product(*games))

count = 0
totalscenarios = 2 ** len(games)
print("total number of scenarios: ", totalscenarios)
print("evaluating scenarios...", end = '')

#determine number of wins for each team at the end of each scenario
for result in results:
    for team in teams:
        team.wins = team.currentwins #reset wins for each team for each result
        
    for team in result:
        team.wins += 1
    
    teams.sort(key = lambda x: (x.wins, x.points), reverse = True) #sort teams by wins then points (both descending)

    for i in range(0, len(teams)): #summarize results
        teams[i].ranksummary[i + 1] += 1

    if count % 100000 == 0:
        print(count, end = '')
        
    if count % 10000 == 0:
        print('.', end = '')
    
    count += 1

#determine playoff odds based off of scenario summary- teams make playoffs if they are one of the top 4 ranked teams
for team in teams:
    playoffodds = 0
    for rank in range(1, 5):
        playoffodds += (team.ranksummary[rank] / totalscenarios)
    team.playoffodds = round(playoffodds * 100, 2)

    expectedrank = 0
    for rank in team.ranksummary:
        expectedrank += rank * (team.ranksummary[rank] / totalscenarios)
    team.expectedrank = round(expectedrank, 2)

teams.sort(key = lambda x: x.expectedrank)

print('\n')

visdata = {'rank' : list(range(1, len(teams) + 1))}

maxrankodds = 0 #save to scale visualizations
for team in teams:
    #round and display raw rank data
    for rank in team.ranksummary:
        rankodds = round((team.ranksummary[rank] / totalscenarios) * 100, 2)
        maxrankodds = rankodds if rankodds > maxrankodds else maxrankodds
        team.ranksummary[rank] = rankodds
    print(team.name, '|', str(team.playoffodds) + '%', '|', team.expectedrank, '|', team.ranksummary)

    #save data in a dictionary for visualization
    visdata[team.name] = list(team.ranksummary.values())

playoffodds = pd.DataFrame(visdata)

#initialize plot
fig, axes = plt.subplots(figsize = (9, 9), nrows = 3, ncols = 4)
playoffodds.set_index('rank', drop = True, inplace = True)

colors = []
playoffcolors = ['g'] * 4
othercolors = ['b'] * 7
lastplacecolor = 'r'

colors.extend(playoffcolors)
colors.extend(othercolors)
colors.append(lastplacecolor)

#generate subplots for each team
for x in range(0, 3):
    for y in range(0, 4):
        teamname = teams[(4 * x) + y].name
        playoffodds[teamname].plot(ax = axes[x,y], kind = 'bar', color = colors)
        axes[x, y].set_ylim(0, 10 * math.ceil(maxrankodds / 10)) #set y axis limit based on largest rank odds(round up to nearest 10)
        axes[x, y].set_title(teamname)
        axes[x, y].set_xlabel('')

fig.text(0.5,0.04, "rank", ha = "center", va = "center")
fig.text(0.05,0.5, "% chance of outcome", ha = "center", va = "center", rotation = 90)

plt.tight_layout(pad = 4.0, w_pad = 0.0, h_pad = 1.0)
plt.show()
