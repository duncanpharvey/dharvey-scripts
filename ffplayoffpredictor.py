import itertools
import pandas as pd
import matplotlib.pyplot as plt
import math

import time
start = time.time()

class Team:
    def __init__(self, name, currentwins, points, ranksummary):
        self.name = name
        self.currentwins = currentwins
        self.points = points
        self.ranksummary = ranksummary

ranksummarybase = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}

mahomes = Team("quarantined in mahomes", 6, 940, ranksummarybase.copy())
comeback = Team("don't call it a comeback", 6, 908, ranksummarybase.copy())
gore = Team("goreonavirus", 6, 876, ranksummarybase.copy())
bortles = Team("bortles' chortles", 5, 952, ranksummarybase.copy())
fresh = Team("fresh prince of helaire", 5, 856, ranksummarybase.copy())
chubba = Team("chubba chubba choo choo", 5, 845, ranksummarybase.copy())
josh = Team("josh jacobs jingleheimerschmidt", 5, 792, ranksummarybase.copy())
bucs = Team("bucs bandwagon", 4, 861, ranksummarybase.copy())
lil = Team("lil harvey", 4, 817, ranksummarybase.copy())
krakens = Team("the purple krakens", 4, 801, ranksummarybase.copy())
juju = Team("need that good juju", 2, 779, ranksummarybase.copy())
charm = Team("eighth time's a charm", 2, 760, ranksummarybase.copy())


teams = [mahomes, comeback, gore, bortles, fresh, chubba, josh, bucs,
         lil, krakens, juju, charm]

game1 = [josh, lil]
game2 = [comeback, charm]
game3 = [chubba, krakens]
game4 = [juju, gore]
game5 = [bucs, fresh]
game6 = [bortles, mahomes]

game7 = [josh, comeback]
game8 = [charm, bucs]
game9 = [gore, bortles]
game10 = [mahomes, lil]
game11 = [juju, krakens]
game12 = [fresh, chubba]

game13 = [josh, krakens]
game14 = [chubba, fresh]
game15 = [bucs, bortles]
game16 = [mahomes, juju]
game17 = [charm, comeback]
game18 = [lil, gore]

game19 = [josh, juju]
game20 = [mahomes, comeback]
game21 = [bucs, krakens]
game22 = [fresh, gore]
game23 = [bortles, charm]
game24 = [lil, chubba]

game25 = [josh, bortles]
game26 = [charm, mahomes]
game27 = [gore, chubba]
game28 = [juju, comeback]
game29 = [krakens, fresh]
game30 = [lil, bucs]

games = [
            game1, game2, game3, game4, game5, game6,
            game7, game8, game9, game10, game11, game12,
            game13, game14, game15, game16, game17, game18,
            game19, game20, game21, game22, game23, game24,
            game25, game26, game27, game28, game29, game30
        ]

totalscenarios = 2 ** len(games)
print("total number of scenarios:", totalscenarios)

#determine number of wins for each team at the end of each scenario
for result in itertools.product(*games):
    for team in teams:
        team.wins = team.currentwins #reset wins for each team for each result
        
    for team in result:
        team.wins += 1
    
    teams.sort(key = lambda x: (x.wins, x.points), reverse = True) #sort teams by wins then points (both descending)

    for i in range(0, len(teams)): #summarize results
        teams[i].ranksummary[i + 1] += 1

end = time.time()
print("time:", end - start, "seconds")

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