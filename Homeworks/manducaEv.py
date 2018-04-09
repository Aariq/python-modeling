# This is the top-level file for Manduca optimization.
# Its one and only entry point is manducaEv(), which it calls itself
# automatically upon loading.

import numpy as np
import random
import manducaFitness

#random.seed(55)
#np.random.seed(55)

MUSCLE_ON = 100
MAX_MUTATIONS = 10

# run_generation(pop, n_matings, n_mutations) runs one generation of a genetic
# algorithm. It:
#   - starts with the given population.
#   - makes n_matings calls to the function parent1.mate(parent2); each time
#     picking a random pair of parents from population to mate.
#   - calls parent.copy().mutate() n_mutations times; each time picking a
#     parent randomly from the population.
#   - after adding the new children from mate() and mutate() to the population,
#     prunes the population down to the pop_size fittest individuals (with some
#     randomness).
#   - returns the resultant population, ordered by fitness (i.e., population[0]
#     is the most fit).


def run_generation(pop, n_matings, n_mutations):
    pop_size = pop.size # Remember the size, even as we add & cull new children
    print("Running a generation with", pop_size, "individuals")
    print("Incoming fitnesses: [",
          ",".join(["{:.3f}".format(p.fitness()) for p in pop]), "]")

    # Create an array of new_children. First, fill it in with the matings.
    # Each mating is two randomly-chosen parents.
    new_children = np.empty(n_matings+n_mutations, dtype=object)
    for i in range(n_matings):
        p1 = pop[random.randrange(0, pop_size)]
        p2 = pop[random.randrange(0, pop_size)]
        child = p1.mate(p2)   #you will have to write mate()
        new_children[i] = child

    # Next, add the mutations (again, mutating random parents).
    for i in range(n_mutations):
        p = pop[random.randrange(0, pop_size)]
        child = p.copy()
        child.mutate()     #you will have to write mutate()
        new_children[n_matings+i] = child

    # Add the new children to the population.
    print("We created",len(new_children), "new children [",
           ",".join(["{:.3f}".format(c.fitness()) for c in new_children]),"]")
    pop = np.append (pop, new_children)
    print("The entire population now has",pop.size,"individuals")

    # sort by fitness.
    fit = np.array([pop[i].fitness() for i in range(pop.size)])
    indices = np.argsort(fit)
    indices = indices[-1::-1]	# Reverse it, so the fittest is now first.
    pop = pop[indices]
    fit = fit[indices]
    fit -= fit[-1]  # offset everyone so the least fit has fitness=0
    print("Sorted fitnesses: [",
          ",".join(["{:.3f}".format(p.fitness()) for p in pop]),"]")

    # Always keep the best 10 individuals
    new_pop = np.empty(pop_size, dtype=object)
    new_pop[0:10] = pop[0:10]

    # Remove all duplicates (after the 10 we've already done)
    fittest = pop[0]
    pop_end = pop.size
    i = 10
    while i < pop_end:
        if pop[i] == fittest:
            pop[i:pop_end-1] = pop[i+1:pop_end]
            fit[i:pop_end-1] = fit[i+1:pop_end]
            pop_end -= 1
        else:
            i += 1
            
    # Pick 3 more completely randomly
    new_pop[10:13] = np.random.choice(pop[10:pop_end], 3, replace=False)

    # Pick the rest randomly, but weighted by fitness.
    sum = np.sum(fit[10:pop_end])
    probs = fit[10:pop_end] / sum
    new_pop[13:] = np.random.choice(pop[10:pop_end], pop_size-13,
                                     replace=False, p=probs)

    print("Outgoing fitnesses: [",
          ",".join(["{:.3f}".format(p.fitness()) for p in new_pop]), "]")
    return new_pop

# This is the function that you will (mostly) write yourself.
def manducaEv(n_gen, pop_size, n_matings, n_mutations, seed):
    # Seed the random-number generator so that we get the same "random"
    # numbers every time :-)
    random.seed(seed)
    np.random.seed(seed)

    # First create a population of random individuals.
    print("In manducaRun")
    pop = np.array(np.empty(pop_size), dtype=object)  # creates array to put manduca objects in.
    for i in range(pop_size):
        pop[i] = random_manduca()
    print("Built random population of", pop_size, "individuals")

    # Then run evolution.
    for i in range(n_gen):
        pop = run_generation (pop, n_matings, n_mutations)
        print('After generation #', i, '/', n_gen, ', best=', pop[0].fitness(), "\n")
        if i % 20 == 0:
            print("Generation=", i, ", best=", pop[0])

    print("All done. Best=", pop[0])

# Build a random individual. Basically, every leg & every muscle is random.
def random_manduca(n_time_seg=10):
    legs = np.empty((n_time_seg, 5))
    musc = np.empty((n_time_seg, 4))
    for r in range(n_time_seg):
        for l in range(5):
            legs[r, l] = random.randrange(0, 2)  # 0 or 1
        for m in range(4):
            musc[r, m] = random.randrange(0, 2) * MUSCLE_ON
    return Manduca(legs, musc)

# A useful little utility function that anyone can use.
# Read a text file with one line per time segment; each line looks like
#          0 0 1 1 0 | 100 100 0 100
# Return two arrays: legs and muscles.
def read_from_file (file):
    ar = np.loadtxt (file, comments='#', dtype=str)
    assert (ar.shape[1]==10) # 5 legs, "|', 4 muscles.
    assert ((ar[:,5]=='|').all()) # Every line has the "|" separator.
    legs = ar[:,0:5].astype (np.int)
    musc = ar[:,6:10].astype (np.int)
    return (legs,musc)

# Another useful little utility function that anyone can use.
# Read a text file with one line per time segment, using read_from_file() just
# above. Then animate it, using manducaGraph.py
def read_from_file_and_graph (file):
    import manducaGraph
    (legs, musc) = read_from_file (file)
    (fitn,details) = manducaFitness.manducaFitness(legs, musc, 2)
    manducaGraph.manducaGraph (0, 30, 'manduca_output_long.txt', 'M.sexta')

# Our class definition for the Manduca.
class Manduca:
    def __init__(self, legs=None, muscles=None):
        self.legs = np.copy(legs)
        self.muscles = np.copy(muscles)
        self.fitn = -1

    def __eq__(self, other):
        return (np.array_equal(self.legs, other.legs) and
                np.array_equal(self.muscles, other.muscles))

    def __repr__(self):
        str = "\n   legs   |     muscles\n"
        for r in range(self.legs.shape[0]):	# for each row
            str += (" ".join(["{:>1}".format(int(l)) for l in self.legs[r, :]]) +
                    " | " +
                    " ".join(["{:>3}".format(int(l)) for l in self.muscles[r, :]]) +
                    "\n")
        return str

    def fitness(self):
        if self.fitn == -1:
            [self.fitn, details] = manducaFitness.manducaFitness(self.legs, self.muscles)
        return self.fitn

    # Make an actual copy, so that the caller can modify the copy without
    # modifying the original.

    def copy(self):
        return (Manduca(np.copy(self.legs), np.copy(self.muscles)))

    # Mutate ourself.
    # This is the next function that you write yourself.
    # First randomly choose the number of mutations (1 up to MAX_MUTATIONS)
    # Then, for each of them, choose to either
    #	- flip a random leg-locked
    #	- flip a random muscle-on
    #	- do the secret-sauce mutation if desired.

    def mutate(self):
        n_mutations = random.randrange(1, MAX_MUTATIONS)
        print(str(n_mutations) + " mutations")
        #decide how many are leg and which are muscle mutations
        n_leg = np.random.choice(n_mutations, 1)
        n_muscle = n_mutations - n_leg

        #mutate legs:
        n = 0
        while n < n_leg:
            row = random.randint(0, 9)
            col = random.randint(0, 4)
            if self.legs[row, col] == 1.:
                self.legs[row, col] = 0
            else:
                self.legs[row, col] = 1
            n = n+1

        #mutate muscles:
        k = 0
        while k < n_muscle:
            row = random.randint(0, 9)
            col = random.randint(0, 3)
            if self.muscles[row, col] == 100:
                self.muscles[row, col] = 0
            else:
                self.muscles[row, col] = 100
            k = k+1


    # Pick entire rows from one parent or the other. Each row of the child comes
    # from the first parent or the second (with equal likelihood). 
    # This is the final function that you write yourself.
    def mate(self, parent2):


#manducaEv (n_gen=5000, pop_size=20, n_matings=10, n_mutations=10, seed=1)
test = random_manduca(10)
print(test)
test2 = Manduca.copy(test)
test2.mutate()
print(test2)
