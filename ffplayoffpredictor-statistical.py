import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

ranksummarybase = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}

class Team:
    def __init__(self, name, currentwins, currentpoints, mean, stddev, weightedmean, weightedstddev):
        self.name = name
        self.currentwins = currentwins
        self.currentpoints = currentpoints
        self.mean = mean
        self.stddev = stddev
        self.ranksummary = ranksummarybase.copy()

mahomes = Team("quarantined in mahomes", 7, 1212.04, 101, 17.25, 95.71, 16.43)
comeback = Team("don't call it a comeback", 6, 1180.26, 98.36, 16.84, 96.59, 14.76)
gore = Team("goreonavirus", 8, 1148.8, 95.73, 15.04, 90.65, 12.93)
bortles = Team("bortles' chortles", 7, 1253.42, 104.45, 19.3, 104.31, 17.17)
fresh = Team("fresh prince of helaire", 7, 1115.4, 92.95, 10.18, 90.6, 10.06)
chubba = Team("chubba chubba choo choo", 7, 1115.82, 92.99, 11.88, 91.23, 11.84)
josh = Team("josh jacobs jingleheimerschmidt", 8, 1128.66, 94.06, 16.88, 100.49, 17.04)
bucs = Team("bucs bandwagon", 4, 1081.6, 90.13, 19.42, 87.04, 20.38)
lil = Team("lil harvey", 5, 1090.78, 90.9, 19.19, 89.43, 18.54)
krakens = Team("purple krakens", 4, 981.34, 81.78, 23.92, 73.3, 22.9)
juju = Team("need that good juju", 4, 1012.94, 84.41, 22.07, 84.3, 22.91)
charm = Team("eighth time's a charm", 5, 1067.08, 88.92, 15.96, 89.28, 16.85)

teams = [mahomes, comeback, gore, bortles, fresh, chubba, josh, bucs,
         lil, krakens, juju, charm]

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
            game19, game20, game21, game22, game23, game24,
            game25, game26, game27, game28, game29, game30
        ]

start = time.time()

trials = 1000000

for i in range(trials):
    for team in teams:
        team.wins = team.currentwins
        team.points = team.currentpoints

    for game in games:
        team1 = game[0]
        team2 = game[1]

        scores = list(map(lambda team: np.random.normal(team.mean, team.stddev, 1)[0], game))
        score1 = scores[0]
        score2 = scores[1]

        if score1 > score2:
            team1.wins += 1
        elif score2 > score1:
            team2.wins += 1
        else:
            team1.wins += 0.5
            team2.wins += 0.5

        team1.points += score1
        team2.points += score2

    teams.sort(key = lambda x: (x.wins, x.points), reverse = True)

    rank = 1
    for team in teams:
        team.ranksummary[rank] += 1
        rank += 1

end = time.time()
print("time:", end - start, "seconds")

#determine playoff odds based off of scenario summary- teams make playoffs if they are one of the top 4 ranked teams
for team in teams:
    playoffodds = 0
    for rank in range(1, 5):
        playoffodds += (team.ranksummary[rank] / trials)
    team.playoffodds = round(playoffodds * 100, 2)

    expectedrank = 0
    for rank in team.ranksummary:
        expectedrank += rank * (team.ranksummary[rank] / trials)
    team.expectedrank = round(expectedrank, 2)

teams.sort(key = lambda x: x.expectedrank)

visdata = {'rank' : list(range(1, len(teams) + 1))}

maxrankodds = 0 #save to scale visualizations
for team in teams:
    #round and display raw rank data
    for rank in team.ranksummary:
        rankodds = round((team.ranksummary[rank] / trials) * 100, 2)
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