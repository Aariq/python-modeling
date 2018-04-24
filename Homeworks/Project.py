import numpy as np
import random

# Properties of individuals
class turtle:
    def __init__(self, age=None, fmod=None, smod=None):
        self.age = age
        self.fmod = fmod  # modifier on fecundity
        self.smod = smod  # modifier on survival

    def __eq__(self, other):
        return self.age == other.age and self.fmod == other.fmod and self.smod == other.smod

    def __repr__(self):
        repstr = "Age: {:}\nFecundity bonus/penalty: {:.3f}\nSurvival bonus/penalty: {:.3f}"\
            .format(self.age, self.fmod, self.smod)
        return repstr

def random_turtle(max_age, f_sigma, s_sigma):
    age = random.randint(0, max_age)
    fmod = random.gauss(0, f_sigma)
    smod = random.gauss(0, s_sigma)
    return turtle(age, fmod, smod)

# Properties of population
# maybe some of these things go in the simulation function rather than here
def create_pop(n, m, p, age_classes):
    assert len(m) == len(p) == len(age_classes), "m, p, and age_classes must be of equal length"
    pop = np.array(np.empty(n), dtype=object)  # creates array to put turtle objects in.
    for i in range(n):
        pop[i] = random_manduca()
    print("Built random population of", pop_size, "individuals")

# do some checks to make sure the lengths of things match
# figure out max_age from age_classes and pass to turtle()
# make a bunch of turtles using the turtle() function
# do some calculations to set up per year m and p
n_i = 10  # number of individuals to start with
m = np.array([0, 0.42, 3.5, 4.3, 4.8])  # array of class-based birth rates
p = np.array([0.76, 0.84, 0.92, 0.95, 0.96])  # array of class-based survival probabilities
age_classes = [7, 8, 13, 25, 22]  # vector of age class cutoffs??

# properties of simulation
# def turtle_sim(years, y_sigma)
years = 100  # how long to run the simulation, if None, run until everyone dies or pop stabilizes (see HW3.py)
y_sigma = 0.15  # add some stochasticity year to year

chester = turtle(5, .1657576576575765765, .2)
print(chester)
bob = random_turtle(100, .2, .15)
print(bob)