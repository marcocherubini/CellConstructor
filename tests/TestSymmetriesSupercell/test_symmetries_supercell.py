# -*- coding: utf-8 -*-
import numpy as np

import cellconstructor as CC
import cellconstructor.Phonons
import cellconstructor.symmetries


# ---- INPUT PARAMETERS -----
FILDYN = "SnSe.dyn.2x2x2"
NQIRR = 3
SUPERCELL = (2,2,1)
# ----



dynmat = CC.Phonons.Phonons(FILDYN, NQIRR)

# Test the symmetrization
qe_sym = CC.symmetries.QE_Symmetry(dynmat.structure)

fc_dynmat_start = np.array(dynmat.dynmats)


after_sym = fc_dynmat_start.copy()
qe_sym.SymmetrizeFCQ(after_sym, np.array(dynmat.q_stars))

# Print the difference between before and after the symmetrization
print ""
print "Difference of the symmetrization:",
print np.sqrt( np.sum( (after_sym - fc_dynmat_start)**2 ) / np.sum(after_sym*fc_dynmat_start))

print ""

# Now lets try to randomize the matrix
new_random = np.random.uniform( size = np.shape(fc_dynmat_start)) + 1j*np.random.uniform( size = np.shape(fc_dynmat_start))

print "Saving a not symmetrized random matrix to Random.dyn.IQ, where IQ is the q index"
# Lets save the new matrix in QE format
for i, q in enumerate(dynmat.q_tot):
    dynmat.dynmats[i] = new_random[i, :, :]
dynmat.save_qe("Random.dyn.")

# Lets constrain the symmetries
# We use asr = crystal to force the existence of the acustic modes in Gamma
qe_sym.SymmetrizeFCQ(new_random, np.array(dynmat.q_stars), asr = "no")

# Lets save the new matrix in QE format
for i, q in enumerate(dynmat.q_tot):
    dynmat.dynmats[i] = new_random[i, :, :]

print "Saving a symmetrized random matrix to Sym.dyn.IQ, where IQ is the q index"
dynmat.save_qe("Sym.dyn.")
print ""

# Compute the frequencies
supercell_dyn = dynmat.GenerateSupercellDyn(SUPERCELL)
w, pols = supercell_dyn.DyagDinQ(0)
# Get the translations
t = CC.Methods.get_translations(pols, supercell_dyn.structure.get_masses_array())

print "Frequencies:"
print "\n".join(["%.4f cm-1   T: %d" % (w[i]*CC.Phonons.RY_TO_CM, t[i]) for i in range(len(w))])
print ""
print "Done."