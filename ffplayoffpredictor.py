import itertools

ranksummary = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}

class Team:
    def __init__(self, name, currentwins, points, ranksummary):
        self.name = name
        self.currentwins = currentwins
        self.points = points
        self.ranksummary = ranksummary

chubba = Team("chubba chubba choo choo", 9, 1079.1, ranksummary.copy())
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

results = list(itertools.product(game1, game2, game3, game4, game5, game6, \
                                 game7, game8, game9, game10, game11, game12, \
                                 game13, game14, game15, game16, game17, game18))

count = 0
totalscenarios = 2 ** 18
print("total number of scenarios: ", totalscenarios)
print("evaluating scenarios...", end = "")

for result in results:
    for team in teams:
        team.wins = team.currentwins #reset wins for each team for each result
        
    for team in result:
        team.wins += 1
    
    teams.sort(key = lambda x: (x.wins, x.points), reverse = True) #sort teams by wins then points (both descending)

    for i in range(0, len(teams)):
        teams[i].ranksummary[i + 1] += 1

    if count % 100000 == 0:
        print(count, end = "")
        
    if count % 10000 == 0:
        print(".", end = "")
    
    count += 1

print("\n")

#determine playoff odds- teams make playoffs if they are one of the top 4 ranked teams
for team in teams:
    playoffodds = 0
    for rank in range(1, 5):
        playoffodds += (team.ranksummary[rank] / totalscenarios)
    team.playoffodds = round(playoffodds * 100, 2)

teams.sort(key = lambda x: x.playoffodds, reverse = True)

for team in teams:
    for key in team.ranksummary:
        team.ranksummary[key] = round((team.ranksummary[key] / totalscenarios) * 100, 2) #convert to percentage
    print(team.name, str(team.playoffodds) + "%",team.ranksummary)
