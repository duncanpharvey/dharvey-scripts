import scipy.integrate as integrate
import numpy as np
import math

mu1 = 106.16
mu2 = 85.54
sd1 = 28.33
sd2 = 25.77

#Lower limits of integrals set at 0 and upper limit set to 200 since that is the range of realistic scores
result = integrate.dblquad(lambda x, y: (1 / (2 * math.pi * sd1 * sd2)) * \
                            np.exp((-1 / (2 * math.pow(sd2, 2))) * math.pow(y - mu2, 2)) * np.exp((-1 / (2 * math.pow(sd1, 2))) * math.pow(x - mu1, 2)), \
                            0, 200, lambda x: 0, lambda x: x)


result2 = round(result[0] * 100, 2)
print("team1 wins:", str(100 - result2) + "%")
print("team2 wins:", str(result2) + "%")

