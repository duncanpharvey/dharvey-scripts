import scipy.integrate as integrate
import numpy as np
import math

mu1 = 94.06
mu2 = 104.45
sd1 = 16.88
sd2 = 19.3

#Lower limits of integrals set at 0 and upper limit set to 200 since that is the range of realistic scores
result = integrate.dblquad(lambda x, y: (1 / (2 * math.pi * sd1 * sd2)) * \
                            np.exp((-1 / (2 * math.pow(sd2, 2))) * math.pow(y - mu2, 2)) * np.exp((-1 / (2 * math.pow(sd1, 2))) * math.pow(x - mu1, 2)), \
                            0, 200, lambda x: 0, lambda x: x)


result2 = round(result[0] * 100, 2)
print("Mathematical Analysis:")
print("team1 wins:", str(round(100 - (result[0] * 100), 2)) + "%")
print("team2 wins:", str(round(result2, 2)) + "%")

trials = 100000

a = np.random.normal(mu1, sd1, trials)
b = np.random.normal(mu2, sd2, trials)

summary = [0, 0]
for x in range(trials):
    scorea = a[x]
    scoreb = b[x]

    if scorea > scoreb:
        summary[0] += 1
    elif scoreb > scorea:
        summary[1] += 1
    else:
        summary[0] += 0.5
        summary[1] += 0.5

print("\nStatistical Analysis")
print("team1 wins:", str(round((summary[0] / trials) * 100, 2)) + "%")
print("team2 wins:", str(round((summary[1] / trials) * 100, 2)) + "%")

