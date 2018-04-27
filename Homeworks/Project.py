import numpy as np
import random


# Properties of individuals
class turtle:
    def __init__(self, age=None, mmod=None, pmod=None):
        self.age = age
        self.mmod = mmod  # modifier on fecundity
        self.pmod = pmod  # modifier on survival

    def __eq__(self, other):
        return self.age == other.age and self.mmod == other.mmod and self.pmod == other.pmod

    def __repr__(self):
        repstr = "Age: {:}\nFecundity bonus/penalty: {:.3f}\nSurvival bonus/penalty: {:.3f}"\
            .format(self.age, self.mmod, self.pmod)
        return repstr


def random_turtle(m_sigma, p_sigma, rand_age=False):
    if rand_age==False:
        age = 0
    else:
        assert len(rand_age) == 2, "Please supply a range [min, max] to generate random age with"
        min_age = rand_age[0]
        max_age = rand_age[1]
        assert isinstance(min_age, int) and isinstance(max_age, int), "Min and max age should be integers"
        age = random.randint(min_age, max_age)
    mmod = random.gauss(0, m_sigma) #f_sigma and s_sigma will need to be defined globally
    pmod = random.gauss(0, p_sigma)
    return turtle(age, mmod, pmod)


# Properties of population
# n = int; number of individuals
# age_range; passed on to random_turtle()
# m_sigma, p_sigma; passed on to random_turtle()
def create_pop(n, age_range, m_sigma=.1, p_sigma=.1):
    assert len(age_range) == 2, "Please supply a range [min, max] to generate random age with"
    pop = np.array(np.empty(n), dtype=object)  # creates array to put turtle objects in.
    for i in range(n):
        pop[i] = random_turtle(m_sigma, p_sigma, [age_range[0], age_range[1]])
    print("Built random population of", n, "individuals")
    return(pop)


# Simulate population


# m = float array; birth rates for each age class
# p = float array; survival rates for each age class
# age_classes = float array; cutoffs for the end of each age class in years.
# Anything older than the final age class is assumed to have a survival of 0 and birth rate of 0
# f_sigma and s_sigma = floats.
# Parameters used to generate random variation in survival and birth rate for each individual

def simulate_pop(pop, years, m, p, age_classes):
    assert len(m) == len(p) == len(age_classes), "m, p, and age_classes must be of equal length"
    #calculate per-year m and p
    age_class_len = age_classes - np.append([0], classes[:-1])
    death_prob = 1-p
    per_yr_p = 1-(death_prob/age_class_len)
    per_yr_p = np.append(per_yr_p) #might be easier this way to ensure that olds die
    # for each year
    for n in range(years):
        #figure out if it's a good year or a bad year
        #for each turtle
        for i in range(len(pop)):
            #figure out your age-associated survival rate
            x = pop[i].age > np.append(age_classes, [100000]) #need to capture if it is beyond the final age class
            which_class = np.nonzero(x==False)[0][0] #finds the index of the first instance of "False"
            if which_class >= len(age_classes): #if the first appearance is the last index (100000), then its gonna die
                pers_m = 0
                pers_p = 0
            else:
                pers_p = per_yr_p[which_class] + pop[i].pmod #need to set bound at 1
                #pers_m = per_yr_m[which_class] + pop[i].mmod #can't be lower than 0
                print(pers_p)
            #survive

            #np.random.choice([1,0], p=[p])
            #figure out what your age-associated birth rate (+penalty/bonus) is
            #give birth
            #age
            pop[i].age = pop[i].age + 1 #done


# birth rates
m = np.array([0, 0.42, 3.5, 4.3, 4.8])
# survival rates
p = np.array([0.76, 0.84, 0.92, 0.95, 0.96])

# age classes:
# 0-6 years (7)
# 7-14 years (7)
# 15-27 years
# 28-52 years
# 53-74 years

classes = np.array([6, 14, 27, 52, 74])

turtletown = create_pop(n=1, age_range=[0, 100])
#print(turtletown)
simulate_pop(turtletown, 10, m=m, p=p, age_classes=classes)
