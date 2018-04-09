#### PROBLEM 1 ####
#Code from HW2_problem1.py
import random
import numpy as np
# birth rates
m = np.array([0, 1, 5/6, 0])
# survival rates
p = np.array([0.6, 0.8, 5/6, 0])
# initial population
n = np.array([750, 450, 360, 240])
# initialize vector to hold next generation
n_next = np.array([0, 0, 0, 0])

years = 5

# parameter for stochasticity
sigma = 0

for i in range(years):
    # Generate random number
    r = np.clip(random.gauss(0, sigma), -1, None)  # bound random number to be > -1

    m_current = m * (r + 1)
    p_current = np.clip(p * (r + 1), None, 1)  # don't allow any p's to be > 1

    n_next[1:4] = np.round(n[0:3] * p_current[0:3])  # round to nearest individual

    n_next[0] = np.round(np.dot(n_next[1:4], m_current[1:4]))  # round to nearest individual

    # overwrite n for next year
    n = n_next
    print(n)

###################
#### PROBLEM 2 ####

# birth rates
m = np.array([0, 1, 5/6, 0])
# survival rates
p = np.array([0.6, 0.8, 5/6, 0])
# initial population
n = np.array([750, 450, 360, 240])
# initialize vector to hold next generation
n_next = np.array([0, 0, 0, 0])

# parameter for stochasticity
sigma = 0.15

random.seed(0)

i = 0
while(n.sum() != 0):
    # Generate random number
    r = np.clip(random.gauss(0, sigma), -1, None)  # bound random number to be > -1

    m_current = m * (r + 1)
    p_current = np.clip(p * (r + 1), None, 1)  # don't allow any p's to be > 1

    n_next[1:4] = np.round(n[0:3] * p_current[0:3])  # round to nearest individual

    n_next[0] = np.round(np.dot(n_next[1:4], m_current[1:4]))  # round to nearest individual

    # overwrite n for next year
    n = n_next
    print("Year" + str(i))
    print(n)
    i = i + 1
# Ends at year 2709
###################
#### PROBLEM 3 ####

# birth rates
m = np.array([0, 1, 5/6, 0])
# survival rates
p = np.array([0.6, 0.8, 5/6, 0])
# initial population
n = np.array([750, 450, 360, 240])
# initialize vector to hold next generation
n_next = np.array([0, 0, 0, 0])

# parameter for stochasticity
sigma = 0.25

random.seed(0)

i = 0
while(n.sum() != 0):
    # Generate random number
    r = np.clip(random.gauss(0, sigma), -1, None)  # bound random number to be > -1

    m_current = m * (r + 1)
    p_current = np.clip(p * (r + 1), None, 1)  # don't allow any p's to be > 1

    n_next[1:4] = np.round(n[0:3] * p_current[0:3])  # round to nearest individual

    n_next[0] = np.round(np.dot(n_next[1:4], m_current[1:4]))  # round to nearest individual

    # overwrite n for next year
    n = n_next
    print("Year" + str(i))
    print(n)
    i = i + 1

    #Ends at year 80