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


def random_turtle(m_sigma=0.01, p_sigma=0.01, age_range=[0, 0]):
    assert len(age_range) == 2, "Please supply a range [min, max] to generate random age with"
    min_age = age_range[0]
    max_age = age_range[1]
    assert isinstance(min_age, int) and isinstance(max_age, int), "Min and max age should be integers"
    age = random.randint(min_age, max_age)
    mmod = random.gauss(0, m_sigma)
    pmod = random.gauss(0, p_sigma)
    return turtle(age, mmod, pmod)


# Properties of population
# n = int; number of individuals
# age_range; passed on to random_turtle()
# m_sigma, p_sigma; passed on to random_turtle()
def create_pop(n, age_range, m_sigma=.01, p_sigma=.01):
    assert len(age_range) == 2, "Please supply a range [min, max] to generate random age with"
    pop = np.array(np.empty(n), dtype=object)  # creates array to put turtle objects in.
    for i in range(n):
        pop[i] = random_turtle(m_sigma, p_sigma, [age_range[0], age_range[1]])
    #print("Built random population of", n, "individuals")
    return pop


# Simulate population


# m = float array; birth rates for each age class
# p = float array; survival rates for each age class
# age_classes = float array; cutoffs for the end of each age class in years.
# Anything older than the final age class is assumed to have a survival of 0
# f_sigma and s_sigma = floats.
# Parameters used to generate random variation in survival and birth rate for each individual

def simulate_pop(pop, years, m, p, age_classes, r_sigma=0.15):
    assert len(m) == len(p) == len(age_classes), "m, p, and age_classes must be of equal length"
    # calculate per-year m and p
    age_class_len = age_classes - np.append([0], age_classes[:-1])
    per_yr_p = p**(1/age_class_len)
    per_yr_p = np.append(per_yr_p, 0) #This ensures that individuals older than last age class die
    # initiate array to save data
    pop_data = np.zeros(years, dtype=int)
    for n in range(years):
        print("Year " + str(n))
        print("Population Size: " + str(len(pop)))
        pop_data[n] = len(pop)
        #figure out if it's a good year or a bad year
        r = np.clip(random.gauss(0, r_sigma), -1, None)  # bound random number to be > -1
        #initialize survival array
        pop_surv = np.array([], dtype=bool)
        #for each turtle, figure out survival
        for i in range(len(pop)):
            #figure out your age-associated survival rate
            x = pop[i].age > np.append(age_classes, [100000]) #need to capture if it is beyond the final age class
            which_class = np.nonzero(x==False)[0][0] #finds the index of the first instance of "False"
            if which_class >= len(age_classes): #if the first appearance is the last index (100000), then its gonna die
                pers_p = 0
            else:
                pers_p = per_yr_p[which_class] + pop[i].pmod
                #factor in r and cap at 1
                pers_p = np.clip(pers_p * (r + 1), 0, 1) #bound between 0 and 1 b/c its a probability

            #survive
            surv = np.random.choice([True, False], p=[pers_p, 1-pers_p])
            pop_surv = np.append(pop_surv, surv)
        print("Deaths: " + str(len(pop[np.logical_not(pop_surv)])))
        pop = pop[pop_surv]


        #figure out how many births
        count = np.zeros(len(age_classes), dtype=int)  # initialize array for counting age classes
        m_current = m * (r + 1)  # yearly m
        per_yr_m = m_current / age_class_len  # for pulsed-birth type model.
        for i in range(len(pop)):
            # figure out age-associated fecundity
            # Since birth-rates (m) are not probabilities, I'm not sure how to calculate per year birth-rates and use
            # them on an individual basis.

            # Instead, I figure out how many individuals are in each age class, and then use a dot product to
            # calculate the number of births.  Then I can create that many turtles and append them to the population.
            # This means I won't be able to use individual the fecundity bonus/penalty.
            x = pop[i].age > age_classes
            which_class = np.nonzero(x == False)[0][0]
            count[which_class] = count[which_class] + 1  # populates age class array with counts of turtles
        births = np.round(np.dot(count, per_yr_m)).astype(np.int)  # round to nearest integer
        print("Births: " + str(births))

        #age
        for i in range(len(pop)):
            pop[i].age = pop[i].age + 1

        #give birth
        pop = np.append(pop, create_pop(n=births, age_range=[0, 0]))

        #Stop simulating if all individuals are dead
        if len(pop) == 0:
            print("Population extinct at year " + str(n))
            break
    return pop_data


# birth rates
m = np.array([0, 0.42, 3.5, 4.3, 4.8])
# survival rates
p = np.array([0.76, 0.84, 0.92, 0.95, 0.96])

# age classes:
# 0-6 years; 0 individuals
# 7-14 years; 100
# 15-27 years; 200
# 28-52 years; 400
# 53-74 years; 500

classes = np.array([6, 14, 27, 52, 74])
n_initial = np.array([0, 100, 200, 400, 500])
class_len = classes - np.append([0], classes[:-1])


#turtletown = create_pop(n=10, age_range=[0, 100])
turtletown = create_pop(n=100, age_range=[7, 14])
turtletown = np.append(turtletown, create_pop(n=200, age_range=[15, 27]))
turtletown = np.append(turtletown, create_pop(n=400, age_range=[28, 52]))
turtletown = np.append(turtletown, create_pop(n=500, age_range=[53, 74]))

test = simulate_pop(turtletown, 100, m=m, p=p, age_classes=classes, r_sigma=0.2)
print(test)
