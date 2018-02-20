import numpy as np

# age classes:
# 0-6 years
C1 = 7
# 7-14 years
C2 = 8
# 15-27 years
C3 = 13
# 28-52 years
C4 = 25
# 53-74 years
C5 = 22

classes = [C1, C2, C3, C4, C5]

# birth rates
m = np.repeat([0, 0.42, 3.5, 4.3, 4.8], classes)

# survival rates
p = np.repeat([0.76, 0.84, 0.92, 0.95, 0.96], classes)

# initial population
n = np.repeat([0, 100 / C2, 200 / C3, 400 / C4, 500 / C5], classes)

years = 20

# Run Simulation
# initialize n_next
n_next = n[:]
for i in range(years):
    # calculate survival into next age class
    n_next[1:] = n[:-1] * p[:-1]

    # calculate pulsed births
    n_next[0] = np.dot(n_next[1:], m[1:])

    # overwrite n
    n = n_next[:]  # must explicitly copy.  Python makes an alias by default.

    # Display current population
    print("\nPopulation at year", str(i + 1))
    print("0-7 years: ", str(sum(n[0:7])))
    print("7-14 years: ", str(sum(n[7:15])))
    print("15-27 years: ", str(sum(n[15:28])))
    print("28-52 years: ", str(sum(n[28:53])))
    print("53+ years: ", str(sum(n[53:])))
    print("Total: ", str(sum(n)))
    print("Total without juveniles: ", str(sum(n[7:])))
