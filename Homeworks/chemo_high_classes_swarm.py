# This file takes bits and snippets from chemo_high.py. It rewrites them to
# make them object oriented, instantiate multiple EColi objects, and let
# them move independently

import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
#TIME_STEP = 1
#N_ECOLI = 15
#I edited chemotaxis() to take number of ecoli as an argument.

class Ecoli:
    # You must write this function yourself.
    # Your instance variables must be (at a minimum) x, y, Vx, Vy and
    # concentration (i.e., the memory)
    def __init__(self, x = None, y = None):
        #initiate with random location
        #self.x = random.uniform(0, 100)
        #self.y = random.uniform(0, 100)

        #initiate at lower left
        self.x = 0
        self.y = 0

        #and random direction (actually doesn't need to be random.  Chemotaxis() seeds random directions)
        xdir = random.uniform(-1, 1)
        ydir = random.uniform(-1, 1)
        adj = 1 / ((xdir * xdir + ydir * ydir) ** .5)
        self.Vx = xdir * adj
        self.Vy = ydir * adj
        #self.Vx, self.Vy = self.pick_random_direction() # could also do this, but then prints a string

        #initiate sugar memory
        self.sugar = sample(self.x, self.y)

        # OK, I wrote this part of __init__ for you. It prepares the [x,y]
        # locations on our path for swim() to update and display() to draw.
        self.saveX = []
        self.saveY = []

    # This function is provided. It returns a printable representation
    # of the Ecoli object as a string.
    # It uses the instance variables x, y, Vx and Vy.
    def __repr__(self):
        dist = ((self.x-50)**2 + (self.y-50)**2)**0.5
        s = "x, y = ({:.2f}, {:.2f}). Vx, Vy = ({:.2f}, {:.2f}), distance = {:.2f}, and local [sugar] = {:.4f}"\
            .format(self.x, self.y, self.Vx, self.Vy, dist, sample(self.x, self.y))
        return s

    # Pick a random direction, and update our internal velocity vector (i.e.,
    # Vx and Vy). Remember that the swimming speed must always be one; it's
    # only the direction that you're picking. In other words, you should ensure
    # that Vx**2 + Vy**2 = 1.
    # This is for you to write.
    def pick_random_direction(self):
        # First pick the x and y components of the direction.
        xdir = random.uniform(-1, 1)
        ydir = random.uniform(-1, 1)

        # Now normalize to have magnitude=1.
        adj = 1 / ((xdir * xdir + ydir * ydir) ** .5)
        print("new direction: x = {:.3f}, y = {:.3f}".format(xdir * adj, ydir * adj))
        return (xdir * adj, ydir * adj)

    # Swim for one TIME_STEP at the current (Vx,Vy) direction,
    # and update the new x,y location.
    # I've writen this to allow the user to specify how long Ecoli swims before
    # re-evaluating it's direction (tstep)
    def swim(self, tstep = 1):
        self.x = self.x + self.Vx * tstep
        self.y = self.y + self.Vy * tstep

        # OK, I wrote this part for you.
        self.saveX.append(self.x)
        self.saveY.append(self.y)

    # This function doesn't return any values. What it does:
    #  - samples the concentration at the current location by calling sample()
    #  - decides whether to tumble or not (by comparing the new sugar
    #    concentration with our last one)
    #  - picks a new random direction if needed, with pick_random_direction()
    #  - Saves the new concentration in our memory.
    # Why put these into a class member function? It helps us encapsulate the
    # inner workings of the class (things like the location, memory, etc) and
    # not let them be visible outside of the class.
    def sampleAndTumble(self):
        sugarnew = sample(self.x, self.y)
        if sugarnew <= self.sugar:
            self.Vx, self.Vy = self.pick_random_direction()
        self.sugar = sugarnew

# The routine that implements high-level chemotaxis
# I edited this so the user can specify the total runtime of the simulation (t) and
# how often the Ecoli swim between concentration checks (tstep).
# t is passed on to self.swim()

def chemotaxis(n, t=200, tstep=1):
    # Instantiate an array of E-coli objects. Pick the initial random direction
    # for each one.
    random.seed(0)
    Es = np.empty(n, dtype=object)
    for i in range(n):
        Es[i] = Ecoli()
        Es[i].pick_random_direction()
    print("Initially: ", Es)

    # Now for the main loop.
    for i in range(t):		# for each timepoint...
        for i,E in enumerate(Es):   # for each Ecoli object...
            print('EColi #', i, ':')
            E.swim(tstep)			# tell it to swim for a while
            print(E)
            # tell it to re-evaluate its direction and tumble if needed.
            E.sampleAndTumble()

    # plot the swarm's motion.
    display(Es)

# Return the sugar concentration at any [x,y] location.
# Our field has sugar at x=50, y=50.
# It then tails off slowly around that.
def sample (x,y):
    distance = ((x-50)**2 + (y-50)**2) ** 0.5
    distance = max (distance, 1)	# To avoid /0 if x,y=(50,50)
    return (10/distance)		# So small distance => return big number

###############################################################
# This part of the file deals with showing an animated movie of our chemotaxis.
# It is based on Python's matplotlib package (which does all kinds of plotting),
# and specifically on the matplotlib.animate package (which focuses on
# animation).
###############################################################

# The top-level animation function.
# It takes a single argument; an array of Ecoli objects to animate.
# Each of these objects must have saveX and saveY (which, taken together,
# form a list of [x,y] locations on the Ecoli's path).
def display(Es):
    # First, create the figure, axes, etc.
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.animation as animation
    fig, axes = plt.subplots()
    xmin=0; xmax=1; ymin=0; ymax=1
    axes.axis ([xmin,xmax,ymin,ymax])	# Set the axes to range from [-1,1].
    axes.set_autoscale_on(False)	# Make sure they stay at [-1,1].

    # Create/draw the sugar object in the middle. It never moves.
    axes.add_patch (patches.Circle ((.5,.5), radius=.03, facecolor='r'))

    # The globals are to communicate with per_frame()
    global displayEs, pats, nInterps
    displayEs = Es

    # Now create the bacteria icon (which will move around)
    pats = []
    for p in range(Es.size):
        pat = patches.Rectangle ((0,0),.03,.03, facecolor='b')
        axes.add_patch (pat)
        pats.append(pat)

    print ("Starting animation")
    # Note that FuncAnimation is an *object*, so we must assign it to something
    # "blit=True" is a trick that makes the animation run fast. It says to
    # draw the axes and the sugar once only, and then in every frame just
    # redraw the EColi.
    nInterps=4		# Numb of interpolated frames between each saveXY point
    nFrames = (nInterps+1)*(len(Es[0].saveX)-1)
    ani = animation.FuncAnimation(fig, per_frame, frames=nFrames,
                                  interval=1, blit=True, repeat=False)
    print ("Finished animation")
    plt.show()

# Our per-frame animation function. It takes the frame number and returns a
# list of objects that have moved (in fact there is only one; the EColi).
# It also must update those object(s), which we do with the pat.set_x and set_y.
#
# The hard part is figuring out where to draw the bacteria.
# Consider 3 data items and nInterps=4.
# Then frame #0 is data[0]; #1-4 mix [0] and [1]; #5 is data[1]; #6-9
# mix [1] and [2], and #10 is data[2], with 11 frames total.
def per_frame(f):
    global pats, displayEs, nInterps

    recip = 1/(nInterps+1)
    i0 = int (f*recip+.00001)
    alpha = (f - i0*(nInterps+1)) * recip
    for i,E in enumerate(displayEs):
        x = E.saveX[i0] + (E.saveX[i0+1]-E.saveX[i0])*alpha
        y = E.saveY[i0] + (E.saveY[i0+1]-E.saveY[i0])*alpha
        #print ("Animating frame #",f,"->",x,y)
        pats[i].set_x (x/100 - .015)    # x/100 is the rectangle's center;
        pats[i].set_y (y/100 - .015)    # -.015  gets you the lower-left corner

    return pats		# Always return a list of the changed items.

chemotaxis(20, t=200, tstep=3)
