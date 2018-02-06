# Problem 1
# birth rates
m0 = 0  # age class 0-1
m1 = 1  # 1-2
m2 = 5 / 6  # 2-3
m3 = 0  # 3-4

# survival rates

p0 = 0.6
p1 = 0.8
p2 = 2 / 3
p3 = 0

# number of individuals

n0 = 0
n1 = 1200
n2 = 900
n3 = 900

# first they survive, then pulsed birth

# survival.  Using t0, t1, etc. for year t+1
t1 = n0 * p0
t2 = n1 * p1
t3 = n2 * p2

# births
t0 = (t1 * m1) + (t2 * m2) + (t3 * m3)

print("0-1: " + str(t0))
print("1-2: " + str(t1))
print("2-3: " + str(t2))
print("3-4: " + str(t3))
#########################

# Problem 2: do a for loop

years = 70

# starting population
n0 = 0
n1 = 1200
n2 = 900
n3 = 900

for i in range(years):
    # survival
    t1 = n0 * p0
    t2 = n1 * p1
    t3 = n2 * p2

    # births
    t0 = (t1 * m1) + (t2 * m2) + (t3 * m3)

    # overwrite starting population for next year
    n0 = t0
    n1 = t1
    n2 = t2
    n3 = t3

    # print results of every year
    print("\nYear " + str(i+1))
    print("0-1: " + str(n0))
    print("1-2: " + str(n1))
    print("2-3: " + str(n2))
    print("3-4: " + str(n3))
    print("Total: " + str(n0+n1+n2+n3))
############################

# problem 3: re-run with m2 = .9

m2 = .9

years = 70

# starting population
n0 = 0
n1 = 1200
n2 = 900
n3 = 900

for i in range(years):
    # survival
    t1 = n0 * p0
    t2 = n1 * p1
    t3 = n2 * p2

    # births
    t0 = (t1 * m1) + (t2 * m2) + (t3 * m3)

    # overwrite starting population
    n0 = t0
    n1 = t1
    n2 = t2
    n3 = t3

    # print results of every year
    print("\nYear " + str(i+1))
    print("0-1: " + str(n0))
    print("1-2: " + str(n1))
    print("2-3: " + str(n2))
    print("3-4: " + str(n3))
    print("Total: " + str(n0+n1+n2+n3))