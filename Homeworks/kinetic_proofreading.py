# Reactions:
#	1. binding: mRNA + tRNA <-> mRNA.tRNA (bF, bR)
#	2. exciting: mRNA.tRNA <-> mRNA.tRNA* (eF, eR)
#	3. Edecay: mRNA.tRNA* <-> mRNA + tRNA (dR, dF)
#	4. product: mRNA.tRNA* <-> product (pF, dR)
# We will take [mRNA] and [tRNA] as given inputs. While reactions #1,3,4 can
# generate them, their concentrations nonetheless never change.
#
# To simplify life, we won't actually simulate #4; all we really care about is
# the steady-state [mRNA.tRNA*]. Since this metabolite simply creates product,
# it serves as a fine stand-in for [product]. And if we did simulate #4, we
# would also need a product-decay term (since otherwise [product] would just
# keep increasing linearly).
# Similarly, in real life transcription will create new mRNA, and other
# processes will keep [tRNA] fairly constant. By simply assuming [mRNA] and
# [tRNA] to be constant, we can ignore those processes.

# Abbreviations:
#	mRNA.tRNA = B (bound complex)
#	mRNA.tRNA* = EB (excited bound complex)


# TO DO:


import sim_infrastructure as si
import numpy as np

def kinetic_proofreading():

    testvals1 = np.array([0.0001, 0.001, 0.01, 0.1, 1])
    testvals2 = np.array([0, 0.001, 0.01, 0.1, 1])
    best_ratio = 9000  # Initialize best_ratio

    bF = 1.0    # assume bF is always 1
    for i in testvals1:
        bR = i
    #bR = 0.1  # .0001, .001, .01, .1 and 1.
        for j in testvals1:
            eF = j
    #eF = 5    # .0001, .001, .01, .1 and 1.
            for k in testvals2:
                eR = k
    #eR = 0    # 0, .001, .01, .1 and 1
                for l in testvals2:
                    dF = l
    #dF = 0    # 0, .001, .01, .1 and 1
                    dR = bR   # same value as bR


                    [correct_EB, OK1] = sim(bF, bR, eF, eR, dF, dR)
                    [wrong_EB, OK2] = sim(bF, bR * 100, eF, eR, dF, dR * 100)

                    if(OK1 and OK2):
                        if(correct_EB / wrong_EB > 9900):
                            print("Ratio of right tRNA to wrong tRNA: " + str(correct_EB / wrong_EB))
                            print("Reaction rates:",
                                  "\n bF = " + str(bF),
                                  "\n bR = " + str(bR),
                                  "\n eF = " + str(eF),
                                  "\n eR = " + str(eR),
                                  "\n dF = " + str(dF),
                                  "\n dR = " + str(dR))
                            if(correct_EB / wrong_EB > best_ratio):
                                best_ratio = correct_EB/wrong_EB
                                best_rates = np.array([bF, bR, eF, eR, dF, dR])
                    else:
                        print("One or both models failed to converge")
    print("\nWinning reaction rates:",
          "\n bF = ", best_rates[0],
          "\n bR = ", best_rates[1],
          "\n eF = ", best_rates[2],
          "\n eR = ", best_rates[3],
          "\n dF = ", best_rates[4],
          "\n dR = ", best_rates[5],
          "\nDiscrimination (right/wrong tRNA): ", best_ratio)

def sim(bF, bR, eF, eR, dF, dR):
    si.clear_sim()
    final_EB=0		# In case the sim does not converge.

    # Add metabolites here.
    si.add_metab('mRNA', 1)
    si.add_metab('tRNA', 1)
    si.add_metab('B', 1)
    si.add_metab('EB', 1)

    si.add_reaction(binding, 'binding', ['mRNA', 'tRNA'], ['B'], [bF, bR])
    si.add_reaction(exciting, 'exciting', ['B'], ['EB'], [eF, eR])
    si.add_reaction(Edecay, 'Edecay', ['mRNA', 'tRNA'], ['EB'], [dF, dR])
    # si.add_reaction (product,'product',['EB','prod'],['prod','EB'], [pF pR])

    [t, y, OK] = si.steady_state_sim(2000)
    final_EB = si.final_val(y, 'EB')
    return (final_EB, OK)

######################################################

# reaction binding: inputs=mRNA, tRNA; outputs=B; params=bF, bR.
#	1. binding: mRNA + tRNA <-> mRNA.tRNA (bF, bR)

def binding(t, inputs, outputs, params):
    import sim_library as sl
    sl.checkInputs('binding', 2, 1, 2, inputs, outputs, params)
    mRNA, tRNA = inputs
    [B] = outputs
    bF, bR = params

    # Note that we do not assign any flow on the inputs; they are assumed to
    # have constant concentration.
    return ([[], [bF * mRNA * tRNA - bR * B]])

# reaction exciting: inputs=B; outputs=EB; params=eR, eF.
#	2. exciting: mRNA.tRNA <-> mRNA.tRNA* (eF, eR)

def exciting(t, inputs, outputs, params):
    import sim_library as sl
    sl.checkInputs('exciting', 1, 1, 2, inputs, outputs, params)
    [B] = inputs
    [EB] = outputs
    eF, eR = params

    d = eF * B - eR * EB	# d(EB)/dt
    return ([[-d], [d]])

# reaction Edecay; inputs=mRNA, tRNA; outputs=EB, params=dF, dR.
#	3. Edecay: mRNA.tRNA* <-> mRNA + tRNA (dR, dF)

def Edecay(t, inputs, outputs, params):
    import sim_library as sl
    sl.checkInputs('Edecay', 2,1,2, inputs, outputs, params)
    mRNA, tRNA = inputs
    [EB] = outputs
    dF, dR = params
    return ([[], [dF * mRNA * tRNA - dR * EB]])

# reaction product; inputs=EB, product; outputs=product,EB, params=pF, pR.
#	4. product: mRNA.tRNA* <-> product (pF, pR)

def product(t, inputs, outputs, params):
    import sim_library as sl
    sl.checkInputs('product', 2, 1, 2, inputs, outputs, params)
    EB, product = inputs
    pF, pR = params

    d = pF * EB - pR * product
    return ([[], [d,-d]])


kinetic_proofreading()
