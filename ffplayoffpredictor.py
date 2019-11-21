import itertools
import pandas as pd
import matplotlib.pyplot as plt

ranksummary = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}

class Team:
    def __init__(self, name, currentwins, points, ranksummary):
        self.name = name
        self.currentwins = currentwins
        self.points = points
        self.ranksummary = ranksummary

chubba = Team("chubba chubba choo choo", 9, 1078.4, ranksummary.copy())
golladays = Team("happy golladays", 8, 1167.76, ranksummary.copy())
bortles = Team("bortles' chortles", 7, 1168.58, ranksummary.copy())
job = Team("do your job", 7, 1120.26, ranksummary.copy())
obj = Team("bend it like obj", 7, 1043.60, ranksummary.copy())
luck = Team("shit outta luck", 6, 1050.30, ranksummary.copy())
apple = Team("the big apple", 6, 957.44, ranksummary.copy())
allstars = Team("titty city all stars", 5, 1028.62, ranksummary.copy())
krakens = Team("the purple krakens", 3, 900.70, ranksummary.copy())
juju = Team("got that good juju", 3, 894.96, ranksummary.copy())
charm = Team("fifth time's a charm", 3, 862.12, ranksummary.copy())
ships = Team("sinking ships losing 'chips", 2, 940.90, ranksummary.copy())

teams = [chubba, golladays, bortles, job, obj, luck, apple, allstars, \
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

#find all possible scenarios
results = list(itertools.product(game1, game2, game3, game4, game5, game6, \
                                 game7, game8, game9, game10, game11, game12, \
                                 game13, game14, game15, game16, game17, game18))

count = 0
totalscenarios = 2 ** 18
print("total number of scenarios: ", totalscenarios)
print("evaluating scenarios...", end = '')

#determine number of wins for each team at the end of each scenario
for result in results:
    for team in teams:
        team.wins = team.currentwins #reset wins for each team for each result
        
    for team in result:
        team.wins += 1
    
    teams.sort(key = lambda x: (x.wins, x.points), reverse = True) #sort teams by wins then points (both descending)

    for i in range(0, len(teams)):
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

#round and display raw rank data
for team in teams:
    for rank in team.ranksummary:
        team.ranksummary[rank] = round((team.ranksummary[rank] / totalscenarios) * 100, 2)
    print(team.name, '|', str(team.playoffodds) + '%', '|', team.expectedrank, '|', team.ranksummary)

#save data to use in pandas
playoffodds = pd.DataFrame({'rank' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12],
                            chubba.name : list(chubba.ranksummary.values()),
                            golladays.name : list(golladays.ranksummary.values()),
                            bortles.name : list(bortles.ranksummary.values()),
                            job.name : list(job.ranksummary.values()),
                            obj.name : list(obj.ranksummary.values()),
                            luck.name : list(luck.ranksummary.values()),
                            apple.name : list(apple.ranksummary.values()),
                            allstars.name : list(allstars.ranksummary.values()),
                            krakens.name : list(krakens.ranksummary.values()),
                            juju.name : list(juju.ranksummary.values()),
                            charm.name : list(charm.ranksummary.values()),
                            ships.name : list(ships.ranksummary.values())})

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
        axes[x, y].set_ylim(0, 60)
        axes[x, y].set_title(teamname)
        axes[x, y].set_xlabel('')

fig.text(0.5,0.04, "rank", ha = "center", va = "center")
fig.text(0.05,0.5, "% chance of outcome", ha = "center", va = "center", rotation = 90)

plt.tight_layout(pad = 4.0, w_pad = 0.0, h_pad = 1.0)
plt.show()
