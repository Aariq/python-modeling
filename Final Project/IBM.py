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

    def copy(self):
        return turtle(self.age, self.mmod, self.pmod)



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
def create_pop(n, age_range, m_sigma=0.01, p_sigma=0.01):
    assert len(age_range) == 2, "Please supply a range [min, max] to generate random age with"
    pop = np.array(np.empty(n), dtype=object)  # creates array to put turtle objects in.
    for i in range(n):
        pop[i] = random_turtle(m_sigma, p_sigma, [age_range[0], age_range[1]])
    # print("Built random population of", n, "individuals")
    return pop


# Simulate population

# m = float array; birth rates for each age class
# p = float array; survival rates for each age class
# age_classes = float array; cutoffs for the end of each age class in years.
# Anything older than the final age class is assumed to have a survival of 0
# p_sigma and m_sigma = floats, passed to create_pop()

def simulate_pop(start_pop, years, m, p, age_classes, r_sigma=0.15, p_sigma=0.01, m_sigma=0.01):
    assert len(m) == len(p) == len(age_classes), "m, p, and age_classes must be of equal length"
    # copy pop so original is untouched
    pop = np.empty(len(start_pop), dtype=object)
    for i, turt in enumerate(start_pop):  # i is the index, turtle is the actual turtle object
        pop[i] = turt.copy()
    # calculate per-year p
    age_class_len = age_classes - np.append([0], age_classes[:-1])  # figure out how long each age class lasts in years
    per_yr_p = p**(1/age_class_len)  # because AND rule
    per_yr_p = np.append(per_yr_p, 0)  # This ensures that individuals older than last age class die
    # initiate array to save data
    pop_data = np.zeros(years, dtype=int)
    for n in range(years):
        print("Year " + str(n))
        print("Population Size: " + str(len(pop)))
        pop_data[n] = len(pop)  # save population size for this year
        # figure out if it's a good year or a bad year
        r = np.clip(random.gauss(0, r_sigma), -1, None)  # bound random number to be > -1
        p_current = per_yr_p * (r + 1)
        # initialize survival array
        pop_surv = np.empty((len(pop)), dtype=bool)
        # for each turtle, figure out survival
        for i in range(len(pop)):
            # figure out your age-associated survival rate
            x = pop[i].age > np.append(age_classes, [100000]) #need to capture if it is beyond the final age class
            which_class = np.nonzero(x==False)[0][0] #finds the index of the first instance of "False"
            if which_class >= len(age_classes): #if the first appearance is the last index (100000), then its gonna die
                pers_p = 0
            else:
                pers_p = p_current[which_class] * (pop[i].pmod + 1)
                pers_p = np.clip(pers_p, 0, 1) #bound between 0 and 1 b/c its a probability
            #survive
            pop_surv[i] = np.random.choice([True, False], p=[pers_p, 1-pers_p])
        print("Deaths: " + str(len(pop[np.logical_not(pop_surv)])))
        pop = pop[pop_surv]

        # figure out how many births for pulsed-birth type model
        count = np.zeros(len(age_classes), dtype=int)  # initializes array for counting age classes
        # calculate current m on per-year basis
        per_yr_m = m / age_class_len
        m_current = per_yr_m * (r + 1)
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
        births = np.round(np.dot(count, m_current)).astype(np.int)  # round to nearest integer
        print("Births: " + str(births))

        # Grow older
        for i in range(len(pop)):
            pop[i].age = pop[i].age + 1

        # give birth
        pop = np.append(pop, create_pop(n=births, age_range=[0, 0], p_sigma=p_sigma, m_sigma=m_sigma))

        # Stop simulating if all individuals are dead
        if len(pop) == 0:
            print("Population extinct at year " + str(n))
            break
    return pop_data

