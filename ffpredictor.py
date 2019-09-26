import scipy.integrate as integrate
import numpy as np
import math

mu1 = 95.84
mu2 = 85.43
sd1 = 26.98
sd2 = 19.5

#Lower limits of integrals set at 0 and upper limit set to 200 since that is the range of realistic scores
result = integrate.dblquad(lambda x, y: (1 / (2 * math.pi * sd1 * sd2)) * \
                            np.exp((-1 / (2 * math.pow(sd2, 2))) * math.pow(y - mu2, 2)) * np.exp((-1 / (2 * math.pow(sd1, 2))) * math.pow(x - mu1, 2)), \
                            0, 200, lambda x: 0, lambda x: x)


result2 = round(result[0] * 100, 2)
print(result2) #percent chance team 2 wins

